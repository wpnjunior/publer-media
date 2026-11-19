#!/bin/bash
# remix.sh id...: refaz só o áudio (mix.py) e junta com o vídeo já renderizado (saida/<id>_v.mp4); roda portões.
cd "$(dirname "$0")"
for id in "$@"; do
  python3 audio_plano.py planos/$id.json || { echo "AUDIO_PLANO REPROVADO $id"; continue; }
  python3 mix.py planos/$id.json saida/$id.m4a > /dev/null
  ffmpeg -v error -y -i saida/${id}_v.mp4 -i saida/$id.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart saida/$id.mp4
  python3 portoes.py saida/$id.mp4 > saida/$id.gate 2>&1; echo FIM >> saida/$id.gate
  echo "== $id"; cat saida/$id.gate
done
