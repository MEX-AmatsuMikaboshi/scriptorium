"""Escritura de productos legibles (Markdown) y del manifiesto de cada obra."""

from __future__ import annotations

import json
from pathlib import Path

from .ingesta import Obra

NIVELES = {
    0: "Nivel 0 · Literal: las mismas palabras en otro medio",
    1: "Nivel 1 · Estructural: palabras del autor, extraídas o reorganizadas",
    2: "Nivel 2 · Explicativo fiel: paráfrasis anclada a cada párrafo de origen",
    3: "Nivel 3 · Didáctico: añadidos marcados como tales",
}
AVISO = {"añadido": "⚠ añadido", "contradiccion": "⚠ contradicción", "inferencia": "≈ inferencia"}


def manifiesto(obra: Obra) -> dict:
    archivo = obra.derivados / "manifest.json"
    if archivo.exists():
        return json.loads(archivo.read_text(encoding="utf-8"))
    return {"slug": obra.slug, "meta": obra.meta, "productos": {}}


def registrar(obra: Obra, clave: str, ruta: Path, nivel: int, titulo: str, tipo: str) -> None:
    m = manifiesto(obra)
    m["meta"] = obra.meta
    m["productos"][clave] = {"ruta": str(ruta.relative_to(obra.derivados)), "nivel": nivel, "titulo": titulo, "tipo": tipo}
    obra.derivados.mkdir(parents=True, exist_ok=True)
    (obra.derivados / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")


def _anclas(item: dict) -> str:
    anclas = item.get("anclas") or ([item["ancla"]] if item.get("ancla") else [])
    return " " + " ".join(f"[§{a}]" for a in anclas) if anclas else ""


def _linea(item: dict) -> str:
    aviso = AVISO.get(item.get("fidelidad", {}).get("clase", ""), "")
    return f"{item['texto']}{_anclas(item)}" + (f" *({aviso}: {item['fidelidad']['motivo']})*" if aviso else "")


def escribir_textos(obra: Obra, derivados: list[dict]) -> None:
    carpeta = obra.derivados / "texto"
    carpeta.mkdir(parents=True, exist_ok=True)
    titulo = obra.meta["titulo"]
    autor = obra.meta.get("autor", "")

    def doc(nombre: str, encabezado: str, nivel: int, cuerpo: list[str]) -> Path:
        lineas = [f"# {encabezado} — {titulo}", f"*{autor}*" if autor else "", "", f"> {NIVELES[nivel]}", ""]
        ruta = carpeta / nombre
        ruta.write_text("\n".join(lineas + cuerpo) + "\n", encoding="utf-8")
        return ruta

    resumen, glosario, citas, esquema, preguntas, guiones, fidelidad = [], [], [], [], [], [], []
    for d in derivados:
        cap = f"## {d['titulo']}" if d.get("titulo") else ""
        r = d["resumen"]
        resumen += [cap, "### En una línea", _linea(r["una_linea"]), "", "### En un párrafo", _linea(r["parrafo"]), ""]
        resumen += ["### En una página"] + [f"- {_linea(p)}" for p in r["pagina"]] + [""]
        glosario += [cap] + [
            f"- **{t['termino']}**: «{t['definicion_literal']}» [§{t['ancla']}]" for t in d["glosario"]["terminos"]
        ] + [""]
        citas += [cap] + [f"> «{c['cita']}» [§{c['ancla']}]\n>\n> — {c['por_que']}\n" for c in d["citas"]["citas"]]
        e = d["esquema"]
        esquema += [cap, "**Tesis.** " + _linea(e["tesis"]), "", "**Premisas**"]
        esquema += [f"{i}. {_linea(p)}" for i, p in enumerate(e["premisas"], 1)]
        if e["objeciones"]:
            esquema += ["", "**Objeciones que el autor considera**"] + [f"- {_linea(o)}" for o in e["objeciones"]]
        esquema += ["", "**Conclusión.** " + _linea(e["conclusion"]), ""]
        preguntas += [cap] + [f"- {p['texto']}{_anclas(p)}" for p in d["preguntas"]["preguntas"]] + [""]
        guiones += [cap, "### Guion del video"] + [f"{i}. {_linea(s)}" for i, s in enumerate(d["guion_video"]["segmentos"], 1)]
        guiones += ["", "### Guion de la audio-guía"] + [f"{i}. {_linea(s)}" for i, s in enumerate(d["guion_audio"]["segmentos"], 1)]
        guiones += ["", "### Podcast a dos voces"] + [
            f"- **{'Anfitrión' if t['voz'] == 'anfitrion' else 'Especialista'}:** {_linea(t)}" for t in d["podcast"]["turnos"]
        ] + [""]
        f = d["fidelidad"]
        fidelidad += [cap, "### Juez de fidelidad (LLM local)"]
        fidelidad += [f"- {clase}: {n}" for clase, n in sorted(f.get("juez", {}).items())]
        fidelidad += ["", "### Citas y definiciones (verificación por código, carácter por carácter)"]
        fidelidad += [f"- Citas verificadas: {len(d['citas']['citas'])} · rechazadas: {len(f['citas_rechazadas'])}"]
        fidelidad += [f"- Definiciones verificadas: {len(d['glosario']['terminos'])} · rechazadas: {len(f['definiciones_rechazadas'])}"]
        fidelidad += [f"  - Rechazada: «{c['cita']}»" for c in f["citas_rechazadas"]]
        fidelidad += [f"  - Rechazada ({t['termino']}): «{t['definicion_literal']}»" for t in f["definiciones_rechazadas"]]
        if f.get("quiz_descartadas"):
            fidelidad += ["", "### Preguntas del quiz descartadas por el juez"] + [f"- {p}" for p in f["quiz_descartadas"]]
        if f.get("señaladas"):
            fidelidad += ["", "### Señaladas para revisión"] + [
                f"- [{s['producto']}] {s['texto']} — **{s['clase']}**: {s['motivo']}" for s in f["señaladas"]
            ]
        fidelidad += [""]

    productos = [
        ("resumen", "resumen.md", "Resumen con zoom", 2, resumen),
        ("glosario", "glosario.md", "Glosario del autor", 1, glosario),
        ("citas", "citas.md", "Citas clave verificadas", 1, citas),
        ("esquema", "esquema.md", "Esquema argumental", 2, esquema),
        ("preguntas", "preguntas.md", "Preguntas de reflexión", 3, preguntas),
        ("guiones", "guiones.md", "Guiones", 2, guiones),
        ("fidelidad", "fidelidad.md", "Informe de fidelidad", 1, fidelidad),
    ]
    for clave, nombre, encabezado, nivel, cuerpo in productos:
        ruta = doc(nombre, encabezado, nivel, cuerpo)
        registrar(obra, clave, ruta, nivel, encabezado, "texto")
