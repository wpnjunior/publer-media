import sys; sys.path.insert(0,'scripts')
from mk import *
P='cr'; vd=5.17; r1=8.17; dur=42.9
n=lambda v: v+5.45
r2=n(24.6); g=n(28.0); n2=n(29.85)
c=abertura(P,vd,"via @canalgnt","center 17%","Responde aí 👇","Engravidar depois dos 50 é...",[])
for x in c:
    if x.get("tipo")=="pergunta": x["botoes"]=["RARO","COMUM"]
c+=[rosto_r1(P,vd,r1-vd,0)]
c+=B(P+"_viral_blur.mp4",r1,r2-r1,0.5)+B(P+"_viral_blur.mp4",g,dur-g,6.0)
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 T(n(2.75),n(5.6)-n(2.75),"ELA ACERTA: É RARO",f="150px Anton"),
 {"tipo":"gigante","t":n(4.7),"d":0.6,"txt":"RARO","y":1180,"tam":300,"cor":"#c6ff3d","x":[1000,-1500],"z":42},
 T(n(5.65),n(8.05)-n(5.65),"EU NÃO EXAMINEI NINGUÉM",f="130px Anton"),
 T(n(6.9),n(8.05)-n(6.9),"falo de número",y=930,f="100px Caveat",cor="#c6ff3d",vel=0.08,z=46),
 {"tipo":"flash","t":n(8.08),"d":0.2,"max":0.5},
 {"tipo":"artigo","t":n(8.1),"d":n(10.68)-n(8.1),"box":[70,240,940,1000],"revista":"Hum Reprod · 2014","titulo":"Com que idade termina a fertilidade natural?","autores":"Eijkemans MJC, van Poppel F, te Velde ER et al.","linhas":[{"txt":"58.051 mulheres sem controle de natalidade"},{"txt":"aos 45: quase 90% já tinham tido o último filho","grifo":True},{"txt":"6 populações históricas"}],"rodape":"PubMed 24676403","rola":0,"z":40},
 {"tipo":"flash","t":n(10.68),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(10.7),"d":n(14.2)-n(10.7),"xy":[0,420],"valor":90,"suf":"%","rotulo":"não tiveram mais filhos depois dos 45","tam":300,"cor":"#f2c230","z":44},
 {"tipo":"flash","t":n(14.2),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(14.22),"d":n(16.68)-n(14.22),"xy":[0,420],"valor":100,"suf":"%","rotulo":"depois dos 50: perto de todas","tam":300,"cor":"#ff2d3d","sombra":"#5a0d10","z":44},
 F(n(8.1),n(16.68)-n(8.1),"Eijkemans et al., Hum Reprod 2014"),
 {"tipo":"flash","t":n(16.68),"d":0.2,"max":0.5},
 {"tipo":"artigo","t":n(16.7),"d":n(19.95)-n(16.7),"box":[70,240,940,1000],"revista":"Reprod Biol Endocrinol · 2023","titulo":"Bebê com óvulos próprios depois dos 42","autores":"Seifer DB, Wang SF, Frankfurter D","linhas":[{"txt":"24.650 mulheres no registro dos EUA"},{"txt":"começando aos 45: 5 em cada 100 tiveram bebê","grifo":True},{"txt":"tratamento com óvulos próprios"}],"rodape":"PubMed 37872609","rola":0,"z":40},
 {"tipo":"flash","t":n(19.95),"d":0.2,"max":0.5},
 {"tipo":"numero","t":n(19.97),"d":n(22.0)-n(19.97),"xy":[0,420],"valor":5,"suf":" EM 100","rotulo":"tiveram bebê aos 45 com óvulos próprios","tam":240,"cor":"#f2c230","z":44},
 F(n(16.7),n(22.0)-n(16.7),"Seifer et al., Reprod Biol Endocrinol 2023"),
 T(n(22.02),r2-n(22.02),"É MÉDIA, NÃO SENTENÇA",f="140px Anton",cor="#3ddc84",css="text-shadow:8px 8px 0 #000")]
