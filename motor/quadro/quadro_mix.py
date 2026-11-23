"""quadro_mix.py: áudio da edição Quadro.
Voz (sobe para -17 LUFS) + CTA do banco + trilha calma com ducking + efeitos do SFX Kit tirados do próprio plano:
whoosh suave em cada troca de cena, whoosh ao contrário no afastar, marca-texto em cada marca, lápis nos traços
grandes (onda), papel na foto e pop no botão. Master -14 LUFS, pico -1,5 dBTP.

Uso: python3 quadro_mix.py plano.json voz.wav musica.wav saida.m4a [sfx_dir=/tmp/claude-0/sfxkit/sounds] [midia_dir=.]
"""
import json, re, subprocess, sys
from pathlib import Path

P = json.load(open(sys.argv[1]))
voz, musica, out = sys.argv[2], sys.argv[3], sys.argv[4]
SFX = Path(sys.argv[5] if len(sys.argv) > 5 else "/tmp/claude-0/sfxkit/sounds")
MID = Path(sys.argv[6] if len(sys.argv) > 6 else ".")
dur = P["dur"]


def lufs(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[0-9.]+) LUFS", r)
    return float(m[-1]) if m else -20.0


ev = []   # (arquivo, t, dB)
for k, c in enumerate(P["cenas"]):
    if k:
        ev.append(("whooshes/whoosh-slow-soft.wav", max(0, c["t"] - c.get("mov", .8) * .6), -20))
    ondas = 0
    for el in c["elementos"]:
        if el["tipo"] == "marca":
            ev.append(("writing-and-drawing/writing-highlighter.wav", el["t"], -18))
        elif el["tipo"] == "onda" and ondas == 0:
            ev.append(("writing-and-drawing/writing-pencil-draw.wav", el["t"], -24)); ondas += 1
        elif el["tipo"] == "foto":
            ev.append(("foley/foley-paper-slide.wav", el["t"] - .1, -16))
        elif el["tipo"] == "botao":
            ev.append(("pops/pop-medium-in.wav", el["t"], -12))
if P.get("afastar"):
    ev.append(("reverse-whooshes/reverse-whoosh-medium-soft.wav", P["afastar"]["t"] - 1.0, -18))

ins = ["-i", voz, "-i", musica]
gv = min(0.0, -17.0 - lufs(voz)) if lufs(voz) < -20 else 0.0
fl = [f"[0:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={gv:.2f}dB,asplit=2[voz][sc0]"]
parts = ["[voz]"]
n = 2
cta = P.get("cta")
if cta:
    f = str(MID / cta["src"])
    gc = -17.0 - lufs(f)
    ins += ["-i", f]
    d = int(cta["t"] * 1000)
    fl.append(f"[{n}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={gc:.2f}dB,adelay={d}|{d},asplit=2[cta][sc1]")
    parts.append("[cta]")
    n += 1
    fl.append("[sc0][sc1]amix=inputs=2:normalize=0[sc]")
else:
    fl.append("[sc0]anull[sc]")
gm = -17.0 - 11.0 - lufs(musica)   # trilha ~11 dB abaixo da voz antes do ducking
fl.append(f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,atrim=0:{dur},volume={gm:.2f}dB,afade=t=in:d=0.6,"
          f"afade=t=out:st={dur - 1.5:.2f}:d=1.5[mus0]")
fl.append("[mus0][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=300[mus]")
parts.append("[mus]")
for arq, t, db in ev:
    ins += ["-i", str(SFX / arq)]
    d = int(max(0, t) * 1000)
    fl.append(f"[{n}:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={db}dB,adelay={d}|{d}[s{n}]")
    parts.append(f"[s{n}]")
    n += 1
fl.append(f"{''.join(parts)}amix=inputs={len(parts)}:normalize=0,apad,atrim=duration={dur},alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
tmp = out + ".tmp.m4a"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[out]", "-c:a", "aac", "-b:a", "256k", tmp], check=True)
g = -14 - lufs(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={g + 0.5:.2f}dB,alimiter=limit=0.8:level=false", "-c:a", "aac", "-b:a", "256k", out], check=True)
Path(tmp).unlink()
print(f"mix ok {out}: {len(ev)} efeitos, master {lufs(out):.1f} LUFS")
for arq, t, db in sorted(ev, key=lambda e: e[1]):
    print(f"  {t:6.2f}s  {Path(arq).stem}  {db} dB")
