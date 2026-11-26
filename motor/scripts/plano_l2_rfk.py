import sys, json, subprocess; sys.path.insert(0,'scripts')
from mk import *
# Lote 2 (14/11): react novo "verme no cérebro" (RFK Jr., trecho da CNN no TikTok do @thedailyshow), Papo de Médico.
# Edição da aula: desenhos grandes do caminho (uma ideia por cena, sem b-roll) + MAPEAMENTO (mapa em papel antigo,
# pinos onde o verme é comum, câmera aproximando). Pele: notícia.
# Fala do corte: "um verme que entrou no meu cérebro, comeu um pedaço dele e depois morreu" -> MEIA VERDADE.
# Depois: python3 scripts/entrada.py react_l2_rfk assets/midia/rk_ent.mp4 assets/midia/rk_ent.mp4.words.json 2.07 \
#   "VERME 'COMEU' O CÉREBRO?" "o que a ciência diz sobre verme no cérebro" && python3 scripts/pele.py react_l2_rfk noticia
PID='react_l2_rfk'; P='rk'
vd=10.35                     # viral 15,28-25,63 (corta antes do apresentador voltar) (dublagem Murilo, original a 0,16)
r1=round(vd+7.43,2)          # rosto r1 "Meia verdade, tá? Verme no cérebro existe. Mas ele não come o cérebro."
AU=33.95                     # rk_aula_voz (manso) até "convulsão." + folga
T3=round(r1+AU,2)            # mapa + estudo + prevenção (rk_est_voz 0 -> 25,75)
N1=25.75
c1=round(T3+N1,2)            # CTA 6cd9
c2=round(c1+4.12,2)          # fecho (rk_est_voz 26,6 -> fim)
dur=round(c2+(30.53-26.6)+0.6,2)
a=lambda v: round(r1+v,2)    # tempo da aula
e=lambda v: round(T3+v,2)    # tempo do estudo
SOMBRA="text-shadow:6px 6px 0 #000,0 0 18px rgba(0,0,0,.8)"
def TT(t,d,txt,y=250,f="110px Anton",cor="#ffffff",**k):
    return T(t,d,txt,y=y,f=f,cor=cor,css=SOMBRA,vel=0.09,**k)
def FS(t,d,orgaos,**k):
    L={"tipo":"fisio","t":round(t,2),"d":round(d,2),"z":30,"orgaos":orgaos}; L.update(k); return L
def X(t,d,cx,cy,s=150):
    return {"tipo":"desenho","t":round(t,2),"d":round(d,2),"formas":[{"k":"x","c":[cx,cy],"s":s}],"espessura":20,"cor":"#ff2d3d","z":45}
FL=lambda t,mx=0.5: {"tipo":"flash","t":round(t,2),"d":0.2,"max":mx}

c=abertura(P,vd,"via @thedailyshow · reportagem CNN","center 20%","Mito ou verdade? 👇","Verme pode comer o cérebro?",
  [{"tipo":"numero","t":4.3,"d":vd-4.35,"xy":[0,1150],"valor":885,"suf":" MIL VIEWS","tam":120}])
for L in c:
    if L.get("tipo")=="pergunta": L["botoes"]=["COME","NÃO COME"]; L["escolha"]=1
# r1: rosto embaixo, foto do viral em cima com a resposta grande
c+=[{"tipo":"video","t":vd,"d":round(r1-vd,2),"ms":0,"src":M+"rk_r1.mp4","box":[0,1140,1080,780],"pos":"center 30%","entra":"desliza","z":45},
    {"tipo":"texto","t":vd+0.05,"d":2.15,"xy":[40,520],"w":1000,"fonte":"150px Anton","cor":"#f2c230","alinha":"center","txt":"MEIA VERDADE","z":50,"entra":"zoom","css":"text-shadow:10px 10px 0 #000"},
    TT(vd+2.2,2.6,"VERME NO CÉREBRO EXISTE ✓",y=470,f="120px Anton",cor="#3ddc84"),
    TT(vd+4.8,round(r1-vd-4.8,2),"MAS NÃO COME O CÉREBRO",y=470,f="125px Anton",cor="#ff5a5f")]

