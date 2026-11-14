#!/bin/bash
# fila_viva.sh: processa ids de saida/fila.txt um por vez (uma linha = um id), sem rodar dois renders juntos
cd /tmp/claude-0/motor
touch saida/fila.txt saida/feitos.txt
while true; do
  while pgrep -f "fila.sh react_" > /dev/null; do sleep 10; done
  id=$(grep -vxF -f saida/feitos.txt saida/fila.txt | head -1)
  if [ -z "$id" ]; then sleep 15; continue; fi
  echo "$id" >> saida/feitos.txt
  ./fila.sh "$id"
done
