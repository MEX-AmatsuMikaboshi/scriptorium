#!/usr/bin/env bash
# Espera (máx. ~9 min) a que termine el proceso cuyo comando contiene "$1".
for _ in $(seq 1 108); do
  pgrep -f "$1" >/dev/null || { echo "terminó: $1"; exit 0; }
  sleep 5
done
echo "sigue corriendo: $1"
