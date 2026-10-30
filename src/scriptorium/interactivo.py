"""Interactivos: lector con audio sincronizado, textos, quiz, mapa mental y mazo de Anki."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from html import escape
from typing import Callable

from . import config, publicar
from .estilo import pagina
from .ingesta import Obra
from .publicar import NIVELES

AVISOS = {"añadido": "Añadido: no está en el original", "contradiccion": "Posible contradicción con el original", "inferencia": "Inferencia: el original no lo dice explícitamente"}


def _anclas(item: dict, destino: str = "lector.html") -> str:
    anclas = item.get("anclas") or ([item["ancla"]] if item.get("ancla") else [])
    return "".join(f'<a class="ancla" href="{destino}#p-{a}">§{a}</a>' for a in anclas)


def _afirmacion(item: dict, etiqueta: str = "p") -> str:
    clase = item.get("fidelidad", {}).get("clase", "")
    aviso = AVISOS.get(clase)
    contenido = escape(item["texto"]) + _anclas(item)
    if aviso:
        contenido += f"<small>{aviso}. {escape(item['fidelidad'].get('motivo', ''))}</small>"
    return f'<{etiqueta} class="{"aviso" if clase in ("añadido", "contradiccion") else ""}">{contenido}</{etiqueta}>'


def _cabecera(obra: Obra, subtitulo: str, nivel: int | None = None) -> str:
    autor = escape(obra.meta.get("autor", ""))
    nivel_html = f'<span class="nivel">{NIVELES[nivel]}</span>' if nivel is not None else ""
    return (f'<header class="obra"><div class="migas"><a href="../../../03_biblioteca/index.html">Biblioteca</a> · '
            f'{escape(subtitulo)}</div><h1>{escape(obra.meta["titulo"])}</h1><div class="autor">{autor}</div>{nivel_html}</header>')


# ---------------------------------------------------------------- lector


def lector(obra: Obra, derivados: list[dict]) -> str:
    glosario = {t["termino"]: t for d in derivados for t in d["glosario"]["terminos"]}
    tiempos_archivo = obra.derivados / "audio" / "tiempos.json"
    tiempos = json.loads(tiempos_archivo.read_text()) if tiempos_archivo.exists() else {}
    marcados: set[str] = set()

    def con_glosario(texto: str) -> str:
        """Marca la primera aparición de cada término sobre el texto plano (sin tocar HTML ya generado)."""
        marcas: list[tuple[int, int, dict]] = []
        for termino, t in glosario.items():
            if termino in marcados:
                continue
            m = re.search(rf"\b{re.escape(termino)}\b", texto, re.I)
            if m and not any(m.start() < b and a < m.end() for a, b, _ in marcas):
                marcas.append((m.start(), m.end(), t))
                marcados.add(termino)
        partes, pos = [], 0
        for a, b, t in sorted(marcas, key=lambda x: x[0]):
            definicion = escape(f"«{t['definicion_literal']}» (§{t['ancla']})", quote=True)
            partes += [escape(texto[pos:a]), f'<span class="termino" tabindex="0" data-def="{definicion}">{escape(texto[a:b])}</span>']
            pos = b
        return "".join(partes) + escape(texto[pos:])

    partes = []
    for b in obra.bloques:
        if b.tipo == "titulo":
            etiqueta = "h2" if b.nivel == 1 else "h3"
            partes.append(f'<{etiqueta} id="p-{b.id}" data-id="{b.id}">{escape(b.texto)}</{etiqueta}>')
        else:
            partes.append(f'<p id="p-{b.id}" data-id="{b.id}"><a class="num" href="#p-{b.id}" title="Escuchar desde aquí">§{b.id}</a> {con_glosario(b.texto)}</p>')
    reproductor = ""
    if tiempos:
        reproductor = ('<div class="reproductor"><audio id="audio" controls preload="metadata" src="../audio/audiolibro.mp3"></audio>'
                       '<label><input type="checkbox" id="seguir" checked> seguir la lectura</label></div>')
    cuerpo = f'<div class="envoltura">{_cabecera(obra, "Lector", 0)}{reproductor}<article>{"".join(partes)}</article></div>'
    css = """.num{font:600 11px system-ui,sans-serif;color:var(--suave);text-decoration:none;margin-right:4px;vertical-align:2px}
