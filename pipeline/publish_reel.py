# -*- coding: utf-8 -*-
"""Publica o Reel FRASCO PARA X: le reels_queue/<data>-<slug>/meta.json + reel.mp4 (ja no repo)
e agenda no Instagram, TikTok e YouTube via Publer. Roda no GitHub Actions (que tem rede + chave)."""
import json, os, sys, time, urllib.request, urllib.error, datetime as dt

KEY = os.environ["PUBLER_KEY"].strip()
WS = "6a331bf8de25980271e20cc5"
IG = "6a33206a2e5a43b4b2de3428"
TT = "6a332078c7ca16d627869341"
YT = "6a33203e2e5a43b4b2de33cb"
BASE = "https://app.publer.com/api/v1"
RAW = "https://raw.githubusercontent.com/wpnjunior/publer-media/master/{}"
H = {"Authorization": "Bearer-API " + KEY, "Publer-Workspace-Id": WS,
     "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 Chrome/126.0", "Accept": "application/json"}

def titulo_yt(texto):
    """YouTube exige titulo: usa a 1a linha util da legenda (max 90 chars)."""
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            return linha[:90]
    return "Dr. Wagner Novaes Jr."


def req(m, p, b=None):
    d = json.dumps(b).encode() if b is not None else None
    r = urllib.request.Request(BASE + p, data=d, headers=H, method=m)
    try:
        return json.loads(urllib.request.urlopen(r, timeout=180).read().decode())
    except urllib.error.HTTPError as e:
        return {"_err": e.code, "_b": e.read().decode()[:400]}

def poll(job, n=60):
    for _ in range(n):
        time.sleep(3)
        s = req("GET", "/job_status/" + job)
        if s.get("status", "").startswith("complete") or s.get("status") == "failed":
            return s
    return {"status": "timeout"}

def main(qdir):
    meta = json.load(open(os.path.join(qdir, "meta.json"), encoding="utf-8"))
    if meta.get("published"):
        print("ja publicado"); return 0
    mp4 = os.path.join(qdir, "reel.mp4")
    if not os.path.exists(mp4):
        print("ERRO: reel.mp4 ausente"); return 1
    url = RAW.format(qdir.replace(os.sep, "/").strip("/") + "/reel.mp4")
    ok = False
    for _ in range(8):
        try:
            urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
            ok = True; break
        except Exception:
            time.sleep(10)
    if not ok:
        print("ERRO: raw inacessivel:", url); return 1

    j = req("POST", "/media/from-url", {"media": [{"url": url, "name": "reel_frasco"}],
                                        "type": "single", "direct_upload": False, "in_library": True})
    if "job_id" not in j:
        print("ERRO upload:", json.dumps(j)[:300]); return 1
    r = poll(j["job_id"])
    pay = r.get("payload")
    if isinstance(pay, dict):
        pay = pay.get("media") or pay.get("data") or []
    media = [m for m in (pay or []) if isinstance(m, dict) and m.get("id")]
    if not media:
        print("ERRO payload:", json.dumps(r)[:400]); return 1
    m = media[0]
    mm = {"id": m["id"], "thumbnails": m.get("thumbnails", []),
          "title": meta.get("titulo", "Frasco"), "default_thumbnail": 0}

    # VIDEO exige >=45min de antecedencia no Publer; garante margem
    when = meta["schedule_at"]
    alvo = dt.datetime.strptime(when, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.UTC)
    minimo = dt.datetime.now(dt.UTC) + dt.timedelta(minutes=50)
    if alvo < minimo:
        alvo = minimo.replace(second=0, microsecond=0)
        print("horario ajustado (regra dos 45min):", alvo.isoformat())

    for _ in range(5):
        w = alvo.strftime("%Y-%m-%dT%H:%M:00Z")
        body = {"bulk": {"state": "scheduled", "posts": [{
            "networks": {
                "instagram": {"type": "video", "media": [mm], "text": meta["caption"]},
                "tiktok": {"type": "video", "media": [mm], "text": meta["caption"]},
                # YouTube so aceita type "video" ("short"/"reel" da "Post type is
                # not valid"); vertical e curto ele mesmo publica como Short
                "youtube": {"type": "video", "media": [mm], "text": meta["caption"],
                            "title": titulo_yt(meta["caption"]), "privacy": "public",
                            "made_for_kids": False},
            },
            "accounts": [{"id": IG, "scheduled_at": w},
                         {"id": TT, "scheduled_at": w},
                         {"id": YT, "scheduled_at": w}]}]}}
        j2 = req("POST", "/posts/schedule", body)
        if "job_id" not in j2:
            print("ERRO schedule:", json.dumps(j2)[:300]); return 1
        r2 = poll(j2["job_id"])
        fails = r2.get("payload", {}).get("failures", {}) if isinstance(r2, dict) else {"x": 1}
        if r2.get("status", "").startswith("complete") and not fails:
            print("REEL AGENDADO:", w)
            meta["published"] = True; meta["slot"] = w
            json.dump(meta, open(os.path.join(qdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            return 0
        if "another post at this time" in json.dumps(fails):
            alvo += dt.timedelta(minutes=10); print("conflito, tentando", alvo.isoformat()); continue
        print("ERRO:", json.dumps(fails)[:300]); return 1
    print("ERRO: conflitos seguidos"); return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
