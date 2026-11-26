#!/bin/bash
# fila.sh id1 id2 ...: renderiza em sequência e escreve saida/<id>.gate (portões + FIM)
cd /tmp/claude-0/motor
for id in "$@"; do
  rm -f saida/$id.gate
  if ./fazer.sh $id; then python3 portoes.py saida/$id.mp4 > saida/$id.gate 2>&1; else echo "ERRO no render" > saida/$id.gate; fi
  echo FIM >> saida/$id.gate
done