article p{border-radius:8px;padding:2px 6px;margin:0 -6px 1em;transition:background .3s}
article .leyendo{background:var(--acento-suave)}
.termino{border-bottom:1px dotted var(--acento);cursor:help;position:relative}
.termino:hover::after,.termino:focus::after{content:attr(data-def);position:absolute;left:0;top:1.6em;z-index:9;width:min(360px,80vw);
background:var(--papel);color:var(--tinta);border:1px solid var(--linea);box-shadow:var(--sombra);border-radius:10px;padding:10px 12px;font:14px/1.45 system-ui,sans-serif}
.reproductor{position:sticky;top:0;z-index:8;background:var(--fondo);padding:10px 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap;
border-bottom:1px solid var(--linea);font:14px system-ui,sans-serif}.reproductor audio{flex:1;min-width:240px}"""
    script = f"""const T={json.dumps(tiempos)};const a=document.getElementById('audio');let actual=null;
if(a){{const ids=Object.keys(T);a.addEventListener('timeupdate',()=>{{const t=a.currentTime;const id=ids.find(k=>t>=T[k][0]&&t<T[k][1]+0.5);
if(id&&id!==actual){{document.querySelectorAll('.leyendo').forEach(e=>e.classList.remove('leyendo'));const el=document.getElementById('p-'+id);
if(el){{el.classList.add('leyendo');if(document.getElementById('seguir').checked)el.scrollIntoView({{behavior:'smooth',block:'center'}});}}actual=id;}}}});
document.querySelectorAll('[data-id]').forEach(el=>el.addEventListener('click',e=>{{const id=el.dataset.id;if(T[id]&&e.target.classList.contains('num')){{e.preventDefault();a.currentTime=T[id][0];a.play();}}}}));}}"""
    return pagina(f"Lector · {obra.meta['titulo']}", cuerpo, css, script)


# ---------------------------------------------------------------- textos


def pagina_textos(obra: Obra, derivados: list[dict]) -> str:
    paneles = {"resumen": [], "esquema": [], "glosario": [], "citas": [], "preguntas": [], "fidelidad": []}
    for d in derivados:
        cap = f"<h2>{escape(d['titulo'])}</h2>" if len(derivados) > 1 else ""
        r = d["resumen"]
        paneles["resumen"].append(
            f'{cap}<span class="nivel">{NIVELES[2]}</span><div class="zoom"><button class="boton activo" data-z="1">1 línea</button>'
            f'<button class="boton" data-z="2">1 párrafo</button><button class="boton" data-z="3">1 página</button></div>'
            f'<div class="tarjeta" data-nivel="1">{_afirmacion(r["una_linea"])}</div>'
            f'<div class="tarjeta" data-nivel="2" hidden>{_afirmacion(r["parrafo"])}</div>'
            f'<div class="tarjeta" data-nivel="3" hidden><ul>{"".join(_afirmacion(p, "li") for p in r["pagina"])}</ul></div>')
        e = d["esquema"]
        objeciones = f'<h3>Objeciones que el autor considera</h3><ul>{"".join(_afirmacion(o, "li") for o in e["objeciones"])}</ul>' if e["objeciones"] else ""
        paneles["esquema"].append(
            f'{cap}<span class="nivel">{NIVELES[2]}</span><div class="tarjeta"><h3>Tesis</h3>{_afirmacion(e["tesis"])}'
            f'<h3>Premisas</h3><ol>{"".join(_afirmacion(p, "li") for p in e["premisas"])}</ol>{objeciones}'
            f'<h3>Conclusión</h3>{_afirmacion(e["conclusion"])}</div>')
        paneles["glosario"].append(f'{cap}<span class="nivel">{NIVELES[1]}</span>' + "".join(
            f'<div class="tarjeta"><strong>{escape(t["termino"])}</strong><blockquote>«{escape(t["definicion_literal"])}»'
            f'{_anclas(t)}</blockquote></div>' for t in d["glosario"]["terminos"]))
        paneles["citas"].append(f'{cap}<span class="nivel">{NIVELES[1]} · verificadas carácter por carácter</span>' + "".join(
            f'<div class="tarjeta"><blockquote>«{escape(c["cita"])}»{_anclas(c)}</blockquote><p class="autor">{escape(c["por_que"])}</p></div>'
            for c in d["citas"]["citas"]))
        paneles["preguntas"].append(f'{cap}<span class="nivel">{NIVELES[3]}</span><ul>' + "".join(
            f'<li>{escape(p["texto"])}{_anclas(p)}</li>' for p in d["preguntas"]["preguntas"]) + "</ul>")
        f = d["fidelidad"]
        juez = "".join(f"<li>{escape(k)}: <strong>{v}</strong></li>" for k, v in sorted(f.get("juez", {}).items()))
        senaladas = "".join(f'<li class="aviso">[{escape(s["producto"])}] {escape(s["texto"])}<small>{escape(s["clase"])}: {escape(s["motivo"])}</small></li>' for s in f.get("señaladas", []))
        paneles["fidelidad"].append(
            f'{cap}<div class="tarjeta"><h3>Juez de fidelidad (LLM local, modelo {escape(d.get("modelo", ""))})</h3><ul>{juez}</ul>'
            f'<h3>Verificación por código</h3><ul><li>Citas verificadas: {len(d["citas"]["citas"])} · rechazadas: {len(f["citas_rechazadas"])}</li>'
            f'<li>Definiciones verificadas: {len(d["glosario"]["terminos"])} · rechazadas: {len(f["definiciones_rechazadas"])}</li></ul>'
            + (f"<h3>Señaladas para revisión</h3><ul>{senaladas}</ul>" if senaladas else "<p>Nada señalado como añadido o contradicción.</p>") + "</div>")
    nombres = {"resumen": "Resumen", "esquema": "Esquema", "glosario": "Glosario", "citas": "Citas", "preguntas": "Reflexión", "fidelidad": "Fidelidad"}
    botones = "".join(f'<button role="tab" aria-selected="{str(i == 0).lower()}" data-p="{k}">{v}</button>' for i, (k, v) in enumerate(nombres.items()))
    cuerpo = "".join(f'<section class="panel" id="{k}" {"" if i == 0 else "hidden"}>{"".join(v)}</section>' for i, (k, v) in enumerate(paneles.items()))
    html = f'<div class="envoltura">{_cabecera(obra, "Textos")}<nav class="pestanas">{botones}</nav>{cuerpo}</div>'
    script = """document.querySelectorAll('.pestanas button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.pestanas button').forEach(x=>x.setAttribute('aria-selected',x===b));
