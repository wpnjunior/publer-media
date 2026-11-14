import sys; sys.path.insert(0,'scripts')
from mk import *
P='cf'; vd=11.25; r1=15.15; dur=51.2
n=lambda v: v+10.95
r2=n(12.7); n2=n(17.45)
c=abertura(P,vd,"via @psi.walace","center 34%","Mito ou verdade? ☕","Café dá sono? Então é TDAH?",
  [{"tipo":"numero","t":4.3,"d":vd-4.35,"xy":[0,1150],"valor":821.8,"dec":1,"suf":" MIL VIEWS","tam":120}])
c+=[{"tipo":"texto","t":vd+0.05,"d":1.75,"xy":[40,1330],"w":1000,"fonte":"220px Anton","cor":"#f2c230","alinha":"center","txt":"CALMA.","z":40,"entra":"zoom","css":"text-shadow:10px 10px 0 #000"},
    rosto_r1(P,vd+1.8,r1-vd-1.8,1.8)]
c+=B(P+"_viral_blur.mp4",r1,r2-r1,0.5)+B(P+"_viral_blur.mp4",n2,dur-n2,20.0)
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 T(r1+0.05,n(6.45)-r1-0.05,"CAFÉ NÃO VIROU CALMANTE",f="140px Anton"),
 {"tipo":"gigante","t":n(5.2),"d":0.6,"txt":"CALMANTE?","y":1180,"tam":240,"cor":"#c6ff3d","x":[1000,-2200],"z":42},
 {"tipo":"flash","t":n(6.45),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(6.48),"d":n(9.88)-n(6.48),"xy":[0,420],"valor":7,"rotulo":"estudos com crianças","tam":300,"z":44},
 {"tipo":"flash","t":n(9.88),"d":0.2,"max":0.5},
 T(n(9.9),r2-n(9.9),"CAFÉ NÃO MELHOROU OS SINTOMAS",y=440,f="140px Anton",cor="#f2c230",vel=0.12,css="text-shadow:8px 8px 0 #000"),
 F(n(6.48),r2-n(6.48),"Perrotte et al., Brain Sci 2023 (7 estudos, crianças de 5 a 15 anos)")]
c+=rosto_r2(P,r2,4.75,4.2)
c[-1]["txt"]="GORJETA: SEGUE + CURTE"
c+=[{"tipo":"flash","t":n2,"d":0.2,"max":0.5},
 T(n(18.35),n(22.4)-n(18.35),"300 ADOLESCENTES COM TDAH",y=440,f="150px Anton",vel=0.12),
 {"tipo":"flash","t":n(22.4),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(22.42),"d":n(26.5)-n(22.42),"xy":[0,420],"valor":2.5,"dec":1,"suf":"x","tam":300,"cor":"#f2c230","z":44},
 T(n(22.6),n(26.5)-n(22.6),"MAIS CAFÉ À NOITE",y=860,f="140px Anton",cor="#ffffff",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 F(n(18.35),n(26.5)-n(18.35),"Cusick et al., J Pediatr Psychol 2020"),
 T(n(26.52),n(28.6)-n(26.52),"DORMIA PIOR",y=440,f="190px Anton",cor="#f2c230",css="text-shadow:8px 8px 0 #000"),
 {"tipo":"gigante","t":n(28.0),"d":0.6,"txt":"SONO","y":700,"tam":320,"cor":"#c6ff3d","x":[1000,-1600],"z":42},
 T(n(28.6),n(31.95)-n(28.6),"ESTUDOS COM JOVENS",y=480,f="150px Anton",cor="#f2c230",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 {"tipo":"checklist","t":n(31.98),"d":n(34.9)-n(31.98),"box":[120,260,840,900],"titulo":"Vale consulta?","entra":"cai","itens":[{"txt":"sono demais","t":n(32.02)},{"txt":"foco que não vem","t":n(33.2)}],"z":40},
 T(n(34.9),n(37.7)-n(34.9),"CONVERSA COM SEU MÉDICO",y=420,f="140px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
 {"tipo":"carimbo","t":n(37.72),"d":dur-n(37.72),"xy":[60,760],"txt":"CAFÉ NÃO É EXAME","tam":118,"rot":-8,"z":60},
 F(n(37.72),dur-n(37.72),"Perrotte, Brain Sci 2023 · doi 10.3390/brainsci13091304 · Cusick, J Pediatr Psychol 2020 · doi 10.1093/jpepsy/jsaa033")]
voz=[{"src":M+"cf_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"cf_viral.words.json"},
 {"src":M+"cf_voz.wav","t":vd,"ms":0,"d":3.9,"palavras":M+"cf_voz.words.json"},
 {"src":M+"cf_voz.wav","t":r1,"ms":4.2,"d":round(dur-r1,2),"palavras":M+"cf_voz.words.json"}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.3,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"boom","t":vd+0.05,"gain":0.5,"pico":0.3,"d":1.2},{"src":"whoosh","t":vd+1.8,"gain":0.4,"pico":0.45},
 {"src":"glitch","t":r1-0.05,"gain":0.5},{"src":"whoosh","t":n(5.2),"gain":0.5,"pico":0.45},{"src":"boom","t":n(6.48),"gain":0.6,"pico":0.3,"d":1.5},
 {"src":"whoosh2","t":n(9.9),"gain":0.4},{"src":"glitch","t":r2-0.05,"gain":0.5},{"src":"notif","t":r2+0.2,"gain":0.4},{"src":"glitch","t":n2-0.05,"gain":0.5},
 {"src":"whoosh2","t":n(18.35),"gain":0.4},{"src":"boing","t":n(22.6),"gain":0.35},{"src":"boom","t":n(22.42),"gain":0.6,"pico":0.3,"d":1.5},{"src":"whoosh2","t":n(26.52),"gain":0.4},
 {"src":"whoosh","t":n(28.0),"gain":0.5,"pico":0.45},{"src":"papel","t":n(31.98),"gain":0.5},{"src":"whoosh2","t":n(34.9),"gain":0.4},{"src":"whoosh2","t":n(28.6),"gain":0.35},{"src":"boom","t":n(37.72),"gain":0.7,"pico":0.3,"d":1.5}]
salvar("react_cafe",dur,91,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1],[10.9,vd+1.85]],"ys":[[4.1,vd,1440],[vd,r1,1000]]})
print("ok",r2,n2)
