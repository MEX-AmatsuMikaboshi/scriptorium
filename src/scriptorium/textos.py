"""Derivados de texto anclados al original.

Niveles de intervención: 0 literal · 1 estructural · 2 explicativo fiel · 3 didáctico.
Todo lo que produce el LLM lleva anclas a los párrafos de origen y pasa por verificación.
"""

from __future__ import annotations

import json
import re
from typing import Callable

from . import verificacion as ver
from .config import Ajustes
from .ingesta import Obra
from .llm import ANCLAS, LLM, TEXTO, lista, objeto

SISTEMA = """Eres un editor académico al servicio de la fidelidad textual. Trabajas SOLO con el texto que se te da, \
dividido en párrafos con identificadores como [§1.0.3].
Reglas inviolables:
1. No añadas información, contexto histórico, ejemplos ni opiniones que no estén en el texto.
2. Conserva los términos técnicos del autor tal cual; no los sustituyas por sinónimos.
3. Cada afirmación lleva en "anclas" los IDs de los párrafos que la sustentan, sin el símbolo § (por ejemplo "1.0.3"). \
Los IDs van SOLO en "anclas": nunca los escribas dentro del texto.
4. Las citas y definiciones literales se copian carácter por carácter del texto.
5. Escribe en español claro y natural."""

ANCLADO = objeto(texto=TEXTO, anclas=ANCLAS)

TAREAS: dict[str, tuple[int, str, dict]] = {
    "resumen": (
        2,
        "Haz un resumen con zoom del texto. «una_linea»: la idea central en una sola oración. «parrafo»: un párrafo de "
        "4 a 6 oraciones. «pagina»: una LISTA de 6 a 14 elementos que recorran el texto en orden; cada elemento es UNA "
        "sola oración con sus propias anclas. Usa las palabras del autor siempre que puedas.",
        objeto(una_linea=ANCLADO, parrafo=ANCLADO, pagina=lista(ANCLADO)),
    ),
    "glosario": (
        1,
        "Extrae de 4 a 12 términos clave que el autor usa o define. Para cada uno: «termino», tal como lo escribe el autor; "
        "«definicion_literal»: el fragmento EXACTO del texto, copiado carácter por carácter, donde el autor lo define o "
        "caracteriza (máximo 40 palabras); «ancla»: el ID de ese párrafo. Si el autor no define un término, no lo incluyas.",
        objeto(terminos=lista(objeto(termino=TEXTO, definicion_literal=TEXTO, ancla=TEXTO))),
    ),
    "citas": (
        1,
        "Selecciona de 4 a 10 citas clave: fragmentos copiados EXACTAMENTE del texto (máximo 45 palabras cada uno) que "
        "condensen las ideas principales. «palabra_clave»: una palabra importante que aparezca dentro de la cita. "
        "«por_que»: en una frase, por qué importa dentro del texto.",
        objeto(citas=lista(objeto(cita=TEXTO, ancla=TEXTO, palabra_clave=TEXTO, por_que=TEXTO))),
    ),
    "esquema": (
        2,
        "Reconstruye la estructura argumental del texto. «tesis»: lo que el autor sostiene. «premisas»: las razones que da "
        "(de 2 a 6). «objeciones»: solo las que el propio autor menciona o responde (puede quedar vacía). «conclusion». "
        "Todo con anclas.",
        objeto(tesis=ANCLADO, premisas=lista(ANCLADO), objeciones=lista(ANCLADO), conclusion=ANCLADO),
    ),
    "mapa": (
        2,
        "Organiza las ideas del texto como un mapa mental: de 3 a 7 ramas, cada una con 2 a 5 hojas. Textos breves "
        "(máximo 12 palabras) y con las palabras del autor. Todo con anclas.",
        objeto(ramas=lista(objeto(titulo=TEXTO, anclas=ANCLAS, hojas=lista(ANCLADO)))),
    ),
    "quiz": (
        2,
        "Escribe de 5 a 8 preguntas de opción múltiple que comprueben la comprensión del texto. Cuatro opciones y solo "
        "una correcta («correcta» es su índice, de 0 a 3). La «explicacion» dice qué afirma el texto al respecto. Las "
        "preguntas deben poder responderse SOLO con el texto.",
        objeto(
            preguntas=lista(
                objeto(pregunta=TEXTO, opciones=lista(TEXTO), correcta={"type": "integer"}, explicacion=TEXTO, anclas=ANCLAS)
            )
        ),
    ),
    "preguntas": (
        3,
        "Propón de 3 a 5 preguntas de reflexión que inviten a pensar críticamente sobre las ideas del texto. Son un "
        "añadido didáctico: no afirmes nada nuevo, solo pregunta. «anclas»: los párrafos que motivan cada pregunta.",
        objeto(preguntas=lista(ANCLADO)),
    ),
    "guion_audio": (
        2,
        "Escribe el guion de una audio-guía de este texto, para escucharse antes o después de leerlo. Tono: un profesor "
        "claro y cercano que acompaña la lectura. Recorre el texto en orden y explícalo sin añadir información externa; "
        "usa citas breves del autor cuando ayuden. Entre 8 y 16 segmentos de 2 a 4 oraciones. Sin saludos ni muletillas "
        "de radio. Cada segmento con sus anclas.",
        objeto(segmentos=lista(ANCLADO)),
    ),
    "guion_video": (
        2,
        "Escribe la narración de un video explicativo de 2 a 4 minutos sobre este texto. Entre 8 y 14 segmentos; cada "
        "uno tiene de 1 a 3 oraciones (máximo 45 palabras) y acompañará una animación. Empieza con la pregunta o tesis "
        "central y termina con la conclusión del autor. Fiel al texto, sin información externa. Cada segmento con anclas.",
        objeto(segmentos=lista(ANCLADO)),
    ),
    "podcast": (
        2,
        "Escribe un diálogo de podcast entre dos voces: «anfitrion» (curioso: pregunta, resume y conecta) y "
        "«especialista» (explica con precisión lo que dice el texto). Entre 12 y 22 turnos de 1 a 4 oraciones. El "
        "especialista solo afirma lo que está en el texto; el anfitrión puede preguntar pero no aporta datos nuevos. "
        "Cada turno con anclas.",
        objeto(turnos=lista(objeto(voz={"type": "string", "enum": ["anfitrion", "especialista"]}, texto=TEXTO, anclas=ANCLAS))),
    ),
}