document.querySelectorAll('.panel').forEach(p=>p.hidden=p.id!==b.dataset.p)});
document.querySelectorAll('.zoom').forEach(z=>z.querySelectorAll('button').forEach(b=>b.onclick=()=>{z.querySelectorAll('button').forEach(x=>x.classList.toggle('activo',x===b));
let n=z.nextElementSibling;while(n&&n.dataset.nivel){n.hidden=n.dataset.nivel!==b.dataset.z;n=n.nextElementSibling;}}));"""
    return pagina(f"Textos · {obra.meta['titulo']}", html, ".zoom{display:flex;gap:8px;margin:12px 0}", script)


# ---------------------------------------------------------------- quiz


def quiz(obra: Obra, derivados: list[dict]) -> str:
    preguntas = [q for d in derivados for q in d["quiz"]["preguntas"]]
    datos = json.dumps(preguntas, ensure_ascii=False)
    cuerpo = (f'<div class="envoltura">{_cabecera(obra, "Quiz", 2)}<div id="quiz"></div>'
              f'<div class="tarjeta" id="marcador" hidden></div></div>')
    script = f"""const Q={datos};let bien=0,hechas=0;const raiz=document.getElementById('quiz');
Q.forEach((q,i)=>{{const t=document.createElement('div');t.className='tarjeta';
t.innerHTML=`<p><strong>${{i+1}}.</strong> ${{q.pregunta}}</p>`+q.opciones.map((o,j)=>`<button class="opcion" data-j="${{j}}">${{o}}</button>`).join('')+`<p class="exp" hidden></p>`;
t.querySelectorAll('.opcion').forEach(b=>b.onclick=()=>{{if(t.dataset.hecha)return;t.dataset.hecha=1;hechas++;const ok=+b.dataset.j===q.correcta;if(ok)bien++;
b.classList.add(ok?'bien':'mal');t.querySelector(`[data-j="${{q.correcta}}"]`).classList.add('bien');const e=t.querySelector('.exp');e.hidden=false;
e.innerHTML=q.explicacion+' '+q.anclas.map(a=>`<a class="ancla" href="lector.html#p-${{a}}">§${{a}}</a>`).join('');
const m=document.getElementById('marcador');m.hidden=false;m.textContent=`${{bien}} de ${{hechas}} correctas (${{Q.length}} preguntas)`;}});raiz.appendChild(t);}});"""
    css = """.opcion{display:block;width:100%;text-align:left;margin:8px 0;padding:12px 14px;border-radius:10px;border:1px solid var(--linea);
background:var(--fondo);color:var(--tinta);font:16px/1.4 system-ui,sans-serif;cursor:pointer}.opcion:hover{border-color:var(--acento)}
.opcion.bien{border-color:var(--ok);background:color-mix(in srgb,var(--ok) 15%,transparent)}.opcion.mal{border-color:var(--mal);background:color-mix(in srgb,var(--mal) 15%,transparent)}
.exp{font:15px/1.5 system-ui,sans-serif;color:var(--suave)}#marcador{position:sticky;bottom:12px;font:600 16px system-ui,sans-serif;text-align:center}"""
    return pagina(f"Quiz · {obra.meta['titulo']}", cuerpo, css, script)


