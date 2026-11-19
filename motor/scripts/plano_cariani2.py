import sys; sys.path.insert(0,'scripts')
from mk import *
# Cariani v2 (Wagner 14/11 00h33): responder SÓ ao que ele disse no corte + aula rápida da fisiologia do músculo
# com órgãos desenhados (camada fisio) em cima de b-roll (Mixkit), depois o estudo.
# Fala do corte: "ele não come proteína e não faz atividade física, perde gordura, mas o corpo, numa resposta
# fisiológica de emergência, começa a catabolizar músculo também" -> VERDADE.
P='ca'; vd=11.59
r1=round(vd+2.75,2)            # rosto "É verdade, tá? E eu te mostro o porquê."
N1=34.75                        # narração ca2_voz 0 -> 34.75 (até "o corpo demite.")
c1=round(r1+N1,2)               # CTA 6cd9
c2=round(c1+4.12,2)             # narração 34.75 -> fim
dur=round(c2+(37.64-34.75)+0.6,2)
n=lambda v: round(r1+v,2)
SOMBRA="text-shadow:6px 6px 0 #000,0 0 18px rgba(0,0,0,.8)"
def BR(src,t,d,ms=0.3):
    z=[[t,1.04,0.01],[round(t+d,2),1.14,round(d,2)]]
    return [{"tipo":"video","t":round(t,2),"d":round(d,2),"ms":ms,"src":M+src,"box":[0,0,1080,1920],"pos":"center","respira":False,"z":10,"zoom":z},
            {"tipo":"fundo","t":round(t,2),"d":round(d,2),"cor":"rgba(6,14,11,.6)","z":11}]
def TT(t,d,txt,y=250,f="104px Anton",cor="#ffffff",**k):
    return T(t,d,txt,y=y,f=f,cor=cor,css=SOMBRA,vel=0.09,**k)

c=abertura(P,vd,"via @flowpdc","center 11%","Mito ou verdade? 👇","Sem proteína e sem treino, o corpo come músculo?",
  [{"tipo":"numero","t":4.3,"d":7.2,"xy":[0,1150],"valor":766,"suf":" MIL VIEWS","tam":120}])
for L in c:
    if L.get("tipo")=="pergunta": L["escolha"]=1
c+=[{"tipo":"texto","t":vd+0.05,"d":1.7,"xy":[40,1105],"w":1000,"fonte":"150px Anton","cor":"#3ddc84","alinha":"center","txt":"VERDADE.","z":50,"entra":"zoom","css":"text-shadow:10px 10px 0 #000"},
    {"tipo":"video","t":vd,"d":r1-vd,"ms":0,"src":M+"ca2_r1.mp4","box":[0,1140,1080,780],"pos":"center 30%","entra":"desliza","z":45}]

# ---------- AULA, cena A: jejum -> fígado -> gordura -> cérebro pede glicose -> músculo vira glicose ----------
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6}]
c+=BR("br_36150.mp4",r1,4.85,2.0)+BR("br_24055.mp4",n(4.85),4.55,1.0)+BR("br_100545.mp4",n(9.4),5.95,0.5)
c+=[{"tipo":"fisio","t":r1,"d":15.3,"z":30,
     "orgaos":[{"k":"figado","xy":[290,1040],"s":.72,"t":0.15,"rotulo":"FÍGADO"},
               {"k":"gordura","xy":[800,1040],"s":.7,"t":4.95,"rotulo":"GORDURA"},
               {"k":"cerebro","xy":[540,660],"s":.72,"t":7.25,"rotulo":"CÉREBRO","rot_y":200},
               {"k":"musculo","xy":[540,1450],"s":.68,"t":10.6,"rotulo":"MÚSCULO","rot_y":175}],
     "fluxos":[{"de":[290,940],"para":[160,430],"curva":-60,"cor":"#ffffff","t":2.05,"d":2.7,"n":5,"rotulo":"AÇÚCAR","viagem":1.1},
               {"de":[800,940],"para":[930,420],"curva":-60,"cor":"#f6d26b","t":5.2,"d":1.9,"n":6,"rotulo":"ENERGIA","viagem":1.0},
               {"de":[600,1370],"para":[380,1110],"curva":90,"cor":"#ffd400","t":11.6,"d":3.4,"n":8,"rotulo":"AMINOÁCIDOS","viagem":1.1},
               {"de":[250,955],"para":[430,720],"curva":-40,"cor":"#4dd8ff","t":13.15,"d":2.0,"n":6,"rotulo":"GLICOSE","viagem":0.9}],
     "pulsos":[{"o":0,"t":2.2},{"o":1,"t":5.3},{"o":2,"t":7.9},{"o":2,"t":8.6},{"o":3,"t":10.75},{"o":0,"t":13.2}]},
   TT(n(0.1),1.9,"EM JEJUM, A INSULINA CAI"),
   TT(n(2.03),2.82,"AÇÚCAR DO FÍGADO: ~1 DIA",f="92px Anton",cor="#f2c230"),
   TT(n(4.92),2.28,"AÍ VAI A GORDURA ✓"),
   TT(n(7.22),2.2,"O CÉREBRO QUER GLICOSE",cor="#4dd8ff"),
   TT(n(9.44),2.1,"DE ONDE? DO MÚSCULO",cor="#ff5a5f"),
   TT(n(11.56),3.75,"MÚSCULO VIRA GLICOSE",cor="#f2c230"),
   {"tipo":"flash","t":n(15.3),"d":0.2,"max":0.5}]

