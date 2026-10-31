#!/usr/bin/env bash
# Instala motores de voz candidatos, cada uno en su propio venv (no tocan el venv principal).
# Uso: voces_instalar.sh qwen3 voxcpm2 chatterbox omnivoice
# torch 2.11 + torchaudio 2.11 (cu126): la última pareja con torchaudio para cu126, con soporte Pascal.
set -u
export UV_HTTP_TIMEOUT=300  # las librerías CUDA pesan cientos de MB
uv="$HOME/.local/bin/uv"
base="$HOME/.local/share/scriptorium/voces"
declare -A paquete=([qwen3]="qwen-tts" [voxcpm2]="voxcpm" [chatterbox]="chatterbox-tts" [omnivoice]="omnivoice")
mkdir -p "$base"
printf 'torch==2.11.0\ntorchaudio==2.11.0\n' > "$base/override.txt"  # algunos paquetes fijan otra versión
for motor in "$@"; do
  echo "== $motor ($(date +%T))"
  [ -x "$base/$motor/bin/python" ] || "$uv" venv -q --python 3.12 "$base/$motor"
  if ! VIRTUAL_ENV="$base/$motor" "$uv" pip install -q --override "$base/override.txt" \
      --extra-index-url https://download.pytorch.org/whl/cu126 --index-strategy unsafe-best-match \
      torch==2.11.0 torchaudio==2.11.0 soundfile "${paquete[$motor]}"; then
    echo "FALLÓ la instalación de $motor"; continue
  fi
  "$base/$motor/bin/python" -c "import torch; print('  torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_capability())"
done
echo "== fin ($(date +%T))"
