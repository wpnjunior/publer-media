# -*- coding: utf-8 -*-
"""Junta os frames dos candidatos de b-roll num contato só, pra revisar de uma olhada."""
import os, sys, glob
from PIL import Image, ImageDraw

pasta = sys.argv[1] if len(sys.argv) > 1 else "broll"
saida = sys.argv[2] if len(sys.argv) > 2 else "contato.png"
CEL_W, CEL_H, COLS = 260, 440, 6

arqs = sorted(glob.glob(os.path.join(pasta, "*.jpg")))
linhas = (len(arqs) + COLS - 1) // COLS
folha = Image.new("RGB", (CEL_W * COLS, (CEL_H + 26) * linhas), "#11161d")
d = ImageDraw.Draw(folha)

for i, a in enumerate(arqs):
    im = Image.open(a).convert("RGB")
    im.thumbnail((CEL_W - 8, CEL_H - 8))
    x = (i % COLS) * CEL_W + (CEL_W - im.width) // 2
    y = (i // COLS) * (CEL_H + 26) + 22
    folha.paste(im, (x, y))
    d.text(((i % COLS) * CEL_W + 6, (i // COLS) * (CEL_H + 26) + 4),
           os.path.basename(a)[:-4], fill="#8bd6c8")

folha.save(saida)
print(f"{len(arqs)} candidatos -> {saida}")
