# -*- coding: utf-8 -*-
"""Overlay 1080x1920 TRANSPARENTE — identidade PAPO NEWS aplicada ao Reel "FRASCO PARA X".
Zona segura do IG Reels: topo ~262px, rodape ~566px, direita ~196px."""
import os, json, sys

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = open(os.path.join(BASE, "logo_b64.txt"), encoding="utf-8").read().strip()

def build(cfg, out_html):
    itens = "".join(
        f'<div class="item"><span class="bola"></span><b>{s}</b><span class="dose">{d}</span></div>'
        for s, d in cfg["formula"])
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden;}}
body{{font-family:'Segoe UI',-apple-system,Roboto,Arial,sans-serif;}}
.safe{{position:absolute;left:54px;right:196px;top:262px;bottom:566px;display:flex;flex-direction:column;}}
/* SELO PAPO NEWS */
.selo{{display:inline-flex;align-self:flex-start;font-weight:900;font-size:34px;letter-spacing:.5px;
 border-radius:8px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,.55);margin-bottom:16px;}}
.selo .a{{background:#D62828;color:#fff;padding:9px 16px;}}
.selo .b{{background:#fff;color:#0A0D12;padding:9px 16px;}}
/* URGENCIA dourada caixa alta */
.urg{{display:table;background:rgba(6,9,14,.72);backdrop-filter:blur(6px);color:#F2C14E;
 font-size:31px;font-weight:800;text-transform:uppercase;letter-spacing:1.1px;
 padding:10px 18px;border-radius:8px;margin-bottom:8px;text-shadow:0 2px 8px rgba(0,0,0,.8);}}
/* TITULO estilo manchete */
.titulo{{font-size:60px;font-weight:900;line-height:1.04;letter-spacing:-1.4px;color:#fff;
 margin:16px 0 6px;text-shadow:0 4px 20px rgba(0,0,0,.9);}}
.titulo .hl{{color:#F2C14E;}}
.linha{{width:110px;height:7px;background:#D62828;border-radius:4px;margin:12px 0 18px;}}
/* FORMULA */
.item{{display:flex;align-items:center;gap:14px;background:rgba(6,9,14,.62);backdrop-filter:blur(6px);
 border-left:6px solid #D62828;border-radius:9px;padding:11px 18px;margin-bottom:8px;
 font-size:35px;color:#fff;font-weight:600;text-shadow:0 2px 6px rgba(0,0,0,.6);}}
.item .bola{{width:11px;height:11px;border-radius:50%;background:#F2C14E;flex:none;}}
.item .dose{{color:#F2C14E;font-weight:800;margin-left:auto;padding-left:18px;}}
.uso{{display:table;background:rgba(6,9,14,.62);color:#E9EFF5;font-size:29px;font-weight:600;
 padding:10px 18px;border-radius:8px;margin-top:6px;}}
.dica{{display:table;background:rgba(214,40,40,.30);border-left:6px solid #D62828;color:#fff;
 font-size:29px;font-weight:600;padding:14px 18px;border-radius:9px;margin-top:12px;max-width:640px;line-height:1.3;}}
.alerta{{display:table;background:rgba(6,9,14,.80);color:#FF4136;font-weight:900;font-size:27px;
 letter-spacing:.4px;padding:11px 18px;border-radius:8px;margin-top:14px;}}
/* rodape acima da faixa que o IG cobre */
.marca{{display:flex;align-items:center;gap:13px;margin-top:14px;}}
.chip{{background:#fff;border-radius:11px;padding:6px 8px;}}
.chip img{{height:46px;display:block;}}
.crm{{color:#fff;font-weight:700;font-size:23px;line-height:1.2;text-shadow:0 2px 8px rgba(0,0,0,.9);}}
.crm b{{display:block;font-size:26px;}}
</style></head><body>
<div class="safe">
 <div class="selo"><span class="a">PAPO</span><span class="b">NEWS</span></div>
 <div class="urg">{cfg["urgencia1"]}</div>
 <div class="urg">{cfg["urgencia2"]}</div>
 <div class="titulo">FRASCO PARA<br><span class="hl">{cfg["tema"].upper()}</span></div>
 <div class="linha"></div>
 {itens}
 <div class="uso">📍 {cfg["posologia"]}</div>
 <div class="dica">💡 <b>Dica de rotina:</b> {cfg["dica"]}</div>
 <div class="alerta">ISSO NÃO É UMA RECOMENDAÇÃO · PROCURE O SEU MÉDICO</div>
 <div class="marca"><span class="chip"><img src="{LOGO}"></span>
  <span class="crm"><b>Dr. Wagner Novaes</b>CRM-RJ 0127554-2</span></div>
</div>
</body></html>"""
    open(out_html, "w", encoding="utf-8").write(html)
    print("overlay PAPO NEWS ok:", out_html)

if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
