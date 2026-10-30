"""Hoja de estilo común de las páginas HTML (lector, textos, quiz, biblioteca)."""

from html import escape

CSS = """
:root{--fondo:#f7f4ee;--papel:#fffdf8;--tinta:#1e1c19;--suave:#6b655c;--linea:#e4ddd0;--acento:#a5721f;
--acento-suave:#f3e7cf;--ok:#2f7a52;--mal:#b23b2e;--aviso:#9a6a00;--sombra:0 1px 2px rgba(0,0,0,.05),0 8px 24px rgba(0,0,0,.06)}
@media (prefers-color-scheme:dark){:root:not([data-tema="claro"]){--fondo:#121214;--papel:#1a1a1d;--tinta:#ebe7df;
--suave:#a39d92;--linea:#2c2b2e;--acento:#d9a650;--acento-suave:#3a2f1c;--ok:#5fbf8a;--mal:#e5776a;--aviso:#e0b04a;
--sombra:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.35)}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--fondo);color:var(--tinta);font:18px/1.65 "Iowan Old Style","Palatino Linotype",Georgia,serif}
.envoltura{max-width:820px;margin:0 auto;padding:32px 16px 96px}
header.obra{margin-bottom:28px}header.obra h1{font-size:2.1rem;line-height:1.15;margin:.2em 0}
.autor{color:var(--suave);font-style:italic}
.migas{font:14px/1.4 system-ui,sans-serif;color:var(--suave)}.migas a{color:var(--suave)}
a{color:var(--acento)}h2,h3{line-height:1.25}h2{margin-top:2.2em}
.nivel{display:inline-block;font:600 12px/1 system-ui,sans-serif;letter-spacing:.02em;padding:6px 10px;border-radius:999px;
background:var(--acento-suave);color:var(--acento);margin:4px 0}
.ancla{font:600 12px system-ui,sans-serif;color:var(--acento);text-decoration:none;white-space:nowrap;margin-left:.25em}
.tarjeta{background:var(--papel);border:1px solid var(--linea);border-radius:14px;padding:20px 22px;box-shadow:var(--sombra);margin:16px 0}
.aviso{border-left:3px solid var(--aviso);padding-left:10px}.aviso small{display:block;color:var(--aviso);font:13px system-ui,sans-serif}
blockquote{margin:0;padding:0 0 0 16px;border-left:3px solid var(--acento);font-size:1.08em}
.pestanas{display:flex;flex-wrap:wrap;gap:8px;position:sticky;top:0;background:var(--fondo);padding:10px 0;z-index:5;border-bottom:1px solid var(--linea)}
.pestanas button,.boton{font:500 14px system-ui,sans-serif;border:1px solid var(--linea);background:var(--papel);color:var(--tinta);
padding:8px 14px;border-radius:999px;cursor:pointer}
.pestanas button[aria-selected=true],.boton.activo{background:var(--tinta);color:var(--fondo);border-color:var(--tinta)}
.panel[hidden]{display:none}
"""


def pagina(titulo: str, cuerpo: str, extra_css: str = "", script: str = "") -> str:
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(titulo)}</title><style>{CSS}{extra_css}</style></head>
<body>{cuerpo}{f'<script>{script}</script>' if script else ''}</body></html>"""
