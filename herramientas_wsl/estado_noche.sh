#!/usr/bin/env bash
pkill -f "http.server 8777" 2>/dev/null
echo "== procesos =="; pgrep -af "scriptorium|remotion" | grep -v estado_noche | head -n 5
echo "== obras =="; ls /mnt/d/Scriptorium/01_canonico
for d in /mnt/d/Scriptorium/02_derivados/*/; do echo "-- $d"; ls "$d"*/ 2>/dev/null | tr '\n' ' '; echo; done
python3 -c "import json;m=json.load(open('/mnt/d/Scriptorium/01_canonico/balmes-el-criterio/meta.json'));print(m['titulo'],'|',m['autor'],'|',m['parrafos'],'párrafos |',m['palabras'],'palabras |',[c['titulo'] for c in m['capitulos']])" 2>&1
grep -E "^- (añadido|inferencia|literal|parafrasis|contradiccion)|verificadas" /mnt/d/Scriptorium/02_derivados/balmes-el-criterio/texto/fidelidad.md 2>/dev/null
cd ~/scriptorium && git status --short | head -n 5
