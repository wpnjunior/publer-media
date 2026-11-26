# plano_figado.py: react do fígado (Papo de Médico, 27/11) refeito em 14/11 com as regras novas do Wagner:
# voz Murilo de contexto, resposta só ao que ela disse, aula de fisiologia/fisiopatologia com camada fisio sobre b-roll,
# estudo verificado (Sies & Brooker, Lancet 2005), orientação simples e CTA do banco (cta6, avatar 6cd9).
# Rodar de /tmp/claude-0/motor:  python3 scripts/plano_figado.py
import sys, json, subprocess; sys.path.insert(0,'scripts')
from mk import *
PID='react_figado'; V=M+'fig_viral.mp4'; ARR="via @oficialaandressa"
# ---- viral (tempos antes da entrada) ----
segs=[(0.0,1.65,67.60,"center 55%"),   # A: peneira "Fiquem aí com o meu resultado."
      (1.65,2.55,0.00,"center 12%"),   # B: "Sétimo dia de limpeza hepática."
      (4.20,5.55,3.00,"center 25%"),   # C: ela tomando o sal amargo, Murilo por cima (viral a 0.16)
      (9.75,4.00,51.30,"center 42%")]  # D: "coloquei tanta sujeira para fora, sabe? Um monte de pedra amarela."
vd=13.75; r1=vd+4.5
n=lambda x: round(r1+x-4.40,3)        # x = tempo dentro de fig2_voz.wav
cta=n(40.62); dur=round(cta+4.12,2)
c=[{"tipo":"cartao","t":0,"d":r1,"box":[40,150,1000,990],"aba":"o viral","entra":"whip"}]
for t,d,ms,pos in segs:
    c.append({"tipo":"video","t":t,"d":d,"ms":ms,"src":V,"box":[70,190,940,909],"raio":14,"pos":pos,"arroba":ARR,"arroba_pos":"topo",
              "respira":False,"zoom":[[t,1.0,0.01],[t+0.1,1.07,max(0.5,d-0.2)]],"z":30})
c+=[{"tipo":"pergunta","t":0.1,"d":4.05,"xy":[110,1150],"w":790,"topo":"O que é isso? 👇","txt":"Isso saiu do fígado?","botoes":["PEDRA","OUTRA COISA"],"vel":0.025,"escolha":1,"t_escolha":3.4},
    {"tipo":"glitch","t":vd-0.05,"d":0.25},
    {"tipo":"foto","t":vd,"d":r1-vd,"src":M+"fig2_still.jpg","box":[70,190,940,909],"raio":14,"sombra":False,"z":29},
    rosto_r1("fig2",vd,4.24,0),
    {"tipo":"foto","t":vd+4.22,"d":round(r1-vd-4.22,2),"src":M+"fig2_rosto_fim.jpg","box":[0,1140,1080,780],"pos":"center 30%","sombra":False,"z":44},
    T(4.45,9.65-4.45,"SAL AMARGO · JEJUM · AZEITE",y=1170,f="96px Anton",cor="#ffe27a",vel=0.6,css="text-shadow:6px 6px 0 #000"),
    T(12.2,vd-12.2,"PEDRA AMARELA?",y=1170,f="120px Anton",cor="#ffffff",anim=None,entra="zoom",css="text-shadow:6px 6px 0 #000"),
    {"tipo":"carimbo","t":vd+1.75,"d":r1-vd-1.8,"xy":[150,420],"txt":"NÃO É PEDRA","tam":130,"rot":-8,"z":60}]
# ---- aula (fisiologia + fisiopatologia) sobre b-roll ----
c+=B("fig2_b_sangue.mp4",r1,n(10.6)-r1,0)+B("fig2_b_azeite.mp4",n(10.6),n(14.2)-n(10.6),0)+B("fig2_b_limao.mp4",n(14.2),n(18.3)-n(14.2),0)+\
   B("fig2_b_agua.mp4",n(18.3),n(21.7)-n(18.3),0)+B("fig2_b_lab.mp4",n(21.7),n(28.2)-n(21.7),0)+B("fig2_b_micro.mp4",n(28.2),n(34.0)-n(28.2),0)+\
   B("fig2_b_medico.mp4",n(34.0),n(40.5)-n(34.0),0)