# ================= AULA (desenhos grandes, uma ideia por cena) =================
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},FL(r1,0.6)]
# S0 0-3,65: do caso dele não falo; falo do verme
c+=[TT(a(0.05),3.6,"FALO DO VERME, NÃO DO CASO DELE",f="115px Anton",cor="#f2c230"),
    FS(a(1.9),1.75,[{"k":"solitaria","xy":[540,1000],"s":1.9,"t":0.05}])]
# S1 3,65-6,6: a solitária do porco vive no intestino
c+=[FL(a(3.65)),
    TT(a(3.67),2.93,"SOLITÁRIA DO PORCO",f="120px Anton"),
    FS(a(3.65),2.95,[{"k":"intestino","xy":[540,1020],"s":1.75,"t":0.05,"rotulo":"INTESTINO","rot_y":225},
                     {"k":"solitaria","xy":[540,990],"s":0.75,"t":0.85}],pulsos=[{"o":1,"t":1.6}])]
# S2 6,6-9,05: solta ovinhos nas fezes
c+=[FL(a(6.6)),
    TT(a(6.62),2.43,"SOLTA OVINHOS NAS FEZES",f="115px Anton",cor="#f2c230"),
    FS(a(6.6),2.45,[{"k":"ovos_verme","xy":[540,1020],"s":1.8,"t":0.55}],pulsos=[{"o":0,"t":1.4}])]
# S3 9,05-13,45: mão ou verdura mal lavada leva o ovo para a boca
c+=[FL(a(9.05)),
    TT(a(9.07),4.38,"MÃO OU VERDURA MAL LAVADA → BOCA",f="110px Anton"),
    FS(a(9.05),4.4,[{"k":"mao_suja","xy":[290,1330],"s":1.05,"t":0.1},
                    {"k":"alface","xy":[800,1330],"s":1.0,"t":0.9},
                    {"k":"boca_aberta","xy":[540,720],"s":1.1,"t":3.2}],
       fluxos=[{"de":[300,1130],"para":[470,790],"curva":-40,"cor":"#e0a94e","t":2.1,"d":1.9,"n":5,"r":14,"viagem":0.9},
               {"de":[790,1150],"para":[610,790],"curva":40,"cor":"#e0a94e","t":2.4,"d":1.7,"n":5,"r":14,"viagem":0.9}],
       pulsos=[{"o":2,"t":3.6}])]
# S4 13,45-16,95: a larva cai no sangue e sobe para o cérebro
c+=[FL(a(13.45)),
    TT(a(13.47),3.48,"CAI NO SANGUE E SOBE",f="120px Anton",cor="#ff5a5f"),
    FS(a(13.45),3.5,[{"k":"intestino","xy":[540,1430],"s":0.8,"t":0.05,"rotulo":"INTESTINO","rot_y":215},
                     {"k":"cerebro","xy":[540,700],"s":1.0,"t":0.3,"rotulo":"CÉREBRO","rot_y":200}],
       fluxos=[{"de":[540,1290],"para":[560,820],"curva":-180,"cor":"#ff2d3d","t":0.65,"d":2.6,"n":7,"r":14,"viagem":1.0}],
       pulsos=[{"o":1,"t":2.6}])]
# S5 16,95-20,6: vira uma bolinha de água do tamanho de uma ervilha
c+=[FL(a(16.95)),
    TT(a(16.97),3.63,"BOLINHA DE ÁGUA DO TAMANHO DE ERVILHA",f="110px Anton",cor="#4dd8ff"),
    FS(a(16.95),3.65,[{"k":"cisto_ervilha","xy":[540,950],"s":1.55,"t":0.25,"rotulo":"BOLINHA DE ÁGUA","rot_y":215}],pulsos=[{"o":0,"t":1.0}]),
    FS(a(18.72),1.88,[{"k":"ervilha","xy":[540,1510],"s":0.75,"t":0.05,"rotulo":"ERVILHA","rot_y":180}])]
# S6 20,6-23,15: ela não come nada
c+=[FL(a(20.6)),
    TT(a(20.62),2.53,"ELA NÃO COME NADA",f="135px Anton"),
    FS(a(20.6),2.55,[{"k":"boca_aberta","xy":[540,1050],"s":1.5,"t":0.05}]),
    X(a(21.35),1.8,540,1050,230),
    {"tipo":"carimbo","t":a(21.6),"d":1.55,"xy":[150,1420],"txt":"NÃO COME","tam":150,"rot":-9,"z":60,"cor":"#ff2d3d","blend":"normal","css":"background:rgba(255,255,255,.92)"}]