c+=rosto_r2(P,r2,g-r2,3.15)
c[-1]["txt"]="COMBINADO: CURTE + SEGUE"; c[-1]["d"]=g-r2-0.25
c+=[{"tipo":"glitch","t":g-0.05,"d":0.25},{"tipo":"flash","t":g,"d":0.2,"max":0.5},
 T(g+0.02,n2-g-0.02,"CURTE E SEGUE, CASAL",y=600,f="160px Anton",cor="#c6ff3d",anim=None,entra="zoom",css="text-shadow:10px 10px 0 #000"),
 {"tipo":"flash","t":n2,"d":0.2,"max":0.5},
 T(n(30.0),n(31.3)-n(30.0),"DÚVIDA?",y=620,f="200px Anton",anim=None,entra="zoom"),
 T(n(31.32),n(33.92)-n(31.32),"VOCÊS DOIS, JUNTOS, NO MÉDICO",f="118px Anton",cor="#3ddc84",vel=0.1,css="text-shadow:8px 8px 0 #000"),
 {"tipo":"gigante","t":n(32.2),"d":0.6,"txt":"JUNTOS","y":1180,"tam":280,"cor":"#c6ff3d","x":[1000,-1900],"z":42},
 T(n(33.94),n(35.68)-n(33.94),"MANCHETE MOSTRA A EXCEÇÃO",f="122px Anton"),
 {"tipo":"carimbo","t":n(35.7),"d":dur-n(35.7),"xy":[40,760],"txt":"EXCEÇÃO, NÃO REGRA","tam":100,"rot":-8,"z":60},
 F(n(35.7),dur-n(35.7),"Eijkemans, Hum Reprod 2014 · doi 10.1093/humrep/deu056 · Seifer, Reprod Biol Endocrinol 2023 · doi 10.1186/s12958-023-01144-z")]
voz=[{"src":M+"cr_viral.mp4","t":0,"ms":0,"d":vd,"palavras":M+"cr_viral.words.json"},
 {"src":M+"cr_voz.wav","t":vd,"ms":0,"d":2.72,"palavras":M+"cr_voz.words.json"},
 {"src":M+"cr_voz.wav","t":r1,"ms":2.72,"d":round(dur-r1,2),"palavras":M+"cr_voz.words.json"}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"boing","t":3.3,"gain":0.4},
 {"src":"glitch","t":vd-0.05,"gain":0.5},{"src":"whoosh","t":vd,"gain":0.4,"pico":0.45},{"src":"glitch","t":r1-0.05,"gain":0.5},
 {"src":"whoosh","t":n(4.7),"gain":0.5,"pico":0.45},{"src":"pagina","t":n(8.1),"gain":0.5},{"src":"boom","t":n(10.7),"gain":0.6,"pico":0.3,"d":1.5},
 {"src":"boom","t":n(14.22),"gain":0.5,"pico":0.3,"d":1.2},{"src":"pagina","t":n(16.7),"gain":0.5},{"src":"boom","t":n(19.97),"gain":0.6,"pico":0.3,"d":1.5},
 {"src":"whoosh2","t":n(22.02),"gain":0.4},{"src":"glitch","t":r2-0.05,"gain":0.5},{"src":"notif","t":r2+0.2,"gain":0.4},{"src":"glitch","t":g-0.05,"gain":0.5},
 {"src":"boing","t":g+0.1,"gain":0.4},{"src":"glitch","t":n2-0.05,"gain":0.4},{"src":"whoosh2","t":n(31.32),"gain":0.4},{"src":"whoosh","t":n(32.2),"gain":0.5,"pico":0.45},
 {"src":"boom","t":n(35.7),"gain":0.7,"pico":0.3,"d":1.5}]
salvar("react_claudia",dur,97,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.1]],"ys":[[4.1,vd,1440],[vd,r1,1000]]})
print("ok",r2,g,n2)
