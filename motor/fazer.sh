#!/bin/bash
# fazer.sh <id>: gera, renderiza, mixa e junta -> saida/<id>.mp4
set -e
cd "$(dirname "$0")"
id=$1
python3 gerar.py planos/$id.json amostras/$id > /dev/null
python3 mix.py planos/$id.json saida/$id.m4a
cd amostras/$id
npx hyperframes render --quality looks ${GPU_FLAG:---no-browser-gpu} --workers ${WORKERS:-4} -o ../../saida/${id}_v.mp4 > ../../saida/$id.log 2>&1
cd ../..
ffmpeg -v error -y -i saida/${id}_v.mp4 -i saida/$id.m4a -map 0:v -map 1:a -c:v libx264 -crf 20 -maxrate 16M -bufsize 32M -pix_fmt yuv420p -c:a copy -shortest -movflags +faststart saida/$id.mp4
echo "PRONTO $id"