# Tareas que, en capítulos largos, se hacen sobre el resumen anclado y no sobre el texto completo.
GLOBALES = {"esquema", "mapa", "guion_audio", "guion_video", "podcast"}


def _bloques(obra: Obra, cap: int, max_palabras: int) -> list[str]:
    bloques, actual, palabras = [], [], 0
    for b in obra.bloques:
        if b.capitulo != cap:
            continue
        linea = f"\n## {b.texto}\n" if b.tipo == "titulo" else f"[§{b.id}] {b.texto}"
        n = len(b.texto.split())
        if actual and palabras + n > max_palabras:
            bloques.append("\n".join(actual))
            actual, palabras = [], 0
        actual.append(linea)
        palabras += n
    if actual:
        bloques.append("\n".join(actual))
    return bloques


def _pedir(llm: LLM, obra: Obra, tarea: str, texto: str, nota: str = "") -> dict:
    _, instruccion, esquema = TAREAS[tarea]
    autor = obra.meta.get("autor") or "autor desconocido"
    usuario = f"OBRA: {obra.meta['titulo']} ({autor})\n{nota}\nTEXTO:\n{texto}\n\nTAREA: {instruccion}"
    return llm.json(SISTEMA, usuario, esquema)


def _fusionar(tarea: str, partes: list[dict]) -> dict:
    if len(partes) == 1:
        return partes[0]
    clave = {"glosario": "terminos", "citas": "citas", "quiz": "preguntas", "preguntas": "preguntas"}[tarea]
    return {clave: [x for p in partes for x in p.get(clave, [])]}


_ID_EN_TEXTO = re.compile(r"\s*[\[(]?§?\s?(\d+\.\d+\.\d+)[\])]?")


