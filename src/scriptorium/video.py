"""Video de motion graphics: guion fiel -> director (LLM) -> voz -> render con Remotion.

El LLM local nunca escribe código: solo elige escenas del kit y sus textos (JSON).
Las citas que aparecen en pantalla se verifican carácter por carácter contra el original.
"""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Callable

import soundfile as sf

from . import config, publicar
from . import verificacion as ver
from .alineacion import Alineador, emparejar, norma, palabras_perdidas
from .audio import TASA, Voz, para_voz
from .config import Ajustes
from .ingesta import Obra
from .llm import LLM, TEXTO, lista, objeto

TIPOS = ["Cita", "Concepto", "Lista", "Contraste", "Argumento", "PalabraClave", "Pregunta", "Respiro"]
ACENTOS = ["oro", "azul", "verde", "oro", "violeta", "rojo"]
NIVEL = "Nivel 2 · Explicativo fiel"
# Pictogramas que el kit sabe dibujar (nombre en español -> ícono de Lucide); el director solo elige de aquí.
ICONOS = list(json.loads((config.KIT_VIDEO / "src" / "iconos.json").read_text(encoding="utf-8")))

CATALOGO = """Catálogo de escenas del kit (elige UNA por segmento):
- Cita: muestra una CITA TEXTUAL del autor. «cuerpo» = fragmento copiado EXACTAMENTE de los párrafos originales (máximo 35 palabras). «resaltar» = 1 a 3 palabras de la cita.
- Concepto: un término y su sentido. «titular» = el término (máximo 4 palabras); «cuerpo» = definición breve con palabras del autor (máximo 25 palabras).
- Lista: varias ideas paralelas. «titular» (máximo 7 palabras) e «items» (de 2 a 5, máximo 8 palabras cada uno).
- Contraste: dos ideas opuestas. «izquierda_titulo», «izquierda_texto», «derecha_titulo», «derecha_texto» (títulos de máximo 4 palabras; textos de máximo 16).
- Argumento: razones que llevan a una conclusión. «items» = de 2 a 4 premisas (máximo 12 palabras cada una); «cuerpo» = la conclusión (máximo 18 palabras).
- PalabraClave: una palabra o expresión central. «titular» = de 1 a 3 palabras; «cuerpo» = frase breve (máximo 16 palabras).
- Pregunta: el segmento plantea una pregunta. «titular» = la pregunta (máximo 18 palabras).
- Respiro: pausa visual para una imagen o metáfora del autor. «titular» = máximo 6 palabras.
Reglas: no repitas el mismo tipo en dos segmentos seguidos; usa al menos 5 tipos distintos; los textos en pantalla son \
breves y usan las palabras del autor; no inventes nada que no esté en el segmento o en los párrafos originales. \
Deja vacíos ("" o []) los campos que el tipo elegido no usa.
Además, cada escena puede llevar un «icono»: un pictograma decorativo que se dibuja trazo a trazo. Úsalo sobre \
todo en Concepto, PalabraClave, Lista y Respiro, y solo si representa bien la idea o una imagen que usa el autor \
(p. ej. «ojo» para mirar, «balanza» para juzgar, «cámara» para un daguerrotipo). Elígelo SOLO de esta lista; \
si ninguno encaja, deja «icono» vacío: """ + ", ".join(ICONOS) + "."

ESQUEMA = objeto(
    escenas=lista(
        objeto(
            n={"type": "integer"},
            tipo={"type": "string", "enum": TIPOS},
            titular=TEXTO,
            cuerpo=TEXTO,
            items=lista(TEXTO),
            izquierda_titulo=TEXTO,
            izquierda_texto=TEXTO,
            derecha_titulo=TEXTO,
            derecha_texto=TEXTO,
            resaltar=lista(TEXTO),
            icono={"type": "string", "enum": ["", *ICONOS]},
        )
    )
)

SISTEMA = """Eres el director de arte de videos educativos de humanidades hechos con motion graphics. \
Para cada segmento de narración eliges la escena del kit que mejor muestra la idea y escribes los textos breves \
que aparecerán en pantalla. Eres fiel al texto del autor: no añades información."""


def _cortar(texto: str, n: int) -> str:
    """Recorta a `n` palabras; si hay que cortar, lo hace en la última pausa natural (coma, punto y coma…)."""
    palabras = (texto or "").split()
    if len(palabras) <= n:
        return " ".join(palabras)
    recorte = " ".join(palabras[:n])
    pausa = max(recorte.rfind(c) for c in ",;:.")
    if pausa > len(recorte) * 0.5:
        return recorte[:pausa].rstrip(" ,;:") + "…"
    return recorte + "…"


