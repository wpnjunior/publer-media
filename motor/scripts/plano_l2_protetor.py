import sys; sys.path.insert(0,'scripts')
from mk import *
# Lote 2 (14/11): Papo de Médico, "protetor solar bloqueia a vitamina D?" (Pânico/Jovem Pan, @programapanico).
# Trecho do viral (2 pedaços, 11,2 s): "UVB não dá câncer, o UVB dá vermelhidão." + "Eu passo um protetor pra te não
# ver isso, só que eu bloqueei a vitamina mais importante. (Que a D.) A D, não existe nada igual, é a vitamina anticâncer."
# Veredito: MITO nos dois pontos. Não rebate o "anticâncer".
# EDIÇÃO FULL sem b-roll, pele LOUSA: gigantes Anton (cheias e contorno), número 3D, artigo em perspectiva com grifo,
# carimbo, e um desenho grande por cena (fisio_extra/pv_sol, pv_pele, pv_dna, pv_vitd, pv_peneira).
# Voz: 4 blocos HeyGen por clima, SEM atempo: A indignado (r1 + vereditos), B manso (aula), C neutro (estudo), D alegre (fecho).
# Depois: python3 scripts/entrada.py react_l2_protetor assets/midia/pv_ent6.mp4 assets/midia/pv_ent6.words.json 1.88 \
#   'PROTETOR BLOQUEIA A VITAMINA D?' 'falaram isso num programa de TV' && python3 scripts/pele.py react_l2_protetor lousa
P='pv'; vd=11.18
r1=round(vd+3.40,2)              # rosto 6cd9 "Mito, tá? E são dois de uma vez." (3,4 s)
DA,DB,DC,DD=7.96,30.37,22.27,10.75
tA=r1
tB=round(tA+DA+0.6,2)
tC=round(tB+DB+0.6,2)
c1=round(tC+DC+0.4,2)            # CTA 6cd9 (banco cta6)
c2=round(c1+4.12,2)
dur=round(c2+DD+0.6,2)
a=lambda v: round(tA+v,2); b=lambda v: round(tB+v,2); e=lambda v: round(tC+v,2); f=lambda v: round(c2+v,2)
GIZ,AMAR,ROSA,VERM='#f4f1e8','#ffe27a','#ff9fb4','#ff6b6b'
GZ="text-shadow:0 0 3px rgba(255,255,255,.45),5px 6px 0 rgba(0,0,0,.4)"
def TT(t,d,txt,y=360,fz=120,cor=GIZ,**k):
    return T(t,d,txt,y=y,f=f"{fz}px Anton",cor=cor,css=GZ,vel=0.09,**k)
def GIG(t,d,txt,y=1250,tam=460,cont=False,cor="rgba(244,241,232,.10)",ida=True):
    L={"tipo":"gigante","t":round(t,2),"d":round(d,2),"txt":txt,"y":y,"tam":tam,"cor":cor,"z":12,
       "x":[1100,-int(len(txt)*tam*0.52)] if ida else [-int(len(txt)*tam*0.45),900]}
    if cont: L["contorno"]=True
    return L
def FIS(t,d,orgaos,**k):
    L={"tipo":"fisio","t":round(t,2),"d":round(d,2),"z":30,"orgaos":orgaos}; L.update(k); return L
def X(t,d,cx,cy,s=70,cor=VERM): return {"tipo":"desenho","t":round(t,2),"d":round(d,2),"formas":[{"k":"x","c":[cx,cy],"s":s}],"espessura":16,"cor":cor,"z":45}
def CIRC(t,d,pts,cor=ROSA,lw=12):
    return {"tipo":"desenho","t":round(t,2),"d":round(d,2),"formas":[dict(k="circulo",c=[x,y],r=[r,r],t=tt) for x,y,r,tt in pts],"espessura":lw,"cor":cor,"z":35}
FL=lambda t:{"tipo":"flash","t":round(t,2),"d":0.2,"max":0.5}