# ---------------------------------------------------------------- mapa mental


def mapa_markdown(obra: Obra, derivados: list[dict]) -> str:
    lineas = [f"# {obra.meta['titulo']}"]
    for d in derivados:
        nivel = "##" if len(derivados) > 1 else ""
        if nivel:
            lineas.append(f"## {d['titulo']}")
        for rama in d["mapa"]["ramas"]:
            enlace = " ".join(f"[§{a}](lector.html#p-{a})" for a in rama["anclas"][:2])
            lineas.append(f"{'###' if nivel else '##'} {rama['titulo']} {enlace}".rstrip())
            for hoja in rama["hojas"]:
                enlace = " ".join(f"[§{a}](lector.html#p-{a})" for a in hoja["anclas"][:2])
                lineas.append(f"- {hoja['texto']} {enlace}".rstrip())
    return "\n".join(lineas) + "\n"


def mapa(obra: Obra, derivados: list[dict]) -> None:
    carpeta = obra.derivados / "interactivo"
    md = carpeta / "mapa.md"
    md.write_text(mapa_markdown(obra, derivados), encoding="utf-8")
    markmap = config.KIT_VIDEO / "node_modules" / ".bin" / "markmap"
    destino = carpeta / "mapa.html"
    if markmap.exists():
        subprocess.run([str(markmap), "--offline", "--no-open", "-o", str(destino), str(md)], check=True, capture_output=True)
        extra = ('<a href="../../../03_biblioteca/index.html" style="position:fixed;top:12px;left:16px;font:14px system-ui,sans-serif;'
                 'color:#a5721f;z-index:9">← Biblioteca</a><script>const ajustar=()=>window.mm&&window.mm.fit();'
                 'addEventListener("load",()=>setTimeout(ajustar,300));addEventListener("resize",ajustar);'
                 'document.addEventListener("visibilitychange",ajustar);</script></body>')
        destino.write_text(destino.read_text(encoding="utf-8").replace("</body>", extra, 1), encoding="utf-8")
    else:  # sin markmap: árbol plegable sencillo
        arbol = re.sub(r"\[(§[\d.]+)\]\(([^)]+)\)", r'<a class="ancla" href="\2">\1</a>', escape(md.read_text(encoding="utf-8"), quote=False))
        destino.write_text(pagina(f"Mapa · {obra.meta['titulo']}", f'<div class="envoltura"><pre>{arbol}</pre></div>'), encoding="utf-8")
    publicar.registrar(obra, "mapa", destino, 2, "Mapa mental", "interactivo")


# ---------------------------------------------------------------- Anki


def _id_estable(texto: str) -> int:
    return int(hashlib.sha1(texto.encode()).hexdigest()[:8], 16)