# S7 23,15-26,55: quando morre, é igual farpa no dedo
c+=[FL(a(23.15)),
    TT(a(23.17),3.38,"QUANDO MORRE: IGUAL FARPA NO DEDO",f="120px Anton",cor="#f2c230"),
    FS(a(23.9),2.65,[{"k":"dedo_farpa","xy":[540,1080],"s":1.75,"t":0.05}],pulsos=[{"o":0,"t":1.2}]),
    {"tipo":"gigante","t":a(24.2),"d":2.3,"txt":"FARPA","y":1650,"tam":260,"cor":"rgba(255,255,255,.12)","x":[1000,-1300],"z":20}]
# S8 26,55-30,45: o que incha é a defesa do corpo em volta
c+=[FL(a(26.55)),
    TT(a(26.57),3.88,"O QUE INCHA É A DEFESA DO CORPO",f="110px Anton",cor="#ff5a5f"),
    FS(a(26.55),3.9,[{"k":"cisto_inflamado","xy":[540,1060],"s":1.75,"t":0.1}],
       pulsos=[{"o":0,"t":1.2},{"o":0,"t":2.0},{"o":0,"t":2.8},{"o":0,"t":3.5}])]
# S9 30,45-33,95: esse inchaço pode dar convulsão
c+=[FL(a(30.45)),
    TT(a(30.47),3.48,"PODE DAR CONVULSÃO",f="135px Anton",cor="#f2c230"),
    FS(a(30.45),3.5,[{"k":"cerebro","xy":[540,1060],"s":1.6,"t":0.05},
                     {"k":"raio","xy":[790,800],"s":0.8,"t":1.4}],
       pulsos=[{"o":0,"t":1.5},{"o":0,"t":2.1},{"o":1,"t":1.9},{"o":0,"t":2.7}])]
c+=[{"tipo":"glitch","t":T3-0.05,"d":0.25},FL(T3)]

# ================= MAPA: onde o verme é comum (rk_est_voz 0-12,2) =================
PIN=dict(fs=34,stroke="#fff",sw=7,cor_txt="#1b1b1b")
c+=[{"tipo":"mapa","t":T3,"d":12.25,"tema":"papel","area":[0,380,1080,1300],
     "camera":[[T3,8,-15,0.52,0],[e(0.85),-8,-68,1.45,1.3],[e(3.75),12,55,0.85,1.3],[e(6.45),-14,-50,2.6,1.6],[e(9.1),5,-20,0.62,2.6]],
     "pinos":[dict(ll=[19.4,-99.1],t=e(1.0),txt="MÉXICO",**PIN),dict(ll=[-12.0,-77.0],t=e(1.35),txt="PERU",**PIN),
              dict(ll=[-16.7,-49.3],t=e(2.9),txt="BRASIL",cor="#b3121f",**PIN),
              dict(ll=[9.1,8.7],t=e(4.1),txt="ÁFRICA",**PIN),dict(ll=[-6.4,34.9],t=e(4.35),txt="",**PIN),
              dict(ll=[21.0,78.0],t=e(5.15),txt="ÁSIA",**PIN),dict(ll=[23.0,105.0],t=e(5.35),txt="",**PIN)],
     "z":20,"fixo":True},
    TT(e(0.05),5.8,"ONDE ESSE VERME É COMUM",y=210,f="105px Anton"),
    TT(e(6.45),2.5,"NÃO É RARO",y=210,f="160px Anton",cor="#ffd400",anim=None,entra="zoom"),
    TT(e(9.05),3.15,"REVISÃO DE ESTUDOS",y=210,f="125px Anton"),
    F(e(9.05),3.15,"Ndimubanzi e col., PLoS Negl Trop Dis 2010 (revisão sistemática)")]
