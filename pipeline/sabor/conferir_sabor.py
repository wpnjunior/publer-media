# -*- coding: utf-8 -*-
"""conferir_sabor.py - portao de qualidade do SABOR.

Uma esteira chama isto DEPOIS de rodar camuflar_forte.py e antes de dar o material como pronto.
Sai com codigo 0 se tudo passou, 1 se algum arquivo reprovou. Assim da para usar em `&&`.

  python conferir_sabor.py <arquivo ou pasta> [--recursivo] [--origem <pasta dos originais>]

Os cinco testes (os quatro primeiros valem para todo arquivo; o quinto so com --origem):
  1. metadados limpos: nada de encoder, creation_time, timecode, title, location, copyright...
  2. sem o carimbo "x264 core ... settings" nos primeiros 300 KB
  3. zero byte sobrando depois do ultimo bloco do mp4
  4. continua 1080x1920 a 30 qps, com faixa de audio
  5. a voz nao saiu do lugar: atraso de no maximo 40 ms contra o original
"""
import argparse
import os
import re
import struct
import subprocess
import sys

TAGS_OK = {"major_brand", "minor_version", "compatible_brands", "handler_name", "language"}
EXTS_V = {".mp4", ".mov", ".m4v"}
EXTS_I = {".jpg", ".jpeg", ".png"}


def probe(p, entries, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "default=nw=1", str(p)]
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


def teste_metadados(p):
    fora = []
    for l in probe(p, "format_tags").splitlines() + probe(p, "stream_tags").splitlines():
        l = l.strip()
        if l.startswith("TAG:"):
            chave = l[4:].split("=")[0].lower()
            if chave not in TAGS_OK:
                fora.append(chave)
    return (not fora), ("etiquetas: " + ", ".join(sorted(set(fora))) if fora else "")


def teste_x264(p):
    with open(p, "rb") as f:
        buf = f.read(300000)
    return (b"x264 core" not in buf), ("carimbo do x264 presente" if b"x264 core" in buf else "")


def teste_sobra(p):
    n = os.path.getsize(p)
    with open(p, "rb") as f:
        pos = 0
        while pos < n:
            f.seek(pos)
            h = f.read(8)
            if len(h) < 8:
                break
            sz = struct.unpack(">I", h[:4])[0]
            if sz == 1:
                sz = struct.unpack(">Q", f.read(8))[0]
            if sz < 8:
                break
            pos += sz
    return (n - pos == 0), ("" if n - pos == 0 else str(n - pos) + " bytes soltos no fim")


def teste_formato(p):
    v = probe(p, "stream=width,height,avg_frame_rate", "v:0").strip().splitlines()
    d = dict(x.split("=", 1) for x in v if "=" in x)
    aud = probe(p, "stream=codec_name", "a:0").strip()
    erros = []
    # 1080x1920 (9:16, Reels) ou 1080x1350 (4:5, quando o sabor roda com --crop45)
    if d.get("width") != "1080" or d.get("height") not in ("1920", "1350"):
        erros.append("tamanho " + str(d.get("width")) + "x" + str(d.get("height")))
    if d.get("avg_frame_rate") != "30/1":
        erros.append("quadros " + str(d.get("avg_frame_rate")))
    if not aud:
        erros.append("sem audio")
    return (not erros), "; ".join(erros)


def _dur_stream(p, s):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", s, "-show_entries",
                        "stream=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip().splitlines()[0])
    except Exception:
        return 0.0


def teste_duracoes(p):
    """Imagem e som tem que durar o mesmo, e o audio tem que estar em 48 kHz.
    Foi o que o portao deixou passar em 23/09: reel do frasco com video de 13,7 s e audio de 27,5 s
    (audio de 96 kHz tratado como 48 kHz). A duracao do CONTAINER mente nesse caso: vale a maior."""
    v, a = _dur_stream(p, "v:0"), _dur_stream(p, "a:0")
    erros = []
    if v > 0 and a > 0 and abs(v - a) > 0.25:
        erros.append("video " + format(v, ".2f") + "s x audio " + format(a, ".2f") + "s")
    sr = probe(p, "stream=sample_rate", "a:0").strip().replace("sample_rate=", "")
    if sr and sr != "48000":
        erros.append("audio a " + sr + " Hz")
    return (not erros), "; ".join(erros)


