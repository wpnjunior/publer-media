# -*- coding: utf-8 -*-
"""Card 1080x1350 estilo post de texto — fundo branco, avatar + @ + selo verificado.
Uso: python gen_card.py banco.json <indice|id> saida.html
"""
import os, json, sys, base64

BASE = os.path.dirname(os.path.abspath(__file__))
def b64(p):
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()

AVATAR = b64(os.path.join(BASE, "assets", "avatar.png"))
LOGO = open(os.path.join(BASE, "assets", "logo_b64.txt"), encoding="utf-8").read().strip()

def escala(post):
    """Fonte cai conforme o texto cresce — o card nunca estoura."""
    n = sum(len(t) for t in post["texto"])
    for limite, fs, lh in ((260, 50, 1.40), (420, 45, 1.40), (620, 40, 1.38),
                           (900, 34, 1.36), (1300, 28, 1.34)):
        if n <= limite:
            return fs, lh
    return 24, 1.32

def build(post, out_html):
    fs, lh = escala(post)
    centro = post.get("centro")
    paras = "".join(f"<p>{t}</p>" for t in post["texto"])
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1350px;}}
body{{background:#fff;font-family:'Segoe UI',-apple-system,Roboto,Helvetica,Arial,sans-serif;
 padding:70px 76px 54px;display:flex;flex-direction:column;color:#15191E;}}
.miolo{{flex:1;display:flex;flex-direction:column;justify-content:center;}}
.top{{display:flex;align-items:center;gap:18px;margin-bottom:40px;
 {"justify-content:center;" if centro else ""}}}
.top img.av{{width:80px;height:80px;border-radius:50%;display:block;}}
.nome{{display:flex;align-items:center;gap:9px;font-size:34px;font-weight:800;}}
.ver{{width:32px;height:32px;}}
.txt p{{font-size:{fs}px;line-height:{lh};font-weight:600;margin-bottom:{int(fs*0.62)}px;
 {"text-align:center;" if centro else ""}}}
.txt p:last-child{{margin-bottom:0;}}
.rod{{display:flex;align-items:center;justify-content:space-between;
 border-top:2px solid #EAEEF2;padding-top:22px;}}
.marca{{display:flex;align-items:center;gap:13px;}}
.marca img{{height:52px;display:block;}}
.crm{{font-size:22px;color:#7B8896;font-weight:700;line-height:1.25;}}
.crm b{{display:block;color:#15191E;font-size:25px;}}
.selo{{display:inline-flex;font-weight:900;font-size:21px;border-radius:6px;overflow:hidden;}}
.selo .a{{background:#D62828;color:#fff;padding:6px 11px;}}
.selo .b{{background:#15191E;color:#fff;padding:6px 11px;}}
</style></head><body>
 <div class="miolo">
  <div class="top">
   <img class="av" src="{AVATAR}">
   <span class="nome">dr.wagnernovaesjr
    <svg class="ver" viewBox="0 0 24 24" fill="#1C9FE0"><path d="M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81C14.67 2.63 13.43 1.75 12 1.75s-2.67.88-3.34 2.19c-1.39-.46-2.9-.2-3.91.81s-1.27 2.52-.81 3.91C2.63 9.33 1.75 10.57 1.75 12s.88 2.67 2.19 3.34c-.46 1.39-.2 2.9.81 3.91s2.52 1.27 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.67-.88 3.34-2.19c1.39.46 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34zm-11.71 4.2L6.8 12.46l1.41-1.42 2.26 2.26 4.8-5.23 1.47 1.36-6.2 6.77z"/></svg>
   </span>
  </div>
  <div class="txt">{paras}</div>
 </div>
 <div class="rod">
  <div class="marca"><img src="{LOGO}">
   <span class="crm"><b>Dr. Wagner Novaes</b>CRM-RJ 0127554-2 · conteúdo educativo</span></div>
  <span class="selo"><span class="a">PAPO</span><span class="b">NEWS</span></span>
 </div>
</body></html>"""
    open(out_html, "w", encoding="utf-8").write(html)
    return post

if __name__ == "__main__":
    banco = json.load(open(sys.argv[1], encoding="utf-8"))["posts"]
    chave = sys.argv[2]
    post = banco[int(chave)] if chave.isdigit() else next(p for p in banco if p["id"] == chave)
    build(post, sys.argv[3])
    print("card ok:", sys.argv[3], "|", post["id"])
