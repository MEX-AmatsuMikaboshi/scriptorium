#!/usr/bin/env bash
# Mide inteligibilidad de las muestras y arma la página de la cata a ciegas.
cd "$HOME/scriptorium" || exit 1
PYTHONPATH="$HOME/scriptorium/src" "$HOME/.local/share/scriptorium/venv/bin/python" herramientas_wsl/cata_pagina.py \
  /mnt/d/Scriptorium/03_biblioteca/cata 2>&1 | grep -v -E 'Warning|warn|Loading weights|^\s*$'