c[-1]["xy"]=[40,1860]
# número (12,25-18,0)
c+=[FL(e(12.25)),
    TT(e(12.27),5.73,"DE CADA 100 COM EPILEPSIA",y=260,f="110px Anton"),
    {"tipo":"numero","t":e(14.72),"d":3.28,"xy":[0,560],"valor":29,"suf":" EM 100","tam":250,"cor":"#ffd400","z":44},
    TT(e(14.95),3.05,"TINHAM AS BOLINHAS",y=1000,f="120px Anton",cor="#ffffff",anim=None,entra="zoom"),
    FS(e(14.72),3.28,[{"k":"cisto_ervilha","xy":[540,1440],"s":0.8,"t":0.6}]),
    F(e(12.27),5.73,"Ndimubanzi e col., PLoS Negl Trop Dis 2010 · regiões onde o verme é comum")]
c[-1]["xy"]=[40,1860]
# prevenção (18,0-25,75)
c+=[FL(e(18.0)),
    TT(e(18.02),2.6,"PARA SE PROTEGER",y=260,f="130px Anton",cor="#3ddc84"),
    {"tipo":"checklist","t":e(20.0),"d":round(N1-20.0,2),"box":[90,520,900,700],"titulo":"Para a família toda:","entra":"cai",
     "itens":[{"txt":"lavar a mão","t":e(20.5),"marca":e(21.1)},{"txt":"lavar bem a verdura","t":e(21.6),"marca":e(22.6)},
              {"txt":"carne de porco bem passada","t":e(23.5),"marca":e(24.9)}],"z":40}]

# ================= CTA (6cd9) + fecho =================
c+=[{"tipo":"glitch","t":c1-0.05,"d":0.25},
    {"tipo":"video","t":c1,"d":4.12,"ms":0,"src":M+"rk_cta.mp4","box":[0,0,1080,1920],"pos":"center 30%","zoom":[[c1,1.0,0.01],[c1+2.6,1.1,0.3]],"z":40},
    {"tipo":"barra","t":c1+0.2,"d":3.87,"y":215,"txt":"AULA VALEU? SEGUE + CURTE","cor":"#c6ff3d","cor_txt":"#0b1512"}]