def _sin_ids(texto: str, obra: Obra) -> tuple[str, list[str]]:
    """Quita del texto los IDs de párrafo que el modelo haya escrito en línea y los devuelve aparte."""
    validos = obra.por_id()
    encontrados = [m.group(1) for m in _ID_EN_TEXTO.finditer(texto) if m.group(1) in validos]
    if not encontrados:
        return texto, []
    limpio = _ID_EN_TEXTO.sub(lambda m: "" if m.group(1) in validos else m.group(0), texto)
    limpio = re.sub(r"(\s*,)+\s*(?=[.;:!?]|$)", "", limpio)
    limpio = re.sub(r"\s+([.,;:!?])", r"\1", limpio)
    return limpio.strip(), encontrados


def _anclar(item: dict, obra: Obra) -> dict:
    texto, en_linea = _sin_ids(item.get("texto", ""), obra)
    if "texto" in item:
        item["texto"] = texto
    item["anclas"] = ver.limpiar_anclas(list(item.get("anclas", [])) + en_linea, obra)
    return item


def _por_oraciones(items: list[dict], obra: Obra) -> list[dict]:
    """Si el modelo entregó varias oraciones en un elemento, las separa, cada una con su ancla."""
    salida = []
    for item in items:
        oraciones = re.split(r"(?<=[.?!])\s+(?=[¿¡«A-ZÁÉÍÓÚÑ])", item.get("texto", "").strip())
        if len(oraciones) <= 1:
            salida.append(item)
            continue
        for o in oraciones:
            _, propias = _sin_ids(o, obra)
            salida.append({"texto": o, "anclas": propias or list(item.get("anclas", []))})
    return salida


def derivar_capitulo(llm: LLM, obra: Obra, cap: int, ajustes: Ajustes, avisar: Callable[[str], None]) -> dict:
    bloques = _bloques(obra, cap, ajustes.palabras_por_bloque)
    res: dict = {"capitulo": cap, "titulo": obra.titulo_capitulo(cap), "modelo": llm.modelo, "niveles": {}}

    for tarea in ("resumen", "glosario", "citas", "quiz", "preguntas"):
        avisar(f"cap. {cap} · {tarea}")
        partes = [_pedir(llm, obra, tarea, b) for b in bloques]
        if tarea == "resumen" and len(partes) > 1:
            puntos = "\n".join(
                f"- {p['texto']} [{', '.join(p['anclas'])}]" for parte in partes for p in parte.get("pagina", [])
            )
            res[tarea] = _pedir(llm, obra, tarea, puntos, "(El TEXTO es un resumen fiel por partes; conserva sus anclas.)")
        else:
            res[tarea] = partes[0] if tarea == "resumen" else _fusionar(tarea, partes)

    fuente, nota = bloques[0], ""
    if len(bloques) > 1:
        fuente = "\n".join(f"- {p['texto']} [{', '.join(p['anclas'])}]" for p in res["resumen"].get("pagina", []))
        nota = "(El TEXTO es un resumen fiel del capítulo; usa sus anclas.)"
    for tarea in GLOBALES:
        avisar(f"cap. {cap} · {tarea}")
        res[tarea] = _pedir(llm, obra, tarea, fuente, nota)

    _verificar(llm, obra, res, avisar)
    res["niveles"] = {t: TAREAS[t][0] for t in TAREAS}
    return res


