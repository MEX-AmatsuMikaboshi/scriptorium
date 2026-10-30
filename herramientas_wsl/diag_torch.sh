#!/usr/bin/env bash
export PATH="$HOME/.local/bin:$PATH"
echo "== índice PyTorch cu126 =="
curl -s https://download.pytorch.org/whl/cu126/nvidia-cuda-cupti-cu12/ | grep -o 'nvidia_cuda_cupti_cu12-12\.6\.80[^"#<]*' | sort -u | head -n 5
echo "== PyPI =="
curl -s https://pypi.org/simple/nvidia-cuda-cupti-cu12/ | grep -o 'nvidia_cuda_cupti_cu12-12\.6\.80[^"#<]*' | sort -u | head -n 5
echo "== reintento con mejor coincidencia entre índices =="
cd /tmp && uv run --no-project --python 3.12 --with "torch==2.14.1" --index https://download.pytorch.org/whl/cu126 --index-strategy unsafe-best-match python -c "import torch; print('torch', torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))" 2>&1 | tail -n 6