c+=B(P+"_viral_blur.mp4",c2,dur-c2,3.0)
c+=[FL(c2),
    T(c2+0.03,2.4,"1ª CONVULSÃO NA VIDA?",y=420,f="135px Anton"),
    T(c2+2.45,round(dur-c2-2.45,2),"PROCURA O MÉDICO",y=420,f="145px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
    {"tipo":"carimbo","t":c2+0.6,"d":round(dur-c2-0.6,2),"xy":[70,820],"txt":"NÃO COME O CÉREBRO","tam":105,"rot":-6,"z":60,"blend":"normal","css":"background:rgba(255,255,255,.92)"},
    F(c2,dur-c2,"Ndimubanzi e col., PLoS Negl Trop Dis 2010 · doi 10.1371/journal.pntd.0000870")]

CTA=M+"rk_cta.mp4"
voz=[{"src":M+"rk_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"rk_viral.words.json","gain":0.16},
     {"src":M+"rk_dub_voz.wav","t":0.2,"ms":0,"d":9.84,"gain":1.0},
     {"src":M+"rk_r1.mp4","t":vd,"ms":0,"d":round(r1-vd,2),"palavras":M+"rk_r1.words.json"},
     {"src":M+"rk_aula_voz.wav","t":r1,"ms":0,"d":33.46,"palavras":M+"rk_aula_voz.words.json"},
     {"src":M+"rk_est_voz.wav","t":T3,"ms":0,"d":N1,"palavras":M+"rk_est_voz.words.json"},
     {"src":CTA,"t":c1,"ms":0,"d":4.12,"palavras":M+"rk_cta.words.json"},
     {"src":M+"rk_est_voz.wav","t":c2,"ms":26.6,"d":round(30.53-26.6,2),"palavras":M+"rk_est_voz.words.json"}]
musica=[{"src":"m_investiga","t":vd,"ms":0,"d":round(c1-vd,2),"gain":0.3,"fade":0.8},
        {"src":"m_noticia","t":c2,"ms":0,"d":round(dur-c2,2),"gain":0.22,"fade":0.6}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.3,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"boom","t":vd+0.05,"gain":0.5,"pico":0.3,"d":1.2},{"src":"boing","t":vd+2.2,"gain":0.3},{"src":"scratch","t":vd+4.85,"gain":0.3},
 {"src":"glitch","t":r1-0.05,"gain":0.5},{"src":"whoosh","t":r1,"gain":0.5,"pico":0.45},{"src":"boing","t":a(1.95),"gain":0.3},
 {"src":"whoosh2","t":a(3.65),"gain":0.35},{"src":"boing","t":a(4.5),"gain":0.3},
 {"src":"whoosh2","t":a(6.6),"gain":0.35},{"src":"boing","t":a(7.15),"gain":0.3},
 {"src":"whoosh2","t":a(9.05),"gain":0.35},{"src":"boing","t":a(9.15),"gain":0.25},{"src":"boing","t":a(9.95),"gain":0.25},{"src":"boing","t":a(12.25),"gain":0.3},
 {"src":"whoosh2","t":a(13.45),"gain":0.35},{"src":"riser","t":a(14.1),"gain":0.22,"d":2.5},
 {"src":"whoosh2","t":a(16.95),"gain":0.35},{"src":"boing","t":a(17.2),"gain":0.3},{"src":"boing","t":a(18.77),"gain":0.3},
 {"src":"whoosh2","t":a(20.6),"gain":0.35},{"src":"scratch","t":a(21.35),"gain":0.3},{"src":"boom","t":a(21.6),"gain":0.55,"pico":0.3,"d":1.2},
 {"src":"whoosh2","t":a(23.15),"gain":0.35},{"src":"boing","t":a(24.2),"gain":0.3},
 {"src":"whoosh2","t":a(26.55),"gain":0.35},{"src":"riser","t":a(27.2),"gain":0.2,"d":2.8},
 {"src":"whoosh2","t":a(30.45),"gain":0.35},{"src":"glitch","t":a(31.9),"gain":0.35},
 {"src":"glitch","t":T3-0.05,"gain":0.5},{"src":"papel","t":T3,"gain":0.45},{"src":"whoosh2","t":e(0.85),"gain":0.3},
 {"src":"boing","t":e(1.0),"gain":0.25},{"src":"boing","t":e(1.35),"gain":0.25},{"src":"boing","t":e(2.9),"gain":0.35},
 {"src":"whoosh2","t":e(3.75),"gain":0.3},{"src":"boing","t":e(4.1),"gain":0.25},{"src":"boing","t":e(5.15),"gain":0.25},
 {"src":"whoosh","t":e(6.45),"gain":0.4,"pico":0.45},{"src":"pagina","t":e(9.05),"gain":0.4},
 {"src":"whoosh2","t":e(12.25),"gain":0.35},{"src":"boom","t":e(14.72),"gain":0.6,"pico":0.3,"d":1.5},
 {"src":"whoosh2","t":e(18.0),"gain":0.35},{"src":"papel","t":e(20.0),"gain":0.45},{"src":"boing","t":e(21.1),"gain":0.3},{"src":"boing","t":e(22.6),"gain":0.3},{"src":"boing","t":e(24.9),"gain":0.3},
 {"src":"glitch","t":c1-0.05,"gain":0.5},{"src":"notif","t":c1+0.2,"gain":0.4},{"src":"glitch","t":c2-0.05,"gain":0.5},
 {"src":"boom","t":c2+0.6,"gain":0.55,"pico":0.3,"d":1.5},{"src":"whoosh2","t":c2+2.45,"gain":0.4}]
for L in c:
    if vd<=L.get("t",0)<c1-0.06: L["fixo"]=True
salvar(PID,dur,141,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000],[r1,c1,1760]]})
p=json.load(open(f'planos/{PID}.json')); p['audio']['musica']=musica
json.dump(p,open(f'planos/{PID}.json','w'),ensure_ascii=False,indent=1)
print("ok dur",dur,"r1",r1,"T3",T3,"c1",c1,"c2",c2)
if '--sem-pos' not in sys.argv:
    subprocess.run(["python3","scripts/entrada.py",PID,M+"rk_ent.mp4",M+"rk_ent.mp4.words.json","2.07",
                    "VERME 'COMEU' O CÉREBRO?","o que a ciência diz sobre verme no cérebro"],check=True)
    subprocess.run(["python3","scripts/pele.py",PID,"noticia"],check=True)
