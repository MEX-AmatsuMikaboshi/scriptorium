#!/usr/bin/env bash
chrome=$(ls -d "$HOME"/scriptorium/video/node_modules/.remotion/chrome-headless-shell/linux64/*/chrome-headless-shell | head -n 1)
echo "chrome: $chrome"
cp /mnt/d/Scriptorium/02_derivados/jaime-balmes-el-criterio/interactivo/quiz.html /tmp/quiz.html
cd /tmp && timeout 40 "$chrome" --no-sandbox --disable-gpu --hide-scrollbars --window-size=1100,1300 --screenshot=/tmp/quiz.png file:///tmp/quiz.html 2>&1 | tail -n 8
echo "exit $?"; ls -la /tmp/*.png 2>/dev/null
