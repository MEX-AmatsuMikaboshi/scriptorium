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
from .audio import TASA, Voz, para_voz
from .config import Ajustes
from .ingesta import Obra
from .llm import LLM, TEXTO, lista, objeto

TIPOS = ["Cita", "Concepto", "Lista", "Contraste", "Argumento", "PalabraClave", "Pregunta", "Respiro"]
ACENTOS = ["oro", "azul", "verde", "oro", "violeta", "rojo"]
NIVEL = "Nivel 2 · Explicativo fiel"

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
Deja vacíos ("" o []) los campos que el tipo elegido no usa."""

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
    if tipo == "Lista" and not titular:
        titular = _cortar(re.split(r"(?<=[.?!])\s+", segmento["texto"])[0].rstrip("."), 7)
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


# ---------------------------------------------------------------- 2. voz por segmento


def narrar(voz: Voz, obra: Obra, forzar: bool, avisar: Callable[[str], None]) -> None:
    fps = voz.ajustes.video_fps
    for plan_archivo in sorted(_carpeta(obra).glob("plan_cap*.json")):
        plan = json.loads(plan_archivo.read_text(encoding="utf-8"))
        trabajo = _trabajo(obra, plan["capitulo"])
        props_archivo = trabajo / "props.json"
        if props_archivo.exists() and not forzar:
            continue
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
            if e["narracion"]:
                audio = voz.decir(para_voz(e["narracion"]))
                nombre = f"seg_{i:02d}.wav"
                sf.write(publico / nombre, audio, TASA, subtype="PCM_16")
                e["audio"] = nombre
                e["voz"] = math.ceil(len(audio) / TASA * fps)
                e["duracion"] = e["voz"] + int(fps * (1.1 if e["tipo"] == "Portada" else 0.55))
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
