# -*- coding: utf-8 -*-
"""Roda no GitHub Actions (cron diario): pega o proximo card nao publicado em cards/
e agenda no Instagram as 14h de Brasilia (17:00Z) do dia da execucao."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.error

KEY = os.environ["PUBLER_KEY"].strip()
WS = "6a331bf8de25980271e20cc5"
IG = "6a33206a2e5a43b4b2de3428"
BASE = "https://app.publer.com/api/v1"
H = {"Authorization": "Bearer-API " + KEY, "Publer-Workspace-Id": WS,
     "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 Chrome/126.0", "Accept": "application/json"}
RAW = "https://raw.githubusercontent.com/wpnjunior/publer-media/master/cards/{}.png"
IDX = "cards/index.json"

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

def main():
    idx = json.load(open(IDX, encoding="utf-8"))
    pend = [c for c in idx["cards"] if not c.get("published")]
    if not pend:
        print("ACABOU: todos os cards do banco ja foram agendados. Reabastecer cards/."); return 0
    card = pend[0]
    url = RAW.format(card["id"])
    for _ in range(6):
        try:
            urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
            break
        except Exception:
            time.sleep(8)
    else:
        print("ERRO: raw inacessivel:", url); return 1

    j = req("POST", "/media/from-url", {"media": [{"url": url, "name": "card_" + card["id"]}],
                                        "type": "multi", "direct_upload": False, "in_library": True})
    if "job_id" not in j:
        print("ERRO upload:", json.dumps(j)[:300]); return 1
    r = poll(j["job_id"])
    payload = r.get("payload")
    if isinstance(payload, dict):
        payload = payload.get("media") or payload.get("data") or payload.get("payload") or []
    media = [m for m in (payload or []) if isinstance(m, dict) and m.get("id")]
    if not media:
        print("ERRO: nenhum media id:", json.dumps(r)[:600]); return 1
    mid = [{"id": media[0]["id"], "type": "photo"}]

    # 14h de Brasilia = 17:00Z; se ja passou, empurra pro dia seguinte
    agora = dt.datetime.now(dt.UTC)
    alvo = agora.replace(hour=17, minute=0, second=0, microsecond=0)
    if alvo < agora + dt.timedelta(minutes=50):
        alvo += dt.timedelta(days=1)
    # um card por dia: se o dia-alvo ja tem card na fila, pula pro proximo dia livre
    ocupados = {c["slot"][:10] for c in idx["cards"] if c.get("slot")}
    while alvo.strftime("%Y-%m-%d") in ocupados:
        alvo += dt.timedelta(days=1)
    when = alvo.strftime("%Y-%m-%dT%H:%M:%SZ")

    for _ in range(5):
        body = {"bulk": {"state": "scheduled", "posts": [{
            "networks": {"instagram": {"type": "photo", "media": mid, "text": card["caption"]}},
            "accounts": [{"id": IG, "scheduled_at": when}]}]}}
        j2 = req("POST", "/posts/schedule", body)
        if "job_id" not in j2:
            print("ERRO schedule:", json.dumps(j2)[:300]); return 1
        r2 = poll(j2["job_id"])
        fails = r2.get("payload", {}).get("failures", {}) if isinstance(r2, dict) else {"x": 1}
        if r2.get("status", "").startswith("complete") and not fails:
            print("AGENDADO:", card["id"], when)
            card["published"] = True
            card["slot"] = when
            json.dump(idx, open(IDX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            return 0
        msg = json.dumps(fails)
        if "another post at this time" in msg:
            alvo += dt.timedelta(minutes=5)
            when = alvo.strftime("%Y-%m-%dT%H:%M:%SZ")
            print("conflito, tentando", when)
            continue
        print("ERRO agendamento:", msg[:300]); return 1
    print("ERRO: conflitos seguidos"); return 1

if __name__ == "__main__":
    sys.exit(main())
