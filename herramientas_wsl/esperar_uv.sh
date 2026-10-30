#!/usr/bin/env bash
# Espera (máx. ~9 min) a que termine `uv sync`.
for _ in $(seq 1 108); do
  pgrep -f "uv sync" >/dev/null || { echo "uv sync terminó"; exit 0; }
  sleep 5
done
echo "uv sync sigue corriendo; caché: $(du -sh ~/.cache/uv | cut -f1)"
