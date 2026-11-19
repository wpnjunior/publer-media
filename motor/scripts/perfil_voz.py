#!/usr/bin/env python3
"""Perfil completo de uma voz em 10 características (Praat/parselmouth), para comparar o clone com a voz real.
uso: perfil_voz.py arquivo1 [arquivo2 ...] [--json saida.json]
1 tom (Hz, p10/p90) · 2 melodia (semitons) · 3 timbre (formantes F1/F2/F3, centroide) · 4 ressonância
(índice nasal: energia 200-350 Hz menos 400-1000 Hz nas vogais; mais alto = mais nasal) · 5 textura (HNR, jitter,
shimmer, CPPS, H1-H2: soproso) · 6 dinâmica (variação de volume) · 7 ritmo (só se houver .words.json) ·
8 articulação (energia 4-8 kHz: consoantes/chiado) · 9 sotaque (F1/F2 das vogais: abertura e posição) · 10 bandas."""
import sys, json, subprocess, numpy as np, parselmouth
from parselmouth.praat import call
def carrega(f, sr=22050):
    raw = subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True,check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64), sr
def db(x): return 10*np.log10(x+1e-12)
def perfil(f):
    x, sr = carrega(f); snd = parselmouth.Sound(x, sampling_frequency=sr)
    pit = snd.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=300)
    f0 = pit.selected_array['frequency']; v = f0 > 0; f0v = f0[v]
    st = 12*np.log2(f0v/np.median(f0v))
    form = snd.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5000)
    ts = pit.xs()[v]
    F = np.array([[form.get_value_at_time(k, t) for k in (1,2,3)] for t in ts]); F = F[~np.isnan(F).any(1)]
    hnr = snd.to_harmonicity_cc(time_step=0.01, minimum_pitch=60); h = hnr.values[hnr.values > -100]
    pp = call(snd, "To PointProcess (periodic, cc)", 60, 300)
    jit = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)*100
    shi = call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)*100
    cep = call(snd, "To PowerCepstrogram", 60, 0.002, 5000, 50)
    cpps = call(cep, "Get CPPS", True, 0.02, 0.0005, 60, 330, 0.05, "Parabolic", 0.001, 0.05, "Exponential decay", "Robust")
    # por quadro sonoro: H1-H2, índice nasal, bandas
    n = int(0.04*sr); hop = int(0.01*sr); win = np.hanning(n); fr = np.fft.rfftfreq(n*4, 1/sr)
    h12, nas, ener, hf = [], [], [], []
    for t, f0t in zip(pit.xs(), f0):
        i = int(t*sr) - n//2
        if i < 0 or i+n > len(x): continue
        seg = x[i:i+n]*win; e = float(np.sum(seg**2))
        if e < 1e-6: continue
        S = np.abs(np.fft.rfft(seg, n*4))**2
        band = lambda a, b: S[(fr>=a)&(fr<b)].sum()
        if f0t > 0:
            amp = lambda hz: S[(fr>hz*0.9)&(fr<hz*1.1)].max()
            h12.append(db(amp(f0t)) - db(amp(2*f0t)))
            nas.append(db(band(200,350)) - db(band(400,1000)))
            ener.append(db(e))
        hf.append(db(band(4000,8000)) - db(band(0,8000)))
    ener = np.array(ener)
    B = [(80,200),(200,350),(350,800),(800,1500),(1500,3000),(3000,5000),(5000,8000)]
    S_all = np.abs(np.fft.rfft(x, len(x)))**2; frq = np.fft.rfftfreq(len(x), 1/sr); tot = S_all[(frq>=80)&(frq<8000)].sum()
    bandas = {f'{a}-{b}': round(float(db(S_all[(frq>=a)&(frq<b)].sum()) - db(tot)),1) for a,b in B}
    cent = float((frq*S_all).sum()/S_all.sum())
    r = {'arquivo': f.split('/')[-1],
         '1_tom_hz': round(float(np.median(f0v)),1), 'tom_p10': round(float(np.percentile(f0v,10)),1), 'tom_p90': round(float(np.percentile(f0v,90)),1),
         '2_melodia_st': round(float(np.percentile(st,90)-np.percentile(st,10)),2),
         '3_F1': round(float(np.median(F[:,0]))), '3_F2': round(float(np.median(F[:,1]))), '3_F3': round(float(np.median(F[:,2]))), 'centroide': round(cent),
         '4_nasal_db': round(float(np.median(nas)),1),
         '5_hnr_db': round(float(np.median(h)),1), '5_jitter_pct': round(jit,2), '5_shimmer_pct': round(shi,2), '5_cpps': round(cpps,1), '5_h1h2_db': round(float(np.median(h12)),1),
         '6_dinamica_db': round(float(np.percentile(ener,90)-np.percentile(ener,10)),1),
         '8_agudos_db': round(float(np.median(hf)),1), 'bandas_db': bandas}
    return r
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    out = sys.argv[sys.argv.index('--json')+1] if '--json' in sys.argv else None
    if out: args = [a for a in args if a != out]
    res = [perfil(a) for a in args]
    for r in res: print(json.dumps(r, ensure_ascii=False))
    if out: json.dump(res, open(out,'w'), ensure_ascii=False, indent=1)