f1=n(4.45)
c+=[{"tipo":"glitch","t":r1-0.05,"d":0.25},{"tipo":"flash","t":r1,"d":0.2,"max":0.6},
 T(n(4.56),n(7.0)-n(4.56),"O FÍGADO JÁ FAZ FAXINA",y=240,f="104px Anton",cor="#ffe27a",vel=0.1,css="text-shadow:6px 6px 0 #000"),
 {"tipo":"fisio","t":f1,"d":n(10.6)-f1,"z":40,
  "orgaos":[{"k":"figado","xy":[560,800],"s":1.25,"t":0.15,"rotulo":"FÍGADO","rot_y":200}],
  "fluxos":[{"de":[40,470],"para":[400,720],"curva":-120,"cor":"#ff4d5a","t":n(7.06)-f1,"d":2.6,"n":8,"rotulo":"SANGUE","r":14},
            {"de":[700,900],"para":[1010,1220],"curva":-60,"cor":"#ffd400","t":n(8.6)-f1,"d":1.9,"n":6,"rotulo":"LIXO FORA","r":14}],
  "pulsos":[{"o":0,"t":n(7.1)-f1},{"o":0,"t":n(8.7)-f1}]},
 T(n(9.4),n(10.6)-n(9.4)+0.2,"URINA E BILE",y=1150,f="90px Anton",cor="#ffffff",anim=None,entra="zoom",css="text-shadow:6px 6px 0 #000")]
f2=n(10.7)
c+=[{"tipo":"flash","t":n(10.6),"d":0.2,"max":0.5},
 T(n(10.8),n(12.4)-n(10.8),"A RECEITA",y=240,f="120px Anton",cor="#ffe27a",css="text-shadow:6px 6px 0 #000"),
 {"tipo":"fisio","t":f2,"d":n(21.7)-f2,"z":40,
  "orgaos":[{"k":"intestino","xy":[540,800],"s":1.05,"t":0.2,"rotulo":"INTESTINO","rot_y":250},
            {"k":"sabao","xy":[540,820],"s":0.75,"t":n(17.2)-f2,"rotulo":"BOLINHA MOLE","rot_y":175,"cor_rotulo":"#e8f26a"}],
  "fluxos":[{"de":[540,300],"para":[540,600],"curva":0,"cor":"#d8c234","t":n(12.32)-f2,"d":1.9,"n":8,"rotulo":"AZEITE","r":16},
            {"de":[40,560],"para":[330,760],"curva":-90,"cor":"#fff04a","t":n(15.7)-f2,"d":1.6,"n":6,"rotulo":"LIMÃO","r":13},
            {"de":[1040,520],"para":[760,740],"curva":-90,"cor":"#5ab8ff","t":n(19.42)-f2,"d":1.3,"n":6,"rotulo":"ÁGUA","r":14},
            {"de":[700,980],"para":[1000,1250],"curva":-40,"cor":"#b9c94a","t":n(20.3)-f2,"d":1.1,"n":5,"rotulo":"PRA FORA","r":22}],
  "pulsos":[{"o":0,"t":n(13.3)-f2},{"o":1,"t":n(17.6)-f2},{"o":0,"t":n(20.3)-f2}]},
 T(n(14.3),n(16.8)-n(14.3),"A GORDURA SE QUEBRA",y=240,f="100px Anton",cor="#ffffff",vel=0.1,css="text-shadow:6px 6px 0 #000"),
 T(n(18.5),n(21.6)-n(18.5),"SAL AMARGO PUXA ÁGUA",y=240,f="100px Anton",cor="#5ab8ff",vel=0.1,css="text-shadow:6px 6px 0 #000")]
