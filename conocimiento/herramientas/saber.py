#!/usr/bin/env python3
"""Saber: consulta y mantenimiento de la biblioteca de conocimiento audiovisual.

Solo usa la biblioteca estándar (Python 3.10+): corre igual desde cualquier proyecto y sin red.

    saber buscar "animar letras una por una"        qué técnicas, herramientas, recetas y docs sirven
    saber ver remotion [--breve]                    una ficha, técnica, principio, flujo o receta
    saber contexto "video explicativo de 30 s"      paquete de contexto para pegarle a un modelo
    saber capacidades                               taxonomía de capacidades y cuántos recursos tiene cada una
    saber validar                                   revisa formato, referencias internas y duplicados
    saber actualizar [--solo a,b] [--sin-docs]      metadatos de GitHub/npm/PyPI y documentación a la caché
    saber enlaces                                   revisa que los enlaces respondan
    saber nuevo <url-de-github> [--id x]            esqueleto de ficha (avisa si el recurso ya existe)
    saber bandeja                                   notas crudas que faltan por procesar
    saber probar                                    pruebas de consulta (catalogo/pruebas.json)
    saber indexar                                   rehace el índice (normalmente se rehace solo)

Formato de los documentos: Markdown con un bloque ```json de metadatos al principio (ver fichas/_plantilla.md).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import sqlite3
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CATALOGO = RAIZ / "catalogo"
CACHE = RAIZ / ".cache"
DOCS = CACHE / "docs"
INDICE = CACHE / "indice.sqlite"
CARPETAS = {"ficha": "fichas", "tecnica": "tecnicas", "principio": "principios", "flujo": "flujos"}
HOY = dt.date.today().isoformat()
AGENTE_HTTP = "scriptorium-saber/1.0 (+https://github.com/MEX-AmatsuMikaboshi/scriptorium)"

VALORES = {
    "tipo": {"motor", "libreria", "skill", "mcp", "plantilla", "referencia", "aplicacion", "modelo-ia", "herramienta", "infraestructura"},
    "areas": {"video-explicativo", "motion-graphics", "audio-voz", "2d", "3d", "personajes", "anime", "conocimiento"},
    "prioridad": {"ahora", "complemento", "futuro"},
    "estado_local": {"en-uso", "instalado", "no-instalado", "incompatible"},
    "confianza": {"verificado", "parcial", "por-verificar"},
    "exporta_video": {"si", "no", "indirecto", "no-aplica"},
}
OBLIGATORIOS = {
    "ficha": ["id", "nombre", "tipo", "areas", "prioridad", "estado_local", "capacidades", "resumen", "confianza", "verificado"],
    "tecnica": ["id", "nombre", "capacidades", "herramientas", "resumen"],
    "principio": ["id", "nombre", "resumen"],
    "flujo": ["id", "nombre", "capacidades", "herramientas", "resumen"],
}
ETIQUETAS = {"tecnica": "TÉCNICAS", "ficha": "HERRAMIENTAS Y RECURSOS", "flujo": "FLUJOS DE TRABAJO",
             "receta": "RECETAS DE CÓDIGO", "principio": "PRINCIPIOS DE DISEÑO", "doc": "DOCUMENTACIÓN LOCAL"}
ORDEN_GRUPOS = ["tecnica", "ficha", "flujo", "receta", "principio", "doc"]


# ---------------------------------------------------------------- texto

VACIAS = set("""
a al algo algun alguna ante asi bien cada como con cual cuando da de del desde donde dos el ella ellas en entre era es
esa ese eso esta estan este esto hace hacer haga hay la las le les lo los mas me mi mis mucho muy necesito ni no nos o
otra otro para pero poco por puede puedo pueda que quiero quisiera se sea ser si sin sobre solo su sus tambien tengo
tener todo tu un una uno unos unas usar uso y ya yo crear crea genera generar hagas quiero quieres seria
the of and to for with in on an is are be by it this that i want need make my me how can using use do
""".split())
SUFIJOS = ("amientos", "imientos", "amiento", "imiento", "aciones", "iciones", "ations", "mente", "acion", "icion",
           "ation", "ition", "ciones", "cion", "tion", "idades", "idad", "ables", "ibles", "able", "ible", "ando",
           "iendo", "ating", "ated", "ates", "ados", "idos", "adas", "idas", "ado", "ido", "ada", "ida", "ing",
           "ers", "ar", "er", "ir", "ed", "ate")


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def palabras(texto: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", normalizar(texto))


NO_RAIZ = {"anime", "animes", "manga", "mangas"}  # sin esto «anime» y «animar» comparten raíz


def raiz(p: str) -> str:
    """Raíz ligera para español e inglés: «letras»/«letra» → «letr», «animación»/«animation»/«animar» → «anim»."""
    if len(p) <= 3 or p.isdigit():
        return p
    if p in NO_RAIZ:
        return p.rstrip("s")
    if p.endswith("es") and len(p) > 5 and p[-3] not in "aeiou":
        p = p[:-2]
    elif p.endswith("s") and not p.endswith("ss") and len(p) > 4:
        p = p[:-1]
    for s in SUFIJOS:
        if p.endswith(s) and len(p) - len(s) >= 4:
            p = p[: -len(s)]
            break
    if p[-1] in "aeo" and len(p) > 4:
        p = p[:-1]
    return p


def raices(texto: str, sin_vacias: bool = True) -> list[str]:
    return [raiz(p) for p in palabras(texto) if not (sin_vacias and p in VACIAS)]


def aproximar_tokens(texto: str) -> int:
    return int(len(texto) / 3.6) + 1


# ---------------------------------------------------------------- documentos

@dataclass
class Doc:
    id: str
    tipo: str  # ficha, tecnica, principio, flujo, receta, doc
    titulo: str
    ruta: str  # relativa a RAIZ
    meta: dict = field(default_factory=dict)
    texto: str = ""

    @property
    def resumen(self) -> str:
        return self.meta.get("resumen") or self.meta.get("que_se_mueve") or self.texto[:200].replace("\n", " ")

    def secciones(self) -> dict[str, str]:
        partes = re.split(r"^## +(.+)$", self.texto, flags=re.M)
        return {partes[i].strip(): partes[i + 1].strip() for i in range(1, len(partes) - 1, 2)}


def leer_md(ruta: Path) -> tuple[str, dict, str]:
    texto = ruta.read_text(encoding="utf-8")
    m = re.search(r"```json[ \t]*\n(.*?)\n```", texto, re.S)
    if not m:
        raise ValueError("falta el bloque ```json de metadatos")
    meta = json.loads(m.group(1))
    titulo = re.search(r"^# +(.+)$", texto, re.M)
    cuerpo = (texto[: m.start()] + texto[m.end():]).strip()
    cuerpo = re.sub(r"^# +.+\n", "", cuerpo, count=1).strip()
    return (titulo.group(1).strip() if titulo else meta.get("nombre", ruta.stem)), meta, cuerpo


def _rel(ruta: Path) -> str:
    return ruta.relative_to(RAIZ).as_posix()


def cargar_capacidades() -> dict[str, dict]:
    datos = json.loads((CATALOGO / "capacidades.json").read_text(encoding="utf-8"))
    return {c["id"]: c for c in datos["capacidades"]}


def cargar_estado() -> dict:
    ruta = CATALOGO / "estado.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def cargar_fuentes(errores: list[str] | None = None) -> list[Doc]:
    """Fichas, técnicas, principios, flujos y recetas (sin la documentación descargada)."""
    docs: list[Doc] = []
    for tipo, carpeta in CARPETAS.items():
        for ruta in sorted((RAIZ / carpeta).glob("*.md")):
            if ruta.name.startswith("_"):
                continue
            try:
                titulo, meta, cuerpo = leer_md(ruta)
                docs.append(Doc(meta.get("id", ruta.stem), tipo, titulo, _rel(ruta), meta, cuerpo))
            except (ValueError, json.JSONDecodeError) as e:
                (errores if errores is not None else []).append(f"{_rel(ruta)}: {e}")
                if errores is None:
                    print(f"aviso: {_rel(ruta)}: {e}", file=sys.stderr)
    caps = cargar_capacidades()
    for ruta in sorted((RAIZ / "recetas").glob("*/recetas.json")):
        coleccion = ruta.parent.name
        for r in json.loads(ruta.read_text(encoding="utf-8")):
            texto = "\n".join([r["que_se_mueve"], *r.get("pasos", []), " · ".join(r.get("parametros", []))])
            meta = {k: v for k, v in r.items() if k != "codigo"}
            meta["capacidades"] = sorted(detectar_capacidades(f"{r['nombre']} {r['categoria']} {r['que_se_mueve']}", caps))
            meta["coleccion"] = coleccion
            docs.append(Doc(f"{coleccion}/{r['id']}", "receta", r["nombre"], _rel(ruta), meta, texto))
    return docs


def _limpiar_readme(texto: str) -> str:
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    lineas = [l for l in texto.splitlines() if not re.match(r"\s*(\[!\[|!\[|<img|<a href=.*<img|<p align|</?p>|</?div)", l)]
    return re.sub(r"<[^>]+>", "", "\n".join(lineas))


def trozos_de_documentacion() -> list[Doc]:
    """README y llms.txt descargados por «actualizar», partidos por encabezados."""
    docs: list[Doc] = []
    if not DOCS.exists():
        return docs
    for carpeta in sorted(p for p in DOCS.iterdir() if p.is_dir()):
        for archivo in sorted(carpeta.iterdir()):
            if archivo.suffix not in (".md", ".txt", ".rst"):
                continue
            texto = _limpiar_readme(archivo.read_text(encoding="utf-8", errors="replace"))
            actual, titulo, n = [], archivo.name, 0
            def cerrar():
                nonlocal n
                cuerpo = "\n".join(actual).strip()
                if len(cuerpo) >= 80:
                    n += 1
                    docs.append(Doc(f"doc:{carpeta.name}/{archivo.name}#{n}", "doc", f"{archivo.name} de {carpeta.name} › {titulo}",
                                    _rel(archivo), {"ficha": carpeta.name, "seccion": titulo}, cuerpo[:3000]))
            for linea in texto.splitlines():
                m = re.match(r"#{1,4} +(.+)", linea)
                if m and sum(len(x) for x in actual) > 300:
                    cerrar()
                    actual, titulo = [], m.group(1).strip()
                elif m and not actual:
                    titulo = m.group(1).strip()
                actual.append(linea)
                if sum(len(x) for x in actual) > 2500:
                    cerrar()
                    actual = []
                if n >= 400:
                    break
            cerrar()
    return docs


# ---------------------------------------------------------------- capacidades

_SINONIMOS: dict[str, list[list[str]]] | None = None


def detectar_capacidades(texto: str, caps: dict[str, dict] | None = None) -> dict[str, int]:
    """Capacidad → fuerza (número de palabras del sinónimo más largo que aparece en el texto)."""
    global _SINONIMOS
    caps = caps or cargar_capacidades()
    if _SINONIMOS is None:
        _SINONIMOS = {}
        for cid, c in caps.items():
            frases = [c["nombre"], cid.replace("-", " "), *c.get("sinonimos", [])]
            _SINONIMOS[cid] = [r for r in (raices(f) for f in frases) if r]
    presentes = set(raices(texto))
    encontrados = {}
    for cid, frases in _SINONIMOS.items():
        fuerza = max((len(f) for f in frases if all(p in presentes for p in f)), default=0)
        if fuerza:
            encontrados[cid] = fuerza
    return encontrados


# ---------------------------------------------------------------- índice

def _archivos_fuente() -> list[Path]:
    rutas = [CATALOGO / "capacidades.json", CATALOGO / "estado.json"]
    for carpeta in CARPETAS.values():
        rutas += (RAIZ / carpeta).glob("*.md")
    rutas += (RAIZ / "recetas").glob("*/recetas.json")
    if DOCS.exists():
        rutas += [p for p in DOCS.rglob("*") if p.is_file()]
    return [p for p in rutas if p.exists()]


def _firma() -> str:
    rutas = _archivos_fuente()
    return f"{len(rutas)}:{max((p.stat().st_mtime_ns for p in rutas), default=0)}:{Path(__file__).stat().st_mtime_ns}"


def _crear_indice(con: sqlite3.Connection, firma: str) -> None:
    con.executescript("""
        DROP TABLE IF EXISTS docs; DROP TABLE IF EXISTS fts; DROP TABLE IF EXISTS info;
        CREATE TABLE docs(id TEXT PRIMARY KEY, tipo TEXT, titulo TEXT, ruta TEXT, meta TEXT, texto TEXT);
        CREATE VIRTUAL TABLE fts USING fts5(id UNINDEXED, r_titulo, r_claves, r_texto, tokenize="unicode61 remove_diacritics 2");
        CREATE TABLE info(clave TEXT PRIMARY KEY, valor TEXT);
    """)
    caps = cargar_capacidades()
    for d in cargar_fuentes() + trozos_de_documentacion():
        m = d.meta
        claves = " ".join([d.id.replace("-", " "), m.get("nombre", ""), m.get("resumen", ""), " ".join(m.get("areas", [])),
                           " ".join(c.replace("-", " ") + " " + caps.get(c, {}).get("nombre", "") for c in m.get("capacidades", [])),
                           " ".join(m.get("lenguajes", [])), m.get("tipo", ""), m.get("categoria", ""), m.get("seccion", "")])
        extra = " ".join(str(m.get(k, "")) for k in ("licencia", "agentes", "requisitos"))
        con.execute("INSERT INTO docs VALUES (?,?,?,?,?,?)", (d.id, d.tipo, d.titulo, d.ruta, json.dumps(m, ensure_ascii=False), d.texto))
        con.execute("INSERT INTO fts VALUES (?,?,?,?)", (d.id, " ".join(raices(d.titulo)), " ".join(raices(claves)),
                                                       " ".join(raices(d.texto + " " + extra))))
    con.execute("INSERT INTO info VALUES ('firma', ?)", (firma,))
    con.commit()


def indice(forzar: bool = False) -> sqlite3.Connection:
    """Índice SQLite FTS5 en .cache/; se rehace solo cuando cambia algún archivo fuente."""
    firma = _firma()
    CACHE.mkdir(exist_ok=True)
    try:
        if INDICE.exists() and not forzar:
            con = sqlite3.connect(INDICE)
            fila = con.execute("SELECT valor FROM info WHERE clave='firma'").fetchone()
            if fila and fila[0] == firma:
                return con
            con.close()
        temporal = INDICE.with_suffix(".nuevo")
        temporal.unlink(missing_ok=True)
        con = sqlite3.connect(temporal)
        _crear_indice(con, firma)
        con.close()
        os.replace(temporal, INDICE)
        return sqlite3.connect(INDICE)
    except sqlite3.OperationalError:  # disco que no admite bloqueos (algunas unidades de red): índice en memoria
        con = sqlite3.connect(":memory:")
        _crear_indice(con, firma)
        return con


def _doc_de_fila(fila) -> Doc:
    return Doc(fila[0], fila[1], fila[2], fila[3], json.loads(fila[4]), fila[5])


def obtener(con: sqlite3.Connection, ident: str) -> Doc | None:
    fila = con.execute("SELECT * FROM docs WHERE id=?", (ident,)).fetchone()
    if not fila:  # «golpe» encuentra «canvas2d/golpe»
        fila = con.execute("SELECT * FROM docs WHERE id LIKE ? AND tipo='receta'", (f"%/{ident}",)).fetchone()
    return _doc_de_fila(fila) if fila else None


# ---------------------------------------------------------------- búsqueda

@dataclass
class Hallazgo:
    doc: Doc
    puntaje: float
    razones: list[str]


def _fts(con: sqlite3.Connection, terminos: list[str]) -> dict[str, float]:
    if not terminos:
        return {}
    expr = " OR ".join(f'"{t}" *' if len(t) >= 4 else f'"{t}"' for t in sorted(set(terminos)))
    filas = con.execute("SELECT id, bm25(fts, 0, 6, 3, 1) FROM fts WHERE fts MATCH ? ORDER BY 2 LIMIT 400", (expr,)).fetchall()
    if not filas:
        return {}
    mejor = max(-b for _, b in filas) or 1
    return {i: (-b) / mejor for i, b in filas}


def buscar(consulta: str, limite: int = 5, tipos: list[str] | None = None) -> dict:
    con = indice()
    caps = cargar_capacidades()
    estado = cargar_estado()
    detectadas = detectar_capacidades(consulta, caps)
    directo = _fts(con, raices(consulta))
    expansion = _fts(con, [r for c in detectadas for s in caps[c].get("sinonimos", [])[:6] for r in raices(s)])
    candidatos = set(directo) | set(expansion)
    if detectadas:
        for (ident, meta) in con.execute("SELECT id, meta FROM docs WHERE tipo != 'doc'"):
            if set(json.loads(meta).get("capacidades", [])) & set(detectadas):
                candidatos.add(ident)
    todos: dict[str, Hallazgo] = {}
    for ident in candidatos:
        d = obtener(con, ident)
        if d is None:
            continue
        razones, p = [], 0.0
        comunes = [c for c in d.meta.get("capacidades", []) if c in detectadas]
        if comunes:
            p += 1.3 * sum(min(detectadas[c], 2) for c in comunes)
            if d.meta.get("capacidades", [None])[0] in comunes:  # es su capacidad principal
                p += 0.6
            razones.append("sirve para " + ", ".join(comunes))
        p += 2.0 * directo.get(ident, 0) + 0.8 * expansion.get(ident, 0)
        if d.tipo == "ficha":
            p += {"ahora": 0.6, "complemento": 0.1, "futuro": -0.4}.get(d.meta.get("prioridad"), 0)
            local = d.meta.get("estado_local")
            p += {"en-uso": 0.8, "instalado": 0.4, "incompatible": -1.5}.get(local, 0)
            if local in ("en-uso", "instalado", "incompatible"):
                razones.append(local)
            if d.meta.get("confianza") == "por-verificar":
                p -= 0.3
                razones.append("por verificar")
            for alerta in estado.get(d.id, {}).get("alertas", []):
                p -= 1.0 if "archivado" in alerta else 0.4
                razones.append(alerta)
        todos[ident] = Hallazgo(d, p, razones)
    # Grafo ligero: las técnicas mejor puntuadas recomiendan sus herramientas (en orden de preferencia).
    tecnicas = sorted((h for h in todos.values() if h.doc.tipo == "tecnica" and h.razones), key=lambda h: -h.puntaje)[:2]
    for rango, t in enumerate(tecnicas):
        for orden, herramienta in enumerate(t.doc.meta.get("herramientas", [])):
            if herramienta not in todos:
                d = obtener(con, herramienta)
                if d is None:
                    continue
                todos[herramienta] = Hallazgo(d, 0.0, [])
            peso = 2.2 if orden == 0 else max(0.3, 1.6 - 0.2 * orden)  # la primera es su recomendación por defecto
            todos[herramienta].puntaje += peso * (1.0 if rango == 0 else 0.5)
            todos[herramienta].razones.append(f"la recomienda la técnica {t.doc.id}")
    # La documentación descargada pesa más si es de una herramienta que ya salió arriba.
    fichas_arriba = {h.doc.id for h in sorted((h for h in todos.values() if h.doc.tipo == "ficha"), key=lambda h: -h.puntaje)[:limite]}
    hallazgos: dict[str, list[Hallazgo]] = {}
    for h in todos.values():
        if h.doc.tipo == "doc":
            h.puntaje *= 1.2 if h.doc.meta.get("ficha") in fichas_arriba else 0.4
        if h.puntaje > 0.15 and not (tipos and h.doc.tipo not in tipos):
            h.puntaje = round(h.puntaje, 3)
            hallazgos.setdefault(h.doc.tipo, []).append(h)
    grupos = {}
    for tipo in ORDEN_GRUPOS:
        lista = sorted(hallazgos.get(tipo, []), key=lambda h: -h.puntaje)
        lista = [h for h in lista if h.puntaje >= 0.3 * lista[0].puntaje] if lista else []  # corta la cola de coincidencias sueltas
        if lista:
            grupos[tipo] = lista[: (3 if tipo in ("doc", "principio", "flujo") else limite)]
    return {"consulta": consulta, "capacidades": [(c, caps[c]["nombre"], f) for c, f in sorted(detectadas.items(), key=lambda x: -x[1])],
            "grupos": grupos}


def formatear_busqueda(r: dict) -> str:
    salida = [f"Biblioteca: {RAIZ}", f"Consulta: «{r['consulta']}»"]
    if r["capacidades"]:
        salida.append("Capacidades detectadas: " + "; ".join(f"{c} ({n})" for c, n, _ in r["capacidades"]))
    else:
        salida.append("Capacidades detectadas: ninguna (búsqueda solo por palabras; prueba otras o mira «saber capacidades»)")
    for tipo, lista in r["grupos"].items():
        salida.append(f"\n{ETIQUETAS[tipo]}")
        for i, h in enumerate(lista, 1):
            d, m = h.doc, h.doc.meta
            if tipo == "ficha":
                etiqueta = f"[{m.get('tipo')} · {m.get('prioridad')} · {m.get('estado_local')}]"
                salida.append(f"  {i}. {d.id} — {d.titulo} {etiqueta}\n     {d.resumen}")
            elif tipo == "doc":
                salida.append(f"  {i}. {d.titulo}\n     {d.ruta}")
                continue
            elif tipo == "receta":
                salida.append(f"  {i}. {d.id} — {d.titulo} ({m.get('verificacion')})\n     {d.resumen[:180]}")
            else:
                salida.append(f"  {i}. {d.id} — {d.titulo}\n     {d.resumen}")
            salida.append(f"     → {d.ruta}" + (f"   ({'; '.join(h.razones)})" if h.razones else ""))
    if not r["grupos"]:
        salida.append("\nSin resultados.")
    salida.append("\nSiguiente: «saber ver <id>» para leer uno completo; «saber contexto \"<petición>\"» arma el paquete para un modelo.")
    return "\n".join(salida)


def breve(d: Doc, tope: int = 700) -> str:
    m = d.meta
    if d.tipo == "ficha":
        datos = " · ".join(f"{k}: {m[k]}" for k in ("tipo", "prioridad", "estado_local", "exporta_video") if m.get(k))
        lineas = [f"## {d.titulo} ({d.id})", m.get("resumen", ""), datos]
        if m.get("licencia"):
            lineas.append(f"Licencia: {m['licencia']}")
        if m.get("requisitos"):
            lineas.append(f"Requisitos: {m['requisitos']}")
        sec = d.secciones()
        for titulo in ("Úsalo para", "Instalación", "Limitaciones", "En este equipo"):
            if sec.get(titulo):
                texto = sec[titulo] if len(sec[titulo]) <= tope else sec[titulo][:tope].rsplit("\n", 1)[0] + "\n…"
                lineas.append(f"{titulo}:\n{texto}")
        enlaces = [e for e in [m.get("web"), m.get("repo") and f"https://github.com/{m['repo']}"] + m.get("docs", [])[:2] if e]
        if enlaces:
            lineas.append("Enlaces: " + " · ".join(enlaces))
        return "\n".join(l for l in lineas if l)
    if d.tipo == "receta":
        return f"## Receta {d.id}: {d.titulo}\n{d.resumen}\nPasos: " + " ".join(m.get("pasos", [])) + \
               f"\nParámetros: {' · '.join(m.get('parametros', []))}\nCódigo: «saber ver {d.id}» (requiere recetas/{m.get('coleccion')}/motor.js)"
    return f"## {d.titulo} ({d.id})\n{d.resumen}"


def ver(ident: str, es_breve: bool = False) -> str:
    con = indice()
    d = obtener(con, ident)
    if d is None:
        r = buscar(ident, limite=3)
        sugerencias = [h.doc.id for lista in r["grupos"].values() for h in lista][:6]
        return f"No existe «{ident}». ¿Quisiste decir: {', '.join(sugerencias) or '(nada parecido)'}?"
    if es_breve:
        return breve(d)
    if d.tipo == "receta":
        receta = next(x for x in json.loads((RAIZ / d.ruta).read_text(encoding="utf-8")) if x["id"] == d.meta["id"])
        return breve(d) + f"\nFuente: {d.meta['fuente']} · {d.meta['nota_verificacion']}\n\n```js\n{receta['codigo']}\n```"
    if d.tipo == "doc":
        return f"{d.titulo}\n({d.ruta})\n\n{d.texto}"
    return (RAIZ / d.ruta).read_text(encoding="utf-8")


def contexto(peticion: str, tokens: int = 3500) -> str:
    """Junta lo más útil para una petición sin pasarse del presupuesto (tokens aproximados)."""
    r = buscar(peticion, limite=4)
    g = r["grupos"]
    partes = [f"# Contexto de la biblioteca para: «{peticion}»",
              "Capacidades: " + (", ".join(f"{c} ({n})" for c, n, _ in r["capacidades"]) or "ninguna detectada"),
              "Reglas: herramientas locales y gratuitas primero; código determinista (cada cuadro depende solo del tiempo); "
              "verifica licencias; en Scriptorium el LLM del pipeline nunca escribe código, solo elige escenas del kit."]
    usados = aproximar_tokens("\n".join(partes))

    def agregar(texto: str, minimo: str | None = None) -> None:
        nonlocal usados
        for opcion in (texto, minimo):
            if opcion and usados + aproximar_tokens(opcion) <= tokens:
                partes.append(opcion)
                usados += aproximar_tokens(opcion)
                return

    for h in g.get("flujo", [])[:1]:  # un flujo que coincide por capacidad es la receta completa: va primero
        if h.razones:
            agregar(f"\n## Flujo: {h.doc.titulo}\n{h.doc.texto}", f"\n{breve(h.doc)}")
    for i, h in enumerate(g.get("tecnica", [])[:2]):
        agregar(f"\n## Técnica: {h.doc.titulo}\n{h.doc.texto}" if i == 0 else "", f"\n{breve(h.doc)}")
    for h in g.get("ficha", [])[:3]:
        agregar(f"\n{breve(h.doc, tope=350)}", f"\n## {h.doc.titulo} ({h.doc.id}): {h.doc.resumen}")
    con = indice()
    control = obtener(con, "lista-de-control")
    if control:
        agregar(f"\n## Lista de control de calidad\n{control.texto}", f"\n{breve(control)}")
    for h in g.get("receta", [])[:2]:
        agregar(f"\n{ver(h.doc.id)}", f"\n{breve(h.doc)}")
    for h in g.get("doc", [])[:2]:
        agregar(f"\n## {h.doc.titulo}\n{h.doc.texto[:1500]}")
    partes.append(f"\n(≈{usados} tokens. Más detalle: «saber ver <id>» o los archivos en {RAIZ})")
    return "\n".join(partes)


# ---------------------------------------------------------------- validación

def validar() -> tuple[list[str], list[str]]:
    errores: list[str] = []
    avisos: list[str] = []
    docs = cargar_fuentes(errores)
    caps = cargar_capacidades()
    ids: dict[str, str] = {}
    repos: dict[str, str] = {}
    for d in docs:
        if d.id in ids:
            errores.append(f"id repetido «{d.id}»: {ids[d.id]} y {d.ruta}")
        ids[d.id] = d.ruta
        if d.tipo == "receta":
            continue
        if Path(d.ruta).stem != d.id:
            errores.append(f"{d.ruta}: el id «{d.id}» no coincide con el nombre del archivo")
        for campo in OBLIGATORIOS[d.tipo]:
            if campo not in d.meta or d.meta[campo] in ("", None):
                errores.append(f"{d.ruta}: falta «{campo}»")
        for campo, permitidos in VALORES.items():
            if d.tipo != "ficha" or campo not in d.meta:
                continue
            valores = d.meta[campo] if isinstance(d.meta[campo], list) else [d.meta[campo]]
            for v in valores:
                if v not in permitidos:
                    errores.append(f"{d.ruta}: {campo}=«{v}» no es válido ({', '.join(sorted(permitidos))})")
        for c in d.meta.get("capacidades", []):
            if c not in caps:
                errores.append(f"{d.ruta}: capacidad desconocida «{c}» (agrégala a catalogo/capacidades.json)")
        if d.tipo == "ficha" and not d.meta.get("capacidades"):
            avisos.append(f"{d.ruta}: sin capacidades (la búsqueda por intención no la encontrará)")
        if d.tipo == "ficha" and d.meta.get("repo"):
            clave = d.meta["repo"].lower()
            if clave in repos:
                errores.append(f"repositorio duplicado {d.meta['repo']}: {repos[clave]} y {d.ruta}")
            repos[clave] = d.ruta
        if d.tipo == "ficha" and len(d.meta.get("resumen", "")) > 220:
            avisos.append(f"{d.ruta}: el resumen pasa de 220 caracteres (los modelos chicos lo leen en listas)")
    for d in docs:
        for campo in ("relacionados", "herramientas", "recetas"):
            for otro in d.meta.get(campo, []):
                if otro not in ids:
                    errores.append(f"{d.ruta}: {campo} menciona «{otro}», que no existe")
        if d.tipo != "receta":
            for destino in re.findall(r"\]\((?!https?:|#|mailto:)([^)#\s]+)", d.texto):
                if not (RAIZ / Path(d.ruta).parent / destino).resolve().exists():
                    errores.append(f"{d.ruta}: enlace interno roto → {destino}")
    for cid, c in caps.items():
        for t in c.get("tecnicas", []):
            if t not in ids:
                errores.append(f"capacidades.json: «{cid}» menciona la técnica «{t}», que no existe")
    usadas = {c for d in docs for c in d.meta.get("capacidades", [])}
    for cid in caps:
        if cid not in usadas:
            avisos.append(f"capacidad «{cid}» sin recursos todavía")
    return errores, avisos


# ---------------------------------------------------------------- red

def _pedir(url: str, cabeceras: dict | None = None, metodo: str = "GET", limite: int = 4_000_000):
    req = urllib.request.Request(url, method=metodo, headers={"User-Agent": AGENTE_HTTP, **(cabeceras or {})})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status, dict(r.headers), (r.read(limite) if metodo != "HEAD" else b"")


def _github(repo: str, cache: Path, token: str | None) -> tuple[dict | None, str]:
    archivo = cache / (repo.replace("/", "__") + ".json")
    guardado = json.loads(archivo.read_text(encoding="utf-8")) if archivo.exists() else {}
    cab = {"Accept": "application/vnd.github+json"}
    if token:
        cab["Authorization"] = f"Bearer {token}"
    if guardado.get("etag"):
        cab["If-None-Match"] = guardado["etag"]  # una respuesta 304 no gasta del límite por hora
    try:
        _, h, cuerpo = _pedir(f"https://api.github.com/repos/{repo}", cab)
        datos = json.loads(cuerpo)
        archivo.write_text(json.dumps({"etag": h.get("ETag") or h.get("Etag"), "datos": datos}), encoding="utf-8")
        return datos, "ok"
    except urllib.error.HTTPError as e:
        if e.code == 304:
            return guardado["datos"], "sin cambios"
        if e.code in (403, 429) and e.headers.get("X-RateLimit-Remaining") == "0":
            reinicio = dt.datetime.fromtimestamp(int(e.headers.get("X-RateLimit-Reset", "0"))).strftime("%H:%M")
            return guardado.get("datos"), f"límite de la API agotado (se renueva a las {reinicio}; con GITHUB_TOKEN son 5000/h)"
        return None, f"HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError) as e:
        return guardado.get("datos"), f"sin red ({e})"


def _descargar_doc(url: str, destino: Path) -> bool:
    try:
        estado, _, cuerpo = _pedir(url)
        if estado == 200 and cuerpo.strip():
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_bytes(cuerpo)
            return True
    except (urllib.error.URLError, TimeoutError):
        pass
    return False


def actualizar(solo: list[str] | None, con_docs: bool = True) -> str:
    fichas = [d for d in cargar_fuentes() if d.tipo == "ficha" and (not solo or d.id in solo)]
    estado = cargar_estado()
    cache_gh = CACHE / "github"
    cache_gh.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    agotado = False
    informe = []
    hace_18_meses = (dt.date.today() - dt.timedelta(days=548)).isoformat()
    for d in fichas:
        m, e = d.meta, {"revisado": HOY, "alertas": []}
        if m.get("repo") and not agotado:
            datos, nota = _github(m["repo"], cache_gh, token)
            agotado = "límite" in nota
            if datos and "full_name" in datos:
                e["github"] = {"nombre": datos["full_name"], "descripcion": datos.get("description"),
                               "estrellas": datos.get("stargazers_count"), "ultimo_push": (datos.get("pushed_at") or "")[:10],
                               "archivado": datos.get("archived"), "licencia": (datos.get("license") or {}).get("spdx_id"),
                               "web": datos.get("homepage") or None, "temas": datos.get("topics", [])}
                if datos["full_name"].lower() != m["repo"].lower():
                    e["alertas"].append(f"renombrado a {datos['full_name']}")
                if datos.get("archived"):
                    e["alertas"].append("repositorio archivado")
                elif e["github"]["ultimo_push"] and e["github"]["ultimo_push"] < hace_18_meses:
                    e["alertas"].append(f"sin cambios desde {e['github']['ultimo_push']}: posiblemente abandonado")
            elif nota.startswith("HTTP 404"):
                e["alertas"].append("el repositorio no existe (404)")
            if nota not in ("ok", "sin cambios"):
                informe.append(f"{d.id}: GitHub {nota}")
        elif m.get("repo") and estado.get(d.id, {}).get("github"):
            e["github"] = estado[d.id]["github"]  # sin consulta: se conserva lo anterior
        for paquete in m.get("paquetes", {}).get("npm", [])[:3]:
            try:
                _, _, cuerpo = _pedir(f"https://registry.npmjs.org/{paquete.replace('/', '%2F')}/latest")
                info = json.loads(cuerpo)
                e.setdefault("npm", {})[paquete] = {"version": info.get("version"), "licencia": info.get("license")}
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as x:
                e["alertas"].append(f"npm {paquete}: {x}")
        for paquete in m.get("paquetes", {}).get("pypi", [])[:3]:
            try:
                _, _, cuerpo = _pedir(f"https://pypi.org/pypi/{paquete}/json", limite=20_000_000)
                info = json.loads(cuerpo)
                fecha = max((u["upload_time"][:10] for u in info.get("urls", [])), default=None)
                e.setdefault("pypi", {})[paquete] = {"version": info["info"]["version"], "publicado": fecha,
                                                     "licencia": (info["info"].get("license_expression") or info["info"].get("license") or "")[:60]}
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as x:
                e["alertas"].append(f"PyPI {paquete}: {x}")
        if con_docs:
            carpeta = DOCS / d.id
            if m.get("repo"):
                for nombre in ("README.md", "readme.md", "README.MD", "Readme.md", "README.rst", "README"):
                    if _descargar_doc(f"https://raw.githubusercontent.com/{m['repo']}/HEAD/{nombre}", carpeta / "README.md"):
                        e["docs"] = [f".cache/docs/{d.id}/README.md"]
                        break
            if m.get("llms_txt"):
                if _descargar_doc(m["llms_txt"], carpeta / "llms.txt"):
                    e.setdefault("docs", []).append(f".cache/docs/{d.id}/llms.txt")
                else:
                    e["alertas"].append(f"no se pudo bajar {m['llms_txt']}")
        if not e["alertas"]:
            del e["alertas"]
        estado[d.id] = e
        if e.get("alertas"):
            informe.append(f"{d.id}: " + "; ".join(e["alertas"]))
    (CATALOGO / "estado.json").write_text(json.dumps(dict(sorted(estado.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    _escribir_recursos()
    return f"Revisadas {len(fichas)} fichas → catalogo/estado.json\n" + ("\n".join(informe) if informe else "Sin alertas.")


def _escribir_recursos() -> None:
    """catalogo/recursos.json: todas las fichas en compacto, con su estado, para agentes que solo leen JSON."""
    estado = cargar_estado()
    fichas = [d for d in cargar_fuentes() if d.tipo == "ficha"]
    salida = [{**{k: v for k, v in d.meta.items()}, "ficha": d.ruta, "estado": estado.get(d.id, {})} for d in fichas]
    (CATALOGO / "recursos.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def enlaces() -> str:
    usos: dict[str, set[str]] = {}
    for d in cargar_fuentes():
        if d.tipo == "receta":
            continue
        m = d.meta
        candidatos = [m.get("web"), m.get("llms_txt"), *(m.get("docs") or [])]
        if m.get("repo"):
            candidatos.append(f"https://github.com/{m['repo']}")
        candidatos += re.findall(r"https?://[^\s)>\]`\"']+", d.texto)
        for u in candidatos:
            if u:
                usos.setdefault(u.rstrip(".,;"), set()).add(d.ruta)

    def probar(url: str) -> tuple[str, str]:
        codificada = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")  # acentos y eñes en la ruta
        for metodo, cab in (("HEAD", {}), ("GET", {"Range": "bytes=0-0"})):
            try:
                estado, _, _ = _pedir(codificada, cab, metodo, limite=1)
                return url, f"{estado}"
            except urllib.error.HTTPError as e:
                if metodo == "GET" or e.code not in (400, 403, 405, 429):
                    return url, f"HTTP {e.code}"
            except Exception as e:  # red, certificados, URL mal formada: se informa y se sigue con las demás
                return url, f"error: {getattr(e, 'reason', e)}"
        return url, "?"

    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        resultados = dict(ex.map(probar, sorted(usos)))
    malos = {u: r for u, r in resultados.items() if not r[:1] in ("2", "3")}
    CACHE.mkdir(exist_ok=True)
    (CACHE / "enlaces.json").write_text(json.dumps({"revisado": HOY, "resultados": resultados}, indent=1), encoding="utf-8")
    lineas = [f"{len(resultados)} enlaces revisados, {len(malos)} con problemas."]
    for u, r in sorted(malos.items()):
        nota = "  (403 suele ser bloqueo a robots: revisar a mano)" if r == "HTTP 403" else ""
        lineas.append(f"  {r:>10}  {u}{nota}\n             en: {', '.join(sorted(usos[u]))}")
    return "\n".join(lineas)


PLANTILLA = """# {nombre}

