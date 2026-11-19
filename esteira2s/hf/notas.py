#!/usr/bin/env python3
"""Edição NOTAS (HyperFrames): a lista é digitada no bloco de notas do celular.

Uso: python esteira2s/hf/notas.py bruto.mp4 words.json plano_notas.json projeto_dir saida.mp4

- bruto.mp4 vem do montar_bruto.py (clipes de rosto + narração); os trechos estão em bruto.mp4.trechos.json.
- words.json vem do reel_kit/diario/transcrever.py ({w, s, e} por palavra).
- plano_notas.json:
  {"arroba":"@conta","marca":"NOME","aviso":["Nova nota","título curto"],"titulo":["linha 1","linha 2"],
   "itens":[{"quando":"primeiras palavras da fala","texto":"até 30 letras"}],
   "cartao":{"quando":"...","topo":"O ITEM MAIS","meio":"IMPORTANTE:","base":"ELE",
             "linhas":[{"quando":"...","rotulo":"OS DOIS","valor":"JUNTOS"}]},
   "seguir":"curte + segue","fim":{"frase":"...","ref":"..."},"trilha":"moment_of_peace"}
Linguagem "notas" na trava da mesmice. Rosto aparece em tela cheia nos trechos de rosto.
"""
import html, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
KIT = AQUI.parent.parent / "reel_kit"
FIM_S = 2.6


def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    return re.sub(r"[^a-z0-9 ]", "", "".join(c for c in t if unicodedata.category(c) != "Mn"))


def achar(words: list[dict], frase: str, desde: float = 0.0) -> float:
    alvo = norm(frase).split()
    ws = [norm(w["w"]) for w in words]
    for i in range(len(ws) - len(alvo) + 1):
        if words[i]["s"] >= desde and ws[i:i + len(alvo)] == alvo:
            return words[i]["s"]
    raise SystemExit(f"não achei na fala: {frase!r}")


def blocos(words: list[dict], trechos: list[dict], n: int = 4) -> list[dict]:
    """Legenda em blocos de até n palavras, sem atravessar a troca rosto/voz nem ponto final."""
    out, atual = [], []
    def tipo(t):
        return next((x["tipo"] for x in trechos if x["t0"] <= t < x["t1"]), trechos[-1]["tipo"])
    for w in words:
        if atual and (len(atual) >= n or tipo(w["s"]) != tipo(atual[0]["s"]) or atual[-1]["w"][-1:] in ".?!"):
            out.append(atual); atual = []
        atual.append(w)
    if atual:
        out.append(atual)
    res = []
    for i, b in enumerate(out):
        fim = out[i + 1][0]["s"] if i + 1 < len(out) else b[-1]["e"] + 0.3
        res.append({"t0": b[0]["s"], "t1": fim, "txt": " ".join(x["w"] for x in b), "tipo": tipo(b[0]["s"])})
    return res


