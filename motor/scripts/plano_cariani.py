import sys; sys.path.insert(0,'scripts')
from mk import *
P='ca'; vd=11.59; r1=14.59; dur=43.5; r2=32.4; n2=37.05
c=abertura(P,vd,"via @flowpdc","center 11%","Mito ou verdade? 👇","Na caneta, só perde músculo quem não treina?",
  [{"tipo":"numero","t":4.3,"d":7.2,"xy":[0,1150],"valor":766,"suf":" MIL VIEWS","tam":120}])
c+=[rosto_r1(P,vd,r1-vd,0)]
c+=B(P+"_viral_blur.mp4",r1,r2-r1,0.5)+B(P+"_viral_blur.mp4",n2,dur-n2,25.0)
n=lambda v: v+10.89
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 {"tipo":"checklist","t":n(3.84),"d":n(7.5)-n(3.84),"box":[120,260,840,900],"titulo":"Protege o músculo?","entra":"cai","itens":[{"txt":"proteína","t":n(5.22)},{"txt":"treino de força","t":n(6.0)}],"z":40},
 {"tipo":"desenho","t":n(5.5),"d":n(7.5)-n(5.5),"formas":[{"k":"check","c":[262,412],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":n(6.3),"d":n(7.5)-n(6.3),"formas":[{"k":"check","c":[262,506],"s":34}],"espessura":12,"z":45},
 T(n(7.56),n(9.85)-n(7.56),"PERDE MESMO COM MÉDICO",f="140px Anton",cor="#f2c230",css="text-shadow:8px 8px 0 #000"),
 {"tipo":"flash","t":n(9.85),"d":0.2,"max":0.5},
 T(n(9.9),n(14.42)-n(9.9),"35 ESTUDOS, COM MÉDICO DO LADO",y=440,f="140px Anton",vel=0.12),
 {"tipo":"flash","t":n(14.42),"d":0.2,"max":0.5},
 T(n(14.46),n(17.5)-n(14.46),"3 EM CADA 10 QUILOS",y=380,f="150px Anton",cor="#f2c230",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 T(n(15.2),n(17.5)-n(15.2),"NÃO ERA GORDURA",y=760,f="160px Anton",cor="#ff2d3d",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #5a0d10"),
 T(n(17.56),r2-n(17.56),"NEM TUDO É MÚSCULO",y=480),
 T(n(18.9),r2-n(18.9),"TEM ÁGUA NA CONTA",y=900,f="120px Anton",cor="#f2c230",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 F(n(9.9),r2-n(9.9),"Batsis et al., Ann Intern Med 2026 (revisão de 35 estudos)")]
c+=rosto_r2(P,r2,4.65,3.56)
m=lambda v: v+10.0
c+=[{"tipo":"flash","t":n2,"d":0.2,"max":0.5},
 T(m(27.2),m(30.3)-m(27.2),"TREINO? COMBINA COM SEU MÉDICO",f="130px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
 T(m(30.34),dur-m(30.34),"A BALANÇA CONTA O PESO",y=380,f="140px Anton"),
 {"tipo":"gigante","t":m(31.84),"d":0.6,"txt":"TREINO","y":700,"tam":300,"cor":"#c6ff3d","x":[1000,-1800],"z":42},
 {"tipo":"carimbo","t":m(32.16),"d":dur-m(32.16),"xy":[60,760],"txt":"O TREINO ESCOLHE","tam":120,"rot":-8,"z":60},
 F(m(32.16),dur-m(32.16),"Batsis et al., Ann Intern Med 2026 · doi 10.7326/ANNALS-25-00478")]
voz=[{"src":M+"ca_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"ca_viral.words.json"},
 {"src":M+"ca_voz.wav","t":vd,"ms":0,"d":round(r1-vd,2),"palavras":M+"ca_voz.words.json"},
 {"src":M+"ca_voz.wav","t":r1,"ms":3.7,"d":round(r2-r1,2),"palavras":M+"ca_voz.words.json"},
 {"src":M+"ca_voz.wav","t":r2,"ms":22.16,"d":4.65,"palavras":M+"ca_voz.words.json"},
 {"src":M+"ca_voz.wav","t":n2,"ms":27.05,"d":round(dur-n2,2),"palavras":M+"ca_voz.words.json"}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.3,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"glitch","t":r1-0.05,"gain":0.5},{"src":"whoosh","t":r1,"gain":0.5,"pico":0.45},
 {"src":"papel","t":n(3.84),"gain":0.5},{"src":"boing","t":n(5.5),"gain":0.3},{"src":"boing","t":n(6.3),"gain":0.3},{"src":"whoosh2","t":n(7.56),"gain":0.4},
 {"src":"whoosh2","t":n(9.9),"gain":0.4},{"src":"boing","t":n(15.2),"gain":0.35},{"src":"boing","t":n(18.9),"gain":0.3},{"src":"boom","t":n(14.46),"gain":0.6,"pico":0.3,"d":1.5},{"src":"whoosh","t":n(17.56),"gain":0.4,"pico":0.45},
 {"src":"glitch","t":r2-0.05,"gain":0.5},{"src":"notif","t":r2+0.2,"gain":0.4},{"src":"glitch","t":n2-0.05,"gain":0.5},
 {"src":"whoosh2","t":m(27.2),"gain":0.4},{"src":"whoosh","t":m(31.84),"gain":0.5,"pico":0.45},{"src":"boom","t":m(32.16),"gain":0.7,"pico":0.3,"d":1.5}]
salvar("react_cariani",dur,83,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000]]})
print("ok")
