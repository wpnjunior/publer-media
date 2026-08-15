# -*- coding: utf-8 -*-
"""Calcula em que segundo cada slide deve entrar, a partir do roteiro e da duração do vídeo.

Uso: python tempos.py <roteiro.txt> <video_do_clone>

O roteiro tem um bloco por slide, separados por uma linha "---".
Como o clone fala em ritmo constante, o tempo de cada bloco é proporcional ao
número de palavras dele. Imprime a string de tempos que o montar_comentado.py espera.
"""
import sys, subprocess, re

roteiro = open(sys.argv[1], encoding="utf-8").read()
video = sys.argv[2]

blocos = [b.strip() for b in roteiro.split("---") if b.strip()]
palavras = [len(re.findall(r"\S+", b)) for b in blocos]
total = sum(palavras)

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", video], capture_output=True, text=True).stdout.strip())

t, tempos = 0.0, []
for p in palavras:
    tempos.append(round(t, 1))
    t += dur * p / total

print(f"{len(blocos)} blocos | {total} palavras | video {dur:.1f}s | ritmo {total/dur*60:.0f} palavras/min")
for i, (tp, p) in enumerate(zip(tempos, palavras), 1):
    print(f"  slide {i}: entra em {tp:5.1f}s  ({p} palavras)")
print("\n" + ",".join(str(x) for x in tempos))
