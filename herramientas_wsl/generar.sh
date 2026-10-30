#!/usr/bin/env bash
# Corre la fábrica completa sobre una obra, filtrando avisos ruidosos de PyTorch.
obra="${1:-balmes}"
shift
/home/gaber/.local/bin/scriptorium generar "$obra" "$@" 2>&1 \
  | grep --line-buffered -v -E 'UserWarning|super\(\)\.__init__|WeightNorm|warnings\.warn|^\s*$'
echo "salida: ${PIPESTATUS[0]}"
