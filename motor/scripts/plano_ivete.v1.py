import sys; sys.path.insert(0,'scripts')
from mk import *
P='iv'; vd=8.85; r1=11.55; dur=51.1
n=lambda v: v+8.25
r2=n(25.9); g=n(28.6); n2=n(31.2)
c=abertura(P,vd,"via @natal.noticias","center 34%","Mito ou verdade? 👇","Dá para saber por foto se alguém usou caneta?",
  [{"tipo":"numero","t":4.3,"d":vd-4.35,"xy":[0,1150],"valor":7.4,"dec":1,"suf":" MI VIEWS","tam":120}])
c+=[rosto_r1(P,vd,r1-vd,0)]
c+=B(P+"_viral_blur.mp4",r1,r2-r1,10.0)+B(P+"_viral_blur.mp4",g,dur-g,35.0)
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 T(n(3.5),n(6.12)-n(3.5),"NINGUÉM SABE POR FOTO",f="145px Anton"),
 {"tipo":"gigante","t":n(5.0),"d":0.6,"txt":"POR FOTO?","y":1060,"tam":250,"cor":"#c6ff3d","x":[1000,-2200],"z":42},
 T(n(6.15),n(9.7)-n(6.15),"FOFOCA CORRE MAIS QUE A VERDADE",f="125px Anton",cor="#f2c230",css="text-shadow:8px 8px 0 #000"),
 {"tipo":"flash","t":n(9.7),"d":0.2,"max":0.5},
 {"tipo":"artigo","t":n(9.72),"d":n(11.62)-n(9.72),"box":[70,240,940,1000],"revista":"Science · 2018","titulo":"Como a verdade e a mentira se espalham na internet","autores":"Vosoughi S, Roy D, Aral S (MIT)","linhas":[{"txt":"126 mil notícias checadas, de 2006 a 2017"},{"txt":"a falsa foi mais longe e mais rápido","grifo":True},{"txt":"3 milhões de pessoas no antigo Twitter"}],"rodape":"PubMed 29590045","rola":0,"z":40},
 {"tipo":"flash","t":n(11.62),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(11.64),"d":n(14.36)-n(11.64),"xy":[0,420],"valor":126,"suf":" MIL","rotulo":"notícias checadas","tam":260,"z":44},
 {"tipo":"flash","t":n(14.36),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(14.38),"d":n(17.82)-n(14.38),"xy":[0,420],"valor":70,"suf":"%","rotulo":"mais chance de a falsa ser repassada","tam":300,"cor":"#ff2d3d","sombra":"#5a0d10","z":44},
 {"tipo":"flash","t":n(17.82),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(17.84),"d":n(22.15)-n(17.84),"xy":[0,420],"valor":6,"suf":"x","rotulo":"mais tempo pra verdade chegar a 1.500 pessoas","tam":300,"cor":"#f2c230","z":44},
 F(n(9.72),n(22.15)-n(9.72),"Vosoughi, Roy e Aral (MIT), Science 2018"),
 {"tipo":"checklist","t":n(22.18),"d":r2-n(22.18),"box":[120,260,840,900],"titulo":"Quem mais espalhou?","entra":"cai","itens":[{"txt":"robô","t":n(23.6)},{"txt":"gente","t":n(24.5)}],"z":40},
 {"tipo":"desenho","t":n(23.9),"d":r2-n(23.9),"formas":[{"k":"x","c":[262,412],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":n(24.75),"d":r2-n(24.75),"formas":[{"k":"check","c":[262,506],"s":34}],"espessura":12,"z":45}]
c+=rosto_r2(P,r2,g-r2,3.05)
c[-1]["txt"]="COMBINADO: CURTE + SEGUE"; c[-1]["d"]=g-r2-0.25
c+=[{"tipo":"glitch","t":g-0.05,"d":0.25},{"tipo":"flash","t":g,"d":0.2,"max":0.5},
 T(g+0.02,n(29.75)-g-0.02,"CURTE E SEGUE",y=600,f="170px Anton",cor="#c6ff3d",anim=None,entra="zoom",css="text-shadow:10px 10px 0 #000"),
 T(n(29.78),n2-n(29.78),"AQUI A VERDADE CHEGA PRIMEIRO",f="125px Anton"),
 {"tipo":"flash","t":n2,"d":0.2,"max":0.5},
 T(n(31.9),n(33.5)-n(31.9),"PENSANDO EM CANETA?",y=600,f="160px Anton",anim=None,entra="zoom"),
 {"tipo":"checklist","t":n(33.5),"d":n(37.4)-n(33.5),"box":[120,260,840,900],"titulo":"Isso se decide com:","entra":"cai","itens":[{"txt":"consulta","t":n(34.3)},{"txt":"exame","t":n(35.2)},{"txt":"foto de show","t":n(36.2)}],"z":40},
 {"tipo":"desenho","t":n(34.6),"d":n(37.4)-n(34.6),"formas":[{"k":"check","c":[262,412],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":n(35.45),"d":n(37.4)-n(35.45),"formas":[{"k":"check","c":[262,506],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":n(36.5),"d":n(37.4)-n(36.5),"formas":[{"k":"x","c":[262,600],"s":34}],"espessura":12,"z":45},
 T(n(37.42),n(40.18)-n(37.42),"TREINO DE FORÇA E PROTEÍNA",f="118px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
 {"tipo":"gigante","t":n(40.2),"d":0.6,"txt":"FOFOCA","y":700,"tam":300,"cor":"#c6ff3d","x":[1000,-1900],"z":42},
 T(n(40.6),n(41.3)-n(40.6),"CORRE",y=600,f="180px Anton",anim=None,entra="zoom"),
 {"tipo":"carimbo","t":n(41.32),"d":dur-n(41.32),"xy":[40,760],"txt":"CIÊNCIA CONFERE","tam":115,"rot":-8,"z":60},
 F(n(41.32),dur-n(41.32),"Vosoughi, Roy e Aral, Science 2018 · doi 10.1126/science.aap9559")]
voz=[{"src":M+"iv_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"iv_viral.words.json"},
 {"src":M+"iv_voz.wav","t":vd,"ms":0,"d":2.7,"palavras":M+"iv_voz.words.json"},
 {"src":M+"iv_voz.wav","t":r1,"ms":3.3,"d":round(dur-r1,2),"palavras":M+"iv_voz.words.json"}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.3,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"whoosh","t":vd,"gain":0.4,"pico":0.45},{"src":"glitch","t":r1-0.05,"gain":0.5},
 {"src":"whoosh","t":n(5.0),"gain":0.5,"pico":0.45},{"src":"whoosh2","t":n(6.15),"gain":0.4},{"src":"pagina","t":n(9.72),"gain":0.5},
 {"src":"boom","t":n(11.64),"gain":0.5,"pico":0.3,"d":1.2},{"src":"boom","t":n(14.38),"gain":0.6,"pico":0.3,"d":1.5},{"src":"boom","t":n(17.84),"gain":0.5,"pico":0.3,"d":1.2},
 {"src":"papel","t":n(22.18),"gain":0.5},{"src":"glitch","t":n(23.9),"gain":0.4},{"src":"boing","t":n(24.75),"gain":0.3},
 {"src":"glitch","t":r2-0.05,"gain":0.5},{"src":"notif","t":r2+0.2,"gain":0.4},{"src":"glitch","t":g-0.05,"gain":0.5},{"src":"boing","t":g+0.1,"gain":0.4},{"src":"whoosh2","t":n(29.78),"gain":0.4},
 {"src":"papel","t":n(33.5),"gain":0.5},{"src":"boing","t":n(34.6),"gain":0.3},{"src":"boing","t":n(35.45),"gain":0.3},{"src":"glitch","t":n(36.5),"gain":0.4},
 {"src":"whoosh2","t":n(37.42),"gain":0.4},{"src":"whoosh","t":n(40.2),"gain":0.5,"pico":0.45},{"src":"boom","t":n(41.32),"gain":0.7,"pico":0.3,"d":1.5}]
for x in c:
    if x.get("tipo")=="video" and "viral_blur" in x.get("src",""): x["box"]=[0,0,1080,2600]
salvar("react_ivete",dur,107,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000]]})
print("ok",r2,n2)
