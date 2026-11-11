#!/usr/bin/env python3
"""Reels de texto (sem voz, custo 0): cartões 1080x1920 do telas.py viram vídeo com zoom leve, troca suave e trilha.

Uso: python esteira2s/reels_texto.py spec.json saida.mp4
spec.json = o mesmo do telas.py (formato forçado para "story"), mais:
  "trilha": nome de reel_kit/trilhas (sem .m4a), "segundos": [5, 6, ...] (opcional; padrão = pelo tamanho do texto)
Cada tela fica o tempo de leitura (~2,2 s + 0,06 s por caractere, entre 3,5 e 8 s).
"""
import json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import telas

RAIZ = Path(__file__).resolve().parent.parent
FPS, TROCA = 30, 0.4


def main(spec_arq, saida):
    spec = json.loads(Path(spec_arq).read_text(encoding="utf-8"))
    spec["formato"] = "story"
    with tempfile.TemporaryDirectory() as tmp:
        imgs = telas.gerar(spec, tmp)
        segs = spec.get("segundos") or []
        durs = []
        for i, t in enumerate(spec["telas"]):
            n = sum(len(str(t.get(k, ""))) for k in ("rotulo", "titulo", "texto")) + sum(map(len, t.get("lista", [])))
            durs.append(float(segs[i]) if i < len(segs) else max(3.5, min(8.0, 2.2 + 0.06 * n)))
        cmd, filtros = ["ffmpeg", "-y", "-v", "error"], []
        for img, d in zip(imgs, durs):
            cmd += ["-framerate", str(FPS), "-loop", "1", "-t", f"{d + TROCA:.2f}", "-i", img]
        for i, d in enumerate(durs):
            q = int((d + TROCA) * FPS)
            filtros.append(f"[{i}:v]scale=1188:2112,zoompan=z='1.10-0.10*on/{q}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                           f":d=1:s=1080x1920:fps={FPS},trim=duration={d + TROCA:.2f},setpts=PTS-STARTPTS,settb=AVTB,format=yuv420p[v{i}]")
        ant, pos = "v0", 0.0
        for i in range(1, len(durs)):
            pos += durs[i - 1]
            filtros.append(f"[{ant}][v{i}]xfade=transition=slideleft:duration={TROCA}:offset={pos:.2f}[x{i}]")
            ant = f"x{i}"
        total = sum(durs) + TROCA
        trilha = RAIZ / "reel_kit" / "trilhas" / f"{spec.get('trilha', 'educacional')}.m4a"
        cmd += ["-stream_loop", "-1", "-i", str(trilha)]
        filtros.append(f"[{len(durs)}:a]volume=0.5,afade=t=in:d=0.5,afade=t=out:st={total - 1.2:.2f}:d=1.2[a]")
        cmd += ["-filter_complex", ";".join(filtros), "-map", f"[{ant}]", "-map", "[a]", "-t", f"{total:.2f}",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart", saida]
        subprocess.run(cmd, check=True)
    print(f"{saida}: {total:.1f} s, {Path(saida).stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
