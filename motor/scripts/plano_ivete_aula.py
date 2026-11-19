import sys; sys.path.insert(0,'scripts')
from mk import *
# Ivete remake com aula (14/11): roteiro /mnt/project-files/reacts/remakes/ivete.md
# Mantém o vídeo atual (react_ivete) intacto. Entra aula de leigo "por que um rosto afina" (almofadinhas de gordura)
# depois de "ninguém sabe o tratamento de ninguém por foto", antes do estudo do MIT.
# Corta de iv_voz.wav: 22,15-25,90 ("E quem mais espalhou...") e 37,20-40,05 ("E quem usa, mantém treino de força
# e proteína", decisão da thread principal: perfil Caneta nunca orienta uso).
# Depois: python3 scripts/entrada.py react_ivete_aula assets/midia/ca_entA.mp4 assets/midia/ca_entA.mp4.words.json 2.1 \
#   'IRRECONHECÍVEL POR CAUSA DA CANETA?' 'a fofoca passou de 7 milhões de views' 'Fofoca do Dia'
#   && python3 scripts/pele.py react_ivete_aula noticia
P='iv'; vd=8.85; r1=11.55
A=15.23                          # iv_aula_voz.wav (1,3x)
n=lambda v: round(v+8.25,2)      # iv_voz 3,30-6,05
L0=14.50                         # início da aula
AU=15.73                         # aula + folga depois do "tá?"
T3=round(L0+AU,2)
m=lambda v: round(v+(T3-6.05),2) # iv_voz 6,05-22,15
r2=m(22.15)
k=lambda v: round(v+(r2-25.90),2)# iv_voz 25,90-37,20
g=k(28.6); n2=k(31.2); cut1=k(37.2)
f=lambda v: round(v+(cut1-40.05),2)  # iv_voz 40,05-fim
dur=round(f(42.42)+0.45,2)
a=lambda v: round(L0+v,2)        # tempo relativo à aula
SOMBRA="text-shadow:6px 6px 0 #000,0 0 18px rgba(0,0,0,.8)"
def BR(src,t,d,ms=0.3):
    z=[[t,1.04,0.01],[round(t+d,2),1.14,round(d,2)]]
    return [{"tipo":"video","t":round(t,2),"d":round(d,2),"ms":ms,"src":M+src,"box":[0,0,1080,1920],"pos":"center","respira":False,"z":10,"zoom":z},
            {"tipo":"fundo","t":round(t,2),"d":round(d,2),"cor":"rgba(6,14,11,.6)","z":11}]
def TT(t,d,txt,y=250,f="104px Anton",cor="#ffffff",**kw):
    return T(t,d,txt,y=y,f=f,cor=cor,css=SOMBRA,vel=0.09,**kw)

c=abertura(P,vd,"via @natal.noticias","center 34%","Mito ou verdade? 👇","Dá para saber por foto se alguém usou caneta?",
  [{"tipo":"numero","t":4.3,"d":vd-4.35,"xy":[0,1150],"valor":7.4,"dec":1,"suf":" MI VIEWS","tam":120}])
c+=[rosto_r1(P,vd,r1-vd,0)]
c+=B(P+"_viral_blur.mp4",r1,L0-r1,10.0)
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 T(n(3.5),n(6.12)-n(3.5),"NINGUÉM SABE POR FOTO",f="145px Anton"),
 {"tipo":"gigante","t":n(5.0),"d":0.6,"txt":"POR FOTO?","y":1060,"tam":250,"cor":"#c6ff3d","x":[1000,-2200],"z":42}]