def _ventana_de_cita(cita: str, narracion: str) -> list[float]:
    """Fracción de la narración en la que se pronuncia la cita, para iluminarla a la vez que la voz."""
    norma = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", s.lower())).strip()
    n, c = norma(narracion), norma(cita)
    inicio = n.find(" ".join(c.split()[:4]))
    if not n or inicio < 0:
        return [0.05, 0.92]
    fin = min(len(n), inicio + len(c))
    return [round(inicio / len(n), 3), round(max(fin / len(n), inicio / len(n) + 0.2), 3)]


def _carpeta(obra: Obra) -> Path:
    return obra.derivados / "video"


def _trabajo(obra: Obra, cap: int) -> Path:
    return config.TRABAJO / "video" / obra.slug / f"cap{cap}"


# ---------------------------------------------------------------- 1. director (LLM)


def _normalizar(escena: dict, segmento: dict, obra: Obra, citas: list[dict]) -> dict:
    tipo = escena.get("tipo") if escena.get("tipo") in TIPOS else "Concepto"
    titular = _cortar(escena.get("titular", ""), 18)
    cuerpo = escena.get("cuerpo", "").strip()
    items = [_cortar(i, 12) for i in escena.get("items", []) if i.strip()][:5]
    izq = {"titulo": _cortar(escena.get("izquierda_titulo", ""), 4), "texto": _cortar(escena.get("izquierda_texto", ""), 18)}
    der = {"titulo": _cortar(escena.get("derecha_titulo", ""), 4), "texto": _cortar(escena.get("derecha_texto", ""), 18)}
    anclas = segmento["anclas"]

    if tipo == "Cita":
        literal = ver.localizar_literal(cuerpo, obra, anclas[0] if anclas else None) if cuerpo else None
        if literal and len(cuerpo.split()) <= 45:
            anclas = [literal] + [a for a in anclas if a != literal]
        else:  # nunca mostrar como cita algo que no está en el original
            alternativa = next((c for c in citas if c["ancla"] in anclas), None)
            if alternativa:
                cuerpo, anclas = alternativa["cita"], [alternativa["ancla"]] + [a for a in anclas if a != alternativa["ancla"]]
            else:
                tipo = "PalabraClave"
                titular = titular if 0 < len(titular.split()) <= 3 else (escena.get("resaltar") or ["Idea"])[0]
                cuerpo = _cortar(segmento["texto"], 16)
    if tipo == "Lista" and len(items) < 2:
        tipo = "Concepto"
    if tipo == "Argumento" and (len(items) < 2 or not cuerpo):
        tipo = "Lista" if len(items) >= 2 else "Concepto"
    if tipo == "Lista" and not titular:  # mejor sin titular («N ideas» encabeza) que un fragmento cortado
        primera = re.split(r"(?<=[.?!])\s+", segmento["texto"])[0].rstrip(".")
        titular = (escena.get("resaltar") or [""])[0] or (primera if len(primera.split()) <= 7 else "")
    if tipo == "Contraste" and not (izq["titulo"] and der["titulo"]):
        tipo = "Concepto"
    if tipo == "Pregunta" and not titular:
        preguntas = [o for o in re.split(r"(?<=[.?!])\s+", segmento["texto"]) if o.strip().endswith("?")]
        if preguntas:
            titular = _cortar(preguntas[0], 18)
        else:
            tipo, titular = "PalabraClave", ""
    if tipo in ("Concepto", "PalabraClave") and not titular:
        titular = (escena.get("resaltar") or [""])[0] or _cortar(segmento["texto"], 3)
    if tipo == "Concepto" and not cuerpo:
        cuerpo = _cortar(segmento["texto"], 25)
    if tipo == "Respiro" and not titular:
        titular = _cortar(segmento["texto"], 6)

    limites = {"Cita": 45, "Concepto": 28, "Argumento": 20, "PalabraClave": 22}
    return {
        "tipo": tipo,
        "revelar": _ventana_de_cita(cuerpo, segmento["texto"]) if tipo == "Cita" else [0.05, 0.92],
        "narracion": segmento["texto"],
        "anclas": anclas,
        "titular": titular,
        "cuerpo": cuerpo if tipo == "Cita" else _cortar(cuerpo, limites.get(tipo, 25)),
        "items": items[:4] if tipo == "Argumento" else items,
        "izquierda": izq,
        "derecha": der,
        "resaltar": [r for r in escena.get("resaltar", []) if r.strip()][:3],
        "icono": escena.get("icono") if escena.get("icono") in ICONOS else "",
    }


