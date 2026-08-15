# -*- coding: utf-8 -*-
"""Busca b-roll no Pexels (licença livre, uso comercial) para o reel comentado.

Uso: python buscar_broll.py "termo em ingles" <slug> [quantos]

Baixa vídeos VERTICAIS curtos e salva um frame de cada para revisão visual —
só entra no reel o que eu olhar e aprovar.
"""
import os, sys, json, urllib.request, urllib.error, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(BASE, "broll")
os.makedirs(DEST, exist_ok=True)
KEY = open(r"C:\Users\Neves\.claude\pexels.key", encoding="utf-8").read().strip()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"

termo, slug = sys.argv[1], sys.argv[2]
quantos = int(sys.argv[3]) if len(sys.argv) > 3 else 3

url = ("https://api.pexels.com/videos/search?query=" + urllib.parse.quote(termo) +
       "&orientation=portrait&size=medium&per_page=" + str(quantos * 2))
req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": UA})
dados = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())

n = 0
for v in dados.get("videos", []):
    if n >= quantos:
        break
    if v.get("duration", 0) > 40:          # clipe longo demais não serve de b-roll
        continue
    # menor arquivo com pelo menos 1000px de largura
    arqs = sorted((f for f in v["video_files"] if (f.get("width") or 0) >= 1000),
                  key=lambda f: f.get("width") or 0)
    if not arqs:
        continue
    n += 1
    nome = f"{slug}_{n}"
    mp4 = os.path.join(DEST, nome + ".mp4")
    try:
        r = urllib.request.Request(arqs[0]["link"], headers={"User-Agent": UA})
        with urllib.request.urlopen(r, timeout=180) as resp, open(mp4, "wb") as f:
            f.write(resp.read())
    except Exception as e:
        print(f"  {nome} FALHOU: {e}")
        n -= 1
        continue
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", mp4,
                    "-frames:v", "1", "-vf", "scale=300:-1",
                    os.path.join(DEST, nome + ".jpg")], capture_output=True)
    print(f"  {nome}.mp4 | {v['duration']}s | {v['user']['name']} | {v['url']}")

print(f"{n} clipes baixados para '{termo}'")
