#!/usr/bin/env python3
"""Casa a voz do ElevenLabs (clone voz wagner) com a voz do HeyGen (Wagner comunidade).
Medido em 15/11/2026 contra 5 narrações HeyGen: ElevenLabs sai ~4-6 dB mais brilhante em 1,2-4 kHz,
mais rápido (166 x 155 ppm) e com pausas curtas (0,3-0,5 x 0,55-0,95 s).
Faz, sem crédito: (1) EQ que copia o espectro médio do HeyGen; (2) abre as pausas nas pontuações;
(3) atempo leve opcional. Tom (Hz) se acerta na geração com a tag [deep voice] [calm].
uso: casar_voz.py entrada.mp3 words.json saida.wav [--virgula 0.55] [--ponto 0.9] [--tempo 1.0] [--sem-eq]
words.json: lista de {"w","s","e"} (faster-whisper). Grava saida.words.json com os tempos novos."""
import sys, json, subprocess, argparse, numpy as np
# ganho por banda de 1/3 de oitava (dB), HeyGen menos ElevenLabs, suavizado; graves pela metade (harmônicos do tom)
EQ = {63:1,80:1,100:0,125:0,160:-1.5,200:0,250:-0.5,315:-1.5,400:0,500:0,630:0,800:0,1000:-1,1250:-2.5,
      1600:-3,2000:-3,2500:-4.5,3150:-6,4000:-5.5,5000:-2.5,6300:-2,8000:-2,10000:-3.5,12500:-5,16000:-3}
SR = 48000
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('entrada'); ap.add_argument('words'); ap.add_argument('saida')
    ap.add_argument('--virgula', type=float, default=0.55); ap.add_argument('--ponto', type=float, default=0.9)
    ap.add_argument('--tempo', type=float, default=1.0); ap.add_argument('--sem-eq', action='store_true')
    a = ap.parse_args()
    W = json.load(open(a.words))
    if isinstance(W[0], list): W = [{'s': x[0], 'e': x[1], 'w': x[2]} for x in W]
    eq = '' if a.sem_eq else "firequalizer=gain_entry='" + ';'.join(f'entry({f},{g})' for f, g in EQ.items()) + "',"
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.entrada, '-af', eq + 'aresample=48000', '-ac', '1', '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).copy()
    # abre as pausas: corta no meio do silêncio entre palavras com pontuação e completa até o alvo
    partes, novos, cur, desloc = [], [], 0, 0.0
    for i, w in enumerate(W):
        novos.append({'w': w['w'], 's': round(w['s'] + desloc, 3), 'e': round(w['e'] + desloc, 3)})
        if i == len(W) - 1: break
        fim = w['w'].rstrip()[-1:]
        alvo = a.ponto if fim in '.?!:' else a.virgula if fim in ',;' else 0
        gap = W[i + 1]['s'] - w['e']
        if alvo and gap < alvo:
            meio = int((w['e'] + gap / 2) * SR)
            partes.append(x[cur:meio]); cur = meio
            extra = alvo - gap
            partes.append(np.zeros(int(extra * SR), dtype=np.float32)); desloc += extra
    partes.append(x[cur:]); y = np.concatenate(partes)
    tmp = a.saida + '.tmp.f32'
    y.astype(np.float32).tofile(tmp)
    af = f'atempo={a.tempo}' if abs(a.tempo - 1) > 1e-3 else 'anull'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', tmp, '-af', af,
                    '-ar', str(SR), '-c:a', 'pcm_s16le', a.saida], check=True)
    import os; os.remove(tmp)
    for n in novos: n['s'] = round(n['s'] / a.tempo, 3); n['e'] = round(n['e'] / a.tempo, 3)
    json.dump(novos, open(a.saida.rsplit('.', 1)[0] + '.words.json', 'w'), ensure_ascii=False)
    span = novos[-1]['e'] - novos[0]['s']
    print(f'ok {a.saida}: {len(novos)} palavras, {span:.1f} s, {60*len(novos)/span:.0f} ppm')
main()