def dirigir(llm: LLM, obra: Obra, derivados: list[dict], forzar: bool, avisar: Callable[[str], None]) -> None:
    carpeta = _carpeta(obra)
    carpeta.mkdir(parents=True, exist_ok=True)
    por_id = obra.por_id()
    for d in derivados:
        plan_archivo = carpeta / f"plan_cap{d['capitulo']}.json"
        if plan_archivo.exists() and not forzar:
            continue
        avisar(f"cap. {d['capitulo']} · director de video")
        segmentos = d["guion_video"]["segmentos"]
        bloques = []
        for i, s in enumerate(segmentos):
            originales = "\n".join(f"    [§{a}] {por_id[a].texto}" for a in s["anclas"] if a in por_id)
            bloques.append(f"SEGMENTO {i}: {s['texto']}\n  PÁRRAFOS ORIGINALES:\n{originales}")
        citas = d["citas"]["citas"]
        citas_txt = "\n".join(f"- «{c['cita']}» [§{c['ancla']}]" for c in citas)
        usuario = f"{CATALOGO}\n\nCITAS VERIFICADAS DISPONIBLES:\n{citas_txt}\n\n" + "\n\n".join(bloques)
        datos = llm.json(SISTEMA, usuario, ESQUEMA, temperatura=0.4)
        elegidas = {e.get("n"): e for e in datos.get("escenas", [])}
        escenas = [_normalizar(elegidas.get(i, {}), s, obra, citas) for i, s in enumerate(segmentos)]
        plan = {"capitulo": d["capitulo"], "titulo_capitulo": d["titulo"], "escenas": escenas}
        plan_archivo.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
        avisar("escenas: " + ", ".join(e["tipo"] for e in escenas))


# ---------------------------------------------------------------- 2. voz por segmento y sincronía real
#
# Regla: lo que se ilumina palabra por palabra en pantalla es exactamente lo que dice la voz, en el
# cuadro en que lo dice (alineación forzada). Lo que no se dice aparece completo, sin «karaoke».


def _con_cita_literal(narracion: str, cita: str, autor: str) -> str:
    """La voz lee la cita tal cual: las oraciones que la parafrasean se sustituyen por la cita."""
    pares = emparejar(cita.split(), narracion.split())
    if all(p is not None for p in pares):
        return narracion  # ya la dice palabra por palabra (una cita no admite «casi»)
    contenido = lambda s: {norma(p) for p in s.split() if len(norma(p)) > 3}
    de_la_cita = contenido(cita)
    oraciones = re.split(r"(?<=[.?!])\s+", narracion.strip())
    parafrasis = [o for o in oraciones if contenido(o) and len(contenido(o) & de_la_cita) / len(contenido(o)) >= 0.5]
    lectura = f"Como escribe {autor or 'el autor'}: «{cita.strip().rstrip('.,;: ')}»."
    if not parafrasis:
        return f"{narracion.strip()} {lectura}"
    salida = []
    for o in oraciones:
        if o is parafrasis[0]:
            salida.append(lectura)
        elif o not in parafrasis:
            salida.append(o)
    return " ".join(salida)


def _rellenar(cuadros: list[int | None], inicio: int, fin: int) -> list[int]:
    """Interpola los huecos (palabras sin tiempo) entre sus vecinas conocidas."""
    salida = list(cuadros)
    conocidos = [(-1, inicio)] + [(i, c) for i, c in enumerate(cuadros) if c is not None] + [(len(cuadros), fin)]
    for (i0, c0), (i1, c1) in zip(conocidos, conocidos[1:]):
        for k in range(i0 + 1, i1):
            salida[k] = int(round(c0 + (c1 - c0) * (k - i0) / (i1 - i0)))
    return salida


def _momento(texto: str, narr: list[str], desde: int = 0) -> int | None:
    """Índice de la palabra de la narración donde empieza a decirse la idea de `texto`."""
    clave = {norma(p) for p in texto.split() if len(norma(p)) > 3}
    largo = len(texto.split()) + 6
    mejor, pos = 0, None
    for k in range(desde, len(narr)):
        if narr[k] in clave:
            puntos = len(clave & set(narr[k : k + largo]))
            if puntos > mejor:
                mejor, pos = puntos, k
    return pos


