"""Voz local (voces fijadas con VoxCPM2/Qwen3-TTS, o Kokoro) y productos de audio."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Callable

import numpy as np
import soundfile as sf

from . import config, publicar
from .config import Ajustes
from .ingesta import Obra, listar_obras

TASA = 24000
VOCES_ES = {"em_alex": "Alex (masculina)", "ef_dora": "Dora (femenina)", "em_santa": "Santa (masculina, grave)"}


# ---------------------------------------------------------------- texto para voz


def _romano_a_entero(s: str) -> int | None:
    valores = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if not s or any(c not in valores for c in s):
        return None
    total = 0
    for a, b in zip(s, s[1:] + " "):
        v = valores[a]
        total += -v if b in valores and valores[b] > v else v
    return total


def _numero(n: int) -> str:
    try:
        from num2words import num2words

        return num2words(n, lang="es")
    except Exception:
        return str(n)


def para_voz(texto: str, titulo: bool = False) -> str:
    texto = re.sub(r"\[§?[\d.,\s§]+\]", "", texto)  # anclas
    texto = texto.replace("§", "")

    def romano(m: re.Match) -> str:
        n = _romano_a_entero(m.group(2))
        if not n:
            return m.group(0)
        return f"{m.group(1)}{_numero(n)}" if m.group(1) else _numero(n).capitalize()

    # «Capítulo I» -> «Capítulo uno» en cualquier parte (un repaso empieza «Repaso. Capítulo I. …»).
    # El numeral, solo en mayúsculas: «la parte civil» no es la parte 153.
    texto = re.sub(r"\b((?i:cap[ií]tulo|parte|libro)\s+)([IVXLCDM]+)\b", romano, texto)
    if titulo:
        # «V. Algo» -> «Cinco. Algo»; «II - Algo» -> «Dos. Algo» (y «MI VIDA» se queda igual)
        texto = re.sub(r"^()([IVXLCDM]+)(?=\s*[.:\-–—]|\s*$)", romano, texto)
        texto = re.sub(r"^(\w+)\s+-\s+", lambda m: m.group(1).capitalize() + ". ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    if texto and texto[-1] not in ".?!:;»\"":
        texto += "."
    return texto


def trozos(texto: str, maximo: int = 220) -> list[str]:
    """Kokoro admite ~510 fonemas por llamada: partir en oraciones y, si hace falta, en comas."""
    oraciones = re.split(r"(?<=[.?!;:»])\s+", texto)
    salida, actual = [], ""
    for o in oraciones:
        partes = [o] if len(o) <= maximo else re.split(r"(?<=,)\s+", o)
        for parte in partes:
            if actual and len(actual) + len(parte) + 1 > maximo:
                salida.append(actual)
                actual = parte
            else:
                actual = f"{actual} {parte}".strip()
    if actual:
        salida.append(actual)
    return salida


# ---------------------------------------------------------------- motor de voz

INTENTOS = 3  # tomas por trozo si el reconocedor no oye parte del texto


def nivelar(audio: np.ndarray, rms_db: float = -20.0, pico: float = 0.89) -> np.ndarray:
    """Ganancia lineal (sin compresor, que es lo que satura): la parte con voz a -20 dBFS RMS y el pico
    nunca por encima de -1 dBFS. Así todos los segmentos y las dos voces suenan al mismo volumen.

    Antes se redondean los chasquidos: VoxCPM2 sin su tanh deja picos sueltos de ~0.3 ms hasta 20×
    el nivel de la voz (cresta de 28 dB), que obligarían a bajar todo. La voz natural casi no pasa de
    6× (en Qwen3, el 99.99 % de las muestras queda debajo), así que solo se toca lo que excede eso."""
    marco = TASA // 50
    n = len(audio) // marco * marco
    if not n:
        return audio
    energia = np.sqrt(np.mean(audio[:n].reshape(-1, marco) ** 2, axis=1))
    con_voz = energia[energia > energia.max() * 0.05]
    rms = float(np.sqrt(np.mean(con_voz**2))) if len(con_voz) else 0.0
    if rms < 1e-5:
        return audio
    umbral, tope = 6 * rms, 8 * rms
    magnitud = np.abs(audio)
    encima = magnitud > umbral
    if encima.any():
        audio = audio.copy()
        audio[encima] = np.sign(audio[encima]) * (umbral + (tope - umbral) * np.tanh((magnitud[encima] - umbral) / (tope - umbral)))
    return (audio * min(10 ** (rms_db / 20) / rms, pico / float(np.abs(audio).max()))).astype(np.float32)


def _recortar(audio: np.ndarray, margen: float = 0.05) -> np.ndarray:
    """Quita el silencio de los bordes que dejan los motores neuronales (las pausas las pone el producto)."""
    marco = TASA // 100
    n = len(audio) // marco
    if not n:
        return audio
    energia = np.sqrt(np.mean(audio[: n * marco].reshape(n, marco) ** 2, axis=1))
    activos = np.nonzero(energia > energia.max() * 0.02)[0]
    if not len(activos):
        return audio
    m = int(margen * TASA)
    return audio[max(activos[0] * marco - m, 0): min((activos[-1] + 1) * marco + m, len(audio))]


def _termina_de_golpe(audio: np.ndarray) -> bool:
    """El motor dejó de hablar a media palabra: una toma sana se apaga antes de terminar; una cortada
    acaba con la voz a pleno (en la caché, el último marco va de 0.9 a 1.4 del RMS contra < 0.1)."""
    marco = TASA // 100
    n = len(audio) // marco
    if n < 10:
        return False
    energia = np.sqrt(np.mean(audio[: n * marco].reshape(n, marco) ** 2, axis=1))
    voz = energia[energia > energia.max() * 0.05]
    return bool(energia[-1] > 0.3 * np.sqrt(np.mean(voz**2)))


class _Trabajador:
    """Un motor de voz en su propio venv, como proceso aparte que se queda cargado (`voz_trabajador.py`)."""

    def __init__(self, motor: str):
        python = config.ENTORNOS_VOZ / motor / "bin" / "python"
        if not python.exists():
            raise RuntimeError(f"Falta el motor de voz {motor}: corre herramientas_wsl/voces_instalar.sh {motor}")
        self.motor = motor
        self.registro = config.TRABAJO / f"voz_{motor}.log"
        self.salida = config.TRABAJO / f"voz_{motor}.npy"
        with open(self.registro, "a", encoding="utf-8") as registro:
            # -P: que la carpeta del script (con audio.py, config.py…) no tape módulos de las bibliotecas.
            self.proceso = subprocess.Popen(
                [str(python), "-P", str(Path(__file__).with_name("voz_trabajador.py")), motor],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=registro, text=True, encoding="utf-8",
                env={**os.environ, "HF_HUB_DOWNLOAD_TIMEOUT": "120", "PYTHONUNBUFFERED": "1"},
            )
        self._respuesta()  # espera a que el modelo termine de cargar

    def _respuesta(self) -> dict:
        linea = self.proceso.stdout.readline()
        if not linea:
            raise RuntimeError(f"El motor de voz {self.motor} se cerró; revisa {self.registro}")
        respuesta = json.loads(linea)
        if "error" in respuesta:
            raise RuntimeError(f"{self.motor}: {respuesta['error']} (detalle en {self.registro})")
        return respuesta

    def decir(self, texto: str, referencia: Path, texto_referencia: str, semilla: int, opciones: dict) -> np.ndarray:
        pedido = {"texto": texto, "referencia": str(referencia), "texto_referencia": texto_referencia,
                  "salida": str(self.salida), "semilla": semilla, "opciones": opciones}
        self.proceso.stdin.write(json.dumps(pedido, ensure_ascii=False) + "\n")
        self.proceso.stdin.flush()
        self._respuesta()
        return np.load(self.salida)

    def cerrar(self) -> None:
        if self.proceso.poll() is None:
            self.proceso.stdin.close()
            try:
                self.proceso.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.proceso.kill()


class Voz:
    """La voz de los productos, con caché en disco para no regenerar lo ya dicho.

    Una voz es una voz fijada de `voces/voces.json` —una referencia sintética que VoxCPM2 o Qwen3-TTS
    clonan en cada segmento, para que no cambie de un segmento a otro— o un nombre de Kokoro (em_alex).
    """

    def __init__(self, ajustes: Ajustes, avisar: Callable[[str], None] | None = None):
        self.ajustes = ajustes
        self.avisar = avisar or (lambda mensaje: None)
        self.cache = config.TRABAJO / "tts"
        self.cache.mkdir(parents=True, exist_ok=True)
        archivo = config.VOCES / "voces.json"
        self.fijadas: dict[str, dict] = json.loads(archivo.read_text(encoding="utf-8")) if archivo.exists() else {}
        self._huellas: dict[str, str] = {}
        self._trabajadores: dict[str, _Trabajador] = {}
        self._alineador = None
        self._pipeline = None

    def __enter__(self) -> "Voz":
        return self

    def __exit__(self, *exc) -> None:
        for trabajador in self._trabajadores.values():
            trabajador.cerrar()
        self._trabajadores.clear()
        if self._alineador is not None:
            self._alineador.__exit__()
            self._alineador = None
        if self._pipeline is not None:
            import torch

            del self._pipeline
            self._pipeline = None
            torch.cuda.empty_cache()

    @property
    def alineador(self):
        """wav2vec2 compartido: controla las voces clonadas y da los tiempos del video."""
        if self._alineador is None:
            from .alineacion import Alineador

            self._alineador = Alineador()
        return self._alineador

    @property
    def pipeline(self):
        if self._pipeline is None:
            import torch
            from kokoro import KPipeline

            dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
            self._pipeline = KPipeline(lang_code="e", repo_id="hexgrad/Kokoro-82M", device=dispositivo)
            try:  # español latinoamericano (seseo) en lugar del peninsular
                from misaki.espeak import EspeakG2P

                self._pipeline.g2p = EspeakG2P(language="es-419")
            except Exception:
                pass
        return self._pipeline

    def decir(self, texto: str, voz: str | None = None, velocidad: float | None = None) -> np.ndarray:
        voz = voz or self.ajustes.voz_narrador
        fijada = self.fijadas.get(voz)
        if fijada:  # la clave cambia si cambia la referencia o los ajustes del motor
            opciones = json.dumps(fijada.get("opciones", {}), sort_keys=True)
            clave = hashlib.sha1(f"{voz}|{fijada['motor']}|{self._huella(fijada)}|{opciones}|{texto}".encode()).hexdigest()
        else:
            velocidad = velocidad or self.ajustes.velocidad_voz
            clave = hashlib.sha1(f"{voz}|{velocidad}|es-419|{texto}".encode()).hexdigest()
        archivo = self.cache / f"{clave}.npy"
        if archivo.exists():
            try:
                return nivelar(np.load(archivo))
            except (EOFError, ValueError, OSError):  # quedó a medio escribir: se regenera
                archivo.unlink()
        audio = self._clonar(texto, fijada) if fijada else self._kokoro(texto, voz, velocidad)
        temporal = archivo.with_suffix(".tmp.npy")  # escritura atómica: un corte no deja basura
        np.save(temporal, audio)
        temporal.replace(archivo)
        return nivelar(audio)

    def preparar(self, pedidos: list[tuple[str, str | None]]) -> None:
        """Deja en la caché lo que se va a decir, agrupado por voz, para cargar cada motor una sola vez
        (un podcast alterna voces turno por turno). El narrador va al final: así queda cargado para lo
        que sigue (el video)."""
        por_voz: dict[str, list[str]] = {}
        for texto, voz in pedidos:
            if texto:
                por_voz.setdefault(voz or self.ajustes.voz_narrador, []).append(texto)
        for voz in sorted(por_voz, key=lambda v: v == self.ajustes.voz_narrador):
            textos = list(dict.fromkeys(por_voz[voz]))
            for i, texto in enumerate(textos, 1):
                if i % 10 == 0:
                    self.avisar(f"voz {voz} · {i}/{len(textos)}")
                self.decir(texto, voz)

    def _huella(self, fijada: dict) -> str:
        nombre = fijada["referencia"]
        if nombre not in self._huellas:
            self._huellas[nombre] = hashlib.sha1((config.VOCES / nombre).read_bytes()).hexdigest()[:12]
        return self._huellas[nombre]

    def _clonar(self, texto: str, fijada: dict) -> np.ndarray:
        """Trozo por trozo. Si el reconocedor no oye parte del texto (la voz se comió o cambió palabras),
        se repite con otra semilla y se queda la mejor toma: el audio debe decir lo que dice el texto."""
        from .alineacion import palabras_perdidas

        motor = fijada["motor"]
        if motor not in self._trabajadores:
            for otro in self._trabajadores.values():  # uno a la vez: dos motores no caben en la RAM de WSL
                otro.cerrar()
            self._trabajadores.clear()
            self.avisar(f"cargando la voz {motor}")
            self._trabajadores[motor] = _Trabajador(motor)
        trabajador = self._trabajadores[motor]
        piezas = []
        for trozo in trozos(texto, maximo=300):
            palabras = trozo.split()
            mejor = None
            for semilla in range(1, INTENTOS + 1):
                audio = _recortar(trabajador.decir(trozo, config.VOCES / fijada["referencia"], fijada["texto"], semilla, fijada.get("opciones", {})))
                _, oido = self.alineador.analizar(audio, TASA, palabras)
                perdidas, faltan, sobran = palabras_perdidas(trozo, oido)
                error = perdidas
                de_mas = len(sobran) - len(faltan)  # una palabra mal reconocida cuenta en las dos listas
                if de_mas >= 3:  # dijo de más (un motor neuronal puede seguir hablando solo)
                    error += de_mas / len(palabras)
                if len(audio) / TASA > 1.0 + 0.8 * len(palabras):  # demasiado largo para lo que dice
                    error = max(error, 1.0)
                cortada = _termina_de_golpe(audio)
                if cortada:  # el reconocedor apenas lo nota: falta media palabra
                    error = max(error, 0.5)
                if mejor is None or error < mejor[0]:
                    mejor = (error, audio, ["(cortada)"] * cortada + faltan + [f"+{p}" for p in sobran])
                if error <= 0.08:
                    break
            if mejor[0] > 0.15:
                self.avisar(f"[yellow]voz {motor}: tras {INTENTOS} tomas «{trozo[:60]}…» no coincide en un {min(mejor[0], 1):.0%} (faltan/sobran: {' '.join(mejor[2][:10])})")
            piezas += [mejor[1], silencio(0.15)]
        return np.concatenate(piezas).astype(np.float32) if piezas else silencio(0.1)

    def _kokoro(self, texto: str, voz: str, velocidad: float) -> np.ndarray:
        piezas = []
        for trozo in trozos(texto):
            for resultado in self.pipeline(trozo, voice=voz, speed=velocidad, split_pattern=None):
                a = resultado.audio if hasattr(resultado, "audio") else resultado[2]
                if a is not None:
                    piezas.append(a.detach().cpu().numpy() if hasattr(a, "detach") else np.asarray(a))
            piezas.append(silencio(0.12))
        return np.concatenate(piezas).astype(np.float32) if piezas else silencio(0.1)


def silencio(segundos: float) -> np.ndarray:
    return np.zeros(int(TASA * segundos), dtype=np.float32)


# ---------------------------------------------------------------- codificación


def codificar(audio: np.ndarray, destino: Path, capitulos: list[tuple[float, str]] | None = None) -> Path:
    """WAV temporal en disco Linux -> MP3 / M4B (con capítulos) en la carpeta de destino."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = config.TRABAJO / f"tmp_{destino.stem}.wav"
    sf.write(tmp, audio, TASA, subtype="PCM_16")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp)]
    if capitulos and destino.suffix == ".m4b":
        meta = config.TRABAJO / f"tmp_{destino.stem}.txt"
        duracion = len(audio) / TASA
        lineas = [";FFMETADATA1"]
        for i, (inicio, titulo) in enumerate(capitulos):
            fin = capitulos[i + 1][0] if i + 1 < len(capitulos) else duracion
            lineas += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(inicio * 1000)}", f"END={int(fin * 1000)}", f"title={titulo}"]
        meta.write_text("\n".join(lineas), encoding="utf-8")
        cmd += ["-i", str(meta), "-map_metadata", "1", "-map", "0:a"]
    if destino.suffix in (".m4b", ".m4a"):
        cmd += ["-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", "-f", "mp4"]
    else:
        cmd += ["-c:a", "libmp3lame", "-q:a", "5"]
    subprocess.run(cmd + [str(destino)], check=True)
    tmp.unlink(missing_ok=True)
    return destino


