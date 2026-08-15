# -*- coding: utf-8 -*-
"""Recorta o clone do fundo (mediapipe selfie segmenter) e salva com canal alfa.

Uso: python recortar_clone.py <video_entrada> <saida.mov> [t_inicio] [t_fim]

Sai em .mov ProRes 4444 (alfa de verdade) para o ffmpeg compor depois.
Escala para 720px de largura antes de segmentar: acima disso a máscara não
melhora e o processamento triplica.
"""
import sys, os, subprocess, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

BASE = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.join(BASE, "selfie_segmenter.tflite")
LARGURA = 720

ENTRADA = sys.argv[1]
SAIDA = sys.argv[2]
T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
T1 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0

cap = cv2.VideoCapture(ENTRADA)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
esc = LARGURA / W
w, h = LARGURA, int(round(H * esc / 2) * 2)

seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=MODELO),
    output_category_mask=False, output_confidence_masks=True))

# ffmpeg recebe RGBA cru na 1a entrada e a voz original na 2a; escreve ProRes 4444 com alfa
corte_audio = ["-ss", str(T0)] + (["-to", str(T1)] if T1 else [])
proc = subprocess.Popen([
    "ffmpeg", "-y", "-loglevel", "error",
    "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
    *corte_audio, "-i", ENTRADA,
    "-map", "0:v", "-map", "1:a?", "-shortest",
    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
    "-c:a", "pcm_s16le", SAIDA],
    stdin=subprocess.PIPE)

if T0:
    cap.set(cv2.CAP_PROP_POS_MSEC, T0 * 1000)

i, escritos = 0, 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    t = T0 + i / fps
    if T1 and t > T1:
        break
    frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    m = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB,
                             data=np.ascontiguousarray(rgb))).confidence_masks[0].numpy_view()
    m = cv2.GaussianBlur(m, (0, 0), 3)
    m = np.clip((m - 0.40) / 0.25, 0, 1)          # firma a borda, tira o halo do fundo
    alfa = (m * 255).astype(np.uint8)
    proc.stdin.write(np.dstack([rgb, alfa]).tobytes())
    i += 1
    escritos += 1

cap.release()
proc.stdin.close()
proc.wait()
print(f"recortado: {SAIDA} | {escritos} quadros | {w}x{h} @ {fps:.0f}fps")
