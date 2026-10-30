#!/usr/bin/env bash
# Extrae cuadros del video final para revisión visual.
v=/mnt/d/Scriptorium/02_derivados/jaime-balmes-el-criterio/video/explicador_cap1.mp4
o=/mnt/c/Users/gaber/AppData/Local/Temp/scr-stills/final
rm -rf "$o"; mkdir -p "$o"
for t in 4 14 24 34 44 56 68 80 92 104 116 126 134; do
  ffmpeg -v error -ss "$t" -i "$v" -frames:v 1 -vf scale=960:-1 "$o/t$(printf '%03d' "$t").jpg"
done
ls "$o"
python3 - <<'EOF'
import json
p = json.load(open('/home/gaber/.cache/scriptorium/video/jaime-balmes-el-criterio/cap1/props.json'))
t = 0
for e in p['escenas']:
    print(f"{t/60:5.1f}s {e['tipo']:<13} {e['duracion']/60:5.1f}s  {e['titular'][:40]!r}")
    t += e['duracion']
EOF
