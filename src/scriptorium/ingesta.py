"""Ingesta: cualquier archivo de entrada -> texto canónico con IDs estables.

Cada párrafo recibe un ID `capítulo.sección.párrafo` (p. ej. 1.2.14). Todo lo
derivado apunta a esos IDs, así que siempre se puede volver al original.
"""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from . import config

FORMATOS = {".pdf", ".md", ".markdown", ".txt", ".docx", ".pptx", ".epub", ".html", ".htm"}


@dataclass
class Bloque:
    id: str
    tipo: str  # "titulo" | "parrafo"
    capitulo: int
    seccion: int
    texto: str
    nivel: int = 0  # nivel del encabezado (solo títulos)


def slugify(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return texto[:60].strip("-") or "obra"


# ---------------------------------------------------------------- conversión a markdown


def _pdf_a_markdown(ruta: Path) -> str:
    import pymupdf
    import pymupdf4llm

    doc = pymupdf.open(ruta)
    caracteres = sum(len(p.get_text()) for p in doc)
    if caracteres / max(1, len(doc)) >= 200:
        # Sin encabezados ni pies de página (títulos corridos, números de página, pie de Wikisource).
        return pymupdf4llm.to_markdown(doc, show_progress=False, header=False, footer=False)
    # PDF escaneado: OCR página por página con Tesseract (español).
    paginas = []
    for pagina in doc:
        imagen = pagina.get_pixmap(dpi=300).tobytes("png")
        r = subprocess.run(["tesseract", "stdin", "stdout", "-l", "spa"], input=imagen, capture_output=True)
        paginas.append(r.stdout.decode("utf-8", "ignore"))
    return "\n\n".join(paginas)


def a_markdown(ruta: Path) -> str:
    sufijo = ruta.suffix.lower()
    if sufijo in {".md", ".markdown", ".txt"}:
        return ruta.read_text(encoding="utf-8", errors="replace")
    if sufijo == ".pdf":
        return _pdf_a_markdown(ruta)
    from markitdown import MarkItDown

    return MarkItDown().convert(str(ruta)).text_content


# ---------------------------------------------------------------- limpieza y segmentación


def _frontmatter(md: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", md, re.S)
    if not m:
        return {}, md
    meta = {}
    for linea in m.group(1).splitlines():
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            meta[clave.strip().lower()] = valor.strip().strip('"')
    return meta, md[m.end() :]


def _limpiar_linea(linea: str) -> str:
    linea = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", linea)  # imágenes
    linea = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", linea)  # enlaces -> texto
    linea = re.sub(r"\[\^?\d+\]", "", linea)  # llamadas a notas
    linea = re.sub(r"</?[a-zA-Z][^>]*>", "", linea)  # etiquetas HTML (<u>, <br>, <sup>…)
    linea = re.sub(r"(\*\*|__)(.+?)\1", r"\2", linea)
    linea = re.sub(r"(?<![\w*])[*_](\S(?:.*?\S)?)[*_](?![\w*])", r"\1", linea)
    linea = linea.replace("­", "")  # guiones blandos
    return linea.strip()


def _parrafos_y_titulos(md: str) -> list[tuple[int, str]]:
    """Devuelve [(nivel, texto)]: nivel 0 = párrafo, 1..6 = encabezado."""
    salida: list[tuple[int, str]] = []
    buffer: list[str] = []

    def volcar():
        if buffer:
            texto = " ".join(buffer)
            texto = re.sub(r"(\w)- (\w)", r"\1\2", texto)  # palabras partidas al final de línea
            texto = re.sub(r"\s+", " ", texto).strip()
            if texto and not re.fullmatch(r"[\d\s\-–—.]+", texto):
                salida.append((0, texto))
            buffer.clear()

    for cruda in md.splitlines():
        if re.match(r"^\s*(\|.*\||[-*_]{3,}|```.*)\s*$", cruda):
            volcar()
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", cruda.strip())
        if m:
            volcar()
            titulo = _limpiar_linea(m.group(2)).strip("# ")
            if titulo:
                salida.append((len(m.group(1)), titulo))
            continue
        linea = _limpiar_linea(cruda)
        if not linea:
            volcar()
            continue
        if re.match(r"^([-*+]|\d+[.)])\s+", linea):  # cada elemento de lista es su propio párrafo
            volcar()
            buffer.append(re.sub(r"^([-*+])\s+", "", linea))
            volcar()
            continue
        buffer.append(linea)
        # Una línea larga que termina en punto es un párrafo completo (textos con un salto
        # simple entre párrafos); las líneas cortas de un PDF maquetado siguen uniéndose.
        if len(linea) > 160 and re.search(r"[.?!:»\"”]$", linea):
            volcar()
    volcar()
    return salida


_PARECE_CAPITULO = re.compile(r"^(cap[ií]tulo|chapter|parte|libro|lecci[oó]n|tema|unidad|[IVXLC]+[.\s-])", re.I)
# Restos de páginas web impresas: navegación («< El criterio», «Capítulo III >») y pie de MediaWiki.
_RESTO_WEB = re.compile(r"^(?:[<←]\s.{1,80}|.{1,80}\s[>→]|(?:Obtenido de|Retrieved from)\s*«?https?://\S+?»?)$")
_SUBPAGINA_WIKI = re.compile(r"^[^/]+/\d+$")  # nombre de página de Wikisource: «El criterio/02»


def segmentar(md: str, tiene_titulo: bool = False, parte: str | None = None) -> tuple[str | None, list[Bloque]]:
    # El nombre de subpágina no es un título: se sustituye por la parte del nombre de archivo.
    piezas = [
        (n, parte if n and parte and _SUBPAGINA_WIKI.match(t) else t)
        for n, t in _parrafos_y_titulos(md)
        if not _RESTO_WEB.match(t)
    ]
    niveles = [n for n, _ in piezas if n > 0]
    titulo_doc = None
    nivel_cap = min(niveles) if niveles else 1
    unico = next((t for n, t in piezas if n == nivel_cap), "") if niveles else ""
    if (
        niveles
        and niveles.count(nivel_cap) == 1
        and len(set(niveles)) > 1
        and not tiene_titulo
        and not _PARECE_CAPITULO.match(unico)
    ):
        # Un único encabezado de nivel superior que no parece capítulo = título del documento.
        titulo_doc = unico
        piezas = [(n, t) for n, t in piezas if not (n == nivel_cap and t == titulo_doc)]
        nivel_cap = min(n for n, _ in piezas if n > 0) if any(n > 0 for n, _ in piezas) else nivel_cap + 1

    bloques: list[Bloque] = []
    cap, sec, par = 0, 0, 0
    for nivel, texto in piezas:
        if nivel and nivel <= nivel_cap:
            cap, sec, par = cap + 1, 0, 0
            bloques.append(Bloque(f"{cap}.0.0", "titulo", cap, 0, texto, 1))
        elif nivel:
            cap = cap or 1
            sec, par = sec + 1, 0
            bloques.append(Bloque(f"{cap}.{sec}.0", "titulo", cap, sec, texto, 2))
        else:
            cap = cap or 1
            par += 1
            bloques.append(Bloque(f"{cap}.{sec}.{par}", "parrafo", cap, sec, texto))
    return titulo_doc, bloques


# ---------------------------------------------------------------- obra canónica


@dataclass
class Obra:
    slug: str
    meta: dict
    bloques: list[Bloque]

    @property
    def carpeta(self) -> Path:
        return config.CANONICO / self.slug

    @property
    def derivados(self) -> Path:
        return config.DERIVADOS / self.slug

    @property
    def parrafos(self) -> list[Bloque]:
        return [b for b in self.bloques if b.tipo == "parrafo"]

    def por_id(self) -> dict[str, Bloque]:
        return {b.id: b for b in self.bloques}

    def capitulos(self) -> list[int]:
        return sorted({b.capitulo for b in self.bloques})

    def titulo_capitulo(self, cap: int) -> str:
        for b in self.bloques:
            if b.capitulo == cap and b.tipo == "titulo" and b.nivel == 1:
                return b.texto
        return f"Capítulo {cap}" if len(self.capitulos()) > 1 else self.meta.get("titulo", "")

    def texto_con_ids(self, capitulo: int | None = None) -> str:
        lineas = []
        for b in self.bloques:
            if capitulo is not None and b.capitulo != capitulo:
                continue
            lineas.append(f"\n## {b.texto}\n" if b.tipo == "titulo" else f"[§{b.id}] {b.texto}")
        return "\n".join(lineas).strip()

    def guardar(self) -> None:
        self.carpeta.mkdir(parents=True, exist_ok=True)
        with open(self.carpeta / "parrafos.jsonl", "w", encoding="utf-8") as f:
            for b in self.bloques:
                f.write(json.dumps(asdict(b), ensure_ascii=False) + "\n")
        (self.carpeta / "meta.json").write_text(json.dumps(self.meta, indent=2, ensure_ascii=False), encoding="utf-8")
        md = [f"# {self.meta['titulo']}", f"*{self.meta.get('autor') or 'Autor desconocido'}*", ""]
        for b in self.bloques:
            md.append(("#" * (b.nivel + 1) + " " + b.texto) if b.tipo == "titulo" else f"<a id=\"p-{b.id}\"></a>**§{b.id}** {b.texto}")
            md.append("")
        (self.carpeta / "texto.md").write_text("\n".join(md), encoding="utf-8")

    @classmethod
    def cargar(cls, slug: str) -> "Obra":
        carpeta = config.CANONICO / slug
        meta = json.loads((carpeta / "meta.json").read_text(encoding="utf-8"))
        with open(carpeta / "parrafos.jsonl", encoding="utf-8") as f:
            bloques = [Bloque(**json.loads(l)) for l in f if l.strip()]
        return cls(slug, meta, bloques)


def listar_obras() -> list[str]:
    if not config.CANONICO.exists():
        return []
    return sorted(p.name for p in config.CANONICO.iterdir() if (p / "meta.json").exists())


def ingerir(ruta: Path, titulo: str | None = None, autor: str | None = None) -> Obra:
    if ruta.suffix.lower() not in FORMATOS:
        raise ValueError(f"Formato no soportado: {ruta.suffix}. Acepto: {', '.join(sorted(FORMATOS))}")
    # Convención de nombre «Autor - Título - Parte.pdf» cuando el archivo no trae metadatos.
    partes = [p.strip() for p in ruta.stem.split(" - ") if p.strip()]
    parte = " - ".join(partes[2:]) or None
    if parte:  # los nombres de archivo suelen ir sin acentos: «Capitulo II» → «Capítulo II»
        parte = re.sub(r"^(capitulo|leccion)\b", lambda m: {"capitulo": "Capítulo", "leccion": "Lección"}[m[1].lower()], parte, flags=re.I)
    frontmatter, md = _frontmatter(a_markdown(ruta))
    titulo_doc, bloques = segmentar(md, bool(titulo or frontmatter.get("titulo") or " - " in ruta.stem), parte)
    if not any(b.tipo == "parrafo" for b in bloques):
        raise ValueError(f"No encontré texto en {ruta.name}")
    autor = autor or frontmatter.get("autor") or (partes[0] if len(partes) >= 2 else "")
    titulo = titulo or frontmatter.get("titulo") or (partes[1] if len(partes) >= 2 else None) or titulo_doc or ruta.stem
    parrafos = [b for b in bloques if b.tipo == "parrafo"]
    meta = {
        "titulo": titulo,
        "autor": autor,
        "fecha_obra": frontmatter.get("fecha", ""),
        "traduccion": frontmatter.get("traduccion", ""),
        "fuente": frontmatter.get("fuente", ""),
        "archivo_original": ruta.name,
        "ingerido": datetime.now().isoformat(timespec="seconds"),
        "parrafos": len(parrafos),
        "palabras": sum(len(b.texto.split()) for b in parrafos),
    }
    slug = slugify(f"{meta['autor']} {titulo}" if meta["autor"] else titulo)
    existente = config.CANONICO / slug / "meta.json"
    if existente.exists() and json.loads(existente.read_text(encoding="utf-8")).get("archivo_original") != ruta.name:
        # Otro archivo de la misma obra (p. ej. otro capítulo): no sobrescribir, distinguir por archivo.
        slug = slugify(f"{meta['autor']} {titulo} {ruta.stem}")[:80]
    obra = Obra(slug, meta, bloques)
    meta["slug"] = obra.slug
    meta["capitulos"] = [{"n": c, "titulo": obra.titulo_capitulo(c)} for c in obra.capitulos()]
    obra.guardar()
    return obra
