#!/usr/bin/env bash
# Agrega paquetes al kit de video con versión exacta. Uso: npm_agregar.sh [paquete@versión ...] [-D ...]
# node_modules vive en el disco de Linux (rápido) y el proyecto lo enlaza; si npm se corre dentro del
# proyecto, borra ese enlace e instala en C:. Por eso se instala allá y se copian los manifiestos.
export PATH="$HOME/.local/bin:$PATH"
proyecto="$HOME/scriptorium/video"
linux="$HOME/.local/share/scriptorium/video"
mkdir -p "$linux"
cp "$proyecto/package.json" "$proyecto/package-lock.json" "$linux/"
cd "$linux" || exit 1
if [ $# -gt 0 ]; then npm install --save-exact --no-audit --no-fund "$@" 2>&1 | tail -n 3; fi
npm install --no-audit --no-fund 2>&1 | tail -n 2
cp "$linux/package.json" "$linux/package-lock.json" "$proyecto/"
if [ ! -L "$proyecto/node_modules" ]; then
  rm -rf "$proyecto/node_modules"
  ln -s "$linux/node_modules" "$proyecto/node_modules"
fi
ls -ld "$proyecto/node_modules"; ls "$linux/node_modules/@remotion"
