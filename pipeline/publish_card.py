# -*- coding: utf-8 -*-
"""Roda no GitHub Actions (cron diario ~14h BRT): pega o proximo card nao publicado em cards/
e publica NA HORA no Instagram pela API oficial da Meta (Content Publishing API, gratis).
Substituiu o Publer em 07/10/2026 (Publer exige plano Business pra API).
A API da Meta nao agenda post de feed — por isso o cron roda no horario e publica direto."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error

TOKEN = os.environ["IG_TOKEN"].strip()   # token de PAGINA (nao expira), gerado por pipeline/ig_token.py
IG = "17841401642025519"                 # Instagram business do Dr. Wagner
GRAPH = "https://graph.facebook.com/v25.0"
RAW = "https://raw.githubusercontent.com/wpnjunior/publer-media/master/cards/jpg/{}.jpg"
IDX = "cards/index.json"

def req(m, p, params=None):
    params = dict(params or {}, access_token=TOKEN)
    data = urllib.parse.urlencode(params).encode()
    url = GRAPH + p
    if m == "GET":
        url, data = url + "?" + data.decode(), None
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url, data=data, method=m), timeout=120).read().decode())
    except urllib.error.HTTPError as e:
        return {"_err": e.code, "_b": e.read().decode()[:400]}

def main():
    idx = json.load(open(IDX, encoding="utf-8"))
    pend = [c for c in idx["cards"] if not c.get("published")]
    if not pend:
        print("ACABOU: todos os cards do banco ja foram publicados. Reabastecer cards/."); return 0

    # um card por dia: o cron reserva so age se hoje ficou sem card
    agora = dt.datetime.now(dt.UTC)
    hoje = agora.strftime("%Y-%m-%d")
    if any((c.get("slot") or "").startswith(hoje) for c in idx["cards"]):
        print("HOJE ja tem card publicado, nada a fazer."); return 0

    card = pend[0]
    url = RAW.format(card["id"])
    for _ in range(6):
        try:
            urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
            break
        except Exception:
            time.sleep(8)
    else:
        print("ERRO: jpg inacessivel (a API do IG so aceita JPEG; rodar pipeline/png2jpg.py):", url); return 1

    c = req("POST", f"/{IG}/media", {"image_url": url, "caption": card["caption"]})
    if "id" not in c:
        print("ERRO container:", json.dumps(c)[:400]); return 1
    # espera o IG baixar e processar a imagem
    for _ in range(20):
        s = req("GET", "/" + c["id"], {"fields": "status_code"})
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") == "ERROR":
            print("ERRO processamento:", json.dumps(s)[:400]); return 1
        time.sleep(5)
    p = req("POST", f"/{IG}/media_publish", {"creation_id": c["id"]})
    if "id" not in p:
        print("ERRO publish:", json.dumps(p)[:400]); return 1

    print("PUBLICADO:", card["id"], "media", p["id"])
    card["published"] = True
    card["slot"] = agora.strftime("%Y-%m-%dT%H:%M:%SZ")
    card["ig_media"] = p["id"]
    json.dump(idx, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 0

if __name__ == "__main__":
    sys.exit(main())