# ================= AULA: por que um rosto afina =================
c+=[{"tipo":"glitch","t":L0-0.05,"d":0.25},{"tipo":"flash","t":L0,"d":0.2,"max":0.6}]
# cena A: rosto + almofadinhas (homem no espelho)
c+=BR("iv_br_50756.mp4",L0,4.30,0.3)
# cena B: perdeu peso (fita métrica na barriga)
c+=BR("iv_br_46085.mp4",a(4.30),4.25,2.0)
c+=[{"tipo":"fisio","t":L0,"d":7.55,"z":30,
     "orgaos":[{"k":"rosto","xy":[540,900],"s":1.5,"t":0.15},
               {"k":"coxim","xy":[420,960],"s":1.5,"t":2.75},
               {"k":"coxim","xy":[660,960],"s":1.5,"t":2.95}],
     "pulsos":[{"o":1,"t":3.45},{"o":2,"t":3.65},{"o":1,"t":4.65},{"o":2,"t":4.65}],
     "encolhe":[{"o":1,"t":6.75,"para":.7,"d":.7},{"o":2,"t":6.75,"para":.7,"d":.7}],
     "fluxos":[{"de":[420,990],"para":[330,1330],"curva":-30,"cor":"#f6d26b","t":6.75,"d":0.75,"n":4,"r":10,"viagem":0.6},
               {"de":[660,990],"para":[750,1330],"curva":30,"cor":"#f6d26b","t":6.75,"d":0.75,"n":4,"r":10,"viagem":0.6}]},
    {"tipo":"flash","t":a(7.55),"d":0.15,"max":0.5},
    {"tipo":"fisio","t":a(7.55),"d":1.0,"z":30,"orgaos":[{"k":"rosto_fino","xy":[540,900],"s":1.5,"t":0.0}]},
    TT(a(0.10),1.85,"POR QUE AFINA?",f="120px Anton"),
    TT(a(1.95),2.35,"ALMOFADINHAS DE GORDURA",cor="#f6d26b"),
    TT(a(4.30),2.30,"PERDEU PESO RÁPIDO"),
    TT(a(6.60),1.95,"MURCHAM. PELE SOBRA.",cor="#f6d26b"),
    {"tipo":"flash","t":a(8.55),"d":0.2,"max":0.5}]
# cena C: capa de almofada velha (mulher abraçando almofada)
c+=BR("iv_br_4513.mp4",a(8.55),1.83,2.0)
c+=[{"tipo":"fisio","t":a(8.55),"d":1.83,"z":30,
     "orgaos":[{"k":"almofada","xy":[300,930],"s":1.15,"t":0.05,"rotulo":"NOVA"},
               {"k":"almofada_murcha","xy":[780,950],"s":1.15,"t":0.55,"rotulo":"VELHA"}]},
    TT(a(8.55),1.83,"IGUAL ALMOFADA VELHA"),
    {"tipo":"flash","t":a(10.38),"d":0.2,"max":0.5}]
# cena D: vai músculo junto (treino)
c+=BR("iv_br_52112.mp4",a(10.38),2.72,1.0)
c+=[{"tipo":"fisio","t":a(10.38),"d":2.72,"z":30,
     "orgaos":[{"k":"musculo","xy":[540,1000],"s":1.1,"t":0.05,"rotulo":"MÚSCULO","rot_y":175}],
     "encolhe":[{"o":0,"t":1.3,"para":.72,"d":1.1}]},
    TT(a(10.38),2.72,"SEM MÚSCULO:\\nPELE E OSSO",cor="#ff5a5f",anim=None,entra="zoom"),
    {"tipo":"flash","t":a(13.10),"d":0.2,"max":0.5}]
# cena E: foto não conta o motivo (lente de fotógrafo)
c+=BR("iv_br_50635.mp4",a(13.10),AU-13.10,1.0)
c+=[{"tipo":"desenho","t":a(13.12),"d":round(AU-13.12,2),"formas":[{"k":"caixa","b":[250,580,580,720]}],"espessura":14,"cor":"#ffffff","z":29},
    {"tipo":"fisio","t":a(13.10),"d":round(AU-13.10,2),"z":30,"orgaos":[{"k":"rosto_fino","xy":[540,940],"s":1.25,"t":0.1}]},
    {"tipo":"texto","t":a(14.0),"d":round(AU-14.0,2),"xy":[790,470],"w":240,"fonte":"220px Anton","cor":"#f6d26b","alinha":"center","txt":"?","z":45,"entra":"zoom","css":SOMBRA},
    TT(a(13.10),round(AU-13.10,2),"FOTO NÃO CONTA\\nO MOTIVO",cor="#f2c230",anim=None,entra="zoom")]
c+=[{"tipo":"glitch","t":T3-0.05,"d":0.25},{"tipo":"flash","t":T3,"d":0.2,"max":0.5}]

