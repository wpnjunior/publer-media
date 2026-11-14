# broll.py categoria [n] [--baixar] : b-roll grátis do Mixkit (licença Mixkit: uso livre em redes, sem atribuição obrigatória).
# Wagner 14/11 00h43: "na aula, procurar b-roll que encaixe com a explicação e animações em cima do b-roll".
# Categoria = palavra simples em inglês (food, fitness, workout, doctor, laboratory...). Lista id, título e o mp4 1080p.
import re, subprocess, sys, os
os.makedirs("broll_cache", exist_ok=True)
termo = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 6
slug = re.sub(r'[^a-z0-9]+', '-', termo.lower()).strip('-')
html = subprocess.run(["curl", "-sS", "-m", "25", "-A", "Mozilla/5.0", f"https://mixkit.co/free-stock-video/{slug}/"],
                      capture_output=True, text=True).stdout
achados = []
for m in re.finditer(r'https://assets\.mixkit\.co/(?:active_storage/video_items/(\d+)/(\d+)/\1-video-360\.mp4|videos/(\d+)/\3-360\.mp4)', html):
    if m.group(1):
        vid, mp4 = m.group(1), f"https://assets.mixkit.co/active_storage/video_items/{m.group(1)}/{m.group(2)}/{m.group(1)}-video-1080.mp4"
    else:
        vid, mp4 = m.group(3), f"https://assets.mixkit.co/videos/{m.group(3)}/{m.group(3)}-1080.mp4"
    if vid not in [a[0] for a in achados]:
        achados.append((vid, mp4))
tit = {i: t for t, i in re.findall(r'/free-stock-video/([a-z0-9-]+)-(\d+)/', html)}
for vid, mp4 in achados[:n]:
    print(vid, tit.get(vid, '?'), mp4)
    if '--baixar' in sys.argv:
        r = subprocess.run(["curl", "-sSf", "-m", "90", "-A", "Mozilla/5.0", "-o", f"broll_cache/{vid}.mp4", mp4]); r.returncode and subprocess.run(["curl", "-sSf", "-m", "90", "-A", "Mozilla/5.0", "-o", f"broll_cache/{vid}.mp4", mp4.replace("-1080.mp4", "-720.mp4")])
