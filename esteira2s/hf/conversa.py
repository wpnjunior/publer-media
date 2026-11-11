#!/usr/bin/env python3
"""Edição CONVERSA (HyperFrames): a explicação chega como conversa de mensagens no celular.

Uso: python esteira2s/hf/conversa.py bruto.mp4 words.json plano_conversa.json projeto_dir saida.mp4

- bruto.mp4 vem do montar_bruto.py (rosto do banco ou clone novo + narração só em áudio).
- words.json vem do reel_kit/diario/transcrever.py.
- plano_conversa.json:
  {"arroba":"@conta","marca":"NOME","contato":"Pergunta do dia","iniciais":"PD","status":"online",
   "aviso":["Nova mensagem","Doutor, café quebra o jejum?"],
   "mensagens":[{"quando":"primeiras palavras","lado":"ele|eu","texto":"..."}],
   "seguir":"curte + segue","fim":{"frase":"...","ref":"..."},"trilha":"educacional"}
"ele" = balão cinza à esquerda (quem pergunta); "eu" = balão azul à direita (a resposta).
Cada balão entra na hora da fala; a conversa sobe sozinha quando enche a tela. Nenhum intervalo entre
balões pode passar de 6 s (o Porteiro reprova tela parada). Linguagem "conversa" na trava da mesmice.
"""
import html, json, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notas import achar, blocos, AQUI, KIT, FIM_S  # noqa: E402


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

    e = html.escape
    msgs, desde = [], 0.0
    for m in plano["mensagens"]:
        t = achar(words, m["quando"], desde); desde = t
        msgs.append({"t": round(t, 2), "lado": m["lado"]})
    ant = [x["t"] for x in msgs]
    for a, b in zip(ant, ant[1:]):
        if b - a > 6.5:
            print(f"AVISO: {b - a:.1f} s sem balão novo entre {a} e {b}", file=sys.stderr)
    rostos = [x for x in trechos if x["tipo"] == "rosto"]
    vozes = [x for x in trechos if x["tipo"] != "rosto"]
    dados = {"msgs": msgs, "rostos": rostos, "vozes": vozes, "dur": dur, "total": total,
             "blocos": blocos(words, trechos), "seg": rostos[1] if len(rostos) > 2 else None}
    bal = "\n".join(f'<div class="row {m["lado"]}"><div class="bal" id="m{i}">{e(m["texto"])}</div></div>'
                    for i, m in enumerate(plano["mensagens"]))
    caps = "\n".join(f'<span class="cap {b["tipo"]}" id="cap{i}">{e(b["txt"])}</span>' for i, b in enumerate(dados["blocos"]))
    doc = MOLDE
    for k, v in {"__TOTAL__": str(total), "__DUR__": str(round(dur, 2)), "__BAL__": bal, "__CAPS__": caps,
                 "__CONTATO__": e(plano["contato"]), "__INI__": e(plano.get("iniciais", "?")),
                 "__STATUS__": e(plano.get("status", "online")),
                 "__AV1__": e(plano["aviso"][0]), "__AV2__": e(plano["aviso"][1]),
                 "__SEGUIR__": e(plano.get("seguir", "curte + segue")), "__ARROBA__": e(plano["arroba"]),
                 "__MARCA__": e(plano["marca"]), "__FIMFRASE__": e(plano["fim"]["frase"]),
                 "__FIMREF__": e(plano["fim"]["ref"]).replace("\n", "<br>"),
                 "__DADOS__": json.dumps(dados, ensure_ascii=False)}.items():
        doc = doc.replace(k, v)
    (proj / "index.html").write_text(doc, encoding="utf-8")
    mudo = proj / "render.mp4"
    subprocess.run(["npx", "hyperframes", "render", "--quality", "looks", "-o", str(mudo)], cwd=proj, check=True)
    trilha = KIT / "trilhas" / f'{plano.get("trilha", "educacional")}.m4a'
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mudo), "-stream_loop", "-1", "-i", str(trilha),
                    "-filter_complex",
                    f"[0:a]apad[v];[1:a]volume=0.10,afade=t=out:st={total - 1.2}:d=1.2[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-t", str(total), "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(saida)], check=True)
    print(f"CONVERSA OK: {saida} ({total} s)")


