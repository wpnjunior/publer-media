#!/usr/bin/env python3
"""Edição DOSSIÊ (HyperFrames): história contada como arquivo secreto aberto em cima da mesa.

Uso: python esteira2s/hf/dossie.py bruto.mp4 words.json plano_dossie.json projeto_dir saida.mp4

- bruto.mp4 vem do montar_bruto.py (rosto gerado no avatar padrão + narração só em áudio).
- words.json vem do reel_kit/diario/transcrever.py ({w, s, e} por palavra).
- plano_dossie.json:
  {"arroba":"@conta","marca":"NOME","pasta":"ARQUIVO MKULTRA","anos":"1953 a 1973","carimbo":"CONFIDENCIAL",
   "folhas":[{"quando":"primeiras palavras","tipo":"titulo|numero|ficha|lista","rotulo":"PROJETO",
              "texto":"MKULTRA","numero":"1953","sub":"...","linhas":["..."],"carimbo":"DESTRUÍDO"}],
   "fonte":"...","seguir":"curte + segue","fim":{"frase":"...","ref":"..."},"trilha":"dark_cinematic"}
Cada folha cai na pilha, o texto é batido à máquina e o carimbo bate por cima. Rosto em tela cheia nos
trechos de rosto, com a aba da pasta e o carimbo no gancho. Linguagem "dossie" na trava da mesmice.
"""
import html, json, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notas import achar, blocos, AQUI, KIT, FIM_S  # noqa: E402

ROT = [-3, 2.2, -1.4, 3, -2.2, 1.6, -2.8, 2.6]


def folha_html(i: int, f: dict) -> str:
    e = html.escape
    corpo = ""
    if f["tipo"] == "titulo":
        corpo = f'<div class="big tp" id="tp{i}_0">{e(f["texto"])}</div>'
        if f.get("sub"):
            corpo += f'<div class="sub tp" id="tp{i}_1">{e(f["sub"])}</div>'
    elif f["tipo"] == "numero":
        corpo = f'<div class="num" id="nm{i}">{e(f["numero"])}</div><div class="sub tp" id="tp{i}_0">{e(f.get("sub", ""))}</div>'
    else:
        marca = "— " if f["tipo"] == "lista" else ""
        corpo = "".join(f'<div class="ln tp" id="tp{i}_{j}">{marca}{e(x)}</div>' for j, x in enumerate(f["linhas"]))
    larg = [92, 64, 80, 48]
    nt = 2 if f.get("carimbo") or f["tipo"] != "titulo" and f["tipo"] != "numero" and len(f.get("linhas", [])) > 2 else 4
    if f["tipo"] == "numero":
        nt = 0 if f.get("carimbo") else 2
    corpo += '<div class="tj">' + "".join(
        f'<i id="tj{i}_{j}" style="width:{larg[(i + j) % 4]}%"></i>' for j in range(nt)) + "</div>"
    carimbo = f'<div class="stamp" id="st{i}">{e(f["carimbo"])}</div>' if f.get("carimbo") else ""
    return (f'<div class="sheet" id="sh{i}"><div class="hd"><span>Nº {i + 1:03d}</span><span>SIGILOSO</span></div>'
            f'<div class="rt">{e(f.get("rotulo", ""))}</div><div class="bd">{corpo}</div>{carimbo}</div>')


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

    folhas, desde = [], 0.0
    for f in plano["folhas"]:
        t = achar(words, f["quando"], desde); desde = t
        n = 2 if f["tipo"] == "titulo" and f.get("sub") else (1 if f["tipo"] in ("titulo", "numero") else len(f["linhas"]))
        folhas.append({"t": round(t, 2), "tipo": f["tipo"], "n": n, "carimbo": bool(f.get("carimbo"))})
    rostos = [x for x in trechos if x["tipo"] == "rosto"]
    vozes = [x for x in trechos if x["tipo"] != "rosto"]
    dados = {"folhas": folhas, "rostos": rostos, "vozes": vozes, "dur": dur, "total": total,
             "blocos": blocos(words, trechos), "seg": rostos[1] if len(rostos) > 2 else None, "rot": ROT,
             "tst": round(achar(words, plano["carimbo_quando"]), 2) if plano.get("carimbo_quando") else None}
    e = html.escape
    caps = "\n".join(f'<span class="cap {b["tipo"]}" id="cap{i}">{e(b["txt"])}</span>' for i, b in enumerate(dados["blocos"]))
    doc = MOLDE
    for k, v in {"__TOTAL__": str(total), "__DUR__": str(round(dur, 2)),
                 "__SHEETS__": "\n".join(folha_html(i, f) for i, f in enumerate(plano["folhas"])),
                 "__CAPS__": caps, "__PASTA__": e(plano["pasta"]), "__GANCHO__": e(plano.get("gancho", plano["pasta"])), "__ANOS__": e(plano["anos"]),
                 "__CARIMBO__": e(plano.get("carimbo", "CONFIDENCIAL")), "__FONTE__": e(plano.get("fonte", "")),
                 "__SEGUIR__": e(plano.get("seguir", "curte + segue")), "__ARROBA__": e(plano["arroba"]),
                 "__MARCA__": e(plano["marca"]), "__FIMFRASE__": e(plano["fim"]["frase"]),
                 "__FIMREF__": e(plano["fim"]["ref"]).replace("\n", "<br>"),
                 "__DADOS__": json.dumps(dados, ensure_ascii=False)}.items():
        doc = doc.replace(k, v)
    (proj / "index.html").write_text(doc, encoding="utf-8")
    mudo = proj / "render.mp4"
    subprocess.run(["npx", "hyperframes", "render", "--quality", "looks", "-o", str(mudo)], cwd=proj, check=True)
    trilha = KIT / "trilhas" / f'{plano.get("trilha", "dark_cinematic")}.m4a'
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mudo), "-stream_loop", "-1", "-i", str(trilha),
                    "-filter_complex",
                    f"[0:a]apad[v];[1:a]volume=0.10,afade=t=out:st={total - 1.2}:d=1.2[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-t", str(total), "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(saida)], check=True)
    print(f"DOSSIE OK: {saida} ({total} s)")


