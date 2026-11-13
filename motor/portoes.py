"""Portões da edição: mede o vídeo e reprova se passar dos limites (caso 006, Psiquiatra).
Uso: python3 portoes.py video.mp4 [inicio_sem_viral_s]"""
import re, subprocess, sys

def medir(f, ini=0.0):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    out = subprocess.run(["ffmpeg", "-nostats", "-i", f, "-vf", "scale=180:-2,fps=10,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    ys = [float(x) for x in re.findall(r"YAVG=([0-9.]+)", out)]
    ys = ys[int(ini * 10):]
    parado = sum(1 for y in ys if y < 1.0) / max(1, len(ys))
    run = best = 0
    for y in ys:
        run = run + 1 if y < 1.0 else 0
        best = max(best, run)
    cut = subprocess.run(["ffmpeg", "-nostats", "-i", f, "-vf", "scale=270:-2,select='gt(scene,0.28)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    c = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", cut)]
    gaps = [b - a for a, b in zip([0] + c, c + [d])]
    lu = re.findall(r"I:\s+(-?[0-9.]+) LUFS", subprocess.run(["ffmpeg", "-nostats", "-i", f, "-af", "ebur128", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr)
    r = dict(dur=d, cortes_min=len(c) / d * 60, maior_plano=max(gaps), parado=parado * 100, maior_parado=best / 10, lufs=float(lu[-1]) if lu else None)
    lim = [("parado", r["parado"] <= 10, "tela quase parada ≤ 10% (régua: Rosenhan 8,4%)"), ("maior_parado", r["maior_parado"] <= 3, "sem mudança visual ≤ 3 s"),
           ("lufs", r["lufs"] is not None and -16 <= r["lufs"] <= -12, "volume entre -16 e -12 LUFS")]
    return r, lim

if __name__ == "__main__":
    r, lim = medir(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0)
    print(" | ".join(f"{k} {v:.1f}" if isinstance(v, float) else f"{k} {v}" for k, v in r.items()))
    ok = all(x[1] for x in lim)
    for k, passou, txt in lim:
        print(("OK  " if passou else "FALHA ") + txt)
    print("APROVADO" if ok else "REPROVADO")
