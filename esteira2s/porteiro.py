#!/usr/bin/env python3
"""Porteiro de qualidade: confere o Reels final antes de agendar.

Uso: python esteira2s/porteiro.py final.mp4 pasta_conferencia [--min 25 --max 75]
Mede (e reprova se falhar):
- formato 1080x1920, com áudio; duração entre --min e --max s; arquivo < 48 MB;
- volume a cada 3 s (nenhuma janela abaixo de -45 dB fora do último cartão);
- silêncio maior que 1,2 s no meio da fala;
- tela preta maior que 0,3 s;
- tela parada (congelada) maior que 6 s.
Gera pasta_conferencia/folha.jpg com 16 quadros: OLHE a folha (boca sem sorriso com dentes, sem dedos
contando, nenhuma tela vazia, legenda dentro da tela, @ do autor no react).
Saída: pasta_conferencia/porteiro.json e código 0 (aprovado) ou 1 (reprovado).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    arq, pasta = args[0], Path(args[1])
    dmin = float(args[args.index("--min") + 1]) if "--min" in args else 25
    dmax = float(args[args.index("--max") + 1]) if "--max" in args else 75
    pasta.mkdir(parents=True, exist_ok=True)
    falhas, achados = [], {}

    info = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
                           "-of", "json", arq]).stdout)
    dur = float(info["format"]["duration"])
    vs = [s for s in info["streams"] if s["codec_type"] == "video"]
    tem_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    mb = os.path.getsize(arq) / 1e6
    achados.update(duracao_s=round(dur, 1), tamanho_mb=round(mb, 1))
    if not vs or (vs[0]["width"], vs[0]["height"]) != (1080, 1920):
        falhas.append("formato diferente de 1080x1920")
    if not tem_audio:
        falhas.append("sem áudio")
    if not dmin <= dur <= dmax:
        falhas.append(f"duração {dur:.1f} s fora de {dmin:.0f}-{dmax:.0f} s")
    if mb >= 48:
        falhas.append(f"arquivo com {mb:.1f} MB (teto 48)")

    if tem_audio:
        # volume por janela de 3 s
        baixas = []
        t = 0.0
        while t < dur - 3.2:  # o cartão final pode ser mais baixo
            r = run(["ffmpeg", "-v", "info", "-ss", f"{t:.2f}", "-t", "3", "-i", arq, "-af", "volumedetect",
                     "-vn", "-f", "null", "-"])
            m = re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr)
            if m and float(m.group(1)) < -45:
                baixas.append(round(t, 1))
            t += 3
        achados["janelas_baixas_s"] = baixas
        if baixas:
            falhas.append(f"volume quase mudo em {baixas}")
        r = run(["ffmpeg", "-v", "info", "-i", arq, "-af", "silencedetect=n=-45dB:d=1.2", "-vn", "-f", "null", "-"])
        sil = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
        sil = [s for s in sil if 0.8 < s < dur - 3.5]
        achados["silencios_s"] = sil
        if sil:
            falhas.append(f"silêncio de mais de 1,2 s em {sil}")

    r = run(["ffmpeg", "-v", "info", "-i", arq, "-vf", "blackdetect=d=0.3:pix_th=0.06", "-an", "-f", "null", "-"])
    pretas = re.findall(r"black_start:([\d.]+)", r.stderr)
    achados["telas_pretas_s"] = pretas
    if pretas:
        falhas.append(f"tela preta em {pretas}")
    r = run(["ffmpeg", "-v", "info", "-i", arq, "-vf", "freezedetect=n=0.003:d=6", "-an", "-f", "null", "-"])
    paradas = re.findall(r"freeze_start: ([\d.]+)", r.stderr)
    achados["telas_paradas_s"] = paradas
    if paradas:
        falhas.append(f"tela parada por mais de 6 s em {paradas}")

    # folha de conferência
    ts = [dur * k / 16 + 0.3 for k in range(16)]
    quadros = []
    for i, t in enumerate(ts):
        q = pasta / f"q{i:02d}.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", arq, "-frames:v", "1", "-vf", "scale=270:480",
             str(q)])
        if q.exists():
            quadros.append(str(q))
    if quadros:
        entradas = sum((["-i", q] for q in quadros), [])
        n = len(quadros)
        lay = "|".join(f"{(i % 8) * 270}_{(i // 8) * 480}" for i in range(n))
        run(["ffmpeg", "-y", "-v", "error", *entradas, "-filter_complex", f"xstack=inputs={n}:layout={lay}:fill=black",
             str(pasta / "folha.jpg")])
        for q in quadros:
            os.remove(q)

    res = {"aprovado": not falhas, "falhas": falhas, **achados, "folha": str(pasta / "folha.jpg")}
    (pasta / "porteiro.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False))
    sys.exit(0 if not falhas else 1)


if __name__ == "__main__":
    main()
