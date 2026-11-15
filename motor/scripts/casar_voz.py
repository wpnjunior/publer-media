#!/usr/bin/env python3
"""Casa a voz do ElevenLabs (clone voz wagner) com a voz do HeyGen (Wagner comunidade).
Medido em 15/11/2026 contra 5 narrações HeyGen: ElevenLabs sai ~4-6 dB mais brilhante em 1,2-4 kHz,
mais rápido (166 x 155 ppm) e com pausas curtas (0,3-0,5 x 0,55-0,95 s).
Faz, sem crédito: (1) EQ que copia o espectro médio do HeyGen; (2) abre as pausas nas pontuações com o ruído de fundo do próprio áudio, nunca silêncio digital;
(3) atempo leve opcional. Tom (Hz) se acerta na geração com a tag [deep voice] [calm].
uso: casar_voz.py entrada.mp3 words.json saida.wav [--virgula 0.55] [--ponto 0.9] [--tempo 1.0] [--sem-eq] [--eq heygen|real]
NÃO baixar o tom depois (rubberband/asetrate): medido em 15/11, -2,5 a -4,5 semitons pioram o timbre (MFCC 2,1 -> 3,5-4,6). Tom se acerta na geração.
words.json: lista de {"w","s","e"} (faster-whisper). Grava saida.words.json com os tempos novos."""
import sys, json, subprocess, argparse, numpy as np
# ganho por banda de 1/3 de oitava (dB), HeyGen menos ElevenLabs, suavizado; graves pela metade (harmônicos do tom)
EQ = {63:1,80:1,100:0,125:0,160:-1.5,200:0,250:-0.5,315:-1.5,400:0,500:0,630:0,800:0,1000:-1,1250:-2.5,
      1600:-3,2000:-3,2500:-4.5,3150:-6,4000:-5.5,5000:-2.5,6300:-2,8000:-2,10000:-3.5,12500:-5,16000:-3}
# EQ_REAL (15/11 06h30): espectro médio das 3 gravações reais do Wagner (87 min) menos o v4 cru; graves mais cheios
# (+4 a +5 dB em 63-125 Hz). Medido: distância de timbre MFCC à gravação real caiu de 2,63 para 2,13 só com este EQ.
EQ_REAL = {63:4,80:4.5,100:4.5,125:4,160:1.5,200:2,250:3,315:2.5,400:2,500:0,630:0,800:0.5,1000:1,1250:2,
           1600:0,2000:-0.5,2500:0,3150:0,4000:-0.5,5000:0,6300:0,8000:1,10000:2,12500:2,16000:3}
SR = 48000
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('entrada'); ap.add_argument('words'); ap.add_argument('saida')
    ap.add_argument('--virgula', type=float, default=0.55); ap.add_argument('--ponto', type=float, default=0.9)
    ap.add_argument('--tempo', type=float, default=1.0); ap.add_argument('--sem-eq', action='store_true')
    ap.add_argument('--eq', choices=['heygen', 'real'], default='heygen', help='alvo do timbre: heygen (voz do avatar) ou real (gravações do Wagner)')
    a = ap.parse_args()
    W = json.load(open(a.words))
    if isinstance(W[0], list): W = [{'s': x[0], 'e': x[1], 'w': x[2]} for x in W]
    tab = EQ_REAL if a.eq == 'real' else EQ
    eq = '' if a.sem_eq else "firequalizer=gain_entry='" + ';'.join(f'entry({f},{g})' for f, g in tab.items()) + "',"
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.entrada, '-af', eq + 'aresample=48000', '-ac', '1', '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).copy()
    # abre as pausas SEM silêncio digital (regra áudio sem buraco): corta no ponto mais quieto do vão
    # (o fim de palavra do whisper erra ~0,1 s; cortar no meio do vão cortava o fim do "tá") e preenche com
    # o ruído de fundo do próprio áudio (room tone), com cruzamento de 15 ms
    def rms(seg): return float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 1.0
    win = int(0.02 * SR)
    # room tone: o trecho de 0,3 s mais quieto que não seja zero absoluto
    cand = [(rms(x[i:i + int(0.3 * SR)]), i) for i in range(0, max(1, len(x) - int(0.3 * SR)), int(0.05 * SR))]
    # alvo = nível típico do fundo entre palavras (mediana dos trechos quietos, entre -80 e -45 dB)
    db = lambda v: 20 * np.log10(v + 1e-12)
    quietos = [c for c in cand if -80 < db(c[0]) < -45] or [c for c in cand if c[0] > 1e-6] or [(0, 0)]
    alvo_db = float(np.median([db(c[0]) for c in quietos]))
    _, i0 = min(quietos, key=lambda c: abs(db(c[0]) - alvo_db)); tone = x[i0:i0 + int(0.3 * SR)].copy()
    if not len(tone): tone = np.zeros(int(0.3 * SR), dtype=np.float32)
    def preenche(n):
        rep = np.resize(tone, n).astype(np.float32)
        f = min(int(0.015 * SR), n // 2)
        if f: rep[:f] *= np.linspace(0, 1, f); rep[-f:] *= np.linspace(1, 0, f)
        return rep
    partes, novos, cur, desloc = [], [], 0, 0.0
    for i, w in enumerate(W):
        novos.append({'w': w['w'], 's': round(w['s'] + desloc, 3), 'e': round(w['e'] + desloc, 3)})
        if i == len(W) - 1: break
        fim = w['w'].rstrip()[-1:]
        alvo = a.ponto if fim in '.?!:' else a.virgula if fim in ',;' else 0
        gap = W[i + 1]['s'] - w['e']
        if alvo and gap < alvo:
            # procura o ponto mais quieto entre o fim da palavra (+0,05 s) e o início da próxima
            ini = int((w['e'] + 0.05) * SR); fimv = int(W[i + 1]['s'] * SR) - win
            if fimv <= ini: ini, fimv = int(w['e'] * SR), int(W[i + 1]['s'] * SR)
            pts = [(rms(x[j:j + win]), j) for j in range(ini, max(ini + 1, fimv), int(0.005 * SR))]
            _, corte = min(pts); corte += win // 2
            if corte <= cur: continue
            partes.append(x[cur:corte]); cur = corte
            extra = alvo - gap
            partes.append(preenche(int(extra * SR))); desloc += extra
            # palavras depois do corte andam junto (ajuste do tempo das próximas é feito pelo desloc)
    partes.append(x[cur:]); y = np.concatenate(partes)
    tmp = a.saida + '.tmp.f32'
    y.astype(np.float32).tofile(tmp)
    af = f'atempo={a.tempo}' if abs(a.tempo - 1) > 1e-3 else 'anull'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', tmp, '-af', af,
                    '-ar', str(SR), '-c:a', 'pcm_s16le', a.saida], check=True)
    import os; os.remove(tmp)
    # portão: nada de silêncio digital nem corte seco (buracos.py); se reprovar, o script falha
    import os as _os
    r = subprocess.run([sys.executable, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'buracos.py'), a.saida])
    if r.returncode: sys.exit('casar_voz: REPROVADO no portão de buracos, não use este arquivo')
    for n in novos: n['s'] = round(n['s'] / a.tempo, 3); n['e'] = round(n['e'] / a.tempo, 3)
    json.dump(novos, open(a.saida.rsplit('.', 1)[0] + '.words.json', 'w'), ensure_ascii=False)
    span = novos[-1]['e'] - novos[0]['s']
    print(f'ok {a.saida}: {len(novos)} palavras, {span:.1f} s, {60*len(novos)/span:.0f} ppm')
main()
