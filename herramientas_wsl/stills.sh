#!/usr/bin/env bash
# Renderiza un cuadro de cada escena de ejemplo para revisar el kit visualmente.
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/scriptorium/video" || exit 1
npm install-scripts approve esbuild >/dev/null 2>&1 && npm rebuild esbuild >/dev/null 2>&1
npx remotion browser ensure 2>&1 | tail -n 2
salida=/mnt/c/Users/gaber/AppData/Local/Temp/scr-stills
mkdir -p "$salida"
inicio=$(date +%s)
for i in 0 1 2 3 4 5 6 7 8 9; do
  frame=$((240 * i + 150))
  npx remotion still src/index.ts Explicador "$salida/escena_$i.png" --frame=$frame --scale=0.5 --log=error 2>&1 | tail -n 3
done
echo "stills en $(( $(date +%s) - inicio )) s"
ls "$salida"