MOLDE = r"""<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{font-family:"Permanent Marker";src:url("assets/permanent-marker-400.woff2") format("woff2")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000;font-family:Inter,sans-serif}
#root{position:relative;width:1080px;height:1920px;overflow:hidden}
#v{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;z-index:1}
#chat,#capsRosto,#aviso,#adesivo,#fim{position:absolute;inset:0}
#chat{z-index:2}
#chatIn{position:absolute;inset:0;background:#efeae2}
#topo{position:absolute;left:0;right:0;top:0;height:250px;background:#1f2c34;padding:96px 44px 0;display:flex;align-items:center;gap:30px}
#volta{font-size:64px;color:#8fa3ad;font-weight:300}
#foto{width:104px;height:104px;border-radius:52px;background:#5b7bd5;color:#fff;font-size:42px;font-weight:800;display:grid;place-items:center}
#nome{font-size:48px;font-weight:800;color:#fff;white-space:nowrap}
#st{font-size:32px;color:#9fe0b1;margin-top:4px}
#area{position:absolute;left:0;right:0;top:250px;height:1220px;overflow:hidden}
#msgs{position:absolute;left:0;right:0;top:0;padding:40px 40px 0}
.row{display:flex;margin-bottom:26px}
.row.eu{justify-content:flex-end}
.bal{max-width:800px;font-size:54px;line-height:1.22;font-weight:600;padding:26px 36px;border-radius:38px;box-shadow:0 4px 10px rgba(0,0,0,.10)}
.ele .bal{background:#fff;color:#1b1f23;border-bottom-left-radius:10px;transform-origin:left bottom}
.eu .bal{background:#2f6fed;color:#fff;border-bottom-right-radius:10px;transform-origin:right bottom}
#faixa{position:absolute;left:0;right:0;top:1470px;height:450px;background:#f7f4ee;border-top:3px solid #d8d2c6}
.cap{position:absolute;opacity:0;white-space:nowrap}
.cap.voz{left:0;right:0;top:50px;text-align:center;font-size:50px;font-weight:700;color:#3a3f45}
#capsRosto{z-index:3;pointer-events:none}
.cap.rosto{left:60px;right:60px;top:1190px;text-align:center;font-size:74px;font-weight:900;color:#fff;white-space:normal;text-shadow:0 4px 18px rgba(0,0,0,.85),0 0 4px #000}
#aviso{z-index:4}
#avIn{position:absolute;left:40px;right:40px;top:150px;background:rgba(255,255,255,.96);border-radius:40px;padding:30px 38px;display:flex;gap:28px;align-items:center;box-shadow:0 16px 40px rgba(0,0,0,.35)}
#avFoto{flex:none;width:96px;height:96px;border-radius:48px;background:#5b7bd5;color:#fff;font-size:38px;font-weight:800;display:grid;place-items:center}
#av1{font-size:32px;color:#6b7280;font-weight:600}#av2{font-size:46px;color:#111;font-weight:800;line-height:1.15}
#adesivo{z-index:4}#adIn{position:absolute;left:50%;top:330px;white-space:nowrap;background:#2f6fed;color:#fff;border-radius:44px;padding:22px 50px;text-align:center;box-shadow:0 12px 30px rgba(0,0,0,.4)}
.s1{font-size:64px;font-weight:900}.s2{font-size:40px;font-weight:700}
#fim{z-index:5}#fimIn{position:absolute;inset:0;background:#efeae2;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 100px;text-align:center}
#fm{font-size:44px;letter-spacing:.2em;color:#6b7280;font-weight:700}
#ff{font-family:"Permanent Marker";font-size:104px;line-height:1.1;color:#2f6fed;margin:54px 0}
#fr{font-size:36px;line-height:1.45;color:#4b5563}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__TOTAL__" data-width="1080" data-height="1920" data-fps="30">
<video id="v" class="clip" src="assets/bruto.mp4" data-start="0" data-duration="__DUR__" data-track-index="0" data-has-audio="true"></video>
<div id="chat" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="1" data-track-kind="graphics"><div id="chatIn">
 <div id="topo"><div id="volta">‹</div><div id="foto">__INI__</div><div><div id="nome">__CONTATO__</div><div id="st">__STATUS__</div></div></div>
 <div id="area"><div id="msgs">
__BAL__
 </div></div>
 <div id="faixa">__CAPS__</div>
</div></div>
<div id="capsRosto" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="2" data-track-kind="captions"></div>
<div id="aviso" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="3" data-track-kind="graphics"><div id="avIn"><div id="avFoto">__INI__</div><div><div id="av1">__AV1__</div><div id="av2">__AV2__</div></div></div></div>
<div id="adesivo" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="4" data-track-kind="graphics"><div id="adIn"><div class="s1">__SEGUIR__</div><div class="s2">__ARROBA__</div></div></div>
<div id="fim" class="clip" data-start="0" data-duration="__TOTAL__" data-track-index="5" data-track-kind="graphics"><div id="fimIn"><div id="fm">__MARCA__</div><div id="ff">__FIMFRASE__</div><div id="fr">__FIMREF__</div></div></div>
</div>
<script>
const D=__DADOS__;
const tl=gsap.timeline({paused:true});
const $=s=>document.querySelector(s);
document.querySelectorAll('.cap.rosto').forEach(c=>$('#capsRosto').appendChild(c));
D.blocos.forEach((b,i)=>{tl.set('#cap'+i,{opacity:1},b.t0);tl.set('#cap'+i,{opacity:0},b.t1);});
gsap.set('#chatIn',{opacity:0});gsap.set('#fimIn',{opacity:0});gsap.set('#adIn',{xPercent:-50,scale:0});
D.vozes.forEach(v=>{tl.fromTo('#chatIn',{opacity:0,scale:1.06},{opacity:1,scale:1,duration:.25,ease:'power3.out'},v.t0);tl.to('#chatIn',{opacity:0,duration:.12},v.t1-.06);});
// gancho: a notificação da mensagem cai sobre o rosto
const g0=D.rostos[0];
gsap.set('#avIn',{y:-420});
tl.to('#avIn',{y:0,duration:.35,ease:'back.out(1.6)'},.06).to('#avIn',{scale:1.04,duration:.12,yoyo:true,repeat:1},.6)
  .to('#avIn',{y:-420,duration:.2,ease:'power2.in'},Math.max(1,g0.t1-.2));
if(D.seg){tl.to('#adIn',{scale:1,duration:.3,ease:'back.out(2)'},D.seg.t0+.2).to('#adIn',{scale:0,duration:.2},D.seg.t1-.2);}
// balões: entram na fala; a conversa sobe quando passa da área
const AREA=1220;
D.msgs.forEach((m,i)=>{
 const el=document.getElementById('m'+i),row=el.parentElement;
 const fundo=row.offsetTop+row.offsetHeight+26;
 gsap.set(el,{scale:.5,opacity:0});
 const sobe=Math.max(0,fundo-AREA);
 if(sobe>0)tl.to('#msgs',{y:-sobe,duration:.3,ease:'power2.out'},m.t-.05);
 tl.to(el,{scale:1,opacity:1,duration:.28,ease:'back.out(1.8)'},m.t);
});
tl.to('#fimIn',{opacity:1,duration:.3},D.dur-.05);
tl.from('#ff',{y:40,opacity:0,duration:.4,ease:'power3.out'},D.dur+.1);
window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;
</script></body></html>"""

if __name__ == "__main__":
    main()