def _sincronizar(e: dict, dichas: list[str], tiempos: list[dict | None], fps: int) -> None:
    """Cuadros reales de cada palabra narrada y de cada elemento en pantalla (en cuadros de la escena)."""
    cuadro = lambda s: int(round(s * fps))
    fin_voz = max(e["voz"] - 4, 8)
    inicios = _rellenar([cuadro(t["inicio"]) if t else None for t in tiempos], 2, fin_voz)
    finales = [cuadro(t["fin"]) if t else None for t in tiempos]
    mostradas = e["narracion"].split()
    pares = emparejar(mostradas, dichas)
    ini = _rellenar([inicios[j] if j is not None else None for j in pares], 2, fin_voz)
    fin = [finales[j] if j is not None and finales[j] else (ini[k + 1] if k + 1 < len(ini) else fin_voz) for k, j in enumerate(pares)]
    e["palabras"] = [[p, a, b] for p, a, b in zip(mostradas, ini, fin)]

    # Subtítulos por frases: corte al cerrar oración, en comas o a las 12 palabras, sin dejar sueltos
    # los finales de frase de menos de 4 palabras.
    cierra = [bool(re.search(r"[.?!;:»]$", p)) for p in mostradas]
    bloques, desde = [], 0
    for k, p in enumerate(mostradas):
        n = k + 1 - desde
        resto = next((j for j in range(k + 1, len(mostradas)) if cierra[j]), len(mostradas) - 1) - k
        if k == len(mostradas) - 1 or cierra[k] or n >= 16 or (resto > 3 and (n >= 12 or (n >= 6 and p.endswith(",")))):
            bloques.append([desde, k + 1])
            desde = k + 1
    e["subtitulos"] = bloques

    narr = [norma(p) for p in mostradas]

    def karaoke(texto: str) -> list[int] | None:
        palabras = texto.split()
        enlazadas = emparejar(palabras, mostradas)
        if not palabras or sum(j is not None for j in enlazadas) < 0.9 * len(palabras):
            return None  # no es lo que dice la voz: se muestra completo, sin iluminar palabra por palabra
        return _rellenar([ini[j] if j is not None else None for j in enlazadas], 6, fin_voz)

    def cuando(texto: str, desde: int = 0) -> tuple[int | None, int]:
        pos = _momento(texto, narr, desde)
        return (ini[pos], pos) if pos is not None else (None, desde)

    aparece: dict = {}
    texto_principal = e["titular"] if e["tipo"] == "Pregunta" else e["cuerpo"]
    if e["tipo"] in ("Cita", "Concepto", "PalabraClave", "Pregunta") and texto_principal:
        e["tiempos_texto"] = karaoke(texto_principal)
        aparece["texto"] = max(10, cuando(texto_principal)[0] or 14)
    if e["tipo"] in ("Lista", "Argumento"):
        momentos, pos = [], 0
        for item in e["items"]:
            c, pos = cuando(item, pos)
            momentos.append(c)
        momentos = _rellenar(momentos, 8, int(fin_voz * 0.85))
        for k in range(1, len(momentos)):  # en orden y con aire entre uno y otro
            momentos[k] = max(momentos[k], momentos[k - 1] + 10)
        aparece["items"] = [max(6, m - 6) for m in momentos]
        if e["tipo"] == "Argumento":
            c, _ = cuando(e["cuerpo"], pos)
            aparece["texto"] = max(aparece["items"][-1] + 20 if momentos else 20, (c or int(fin_voz * 0.6)) - 6)
    if e["tipo"] == "Contraste":
        c1, p1 = cuando(f"{e['izquierda']['titulo']} {e['izquierda']['texto']}")
        c2, _ = cuando(f"{e['derecha']['titulo']} {e['derecha']['texto']}", p1 + 1)
        aparece["izquierda"] = max(4, (c1 or 4) - 6)
        aparece["derecha"] = max(aparece["izquierda"] + 20, (c2 or int(fin_voz * 0.45)) - 6)
    e["aparece"] = aparece


def narrar(voz: Voz, obra: Obra, forzar: bool, avisar: Callable[[str], None]) -> None:
    fps = voz.ajustes.video_fps
    for plan_archivo in sorted(_carpeta(obra).glob("plan_cap*.json")):
        _narrar_capitulo(voz, voz.alineador, obra, plan_archivo, fps, forzar, avisar)


