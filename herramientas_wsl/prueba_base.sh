#!/usr/bin/env bash
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/scriptorium" || exit 1
echo "== PyTorch =="
uv run --quiet python -c "
import time, torch
print('torch', torch.__version__, '| CUDA', torch.cuda.is_available(), '|', torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
x = torch.randn(4096, 4096, device='cuda'); x @ x; torch.cuda.synchronize(); t = time.time()
for _ in range(20): x @ x
torch.cuda.synchronize(); print(f'matmul fp32: {20*2*4096**3/(time.time()-t)/1e12:.1f} TFLOPS')
" 2>&1 | tail -n 3
echo "== ingesta =="
scriptorium ingerir "/mnt/d/Scriptorium/00_entrada/Balmes - El criterio - Capitulo I.md" 2>&1 | tail -n 3
head -c 1500 "/mnt/d/Scriptorium/01_canonico/jaime-balmes-el-criterio/parrafos.jsonl"; echo
echo "== voz (Kokoro) =="
uv run --quiet python - <<'EOF' 2>&1 | grep -v -E "Warning|warn|^\s*$" | tail -n 8
import time
from scriptorium.config import cargar_ajustes
from scriptorium.audio import Voz, para_voz, codificar, TASA
v = Voz(cargar_ajustes())
t = time.time()
a = v.decir(para_voz("El pensar bien consiste: o en conocer la verdad o en dirigir el entendimiento por el camino que conduce a ella. La verdad es la realidad de las cosas."))
dt = time.time() - t
print(f"primera frase: {len(a)/TASA:.1f} s de audio en {dt:.1f} s (incluye carga del modelo)")
t = time.time()
a2 = v.decir(para_voz("Cuando conocemos perfectamente la verdad, nuestro entendimiento se parece a un espejo en el cual vemos retratados, con toda fidelidad, los objetos como son en sí."))
dt = time.time() - t
print(f"segunda frase: {len(a2)/TASA:.1f} s de audio en {dt:.2f} s -> {len(a2)/TASA/dt:.0f}x tiempo real")
print("g2p:", type(v.pipeline.g2p).__name__, getattr(v.pipeline.g2p, "language", "?"))
from pathlib import Path
codificar(a, Path("/mnt/c/Users/gaber/AppData/Local/Temp/scr-stills/prueba_voz.mp3"))
print("ok")
EOF
