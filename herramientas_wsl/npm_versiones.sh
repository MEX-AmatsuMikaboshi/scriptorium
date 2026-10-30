#!/usr/bin/env bash
export PATH="$HOME/.local/bin:$PATH"
for p in remotion @remotion/cli @remotion/transitions @remotion/media react react-dom typescript @fontsource/eb-garamond @fontsource/inter markmap-cli; do
  printf '%-28s %s\n' "$p" "$(npm view "$p" version 2>/dev/null)"
done
npm view remotion peerDependencies 2>/dev/null
npm view @remotion/cli engines 2>/dev/null
