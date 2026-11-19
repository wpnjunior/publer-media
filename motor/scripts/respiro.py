#!/usr/bin/env python3
"""respiro.py <plano_id> [--fator 0.8846] [--pausa 0.7] [--engine rubberband|atempo] [--sem-loop-musica] [--saida ID]

Deixa um react pronto mais calmo SEM gastar crédito (Wagner, 14/11 07h05: "estou falando um pouco rápido...
está faltando uma pausa maior de uma frase para outra"). Regra: ritmo de 1,15x e pausa >= 0,7 s entre frases.

Como funciona
1. Narração = entradas de audio.voz com arquivo *_voz.wav (sem _calmo). Mídia de velocidade fixa = vídeo com
   boca ou viral: entradas de voz/viral que não são *_voz.wav e camadas de vídeo que não são fundo
   (fundo = nome com br_, _b_ ou _blur). Pedaço de narração coberto por mídia fixa (rosto do HeyGen dublando
   o próprio _voz.wav, dublagem/contexto por cima do viral) fica PROTEGIDO: velocidade 1, só anda no tempo.
2. Cada arquivo de narração vira <nome>_calmo.wav (+ .words.json): pedaços livres esticados pelo fator
   (rubberband; os arquivos já estão a 1,3x, então 0,8846 = 1,15/1,3), pedaços protegidos copiados, e no fim
   de cada frase (palavra que termina em . ? ! :) a pausa é aberta até dar --pausa NA LINHA DO TEMPO (conta
   o que vem depois: outra frase, rosto, CTA), preenchida com o próprio ar da gravação (nunca zero digital).
3. Mapa de tempo por partes (antigo -> novo) da linha do tempo inteira: dentro da narração segue o arquivo
   novo; fora dela, inclinação 1 (rosto, viral, entrada só se deslocam).
4. O mapa vale para tudo: t/d das camadas, tempos internos (fisio, desenho, abas, zoom, itens, pinos, rotas,
   câmera do mapa, t_escolha), legenda (esconde, ys), efeitos sonoros e trilha (repetida se ficar curta).
   Camada parada numa pausa ganha a duração nova; flash/glitch só andam; b-roll que ficaria sem filme recua o ms.
5. Grava planos/<id>_calmo.json (nunca sobrescreve), roda audio_plano.py e leitura.py e mede palavras/min e
   pausa entre frases antes e depois.
"""
import argparse, json, math, os, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

MOTOR = Path(__file__).resolve().parent.parent
os.chdir(MOTOR)
SR = 44100
FIM = ('.', '?', '!', ':', '…')
SO_ANDAM = ('flash', 'glitch')  # efeitos instantâneos: só andam no tempo
EPS = 1e-6


def fim_frase(w):
    return w.strip().rstrip('"\'”)»').endswith(FIM)


def fundo_video(src):
    n = Path(src).name
    return bool(re.search(r'(^|_)br_|_b_|_blur', n))


_DUR = {}
def dur_arquivo(src):
    if src not in _DUR:
        p = src if ('/' in src or src.endswith(('.wav', '.m4a', '.mp4', '.mp3'))) else f"assets/som/{src}.m4a"
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                           capture_output=True, text=True).stdout.strip()
        try:
            _DUR[src] = float(r)
        except ValueError:
            _DUR[src] = None
    return _DUR[src]