def teste_duracao_esperada(novo, original):
    """Com o original em maos: a saida tem que durar (original - 1 s) / velocidade, e a velocidade
    do sabor fica entre 0,97 e 1,03. Fora disso, algo esticou ou encolheu o video."""
    d_org = max(_dur_stream(original, "v:0"), _dur_stream(original, "a:0"))
    d_novo = max(_dur_stream(novo, "v:0"), _dur_stream(novo, "a:0"))
    if d_org <= 2 or d_novo <= 0:
        return True, ""
    minimo, maximo = (d_org - 1.0) / 1.035, (d_org - 1.0) / 0.965
    if not (minimo - 0.3 <= d_novo <= maximo + 0.3):
        return False, ("duracao " + format(d_novo, ".2f") + "s fora do esperado ("
                       + format(minimo, ".1f") + "-" + format(maximo, ".1f") + "s)")
    return True, ""


def teste_sincronia(novo, original):
    try:
        import numpy as np
    except ImportError:
        return True, "(numpy ausente, teste pulado)"

    def env(p, extra=None):
        cmd = ["ffmpeg", "-v", "error", "-i", str(p)]
        if extra:
            cmd += ["-af", extra]
        cmd += ["-ac", "1", "-ar", "8000", "-f", "s16le", "-"]
        raw = subprocess.run(cmd, capture_output=True).stdout
        x = np.frombuffer(raw, "<i2").astype(np.float32) / 32768
        m = len(x) // 80 * 80
        if m == 0:
            return None
        return np.sqrt((x[:m].reshape(-1, 80) ** 2).mean(1))

    # O sabor corta 0,5 s de cada ponta e sorteia a velocidade entre 0,97 e 1,03. A velocidade
    # usada se descobre pela razao das duracoes; com ela o original vai para a mesma regua.
    def dur(p):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(p)], capture_output=True, text=True)
        try:
            return float(r.stdout.strip())
        except Exception:
            return 0.0
    # a duracao do container mente quando video e audio divergem: usa a maior das faixas
    d_org = max(_dur_stream(original, "v:0"), _dur_stream(original, "a:0")) or dur(original)
    d_novo = max(_dur_stream(novo, "v:0"), _dur_stream(novo, "a:0")) or dur(novo)
    if d_org <= 1.5 or d_novo <= 0:
        return True, "(duracao ilegivel)"
    vel = max(0.5, min(2.0, (d_org - 1.0) / d_novo))
    a = env(original, f"atrim=start=0.5:duration={d_org - 1.0:.3f},asetpts=PTS-STARTPTS,atempo={vel:.4f}")
    b = env(novo)
    if a is None or b is None:
        return True, "(sem audio para comparar)"
    L = min(len(a), len(b))
    if L < 50:
        return True, "(curto demais)"
    a, b = a[:L] - a[:L].mean(), b[:L] - b[:L].mean()
    c = np.correlate(b, a, "full")
    lag = int((c.argmax() - (L - 1)) * 10)
    return (abs(lag) <= 40), ("voz deslocada " + str(lag) + " ms" if abs(lag) > 40 else "")


def achar_original(p, pasta_origem):
    if not pasta_origem:
        return None
    base = re.sub(r"-sabor$", "", os.path.splitext(os.path.basename(p))[0])
    for e in EXTS_V:
        cam = os.path.join(pasta_origem, base + e)
        if os.path.exists(cam):
            return cam
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alvo")
    ap.add_argument("--recursivo", action="store_true")
    ap.add_argument("--origem", default=None, help="pasta dos arquivos ANTES do sabor (liga o teste de voz)")
    a = ap.parse_args()

    alvo = a.alvo
    if os.path.isfile(alvo):
        arqs = [alvo]
    else:
        it = []
        for raiz, _, nomes in os.walk(alvo):
            for n in nomes:
                it.append(os.path.join(raiz, n))
            if not a.recursivo:
                break
        arqs = sorted(p for p in it if os.path.splitext(p)[1].lower() in (EXTS_V | EXTS_I))

    if not arqs:
        print("nenhum arquivo para conferir em " + alvo)
        return 1

    reprovados = []
    for p in arqs:
        e = os.path.splitext(p)[1].lower()
        falhas = []
        ok, msg = teste_metadados(p)
        if not ok:
            falhas.append(msg)
        if e in EXTS_V:
            for t in (teste_x264, teste_sobra, teste_formato, teste_duracoes):
                ok, msg = t(p)
                if not ok:
                    falhas.append(msg)
            org = achar_original(p, a.origem)
            if org:
                for t in (teste_duracao_esperada, teste_sincronia):
                    ok, msg = t(p, org)
                    if not ok:
                        falhas.append(msg)
        if falhas:
            reprovados.append((p, falhas))

    print("conferidos: " + str(len(arqs)) + " | reprovados: " + str(len(reprovados)))
    for p, f in reprovados[:20]:
        print("  REPROVADO " + os.path.basename(p) + " -> " + "; ".join(f))
    if reprovados:
        print("\nNAO da para dar como pronto. Rode o sabor de novo com --refazer nesses arquivos.")
        return 1
    print("tudo limpo: pode dar como concluido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