def _verificar(llm: LLM, obra: Obra, res: dict, avisar: Callable[[str], None]) -> None:
    informe = {"citas_rechazadas": [], "definiciones_rechazadas": []}

    # 1. Literales: comprobación carácter por carácter, sin IA.
    citas = []
    for c in res["citas"].get("citas", []):
        encontrado = ver.localizar_literal(c["cita"], obra, c.get("ancla"))
        if encontrado:
            citas.append({**c, "ancla": encontrado, "verificada": True})
        else:
            informe["citas_rechazadas"].append(c)
    res["citas"]["citas"] = citas

    terminos, vistos = [], set()
    for t in res["glosario"].get("terminos", []):
        encontrado = ver.localizar_literal(t["definicion_literal"], obra, t.get("ancla"))
        if encontrado and t["termino"].casefold() not in vistos:
            vistos.add(t["termino"].casefold())
            terminos.append({**t, "ancla": encontrado, "verificada": True})
        elif not encontrado:
            informe["definiciones_rechazadas"].append(t)
    res["glosario"]["terminos"] = terminos

    # 2. Anclas válidas en todo lo demás.
    r = res["resumen"]
    for clave in ("una_linea", "parrafo"):
        _anclar(r[clave], obra)
    r["pagina"] = [_anclar(p, obra) for p in _por_oraciones(r.get("pagina", []), obra)]
    e = res["esquema"]
    for clave in ("tesis", "conclusion"):
        _anclar(e[clave], obra)
    e["premisas"] = [_anclar(p, obra) for p in e.get("premisas", [])]
    e["objeciones"] = [_anclar(p, obra) for p in e.get("objeciones", [])]
    for rama in res["mapa"].get("ramas", []):
        _anclar(rama, obra)
        rama["hojas"] = [_anclar(h, obra) for h in rama.get("hojas", [])]
    for clave, campo in (("quiz", "preguntas"), ("preguntas", "preguntas"), ("guion_audio", "segmentos"), ("guion_video", "segmentos"), ("podcast", "turnos")):
        res[clave][campo] = [_anclar(x, obra) for x in res[clave].get(campo, [])]
    res["quiz"]["preguntas"] = [
        q for q in res["quiz"]["preguntas"] if len(q.get("opciones", [])) == 4 and 0 <= q.get("correcta", -1) <= 3
    ]
    for q in res["quiz"]["preguntas"]:
        q["explicacion"], extra = _sin_ids(q.get("explicacion", ""), obra)
        q["anclas"] = ver.limpiar_anclas(q["anclas"] + extra, obra)

    # 3. Juez de fidelidad sobre todo lo que parafrasea (nivel 2).
    avisar(f"cap. {res['capitulo']} · juez de fidelidad")
    grupos = {
        "resumen": [r["una_linea"], r["parrafo"], *r["pagina"]],
        "esquema": [e["tesis"], *e["premisas"], *e["objeciones"], e["conclusion"]],
        "guion_video": res["guion_video"]["segmentos"],
        "guion_audio": res["guion_audio"]["segmentos"],
        "podcast": [t for t in res["podcast"]["turnos"] if t.get("voz") == "especialista"],
        # Cada pregunta del quiz se juzga junto con su respuesta correcta (va al final para no
        # invalidar la caché de los lotes anteriores).
        "quiz": [
            {"texto": f"{q['pregunta']} Respuesta correcta: {q['opciones'][q['correcta']]}. {q['explicacion']}", "anclas": q["anclas"]}
            for q in res["quiz"]["preguntas"]
        ],
    }
    planos = [(g, i) for g, items in grupos.items() for i in range(len(items))]
    veredictos = ver.juzgar(llm, obra, [{"texto": grupos[g][i]["texto"], "anclas": grupos[g][i]["anclas"]} for g, i in planos])
    conteo: dict[str, int] = {}
    for (g, i), v in zip(planos, veredictos):
        grupos[g][i]["fidelidad"] = {"clase": v["clase"], "motivo": v["motivo"]}
        conteo[v["clase"]] = conteo.get(v["clase"], 0) + 1
    informe["juez"] = conteo
    informe["señaladas"] = [
        {"producto": g, "texto": grupos[g][i]["texto"], **grupos[g][i]["fidelidad"]}
        for g, i in planos
        if grupos[g][i]["fidelidad"]["clase"] in ("añadido", "contradiccion")
    ]
    malas = ("añadido", "contradiccion")
    preguntas = res["quiz"]["preguntas"]
    informe["quiz_descartadas"] = [q["pregunta"] for q, p in zip(preguntas, grupos["quiz"]) if p["fidelidad"]["clase"] in malas]
    res["quiz"]["preguntas"] = [q for q, p in zip(preguntas, grupos["quiz"]) if p["fidelidad"]["clase"] not in malas]
    res["fidelidad"] = informe


def guardar(obra: Obra, derivados: list[dict]) -> None:
    carpeta = obra.derivados / "texto"
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "derivados.json").write_text(json.dumps(derivados, indent=2, ensure_ascii=False), encoding="utf-8")


def cargar(obra: Obra) -> list[dict] | None:
    archivo = obra.derivados / "texto" / "derivados.json"
    return json.loads(archivo.read_text(encoding="utf-8")) if archivo.exists() else None
