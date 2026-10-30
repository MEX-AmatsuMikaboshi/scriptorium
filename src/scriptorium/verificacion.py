"""Controles de fidelidad.

1. Citas y definiciones literales: se comprueban con código, sin IA.
2. Anclas: cada afirmación debe apuntar a párrafos que existen.
3. Juez (LLM local): clasifica cada oración derivada frente a sus párrafos de origen.
"""

from __future__ import annotations

import re
import unicodedata

from .ingesta import Obra
from .llm import LLM, TEXTO, lista, objeto

_COMILLAS = "\"'«»“”„‟‘’‚‛`´"


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto)
    texto = texto.replace("…", "...")
    texto = re.sub(f"[{re.escape(_COMILLAS)}]", "", texto)
    texto = re.sub(r"[‐‑‒–—―]", "-", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.casefold().strip(" .,;:-¡!¿?()")


def _fragmentos(cita: str) -> list[str]:
    partes = re.split(r"\s*(?:\[\s*\.\.\.\s*\]|\(\s*\.\.\.\s*\)|\.\.\.|…)\s*", cita)
    return [normalizar(p) for p in partes if len(normalizar(p)) > 3]


def _contiene_en_orden(parrafo: str, fragmentos: list[str]) -> bool:
    pos = 0
    for frag in fragmentos:
        i = parrafo.find(frag, pos)
        if i < 0:
            return False
        pos = i + len(frag)
    return True


def localizar_literal(texto: str, obra: Obra, ancla: str | None = None) -> str | None:
    """Devuelve el ID del párrafo que contiene `texto` literalmente, o None si no existe."""
    fragmentos = _fragmentos(texto)
    if not fragmentos:
        return None
    parrafos = obra.parrafos
    if ancla:
        parrafos = sorted(parrafos, key=lambda b: b.id != ancla)
    for b in parrafos:
        if _contiene_en_orden(normalizar(b.texto), fragmentos):
            return b.id
    return None


def limpiar_anclas(anclas: list[str], obra: Obra) -> list[str]:
    validos = obra.por_id()
    salida = []
    for a in anclas or []:
        a = a.strip().lstrip("§").strip("[] ")
        if a in validos and a not in salida:
            salida.append(a)
    return salida


# ---------------------------------------------------------------- juez de fidelidad

CLASES = ["literal", "parafrasis_fiel", "inferencia", "añadido", "contradiccion"]

_SISTEMA_JUEZ = """Eres un verificador de fidelidad textual, estricto e imparcial.
Para cada afirmación recibes los párrafos originales que la sustentan.
Clasifícala así:
- literal: repite las palabras del original.
- parafrasis_fiel: dice lo mismo que el original con otras palabras.
- inferencia: se deduce razonablemente del original, pero el original no lo dice.
- añadido: introduce información, ejemplos o juicios que no están en el original.
- contradiccion: dice algo distinto u opuesto a lo que dice el original.
Juzga solo contra los párrafos dados. Explica tu motivo en una frase."""

_ESQUEMA_JUEZ = objeto(veredictos=lista(objeto(n={"type": "integer"}, clase={"type": "string", "enum": CLASES}, motivo=TEXTO)))


def juzgar(llm: LLM, obra: Obra, afirmaciones: list[dict], lote: int = 8) -> list[dict]:
    """`afirmaciones`: [{"texto", "anclas"}]. Devuelve [{"texto", "anclas", "clase", "motivo"}]."""
    por_id = obra.por_id()
    resultado = []
    for inicio in range(0, len(afirmaciones), lote):
        grupo = afirmaciones[inicio : inicio + lote]
        bloques = []
        for i, af in enumerate(grupo):
            fuentes = "\n".join(f"  [§{a}] {por_id[a].texto}" for a in af["anclas"] if a in por_id) or "  (sin párrafos de origen)"
            bloques.append(f"AFIRMACIÓN {i}: {af['texto']}\nORIGINAL:\n{fuentes}")
        datos = llm.json(_SISTEMA_JUEZ, "\n\n".join(bloques), _ESQUEMA_JUEZ, temperatura=0)
        veredictos = {v["n"]: v for v in datos.get("veredictos", []) if isinstance(v.get("n"), int)}
        for i, af in enumerate(grupo):
            v = veredictos.get(i, {"clase": "inferencia", "motivo": "El juez no devolvió veredicto."})
            if not af["anclas"]:
                v = {"clase": "añadido", "motivo": "No cita ningún párrafo de origen."}
            resultado.append({**af, "clase": v["clase"], "motivo": v.get("motivo", "")})
    return resultado
