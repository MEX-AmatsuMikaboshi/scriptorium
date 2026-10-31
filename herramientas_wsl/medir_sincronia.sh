#!/usr/bin/env bash
# Mide, con alineación forzada, el desfase entre lo que se ilumina en pantalla y lo que dice la voz,
# y si la voz sintética se comió o añadió palabras. Uso: medir_sincronia.sh <slug> [capítulo]
cd ~/scriptorium || exit 1
"$HOME/.local/share/scriptorium/venv/bin/python" - "$1" "${2:-1}" <<'EOF' 2>&1 | grep -v -E 'Warning|warn\(|^\s*$'
import json, sys
import numpy as np, soundfile as sf
from scriptorium.alineacion import Alineador, palabras_perdidas
from scriptorium.audio import para_voz

slug, cap = sys.argv[1], sys.argv[2]
trabajo = f"/home/gaber/.cache/scriptorium/video/{slug}/cap{cap}"
props = json.load(open(f"{trabajo}/props.json"))
fps = 60

def estimados(palabras, inicio, fin):  # misma fórmula que tiemposDePalabras del kit (cuadros)
    pesos = [len(p) + 3 for p in palabras]
    total, acum, salida = sum(pesos) or 1, 0, []
    for p in pesos:
        salida.append(inicio + (fin - inicio) * acum / total)
        acum += p
    return salida

errores_sub, perdidas_total = [], []
with Alineador() as al:
    for i, e in enumerate(props["escenas"]):
        if not e.get("audio"):
            continue
        audio, tasa = sf.read(f"{trabajo}/public/{e['audio']}")
        dicho = para_voz(e["narracion"], titulo=e["tipo"] == "Portada")
        palabras = dicho.split()
        tiempos, oido = al.analizar(audio, tasa, palabras)
        perdidas, faltan, sobran = palabras_perdidas(dicho, oido)
        perdidas_total.append(perdidas)
        alineadas = [t for t in tiempos if t]
        msg = f"{i:02d} {e['tipo']:<12} {len(alineadas)}/{len(palabras)} alineadas · conf {np.mean([t['confianza'] for t in alineadas]):.2f} · no se oyen {perdidas:4.0%}"
        if e["tipo"] != "Portada":  # subtítulos: estimación vieja vs voz real
            est = estimados(palabras, 4, e["voz"] - 6)
            difs = [abs(est[k] / fps - t["inicio"]) for k, t in enumerate(tiempos) if t]
            errores_sub += difs
            msg += f" · subtítulo desfasado: medio {np.mean(difs)*1000:4.0f} ms, máx {max(difs)*1000:4.0f} ms"
        print(msg)
        if perdidas > 0.08:
            print(f"     faltan: {' '.join(faltan[:14])}\n     sobran: {' '.join(sobran[:14])}")
print(f"\nSubtítulos: desfase medio {np.mean(errores_sub)*1000:.0f} ms · el {np.mean(np.array(errores_sub) > 0.25):.0%} de las palabras se ilumina con más de 250 ms de error")
print(f"Voz: en promedio no se reconoce el {np.mean(perdidas_total):.0%} de las palabras (incluye errores del reconocedor)")
EOF
