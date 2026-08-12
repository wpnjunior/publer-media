# -*- coding: utf-8 -*-
"""Overlay 1080x1920 TRANSPARENTE — PAPO NEWS LIMPO (painel unico, sobrio).
Zona segura IG Reels: topo 262 / rodape 566 / direita 196."""
import os, json, sys

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = open(os.path.join(BASE, "logo_b64.txt"), encoding="utf-8").read().strip()

def build(cfg, out_html):
    itens = "".join(
        f'<div class="li"><span class="n">{s}</span><span class="d">{d}</span></div>'
        for s, d in cfg["formula"])
    dica = f'<div class="dica">{cfg["dica"]}</div>' if cfg.get("dica") else ""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden;}}
body{{font-family:'Segoe UI',-apple-system,Roboto,Arial,sans-serif;}}
.safe{{position:absolute;left:54px;right:196px;top:262px;bottom:566px;display:flex;flex-direction:column;}}
.selo{{display:inline-flex;align-self:flex-start;font-weight:900;font-size:32px;
 border-radius:7px;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,.5);margin-bottom:20px;}}
.selo .a{{background:#D62828;color:#fff;padding:8px 15px;}}
.selo .b{{background:#fff;color:#0A0D12;padding:8px 15px;}}
/* PAINEL UNICO — nada de caixinhas soltas */
.card{{background:rgba(8,11,17,.74);backdrop-filter:blur(10px);border-radius:20px;
 padding:34px 36px 30px;box-shadow:0 20px 60px rgba(0,0,0,.5);}}
.chapeu{{font-size:25px;font-weight:800;letter-spacing:4px;text-transform:uppercase;color:#F2C14E;}}
.titulo{{font-size:58px;font-weight:900;line-height:1.05;letter-spacing:-1.2px;color:#fff;margin-top:10px;}}
.rule{{width:96px;height:5px;background:#D62828;border-radius:3px;margin:20px 0 24px;}}
.li{{display:flex;align-items:baseline;justify-content:space-between;gap:20px;
 padding:13px 0;border-bottom:1px solid rgba(255,255,255,.13);}}
.li:last-of-type{{border-bottom:none;}}
.n{{font-size:34px;color:#fff;font-weight:600;}}
.d{{font-size:34px;color:#F2C14E;font-weight:800;white-space:nowrap;}}
.uso{{font-size:27px;color:#AEBDCB;font-weight:600;margin-top:22px;}}
.dica{{font-size:27px;color:#D8E2EA;font-weight:600;margin-top:14px;line-height:1.35;
 padding-left:16px;border-left:3px solid rgba(242,193,78,.75);}}
.alerta{{font-size:22px;color:#9AA9B7;font-weight:700;letter-spacing:.8px;text-transform:uppercase;
 margin-top:26px;padding-top:18px;border-top:1px solid rgba(255,255,255,.14);}}
.marca{{display:flex;align-items:center;gap:12px;margin-top:18px;}}
.chip{{background:#fff;border-radius:10px;padding:5px 7px;}}
.chip img{{height:40px;display:block;}}
.crm{{color:#C9D5E0;font-weight:700;font-size:21px;line-height:1.2;}}
.crm b{{display:block;color:#fff;font-size:24px;}}
</style></head><body>
<div class="safe">
 <div class="selo"><span class="a">PAPO</span><span class="b">NEWS</span></div>
 <div class="card">
  <div class="chapeu">{cfg.get("chapeu","O frasco do dia")}</div>
  <div class="titulo">Frasco para<br>{cfg["tema"]}</div>
  <div class="rule"></div>
  {itens}
  <div class="uso">{cfg["posologia"]}</div>
  {dica}
  <div class="alerta">Isso não é uma recomendação · procure o seu médico</div>
  <div class="marca"><span class="chip"><img src="{LOGO}"></span>
   <span class="crm"><b>Dr. Wagner Novaes</b>CRM-RJ 0127554-2</span></div>
 </div>
</div>
</body></html>"""
    open(out_html, "w", encoding="utf-8").write(html)
    print("overlay PAPO NEWS limpo:", out_html)

if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
