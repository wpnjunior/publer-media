"""Trilha + efeitos sonoros + voz, e junta com o vídeo renderizado.

Uso: python mix.py <bruto.mp4> <video_mudo.mp4> <timeline.json> <saida.mp4> [trilha]

- Trilha: uma faixa do banco reel_kit/trilhas (Pixabay, uso comercial livre). Se não vier no
  argumento, usa a "trilha" do plano gravada na timeline, ou o seletor do dia (escolhe_trilha.py).
  As faixas têm 20 s, então tocam em loop com emenda suave.
- Ducking: a música abaixa quando ele fala (sidechaincompress pela voz) e sobe nas pausas.
- Efeitos sintetizados aqui mesmo (sem baixar nada): whoosh nos cortes, thud nos carimbos e
  números, pop nos painéis, ding na fonte, brilho no cartão final.
- Master: loudnorm I=-14 (padrão do Instagram).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent  # reel_kit/
SFX = {
    "whoosh": "anoisesrc=d=0.45:c=pink:a=0.9,highpass=f=500,lowpass=f=5000,afade=t=in:d=0.25:curve=exp,afade=t=out:st=0.25:d=0.2,volume=0.55",
    "thud": "sine=f=58:d=0.5,volume=2.2,afade=t=out:st=0.05:d=0.45:curve=exp",
    "pop": "sine=f=880:d=0.09,volume=0.5,afade=t=out:d=0.09",
    "ding": "sine=f=1318:d=0.6,volume=0.35,afade=t=out:st=0.02:d=0.58:curve=exp",
    "brilho": "sine=f=1760:d=1.0,volume=0.25,tremolo=f=9:d=0.6,afade=t=out:st=0.1:d=0.9",
}


def rodar(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    bruto, mudo, tlp, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    tl = json.loads(tlp.read_text(encoding="utf-8"))
    trilha = sys.argv[5] if len(sys.argv) > 5 else tl.get("trilha") or ""
    if trilha and not trilha.endswith(".m4a"):
        trilha = str(KIT / "trilhas" / f"{trilha}.m4a")
    if not trilha or not Path(trilha).exists():
        trilha = subprocess.run([sys.executable, str(KIT / "escolhe_trilha.py")], capture_output=True, text=True, check=True).stdout.strip()
    total = tl["total"]

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        for nome, expr in SFX.items():
            rodar(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", expr, "-ar", "48000", "-ac", "2", str(td / f"{nome}.wav")])
        evs = [e for e in tl["eventos"] if e["t"] < total]
        inputs = ["-i", str(bruto), "-stream_loop", "-1", "-i", trilha]
        for e in evs:
            inputs += ["-i", str(td / f"{e['sfx']}.wav")]
        f = []
        # voz: o áudio do bruto, com silêncio no cartão final
        f.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={total},atrim=0:{total},asplit=2[voz][sc]")
        # música em loop, -13 dB, cai no fim
        f.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total},volume=-13dB,"
                 f"afade=t=in:d=0.6,afade=t=out:st={total - 1.6}:d=1.6[mus]")
        f.append("[mus][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=220[musd]")
        sfx_labels = []
        for k, e in enumerate(evs):
            ms = max(0, int(e["t"] * 1000) - (120 if e["sfx"] == "whoosh" else 0))
            f.append(f"[{k + 2}:a]adelay={ms}|{ms}[s{k}]")
            sfx_labels.append(f"[s{k}]")
        n = 2 + len(sfx_labels)
        f.append(f"[voz][musd]{''.join(sfx_labels)}amix=inputs={n}:normalize=0:duration=first,"
                 f"alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        script = td / "f.txt"
        script.write_text(";\n".join(f), encoding="utf-8")
        rodar(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex_script", str(script), "-map", "[a]",
               "-ar", "48000", "-c:a", "pcm_s16le", str(td / "mix.wav")])
        rodar(["ffmpeg", "-y", "-v", "error", "-i", str(mudo), "-i", str(td / "mix.wav"), "-map", "0:v", "-map", "1:a",
               "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(total), str(saida)])
    print(f"trilha: {Path(trilha).stem}; {len(evs)} efeitos; saída {saida} ({saida.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
