#!/usr/bin/env bash
# Servidor local de solo lectura para revisar la biblioteca en el navegador.
pkill -f "http.server 8777" 2>/dev/null
cd /mnt/d/Scriptorium && exec python3 -m http.server 8777 --bind 127.0.0.1