# ---- estudo ----
c+=[{"tipo":"flash","t":n(21.7),"d":0.2,"max":0.6},
 T(n(21.92),n(25.4)-n(21.92),"2005: A LANCET ANALISOU",y=470,f="150px Anton",vel=0.12),
 F(n(21.92),n(33.9)-n(21.92),"Sies & Brooker, The Lancet 2005"),
 {"tipo":"checklist","t":n(25.4),"d":n(28.65)-n(25.4),"box":[120,260,840,400],"titulo":"Tinha na bolinha?","entra":"cai","itens":[{"txt":"colesterol","t":n(25.7)},{"txt":"cálcio","t":n(26.8)}],"z":40},
 {"tipo":"desenho","t":n(26.1),"d":n(28.65)-n(26.1),"formas":[{"k":"x","c":[262,412],"s":34}],"espessura":12,"cor":"#d61f2c","z":45},
 {"tipo":"desenho","t":n(27.2),"d":n(28.65)-n(27.2),"formas":[{"k":"x","c":[262,506],"s":34}],"espessura":12,"cor":"#d61f2c","z":45},
 T(n(27.6),n(28.65)-n(27.6)+0.5,"PEDRA É FEITA DISSO",y=860,f="90px Anton",cor="#ffffff",anim=None,entra="zoom",css="text-shadow:6px 6px 0 #000"),
 {"tipo":"flash","t":n(28.7),"d":0.2,"max":0.5},
 T(n(28.72),n(31.3)-n(28.72),"75% ERA GORDURA",y=430,f="170px Anton",cor="#f2c230",anim=None,entra="zoom",css="text-shadow:8px 8px 0 #000"),
 T(n(31.36),n(33.0)-n(31.36),"10 MIN A 40 °C",y=430,f="150px Anton",vel=0.12),
 {"tipo":"gigante","t":n(31.4),"d":1.7,"txt":"DERRETEU","y":900,"tam":300,"cor":"#ff2d3d","x":[1000,-2400],"z":42},
 {"tipo":"carimbo","t":n(33.0),"d":n(34.8)-n(33.0),"xy":[170,700],"txt":"ERA SABÃO","tam":160,"rot":-8,"z":60}]
# ---- orientação ----
c+=[{"tipo":"flash","t":n(34.0),"d":0.2,"max":0.5},
 T(n(34.12),n(35.6)-n(34.12),"DOR DEPOIS DE GORDURA?",y=380,f="120px Anton",vel=0.11),
 T(n(35.6),n(37.8)-n(35.6),"MÉDICO E ULTRASSOM",y=380,f="130px Anton",cor="#3ddc84",css="text-shadow:8px 8px 0 #000"),
 T(n(36.82),n(37.8)-n(36.82),"NÃO AZEITE",y=760,f="130px Anton",cor="#ff2d3d",anim=None,entra="zoom",css="text-shadow:6px 6px 0 #000"),
 {"tipo":"flash","t":n(37.8),"d":0.2,"max":0.5},
 T(n(37.86),n(40.5)-n(37.86),"PEDRA DE VERDADE",y=380,f="130px Anton",vel=0.12),
 T(n(38.6),n(40.5)-n(38.6),"SE VÊ NO EXAME",y=640,f="130px Anton",cor="#3ddc84",vel=0.12,css="text-shadow:8px 8px 0 #000"),
 T(n(39.54),n(40.5)-n(39.54),"NÃO NO VASO",y=900,f="120px Anton",cor="#ff2d3d",anim=None,entra="zoom",css="text-shadow:6px 6px 0 #000")]
# ---- CTA do banco (6cd9) ----
c+=[{"tipo":"glitch","t":cta-0.05,"d":0.25},
 {"tipo":"video","t":cta,"d":round(dur-cta,2),"ms":0,"src":M+"fig_cta.mp4","box":[0,0,1080,1920],"pos":"center 30%","zoom":[[cta,1.0,0.01],[cta+2.0,1.08,1.5]],"z":40},
 {"tipo":"barra","t":cta+0.2,"d":dur-cta-0.3,"y":215,"txt":"VALEU A AULA? SEGUE + CURTE","cor":"#c6ff3d","cor_txt":"#0b1512"},
 {"tipo":"texto","t":cta+0.3,"d":dur-cta-0.4,"xy":[60,370],"w":960,"fonte":"600 28px Montserrat","cor":"#ffffff","alinha":"center",
  "txt":"Sies & Brooker, The Lancet 2005 · doi 10.1016/S0140-6736(05)66373-8","css":"text-shadow:0 2px 6px #000","z":70}]