```json
{meta}
```

## Qué es
{descripcion}

## Úsalo para
- (por completar)

## No lo uses para
- (por completar)

## Instalación
(por completar)

## Ventajas
- (por completar)

## Limitaciones
- (por completar)

## En este equipo
No instalado. (por verificar compatibilidad con la GP100 / 16 GB de RAM / WSL)
"""


def nuevo(url: str, ident: str | None) -> str:
    m = re.search(r"github\.com[/:]([^/\s]+)/([^/\s#?]+)", url) or re.fullmatch(r"([\w.-]+)/([\w.-]+)", url)
    if not m:
        return "Dame una URL de GitHub (https://github.com/dueño/repo) o «dueño/repo». Para otros sitios copia fichas/_plantilla.md."
    repo = f"{m.group(1)}/{m.group(2).removesuffix('.git')}"
    ident = ident or re.sub(r"[^a-z0-9]+", "-", normalizar(m.group(2))).strip("-")
    for d in cargar_fuentes():
        if d.tipo == "ficha" and (d.meta.get("repo", "").lower() == repo.lower() or d.id == ident):
            return f"Ya existe: {d.ruta} ({d.meta.get('repo') or d.id}). Actualiza esa ficha en vez de crear otra."
    datos, nota = _github(repo, CACHE / "github", os.environ.get("GITHUB_TOKEN"))
    if not datos:
        datos = {}
    meta = {"id": ident, "nombre": datos.get("name") or m.group(2), "tipo": "referencia", "areas": [], "prioridad": "futuro",
            "estado_local": "no-instalado", "capacidades": [], "resumen": (datos.get("description") or "(por completar)")[:200],
            "web": datos.get("homepage") or None, "repo": datos.get("full_name") or repo, "paquetes": {},
            "licencia": (datos.get("license") or {}).get("spdx_id") or "por verificar", "exporta_video": "no-aplica",
            "agentes": "por verificar", "relacionados": [], "fuentes": [], "verificado": HOY, "confianza": "por-verificar"}
    meta = {k: v for k, v in meta.items() if v is not None}
    destino = RAIZ / "fichas" / f"{ident}.md"
    destino.write_text(PLANTILLA.format(nombre=meta["nombre"], meta=json.dumps(meta, ensure_ascii=False, indent=2),
                                        descripcion=datos.get("description") or "(por completar)"), encoding="utf-8")
    return f"Creada {_rel(destino)} (GitHub: {nota}). Completa tipo, áreas, prioridad, capacidades y las secciones; luego «saber validar»."


def bandeja() -> str:
    pendientes, hechas = [], []
    for ruta in sorted((RAIZ / "bandeja").glob("*.md")):
        if ruta.name.startswith("_"):
            continue
        cabeza = ruta.read_text(encoding="utf-8")[:600]
        (hechas if re.search(r"procesado:\s*\d{4}-\d\d-\d\d", cabeza) else pendientes).append(_rel(ruta))
    lineas = [f"Pendientes ({len(pendientes)}):"] + [f"  {p}" for p in pendientes]
    lineas += [f"Procesadas: {len(hechas)}"]
    return "\n".join(lineas)


def probar_consultas() -> tuple[str, bool]:
    pruebas = json.loads((CATALOGO / "pruebas.json").read_text(encoding="utf-8"))
    lineas, fallos = [], 0
    for p in pruebas:
        r = buscar(p["consulta"], limite=p.get("top", 5))
        encontrados = {h.doc.id for lista in r["grupos"].values() for h in lista}
        faltan = [e for e in p["esperados"] if e not in encontrados]
        fallos += bool(faltan)
        caps = ",".join(c for c, _, _ in r["capacidades"]) or "-"
        lineas.append(f"{'OK ' if not faltan else 'MAL'} «{p['consulta']}» → {caps}" + (f"\n    faltan: {', '.join(faltan)}" if faltan else ""))
    lineas.append(f"\n{len(pruebas) - fallos}/{len(pruebas)} consultas devuelven lo esperado.")
    return "\n".join(lineas), fallos == 0


def listar_capacidades() -> str:
    caps = cargar_capacidades()
    docs = cargar_fuentes()
    lineas = []
    for cid, c in caps.items():
        n = {t: sum(1 for d in docs if d.tipo == t and cid in d.meta.get("capacidades", [])) for t in ("ficha", "tecnica", "receta")}
        lineas.append(f"{cid:28} {c['nombre']}  ({n['ficha']} recursos, {n['tecnica']} técnicas, {n['receta']} recetas)")
    return "\n".join(lineas)


# ---------------------------------------------------------------- comandos

def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="saber", description="Biblioteca de conocimiento audiovisual: consulta y mantenimiento.")
    sub = p.add_subparsers(dest="comando", required=True)
    s = sub.add_parser("buscar", help="Qué técnicas, herramientas y recetas sirven para una petición.")
    s.add_argument("consulta", nargs="+")
    s.add_argument("--limite", type=int, default=5)
    s.add_argument("--tipo", help="solo estos tipos: ficha,tecnica,principio,flujo,receta,doc")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("ver", aliases=["ficha"], help="Muestra un documento por su id.")
    s.add_argument("id")
    s.add_argument("--breve", action="store_true")
    s = sub.add_parser("contexto", help="Paquete de contexto para un modelo (Markdown).")
    s.add_argument("peticion", nargs="+")
    s.add_argument("--tokens", type=int, default=3500)
    sub.add_parser("capacidades", help="Taxonomía de capacidades.")
    sub.add_parser("validar", help="Revisa formato, referencias y duplicados.")
    s = sub.add_parser("actualizar", help="Metadatos de GitHub/npm/PyPI y documentación a la caché.")
    s.add_argument("--solo", help="ids separados por comas")
    s.add_argument("--sin-docs", action="store_true")
    sub.add_parser("enlaces", help="Revisa que los enlaces respondan.")
    s = sub.add_parser("nuevo", help="Esqueleto de ficha desde una URL de GitHub.")
    s.add_argument("url")
    s.add_argument("--id")
    sub.add_parser("bandeja", help="Notas crudas pendientes.")
    sub.add_parser("probar", help="Pruebas de consulta.")
    sub.add_parser("indexar", help="Rehace el índice.")
    a = p.parse_args(argv)

    if a.comando == "buscar":
        r = buscar(" ".join(a.consulta), a.limite, a.tipo.split(",") if a.tipo else None)
        if a.json:
            r["grupos"] = {t: [{"id": h.doc.id, "titulo": h.doc.titulo, "resumen": h.doc.resumen, "ruta": h.doc.ruta,
                                "puntaje": h.puntaje, "razones": h.razones} for h in lista] for t, lista in r["grupos"].items()}
            print(json.dumps(r, ensure_ascii=False, indent=1))
        else:
            print(formatear_busqueda(r))
    elif a.comando in ("ver", "ficha"):
        print(ver(a.id, a.breve))
    elif a.comando == "contexto":
        print(contexto(" ".join(a.peticion), a.tokens))
    elif a.comando == "capacidades":
        print(listar_capacidades())
    elif a.comando == "validar":
        errores, avisos = validar()
        for x in avisos:
            print(f"aviso: {x}")
        for x in errores:
            print(f"ERROR: {x}")
        print(f"\n{len(errores)} errores, {len(avisos)} avisos.")
        if errores:
            return 1
        _escribir_recursos()
        print("catalogo/recursos.json al día.")
    elif a.comando == "actualizar":
        print(actualizar(a.solo.split(",") if a.solo else None, not a.sin_docs))
    elif a.comando == "enlaces":
        print(enlaces())
    elif a.comando == "nuevo":
        print(nuevo(a.url, a.id))
    elif a.comando == "bandeja":
        print(bandeja())
    elif a.comando == "probar":
        texto, ok = probar_consultas()
        print(texto)
        return 0 if ok else 1
    elif a.comando == "indexar":
        con = indice(forzar=True)
        n = dict(con.execute("SELECT tipo, count(*) FROM docs GROUP BY tipo").fetchall())
        print(f"Índice: {INDICE}\n" + ", ".join(f"{k}: {v}" for k, v in sorted(n.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