MOLDE = r"""<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{font-family:"Permanent Marker";src:url("assets/permanent-marker-400.woff2") format("woff2")}
@font-face{font-family:"Courier Prime";src:url("assets/courier-prime-700.woff2") format("woff2");font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:"Courier Prime",monospace;font-weight:700}
#root{position:relative;width:1080px;height:1920px;overflow:hidden}
#v{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;z-index:1}
#mesa,#capsRosto,#gancho,#adesivo,#fim{position:absolute;inset:0}
#mesa{z-index:2}
#mesaIn{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 38%,#4a3a2a 0%,#2a2018 62%,#17110c 100%)}
#pastaF{position:absolute;left:40px;right:40px;top:150px;height:1330px;background:#c9a56a;border-radius:10px 26px 14px 14px;box-shadow:0 40px 90px rgba(0,0,0,.6)}
#abaF{position:absolute;left:40px;top:86px;width:560px;height:80px;background:#c9a56a;border-radius:18px 18px 0 0;padding:20px 30px;font-size:34px;letter-spacing:.08em;color:#4a3414;white-space:nowrap}
#anosF{position:absolute;right:70px;top:100px;font-size:36px;color:#e6d2ac;letter-spacing:.1em}
.sheet{position:absolute;left:96px;right:96px;top:250px;height:1100px;background:#f4eedf;box-shadow:0 18px 40px rgba(0,0,0,.4);padding:54px 60px;color:#1d1a16}
.hd{display:flex;justify-content:space-between;font-size:30px;letter-spacing:.14em;color:#7c6a55;border-bottom:3px solid #1d1a16;padding-bottom:18px}
.rt{margin-top:56px;display:inline-block;background:#1d1a16;color:#f4eedf;font-size:40px;letter-spacing:.14em;padding:10px 22px}
.bd{margin-top:70px}
.tj{margin-top:70px}.tj i{display:block;height:36px;margin-bottom:30px;background:#1d1a16;transform-origin:left center}
.tj b{display:block;height:6px;margin-bottom:60px;background:#b9ad97}
.tp{white-space:nowrap}
.big{font-size:150px;line-height:1.05;letter-spacing:-.01em}
.sub{font-size:60px;line-height:1.25;margin-top:34px;color:#4b4238;white-space:normal}
.num{font-family:"Permanent Marker";font-weight:400;font-size:400px;line-height:1;color:#a11d1d}
.ln{font-size:58px;line-height:1.9}
.stamp{position:absolute;right:50px;bottom:36px;font-family:"Permanent Marker";font-weight:400;font-size:112px;color:#b01818;border:10px solid #b01818;border-radius:14px;padding:6px 34px;white-space:nowrap}
#fonteF{position:absolute;left:60px;right:60px;top:1500px;text-align:center;font-size:28px;letter-spacing:.06em;color:#bfae93}
#faixa{position:absolute;left:0;right:0;top:1560px;height:150px;display:grid;place-items:center}
.cap{position:absolute;opacity:0;white-space:nowrap}
.cap.voz{left:0;right:0;top:46px;text-align:center;font-size:50px;color:#f4eedf}
#capsRosto{z-index:3;pointer-events:none}
.cap.rosto{left:60px;right:60px;top:1190px;text-align:center;font-family:Inter,sans-serif;font-size:74px;font-weight:900;color:#fff;white-space:normal;text-shadow:0 4px 18px rgba(0,0,0,.85),0 0 4px #000}
#gancho{z-index:4}
#gAba{position:absolute;left:0;top:170px;background:#c9a56a;color:#3a2810;font-size:48px;letter-spacing:.08em;padding:22px 44px 22px 60px;border-radius:0 18px 18px 0;white-space:nowrap;box-shadow:0 12px 30px rgba(0,0,0,.45)}
#gAnos{position:absolute;left:0;top:290px;background:#1d1a16;color:#f4eedf;font-size:40px;letter-spacing:.12em;padding:14px 36px 14px 60px;border-radius:0 14px 14px 0;white-space:nowrap}
#gSt{position:absolute;left:50%;top:1420px;font-family:"Permanent Marker";font-weight:400;font-size:126px;color:#e02626;border:12px solid #e02626;border-radius:16px;padding:4px 40px;white-space:nowrap;background:rgba(20,10,10,.35)}
#adesivo{z-index:4}#adIn{position:absolute;left:50%;top:330px;white-space:nowrap;background:#f4eedf;color:#1d1a16;border:6px solid #1d1a16;padding:22px 50px;text-align:center;box-shadow:10px 10px 0 rgba(0,0,0,.45);font-family:Inter,sans-serif}
.s1{font-size:64px;font-weight:900}.s2{font-size:40px;font-weight:700}
#fim{z-index:5}#fimIn{position:absolute;inset:0;background:#f4eedf;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 100px;text-align:center}
#fm{font-size:44px;letter-spacing:.2em;color:#7c6a55}
#ff{font-family:"Permanent Marker";font-weight:400;font-size:104px;line-height:1.1;color:#a11d1d;margin:54px 0}
#fr{font-size:36px;line-height:1.45;color:#4b4238}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__TOTAL__" data-width="1080" data-height="1920" data-fps="30">
<video id="v" class="clip" src="assets/bruto.mp4" data-start="0" data-duration="__DUR__" data-track-index="0" data-has-audio="true"></video>
<div id="mesa" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="1" data-track-kind="graphics"><div id="mesaIn">
 <div id="abaF">__PASTA__</div><div id="anosF">__ANOS__</div><div id="pastaF"></div>
 __SHEETS__
 <div id="fonteF">FONTE: __FONTE__</div>
 <div id="faixa">__CAPS__</div>
</div></div>
<div id="capsRosto" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="2" data-track-kind="captions"></div>
<div id="gancho" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="3" data-track-kind="graphics"><div id="gAba">__GANCHO__</div><div id="gAnos">__ANOS__</div><div id="gSt">__CARIMBO__</div></div>
<div id="adesivo" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="4" data-track-kind="graphics"><div id="adIn"><div class="s1">__SEGUIR__</div><div class="s2">__ARROBA__</div></div></div>
<div id="fim" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="5" data-track-kind="graphics"><div id="fimIn"><div id="fm">__MARCA__</div><div id="ff">__FIMFRASE__</div><div id="fr">__FIMREF__</div></div></div>
</div>
<script>
const D=__DADOS__;
const tl=gsap.timeline({paused:true});
const $=s=>document.querySelector(s);
document.querySelectorAll('.cap.rosto').forEach(c=>$('#capsRosto').appendChild(c));
D.blocos.forEach((b,i)=>{tl.set('#cap'+i,{opacity:1},b.t0);tl.set('#cap'+i,{opacity:0},b.t1);});
// mesa só aparece na narração
gsap.set('#mesaIn',{opacity:0});gsap.set('#fimIn',{opacity:0});gsap.set('#adIn',{xPercent:-50,scale:0});
D.vozes.forEach(v=>{tl.fromTo('#mesaIn',{opacity:0,scale:1.08},{opacity:1,scale:1,duration:.25,ease:'power3.out'},v.t0);tl.to('#mesaIn',{opacity:0,duration:.12},v.t1-.06);});
// gancho: aba da pasta, anos e carimbo batendo sobre o rosto
const g0=D.rostos[0];
gsap.set('#gAba',{x:-900});gsap.set('#gAnos',{x:-900});gsap.set('#gSt',{xPercent:-50,scale:3,opacity:0,rotation:-9});
tl.to('#gAba',{x:0,duration:.3,ease:'power4.out'},.08).to('#gAnos',{x:0,duration:.3,ease:'power4.out'},.3)
  .to('#gSt',{scale:1,opacity:1,duration:.16,ease:'power4.in'},D.tst||Math.max(.9,g0.t1-2.4))
  .to('#gSt',{x:'+=8',duration:.04,yoyo:true,repeat:3},(D.tst||Math.max(.9,g0.t1-2.4))+.16)
  .to(['#gAba','#gAnos','#gSt'],{opacity:0,duration:.12},g0.t1-.1);
if(D.seg){tl.to('#adIn',{scale:1,duration:.3,ease:'back.out(2)'},D.seg.t0+.2).to('#adIn',{scale:0,duration:.2},D.seg.t1-.2);}
// folhas: caem na pilha, texto batido à máquina, carimbo
D.folhas.forEach((f,i)=>{
 const sh='#sh'+i,r=D.rot[i%D.rot.length];
 gsap.set(sh,{opacity:0,y:-260,scale:1.18,rotation:r*2.2});
 tl.to(sh,{opacity:1,y:0,scale:1,rotation:r,duration:.3,ease:'power4.out'},f.t);
 if(i>0)tl.to('#sh'+(i-1),{filter:'brightness(.72)',duration:.2},f.t);
 let t=f.t+.28;
 if(f.tipo==='numero'){gsap.set('#nm'+i,{scale:2.2,opacity:0});tl.to('#nm'+i,{scale:1,opacity:1,duration:.2,ease:'power4.in'},t);t+=.5;}
 for(let j=0;j<(f.tipo==='numero'?1:f.n);j++){const el=document.getElementById('tp'+i+'_'+j);if(!el)continue;
  const n=Math.max(4,el.textContent.length),d=Math.min(1.1,n*.045);
  gsap.set(el,{clipPath:'inset(0 100% 0 0)'});
  tl.to(el,{clipPath:'inset(0 0% 0 0)',duration:d,ease:'steps('+n+')'},t);t+=d+.18;}
 document.querySelectorAll('#sh'+i+' .tj i').forEach(b=>{gsap.set(b,{scaleX:0});tl.to(b,{scaleX:1,duration:.22,ease:'power3.out'},t);t+=.16;});
 if(f.carimbo){gsap.set('#st'+i,{scale:3,opacity:0,rotation:-12});
  tl.to('#st'+i,{scale:1,opacity:1,rotation:-8,duration:.15,ease:'power4.in'},t+.2).to(sh,{x:'+=7',duration:.04,yoyo:true,repeat:3},t+.35);}
});
const ult=D.rostos[D.rostos.length-1];
tl.to('#fimIn',{opacity:1,duration:.3},D.dur-.05);
tl.from('#ff',{y:40,opacity:0,duration:.4,ease:'power3.out'},D.dur+.1);
window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;
</script></body></html>"""

if __name__ == "__main__":
    main()