voz=[{"src":V,"t":0.0,"ms":67.60,"d":1.65,"palavras":M+"fig_viral.words.json"},
     {"src":V,"t":1.65,"ms":0.0,"d":2.55,"palavras":M+"fig_viral.words.json"},
     {"src":V,"t":4.20,"ms":3.00,"d":5.55,"gain":0.16},
     {"src":M+"fig_ctx_voz.wav","t":4.30,"ms":0,"d":5.35,"palavras":M+"fig_ctx_voz.words.json"},
     {"src":V,"t":9.75,"ms":51.30,"d":4.00,"palavras":M+"fig_viral.words.json"},
     {"src":M+"fig2_voz.wav","t":vd,"ms":0,"d":4.35,"palavras":M+"fig2_voz.words.json"},
     {"src":M+"fig2_voz.wav","t":r1,"ms":4.40,"d":round(40.33-4.40,2),"palavras":M+"fig2_voz.words.json"},
     {"src":M+"fig_cta.mp4","t":cta,"ms":0,"d":4.12,"palavras":M+"fig_cta.mp4.words.json"}]
sfx=[{"src":"whoosh","t":0,"gain":0.6,"pico":0.45},{"src":"notif","t":0.15,"gain":0.5},{"src":"whoosh2","t":1.65,"gain":0.35},{"src":"boing","t":3.4,"gain":0.4},
 {"src":"whoosh2","t":4.2,"gain":0.35},{"src":"whoosh2","t":9.75,"gain":0.35},{"src":"glitch","t":vd-0.05,"gain":0.5},
 {"src":"boom","t":vd+1.75,"gain":0.5,"pico":0.3,"d":1.2},{"src":"glitch","t":r1-0.05,"gain":0.5},{"src":"whoosh","t":r1+0.05,"gain":0.45,"pico":0.45},
 {"src":"riser","t":n(6.6),"gain":0.25,"pico":1.0,"d":1.2},{"src":"whoosh2","t":n(10.6),"gain":0.4},{"src":"whoosh2","t":n(14.2),"gain":0.35},
 {"src":"boing","t":n(17.2),"gain":0.35},{"src":"whoosh2","t":n(18.3),"gain":0.35},{"src":"whoosh","t":n(20.3),"gain":0.4,"pico":0.45},
 {"src":"glitch","t":n(21.7),"gain":0.4},{"src":"papel","t":n(25.4),"gain":0.5},{"src":"boing","t":n(26.1),"gain":0.3},{"src":"boing","t":n(27.2),"gain":0.3},
 {"src":"boom","t":n(28.72),"gain":0.6,"pico":0.3,"d":1.5},{"src":"whoosh","t":n(31.4),"gain":0.5,"pico":0.45},{"src":"boom","t":n(33.0),"gain":0.7,"pico":0.3,"d":1.5},
 {"src":"whoosh2","t":n(34.0),"gain":0.4},{"src":"boing","t":n(36.82),"gain":0.35},{"src":"whoosh2","t":n(37.8),"gain":0.4},{"src":"boom","t":n(39.54),"gain":0.5,"pico":0.3,"d":1.2},
 {"src":"glitch","t":cta-0.05,"gain":0.5},{"src":"notif","t":cta+0.2,"gain":0.4}]
salvar(PID,dur,127,c,voz,sfx,{"r1_fim":r1,"esconde":[[0,4.2]],"ys":[[4.2,vd,1400],[vd,r1,1000]]})
subprocess.run(["python3","scripts/pele.py",PID,"lousa"],check=True)
p=json.load(open(f'planos/{PID}.json'))
for L in p['camadas']:   # b-roll da aula: véu mais leve que o da lousa para o vídeo aparecer
    if L.get('tipo')=='fundo' and L.get('cor')=='rgba(28,50,40,.7)': L['cor']='rgba(16,30,24,.55)'
json.dump(p,open(f'planos/{PID}.json','w'),ensure_ascii=False,indent=1)
subprocess.run(["python3","scripts/entrada.py",PID,M+"fig_ent.mp4",M+"fig_ent.mp4.words.json","1.88",
                "“LIMPEZA DO FÍGADO” SOLTA PEDRAS?","o vídeo passou de 2,8 milhões de views","Plantão das Redes"],check=True)
print("ok vd",vd,"r1",r1,"cta",cta,"dur",dur)
