# -*- coding: utf-8 -*-
"""Roda no GitHub Actions (cron 20h BRT): publica o carrossel da esteira (queue/<data>-<slug>/) NA HORA
no Instagram pela API oficial da Meta. Substituiu o Publer em 23/10/2026 (Publer exige plano Business).

  python pipeline/publish_queue_ig.py preparar   -> escolhe a pasta do dia e passa o SABOR nos slides
                                                   (PNG -> JPEG limpo em <pasta>/jpg/); imprime a pasta
  python pipeline/publish_queue_ig.py publicar <pasta>  -> cria o carrossel e publica; marca meta.json

Entre os dois passos o workflow faz commit+push dos JPEG (a API baixa a imagem pela URL raw do GitHub).
Escolha da pasta: a mais antiga com "published": false e schedule_at <= agora. Uma por dia.
"""
import datetime as dt
import glob
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

IG = "17841401642025519"                 # Instagram business do Dr. Wagner
GRAPH = "https://graph.facebook.com/v25.0"
RAW = "https://raw.githubusercontent.com/wpnjunior/publer-media/master/{}"


def req(m, p, params=None):
    params = dict(params or {}, access_token=os.environ["IG_TOKEN"].strip())
    data = urllib.parse.urlencode(params).encode()
    url = GRAPH + p
    if m == "GET":
        url, data = url + "?" + data.decode(), None
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url, data=data, method=m), timeout=120).read().decode())
    except urllib.error.HTTPError as e:
        return {"_err": e.code, "_b": e.read().decode()[:400]}


def ler(pasta):
    return json.load(open(os.path.join(pasta, "meta.json"), encoding="utf-8"))


def escolher():
    agora = dt.datetime.now(dt.timezone.utc)
    hoje = agora.strftime("%Y-%m-%d")
    pastas = sorted(d for d in glob.glob("queue/*/") if os.path.exists(os.path.join(d, "meta.json")))
    if any((ler(d).get("published_at") or "").startswith(hoje) for d in pastas):
        return None, "HOJE ja saiu carrossel"
    for d in pastas:
        m = ler(d)
        if m.get("published"):
            continue
        try:
            quando = dt.datetime.fromisoformat((m.get("schedule_at") or "").replace("Z", "+00:00"))
        except ValueError:
            continue                                   # sem data valida: nao publica
        if quando > agora:
            continue
        if agora - quando > dt.timedelta(days=2):
            continue   # fila VELHA nao sai sozinha: em 23/10 um carrossel de 21/08 foi ao ar por isso
        return d.rstrip("/\\"), ""
    return None, "nenhum carrossel pendente na fila"


def sabor_jpeg(src, dst):
    """SABOR de imagem (mesmos itens do camuflar_imagem): encolhe mantendo 4:5 exato, mexe 1-3 no
    vermelho do pixel (0,0), salva JPEG novo sem nenhum dado embutido e com qualidade sorteada.
    O Instagram so aceita JPEG e recusa proporcao mais alta que 4:5, por isso 4*d x 5*d."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    w, h = im.size
    d = random.randint(1, 3)
    if abs(w * 5 - h * 4) <= 5:
        im = im.resize((w - 4 * d, h - 5 * d), Image.LANCZOS)
    else:
        im = im.resize((w - d, h - d), Image.LANCZOS)
    px = im.load()
    r, g, b = px[0, 0]
    px[0, 0] = (min(255, r + random.randint(1, 3)), g, b)
    limpa = Image.new("RGB", im.size)
    limpa.putdata(list(im.getdata()))
    limpa.save(dst, "JPEG", quality=random.choice([90, 91, 92, 93, 94]), optimize=True)


def preparar():
    pasta, motivo = escolher()
    if not pasta:
        print("NADA A FAZER:", motivo)
        return 0
    slides = sorted(glob.glob(os.path.join(pasta, "slide_*.png")))
    if not 2 <= len(slides) <= 10:
        print("ERRO: carrossel precisa de 2 a 10 slides; achei", len(slides), "em", pasta)
        return 1
    os.makedirs(os.path.join(pasta, "jpg"), exist_ok=True)
    for s in slides:
        sabor_jpeg(s, os.path.join(pasta, "jpg", os.path.basename(s)[:-4] + ".jpg"))
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a", encoding="utf-8") as f:
        f.write("dir=" + pasta.replace(os.sep, "/") + "\n")
    print("PREPARADO:", pasta, len(slides), "slides com sabor")
    return 0


def esperar(cid, rotulo):
    for _ in range(30):
        s = req("GET", "/" + cid, {"fields": "status_code"})
        if s.get("status_code") == "FINISHED":
            return True
        if s.get("status_code") == "ERROR" or "_err" in s:
            print("ERRO processamento", rotulo, json.dumps(s)[:400])
            return False
        time.sleep(5)
    print("ERRO: tempo esgotado no", rotulo)
    return False


def publicar(pasta, so_testar=False):
    meta = ler(pasta)
    if meta.get("published"):
        print("ja publicado, nada a fazer")
        return 0
    jpgs = sorted(glob.glob(os.path.join(pasta, "jpg", "slide_*.jpg")))
    urls = [RAW.format(j.replace(os.sep, "/")) for j in jpgs]
    for u in urls:                                   # a URL raw demora uns segundos depois do push
        for _ in range(8):
            try:
                urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
                break
            except Exception:
                time.sleep(8)
        else:
            print("ERRO: imagem inacessivel:", u)
            return 1
    filhos = []
    for i, u in enumerate(urls, 1):
        c = req("POST", f"/{IG}/media", {"image_url": u, "is_carousel_item": "true"})
        if "id" not in c or not esperar(c["id"], f"slide {i}"):
            print("ERRO slide", i, json.dumps(c)[:300])
            return 1
        filhos.append(c["id"])
    car = req("POST", f"/{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(filhos), "caption": meta["caption"]})
    if "id" not in car or not esperar(car["id"], "carrossel"):
        print("ERRO carrossel:", json.dumps(car)[:400])
        return 1
    if so_testar:
        print("TESTE OK: carrossel montado e aprovado pela Meta, NAO publicado:", car["id"])
        return 0
    p = req("POST", f"/{IG}/media_publish", {"creation_id": car["id"]})
    if "id" not in p:
        print("ERRO publish:", json.dumps(p)[:400])
        return 1
    meta["published"] = True
    meta["published_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta["ig_media"] = p["id"]
    json.dump(meta, open(os.path.join(pasta, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("PUBLICADO no Instagram:", pasta, "media", p["id"])
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "preparar":
        sys.exit(preparar())
    sys.exit(publicar(sys.argv[2], so_testar="--teste" in sys.argv))