# ---------------------------------------------------------------- productos


def _dichos_audiolibro(obra: Obra) -> list[str]:
    """Lo que dice el audiolibro: el título y cada bloque tal cual."""
    titulo = f"{obra.meta['titulo']}. {obra.meta.get('autor', '')}"
    return [para_voz(titulo)] + [para_voz(b.texto, titulo=b.tipo == "titulo") for b in obra.bloques]


def audiolibro(voz: Voz, obra: Obra, avisar: Callable[[str], None]) -> None:
    """Nivel 0: el texto tal cual, con capítulos y tiempos por párrafo (para el lector sincronizado)."""
    carpeta = obra.derivados / "audio"
    piezas, tiempos, capitulos, t = [], {}, [], 0.0
    titulo, *dichos = _dichos_audiolibro(obra)
    for audio in (voz.decir(titulo), silencio(1.0)):
        piezas.append(audio)
        t += len(audio) / TASA
    total = len(obra.bloques)
    for i, (b, texto) in enumerate(zip(obra.bloques, dichos), 1):
        if i % 10 == 0:
            avisar(f"audiolibro · {i}/{total} bloques")
        if b.tipo == "titulo":
            capitulos.append((t, b.texto))
        audio = voz.decir(texto)
        pausa = silencio(0.9 if b.tipo == "titulo" else 0.55)
        tiempos[b.id] = [round(t, 2), round(t + len(audio) / TASA, 2)]
        piezas += [audio, pausa]
        t += (len(audio) + len(pausa)) / TASA
    completo = np.concatenate(piezas)
    codificar(completo, carpeta / "audiolibro.m4b", capitulos or [(0.0, obra.meta["titulo"])])
    codificar(completo, carpeta / "audiolibro.mp3")
    (carpeta / "tiempos.json").write_text(json.dumps(tiempos), encoding="utf-8")
    publicar.registrar(obra, "audiolibro", carpeta / "audiolibro.m4b", 0, "Audiolibro literal (.m4b con capítulos)", "audio")
    publicar.registrar(obra, "audiolibro_mp3", carpeta / "audiolibro.mp3", 0, "Audiolibro literal (.mp3)", "audio")
    avisar(f"audiolibro: {t / 60:.1f} min")


