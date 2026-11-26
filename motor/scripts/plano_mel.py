import sys; sys.path.insert(0,'scripts')
from mk import *
P='mg'; vd=9.26; r1=12.06; dur=53.2
n=lambda v: v+9.21
r2=n(18.1); n2=n(22.25)
c=abertura(P,vd,"via @medpagetoday","center 21%","Mito ou verdade? 👇","Vermífugo cura câncer em estágio 4?",
  [T(4.3,vd-4.35,"podcast, jan/2025",y=1150,f="110px Caveat",cor="#c6ff3d",vel=0.08)])
for x in c:
    if x.get("tipo") in ("video","foto") and x.get("box")==[70,190,940,909]: x["box"]=[70,190,940,853]
    if x.get("tipo")=="cartao": x["box"]=[40,150,1000,934]
c+=[rosto_r1(P,vd,r1-vd,0)]
c+=B(P+"_viral_blur.mp4",r1,r2-r1,0.5)+B(P+"_viral_blur.mp4",n2,dur-n2,20.0)
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 T(n(3.0),n(7.0)-n(3.0),"DEPOIS DO PODCAST",y=480,f="170px Anton",vel=0.12),
 {"tipo":"flash","t":n(7.15),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(7.0),"d":n(8.95)-n(7.0),"xy":[0,420],"valor":2,"suf":"x","tam":300,"cor":"#f2c230","z":44},
 T(n(7.0),n(8.95)-n(7.0),"RECEITAS DOBRARAM",y=860,f="140px Anton",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 F(n(3.0),n(8.95)-n(3.0),"Rockwell et al., JAMA Netw Open 2026"),
 T(n(8.97),n(10.48)-n(8.97),"SEM PROVA.",y=600,f="180px Anton",cor="#ff2d3d",anim=None,entra="zoom",css="text-shadow:10px 10px 0 #000"),
 {"tipo":"checklist","t":n(10.5),"d":n(15.95)-n(10.5),"box":[120,260,840,900],"titulo":"Onde já freou tumor?","entra":"cai","itens":[{"txt":"célula","t":n(10.7)},{"txt":"bicho","t":n(11.62)},{"txt":"gente","t":n(13.88)}],"z":40},
 {"tipo":"desenho","t":n(10.95),"d":n(15.95)-n(10.95),"formas":[{"k":"check","c":[262,412],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":n(11.85),"d":n(15.95)-n(11.85),"formas":[{"k":"check","c":[262,506],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":n(14.06),"d":n(15.95)-n(14.06),"formas":[{"k":"x","c":[262,600],"s":34}],"espessura":12,"z":45},
 T(n(15.98),r2-n(15.98),"NENHUMA CURA COMPROVADA",f="140px Anton",cor="#f2c230",css="text-shadow:8px 8px 0 #000")]
c+=rosto_r2(P,r2,n2-r2,3.05)
c+=[{"tipo":"flash","t":n2,"d":0.2,"max":0.5},
 T(n(23.2),n(26.1)-n(23.2),"ESTUDO DE YALE",y=480,f="170px Anton",vel=0.12),
 {"tipo":"flash","t":n(26.1),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(26.12),"d":n(28.6)-n(26.12),"xy":[0,420],"valor":840,"rotulo":"com câncer curável","tam":280,"z":44},
 T(n(28.62),n(31.1)-n(28.62),"TROCOU O TRATAMENTO",f="140px Anton"),
 {"tipo":"flash","t":n(31.1),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(31.12),"d":n(33.7)-n(31.12),"xy":[0,420],"valor":2.5,"dec":1,"suf":"x","rotulo":"risco de morrer","tam":300,"cor":"#ff2d3d","sombra":"#5a0d10","z":44},
 F(n(23.2),n(33.7)-n(23.2),"Johnson et al. (Yale), J Natl Cancer Inst 2018"),
 T(n(33.72),n(37.3)-n(33.72),"NÃO TESTOU VERMÍFUGO",y=380,f="150px Anton",anim=None,entra="zoom"),
 T(n(35.5),n(37.3)-n(35.5),"TESTOU LARGAR TRATAMENTO",y=760,f="125px Anton",cor="#f2c230",css="text-shadow:8px 8px 0 #000"),
 T(n(37.32),n(40.82)-n(37.32),"DÚVIDA? LEVA PRO ONCOLOGISTA",f="120px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
 T(n(40.84),dur-n(40.84),"ESPERANÇA SE RESPEITA",y=380,f="135px Anton"),
 {"tipo":"carimbo","t":n(42.44),"d":dur-n(42.44),"xy":[50,760],"txt":"NÃO COMPROVADO","tam":110,"rot":-8,"z":60},
 F(n(42.44),dur-n(42.44),"Johnson, J Natl Cancer Inst 2018 · doi 10.1093/jnci/djx145 · Rockwell, JAMA Netw Open 2026 · doi 10.1001/jamanetworkopen.2026.16780")]
voz=[{"src":M+"mg_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"mg_viral.words.json"},
 {"src":M+"mg_voz.wav","t":vd,"ms":0,"d":2.8,"palavras":M+"mg_voz.words.json"},
 {"src":M+"mg_voz.wav","t":r1,"ms":2.85,"d":round(dur-r1,2),"palavras":M+"mg_voz.words.json"}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"whoosh","t":vd,"gain":0.4,"pico":0.45},{"src":"glitch","t":r1-0.05,"gain":0.5},
 {"src":"whoosh2","t":n(3.0),"gain":0.4},{"src":"boom","t":n(7.17),"gain":0.6,"pico":0.3,"d":1.5},{"src":"boom","t":n(8.97),"gain":0.5,"pico":0.3,"d":1.2},
 {"src":"papel","t":n(10.5),"gain":0.5},{"src":"boing","t":n(10.95),"gain":0.3},{"src":"boing","t":n(11.85),"gain":0.3},{"src":"glitch","t":n(14.06),"gain":0.4},
 {"src":"whoosh2","t":n(15.98),"gain":0.4},{"src":"glitch","t":r2-0.05,"gain":0.5},{"src":"notif","t":r2+0.2,"gain":0.4},{"src":"glitch","t":n2-0.05,"gain":0.5},
 {"src":"whoosh2","t":n(23.2),"gain":0.4},{"src":"boom","t":n(26.12),"gain":0.5,"pico":0.3,"d":1.2},{"src":"whoosh2","t":n(28.62),"gain":0.4},{"src":"boom","t":n(31.12),"gain":0.6,"pico":0.3,"d":1.5},
 {"src":"whoosh2","t":n(35.62),"gain":0.4},{"src":"whoosh2","t":n(37.32),"gain":0.4},{"src":"boom","t":n(42.44),"gain":0.7,"pico":0.3,"d":1.5}]
for x in c:
    if x.get("tipo")=="video" and "viral_blur" in x.get("src",""): x["box"]=[0,0,1080,2400]
salvar("react_mel",dur,101,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000]]})
print("ok",r2,n2)
