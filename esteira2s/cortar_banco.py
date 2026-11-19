#!/usr/bin/env python3
"""Corta um vídeo do HeyGen (várias frases curtas) em clipes do Banco de Rostos.

Uso: python esteira2s/cortar_banco.py video.mp4 cortes.json esteira2s/banco-rostos
cortes.json = [{"arquivo": "abertura_01", "tipo": "abertura", "marca": "todas", "frase": "...", "ini": 0.0, "fim": 1.46}, ...]
(ini/fim = tempo da fala, medido pela transcrição). O corte ganha uma folga antes e depois, sem invadir a frase
vizinha. Acrescenta os clipes em banco-rostos/indice.json (campo usado_em começa vazio).
"""
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    video, cortes, pasta = sys.argv[1], json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")), Path(sys.argv[3])
    pasta.mkdir(parents=True, exist_ok=True)
    idx_p = pasta / "indice.json"
    indice = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else {"clipes": []}
    ordenados = sorted(cortes, key=lambda c: c["ini"])
    for i, c in enumerate(ordenados):
        ant = ordenados[i - 1]["fim"] if i else 0.0
        prox = ordenados[i + 1]["ini"] if i + 1 < len(ordenados) else c["fim"] + 0.4
        ini = max(ant + (c["ini"] - ant) / 2 if i else 0.0, c["ini"] - 0.18)
        fim = min(c["fim"] + (prox - c["fim"]) / 2, c["fim"] + 0.28)
        saida = pasta / f"{c['arquivo']}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ini:.3f}", "-to", f"{fim:.3f}", "-i", video,
                        "-af", f"afade=t=in:d=0.04,afade=t=out:st={fim - ini - 0.06:.3f}:d=0.06",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(saida)], check=True)
        indice["clipes"] = [x for x in indice["clipes"] if x["arquivo"] != saida.name]
        indice["clipes"].append({"arquivo": saida.name, "tipo": c["tipo"], "marca": c.get("marca", "todas"),
                                 "frase": c["frase"], "duracao_s": round(fim - ini, 2), "usado_em": []})
        print(saida.name, round(fim - ini, 2))
    idx_p.write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main()
