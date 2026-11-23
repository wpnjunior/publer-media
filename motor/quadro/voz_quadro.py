"""voz_quadro.py: acelera a narração (atempo) e abre pausa mínima entre frases.
Uso: python3 voz_quadro.py voz_raw.wav words_raw.txt saida_dir [atempo=1.15] [pausa=0.75]
words_raw.txt: "palavra inicio fim" por linha (do create_speech with_timestamps).
Gera voz.wav e words.json (tempos já no áudio novo). Regra do ritmo: atempo 1,15 e pausa >= 0,7 s."""
import json, subprocess, sys
from pathlib import Path

src, wtxt, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
at = float(sys.argv[4]) if len(sys.argv) > 4 else 1.15
pausa = float(sys.argv[5]) if len(sys.argv) > 5 else 0.75
out.mkdir(parents=True, exist_ok=True)
W = [(a, float(b), float(c)) for a, b, c in (l.split() for l in open(wtxt) if l.strip())]
frases, cur = [], []
for w in W:
    cur.append(w)
    if w[0][-1] in ".?!":
        frases.append(cur); cur = []
if cur: frases.append(cur)
parts, words, t = [], [], 0.0
for i, f in enumerate(frases):
    a = max(0, f[0][1] - 0.06); b = f[-1][2] + 0.10
    p = out / f"_f{i:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                    "-af", f"atempo={at},afade=t=in:d=0.02,afade=t=out:st={(b-a)/at-0.04:.3f}:d=0.04",
                    "-ar", "44100", "-ac", "1", str(p)], check=True)
    for txt, s, e in f:
        words.append({"w": txt, "s": round(t + (s - a) / at, 3), "e": round(t + (e - a) / at, 3)})
    t += (b - a) / at
    parts.append(p)
    if i < len(frases) - 1:
        t += pausa
sil = out / "_sil.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono", "-t", str(pausa), str(sil)], check=True)
lst = out / "_lista.txt"
lst.write_text("".join(f"file '{p.resolve()}'\n" + (f"file '{sil.resolve()}'\n" if i < len(parts) - 1 else "") for i, p in enumerate(parts)))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out / "voz.wav")], check=True)
for p in out.glob("_*"): p.unlink()
json.dump(words, open(out / "words.json", "w"), ensure_ascii=False, indent=0)
print(f"voz.wav {t:.2f}s, {len(words)} palavras, {len(frases)} frases")
