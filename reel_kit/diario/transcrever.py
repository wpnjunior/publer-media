"""Tempo de cada palavra do vídeo do HeyGen, com a grafia do roteiro.

Uso: python transcrever.py bruto.mp4 roteiro.txt words.json

O faster-whisper (modelo small, CPU) dá o tempo de cada palavra que ouviu. Como o HeyGen lê o
roteiro exato, alinhamos as palavras ouvidas às do roteiro (difflib) e ficamos com a grafia certa
("AMH", "cá entre nós") e o tempo do whisper. Palavra do roteiro sem par ganha tempo interpolado.
Leva uns 20 s para 1 minuto de vídeo.
"""
import difflib
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np


def norm(p: str) -> str:
    p = p.lower()
    p = re.sub(r"[^\wà-ú]", "", p)
    return p


def ouvir(video: Path) -> list[dict]:
    from faster_whisper import WhisperModel

    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-ac", "1", "-ar", "16000", str(wav)], check=True)
        wf = wave.open(str(wav))
        a = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(a, language="pt", word_timestamps=True)
    out = []
    for s in segs:
        for x in s.words:
            out.append({"w": x.word.strip(), "s": float(x.start), "e": float(x.end)})
    return out


def alinhar(ouvidas: list[dict], roteiro: str) -> list[dict]:
    texto = re.sub(r"\s+", " ", roteiro.replace("\n", " ")).strip()
    palavras = texto.split(" ")
    a = [norm(w["w"]) for w in ouvidas]
    b = [norm(w) for w in palavras]
    res: list[dict | None] = [None] * len(palavras)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and (i2 - i1) == (j2 - j1)):
            for k in range(j2 - j1):
                o = ouvidas[i1 + k]
                res[j1 + k] = {"w": palavras[j1 + k], "s": o["s"], "e": o["e"]}
        elif tag == "replace" and i2 > i1:
            # blocos de tamanho diferente: espalha o tempo do trecho ouvido
            t0, t1 = ouvidas[i1]["s"], ouvidas[i2 - 1]["e"]
            n = j2 - j1
            for k in range(n):
                res[j1 + k] = {"w": palavras[j1 + k], "s": t0 + (t1 - t0) * k / n, "e": t0 + (t1 - t0) * (k + 1) / n}
    # interpola os que sobraram
    for j, r in enumerate(res):
        if r is None:
            prev = next((res[k]["e"] for k in range(j - 1, -1, -1) if res[k]), 0.0)
            nxt = next((res[k]["s"] for k in range(j + 1, len(res)) if res[k]), prev + 0.3)
            res[j] = {"w": palavras[j], "s": prev, "e": max(prev + 0.05, min(nxt, prev + 0.4))}
    for r in res:
        r["s"], r["e"] = round(r["s"], 3), round(r["e"], 3)
    return res


if __name__ == "__main__":
    video, rot, saida = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    ouvidas = ouvir(video)
    words = alinhar(ouvidas, rot.read_text(encoding="utf-8"))
    saida.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    print(f"{len(words)} palavras, última termina em {words[-1]['e']:.2f}s")
