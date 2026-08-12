# -*- coding: utf-8 -*-
"""Molde NEWS — carrossel estilo portal de notícia médica (selo + manchete sobre foto).
Uso: python gen_news.py conteudo.json  -> gera slides_news/slide_NN.html
"""
import os, base64, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("NEWS_OUT", os.path.join(BASE, "slides_news"))
os.makedirs(OUT, exist_ok=True)
LOGO = open(os.path.join(BASE, "pipeline", "logo_b64.txt"), encoding="utf-8").read().strip()
CRM = "CRM-RJ 0127554-2"

def img64(path):
    p = path if os.path.isabs(path) else os.path.join(BASE, "bg_bank", path)
    ext = "png" if p.lower().endswith(".png") else "jpeg"
    return f"data:image/{ext};base64," + base64.b64encode(open(p, "rb").read()).decode()

CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1350px;}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;background:#0A0D12;
 font-family:'Segoe UI',-apple-system,Roboto,Helvetica,Arial,sans-serif;color:#fff;}
.foto{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.veu{position:absolute;inset:0;
 background:linear-gradient(180deg,rgba(6,9,14,.62) 0%,rgba(6,9,14,.22) 32%,rgba(6,9,14,.86) 66%,rgba(6,9,14,.97) 100%);}
/* CAPA */
.capa .veu{background:linear-gradient(180deg,rgba(6,9,14,.10) 0%,rgba(6,9,14,0) 42%,rgba(6,9,14,.80) 72%,rgba(4,6,10,.97) 100%);}
.capa .selo{font-size:40px;order:2;margin-bottom:20px;}
.capa .push{order:1;}
.capa .manchete{order:3;}
.capa .sub{order:4;}
.capa .fonte{order:5;}
.capa .rodape{order:9;}
.capa .editoria{display:none;}
.capa .linha{display:none;}
.capa .manchete{font-size:62px;line-height:1.14;letter-spacing:-1px;}
.capa .sub{font-size:30px;margin-top:16px;color:#C7D3DE;}
.capa .wrap{justify-content:flex-end;}
.wrap{position:absolute;inset:0;padding:64px 62px 58px;display:flex;flex-direction:column;}
.selo{display:inline-flex;align-items:center;gap:0;align-self:flex-start;font-weight:900;
 font-size:36px;letter-spacing:.5px;border-radius:8px;overflow:hidden;box-shadow:0 6px 22px rgba(0,0,0,.5);}
.selo .a{background:#D62828;color:#fff;padding:12px 18px;}
.selo .b{background:#fff;color:#0A0D12;padding:12px 18px;}
.editoria{margin-top:18px;align-self:flex-start;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.34);
 color:#fff;font-size:24px;font-weight:800;letter-spacing:4px;text-transform:uppercase;padding:9px 20px;border-radius:6px;}
.push{flex:1;}
.manchete{font-size:82px;font-weight:900;line-height:1.06;letter-spacing:-1.6px;
 text-shadow:0 4px 24px rgba(0,0,0,.85);}
.capa .manchete{font-size:88px;}
.manchete .hl{color:#F2C14E;}
.linha{width:120px;height:8px;background:#D62828;border-radius:4px;margin:26px 0 22px;}
.sub{font-size:36px;line-height:1.42;color:#D9E1E8;font-weight:600;margin-top:22px;
 text-shadow:0 2px 12px rgba(0,0,0,.8);}
.sub b{color:#fff;}
.corpo{font-size:40px;line-height:1.45;color:#E6ECF2;font-weight:400;margin-top:20px;
 text-shadow:0 2px 12px rgba(0,0,0,.8);}
.corpo b{color:#fff;font-weight:700;}
.destaque{display:block;background:rgba(214,40,40,.16);border-left:8px solid #D62828;border-radius:12px;
 padding:24px 26px;margin-top:22px;font-size:36px;line-height:1.35;}
.numero{font-size:150px;font-weight:900;color:#F2C14E;line-height:.9;letter-spacing:-6px;
 text-shadow:0 4px 20px rgba(0,0,0,.7);}
.rodape{display:flex;align-items:center;justify-content:space-between;margin-top:auto;padding-top:26px;
 border-top:2px solid rgba(255,255,255,.2);}
.marca{display:flex;align-items:center;gap:16px;}
.chip{background:#fff;border-radius:12px;padding:7px 9px;}
.chip img{height:54px;display:block;}
.crm{font-size:25px;color:#B9C6D2;font-weight:700;line-height:1.25;}
.crm b{display:block;color:#fff;font-size:28px;}
.pg{font-size:27px;font-weight:900;color:#F2C14E;}
.fonte{display:block;margin-top:18px;font-size:23px;color:#93A3B1;font-weight:600;line-height:1.35;}
.print{display:block;width:100%;border-radius:14px;border:3px solid rgba(255,255,255,.5);
 box-shadow:0 16px 44px rgba(0,0,0,.65);margin-top:8px;}
.selo-prova{display:inline-block;background:#D62828;color:#fff;font-size:24px;font-weight:900;
 letter-spacing:3px;text-transform:uppercase;padding:9px 18px;border-radius:6px;margin-bottom:16px;}
.prova .veu{background:linear-gradient(180deg,rgba(6,9,14,.92) 0%,rgba(6,9,14,.88) 100%);}
"""

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="s {tipo}">
 <img class="foto" src="{foto}"><div class="veu"></div>
 <div class="wrap">
  <div class="selo"><span class="a">{marca_a}</span><span class="b">{marca_b}</span></div>
  {editoria}
  <div class="push"></div>
  {numero}
  <div class="manchete">{manchete}</div>
  <div class="linha"></div>
  {texto}
  <div class="rodape">
   <div class="marca"><span class="chip"><img src="{logo}"></span>
    <span class="crm"><b>Dr. Wagner Novaes</b>{crm}</span></div>
   <div class="pg">{pg}/{total}</div>
  </div>
 </div>
</div></body></html>"""

def build(cfg):
    marca_a, marca_b = cfg.get("marca", ["PAPO", "NEWS"])
    slides = cfg["slides"]
    total = len(slides)
    for i, sl in enumerate(slides, 1):
        tipo = sl.get("tipo", "conteudo")
        editoria = f'<div class="editoria">{sl["editoria"]}</div>' if sl.get("editoria") else ""
        numero = f'<div class="numero">{sl["numero"]}</div>' if sl.get("numero") else ""
        txt = ""
        if sl.get("print"):    txt += f'<div class="selo-prova">A fonte</div><img class="print" src="{img64(sl["print"])}">'
        if sl.get("sub"):      txt += f'<div class="sub">{sl["sub"]}</div>'
        if sl.get("corpo"):    txt += f'<div class="corpo">{sl["corpo"]}</div>'
        if sl.get("destaque"): txt += f'<span class="destaque">{sl["destaque"]}</span>'
        if sl.get("fonte"):    txt += f'<span class="fonte">{sl["fonte"]}</span>'
        html = TPL.format(css=CSS, tipo=tipo, foto=img64(sl["foto"]), logo=LOGO, crm=CRM,
                          marca_a=marca_a, marca_b=marca_b, editoria=editoria, numero=numero,
                          manchete=sl["manchete"], texto=txt, pg=i, total=total)
        open(os.path.join(OUT, f"slide_{i:02d}.html"), "w", encoding="utf-8").write(html)
    print(f"{total} slides NEWS gerados em {OUT}")

if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")))