# ================= abertura: viral em tela dividida + caixinha =================
c=[{"tipo":"cartao","t":0,"d":None,"box":[40,150,1000,640],"aba":"o viral","entra":"whip"},
   {"tipo":"video","t":0,"d":vd,"ms":0,"src":M+P+"_viral.mp4","box":[70,190,940,553],"raio":14,"pos":"center","arroba":"via @programapanico","respira":False,"zoom":[[0,1.0,0.01],[4.0,1.06,0.4],[vd-2.5,1.0,0.4]],"z":30},
   {"tipo":"pergunta","t":0.1,"d":3.95,"xy":[110,870],"w":790,"topo":"Mito ou verdade? 👇","txt":"Protetor solar bloqueia a vitamina D?","botoes":["MITO","VERDADE"],"vel":0.025,"escolha":0,"t_escolha":3.3},
   T(4.1,vd-4.1,"O QUE FOI DITO NA TV",y=880,f="105px Anton",cor="#ffffff",css="text-shadow:6px 6px 0 #000"),
   GIG(4.1,vd-4.1,"UVB",y=1500,tam=420,cont=True,cor="rgba(198,255,61,.35)"),
   {"tipo":"glitch","t":vd-0.05,"d":0.25},
   {"tipo":"foto","t":vd,"d":None,"src":M+P+"_still.jpg","box":[70,190,940,553],"raio":14,"sombra":False,"z":29},
   {"tipo":"texto","t":vd+0.05,"d":r1-vd-0.05,"xy":[40,830],"w":1000,"fonte":"190px Anton","cor":"#ff2d3d","alinha":"center","txt":"MITO.","z":50,"entra":"zoom","css":"text-shadow:10px 10px 0 #000"},
   {"tipo":"video","t":vd,"d":r1-vd,"ms":0,"src":M+P+"_r1.mp4","box":[0,1140,1080,780],"pos":"center 30%","entra":"desliza","z":45}]

# ================= A (indignado): os dois vereditos =================
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
    GIG(a(0),3.85,"UVB",y=1000,tam=560),
    TT(a(0.05),3.8,"“UVB NÃO DÁ CÂNCER”",y=380,fz=112),
    X(a(0.95),2.9,540,440,s=95),
    TT(a(2.3),1.55,"DÁ, SIM.",y=820,fz=240,cor=AMAR,anim=None,entra="zoom"),
    FL(a(3.85)),
    GIG(a(3.85),DA+0.6-3.85,"VITAMINA D",y=1050,tam=380,cont=True,cor="rgba(255,226,122,.30)",ida=False),
    TT(a(3.87),DA+0.6-3.87,"“PROTETOR BLOQUEIA A VITAMINA D”",y=300,fz=104),
    X(a(5.0),DA+0.6-5.0,540,420,s=110),
    TT(a(6.0),DA+0.6-6.0,"NO DIA A DIA,\\nNÃO.",y=760,fz=190,cor=AMAR,anim=None,entra="zoom")]

# ================= B (manso): AULA, uma ideia por cena =================
c+=[FL(tB)]
# S1 sol manda raio invisível: UVB
c+=[FIS(b(0),4.85,[{"k":"pv_sol","xy":[540,860],"s":1.9,"t":0.1}],
        fluxos=[{"de":[540,1240],"para":[540,1640],"curva":0,"cor":VERM,"t":3.4,"d":1.3,"n":6,"rotulo":"UVB","viagem":0.8}],
        pulsos=[{"o":0,"t":1.5},{"o":0,"t":3.7}]),
    GIG(b(0),4.85,"SOL",y=1180,tam=520),
    TT(b(1.3),3.55,"O SOL MANDA UM RAIO INVISÍVEL",y=250,fz=110),
    FL(b(4.85))]
# S2 bate no DNA e deixa um defeitinho
c+=[FIS(b(4.85),4.15,[{"k":"pv_dna","xy":[540,1060],"s":2.3,"t":0.05}],
        fluxos=[{"de":[640,520],"para":[640,900],"curva":0,"cor":VERM,"t":0.3,"d":1.2,"n":5,"rotulo":"UVB","viagem":0.7}],
        pulsos=[{"o":0,"t":1.5},{"o":0,"t":2.9}]),
    GIG(b(4.85),4.15,"DNA",y=1450,tam=480,cont=True,cor="rgba(77,216,255,.30)",ida=False),
    TT(b(4.9),2.3,"BATE NO DNA",y=330,fz=140),
    CIRC(b(7.25),1.75,[(655,1220,75,0)],cor=VERM,lw=16),
    TT(b(7.2),1.8,"DEIXA UM DEFEITINHO",y=330,fz=125,cor=ROSA),
    FL(b(9.0))]