def main() -> None:
    bruto, wj, pj, proj, saida = map(Path, sys.argv[1:6])
    words = json.loads(wj.read_text())
    plano = json.loads(pj.read_text())
    trechos = json.loads(Path(str(bruto) + ".trechos.json").read_text())
    dur = trechos[-1]["t1"]
    total = round(dur + FIM_S, 2)
    (proj / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(bruto, proj / "assets" / "bruto.mp4")
    for f in (AQUI / "fontes").glob("*.woff2"):
        shutil.copy(f, proj / "assets" / f.name)
    (proj / "hyperframes.json").write_text(json.dumps({"name": proj.name}))

    itens = []
    desde = 0.0
    for it in plano["itens"]:
        t = achar(words, it["quando"], desde); desde = t
        itens.append({"t": round(t, 2), "texto": it["texto"]})
    c = plano["cartao"]
    c_t = round(achar(words, c["quando"], desde), 2)
    linhas = [{"t": round(achar(words, l["quando"], c_t), 2), **l} for l in c["linhas"]]
    rostos = [x for x in trechos if x["tipo"] == "rosto"]
    seg = rostos[1] if len(rostos) > 2 else None
    dados = {"itens": itens, "cartaoT": c_t, "linhas": linhas, "rostos": rostos, "dur": dur, "total": total,
             "blocos": blocos(words, trechos), "seg": seg, "primVoz": rostos[0]["t1"]}
    e = html.escape
    li = "\n".join(
        f'<div class="it" id="it{i}"><span class="bx" id="bx{i}"><i id="ck{i}">✓</i></span>'
        f'<span class="tx" id="tx{i}">{e(x["texto"])}</span><b class="car" id="car{i}"></b></div>'
        for i, x in enumerate(itens))
    rows = "\n".join(
        f'<div class="row" id="row{i}"><span class="rl">{e(l["rotulo"])}</span><span class="rv">{e(l["valor"])}</span>'
        f'<span class="rc" id="rc{i}">✓</span></div>' for i, l in enumerate(linhas))
    caps = "\n".join(
        f'<span class="cap {b["tipo"]}" id="cap{i}">{e(b["txt"])}</span>' for i, b in enumerate(dados["blocos"]))
    teclas = "".join(
        '<div class="kr">' + "".join(f'<span class="k" id="k_{ch}">{ch}</span>' for ch in fila) + "</div>"
        for fila in ("qwertyuiop", "asdfghjkl", "zxcvbnm"))
    doc = MOLDE
    for k, v in {"__TOTAL__": str(total), "__DUR__": str(round(dur, 2)), "__AVISO1__": e(plano["aviso"][0]),
                 "__AVISO2__": e(plano["aviso"][1]), "__T1__": e(plano["titulo"][0]), "__T2__": e(plano["titulo"][1]),
                 "__ITENS__": li, "__TOPO__": e(c["topo"]), "__MEIO__": e(c["meio"]), "__BASE__": e(c["base"]),
                 "__ROWS__": rows, "__CAPS__": caps, "__TECLAS__": teclas, "__SEGUIR__": e(plano.get("seguir", "curte + segue")),
                 "__ARROBA__": e(plano["arroba"]), "__MARCA__": e(plano["marca"]), "__FIMFRASE__": e(plano["fim"]["frase"]),
                 "__FIMREF__": e(plano["fim"]["ref"]).replace("\n", "<br>"),
                 "__DADOS__": json.dumps(dados, ensure_ascii=False)}.items():
        doc = doc.replace(k, v)
    (proj / "index.html").write_text(doc, encoding="utf-8")
    mudo = proj / "render.mp4"
    subprocess.run(["npx", "hyperframes", "render", "--quality", "looks", "-o", str(mudo)], cwd=proj, check=True)
    trilha = KIT / "trilhas" / f'{plano.get("trilha", "moment_of_peace")}.m4a'
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mudo), "-stream_loop", "-1", "-i", str(trilha),
                    "-filter_complex",
                    f"[0:a]apad[v];[1:a]volume=0.10,afade=t=out:st={total - 1.2}:d=1.2[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-t", str(total), "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(saida)], check=True)
    print(f"NOTAS OK: {saida} ({total} s)")


