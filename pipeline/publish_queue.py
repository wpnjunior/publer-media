# -*- coding: utf-8 -*-
"""Roda no GitHub Actions: pega queue/<data>/meta.json + slides PNG já no repo e agenda no Publer."""
import json, os, sys, time, urllib.request, urllib.error, glob

KEY = os.environ["PUBLER_KEY"].strip()
WS = "6a331bf8de25980271e20cc5"
IG = "6a33206a2e5a43b4b2de3428"
BASE = "https://app.publer.com/api/v1"
H = {"Authorization": "Bearer-API " + KEY, "Publer-Workspace-Id": WS,
     "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 Chrome/126.0", "Accept": "application/json"}
RAW = "https://raw.githubusercontent.com/wpnjunior/publer-media/master/{}"

def req(m, p, b=None):
    d = json.dumps(b).encode() if b is not None else None
    r = urllib.request.Request(BASE + p, data=d, headers=H, method=m)
    try:
        return json.loads(urllib.request.urlopen(r, timeout=120).read().decode())
    except urllib.error.HTTPError as e:
        return {"_err": e.code, "_b": e.read().decode()[:400]}

def poll(job, n=40):
    for _ in range(n):
        time.sleep(3)
        s = req("GET", "/job_status/" + job)
        if s.get("status", "").startswith("complete") or s.get("status") == "failed":
            return s
    return {"status": "timeout"}

def main(qdir):
    meta = json.load(open(os.path.join(qdir, "meta.json"), encoding="utf-8"))
    if meta.get("published"):
        print("ja publicado, nada a fazer"); return 0
    slides = sorted(glob.glob(os.path.join(qdir, "slide_*.png")))
    if len(slides) < 5:
        print("ERRO: menos de 5 slides"); return 1
    rel = [os.path.relpath(s, start=os.path.dirname(os.path.dirname(qdir))).replace(os.sep, "/") for s in slides]
    urls = [RAW.format(p) for p in rel]
    # espera raw ficar acessivel
    for u in urls:
        for _ in range(4):
            try:
                urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
                break
            except Exception:
                time.sleep(8)
    media_req = [{"url": u, "name": f"esteira_{i+1}"} for i, u in enumerate(urls)]
    j = req("POST", "/media/from-url", {"media": media_req, "type": "multi", "direct_upload": False, "in_library": True})
    if "job_id" not in j:
        print("ERRO upload:", json.dumps(j)[:300]); return 1
    r = poll(j["job_id"])
    if not r.get("status", "").startswith("complete"):
        print("ERRO upload job:", json.dumps(r)[:300]); return 1
    payload = r.get("payload")
    if isinstance(payload, dict):
        payload = payload.get("media") or payload.get("data") or payload.get("payload") or []
    media = [m for m in (payload or []) if isinstance(m, dict) and m.get("id")]
    if len(media) < len(urls):
        print("AVISO: payload inesperado, bruto:", json.dumps(r)[:800])
    if not media:
        print("ERRO: nenhum media id no payload"); return 1
    mid = [{"id": m["id"], "type": "photo"} for m in media]
    when = meta["schedule_at"]  # ISO UTC ex 2026-08-14T23:00:00Z
    for attempt in range(5):
        body = {"bulk": {"state": "scheduled", "posts": [{
            "networks": {"instagram": {"type": "photo", "media": mid, "text": meta["caption"]}},
            "accounts": [{"id": IG, "scheduled_at": when}]}]}}
        j2 = req("POST", "/posts/schedule", body)
        if "job_id" not in j2:
            print("ERRO schedule:", json.dumps(j2)[:300]); return 1
        r2 = poll(j2["job_id"])
        fails = r2.get("payload", {}).get("failures", {}) if isinstance(r2, dict) else {"x": 1}
        if r2.get("status", "").startswith("complete") and not fails:
            print("AGENDADO:", when)
            meta["published"] = True
            meta["published_at_slot"] = when
            json.dump(meta, open(os.path.join(qdir, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            return 0
        msg = json.dumps(fails)
        if "another post at this time" in msg:
            # empurra 1 dia
            d, t = when.split("T")
            import datetime as dt
            nd = (dt.date.fromisoformat(d) + dt.timedelta(days=1)).isoformat()
            when = nd + "T" + t
            print("conflito, tentando", when)
            continue
        print("ERRO agendamento:", msg[:300]); return 1
    print("ERRO: 5 conflitos seguidos"); return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
