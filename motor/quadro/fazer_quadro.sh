#!/bin/bash
# fazer_quadro.sh <plano.json> <pasta_trabalho> <musica.wav>
# A pasta precisa ter voz.wav e words.json (voz_quadro.py) e assets/midia/<clipe do CTA>.
set -e
Q=$(cd "$(dirname "$0")" && pwd)
P=$(realpath "$1"); D=$(realpath "$2"); M=$(realpath "$3")
cd "$D"
cp "$P" plano.json
[ -L assets ] && rm assets
python3 "$Q/quadro.py" plano.json .
[ -L assets ] && { rm assets; mkdir -p assets; cp -r "$Q/../assets/fonts" assets/; }
npx --yes hyperframes@0.9.42 render --quality looks --no-browser-gpu --workers 4 -o video.mp4 > render.log 2>&1
python3 "$Q/quadro_mix.py" plano.json voz.wav "$M" audio.m4a
ffmpeg -v error -y -i video.mp4 -i audio.m4a -map 0:v -map 1:a -c:v libx264 -crf 20 -maxrate 16M -bufsize 32M \
  -pix_fmt yuv420p -c:a copy -shortest -movflags +faststart final.mp4
python3 "$Q/../portoes.py" final.mp4 || true
echo "PRONTO $D/final.mp4"