# ---------- cena B: sem proteína e sem treino, o corpo desmonta ----------
c+=BR("br_4607.mp4",n(15.3),5.95,3.0)
c+=[{"tipo":"fisio","t":n(15.3),"d":5.95,"z":30,
     "orgaos":[{"k":"prato","xy":[290,780],"s":.6,"t":0.1,"rotulo":"PROTEÍNA"},
               {"k":"haltere","xy":[790,780],"s":.6,"t":1.1,"rotulo":"TREINO"},
               {"k":"musculo","xy":[540,1330],"s":.9,"t":0.25,"rotulo":"MÚSCULO","rot_y":175}],
     "pulsos":[{"o":2,"t":2.6}],
     "encolhe":[{"o":2,"t":3.7,"para":.5,"d":1.7}]},
   {"tipo":"desenho","t":n(15.85),"d":5.4,"formas":[{"k":"x","c":[290,760],"s":120}],"espessura":16,"cor":"#ff2d3d","z":45},
   {"tipo":"desenho","t":n(16.85),"d":4.4,"formas":[{"k":"x","c":[790,760],"s":120}],"espessura":16,"cor":"#ff2d3d","z":45},
   TT(n(15.35),3.4,"SEM PROTEÍNA, SEM TREINO"),
   TT(n(18.79),2.46,"DESMONTA MAIS DO QUE CONSTRÓI",cor="#ff5a5f"),
   {"tipo":"flash","t":n(21.25),"d":0.2,"max":0.5}]

# ---------- cena C: o treino protege, mas não zera ----------
c+=BR("br_100543.mp4",n(21.25),2.45,2.0)
c+=[TT(n(21.27),1.25,"TREINO PROTEGE ✓",y=560,f="140px Anton",cor="#3ddc84"),
    TT(n(22.52),1.18,"MAS NÃO ZERA",y=560,f="170px Anton",cor="#f2c230",anim=None,entra="zoom"),
    {"tipo":"gigante","t":n(22.4),"d":0.6,"txt":"ZERA?","y":1150,"tam":260,"cor":"rgba(255,255,255,.16)","x":[1000,-1400],"z":20}]

# ---------- cena D: o estudo ----------
c+=[{"tipo":"flash","t":n(23.7),"d":0.2,"max":0.5}]
c+=BR("br_22510.mp4",n(23.7),5.3,4.0)+BR("br_40788.mp4",n(29.0),2.05,1.0)
c+=[TT(n(23.72),3.15,"IDOSOS EMAGRECENDO",y=300,f="120px Anton"),
    {"tipo":"numero","t":n(26.9),"d":4.15,"xy":[0,560],"valor":5,"pre":"-","suf":"%","rotulo":"de massa magra, só aeróbico","tam":260,"cor":"#ff5a5f","z":44},
    {"tipo":"numero","t":n(29.0),"d":2.05,"xy":[0,1020],"valor":2,"pre":"-","suf":"%","rotulo":"com musculação","tam":260,"cor":"#3ddc84","z":44},
    F(n(23.72),7.33,"Villareal et al., N Engl J Med 2017 (160 idosos com obesidade, 6 meses de dieta)")]

# ---------- cena E: músculo é igual funcionário ----------
c+=[{"tipo":"flash","t":n(31.03),"d":0.2,"max":0.5}]
c+=BR("br_918.mp4",n(31.03),3.72,1.0)
c+=[{"tipo":"fisio","t":n(31.03),"d":3.72,"z":30,
     "orgaos":[{"k":"musculo","xy":[540,1080],"s":1.0,"t":0.05,"rotulo":"MÚSCULO","rot_y":180}],
     "encolhe":[{"o":0,"t":2.0,"para":.62,"d":1.2}]},
    TT(n(31.05),1.5,"MÚSCULO = FUNCIONÁRIO",y=300,f="112px Anton"),
    TT(n(32.55),2.2,"SEM SERVIÇO...",y=300,f="120px Anton",cor="#f2c230"),
    {"tipo":"carimbo","t":n(33.6),"d":c1-n(33.6),"xy":[170,1230],"txt":"DEMITIDO","tam":150,"rot":-10,"z":60,"cor":"#ff2d3d","blend":"normal","css":"background:rgba(255,255,255,.9)"}]

