"""Mix do áudio do plano: voz + viral (barramento de fala), trilha por clima com ducking, efeitos sonoros. Master -14 LUFS.
Uso: python3 mix.py plano.json saida.m4a"""
import json, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def som(nome):
    p = Path(nome)
    if p.exists():
        return str(p)
    return str(AQUI / "assets" / "som" / f"{nome}.m4a")


def mix(plano, out):
    P = json.load(open(plano))
    A = P["audio"]
    dur = P["dur"]
    ins, fl = [], []
    fala, mus, fx = [], [], []

    def add(src, t, ms, d, gain, fade=0.03, bus=None):
        k = len(ins) // 2
        ins.extend(["-i", src])
        dly = int(round(t * 1000))
        tr = f"atrim=start={ms}:duration={d}," if d else (f"atrim=start={ms}," if ms else "")
        fo = f"afade=t=out:st={max(0, (d or 0) - fade)}:d={fade}," if d else ""
        fl.append(f"[{k}:a]aformat=sample_rates=44100:channel_layouts=stereo,{tr}asetpts=PTS-STARTPTS,afade=t=in:d={fade},{fo}volume={gain},adelay={dly}|{dly}[a{k}]")
        bus.append(f"[a{k}]")

    for v in A.get("voz", []):
        add(v["src"], v["t"], v.get("ms", 0), v["d"], v.get("gain", 1.0), bus=fala)
    for v in A.get("viral", []):
        add(v["src"], v["t"], v.get("ms", 0), v["d"], v.get("gain", 1.0), bus=fala)
    for m in A.get("musica", []):
        add(som(m["src"]), m["t"], m.get("ms", 0), m["d"], m.get("gain", .5), fade=m.get("fade", .4), bus=mus)
    for s in A.get("sfx", []):
        add(som(s["src"]), max(0, s["t"] - s.get("pico", 0)), 0, s.get("d", 0), s.get("gain", .7), bus=fx)
    parts = []
    if fala:
        fl.append(f"{''.join(fala)}amix=inputs={len(fala)}:normalize=0,asplit=2[fala][sc]")
        parts.append("[fala]")
    if mus:
        fl.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0[mus0]")
        if fala:
            fl.append("[mus0][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=250[mus]")
        else:
            fl.append("[mus0]anull[mus]")
        parts.append("[mus]")
    elif fala:
        fl.append("[sc]anullsink")
    if fx:
        fl.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
        parts.append("[fx]")
    fl.append(f"{''.join(parts)}amix=inputs={len(parts)}:normalize=0,apad,atrim=duration={dur},alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "44100", "-c:a", "aac", "-b:a", "256k", out]
    subprocess.run(cmd, check=True)
    print("ok", out)


if __name__ == "__main__":
    mix(sys.argv[1], sys.argv[2])
