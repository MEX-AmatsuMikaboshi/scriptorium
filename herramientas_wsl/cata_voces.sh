#!/usr/bin/env bash
# Corre la cata de voces motor por motor (uno a la vez en la GPU). Uso: cata_voces.sh [motores...]
salida=/mnt/d/Scriptorium/03_biblioteca/cata
b="$HOME/.local/share/scriptorium/voces"
export HF_HUB_DOWNLOAD_TIMEOUT=120 HF_HUB_ETAG_TIMEOUT=60 TOKENIZERS_PARALLELISM=false
cd "$HOME/scriptorium" || exit 1
motores=("$@")
[ ${#motores[@]} -eq 0 ] && motores=(qwen3 voxcpm2 chatterbox omnivoice kokoro)
for motor in "${motores[@]}"; do
  echo "== $motor ($(date +%T))"
  if [ "$motor" = kokoro ]; then py="$HOME/.local/share/scriptorium/venv/bin/python"; else py="$b/$motor/bin/python"; fi
  PYTHONPATH="$HOME/scriptorium/src" "$py" herramientas_wsl/cata_voces.py "$motor" "$salida" 2>&1 \
    | grep --line-buffered -v -E 'Warning|warn|Loading|Fetching|it/s\]|^\s*$|FutureWarning|pkg_resources' \
    || true
done
echo "== fin ($(date +%T))"; ls "$salida"
