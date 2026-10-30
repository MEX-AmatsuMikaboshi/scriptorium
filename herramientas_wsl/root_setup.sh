#!/usr/bin/env bash
# Paquetes de sistema para Scriptorium (se ejecuta como root).
export DEBIAN_FRONTEND=noninteractive
grep -q '^\[user\]' /etc/wsl.conf || printf '\n[user]\ndefault=gaber\n' >> /etc/wsl.conf
apt-get update -qq
apt-get install -y -qq --no-install-recommends \
  ffmpeg espeak-ng tesseract-ocr tesseract-ocr-spa poppler-utils git curl ca-certificates unzip xz-utils jq \
  build-essential pkg-config libsndfile1 libatomic1 fonts-noto-core \
  libnss3 libdbus-1-3 libatk1.0-0 libgbm-dev libasound2t64 libxrandr2 libxkbcommon-dev libxfixes3 \
  libxcomposite1 libxdamage1 libatk-bridge2.0-0 libpango-1.0-0 libcairo2 libcups2t64 > /tmp/apt.log 2>&1
echo "apt exit: $?"
tail -n 2 /tmp/apt.log
ffmpeg -hide_banner -version | head -n 1
espeak-ng --version
echo "tesseract: $(tesseract --list-langs 2>&1 | tail -n +2 | tr '\n' ' ')"
/home/gaber/.local/node/bin/node --version
cat /etc/wsl.conf
