#!/usr/bin/env bash
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/scriptorium/video" || exit 1
npm install --no-audit --no-fund 2>&1 | tail -n 5
echo "== navegador de Remotion =="
npx remotion browser ensure 2>&1 | tail -n 3
ls node_modules/.bin | grep -E '^(remotion|markmap)$'