# S3 vermelhidão = alarme
c+=[{"tipo":"fundo","t":b(9.0),"d":3.45,"cor":"rgba(255,60,60,.22)","z":13,"fixo":True},
    FIS(b(9.0),3.45,[{"k":"pv_pele","xy":[540,1060],"s":2.1,"t":0.05,"rotulo":"PELE","rot_y":205}],
        pulsos=[{"o":0,"t":0.9},{"o":0,"t":1.7},{"o":0,"t":2.5}]),
    GIG(b(9.0),3.45,"ALARME",y=1480,tam=380,cont=True,cor="rgba(255,159,180,.40)"),
    TT(b(9.02),3.43,"VERMELHIDÃO = ALARME",y=340,fz=125,cor=ROSA),
    FL(b(12.45))]
# S4 defeito somado, ano após ano -> câncer
c+=[FIS(b(12.45),4.6,[{"k":"pv_dna","xy":[540,1060],"s":2.3,"t":0.05}]),
    CIRC(b(12.6),4.45,[(264, 1178, 48, 0.0), (632, 904, 48, 0.6), (402, 1207, 48, 1.3), (839, 913, 48, 1.9), (540, 1060, 48, 2.4), (172, 925, 48, 2.8), (908, 1195, 48, 3.1)],cor=VERM,lw=14),
    GIG(b(12.45),4.6,"ANO APÓS ANO",y=1460,tam=330,ida=False),
    TT(b(12.5),2.85,"ANO APÓS ANO",y=340,fz=140),
    TT(b(15.25),1.8,"PODE VIRAR CÂNCER",y=330,fz=150,cor=VERM,anim=None,entra="zoom"),
    FL(b(17.05))]
# S5 vitamina D nasce na pele com o mesmo raio
c+=[FIS(b(17.05),4.8,[{"k":"pv_vitd","xy":[540,1150],"s":1.8,"t":0.1}],
        fluxos=[{"de":[540,520],"para":[540,780],"curva":0,"cor":VERM,"t":1.6,"d":2.6,"n":5,"rotulo":"UVB","viagem":0.8}],
        pulsos=[{"o":0,"t":2.6},{"o":0,"t":3.6}]),
    GIG(b(17.05),4.8,"VITAMINA D",y=1480,tam=360,cont=True,cor="rgba(255,226,122,.35)"),
    TT(b(17.07),1.5,"VITAMINA D?",y=330,fz=150,cor=AMAR),
    TT(b(18.57),3.28,"NASCE NA PELE COM O UVB",y=330,fz=118),
    FL(b(21.85))]
# S6 precisa de pouquinho
c+=[FIS(b(21.85),2.95,[{"k":"pv_sol","xy":[540,1250],"s":1.4,"t":0.1}],pulsos=[{"o":0,"t":1.0},{"o":0,"t":2.0}]),
    GIG(b(21.85),2.95,"POUQUINHO",y=1560,tam=330,cont=True,cor="rgba(244,241,232,.30)",ida=False),
    TT(b(21.87),2.93,"PRECISA DE POUQUINHO",y=330,fz=165,cor=AMAR,anim=None,entra="zoom"),
    FL(b(24.8))]
# S7 protetor é peneira, não parede
c+=[FIS(b(24.8),DB+0.6-24.8,[{"k":"pv_peneira","xy":[540,1060],"s":2.3,"t":0.1}],
        fluxos=[{"de":[540,560],"para":[540,950],"curva":0,"cor":VERM,"t":2.7,"d":2.6,"n":10,"rotulo":"UVB","viagem":0.7},
                {"de":[540,1170],"para":[540,1600],"curva":0,"cor":AMAR,"t":3.9,"d":2.2,"n":3,"rotulo":"UM POUCO PASSA","viagem":0.9,"fica":True}],
        pulsos=[{"o":0,"t":3.2},{"o":0,"t":4.2}]),
    GIG(b(24.8),DB+0.6-24.8,"PENEIRA",y=1560,tam=400),
    TT(b(24.85),2.75,"PROTETOR = PENEIRA, NÃO PAREDE",y=270,fz=125,cor=AMAR),
    TT(b(27.6),DB+0.6-27.6,"SEGURA A QUEIMADURA,\\nDEIXA PASSAR UM POUCO",y=270,fz=105,anim=None,entra="zoom"),
    FL(tC)]

