#!/usr/bin/env bash
# setup.sh PIPELINE_DIR — installe edge-tts et les polices (Anton, Special Elite, Playfair Display) depuis npm.
set -e
P="${1:-$(pwd)}"
pip install --break-system-packages -q edge-tts 2>&1 | grep -v -i warning || true
mkdir -p "$P/fonts" && cd "$P/fonts"
for pkg in @fontsource/anton @fontsource/special-elite @fontsource/playfair-display; do
  t=$(npm pack -q "$pkg" 2>/dev/null | tail -1); d="${t%.tgz}"; mkdir -p "$d" && tar xzf "$t" -C "$d" && rm -f "$t"
done
python3 -c "import edge_tts; print('edge-tts ok')"
ls "$P/fonts"
