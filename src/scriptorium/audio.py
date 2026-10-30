"""Voz local (Kokoro en la GPU) y productos de audio."""

from __future__ import annotations

import hashlib
import json
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
    if titulo:
        # «Capítulo I. Algo» -> «Capítulo uno. Algo»; «II - Algo» -> «Dos. Algo»
        def romano(m: re.Match) -> str:
            n = _romano_a_entero(m.group(2))
            return f"{m.group(1)}{_numero(n)}" if n else m.group(0)

        texto = re.sub(r"^((?:cap[ií]tulo|parte|libro)\s+)?([IVXLCDM]+)\b", romano, texto, flags=re.I)
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


class Voz:
    """Kokoro-82M en la GPU, con caché en disco para no regenerar lo ya dicho."""

    def __init__(self, ajustes: Ajustes):
        self.ajustes = ajustes
        self.cache = config.TRABAJO / "tts"
        self.cache.mkdir(parents=True, exist_ok=True)
        self._pipeline = None

    def __enter__(self) -> "Voz":
        return self

    def __exit__(self, *exc) -> None:
        if self._pipeline is not None:
            import torch

            del self._pipeline
            self._pipeline = None
            torch.cuda.empty_cache()

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
        velocidad = velocidad or self.ajustes.velocidad_voz
        clave = hashlib.sha1(f"{voz}|{velocidad}|es-419|{texto}".encode()).hexdigest()
        archivo = self.cache / f"{clave}.npy"
        if archivo.exists():
            try:
                return np.load(archivo)
            except (EOFError, ValueError, OSError):  # quedó a medio escribir: se regenera
                archivo.unlink()
        piezas = []
        for trozo in trozos(texto):
            for resultado in self.pipeline(trozo, voice=voz, speed=velocidad, split_pattern=None):
                a = resultado.audio if hasattr(resultado, "audio") else resultado[2]
                if a is not None:
                    piezas.append(a.detach().cpu().numpy() if hasattr(a, "detach") else np.asarray(a))
            piezas.append(silencio(0.12))
        audio = np.concatenate(piezas).astype(np.float32) if piezas else silencio(0.1)
        temporal = archivo.with_suffix(".tmp.npy")  # escritura atómica: un corte no deja basura
        np.save(temporal, audio)
        temporal.replace(archivo)
        return audio


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


def audiolibro(voz: Voz, obra: Obra, avisar: Callable[[str], None]) -> None:
    """Nivel 0: el texto tal cual, con capítulos y tiempos por párrafo (para el lector sincronizado)."""
    carpeta = obra.derivados / "audio"
    piezas, tiempos, capitulos, t = [], {}, [], 0.0
    titulo = f"{obra.meta['titulo']}. {obra.meta.get('autor', '')}"
    for audio in (voz.decir(para_voz(titulo)), silencio(1.0)):
        piezas.append(audio)
        t += len(audio) / TASA
    total = len(obra.bloques)
    for i, b in enumerate(obra.bloques, 1):
        if i % 10 == 0:
            avisar(f"audiolibro · {i}/{total} bloques")
        texto = para_voz(b.texto, titulo=b.tipo == "titulo")
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
    if forzar or not (carpeta / "audiolibro.m4b").exists():
        audiolibro(voz, obra, avisar)
    if not derivados:
        return
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
    for clave, (titulo, nivel, frases) in productos.items():
        destino = carpeta / f"{clave}.mp3"
        if destino.exists() and not forzar:
            continue
        avisar(f"audio · {clave}")
        audio = np.concatenate([voz.decir(para_voz(intro)), silencio(0.6)] + [_secuencia(voz, frases(d)) for d in derivados])
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
