"""Prueba de fidelidad entre modelos: gana el que mejor respeta el texto, no el más «creativo»."""

from __future__ import annotations

import time
from pathlib import Path

from . import config, textos
from . import verificacion as ver
from .ingesta import Obra
from .llm import LLM


def comparar(slug: str, modelos: list[str], avisar) -> Path:
    ajustes = config.cargar_ajustes()
    obra = Obra.cargar(slug)
    cap = obra.capitulos()[0]
    bloque = textos._bloques(obra, cap, ajustes.palabras_por_bloque)[0]
    filas = []
    for modelo in modelos:
        llm = LLM(ajustes, modelo)
        if not llm.disponible():
            avisar(f"{modelo}: no está instalado en Ollama, lo salto")
            continue
        avisar(f"probando {modelo}")
        inicio = time.time()
        res = {t: textos._pedir(llm, obra, t, bloque) for t in ("resumen", "citas", "glosario", "esquema")}
        segundos = time.time() - inicio
        velocidad = llm.tokens / llm.segundos if llm.segundos else 0
        llm.descargar()

        citas = res["citas"].get("citas", [])
        citas_ok = sum(1 for c in citas if ver.localizar_literal(c["cita"], obra, c.get("ancla")))
        defs = res["glosario"].get("terminos", [])
        defs_ok = sum(1 for t in defs if ver.localizar_literal(t["definicion_literal"], obra, t.get("ancla")))
        r, e = res["resumen"], res["esquema"]
        afirmaciones = [r["una_linea"], r["parrafo"], *r.get("pagina", []), e["tesis"], *e.get("premisas", []), e["conclusion"]]
        for a in afirmaciones:
            a["anclas"] = ver.limpiar_anclas(a.get("anclas", []), obra)
        filas.append({"modelo": modelo, "segundos": segundos, "velocidad": velocidad, "citas": (citas_ok, len(citas)),
                      "defs": (defs_ok, len(defs)), "afirmaciones": afirmaciones})

    juez = LLM(ajustes, ajustes.modelo_juez)
    for f in filas:
        avisar(f"juzgando a {f['modelo']} con {juez.modelo}")
        veredictos = ver.juzgar(juez, obra, [{"texto": a["texto"], "anclas": a["anclas"]} for a in f["afirmaciones"]])
        f["clases"] = {c: sum(1 for v in veredictos if v["clase"] == c) for c in ver.CLASES}
        n = len(veredictos) or 1
        f["fieles"] = (f["clases"]["literal"] + f["clases"]["parafrasis_fiel"]) / n
        f["con_ancla"] = sum(1 for a in f["afirmaciones"] if a["anclas"]) / n
    juez.descargar()

    lineas = [
        f"# Prueba de fidelidad entre modelos — {obra.meta['titulo']}", "",
        f"Texto de prueba: {len(bloque.split())} palabras. Juez: `{juez.modelo}` (local). Las citas se comprueban con código.", "",
        "| Modelo | Tiempo | Velocidad | Citas literales | Definiciones literales | Afirmaciones fieles | Con ancla | Añadidos | Contradicciones |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for f in filas:
        lineas.append(
            f"| `{f['modelo']}` | {f['segundos']:.0f} s | {f['velocidad']:.0f} tok/s | {f['citas'][0]}/{f['citas'][1]} | "
            f"{f['defs'][0]}/{f['defs'][1]} | {f['fieles']:.0%} | {f['con_ancla']:.0%} | {f['clases']['añadido']} | {f['clases']['contradiccion']} |"
        )
    if filas:
        mejor = max(filas, key=lambda f: (f["fieles"], f["citas"][0] / max(1, f["citas"][1]), -f["segundos"]))
        lineas += ["", f"**Recomendado:** `{mejor['modelo']}` (más afirmaciones fieles y citas literales).",
                   "Para cambiarlo, edita `modelo` en `D:\\Scriptorium\\ajustes.json`."]
    destino = config.DATOS / "comparacion_modelos.md"
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return destino