def ler(src, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", src] + (["-af", af] if af else []) + ["-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    b = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(b, dtype=np.int16).astype(np.float32) / 32768


def gravar(y, path):
    y = np.clip(y, -1, 1)
    with wave.open(str(path), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((y * 32767).astype('<i2').tobytes())


def rms_db(a):
    return 20 * math.log10(max(1e-7, float(np.sqrt(np.mean(a * a))) if len(a) else 1e-7))


def uniao(iv):
    out = []
    for a, b in sorted(iv):
        if out and a <= out[-1][1] + 1e-3:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


# ---------------------------------------------------------------- narração calma (um arquivo)
class Calmo:
    """Mc(t no arquivo antigo) -> t no arquivo novo. Pedaços: livres (inclinação k) e protegidos (1); pausas = saltos."""

    def __init__(self, src, palavras, fator, engine, protegidos):
        self.src = src
        self.ws = json.load(open(palavras))
        self.x = ler(src)
        af = f"atempo={fator}" if engine == 'atempo' else f"rubberband=tempo={fator}:transients=mixed:pitchq=quality"
        self.y = ler(src, af)
        self.k = len(self.y) / len(self.x)
        fim = len(self.x) / SR
        self.prot = [[max(0, a), min(fim, b)] for a, b in uniao(protegidos) if b - a > 0.02]
        # pedaços cobrindo o arquivo todo: (a, b, inclinação)
        pc, t = [], 0.0
        for a, b in self.prot:
            if a > t: pc.append((t, a, self.k))
            pc.append((a, b, 1.0)); t = b
        if t < fim: pc.append((t, fim, self.k))
        self.pc = pc
        self.ins = []  # (x do corte no áudio, j do salto no mapa, segundos, nível dB) -- tempos do arquivo antigo
        self._ar_pool()

    def protegido(self, t):
        return any(a - EPS <= t < b - EPS for a, b in self.prot)

    def Mc(self, t, esquerda=False):
        acc = 0.0
        for a, b, s in self.pc:
            if t >= b:
                acc += (b - a) * s
            else:
                acc += max(0.0, t - a) * s
                break
        if esquerda:
            return acc + sum(f for _, j, f, _ in self.ins if j < t - EPS)
        return acc + sum(f for _, j, f, _ in self.ins if j <= t + EPS)

    def _ar_pool(self):
        """ar da própria gravação: miolo das pausas, quadros de 10 ms abaixo de -46 dB."""
        y, k, fr, runs = self.y, self.k, 441, []
        for a, b in zip(self.ws, self.ws[1:]):
            i0, i1 = int((a['e'] * k + 0.03) * SR), int((b['s'] * k - 0.03) * SR)
            if i1 - i0 < int(0.05 * SR):
                continue
            cur = []
            for i in range(i0, i1 - fr, fr):
                q = y[i:i + fr]
                if rms_db(q) < -46:
                    cur.append(q)
                else:
                    if len(cur) >= 4: runs.append(np.concatenate(cur))
                    cur = []
            if len(cur) >= 4: runs.append(np.concatenate(cur))
        self.ar = self._colar(runs) if sum(len(r) for r in runs) > 0.12 * SR else None

    def silencio(self, lo, hi):
        """maior trecho quieto (< -46 dB em quadros de 10 ms, tolerando 20 ms de ruído) entre lo e hi."""
        fr = 441
        i0, i1 = max(0, int(lo * SR)), min(len(self.x), int(hi * SR))
        q = [rms_db(self.x[i:i + fr]) < -46 for i in range(i0, i1 - fr, fr)]
        runs, ini, ruim = [], None, 0
        for n, ok in enumerate(q + [False, False, False]):
            if ok:
                if ini is None: ini = n
                ruim = 0
            elif ini is not None:
                ruim += 1
                if ruim > 2:
                    fim = n - ruim + 1
                    if fim - ini >= 6: runs.append((ini, fim))
                    ini, ruim = None, 0
        if not runs:
            return None
        a, b = max(runs, key=lambda r: r[1] - r[0])
        return (i0 + a * fr) / SR, (i0 + b * fr) / SR

    def ponto_quieto(self, lo, hi):
        """quadro mais quieto entre lo e hi (tempo do arquivo antigo), medido no áudio que vai sair."""
        best, bx = 9e9, lo
        n = max(1, int((hi - lo) * SR / 110))
        for j in range(n + 1):
            t = lo + (hi - lo) * j / n
            if self.protegido(t):
                continue
            i = int(t * self.k * SR)
            v = rms_db(self.y[max(0, i - 220):i + 220])
            if v < best:
                best, bx = v, t
        return bx, best

    def _montar_eventos(self, rng):
        cortes = sorted(self.ins)
        ev = []  # sequência de ('voz', a, b, s) e ('ar', f, nv)
        for a, b, s in self.pc:
            pontos = sorted(set([a, b] + [x for x, _, _, _ in cortes if a - EPS <= x <= b + EPS]))
            for p0, p1 in zip(pontos, pontos[1:]):
                if p1 - p0 > EPS:
                    ev.append(('voz', p0, p1, s))
        # insere os 'ar' depois do pedaço de voz que termina em x (ou antes do primeiro, se x == 0)
        out = []
        usados = set()
        for e in ev:
            out.append(e)
            for j, (x, _, f, nv) in enumerate(cortes):
                if j not in usados and abs(e[2] - x) < 1e-4:
                    out.append(('ar', f, nv)); usados.add(j)
        audio = []
        xf = int(0.008 * SR)
        prev_s = None
        for e in out:
            if e[0] == 'ar':
                audio.append(self._fade(self._ar(int(round(e[1] * SR)), e[2], rng), True, True))
                prev_s = None
                continue
            _, p0, p1, s = e
            src, f = (self.x, 1.0) if s == 1.0 else (self.y, self.k)
            i0, i1 = int(round(p0 * f * SR)), int(round(p1 * f * SR))
            seg = src[i0:i1].copy()
            if audio and prev_s is not None and prev_s != s and len(seg) > 2 * xf and len(audio[-1]) > 2 * xf:
                # troca de velocidade no meio da fala: cruzamento curto (o pedaço novo começa xf antes)
                pre = src[max(0, i0 - xf):i0]
                if len(pre) == xf:
                    r = np.linspace(0, 1, xf, dtype=np.float32)
                    audio[-1][-xf:] = audio[-1][-xf:] * (1 - r) + pre * r
            elif audio and prev_s is None:
                seg = self._fade(seg, True, False)
            if any(abs(p1 - x) < 1e-4 for x, _, _, _ in cortes):
                seg = self._fade(seg, False, True)
            audio.append(seg)
            prev_s = s
        return np.concatenate(audio) if audio else np.zeros(1, np.float32)

    @staticmethod
    def _colar(runs, xf=int(0.012 * SR)):
        out = runs[0].copy()
        for r in runs[1:]:
            if len(r) <= 2 * xf or len(out) <= 2 * xf:
                out = np.concatenate([out, r]); continue
            ramp = np.linspace(0, 1, xf, dtype=np.float32)
            mid = out[-xf:] * (1 - ramp) + r[:xf] * ramp
            out = np.concatenate([out[:-xf], mid, r[xf:]])
        return out

    @staticmethod
    def _fade(a, fin, fout, n=int(0.006 * SR)):
        a = a.copy()
        if len(a) > 2 * n:
            if fin: a[:n] *= np.linspace(0, 1, n, dtype=np.float32)
            if fout: a[-n:] *= np.linspace(1, 0, n, dtype=np.float32)
        return a

    def _ar(self, n, nivel, rng):
        alvo = min(-50.0, max(-66.0, nivel if nivel < 900 else -58.0))
        if self.ar is None:  # sem ar aproveitável: ruído rosa bem baixo (nunca zero digital)
            w = rng.standard_normal(n + 2000).astype(np.float32)
            b = np.cumsum(w); b = b - np.convolve(b, np.ones(400) / 400, 'same'); seg = b[1000:1000 + n]
        else:
            ar = self.ar
            o = int(rng.integers(0, max(1, len(ar) - 1)))
            seg = np.concatenate([ar[o:]] + [ar] * (n // len(ar) + 2))[:n]
        g = 10 ** (alvo / 20) / max(1e-7, float(np.sqrt(np.mean(seg * seg))))
        return (seg * g).astype(np.float32)

    def palavras_novas(self):
        return [dict(w, s=round(self.Mc(w['s']), 3), e=round(self.Mc(w['e'], esquerda=True), 3)) for w in self.ws]


# ---------------------------------------------------------------- métricas
_PCM = {}
def trilha_voz(plano):
    """só as falas (voz + viral) montadas na linha do tempo, mono 44,1 kHz: régua da pausa de verdade."""
    y = np.zeros(int((plano['dur'] + 1) * SR), np.float32)
    for v in (plano['audio'].get('voz') or []) + (plano['audio'].get('viral') or []):
        if v['src'] not in _PCM:
            _PCM[v['src']] = ler(v['src'])
        x = _PCM[v['src']]
        i0, n = int(v.get('ms', 0) * SR), int(v['d'] * SR)
        seg = x[i0:i0 + n] * v.get('gain', 1.0)
        o = int(v['t'] * SR)
        y[o:o + len(seg)] += seg[:max(0, len(y) - o)]
    return y


def metricas(plano, trechos):
    """trechos: listas de palavras (linha do tempo) de narração contínua. ppm pelos tempos das palavras;
    pausa entre frases medida no áudio (maior trecho < -46 dB entre o fim da frase e a palavra seguinte)."""
    y = trilha_voz(plano)
    nw = sum(len(ws) for ws in trechos)
    fala, pausas = 0.0, []
    for ws in trechos:
        if not ws: continue
        fala += ws[-1]['e'] - ws[0]['s']
        for a, b in zip(ws, ws[1:]):
            if not fim_frase(a['w']): continue
            lo, hi = a['e'] - 0.15, min(b['e'] - 0.05, b['s'] + 1.2)
            fr = 441; i0 = max(0, int(lo * SR))
            q = [rms_db(y[i:i + fr]) < -46 for i in range(i0, int(hi * SR) - fr, fr)]
            best = run = ruim = 0
            for ok in q:
                if ok: run += 1 + ruim; ruim = 0
                else:
                    ruim += 1
                    if ruim > 2: run = ruim = 0
                best = max(best, run)
            pausas.append(best * 0.01)
    return dict(palavras=nw, fala_s=round(fala, 2), ppm=round(nw / fala * 60, 1) if fala else 0,
                pausas=len(pausas), pausa_media=round(sum(pausas) / len(pausas), 2) if pausas else None,
                pausa_min=round(min(pausas), 2) if pausas else None,
                abaixo=sum(1 for p in pausas if p < 0.65))


def palavras_linha(plano, so_narr):
    """palavras na linha do tempo, como legendas() do gerar.py; marca de que entrada vieram."""
    out = []
    for i, v in enumerate(plano['audio'].get('voz') or []):
        if not v.get('palavras'):
            continue
        ws = json.load(open(v['palavras']))
        a, b = v.get('ms', 0), v.get('ms', 0) + v['d']
        for w in ws:
            if w['s'] >= a - .05 and w['e'] <= b + .2 and w['w'].strip():
                out.append(dict(w=w['w'], s=w['s'] - a + v['t'], e=min(w['e'], b) - a + v['t'], i=i,
                                ss=w['s'], se=w['e']))
    out.sort(key=lambda w: w['s'])
    return out


def blocos_narr(ws, narr_i):
    """agrupa palavras de narração em blocos contínuos (sem rosto/viral falando no meio)."""
    blocos, cur = [], []
    for w in ws:
        if w['i'] in narr_i:
            cur.append(w)
        else:
            if cur: blocos.append(cur)
            cur = []
    if cur: blocos.append(cur)
    return blocos


# ---------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pid')
    ap.add_argument('--fator', type=float, default=round(1.15 / 1.3, 4))
    ap.add_argument('--pausa', type=float, default=0.7)
    ap.add_argument('--engine', default='rubberband', choices=['rubberband', 'atempo'])
    ap.add_argument('--sem-loop-musica', action='store_true', help='não repete a trilha quando o trecho fica maior que o arquivo')
    ap.add_argument('--saida', default=None, help='id do plano novo (padrão <id>_calmo)')
    a = ap.parse_args()
    pid = a.pid
    novo_id = a.saida or f"{pid}_calmo"
    if novo_id == pid:
        sys.exit("não sobrescrevo o plano original")
    P = json.load(open(f"planos/{pid}.json"))
    A = P['audio']
    avisos = []

    def narr(v):
        return v['src'].endswith('.wav') and '_voz' in Path(v['src']).stem and '_calmo' not in v['src']

    # mídia de velocidade fixa (linha do tempo)
    fixos = []
    for v in (A.get('voz') or []):
        if not narr(v): fixos.append((v['t'], v['t'] + v['d'], Path(v['src']).name))
    for v in (A.get('viral') or []):
        fixos.append((v['t'], v['t'] + v['d'], Path(v['src']).name))
    for c in P['camadas']:
        if c.get('tipo') in ('video', 'recorte') and c.get('d') and not fundo_video(c['src']):
            fixos.append((c['t'], c['t'] + c['d'], Path(c['src']).name))

    # trechos de narração e pedaços protegidos (no tempo do arquivo)
    segs, prot = [], {}
    for i, v in enumerate(A.get('voz') or []):
        if not narr(v): continue
        t0, t1, ms = v['t'], v['t'] + v['d'], v.get('ms', 0)
        cob = []
        for x, y, n in fixos:
            lo, hi = max(t0, x), min(t1, y)
            if hi - lo > 0.02:
                cob.append((ms + lo - t0, ms + hi - t0, n))
        tot = sum(b - a for a, b in uniao([(p, q) for p, q, _ in cob]))
        nome = Path(v['src']).name
        if tot >= v['d'] - 0.05:
            avisos.append(f"{nome} t={t0:.2f} inteiro sob {cob[0][2]}: só anda (velocidade antiga)")
            continue
        for p, q, n in cob:
            avisos.append(f"{nome} t={t0 + p - ms:.2f}-{t0 + q - ms:.2f} sob {n}: pedaço protegido (velocidade antiga)")
        prot.setdefault(v['src'], []).extend((p, q) for p, q, _ in cob)
        segs.append(dict(i=i, t=t0, d=v['d'], ms=ms, src=v['src'],
                         pal=v.get('palavras') or v['src'][:-4] + '.words.json'))
    segs.sort(key=lambda s: s['t'])
    for s0, s1 in zip(segs, segs[1:]):
        if s1['t'] < s0['t'] + s0['d'] - 0.05:
            avisos.append(f"narração sobreposta em {s1['t']:.2f}: segundo trecho só anda")
            s1['fora'] = True
    segs = [s for s in segs if not s.get('fora')]
    if not segs:
        print("nenhum trecho de narração esticável", *avisos, sep='\n  ')
        sys.exit(2)

    calmos = {}
    for src in dict.fromkeys(s['src'] for s in segs):
        pal = next(s['pal'] for s in segs if s['src'] == src)
        calmos[src] = Calmo(src, pal, a.fator, a.engine, prot.get(src, []))

    def prep():
        for s in segs:
            C = calmos[s['src']]
            s['m0'] = C.Mc(s['ms'])
            s['L'] = C.Mc(s['ms'] + s['d'], esquerda=True) - s['m0']

    def M(T, esquerda=False):
        sh = 0.0
        for s in segs:
            if T < s['t'] - EPS:
                return T + sh
            if T <= s['t'] + s['d'] + EPS:
                C = calmos[s['src']]
                return s['t'] + sh + C.Mc(s['ms'] + T - s['t'], esquerda) - s['m0']
            sh += s['L'] - s['d']
        return T + sh

    # 1ª passada: só esticado. Pausas: fim de frase da narração -> próxima palavra falada (qualquer fonte)
    prep()
    narr_i = {s['i']: s for s in segs}
    W = palavras_linha(P, None)
    nao_abertas, novas = [], []
    for w, nx in zip(W, W[1:]):
        if w['i'] not in narr_i or not fim_frase(w['w']):
            continue
        s = narr_i[w['i']]; C = calmos[s['src']]
        fim_seg = s['ms'] + s['d']
        tl = lambda src_t: s['t'] + src_t - s['ms']
        mesmo = nx['i'] == w['i'] and nx['ss'] >= w['se'] - 0.01
        # pausa de verdade pela energia (os words.json antigos não têm lacuna: a pausa fica dentro da palavra seguinte)
        fim_jan = min(nx['se'] - 0.05, nx['ss'] + 0.8) if mesmo else fim_seg
        run = C.silencio(w['se'] - 0.15, min(fim_jan, fim_seg))
        if run:
            r0, r1 = run
            gap = (M(tl(r1)) if mesmo else M(nx['s'])) - M(tl(r0), esquerda=True)
        else:
            r0, r1 = w['se'], (nx['ss'] if mesmo else fim_seg)
            gap = M(nx['s']) - M(w['e'], esquerda=True)
        falta = a.pausa + 0.03 - gap  # 30 ms de folga: a régua de energia arredonda em quadros de 10 ms
        if falta <= 0.04:
            continue
        # corte do áudio: começo da pausa real, no quadro mais quieto; salto do mapa: no máximo no 's' da palavra
        # seguinte (cartela marcada nela vai junto com ela, depois da pausa)
        lo = max(r0, w['se'] - 0.15) + 0.01
        hi = lo + max(0.02, min(0.11, (r1 - r0) * 0.5))
        for pa, pb in C.prot:
            if pa - EPS <= lo < pb:
                lo = pb + 0.002; hi = max(hi, lo + 0.02)
        hi = min(hi, fim_seg - 0.003, max(r1, lo) - 0.005 if mesmo else fim_seg - 0.003)
        if hi <= lo or C.protegido(lo) or (mesmo and lo > r1 - 0.02):
            nao_abertas.append(f"{w['s']:.2f} '{w['w']}' (rosto/viral cobre a pausa ou corte colado)")
            continue
        x, nv = C.ponto_quieto(lo, hi)
        j = min(x, nx['ss']) if mesmo else x
        j = max(j, w['se'], lo - 0.01)  # nunca dentro de pedaço protegido
        novas.append((C, (x, j, falta, nv)))  # aplica só no fim: as lacunas são medidas sem pausa nenhuma
    for C, ins in novas:
        C.ins.append(ins)
    prep()

    # grava os áudios novos
    for src, C in calmos.items():
        out = Path(src).with_name(Path(src).stem + '_calmo.wav')
        y = C._montar_eventos(np.random.default_rng(7))
        gravar(y, out)
        json.dump(C.palavras_novas(), open(out.with_suffix('.words.json'), 'w'), ensure_ascii=False)
        C.out, C.out_pal = str(out), str(out.with_suffix('.words.json'))
        esperado = C.Mc(len(C.x) / SR)
        print(f"voz {Path(src).name}: x{C.k:.4f}, {len(C.ins)} pausas abertas (+{sum(f for _, _, f, _ in C.ins):.2f}s), "
              f"{len(C.prot)} pedaço(s) protegido(s), ar {'da gravação' if C.ar is not None else 'ruído rosa'}, "
              f"{len(y) / SR:.2f}s (mapa {esperado:.2f}s) -> {out}")
        if abs(len(y) / SR - esperado) > 0.03:
            avisos.append(f"{out.name}: duração {len(y) / SR:.3f} difere do mapa {esperado:.3f}")

    r3 = lambda v: round(v, 3)
    MD = lambda T, d: M(T + d, esquerda=True) - M(T)
    Q = json.loads(json.dumps(P))
    Q['id'] = novo_id

    for c in Q['camadas']:
        if 't' not in c:
            continue
        t0 = c['t']; nt = M(t0)
        tipo = c.get('tipo')
        d_antigo = c.get('d') or 0
        if c.get('d') is not None and tipo not in SO_ANDAM:
            c['d'] = r3(MD(t0, c['d']))
        def rel(x): return r3(M(t0 + x) - nt)
        if tipo == 'fisio':
            for k in ('orgaos', 'pulsos'):
                for o in c.get(k, []):
                    if 't' in o: o['t'] = rel(o['t'])
            for k in ('fluxos', 'encolhe'):
                for o in c.get(k, []):
                    ot = o.get('t', 0)
                    if 'd' in o: o['d'] = r3(MD(t0 + ot, o['d']))
                    o['t'] = rel(ot)
        if tipo == 'desenho':
            for f in c.get('formas', []):
                if 't' in f: f['t'] = rel(f['t'])
        for k in ('t_escolha', 't_botoes', 'pausa'):
            if isinstance(c.get(k), (int, float)) and not isinstance(c.get(k), bool):
                c[k] = r3(M(c[k]))
        if 'abas' in c:
            c['abas'] = [[r3(M(x[0]))] + list(x[1:]) for x in c['abas']]
        for it in c.get('itens', []) or []:
            if isinstance(it, dict):
                if 't' in it: it['t'] = r3(M(it['t']))
                if 'marca' in it and not isinstance(it['marca'], bool): it['marca'] = r3(M(it['marca']))
        for ln in c.get('linhas', []) or []:
            g = ln.get('grifo') if isinstance(ln, dict) else None
            if isinstance(g, (int, float)) and not isinstance(g, bool): ln['grifo'] = r3(M(g))
        for k in ('pinos', 'notif'):
            for o in c.get(k, []) or []:
                if 't' in o: o['t'] = r3(M(o['t']))
        for o in c.get('rotas', []) or []:
            if 't' in o:
                if 'dur' in o: o['dur'] = r3(MD(o['t'], o['dur']))
                o['t'] = r3(M(o['t']))
        if tipo == 'mapa' and 'camera' in c:
            c['camera'] = [[r3(M(k[0]))] + list(k[1:4]) + [r3(MD(k[0], k[4]))] + list(k[5:]) for k in c['camera']]
        if 'zoom' in c:
            c['zoom'] = [[r3(M(z[0])), z[1], r3(MD(z[0], z[2]))] + list(z[3:]) for z in c['zoom']]
        c['t'] = r3(nt)
        if tipo in ('video', 'recorte') and c.get('d'):
            md = dur_arquivo(c['src']); ms = c.get('ms', 0)
            if not fundo_video(c['src']):
                if c['d'] > d_antigo + 0.02:
                    avisos.append(f"vídeo de boca {Path(c['src']).name} t={c['t']} ficou {c['d'] - d_antigo:.2f}s mais longo (conferir)")
            elif md and ms + c['d'] > md - 0.02:
                c['ms'] = r3(max(0.0, md - c['d'] - 0.05))
                if c['d'] > md - 0.05:
                    avisos.append(f"fundo {Path(c['src']).name} t={c['t']}: {c['d']:.2f}s > arquivo {md:.2f}s (vai encurtar)")

    lg = Q.get('legenda') or {}
    if 'esconde' in lg: lg['esconde'] = [[r3(M(x)), r3(M(y, True))] for x, y in lg['esconde']]
    if 'ys' in lg: lg['ys'] = [[r3(M(x)), r3(M(y, True)), yy] for x, y, yy in lg['ys']]

    QA = Q['audio']
    for i, v in enumerate(QA.get('voz') or []):
        if i in narr_i:
            s = narr_i[i]; C = calmos[s['src']]
            v.update(src=C.out, palavras=C.out_pal, ms=r3(s['m0']), d=r3(s['L']), t=r3(M(s['t'])))
        else:
            v['t'] = r3(M(v['t']))
    for v in QA.get('viral') or []:
        v['t'] = r3(M(v['t']))
    mus = []
    for m in QA.get('musica') or []:
        t0 = m['t']; m['t'] = r3(M(t0)); m['d'] = r3(MD(t0, m['d']))
        md = dur_arquivo(m['src']); ms = m.get('ms', 0)
        if md and not a.sem_loop_musica and ms + m['d'] > md - 0.05:
            fade = m.get('fade', .4); t, resto, first = m['t'], m['d'], True
            while resto > 0.05:
                pedaco = min(resto, md - (ms if first else 0) - 0.05)
                mus.append(dict(m, t=r3(t), ms=(ms if first else 0), d=r3(pedaco)))
                if pedaco >= resto - 1e-6: break
                t += pedaco - fade; resto -= pedaco - fade; first = False
            avisos.append(f"trilha {m['src']} ({md:.1f}s) repetida para cobrir {m['d']:.1f}s")
        else:
            mus.append(m)
    if 'musica' in QA: QA['musica'] = mus
    for s in QA.get('sfx') or []:
        t0 = s['t']; s['t'] = r3(M(t0))
        if s.get('d'):
            nd = MD(t0, s['d']); fd = dur_arquivo(s['src'])
            s['d'] = r3(min(nd, fd) if fd else nd)
    Q['dur'] = r3(M(P['dur']))
    for c in Q['camadas']:
        if c.get('tipo') == 'fundo' and c.get('t', 0) == 0 and c.get('d', 0) > Q['dur']:
            c['d'] = Q['dur']

    json.dump(Q, open(f"planos/{novo_id}.json", 'w'), ensure_ascii=False, indent=1)

    # medidas (palavras como a legenda as vê, blocos de narração contínua)
    ni_q = {s['i'] for s in segs}
    ma = metricas(P, blocos_narr(palavras_linha(P, None), ni_q))
    mb = metricas(Q, blocos_narr(palavras_linha(Q, None), ni_q))
    print(f"plano {pid} -> planos/{novo_id}.json")
    print(f"duração {P['dur']:.2f}s -> {Q['dur']:.2f}s (+{Q['dur'] - P['dur']:.2f}s)")
    print(f"narração antes : {ma}")
    print(f"narração depois: {mb}")
    for s in segs:
        print(f"  trecho {Path(s['src']).name} t {s['t']:.2f}->{M(s['t']):.2f} d {s['d']:.2f}->{s['L']:.2f}")
    for w in nao_abertas:
        print("PAUSA NÃO ABERTA", w)
    for w in avisos:
        print("AVISO", w)
    ok = True
    for portao in ('audio_plano.py', 'leitura.py'):
        r = subprocess.run([sys.executable, portao, f"planos/{novo_id}.json"], capture_output=True, text=True)
        print(r.stdout.strip())
        ok &= r.returncode == 0
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
