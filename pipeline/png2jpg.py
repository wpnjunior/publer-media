# -*- coding: utf-8 -*-
"""A API do Instagram so aceita JPEG. Converte cards/*.png -> cards/jpg/*.jpg (rodar ao reabastecer o banco)."""
import glob, os
from PIL import Image
os.makedirs("cards/jpg", exist_ok=True)
for p in glob.glob("cards/*.png"):
    j = os.path.join("cards/jpg", os.path.basename(p)[:-4] + ".jpg")
    if not os.path.exists(j):
        Image.open(p).convert("RGB").save(j, "JPEG", quality=95, optimize=True)
        print("ok", j)
