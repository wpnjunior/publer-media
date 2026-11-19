#!/usr/bin/env python3
"""Tom (F0) por YIN, mais confiável que a autocorrelação simples do medir_voz.py (que errava oitava).
uso: tom_yin.py arquivo [...]  -> mediana, p10, p90 (Hz), desvio em semitons, % de quadros com voz"""
import sys, subprocess, numpy as np
SR = 16000
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vn', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)
def yin(x, fmin=60, fmax=300, fl=0.04, hop=0.01, th=0.12):
    n = int(fl * SR); h = int(hop * SR); tmax = int(SR / fmin); tmin = int(SR / fmax); out = []
    for i in range(0, len(x) - n - tmax, h):
        fr = x[i:i + n + tmax]
        if np.sqrt(np.mean(fr[:n] ** 2)) < 2e-3: out.append(0); continue
        # função diferença via FFT
        w = fr[:n]; d = np.zeros(tmax + 1)
        e0 = np.sum(w ** 2)
        cs = np.concatenate([[0], np.cumsum(fr ** 2)])
        F = np.fft.rfft(fr, 2 * len(fr)); G = np.fft.rfft(w[::-1], 2 * len(fr))
        corr = np.fft.irfft(F * G)[n - 1:n - 1 + tmax + 1]
        for t in range(1, tmax + 1):
            d[t] = e0 + (cs[t + n] - cs[t]) - 2 * corr[t]
        cm = np.ones_like(d); s = 0.0
        for t in range(1, tmax + 1):
            s += d[t]; cm[t] = d[t] * t / s if s > 0 else 1
        cand = np.where(cm[tmin:] < th)[0]
        if not len(cand): out.append(0); continue
        t = cand[0] + tmin
        while t + 1 <= tmax and cm[t + 1] < cm[t]: t += 1
        if 1 <= t < tmax:
            a, b, c = cm[t - 1], cm[t], cm[t + 1]; den = a - 2 * b + c
            t = t + (0.5 * (a - c) / den if den else 0)
        out.append(SR / t)
    return np.array(out)
def resumo(p):
    f = yin(load(p)); v = f[f > 0]
    st = 12 * np.log2(v / np.median(v))
    return dict(arquivo=p.split('/')[-1], f0=round(float(np.median(v)), 1), p10=round(float(np.percentile(v, 10)), 1),
                p90=round(float(np.percentile(v, 90)), 1), var_st=round(float(np.std(st)), 2), voz=round(100 * len(v) / len(f)))
if __name__ == '__main__':
    for p in sys.argv[1:]: print(resumo(p))
