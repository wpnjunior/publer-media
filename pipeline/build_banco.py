# -*- coding: utf-8 -*-
"""Monta o banco final de cards, renderiza os PNG e escreve o index do publicador.

Uso: python build_banco.py banco100.json <pasta_out> <index_destino>

banco100.json: {"posts":[{id,tema,tipo,texto[],legenda,centro?}, ...]}
Ordena intercalando tecnico/reflexivo para o feed nao ficar em bloco.
"""
import os, sys, json, subprocess, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME):
    CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


def intercala(posts):
    """tec, ref, tec, ref... sobra vai no fim, preservando a ordem de cada trilha."""
    tec = [p for p in posts if p.get("tipo") != "reflexivo"]
    ref = [p for p in posts if p.get("tipo") == "reflexivo"]
    out = []
    while tec or ref:
        if tec:
            out.append(tec.pop(0))
        if ref:
            out.append(ref.pop(0))
    return out


def main(banco_path, outdir, index_path):
    posts = json.load(open(banco_path, encoding="utf-8"))["posts"]

    vistos, limpos = set(), []
    for p in posts:
        pid = p["id"]
        if pid in vistos:
            n = 2
            while f"{pid}-{n}" in vistos:
                n += 1
            pid = f"{pid}-{n}"
            p["id"] = pid
        vistos.add(pid)
        limpos.append(p)
    posts = intercala(limpos)

    os.makedirs(outdir, exist_ok=True)
    sys.path.insert(0, BASE)
    from gen_card import build

    for p in posts:
        html = os.path.abspath(os.path.join(outdir, p["id"] + ".html"))
        png = os.path.abspath(os.path.join(outdir, p["id"] + ".png"))
        build(p, html)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1080,1350", "--screenshot=" + png,
                        "file:///" + html.replace("\\", "/")],
                       capture_output=True)
        if not os.path.exists(png):
            print("FALHOU render:", p["id"]); return 1
        os.remove(html)

    idx = {"descricao": "Cards de texto diarios — 14h de Brasilia, um por dia, na ordem desta lista.",
           "cards": [{"id": p["id"], "tema": p["tema"], "published": False, "slot": None,
                      "caption": p["legenda"]} for p in posts]}
    json.dump(idx, open(index_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(posts)} cards renderizados em {outdir}")
    print("index:", index_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
