"""Página de la cata de voces, a ciegas: cada voz con su inteligibilidad medida y un botón para revelarla.

Uso (venv principal): python herramientas_wsl/cata_pagina.py /mnt/d/Scriptorium/03_biblioteca/cata
"""

import html
import json
import random
import re
import sys
from pathlib import Path

import soundfile as sf

sys.path.insert(0, str(Path(__file__).parent))
from cata_voces import TEXTOS  # noqa: E402

from scriptorium.alineacion import Alineador, palabras_perdidas  # noqa: E402

MOTORES = {
    "kokoro": "Kokoro 82M (la voz actual)",
    "qwen3": "Qwen3-TTS 1.7B · diseño de voz",
    "voxcpm2": "VoxCPM2 2B · diseño de voz",
    "chatterbox": "Chatterbox · español LatAm (clona la voz diseñada)",
    "omnivoice": "OmniVoice 0.6B (clona la voz diseñada)",
}
GENERO = {"m": "masculina", "f": "femenina"}


def main(carpeta: Path) -> None:
    voces: dict[tuple[str, str], dict] = {}
    with Alineador() as al:
        for wav in sorted(carpeta.glob("*.wav")):
            m = re.fullmatch(r"([a-z0-9]+)_([mf])_(narracion|lectura)", wav.stem)
            if not m:
                continue
            motor, g, clave = m.groups()
            audio, tasa = sf.read(wav)
            texto = TEXTOS[clave]
            _, oido = al.analizar(audio, tasa, texto.split())
            perdidas, faltan, _ = palabras_perdidas(texto, oido)
            registro = json.loads((carpeta / f"registro_{motor}.json").read_text()) if (carpeta / f"registro_{motor}.json").exists() else {}
            voces.setdefault((motor, g), {})[clave] = {
                "archivo": wav.name,
                "perdidas": perdidas,
                "faltan": faltan,
                "rtf": registro.get(wav.stem, {}).get("rtf"),
                "segundos": round(len(audio) / tasa, 1),
            }
            print(f"{wav.stem:<28} no se entiende {perdidas:4.0%}  {' '.join(faltan[:6])}")
    claves = sorted(voces)
    random.Random(7).shuffle(claves)
    tarjetas = []
    for n, (motor, g) in enumerate(claves):
        v = voces[(motor, g)]
        muestras = "".join(
            f'<div class="muestra"><span>{"Narración del video" if c == "narracion" else "Lectura literal (audiolibro)"}</span>'
            f'<audio controls preload="none" src="{html.escape(d["archivo"])}"></audio></div>'
            for c, d in sorted(v.items(), reverse=True)
        )
        datos = " · ".join(
            f'{"narración" if c == "narracion" else "lectura"}: no se entiende el {d["perdidas"]:.0%}'
            + (f', {d["rtf"]}× tiempo real' if d.get("rtf") else "")
            for c, d in sorted(v.items(), reverse=True)
        )
        tarjetas.append(
            f'<section><h2>Voz {chr(65 + n)} <small>{GENERO[g]}</small></h2>{muestras}'
            f'<details><summary>Revelar</summary><p><b>{html.escape(MOTORES.get(motor, motor))}</b></p><p class="dato">{datos}</p></details></section>'
        )
    textos = "".join(f"<p><b>{'Narración' if c == 'narracion' else 'Lectura'}:</b> {html.escape(t)}</p>" for c, t in TEXTOS.items())
    pagina = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cata de voces · Scriptorium</title><style>
:root{{color-scheme:dark}} body{{margin:0;background:#0b0c10;color:#f2eee6;font:16px/1.5 Inter,system-ui,sans-serif}}
main{{max-width:980px;margin:0 auto;padding:32px 16px 64px}} h1{{font:500 44px/1.1 "EB Garamond",Georgia,serif;margin:0 0 8px}}
.intro{{color:#b9b4ab}} .textos{{border-left:2px solid #e3b261;padding:4px 16px;color:#cfc9bf;font-size:15px}}
.rejilla{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;margin-top:24px}}
section{{background:#14161c;border:1px solid #262933;border-radius:14px;padding:16px}} h2{{margin:0 0 10px;font:500 26px "EB Garamond",Georgia,serif}}
h2 small{{font:500 13px Inter,sans-serif;color:#8d8a84;margin-left:6px}} .muestra span{{display:block;font-size:13px;color:#8d8a84;margin-top:8px}}
audio{{width:100%;height:36px}} details{{margin-top:12px}} summary{{cursor:pointer;color:#e3b261}} .dato{{font-size:13px;color:#b9b4ab}}
</style></head><body><main><h1>Cata de voces</h1>
<p class="intro">Las mismas dos muestras con cada voz, en orden aleatorio y sin nombre para no sesgar el oído. Escucha la narración
(¿suena viva o plana?) y la lectura literal (¿respira bien en una oración larga?). Cuando tengas favoritas, revela de qué motor son.
«No se entiende» lo mide un reconocedor de voz automático: sirve para detectar palabras comidas, no para juzgar la naturalidad.</p>
<div class="textos">{textos}</div><div class="rejilla">{"".join(tarjetas)}</div></main></body></html>"""
    (carpeta / "index.html").write_text(pagina, encoding="utf-8")
    print(f"cata: {carpeta / 'index.html'} ({len(claves)} voces)")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