# ================= estudo do MIT (iv_voz 6,05-22,15) =================
c+=B(P+"_viral_blur.mp4",T3,r2-T3,13.0)+B(P+"_viral_blur.mp4",g,dur-g,35.0)
c+=[T(m(6.15),m(9.7)-m(6.15),"FOFOCA CORRE MAIS QUE A VERDADE",f="125px Anton",cor="#f2c230",css="text-shadow:8px 8px 0 #000"),
 {"tipo":"flash","t":m(9.7),"d":0.2,"max":0.5},
 T(m(9.72),m(14.36)-m(9.72),"ESTUDO DO MIT: 126 MIL NOTÍCIAS",f="140px Anton",cor="#ffffff",vel=0.12),
 {"tipo":"flash","t":m(14.36),"d":0.2,"max":0.5},
 {"tipo":"numero","t":m(14.38),"d":m(17.82)-m(14.38),"xy":[0,420],"valor":70,"suf":"%","rotulo":"no compartilhamento","tam":300,"cor":"#ff2d3d","sombra":"#5a0d10","z":44},
 T(m(14.6),m(17.82)-m(14.6),"A MENTIRA É MAIS REPASSADA",y=960,f="110px Anton",cor="#ff2d3d",anim=None,entra="zoom",css="text-shadow:6px 6px 0 #000"),
 {"tipo":"flash","t":m(17.82),"d":0.2,"max":0.5},
 {"tipo":"numero","t":m(17.84),"d":r2-m(17.84),"xy":[0,420],"valor":6,"suf":"x","rotulo":"para alcançar 1.500 pessoas","tam":300,"cor":"#f2c230","z":44},
 T(m(18.1),r2-m(18.1),"A VERDADE DEMORA 6X MAIS",y=960,f="110px Anton",cor="#f2c230",anim=None,entra="zoom",css="text-shadow:6px 6px 0 #000"),
 F(m(9.72),r2-m(9.72),"Vosoughi, Roy e Aral (MIT), Science 2018")]
