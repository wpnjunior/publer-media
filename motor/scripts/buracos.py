#!/usr/bin/env python3
"""Portão de áudio: acha silêncio digital (buraco) e corte seco dentro de fala em qualquer áudio ou vídeo.
Criado em 15/11/2026 depois do "trava a língua" no segundo 27 da comparação de voz: o casar_voz.py abria
as pausas com zeros e cortava o fim do "tá?". Regra (Wagner, 13/11): nunca silêncio digital.
uso: buracos.py arquivo [arquivo...] [--min 0.05] [--ignorar-inicio 0] [--ignorar ini-fim,ini-fim]
Sai com código 1 se achar buraco >= --min segundos (fora dos trechos ignorados)."""
import sys, subprocess, argparse, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('arquivos', nargs='+')
ap.add_argument('--min', type=float, default=0.05); ap.add_argument('--ignorar', default='')
a = ap.parse_args()
ign = [tuple(map(float, p.split('-'))) for p in a.ignorar.split(',') if p]
ruim = 0
for f in a.arquivos:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    if not len(x): print(f'{f}: sem áudio'); ruim += 1; continue
    w = 160; db = 20 * np.log10(np.sqrt(np.mean(x[:len(x) // w * w].reshape(-1, w) ** 2, axis=1)) + 1e-12)
    runs, cur = [], None
    for i, v in enumerate(db):
        if v < -100:
            cur = i if cur is None else cur
        elif cur is not None:
            runs.append((cur / 100, (i - cur) / 100)); cur = None
    if cur is not None: runs.append((cur / 100, (len(db) - cur) / 100))
    # corte seco: salto de >30 dB em 10 ms saindo de fala (> -35 dB) direto para quase nada (< -80 dB)
    secos = [i / 100 for i in range(1, len(db)) if db[i - 1] > -35 and db[i] < -80]
    dentro = lambda t: any(s <= t <= e for s, e in ign)
    runs = [(s, d) for s, d in runs if d >= a.min and not dentro(s)]
    secos = [t for t in secos if not dentro(t)]
    ok = not runs and not secos
    ruim += (not ok)
    print(f"{'OK ' if ok else 'REPROVADO '}{f}: buracos {[(round(s,2), round(d,2)) for s, d in runs][:15]} cortes secos {secos[:15]}")
sys.exit(1 if ruim else 0)
