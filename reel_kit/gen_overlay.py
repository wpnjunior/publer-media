# -*- coding: utf-8 -*-
"""Overlay 1080x1920 TRANSPARENTE — v2 com ZONA SEGURA do Instagram Reels.
Interface do IG cobre: topo ~260px, rodapé ~560px (nome/legenda/musica), direita ~190px (botoes).
Todo o conteudo vive no miolo seguro. Tarjas translucidas com blur."""
import os, json, sys

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = open(os.path.join(BASE, "logo_b64.txt"), encoding="utf-8").read().strip()

def build(cfg, out_html):
    itens = "".join(f'<div class="tarja item"><b>{s}</b> <span class="dose">{d}</span></div>' for s, d in cfg["formula"])
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden;}}
body{{font-family:'Segoe UI',-apple-system,Roboto,Arial,sans-serif;}}
/* ZONA SEGURA: 260 topo · 560 rodape · 190 direita */
.safe{{position:absolute;left:56px;right:200px;top:270px;bottom:570px;
 display:flex;flex-direction:column;justify-content:flex-start;}}
.tarja{{display:table;background:rgba(0,0,0,.58);backdrop-filter:blur(6px);
 color:#FFF;padding:11px 20px;border-radius:10px;margin-bottom:9px;
 font-size:37px;line-height:1.22;font-weight:600;text-shadow:0 2px 6px rgba(0,0,0,.55);}}
.urg{{font-size:34px;font-weight:800;background:rgba(0,0,0,.62);color:#E8B84B;text-transform:uppercase;letter-spacing:1.2px;text-shadow:0 2px 8px rgba(0,0,0,.75);}}
.titulo{{font-size:46px;font-weight:800;letter-spacing:.3px;background:rgba(0,0,0,.66);margin:14px 0 14px;}}
.titulo .hl{{color:#5FD68A;}}
.item{{font-size:36px;padding:9px 20px;margin-bottom:7px;}}
.item b{{color:#FFF;}} .dose{{color:#9FE8C0;font-weight:700;margin-left:14px;}}
.uso{{font-size:30px;color:#F0F0F0;font-weight:600;margin-top:6px;}}
.dica{{background:rgba(10,58,38,.62);font-size:30px;max-width:660px;margin-top:10px;}}
.alerta{{background:rgba(0,0,0,.66);color:#FF4136;font-weight:800;font-size:29px;letter-spacing:.3px;margin-top:12px;}}
/* marca discreta acima da faixa que o IG cobre */
.marca{{position:absolute;left:56px;bottom:600px;display:flex;align-items:center;gap:13px;}}
.chip{{background:rgba(255,255,255,.95);border-radius:11px;padding:6px 8px;}}
.chip img{{height:46px;display:block;}}
.crm{{color:#FFF;font-weight:700;font-size:23px;line-height:1.2;text-shadow:0 2px 8px rgba(0,0,0,.9);}}
.crm b{{display:block;font-size:26px;}}
</style></head><body>
<div class="safe">
 <div class="tarja urg">{cfg["urgencia1"]}</div>
 <div class="tarja urg">{cfg["urgencia2"]}</div>
 <div class="tarja titulo">FRASCO PARA <span class="hl">{cfg["tema"].upper()}</span></div>
 {itens}
 <div class="tarja uso">📍 {cfg["posologia"]}</div>
 <div class="tarja dica">💡 <b>Dica de rotina:</b> {cfg["dica"]}</div>
 <div class="tarja alerta">ISSO NÃO É UMA RECOMENDAÇÃO · PROCURE O SEU MÉDICO</div>
</div>
<div class="marca"><span class="chip"><img src="{LOGO}"></span>
<span class="crm"><b>Dr. Wagner Novaes</b>CRM-RJ 0127554-2</span></div>
</body></html>"""
    open(out_html, "w", encoding="utf-8").write(html)
    print("overlay v2 (zona segura) ok:", out_html)

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    build(cfg, sys.argv[2])