# ================= CTA (rosto) + fecho =================
c+=rosto_r2(P,r2,g-r2,3.05)
c[-1]["txt"]="COMBINADO: CURTE + SEGUE"; c[-1]["d"]=round(g-r2-0.25,2)
c+=[{"tipo":"glitch","t":g-0.05,"d":0.25},{"tipo":"flash","t":g,"d":0.2,"max":0.5},
 T(g+0.02,n2-g-0.02,"CURTE E SEGUE",y=600,f="170px Anton",cor="#c6ff3d",anim=None,entra="zoom",css="text-shadow:10px 10px 0 #000"),
 {"tipo":"flash","t":n2,"d":0.2,"max":0.5},
 T(n2+0.02,k(33.5)-n2-0.02,"PENSANDO EM CANETA?",y=600,f="160px Anton",anim=None,entra="zoom"),
 {"tipo":"checklist","t":k(33.5),"d":round(cut1-k(33.5),2),"box":[120,260,840,900],"titulo":"Isso se decide com:","entra":"cai","itens":[{"txt":"consulta","t":k(34.3)},{"txt":"exame","t":k(35.2)},{"txt":"foto de show","t":k(36.2)}],"z":40},
 {"tipo":"desenho","t":k(34.6),"d":round(cut1-k(34.6),2),"formas":[{"k":"check","c":[262,412],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":k(35.45),"d":round(cut1-k(35.45),2),"formas":[{"k":"check","c":[262,506],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":k(36.5),"d":round(cut1-k(36.5),2),"formas":[{"k":"x","c":[262,600],"s":34}],"espessura":12,"z":45},
 T(cut1+0.02,round(dur-cut1-0.02,2),"FOFOCA CORRE.",y=380,f="170px Anton",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 {"tipo":"carimbo","t":f(41.32),"d":round(dur-f(41.32),2),"xy":[40,760],"txt":"CIÊNCIA CONFERE","tam":115,"rot":-8,"z":60},
 F(f(41.32),round(dur-f(41.32),2),"Vosoughi, Roy e Aral, Science 2018 · doi 10.1126/science.aap9559")]
W=M+"iv_voz.words.json"
voz=[{"src":M+"iv_viral_bip.wav","t":0,"ms":0,"d":vd,"palavras":M+"iv_viral.words.json"},
 {"src":M+"iv_voz.wav","t":vd,"ms":0,"d":2.7,"palavras":W},
 {"src":M+"iv_voz.wav","t":r1,"ms":3.3,"d":2.75,"palavras":W},
 {"src":M+"iv_aula_voz.wav","t":L0,"ms":0,"d":A,"palavras":M+"iv_aula_voz.words.json"},
 {"src":M+"iv_voz.wav","t":T3,"ms":6.05,"d":16.1,"palavras":W},
 {"src":M+"iv_voz.wav","t":r2,"ms":25.9,"d":11.3,"palavras":W},
 {"src":M+"iv_voz.wav","t":cut1,"ms":40.05,"d":2.36,"palavras":W}]
musica=[{"src":"m_investiga","t":L0,"ms":0,"d":round(T3-L0,2),"gain":0.32,"fade":0.8}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.3,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"whoosh","t":vd,"gain":0.4,"pico":0.45},{"src":"glitch","t":r1-0.05,"gain":0.5},
 {"src":"whoosh","t":n(5.0),"gain":0.5,"pico":0.45},
 # aula
 {"src":"glitch","t":L0-0.05,"gain":0.5},{"src":"whoosh","t":L0,"gain":0.45,"pico":0.45},
 {"src":"boing","t":a(0.15),"gain":0.3},{"src":"boing","t":a(2.75),"gain":0.3},{"src":"boing","t":a(2.95),"gain":0.25},
 {"src":"whoosh2","t":a(4.30),"gain":0.35},{"src":"riser","t":a(6.0),"gain":0.22,"d":1.5},{"src":"whoosh","t":a(7.55),"gain":0.4,"pico":0.45},
 {"src":"whoosh2","t":a(8.55),"gain":0.35},{"src":"boing","t":a(8.6),"gain":0.3},{"src":"boing","t":a(9.1),"gain":0.3},
 {"src":"whoosh2","t":a(10.38),"gain":0.35},{"src":"scratch","t":a(11.68),"gain":0.25},
 {"src":"whoosh","t":a(13.10),"gain":0.4,"pico":0.45},{"src":"pagina","t":a(13.15),"gain":0.3},{"src":"boing","t":a(14.0),"gain":0.35},
 {"src":"glitch","t":T3-0.05,"gain":0.5},
 # estudo
 {"src":"whoosh2","t":m(6.15),"gain":0.4},{"src":"pagina","t":m(9.72),"gain":0.5},
 {"src":"boom","t":m(14.38),"gain":0.6,"pico":0.3,"d":1.5},{"src":"boom","t":m(17.84),"gain":0.5,"pico":0.3,"d":1.2},
 # CTA e fecho
 {"src":"glitch","t":r2-0.05,"gain":0.5},{"src":"notif","t":r2+0.2,"gain":0.4},{"src":"glitch","t":g-0.05,"gain":0.5},{"src":"boing","t":g+0.1,"gain":0.4},
 {"src":"papel","t":k(33.5),"gain":0.5},{"src":"boing","t":k(34.6),"gain":0.3},{"src":"boing","t":k(35.45),"gain":0.3},{"src":"glitch","t":k(36.5),"gain":0.4},
 {"src":"whoosh","t":cut1,"gain":0.5,"pico":0.45},{"src":"boom","t":f(41.32),"gain":0.7,"pico":0.3,"d":1.5}]
for x in c:
    if x.get("tipo")=="video" and "viral_blur" in x.get("src",""): x["box"]=[0,0,1080,2600]
    if L0-0.06<=x.get("t",-1)<T3-0.06: x["fixo"]=True
salvar("react_ivete_aula",dur,107,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000],[L0,T3,1730]]})
import json
p=json.load(open('planos/react_ivete_aula.json')); p['audio']['musica']=musica
json.dump(p,open('planos/react_ivete_aula.json','w'),ensure_ascii=False,indent=1)
print("ok dur",dur,"L0",L0,"T3",T3,"r2",r2,"g",g,"cut1",cut1)