def _narrar_capitulo(voz: Voz, alineador: Alineador, obra: Obra, plan_archivo: Path, fps: int, forzar: bool, avisar: Callable[[str], None]) -> None:
    plan = json.loads(plan_archivo.read_text(encoding="utf-8"))
    trabajo = _trabajo(obra, plan["capitulo"])
    props_archivo = trabajo / "props.json"
    if props_archivo.exists() and not forzar:
        return
    publico = trabajo / "public"
    publico.mkdir(parents=True, exist_ok=True)
    avisar(f"cap. {plan['capitulo']} · voz del video ({len(plan['escenas'])} segmentos)")
    autor = obra.meta.get("autor", "")
    intro = f"{obra.meta['titulo']}, de {autor}. " if autor else f"{obra.meta['titulo']}. "
    portada = {"tipo": "Portada", "revelar": [0.05, 0.92], "narracion": intro + para_voz(plan["titulo_capitulo"], titulo=True), "anclas": [],
               "titular": "", "cuerpo": "", "items": [], "izquierda": {"titulo": "", "texto": ""},
               "derecha": {"titulo": "", "texto": ""}, "resaltar": []}
    cierre = {**portada, "tipo": "Cierre", "narracion": ""}
    escenas = []
    for i, e in enumerate([portada, *plan["escenas"], cierre]):
        e = {**e, "acento": ACENTOS[i % len(ACENTOS)], "semilla": i + 1, "audio": None}
        if e["tipo"] == "Cita" and e["cuerpo"]:
            e["narracion"] = _con_cita_literal(e["narracion"], e["cuerpo"], autor)
        if e["narracion"]:
            dicho = para_voz(e["narracion"])
            audio = voz.decir(dicho)
            nombre = f"seg_{i:02d}.wav"
            sf.write(publico / nombre, audio, TASA, subtype="PCM_16")
            e["audio"] = nombre
            e["voz"] = math.ceil(len(audio) / TASA * fps)
            e["duracion"] = e["voz"] + int(fps * (1.1 if e["tipo"] == "Portada" else 0.55))
            tiempos, oido = alineador.analizar(audio, TASA, dicho.split())
            _sincronizar(e, dicho.split(), tiempos, fps)
            perdidas, faltan, sobran = palabras_perdidas(dicho, oido)
            if perdidas > 0.15:  # la voz sintética se comió o cambió palabras
                avisar(f"[yellow]segmento {i}: no se oye el {perdidas:.0%} del texto (faltan: {' '.join(faltan[:8])}; se oye: {' '.join(sobran[:8])})")
        else:
            e["voz"] = 0
            e["duracion"] = int(fps * 5)
        escenas.append(e)
    props = {
        "titulo": obra.meta["titulo"],
        "autor": autor,
        "capitulo": plan["titulo_capitulo"],
        "nivel": NIVEL,
        "escenas": escenas,
    }
    props_archivo.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    total = sum(e["duracion"] for e in escenas) / fps
    avisar(f"video cap. {plan['capitulo']}: {total / 60:.1f} min de duración")


# ---------------------------------------------------------------- 3. render


def renderizar(obra: Obra, ajustes: Ajustes, forzar: bool, avisar: Callable[[str], None]) -> None:
    carpeta = _carpeta(obra)
    entorno = {**os.environ, "PATH": f"{Path.home() / '.local/bin'}:{os.environ.get('PATH', '')}"}
    for plan_archivo in sorted(carpeta.glob("plan_cap*.json")):
        cap = json.loads(plan_archivo.read_text(encoding="utf-8"))["capitulo"]
        trabajo = _trabajo(obra, cap)
        destino = carpeta / f"explicador_cap{cap}.mp4"
        if destino.exists() and not forzar:
            continue
        if not (trabajo / "props.json").exists():
            avisar(f"cap. {cap}: falta la voz del video; corre la etapa de audio")
            continue
        avisar(f"cap. {cap} · renderizando a {ajustes.video_fps} fps (CPU, {ajustes.video_hilos} hilos)")
        temporal = trabajo / "explicador.mp4"
        inicio = time.time()
        subprocess.run(
            [
                "npx", "remotion", "render", "src/index.ts", "Explicador", str(temporal),
                f"--props={trabajo / 'props.json'}", f"--public-dir={trabajo / 'public'}",
                f"--concurrency={ajustes.video_hilos}", "--crf=20", "--log=error",
            ],
            cwd=config.KIT_VIDEO, env=entorno, check=True,
        )
        shutil.copyfile(temporal, destino)
        props = json.loads((trabajo / "props.json").read_text(encoding="utf-8"))
        duracion = sum(e["duracion"] for e in props["escenas"]) / ajustes.video_fps
        avisar(f"render: {duracion / 60:.1f} min de video en {(time.time() - inicio) / 60:.1f} min")
        publicar.registrar(obra, f"video_cap{cap}", destino, 2, f"Video explicador · {props['capitulo']}", "video")
