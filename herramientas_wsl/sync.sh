#!/usr/bin/env bash
export PATH="$HOME/.local/bin:$PATH"
export UV_HTTP_TIMEOUT=300
cd "$HOME/scriptorium" || exit 1
git init -q 2>/dev/null
echo "== curl a pypi.nvidia.com (diagnóstico) =="
curl -s -o /dev/null -w "%{http_code} en %{time_total}s\n" --max-time 20 https://pypi.nvidia.com/ || echo "sin respuesta"
echo "== uv sync =="
uv sync --python 3.12 2>&1 | grep -v -E '^\s+(Downloading|Downloaded|Built|Building|\+|-)' | tail -n 15
echo "== prueba de PyTorch en la GPU =="
uv run python - <<'EOF'
import time

import torch

print("torch", torch.__version__, "| CUDA:", torch.cuda.is_available(), "|", torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
x = torch.randn(4096, 4096, device="cuda")
x @ x
torch.cuda.synchronize()
t = time.time()
for _ in range(20):
    x @ x
torch.cuda.synchronize()
print(f"matmul fp32: {20 * 2 * 4096**3 / (time.time() - t) / 1e12:.1f} TFLOPS")
EOF
