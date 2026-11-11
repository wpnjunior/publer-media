#!/usr/bin/env python3
"""Monta o "bruto" de um Reels econômico: clipes de rosto do Banco de Rostos + narração só em áudio.

O editor (reel_kit/diario/editar.sh) espera um vídeo falado. Aqui ele nasce sem gerar clone novo:
- trechos ROSTO = clipes prontos do banco (com a própria fala);
- trechos NARRAÇÃO = a foto parada do Wagner com zoom lento + o áudio da narração.
A edição depois cobre a narração com cenas (Mapeamento, painéis, tela dividida).

Uso: python esteira2s/montar_bruto.py montagem.json saida.mp4
montagem.json = {"foto": "reel_kit/foto_wagner.png",
                 "trechos": [{"rosto": "esteira2s/banco-rostos/abertura_03.mp4"},
                             {"voz": "/tmp/x/narracao.mp3"},
                             {"rosto": "esteira2s/banco-rostos/fecho_07.mp4"}]}
Concatena sempre pelo filtro concat (nunca -c copy). Saída 1080x1920, 25 fps, AAC 48 kHz.
"""
import json
import subprocess
import sys
from pathlib import Path

W, H, FPS = 1080, 1920, 25


def dur(arq: str) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    saida = sys.argv[2]
    foto = spec["foto"]
    entradas: list[str] = []
    filtros: list[str] = []
    k = 0
    marcas: list[dict] = []  # onde é rosto de verdade e onde é narração sobre foto (o editor nunca mostra o rosto na narração)
    pos = 0.0
    for i, t in enumerate(spec["trechos"]):
        d_t = dur(t.get("rosto") or t.get("voz"))
        marcas.append({"t0": round(pos, 3), "t1": round(pos + d_t, 3), "tipo": "rosto" if "rosto" in t else "voz"})
        pos += d_t
        if "rosto" in t:
            entradas += ["-i", t["rosto"]]
            filtros.append(
                f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,"
                f"format=yuv420p[v{i}];"
                f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];")
            k += 1
        elif "voz" in t:
            d = dur(t["voz"])
            quadros = int(d * FPS) + 1
            entradas += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", foto, "-i", t["voz"]]
            filtros.append(
                f"[{k}:v]scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                f"zoompan=z='1+0.06*on/{quadros}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                f"trim=duration={d:.3f},setsar=1,format=yuv420p[v{i}];"
                f"[{k + 1}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={d:.3f}[a{i}];")
            k += 2
        else:
            raise SystemExit(f"trecho {i}: use 'rosto' ou 'voz'")
    n = len(spec["trechos"])
    pares = "".join(f"[v{i}][a{i}]" for i in range(n))
    filtros.append(f"{pares}concat=n={n}:v=1:a=1[v][a]")
    cmd = ["ffmpeg", "-y", "-v", "error", *entradas, "-filter_complex", "".join(filtros),
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True)
    Path(saida + ".trechos.json").write_text(json.dumps(marcas, indent=1), encoding="utf-8")
    print(f"bruto montado: {saida} ({dur(saida):.1f} s)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main()
