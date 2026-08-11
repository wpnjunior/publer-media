# -*- coding: utf-8 -*-
import json, time, urllib.request, urllib.error
import os
KEY=os.environ.get("PUBLER_KEY","").strip() or (open(os.path.expanduser("~/.claude/publer.key")).read().strip() if os.path.exists(os.path.expanduser("~/.claude/publer.key")) else "")
WS="6a331bf8de25980271e20cc5"
BASE="https://app.publer.com/api/v1"
IG="6a33206a2e5a43b4b2de3428"
H={"Authorization":"Bearer-API "+KEY,"Publer-Workspace-Id":WS,"Content-Type":"application/json","User-Agent":"Mozilla/5.0 Chrome/126.0","Accept":"application/json"}
def req(m,p,b=None):
    d=json.dumps(b).encode() if b is not None else None
    r=urllib.request.Request(BASE+p,data=d,headers=H,method=m)
    try: return json.loads(urllib.request.urlopen(r,timeout=120).read().decode())
    except urllib.error.HTTPError as e: return {"_err":e.code,"_b":e.read().decode()[:400]}
def poll(j,n=40):
    for _ in range(n):
        time.sleep(3); s=req("GET","/job_status/"+j)
        if s.get("status","").startswith("complete") or s.get("status")=="failed": return s
    return {"status":"timeout"}
def upload_images(urls, name):
    media=[{"url":u,"name":"%s_%d"%(name,i+1)} for i,u in enumerate(urls)]
    j=req("POST","/media/from-url",{"media":media,"type":"multi","direct_upload":False,"in_library":True})
    if "job_id" not in j: return None,j
    r=poll(j["job_id"])
    if r.get("status","").startswith("complete"): return r["payload"],r
    return None,r
def schedule_carousel(media_objs, caption, when, networks=("instagram",)):
    mid=[{"id":mo["id"],"type":"photo"} for mo in media_objs]
    ACC={"instagram":IG,"tiktok":"6a332078c7ca16d627869341"}
    net={k:{"type":"photo","media":mid,"text":caption} for k in networks}
    accounts=[{"id":ACC[k],"scheduled_at":when} for k in networks]
    body={"bulk":{"state":"scheduled","posts":[{"networks":net,"accounts":accounts}]}}
    j=req("POST","/posts/schedule",body)
    if "job_id" not in j: return j
    return poll(j["job_id"])