MOLDE = r"""<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{font-family:"Permanent Marker";src:url("assets/permanent-marker-400.woff2") format("woff2")}
@font-face{font-family:"Courier Prime";src:url("assets/courier-prime-700.woff2") format("woff2");font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Inter,sans-serif}
#root{position:relative;width:1080px;height:1920px;overflow:hidden}
#v{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;z-index:1}
#app,#capsRosto,#aviso,#adesivo,#papel,#fim{position:absolute;inset:0}
#app{z-index:2}#appIn{position:absolute;inset:0;background:#fff}
.st{position:absolute;top:96px;left:70px;right:70px;display:flex;justify-content:space-between;font-weight:700;font-size:38px;color:#111}
.nav{position:absolute;top:186px;left:52px;right:52px;display:flex;justify-content:space-between;align-items:center}
.rd{width:104px;height:104px;border-radius:52px;background:#fff;box-shadow:0 4px 18px rgba(0,0,0,.12);display:grid;place-items:center;font-size:52px;color:#111}
.ok{background:#fbc71d;color:#fff;font-weight:900}
h1{position:absolute;top:340px;left:70px;right:60px;font-size:84px;line-height:1.08;font-weight:900;letter-spacing:-.02em;color:#111}
#lista{position:absolute;top:570px;left:70px;right:40px}
.it{position:relative;display:flex;align-items:center;height:108px;white-space:nowrap}
.bx{width:58px;height:58px;border:4px solid #c6c9cf;border-radius:29px;margin-right:26px;display:grid;place-items:center;flex:none}
.bx i{font-style:normal;font-weight:900;font-size:36px;color:#fff}
.tx{font-size:60px;font-weight:400;color:#111;letter-spacing:-.01em}
.car{position:absolute;left:84px;top:18px;width:6px;height:72px;background:#fbc71d;border-radius:3px}
#kb{position:absolute;left:0;right:0;top:1130px;bottom:0;background:#cfd3da}
#sug{position:absolute;left:0;right:0;top:0;height:150px;display:grid;place-items:center;border-bottom:2px solid #bcc1c9}
.cap{position:absolute;opacity:0;white-space:nowrap}
.cap.voz{font-size:58px;font-weight:700;color:#111;left:0;right:0;text-align:center;top:38px}
.kr{display:flex;justify-content:center;gap:12px;margin-top:22px}
#keys{position:absolute;top:160px;left:0;right:0}
.k{width:92px;height:118px;background:#fff;border-radius:14px;display:grid;place-items:center;font-size:52px;color:#111;box-shadow:0 2px 0 #9a9fa8}
#capsRosto{z-index:3;pointer-events:none}
.cap.rosto{left:60px;right:60px;top:1180px;text-align:center;font-size:74px;font-weight:900;color:#fff;white-space:normal;text-shadow:0 4px 18px rgba(0,0,0,.85),0 0 4px #000}
#aviso{z-index:4}#avisoIn{position:absolute;left:44px;right:44px;top:190px;background:rgba(250,250,252,.96);border-radius:44px;padding:34px 40px;display:flex;gap:30px;align-items:center;box-shadow:0 18px 50px rgba(0,0,0,.35)}
.ic{width:112px;height:112px;border-radius:26px;background:linear-gradient(#ffe46b,#fbc71d);display:grid;place-items:center;font-size:66px;flex:none}
.a1{font-size:36px;font-weight:700;color:#6b7078}.a2{font-size:52px;font-weight:900;color:#111;line-height:1.1}
#adesivo{z-index:4}#adIn{position:absolute;left:50%;top:330px;white-space:nowrap;background:#fbc71d;color:#111;border-radius:60px;padding:26px 54px;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.4)}
.s1{font-size:64px;font-weight:900}.s2{font-size:40px;font-weight:700}
#papel{z-index:2}#papelIn{position:absolute;inset:0;background:#ece2d5}
#folha{position:absolute;left:80px;right:80px;top:230px;height:1200px;background:#fdfcfa;box-shadow:0 30px 70px rgba(60,30,20,.28);padding:90px 70px;text-align:center}
.mk{font-family:"Permanent Marker";color:#5a1f3d;line-height:1.02}
#mk1{font-size:116px}#mk2{font-size:100px;margin-top:8px}
#mk3w{position:relative;display:inline-block;margin-top:26px;padding:10px 60px}#mk3{font-size:230px}
#anel{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.row{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:4px solid #5a1f3d;padding:0 6px 16px;margin-top:92px}
.rl{font-family:"Courier Prime";font-weight:700;font-size:50px;color:#5a1f3d}
.rv{font-family:"Permanent Marker";font-size:78px;color:#5a1f3d}.rc{font-family:"Permanent Marker";font-size:66px;color:#5a1f3d}
#fim{z-index:5}#fimIn{position:absolute;inset:0;background:#ece2d5;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 110px;text-align:center}
#fm{font-family:"Courier Prime";font-weight:700;font-size:46px;letter-spacing:.2em;color:#5a1f3d}
#ff{font-family:"Permanent Marker";font-size:104px;line-height:1.08;color:#5a1f3d;margin:50px 0}
#fr{font-family:"Courier Prime";font-weight:700;font-size:40px;line-height:1.4;color:#7a5868}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__TOTAL__" data-width="1080" data-height="1920" data-fps="30">
<video id="v" class="clip" src="assets/bruto.mp4" data-start="0" data-duration="__DUR__" data-track-index="0" data-has-audio="true"></video>
<div id="app" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="1" data-track-kind="graphics"><div id="appIn">
 <div class="st"><span>9:41</span><span>●●● ▂▄▆ ▮</span></div>
 <div class="nav"><span class="rd">‹</span><span class="rd ok">✓</span></div>
 <h1><span id="h1a">__T1__</span><br><span id="h1b">__T2__</span></h1>
 <div id="lista">__ITENS__</div>
 <div id="kb"><div id="sug">__CAPS__</div><div id="keys">__TECLAS__</div></div>
</div></div>
<div id="papel" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="2" data-track-kind="graphics"><div id="papelIn">
 <div id="folha"><div class="mk" id="mk1">__TOPO__</div><div class="mk" id="mk2">__MEIO__</div>
 <div id="mk3w"><div class="mk" id="mk3">__BASE__</div><svg id="anel" viewBox="0 0 100 100" preserveAspectRatio="none"><ellipse id="el" cx="50" cy="52" rx="49" ry="44" fill="none" stroke="#5a1f3d" stroke-width="2.2" vector-effect="non-scaling-stroke" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100" transform="rotate(-4 50 50)"/></svg></div>
 __ROWS__</div></div></div>
<div id="capsRosto" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="3" data-track-kind="captions"></div>
<div id="aviso" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="4" data-track-kind="graphics"><div id="avisoIn"><span class="ic">📝</span><div><div class="a1">__AVISO1__</div><div class="a2">__AVISO2__</div></div></div></div>
<div id="adesivo" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="5" data-track-kind="graphics"><div id="adIn"><div class="s1">__SEGUIR__</div><div class="s2">__ARROBA__</div></div></div>
<div id="fim" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="6" data-track-kind="graphics"><div id="fimIn"><div id="fm">__MARCA__</div><div id="ff">__FIMFRASE__</div><div id="fr">__FIMREF__</div></div></div>
</div>
<script>
const D=__DADOS__;
const tl=gsap.timeline({paused:true});
const $=s=>document.querySelector(s);
// legendas de rosto vão para a camada por cima do vídeo
document.querySelectorAll('.cap.rosto').forEach(c=>$('#capsRosto').appendChild(c));
D.blocos.forEach((b,i)=>{tl.set('#cap'+i,{opacity:1},b.t0);tl.set('#cap'+i,{opacity:0},b.t1);});
// camadas: rosto (vídeo) x notas x papel
gsap.set('#appIn',{opacity:0});gsap.set('#papelIn',{opacity:0});gsap.set('#fimIn',{opacity:0});
gsap.set('#avisoIn',{y:-420});gsap.set('#adIn',{xPercent:-50,scale:0});
const r=D.rostos;
tl.to('#avisoIn',{y:0,duration:.35,ease:'back.out(1.4)'},.12).to('#avisoIn',{y:-420,duration:.25,ease:'power2.in'},D.primVoz-.05);
tl.fromTo('#appIn',{opacity:0,scale:1.12},{opacity:1,scale:1,duration:.28,ease:'power3.out'},D.primVoz);
if(D.seg){tl.to('#appIn',{opacity:0,duration:.12},D.seg.t0);
 tl.to('#adIn',{scale:1,duration:.3,ease:'back.out(2)'},D.seg.t0+.25).to('#adIn',{scale:0,duration:.2},D.seg.t1-.2);
 tl.set('#papelIn',{opacity:1},D.seg.t1);}
else{tl.set('#appIn',{opacity:0},D.cartaoT);tl.set('#papelIn',{opacity:1},D.cartaoT);}
const ult=r[r.length-1];
tl.to('#papelIn',{opacity:0,duration:.12},ult.t0);
tl.to('#fimIn',{opacity:1,duration:.3},D.dur-.05);
tl.from('#ff',{y:40,opacity:0,duration:.4,ease:'power3.out'},D.dur+.1);
// título e itens digitados
gsap.set(['#h1a','#h1b'],{clipPath:'inset(0 100% 0 0)'});
tl.to('#h1a',{clipPath:'inset(0 0% 0 0)',duration:.45,ease:'steps(12)'},D.primVoz+.15).to('#h1b',{clipPath:'inset(0 0% 0 0)',duration:.4,ease:'steps(10)'},D.primVoz+.6);
const sem=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
D.itens.forEach((it,i)=>{
 const tx=$('#tx'+i),n=it.texto.length,w=tx.getBoundingClientRect().width,d=Math.min(1.7,n*.05);
 gsap.set('#it'+i,{opacity:0});gsap.set(tx,{clipPath:'inset(0 100% 0 0)'});gsap.set('#ck'+i,{scale:0});
 tl.set('#it'+i,{opacity:1},it.t);
 tl.to(tx,{clipPath:'inset(0 0% 0 0)',duration:d,ease:'steps('+n+')'},it.t+.05);
 tl.fromTo('#car'+i,{x:0},{x:w+6,duration:d,ease:'steps('+n+')'},it.t+.05);
 tl.set('#car'+i,{opacity:0},it.t+d+.35);
 tl.to('#bx'+i,{backgroundColor:'#fbc71d',borderColor:'#fbc71d',duration:.15},it.t+d+.1);
 tl.to('#ck'+i,{scale:1,duration:.25,ease:'back.out(3)'},it.t+d+.1);
 [...it.texto].forEach((ch,j)=>{const k=document.getElementById('k_'+sem(ch));if(!k)return;const t=it.t+.05+d*j/n;
  tl.to(k,{backgroundColor:'#9aa1ad',y:4,duration:.04},t).to(k,{backgroundColor:'#ffffff',y:0,duration:.08},t+.06);});
});
// cartão de papel
gsap.set(['#mk1','#mk2','#mk3'],{opacity:0,scale:1.5,rotation:-3});
const c=D.cartaoT;
tl.to('#mk1',{opacity:1,scale:1,rotation:-2,duration:.22,ease:'power4.out'},c+.05)
  .to('#mk2',{opacity:1,scale:1,rotation:1,duration:.22,ease:'power4.out'},c+.75)
  .to('#mk3',{opacity:1,scale:1,rotation:-2,duration:.25,ease:'back.out(2.5)'},c+2.0)
  .to('#el',{strokeDashoffset:0,duration:.5,ease:'power2.inOut'},c+2.25);
D.linhas.forEach((l,i)=>{gsap.set('#row'+i,{opacity:0,x:-60});gsap.set('#rc'+i,{scale:0});
 tl.to('#row'+i,{opacity:1,x:0,duration:.3,ease:'power3.out'},l.t).to('#rc'+i,{scale:1,duration:.25,ease:'back.out(3)'},l.t+.45);});
window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;
</script></body></html>"""

if __name__ == "__main__":
    main()