# ================= C (neutro): o estudo =================
c+=[{"tipo":"artigo","t":e(0),"d":14.2,"box":[100,300,880,640],"z":34,
     "revista":"British Journal of Dermatology · 2019","titulo":"Protetor bem passado no sol forte: a vitamina D sobe, sem queimar",
     "autores":"Young e col. · ensaio randomizado, férias em Tenerife","rola":0,
     "linhas":[{"txt":"Uma semana de férias, sol fortíssimo.","grifo":e(1.3)},
               {"txt":"Protetor passado do jeito certo.","grifo":e(5.4)},
               {"txt":"Ninguém queimou.","grifo":e(7.97)},
               {"txt":"A vitamina D subiu mesmo assim.","grifo":e(11.1)}],
     "rodape":"doi 10.1111/bjd.17888"},
    GIG(e(0),14.2,"ESTUDO",y=1420,tam=420,cont=True,cor="rgba(244,241,232,.25)"),
    TT(e(7.95),3.1,"NINGUÉM QUEIMOU",y=1080,fz=150,cor=AMAR,anim=None,entra="zoom"),
    {"tipo":"desenho","t":e(8.4),"d":2.6,"formas":[{"k":"check","c":[540,1560],"s":60}],"espessura":18,"cor":"#3ddc84","z":46},
    TT(e(11.05),3.15,"VITAMINA D SUBIU",y=1080,fz=150,cor=AMAR,anim=None,entra="zoom"),
    {"tipo":"desenho","t":e(11.4),"d":2.8,"formas":[{"k":"seta","de":[540,1660],"para":[540,1470],"curva":0}],"espessura":18,"cor":"#3ddc84","z":46},
    F(e(0),14.2,"Young e col., Br J Dermatol 2019 · doi 10.1111/bjd.17888"),
    FL(e(14.2)),
    GIG(e(14.2),c1-e(14.2),"AUSTRÁLIA",y=1450,tam=380,cont=True,cor="rgba(255,226,122,.30)",ida=False),
    TT(e(14.25),3.6,"AUSTRÁLIA: PROTETOR TODO DIA",y=420,fz=118),
    {"tipo":"numero","t":e(17.9),"d":round(c1-e(17.9),2),"xy":[0,560],"valor":39,"pre":"-","suf":"%","rotulo":"em 4,5 anos","tam":330,"cor":AMAR,"sombra":"#0e1a14","cor_rotulo":GIZ,"z":44},
    TT(e(17.95),round(c1-e(17.95),2),"MENOS TUMORES DE UM TIPO DE CÂNCER DE PELE",y=1200,fz=105,cor=GIZ,anim=None,entra="zoom"),
    F(e(14.2),round(c1-e(14.2),2),"Green e col., Lancet 1999 · 1.621 moradores, 4,5 anos · doi 10.1016/S0140-6736(98)12168-2")]

# ================= CTA (banco cta6) + fecho (D, alegre) =================
c+=[{"tipo":"glitch","t":c1-0.05,"d":0.25},
    {"tipo":"video","t":c1,"d":4.12,"ms":0,"src":M+P+"_cta6.mp4","box":[0,0,1080,1920],"pos":"center 30%","zoom":[[c1,1.0,0.01],[c1+2.6,1.1,0.3]],"z":40},
    {"tipo":"barra","t":c1+0.2,"d":3.87,"y":215,"txt":"AULA VALEU? SEGUE + CURTE","cor":"#c6ff3d","cor_txt":"#0b1512"},
    {"tipo":"glitch","t":c2-0.05,"d":0.25},FL(c2),
    GIG(f(0),dur-c2,"PROTETOR",y=1480,tam=400),
    TT(f(0.05),4.5,"PROTETOR NO QUE FICA DE FORA, TODO DIA",y=330,fz=112),
    TT(f(4.55),2.25,"VITAMINA D BAIXA?",y=330,fz=135,cor=ROSA),
    TT(f(6.8),2.25,"EXAME DE SANGUE",y=330,fz=150,cor=AMAR,anim=None,entra="zoom"),
    TT(f(9.05),round(dur-f(9.05),2),"CONVERSA COM SEU MÉDICO",y=330,fz=130),
    {"tipo":"carimbo","t":f(1.4),"d":round(dur-f(1.4),2),"xy":[110,900],"txt":"PENEIRA, NÃO PAREDE","tam":100,"rot":-8,"z":60,"cor":"#ff2d3d","blend":"normal","css":"background:rgba(255,255,255,.9)"},
    F(f(0),round(dur-f(0),2),"Young e col., Br J Dermatol 2019 · Green e col., Lancet 1999")]