# ---------- CTA (6cd9) + fecho ----------
c+=[{"tipo":"glitch","t":c1-0.05,"d":0.25},
    {"tipo":"video","t":c1,"d":4.12,"ms":0,"src":M+"ca2_cta.mp4","box":[0,0,1080,1920],"pos":"center 30%","zoom":[[c1,1.0,0.01],[c1+2.6,1.1,0.3]],"z":40},
    {"tipo":"barra","t":c1+0.2,"d":3.87,"y":215,"txt":"AULA VALEU? SEGUE + CURTE","cor":"#c6ff3d","cor_txt":"#0b1512"}]
c+=B(P+"_viral_blur.mp4",c2,dur-c2,25.0)
c+=[{"tipo":"flash","t":c2,"d":0.2,"max":0.5},
    T(c2+0.03,1.6,"FORÇA + PROTEÍNA",y=420,f="150px Anton"),
    T(c2+1.65,dur-c2-1.65,"COMBINA COM SEU MÉDICO",y=420,f="130px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
    {"tipo":"carimbo","t":c2+1.95,"d":dur-c2-1.95,"xy":[60,800],"txt":"MÚSCULO COM SERVIÇO FICA","tam":96,"rot":-7,"z":60},
    F(c2,dur-c2,"Villareal et al., N Engl J Med 2017 · doi 10.1056/NEJMoa1616338")]

voz=[{"src":M+"ca_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"ca_viral.words.json"},
     {"src":M+"ca2_r1.mp4","t":vd,"ms":0,"d":round(r1-vd,2),"palavras":M+"ca2_r1.words.json"},
     {"src":M+"ca2_voz.wav","t":r1,"ms":0,"d":N1,"palavras":M+"ca2_voz.words.json"},
     {"src":M+"ca2_cta.mp4","t":c1,"ms":0,"d":4.12,"palavras":M+"ca2_cta.words.json"},
     {"src":M+"ca2_voz.wav","t":c2,"ms":N1,"d":round(37.64-N1,2),"palavras":M+"ca2_voz.words.json"}]
musica=[{"src":"m_investiga","t":r1,"ms":0,"d":round(c1-r1,2),"gain":0.32,"fade":0.8}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.3,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"boom","t":vd+0.05,"gain":0.5,"pico":0.3,"d":1.2},
 {"src":"glitch","t":r1-0.05,"gain":0.5},{"src":"whoosh","t":r1,"gain":0.5,"pico":0.45},
 {"src":"boing","t":n(0.15),"gain":0.3},{"src":"whoosh2","t":n(4.85),"gain":0.35},{"src":"boing","t":n(4.95),"gain":0.3},
 {"src":"whoosh2","t":n(9.4),"gain":0.35},{"src":"boing","t":n(7.25),"gain":0.3},{"src":"boing","t":n(10.6),"gain":0.35},
 {"src":"riser","t":n(11.6),"gain":0.25,"d":3.4},{"src":"whoosh","t":n(15.3),"gain":0.45,"pico":0.45},
 {"src":"scratch","t":n(15.85),"gain":0.3},{"src":"scratch","t":n(16.85),"gain":0.3},{"src":"whoosh2","t":n(18.79),"gain":0.35},
 {"src":"whoosh","t":n(21.25),"gain":0.45,"pico":0.45},{"src":"boom","t":n(22.52),"gain":0.55,"pico":0.3,"d":1.2},
 {"src":"whoosh2","t":n(23.7),"gain":0.4},{"src":"pagina","t":n(23.75),"gain":0.35},{"src":"boom","t":n(26.9),"gain":0.6,"pico":0.3,"d":1.5},{"src":"boing","t":n(29.0),"gain":0.4},
 {"src":"whoosh","t":n(31.03),"gain":0.45,"pico":0.45},{"src":"boom","t":n(33.6),"gain":0.65,"pico":0.3,"d":1.5},
 {"src":"glitch","t":c1-0.05,"gain":0.5},{"src":"notif","t":c1+0.2,"gain":0.4},{"src":"glitch","t":c2-0.05,"gain":0.5},
 {"src":"whoosh2","t":c2+1.65,"gain":0.4},{"src":"boom","t":c2+1.95,"gain":0.6,"pico":0.3,"d":1.5}]
for L in c:
    if vd<=L.get("t",0)<c1-0.06: L["fixo"]=True
salvar("react_cariani2",dur,84,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000],[r1,c1,1730]]})
import json
p=json.load(open('planos/react_cariani2.json')); p['audio']['musica']=musica
json.dump(p,open('planos/react_cariani2.json','w'),ensure_ascii=False,indent=1)
print("ok dur",dur)
