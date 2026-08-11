# -*- coding: utf-8 -*-
# Template v3 — ESTILO REVISTA: foto real full-bleed + overlay escuro + texto branco
import os, base64
BASE = r"C:\Users\Neves\Desktop\CARROSSEL_MEDSCAPE"
OUT = os.path.join(BASE, "slides")
os.makedirs(OUT, exist_ok=True)
LOGO = open(os.path.join(BASE, "logo_b64.txt"), encoding="utf-8").read().strip()
CRM = "CRM-RJ 0127554-2"
TOTAL = 7

def bg64(n):
    p = os.path.join(BASE, "bg", f"bg_{n}.jpg")
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

# (bg, kicker, titulo, corpo, foco_do_overlay)
SLIDES = [
("01","CIÊNCIA · HEPATOLOGIA",
 'Seu fígado pode estar <span class="hl">gordo</span> —<br>e você não sente <span class="hlb">nada</span>.',
 '<b>1 em cada 3 adultos</b> já carrega gordura no fígado. A ciência sabe flagrar antes do dano — sem biópsia.'
 '<span class="pill">Dossiê: Medscape · AASLD 2023 (Hepatology)</span>', "capa"),
("02","A DOENÇA QUE MUDOU DE NOME",
 'Do "fígado<br>gorduroso" ao<br><span class="hl">MASLD</span>',
 'Durante décadas, o nome culpava o álcool — e deixava passar o verdadeiro motor. '
 'Em 2023, a comunidade científica rebatizou a doença: <b>MASLD</b>, a esteatose ligada à <b>disfunção metabólica</b>. '
 'A troca não é cosmética: o problema nasce da <b>resistência à insulina</b>, do açúcar alto e da gordura abdominal — não do copo.', "conteudo"),
("03","A HISTÓRIA NATURAL",
 'Do silêncio<br>à <span class="hlb">cirrose</span>',
 'A progressão é lenta e muda: gordura → <b>inflamação</b> (esteato-hepatite) → <b>fibrose</b> → <b>cirrose</b>. '
 'E o fígado não é a única vítima: a MASLD aumenta também o <b>risco cardiovascular</b>.<br><br>'
 'Por isso a diretriz da <b>AASLD (2023)</b> recomenda rastreio ativo em quem tem obesidade, diabetes tipo 2 ou síndrome metabólica — <b>mesmo sem sintoma</b>.', "conteudo"),
("04","O FIM DA AGULHA",
 'A biópsia<br>perdeu<br>o <span class="hl">posto</span>',
 'Por anos, estadiar o fígado exigia agulha. Hoje, a triagem começa na matemática:'
 '<span class="card"><b>FIB-4</b> — um índice calculado a partir do próprio exame de sangue de rotina.</span>'
 '<span class="card green"><b>Elastografia</b> — ondas de ultrassom medem a rigidez do tecido hepático, sem cortar a pele.</span>', "conteudo"),
("05","A MATEMÁTICA DO RASTREIO",
 'Quatro números<br>que você já<br><span class="hlb">tem</span>',
 '<span class="formula">FIB-4 = (Idade × AST)<br>÷ (Plaquetas × √ALT)</span>'
 '<b>A leitura, segundo a AASLD (2023):</b><br>'
 '• abaixo de <b>1,3</b> — baixo risco de fibrose avançada<br>'
 '• <b>1,3 a 2,67</b> — zona de dúvida: elastografia<br>'
 '• acima de <b>2,67</b> — alto risco: avaliação especializada<br>'
 '<span class="tip">Calculadoras gratuitas (como o MDCalc) fazem a conta em segundos.</span>', "fib"),
("06","A JANELA DE REVERSÃO",
 'O único órgão<br>que se<br><span class="hl">regenera</span>',
 'Flagrada cedo, a esteatose <b>regride</b> — e os números impressionam:<br><br>'
 '• Perder <b>7 a 10% do peso</b> reduz gordura, inflamação e até fibrose inicial<br>'
 '• Cortar <b>açúcar líquido e ultraprocessados</b> tira a lenha da fogueira<br>'
 '• <b>Treino de força</b> melhora a sensibilidade à insulina — o motor do problema', "conteudo"),
("07","O QUE FICA",
 'A pergunta<br>certa no<br>próximo <span class="hlb">exame</span>',
 'Os quatro números do FIB-4 já estarão no seu hemograma de rotina — a maioria dos laudos só não faz a conta. '
 'Perguntar por ela é o tipo de detalhe que muda desfechos.<br><br>'
 'Guarde este dossiê para a próxima consulta.'
 '<span class="fonte">Fontes: Medscape Education · AASLD Practice Guidance 2023 (Hepatology) · Fotos: Pexels. Conteúdo educativo — não substitui consulta médica.</span>', "fecho"),
]