def _secuencia(voz: Voz, frases: list[tuple[str, str | None, float]]) -> np.ndarray:
    piezas = []
    for texto, nombre_voz, pausa in frases:
        if texto:
            piezas.append(voz.decir(para_voz(texto), nombre_voz))
        piezas.append(silencio(pausa))
    return np.concatenate(piezas)


def producir(voz: Voz, obra: Obra, derivados: list[dict], forzar: bool, avisar: Callable[[str], None]) -> None:
    carpeta = obra.derivados / "audio"
    a = voz.ajustes
    con_audiolibro = forzar or not (carpeta / "audiolibro.m4b").exists()
    autor = obra.meta.get("autor", "")
    intro = f"{obra.meta['titulo']}, de {autor}." if autor else f"{obra.meta['titulo']}."

    productos = {
        "audioguia": ("Audio-guía", 2, lambda d: [(f"Audio-guía. {d['titulo']}.", None, 0.8)]
                      + [(s["texto"], None, 0.6) for s in d["guion_audio"]["segmentos"]]),
        "podcast": ("Podcast a dos voces", 2, lambda d: [(f"{d['titulo']}.", a.voz_anfitrion, 0.6)]
                    + [(t["texto"], a.voz_anfitrion if t["voz"] == "anfitrion" else a.voz_narrador, 0.35)
                       for t in d["podcast"]["turnos"]]),
        "repaso": ("Repaso activo: pregunta, pausa y respuesta", 2, lambda d: [(f"Repaso. {d['titulo']}.", None, 0.8)]
                   + [x for q in d["quiz"]["preguntas"] for x in (
                       (q["pregunta"], a.voz_anfitrion, 4.0),
                       (f"Respuesta: {q['opciones'][q['correcta']]}. {q['explicacion']}", None, 1.2))]),
        "pildoras": ("Píldoras de conceptos con la definición del autor", 1, lambda d: [(f"Conceptos. {d['titulo']}.", None, 0.8)]
                     + [x for t in d["glosario"]["terminos"] for x in (
                         (t["termino"], a.voz_anfitrion, 0.5), (t["definicion_literal"], None, 1.4))]),
    }
    pendientes = {clave: [frases(d) for d in derivados] for clave, (_, _, frases) in productos.items()
                  if derivados and (forzar or not (carpeta / f"{clave}.mp3").exists())}
    # Todo lo que hay que decir, de una vez y agrupado por voz (cada motor se carga una sola vez).
    pedidos = [(texto, None) for texto in _dichos_audiolibro(obra)] if con_audiolibro else []
    if pendientes:
        pedidos.append((para_voz(intro), None))
    pedidos += [(para_voz(t), v) for secuencias in pendientes.values() for s in secuencias for t, v, _ in s if t]
    voz.preparar(pedidos)
    if con_audiolibro:
        audiolibro(voz, obra, avisar)
    for clave, secuencias in pendientes.items():
        titulo, nivel, _ = productos[clave]
        destino = carpeta / f"{clave}.mp3"
        avisar(f"audio · {clave}")
        audio = np.concatenate([voz.decir(para_voz(intro)), silencio(0.6)] + [_secuencia(voz, s) for s in secuencias])
        codificar(audio, destino)
        publicar.registrar(obra, clave, destino, nivel, titulo, "audio")


