#!/usr/bin/env bash
# Re-ingesta de la demo y etapa de texto (LLM) con su director de video.
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/scriptorium" || exit 1
rm -rf /mnt/d/Scriptorium/01_canonico/jaime-balmes-el-criterio /mnt/d/Scriptorium/02_derivados/jaime-balmes-el-criterio
scriptorium ingerir "/mnt/d/Scriptorium/00_entrada/Balmes - El criterio - Capitulo I.md"
cut -c1-110 /mnt/d/Scriptorium/01_canonico/jaime-balmes-el-criterio/parrafos.jsonl
uv run --quiet python - <<'EOF'
from scriptorium import config
from scriptorium.ingesta import Obra
from scriptorium.pipeline import etapa_texto
etapa_texto([Obra.cargar("jaime-balmes-el-criterio")], config.cargar_ajustes(), True, True)
EOF