CSS = """
.slide.capasplit{padding:0 !important;}
.tophalf{position:relative;width:1080px;height:625px;overflow:hidden;}
.tophalf img{width:100%;height:100%;object-fit:cover;display:block;}
.seam{position:absolute;left:0;right:0;bottom:0;height:140px;background:linear-gradient(180deg,rgba(7,16,28,0) 0%,#07101C 100%);}
.bottomhalf{position:relative;height:725px;background:linear-gradient(180deg,#07101C 0%,#0B1B2E 100%);
 display:flex;flex-direction:column;align-items:center;text-align:center;padding:6px 80px 40px;}
.kicker2{background:linear-gradient(90deg,#1C9FE0,#3E9B4F);color:#FFF;padding:12px 28px;border-radius:8px;
 letter-spacing:5px;font-size:25px;font-weight:800;text-transform:uppercase;margin-top:4px;}
.titulo2{font-weight:800;line-height:1.12;letter-spacing:-1.5px;color:#FFF;font-size:57px;margin-top:26px;}
.corpo2{font-size:32px;line-height:1.4;color:#C9D6E0;margin-top:18px;font-weight:600;}
.corpo2 b{color:#FFF;}
.capasplit .footer{margin-top:auto;width:100%;}

*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1350px;}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;
 color:#FFFFFF;font-family:'Segoe UI',-apple-system,Roboto,Helvetica,Arial,sans-serif;
 display:flex;flex-direction:column;padding:88px 84px 60px;}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;}
.shade{position:absolute;inset:0;z-index:1;
 background:linear-gradient(180deg,rgba(6,14,24,.86) 0%,rgba(6,14,24,.55) 42%,rgba(6,14,24,.88) 100%);}
.capa .shade{background:linear-gradient(180deg,rgba(6,14,24,.90) 0%,rgba(6,14,24,.48) 55%,rgba(6,14,24,.92) 100%);}
.inner{position:relative;z-index:2;display:flex;flex-direction:column;height:100%;}
.kicker{font-size:29px;letter-spacing:4px;font-weight:800;color:#63D8C4;text-transform:uppercase;
 text-shadow:0 2px 10px rgba(0,0,0,.6);}
.rule{width:104px;height:7px;border-radius:4px;margin:22px 0 34px;background:linear-gradient(90deg,#1C9FE0,#3E9B4F);}
.titulo{font-weight:800;line-height:1.05;letter-spacing:-1.5px;color:#FFFFFF;
 text-shadow:0 3px 18px rgba(0,0,0,.75);}
.capa .titulo{font-size:92px;}
.conteudo .titulo,.fecho .titulo,.fib .titulo{font-size:80px;}
.hl{color:#5FD68A;} .hlb{color:#5BC4F5;}
.corpo{font-size:44px;line-height:1.5;color:#E9F0F6;margin-top:34px;font-weight:400;
 text-shadow:0 2px 12px rgba(0,0,0,.8);}
.corpo b{color:#FFFFFF;font-weight:700;}
.fib .corpo{font-size:38px;line-height:1.45;margin-top:24px;}
.card{display:block;background:rgba(12,30,48,.72);border-left:8px solid #1C9FE0;border-radius:16px;
 padding:26px 30px;margin-top:22px;font-size:40px;line-height:1.4;color:#EAF2F8;
 backdrop-filter:blur(2px);text-shadow:none;}
.card.green{border-left-color:#3E9B4F;}
.card b{color:#FFFFFF;}
.formula{display:block;background:rgba(10,25,42,.85);border:2px solid rgba(91,196,245,.5);color:#FFFFFF;
 border-radius:18px;padding:28px 24px;margin:8px 0 26px;font-size:46px;font-weight:800;text-align:center;line-height:1.25;}
.tip{display:block;margin-top:18px;font-size:32px;color:#B9C7D2;font-weight:600;}
.pill{display:inline-block;margin-top:30px;background:rgba(10,25,42,.8);border:2px solid rgba(99,216,196,.55);
 color:#8FE9D8;font-size:26px;font-weight:800;padding:14px 26px;border-radius:999px;letter-spacing:.3px;}
.fonte{display:block;margin-top:30px;font-size:24px;line-height:1.35;color:#A9B7C2;font-weight:600;
 border-top:2px solid rgba(255,255,255,.18);padding-top:16px;}
.spacer{flex:1;}
.capa .inner{align-items:center;text-align:center;}
.capa .logochip{background:rgba(255,255,255,.94);border-radius:16px;padding:10px 14px;margin-bottom:6px;}
.capa .logochip img{width:130px;display:block;}
.capa .kicker{background:linear-gradient(90deg,#1C9FE0,#3E9B4F);color:#FFFFFF;padding:12px 26px;border-radius:8px;
 letter-spacing:5px;font-size:26px;text-shadow:none;margin-top:14px;}
.capa .rule{display:none;}
.capa .titulo{margin-top:auto;}
.capa .corpo{font-size:37px;color:#D6E2EC;margin-top:26px;font-weight:600;}
.footer{display:flex;align-items:center;justify-content:space-between;margin-top:auto;padding-top:28px;
 border-top:2px solid rgba(255,255,255,.18);}
.fbrand{display:flex;align-items:center;gap:18px;}
.fbrand .chip{background:rgba(255,255,255,.95);border-radius:16px;padding:8px 10px;}
.fbrand .chip img{height:58px;display:block;}
.fbrand .crm{font-size:26px;color:#C3D0DB;font-weight:700;line-height:1.25;text-align:left;
 text-shadow:0 1px 8px rgba(0,0,0,.7);}
.fbrand .crm b{color:#FFFFFF;display:block;font-size:29px;}
.pg{font-size:30px;color:#5BC4F5;font-weight:800;text-shadow:0 1px 8px rgba(0,0,0,.7);}
"""