def cata_de_voces(ajustes: Ajustes) -> Path:
    """La misma página leída con cada voz, para elegir."""
    carpeta = config.DATOS / "cata_de_voces"
    carpeta.mkdir(parents=True, exist_ok=True)
    obras = listar_obras()
    if obras:
        obra = Obra.cargar(obras[0])
        muestra = " ".join(b.texto for b in obra.parrafos[:2])[:700]
    else:
        muestra = "El pensar bien consiste: o en conocer la verdad o en dirigir el entendimiento por el camino que conduce a ella."
    filas = []
    with Voz(ajustes) as voz:
        for nombre, fijada in voz.fijadas.items():
            archivo = carpeta / f"fijada_{nombre}.mp3"
            codificar(voz.decir(para_voz(muestra), nombre), archivo)
            filas.append(f"<tr><td>{fijada['descripcion']}</td><td>1.0×</td><td><audio controls preload='none' src='{archivo.name}'></audio></td><td><code>{nombre}</code></td></tr>")
        for nombre, descripcion in VOCES_ES.items():
            for velocidad in (1.0, 0.9):
                archivo = carpeta / f"kokoro_{nombre}_{int(velocidad * 100)}.mp3"
                codificar(voz.decir(para_voz(muestra), nombre, velocidad), archivo)
                filas.append(f"<tr><td>Kokoro · {descripcion}</td><td>{velocidad:.1f}×</td><td><audio controls preload='none' src='{archivo.name}'></audio></td><td><code>{nombre}</code></td></tr>")
    html = f"""<!doctype html><meta charset="utf-8"><title>Cata de voces</title>
<style>body{{font-family:Georgia,serif;max-width:900px;margin:40px auto;padding:0 16px;line-height:1.5}}td{{padding:8px 12px;border-bottom:1px solid #ddd}}code{{background:#f3f0e8;padding:2px 6px}}</style>
<h1>Cata de voces</h1><p>El mismo texto con cada voz. Para elegir, cambia <code>voz_narrador</code> y <code>voz_anfitrion</code> en <code>D:\\Scriptorium\\ajustes.json</code>.</p>
<blockquote>{muestra}</blockquote><table>{''.join(filas)}</table>"""
    (carpeta / "index.html").write_text(html, encoding="utf-8")
    return carpeta / "index.html"