voz=[{"src":M+P+"_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+P+"_viral.words.json"},
     {"src":M+P+"_r1.mp4","t":vd,"ms":0,"d":round(r1-vd,2),"palavras":M+P+"_r1.words.json"},
     {"src":M+P+"_a_voz.wav","t":tA,"ms":0,"d":DA,"palavras":M+P+"_a_voz.words.json"},
     {"src":M+P+"_b_voz.wav","t":tB,"ms":0,"d":DB,"palavras":M+P+"_b_voz.words.json"},
     {"src":M+P+"_c_voz.wav","t":tC,"ms":0,"d":DC,"palavras":M+P+"_c_voz.words.json"},
     {"src":M+P+"_cta6.mp4","t":c1,"ms":0,"d":4.12,"palavras":M+P+"_cta6.words.json"},
     {"src":M+P+"_d_voz.wav","t":c2,"ms":0,"d":DD,"palavras":M+P+"_d_voz.words.json"}]
musica=[{"src":"m_investiga","t":r1,"ms":0,"d":round(c1-r1,2),"gain":0.30,"fade":0.8},
        {"src":"m_emocao","t":c2,"ms":0,"d":round(dur-c2,2),"gain":0.26,"fade":0.8}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.1,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"boom","t":vd+0.05,"gain":0.5,"pico":0.3,"d":1.2},
 {"src":"glitch","t":r1-0.05,"gain":0.5},{"src":"whoosh","t":r1,"gain":0.5,"pico":0.45},
 {"src":"scratch","t":a(0.95),"gain":0.35},{"src":"boom","t":a(2.3),"gain":0.5,"pico":0.3,"d":1.2},
 {"src":"whoosh2","t":a(3.85),"gain":0.4},{"src":"scratch","t":a(5.0),"gain":0.35},{"src":"boom","t":a(6.0),"gain":0.5,"pico":0.3,"d":1.2},
 # aula
 {"src":"whoosh","t":tB,"gain":0.45,"pico":0.45},{"src":"boing","t":b(0.15),"gain":0.3},{"src":"riser","t":b(3.0),"gain":0.22,"d":1.5},
 {"src":"whoosh2","t":b(4.85),"gain":0.35},{"src":"boing","t":b(4.9),"gain":0.3},{"src":"scratch","t":b(7.25),"gain":0.3},
 {"src":"whoosh2","t":b(9.0),"gain":0.35},{"src":"glitch","t":b(9.9),"gain":0.3},{"src":"glitch","t":b(10.7),"gain":0.25},
 {"src":"whoosh2","t":b(12.45),"gain":0.35},{"src":"boing","t":b(13.1),"gain":0.22},{"src":"boing","t":b(14.4),"gain":0.22},{"src":"boom","t":b(15.3),"gain":0.5,"pico":0.3,"d":1.2},
 {"src":"whoosh","t":b(17.05),"gain":0.4,"pico":0.45},{"src":"boing","t":b(17.15),"gain":0.3},
 {"src":"whoosh2","t":b(21.85),"gain":0.35},{"src":"boing","t":b(22.0),"gain":0.3},
 {"src":"whoosh","t":b(24.8),"gain":0.4,"pico":0.45},{"src":"boing","t":b(24.9),"gain":0.3},{"src":"riser","t":b(27.0),"gain":0.2,"d":1.5},
 # estudo
 {"src":"whoosh","t":tC,"gain":0.45,"pico":0.45},{"src":"pagina","t":e(0.1),"gain":0.5},{"src":"boing","t":e(8.4),"gain":0.35},{"src":"boing","t":e(11.4),"gain":0.35},
 {"src":"whoosh2","t":e(14.2),"gain":0.4},{"src":"riser","t":e(16.4),"gain":0.25,"d":1.5},{"src":"boom","t":e(17.9),"gain":0.6,"pico":0.3,"d":1.5},
 # CTA e fecho
 {"src":"glitch","t":c1-0.05,"gain":0.5},{"src":"notif","t":c1+0.2,"gain":0.4},{"src":"glitch","t":c2-0.05,"gain":0.5},
 {"src":"boom","t":f(1.4),"gain":0.6,"pico":0.3,"d":1.5},{"src":"whoosh2","t":f(4.55),"gain":0.35},{"src":"whoosh2","t":f(6.8),"gain":0.35},{"src":"whoosh2","t":f(9.05),"gain":0.35}]
for L in c:
    if L.get("t",0)>=vd-0.06: L["fixo"]=True
salvar("react_l2_protetor",dur,214,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1360],[vd,r1,1010],[r1,c1,1720],[c2,dur,1720]]})
import json
p=json.load(open('planos/react_l2_protetor.json')); p['audio']['musica']=musica
json.dump(p,open('planos/react_l2_protetor.json','w'),ensure_ascii=False,indent=1)
print("ok dur",dur,"r1",r1,"tB",tB,"tC",tC,"c1",c1,"c2",c2)