TPL_CAPA_SPLIT = """<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="slide capasplit">
 <div class="tophalf"><img src="{bgtop}"><div class="seam"></div></div>
 <div class="bottomhalf">
  <div class="kicker2">{kicker}</div>
  <div class="titulo2">{titulo}</div>
  <div class="corpo2">{corpo}</div>
  <div class="footer"><div class="fbrand"><span class="chip"><img src="{logo}"></span><span class="crm"><b>Dr. Wagner Novaes</b>{crm}</span></div><div class="pg">1/{total}</div></div>
 </div>
</div></body></html>"""

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="slide {tipo}">
 <img class="bg" src="{bg}"><div class="shade"></div>
 <div class="inner">
  {logotop}
  <div class="kicker">{kicker}</div><div class="rule"></div>
  <div class="titulo">{titulo}</div>
  <div class="corpo">{corpo}</div>
  <div class="spacer"></div>
  <div class="footer"><div class="fbrand"><span class="chip"><img src="{logo}"></span><span class="crm"><b>Dr. Wagner Novaes</b>{crm}</span></div><div class="pg">{pg}/{total}</div></div>
 </div>
</div></body></html>"""

import base64 as _b64
def file64(p):
    return "data:image/jpeg;base64,"+_b64.b64encode(open(p,"rb").read()).decode()
for i,(bg,k,t,c,tipo) in enumerate(SLIDES,1):
    if tipo=="capa":
        html = TPL_CAPA_SPLIT.format(css=CSS,bgtop=file64(os.path.join(BASE,"bg","bg_01_top.jpg")),
                      logo=LOGO,kicker=k,titulo=t,corpo=c,crm=CRM,total=TOTAL)
    else:
        html = TPL.format(css=CSS,tipo=tipo,bg=bg64(bg),logo=LOGO,logotop="",
                      kicker=k,titulo=t,corpo=c,crm=CRM,pg=i,total=TOTAL)
    open(os.path.join(OUT,f"slide_{i:02d}.html"),"w",encoding="utf-8").write(html)
print("7 slides estilo REVISTA gerados")
