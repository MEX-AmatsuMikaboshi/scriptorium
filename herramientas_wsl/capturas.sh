#!/usr/bin/env bash
# Capturas de las páginas HTML con el Chromium headless que instaló Remotion.
chrome=$(ls -d "$HOME"/scriptorium/video/node_modules/.remotion/chrome-headless-shell/linux64/*/chrome-headless-shell | head -n 1)
o=/mnt/c/Users/gaber/AppData/Local/Temp/scr-stills/html
mkdir -p "$o"
d=/mnt/d/Scriptorium
captura() {  # nombre url ancho alto
  timeout 40 "$chrome" --no-sandbox --headless --hide-scrollbars --disable-gpu --allow-file-access-from-files \
    --autoplay-policy=user-gesture-required --window-size="$3,$4" --timeout=6000 --screenshot="$o/$1.png" "$2" >/dev/null 2>&1
  echo "$1: $(stat -c %s "$o/$1.png" 2>/dev/null || echo FALLA)"
}
captura biblioteca "file://$d/03_biblioteca/index.html" 1280 1500
captura lector "file://$d/02_derivados/jaime-balmes-el-criterio/interactivo/lector.html" 1100 1300
captura textos "file://$d/02_derivados/jaime-balmes-el-criterio/interactivo/textos.html" 1100 1300
captura quiz "file://$d/02_derivados/jaime-balmes-el-criterio/interactivo/quiz.html" 1100 1300
captura mapa "file://$d/02_derivados/jaime-balmes-el-criterio/interactivo/mapa.html" 1400 900
captura movil "file://$d/03_biblioteca/index.html" 390 1400
