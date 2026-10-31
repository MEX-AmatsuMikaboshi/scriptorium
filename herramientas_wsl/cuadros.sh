#!/usr/bin/env bash
# Extrae un cuadro a la mitad de cada escena del video final para revisión visual.
# Uso: cuadros.sh [slug] [capítulo]   (por defecto jaime-balmes-el-criterio, cap. 1)
slug=${1:-jaime-balmes-el-criterio}
cap=${2:-1}
v=/mnt/d/Scriptorium/02_derivados/$slug/video/explicador_cap$cap.mp4
o=/mnt/c/Users/gaber/AppData/Local/Temp/scr-stills/$slug-cap$cap
rm -rf "$o"; mkdir -p "$o"
python3 - "$slug" "$cap" <<'EOF' | while read -r n t; do
import json, sys
p = json.load(open(f'/home/gaber/.cache/scriptorium/video/{sys.argv[1]}/cap{sys.argv[2]}/props.json'))
TRANSICION, FPS = 24, 60  # video/src/movimiento.tsx: las transiciones solapan escenas consecutivas
t = 0
for i, e in enumerate(p['escenas']):
    print(f"{i:02d}_{e['tipo']} {(t + e['duracion'] / 2) / FPS:.2f}")
    print(f"{(t / FPS):6.1f}s {e['tipo']:<13} {e['duracion'] / FPS:5.1f}s  {e.get('titular', '')[:40]!r}", file=sys.stderr)
    t += e['duracion'] - TRANSICION
EOF
  ffmpeg -nostdin -v error -ss "$t" -i "$v" -frames:v 1 -vf scale=960:-1 "$o/$n.jpg"
done
ls "$o"
