import json
M='assets/midia/'
def B(src,t,d,ms):
    z=[[t,1.0,0.01]]; k=t+0.35; big=True
    while k<t+d-0.4:
        z.append([round(k,2),1.16 if big else 1.02,0.5]); big=not big; k+=1.05
    return [{"tipo":"video","t":t,"d":round(d,2),"ms":ms,"src":M+src,"box":[0,0,1080,1920],"pos":"center","respira":False,"z":10,"zoom":z},
            {"tipo":"fundo","t":t,"d":round(d,2),"cor":"rgba(6,14,11,.5)","z":11}]
def T(t,d,txt,y=560,f="150px Anton",cor="#ffffff",**k):
    c={"tipo":"texto","t":round(t,2),"d":round(d,2),"xy":[40,y],"w":1000,"fonte":f,"cor":cor,"alinha":"center","txt":txt,"z":40,"anim":"palavras","vel":0.11}
    c.update(k)
    if c.get("anim") is None: c.pop("anim")
    return c
def F(t,d,txt):
    return {"tipo":"texto","t":round(t,2),"d":round(d,2),"xy":[40,215],"w":1000,"fonte":"600 28px Montserrat","cor":"#ffffff","alinha":"center","txt":txt,"z":70,"css":"text-shadow:0 2px 6px #000"}
def abertura(pfx,vdur,arroba,pos,topo,perg,meio,still_pos=None):
    return [
     {"tipo":"cartao","t":0,"d":None,"box":[40,150,1000,990],"aba":"o viral","entra":"whip"},
     {"tipo":"video","t":0,"d":vdur,"ms":0,"src":M+pfx+"_viral.mp4","box":[70,190,940,909],"raio":14,"pos":pos,"arroba":arroba,"respira":False,"zoom":[[0,1.0,0.01],[4.0,1.06,0.4],[vdur-2.5,1.0,0.4]],"z":30},
     {"tipo":"pergunta","t":0.1,"d":3.95,"xy":[110,1150],"w":790,"topo":topo,"txt":perg,"botoes":["MITO","VERDADE"],"vel":0.025,"escolha":0,"t_escolha":3.3},
    ]+meio+[
     {"tipo":"glitch","t":vdur-0.05,"d":0.25},
     {"tipo":"foto","t":vdur,"d":None,"src":M+pfx+"_still.jpg","box":[70,190,940,909],"raio":14,"sombra":False,"z":29}]
def rosto_r1(pfx,t,d,ms=0):
    return {"tipo":"video","t":t,"d":d,"ms":ms,"src":M+pfx+"_rosto.mp4","box":[0,1140,1080,780],"pos":"center 30%","entra":"desliza","z":45}
def rosto_r2(pfx,t,d,ms):
    return [{"tipo":"glitch","t":t-0.05,"d":0.25},
     {"tipo":"video","t":t,"d":d,"ms":ms,"src":M+pfx+"_rosto.mp4","box":[0,0,1080,1920],"pos":"center 30%","zoom":[[t,1.0,0.01],[t+2.6,1.1,0.3]],"z":40},
     {"tipo":"barra","t":t+0.2,"d":d-0.25,"y":215,"txt":"COMBINADO: SEGUE + CURTE","cor":"#c6ff3d","cor_txt":"#0b1512"}]
def fim():
    return [{"tipo":"progresso"},{"tipo":"vinheta"},{"tipo":"grao","op":0.07}]
def salvar(pid,dur,seed,camadas,voz,sfx,ys):
    for c in camadas:
        if c.get("d") is None and c.get("tipo") in ("cartao",): c["d"]=ys["r1_fim"]
        if c.get("d") is None and c.get("tipo")=="foto": c["d"]=round(ys["r1_fim"]-c["t"],2)
    p={"id":pid,"dur":dur,"seed":seed,"fundo":"#0b1512",
       "legenda":{"estilo":"lima","y":1340,"esconde":ys["esconde"],"ys":ys["ys"]},
       "camera":{"amp":1.0},"audio":{"voz":voz,"musica":[],"sfx":sfx},
       "camadas":[{"tipo":"fundo","t":0,"d":dur,"cor":"#0b1512","textura":"grade"}]+camadas+fim()}
    json.dump(p,open(f'planos/{pid}.json','w'),ensure_ascii=False,indent=1)
