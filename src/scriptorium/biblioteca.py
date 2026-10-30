"""Sitio local de la biblioteca: una página con todas las obras y sus productos."""

from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

from . import config
from .estilo import pagina
from .ingesta import Obra, listar_obras
from .publicar import NIVELES, manifiesto

ORDEN = ["lector", "textos", "mapa", "quiz", "anki"]
NIVEL_CORTO = {0: "N0 literal", 1: "N1 estructural", 2: "N2 explicativo", 3: "N3 didáctico"}


def _enlace(slug: str, producto: dict) -> str:
    return f"../02_derivados/{slug}/{producto['ruta']}"


def _tarjeta(obra: Obra) -> str:
    m = manifiesto(obra)
    productos = m["productos"]
    slug = obra.slug
    meta = obra.meta

    videos = "".join(
        f'<figure><video controls preload="metadata" src="{_enlace(slug, p)}"></video><figcaption>{escape(p["titulo"])} · '
        f'<span class="chip">{NIVEL_CORTO[p["nivel"]]}</span></figcaption></figure>'
        for p in productos.values() if p["tipo"] == "video"
    )
    audios = "".join(
        f'<div class="audio"><div>{escape(p["titulo"])} <span class="chip">{NIVEL_CORTO[p["nivel"]]}</span></div>'
        f'<audio controls preload="none" src="{_enlace(slug, p)}"></audio></div>'
        for k, p in productos.items() if p["tipo"] == "audio" and k != "audiolibro"
    )
    if "audiolibro" in productos:
        audios += f'<p class="nota"><a href="{_enlace(slug, productos["audiolibro"])}" download>Descargar audiolibro .m4b con capítulos</a></p>'
    botones = "".join(
        f'<a class="producto" href="{_enlace(slug, productos[k])}">{escape(productos[k]["titulo"])}<span class="chip">{NIVEL_CORTO[productos[k]["nivel"]]}</span></a>'
        for k in ORDEN if k in productos
    )
    textos = " · ".join(
        f'<a href="{_enlace(slug, p)}">{escape(p["titulo"])}</a>' for p in productos.values() if p["tipo"] == "texto"
    )
    capitulos = ", ".join(escape(c["titulo"]) for c in meta.get("capitulos", []) if c.get("titulo"))
    return f"""<section class="tarjeta obra">
<div class="cabeza"><div><h2>{escape(meta['titulo'])}</h2><div class="autor">{escape(meta.get('autor') or 'Autor desconocido')}
{(' · ' + escape(meta['fecha_obra'])) if meta.get('fecha_obra') else ''}</div></div>
<div class="cifras">{meta['palabras']:,} palabras · {meta['parrafos']} párrafos</div></div>
<p class="nota">{capitulos}</p>
{videos}<div class="productos">{botones}</div>{audios}
<p class="nota">Documentos: {textos or '—'}</p></section>"""


def construir() -> Path:
    config.BIBLIOTECA.mkdir(parents=True, exist_ok=True)
    obras = [Obra.cargar(s) for s in listar_obras()]
    tarjetas = "".join(_tarjeta(o) for o in obras) or '<p class="tarjeta">Aún no hay obras. Deja un archivo en 00_entrada y corre <code>scriptorium noche</code>.</p>'
    cata = config.DATOS / "cata_de_voces" / "index.html"
    leyenda = "".join(f"<li>{escape(v)}</li>" for v in NIVELES.values())
    cuerpo = f"""<div class="envoltura ancha">
<header class="obra"><div class="migas">Scriptorium · 100 % local</div><h1>Biblioteca</h1>
<div class="autor">Actualizada {datetime.now():%d/%m/%Y %H:%M}{' · <a href="../cata_de_voces/index.html">Cata de voces</a>' if cata.exists() else ''}</div></header>
{tarjetas}
<details class="tarjeta"><summary>Niveles de intervención y cómo agregar obras</summary><ul>{leyenda}</ul>
<p>Para agregar una obra: deja el PDF, EPUB, DOCX, PPTX, Markdown o TXT en <code>D:\\Scriptorium\\00_entrada</code> y corre
<code>scriptorium noche</code> en PowerShell. Las citas se comprueban carácter por carácter; las paráfrasis pasan por un juez de fidelidad.</p></details>
</div>"""
    css = """.ancha{max-width:1040px}.obra .cabeza{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:baseline}
.obra h2{margin:0;font-size:1.8rem}.cifras,.nota{font:14px/1.5 system-ui,sans-serif;color:var(--suave)}
.chip{font:600 11px system-ui,sans-serif;color:var(--acento);background:var(--acento-suave);border-radius:999px;padding:3px 8px;margin-left:8px;white-space:nowrap}
.productos{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin:18px 0}
.producto{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:12px 14px;border:1px solid var(--linea);border-radius:12px;
text-decoration:none;color:var(--tinta);font:500 15px system-ui,sans-serif;background:var(--fondo)}.producto:hover{border-color:var(--acento)}
figure{margin:16px 0}video{width:100%;border-radius:12px;background:#000}figcaption{font:14px system-ui,sans-serif;color:var(--suave);margin-top:6px}
.audio{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;justify-content:space-between;padding:8px 0;border-top:1px solid var(--linea);font:15px system-ui,sans-serif}
.audio audio{width:min(420px,100%)}summary{cursor:pointer;font-weight:600}code{background:var(--acento-suave);padding:1px 6px;border-radius:6px}"""
    destino = config.BIBLIOTECA / "index.html"
    destino.write_text(pagina("Biblioteca · Scriptorium", cuerpo, css), encoding="utf-8")
    return destino
