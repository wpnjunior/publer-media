#!/usr/bin/env bash
# Edição automática do vídeo diário (formato escolhido no plano). Uso:
#   bash reel_kit/diario/editar.sh <bruto.mp4> <roteiro.txt> <plano.json> <pasta_trabalho> <saida.mp4>
# Etapas: palavras com tempo (whisper) -> linha do tempo -> quadros -> render (Playwright) -> trilha/efeitos -> conferência.
# Quadros de conferência ficam em <pasta_trabalho>/conferir/ (olhe a folha antes de entregar).
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
BRUTO="$1"; ROT="$2"; PLANO="$3"; W="$4"; OUT="$5"
mkdir -p "$W/frames"
python3 -c "import faster_whisper" 2>/dev/null || pip install -q faster-whisper
python3 -c "import PIL" 2>/dev/null || pip install -q pillow
python3 "$D/transcrever.py" "$BRUTO" "$ROT" "$W/words.json"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$BRUTO")
python3 "$D/planejar.py" "$PLANO" "$W/words.json" "$DUR" "$W/timeline.json"
rm -f "$W"/frames/*.jpg
ffmpeg -y -v error -i "$BRUTO" -vf fps=25,scale=1080:1920 -q:v 3 "$W/frames/%05d.jpg"
# conferência: 16 quadros espalhados numa folha
TS=$(python3 -c "import json;t=json.load(open('$W/timeline.json'))['total'];print(','.join(f'{t*k/16+0.5:.2f}' for k in range(16)))")
node "$D/render.js" "$W" test "$W/conferir" "$TS"
python3 - "$W" <<'PY'
import glob, sys
from PIL import Image
w = sys.argv[1]; fs = sorted(glob.glob(f"{w}/conferir/t*.jpg")); W, H = 270, 480
s = Image.new("RGB", (W * 8, H * ((len(fs) + 7) // 8)))
for i, f in enumerate(fs): s.paste(Image.open(f).resize((W, H)), ((i % 8) * W, (i // 8) * H))
s.save(f"{w}/conferir/folha.jpg", quality=85)
PY
node "$D/render.js" "$W" "$W/mudo.mp4" "${PROCESSOS:-3}"
python3 "$D/mix.py" "$BRUTO" "$W/mudo.mp4" "$W/timeline.json" "$W/mix.mp4"
# 0,6 s de entrada (quadro parado + silêncio): o sabor corta 0,5 s de cada ponta e não pode comer o "Ah, doutor"
ffmpeg -y -v error -i "$W/mix.mp4" -vf "tpad=start_duration=0.6:start_mode=clone" -af "adelay=600|600" \
  -c:v libx264 -preset medium -crf 21 -maxrate 12M -bufsize 24M -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
# portão: duração e tamanho
python3 - "$BRUTO" "$OUT" <<'PY'
import subprocess, sys, os
d = lambda f: float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
b, o = d(sys.argv[1]), d(sys.argv[2]); mb = os.path.getsize(sys.argv[2]) / 1e6
print(f"bruto {b:.1f}s, editado {o:.1f}s, {mb:.1f} MB")
assert 0.9 * b <= o <= b + 7, "duração fora do esperado"
assert 1 < mb < 48, "tamanho fora do esperado (o agendador aceita até 50 MB)"
PY
echo "EDITADO OK: $OUT"