def anki(obra: Obra, derivados: list[dict]) -> None:
    import genanki

    css = ".card{font-family:Georgia,serif;font-size:20px;text-align:left;max-width:640px;margin:auto;line-height:1.5}.f{color:#888;font-size:14px}.cloze{color:#a5721f;font-weight:bold}"
    concepto = genanki.Model(_id_estable("scriptorium-concepto"), "Scriptorium · Concepto",
                             fields=[{"name": "Termino"}, {"name": "Definicion"}, {"name": "Fuente"}],
                             templates=[{"name": "Concepto", "qfmt": "<b>{{Termino}}</b><br><span class=f>¿Cómo lo define el autor?</span>",
                                         "afmt": "{{FrontSide}}<hr id=answer>«{{Definicion}}»<br><span class=f>{{Fuente}}</span>"}], css=css)
    cloze = genanki.Model(_id_estable("scriptorium-cita"), "Scriptorium · Cita", model_type=genanki.Model.CLOZE,
                          fields=[{"name": "Text"}, {"name": "Fuente"}],
                          templates=[{"name": "Cita", "qfmt": "{{cloze:Text}}", "afmt": "{{cloze:Text}}<br><span class=f>{{Fuente}}</span>"}], css=css)
    pregunta = genanki.Model(_id_estable("scriptorium-pregunta"), "Scriptorium · Pregunta",
                             fields=[{"name": "Pregunta"}, {"name": "Respuesta"}, {"name": "Fuente"}],
                             templates=[{"name": "Pregunta", "qfmt": "{{Pregunta}}", "afmt": "{{FrontSide}}<hr id=answer>{{Respuesta}}<br><span class=f>{{Fuente}}</span>"}], css=css)
    titulo = obra.meta["titulo"]
    autor = obra.meta.get("autor", "")
    mazo = genanki.Deck(_id_estable(f"mazo-{obra.slug}"), f"Scriptorium::{titulo}")
    for d in derivados:
        for t in d["glosario"]["terminos"]:
            mazo.add_note(genanki.Note(concepto, [escape(t["termino"]), escape(t["definicion_literal"]), f"{escape(autor)}, {escape(titulo)} §{t['ancla']}"],
                                       guid=genanki.guid_for(obra.slug, "c", t["termino"])))
        for c in d["citas"]["citas"]:
            palabra = c.get("palabra_clave", "")
            texto = escape(c["cita"])
            if palabra and re.search(rf"\b{re.escape(escape(palabra))}\b", texto, re.I):
                texto = re.sub(rf"\b({re.escape(escape(palabra))})\b", r"{{c1::\1}}", texto, count=1, flags=re.I)
                mazo.add_note(genanki.Note(cloze, [f"«{texto}»", f"{escape(autor)} §{c['ancla']}"], guid=genanki.guid_for(obra.slug, "q", c["cita"])))
        for q in d["quiz"]["preguntas"]:
            opciones = "<br>".join(f"{'abcd'[i]}) {escape(o)}" for i, o in enumerate(q["opciones"]))
            respuesta = f"<b>{escape(q['opciones'][q['correcta']])}</b><br>{escape(q['explicacion'])}"
            mazo.add_note(genanki.Note(pregunta, [f"{escape(q['pregunta'])}<br><br>{opciones}", respuesta, " ".join(f"§{a}" for a in q["anclas"])],
                                       guid=genanki.guid_for(obra.slug, "p", q["pregunta"])))
    destino = obra.derivados / "interactivo" / "mazo.apkg"
    genanki.Package(mazo).write_to_file(str(destino))
    publicar.registrar(obra, "anki", destino, 1, f"Mazo de Anki ({len(mazo.notes)} tarjetas)", "interactivo")


# ---------------------------------------------------------------- todo


def producir(obra: Obra, derivados: list[dict], avisar: Callable[[str], None]) -> None:
    carpeta = obra.derivados / "interactivo"
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "lector.html").write_text(lector(obra, derivados), encoding="utf-8")
    publicar.registrar(obra, "lector", carpeta / "lector.html", 0, "Lector con audio sincronizado", "interactivo")
    if not derivados:
        return
    (carpeta / "textos.html").write_text(pagina_textos(obra, derivados), encoding="utf-8")
    publicar.registrar(obra, "textos", carpeta / "textos.html", 2, "Resumen, esquema, glosario y citas", "interactivo")
    (carpeta / "quiz.html").write_text(quiz(obra, derivados), encoding="utf-8")
    publicar.registrar(obra, "quiz", carpeta / "quiz.html", 2, "Quiz autocorregible", "interactivo")
    mapa(obra, derivados)
    anki(obra, derivados)
    avisar("interactivos listos")
