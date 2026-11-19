import sys; sys.path.insert(0,'scripts')
from mk import *
P='su'; vd=9.15; r1=13.61; dur=44.8
c=abertura(P,vd,"via @parishilton","center 17%","Mito ou verdade? 👇","TDAH é superpoder?",
  [{"tipo":"numero","t":4.3,"d":4.8,"xy":[0,1150],"valor":2.5,"dec":1,"suf":" MI VIEWS","tam":120}])
c+=[rosto_r1(P,vd,r1-vd,0)]
c+=B(P+"_viral_blur.mp4",r1,24.83-r1,0.5)+B(P+"_viral_blur.mp4",29.08,dur-29.08,20.0)
n=lambda v: v+8.76
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 T(n(4.94),1.96,"NÃO EXAMINEI NINGUÉM",f="140px Anton"),
 {"tipo":"flash","t":n(6.85),"d":0.2,"max":0.5},
 T(n(6.9),1.5,"31 ESTUDOS",y=480,f="190px Anton",cor="#f2c230",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 {"tipo":"checklist","t":n(8.4),"d":n(13.45)-n(8.4),"box":[120,260,840,900],"titulo":"Mais ideia original?","entra":"cai","itens":[{"txt":"só alguns traços","t":n(9.64)},{"txt":"com diagnóstico","t":n(11.14)}],"z":40},
 {"tipo":"desenho","t":n(10.0),"d":n(13.45)-n(10.0),"formas":[{"k":"check","c":[262,412],"s":34}],"espessura":12,"z":45},
 {"tipo":"desenho","t":n(12.52),"d":n(13.45)-n(12.52),"formas":[{"k":"x","c":[262,506],"s":34}],"espessura":12,"z":45},
 T(n(13.5),24.83-n(13.5),"TALENTO APARECE NOS DOIS",f="140px Anton",cor="#3ddc84",css="text-shadow:8px 8px 0 #000"),
 F(n(6.9),24.83-n(6.9),"Hoogman et al., Neurosci Biobehav Rev 2020")]
c+=rosto_r2(P,24.83,4.25,4.95)
m=lambda v: v+7.48
c+=[{"tipo":"flash","t":29.08,"d":0.2,"max":0.5},
 T(29.2,m(26.0)-29.2,"TDAH E ACIDENTE DE TRÂNSITO",y=440,f="140px Anton",vel=0.12),
 {"tipo":"flash","t":m(26.0),"d":0.2,"max":0.5},
 {"tipo":"numero","t":m(26.02),"d":m(28.55)-m(26.02),"xy":[0,420],"valor":45,"suf":"%","rotulo":"mais acidente grave","tam":300,"cor":"#ff2d3d","sombra":"#5a0d10","z":44},
 F(29.2,m(28.55)-29.2,"Chang et al., JAMA Psychiatry 2014 (17.408 adultos, Suécia)"),
 T(m(28.6),m(31.65)-m(28.6),"ATRAPALHA TRABALHO, TRÂNSITO E RELAÇÃO",y=440,f="120px Anton",vel=0.1),
 T(m(31.72),m(34.5)-m(31.72),"CONVERSA COM SEU MÉDICO",f="125px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
 {"tipo":"gigante","t":m(34.5),"d":0.65,"txt":"TRANSTORNO","y":700,"tam":280,"cor":"#c6ff3d","x":[1000,-2400],"z":42},
 {"tipo":"carimbo","t":m(35.12),"d":dur-m(35.12),"xy":[110,760],"txt":"NÃO É SUPERPODER","tam":130,"rot":-8,"z":60},
 F(m(35.12),dur-m(35.12),"Hoogman et al., Neurosci Biobehav Rev 2020 · doi 10.1016/j.neubiorev.2020.09.029 · Chang et al., JAMA Psychiatry 2014 · doi 10.1001/jamapsychiatry.2013.4174")]
voz=[{"src":M+"su_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"su_viral.words.json"},
 {"src":M+"su_voz.wav","t":vd,"ms":0,"d":r1-vd,"palavras":M+"su_voz.words.json"},
 {"src":M+"su_voz.wav","t":r1,"ms":4.85,"d":round(24.83-r1,2),"palavras":M+"su_voz.words.json"},
 {"src":M+"su_voz.wav","t":24.83,"ms":16.7,"d":4.25,"palavras":M+"su_voz.words.json"},
 {"src":M+"su_voz.wav","t":29.08,"ms":21.6,"d":round(dur-29.08,2),"palavras":M+"su_voz.words.json"}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},{"src":"pagina","t":4.3,"gain":0.35},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"glitch","t":r1-0.05,"gain":0.5},{"src":"whoosh","t":r1,"gain":0.5,"pico":0.45},
 {"src":"teclado","t":n(6.9),"gain":0.3,"d":0.6},{"src":"papel","t":n(8.4),"gain":0.5},{"src":"boing","t":n(10.0),"gain":0.3},{"src":"boing","t":n(12.52),"gain":0.3},
 {"src":"whoosh2","t":n(13.5),"gain":0.4},{"src":"glitch","t":24.78,"gain":0.5},{"src":"notif","t":25.03,"gain":0.4},
 {"src":"glitch","t":29.03,"gain":0.5},{"src":"whoosh2","t":29.2,"gain":0.4},{"src":"boom","t":m(26.02),"gain":0.6,"pico":0.3,"d":1.5},
 {"src":"papel","t":m(28.6),"gain":0.5},{"src":"whoosh2","t":m(31.72),"gain":0.4},{"src":"whoosh","t":m(34.5),"gain":0.5,"pico":0.45},{"src":"boom","t":m(35.12),"gain":0.7,"pico":0.3,"d":1.5}]
salvar("react_tdah_superpoder",dur,71,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000]]})
print("ok")
