"""quadro.py: edição "Quadro" (papel infinito desenhado a lápis).

Receita copiada da ESTRUTURA de edição de um Reels de referência (23/11/2026), sem copiar conteúdo nem marca:
- um quadro de papel bege enorme; a câmera passeia de cena em cena e, no fim, afasta e mostra o mapa inteiro;
- tudo nasce desenhado por um lápis que aparece na tela (traço à mão, rabisco duplo);
- poucas cores: tinta marrom, verde de sublinhado, marca-texto mostarda, rosa de pele;
- números grandes, palavra-chave em marca-texto, palavra riscada, etiquetas com losango, setas e anotações manuscritas;
- legenda pequena numa caixinha branca embaixo à esquerda, 3 a 6 palavras por vez;
- sem rosto na narração; CTA desenhado ("Siga esse perfil" + botão Seguindo) com o clone do banco numa foto colada.

Uso: python3 quadro.py plano.json saida_dir   (plano: ver planos/quadro_grelina.json)
Depois: npx hyperframes render dentro de saida_dir e mix com quadro_mix.sh.
"""
import json, math, random, sys
from html import escape as esc
from pathlib import Path

W, H = 1080, 1920
AQUI = Path(__file__).resolve().parent
TINTA, VERDE, MOSTARDA, PELE, PAPEL = "#3b3330", "#2f6b55", "#e3c46b", "#c98b80", "#ece6dc"
FOCO_Y = 690          # centro do conteúdo na tela (acima da legenda; área livre do Instagram)
CENA_W, CENA_H = 1000, 1100


class Q:
    def __init__(self, P):
        self.P, self.rng = P, random.Random(P.get("seed", 7))
        self.svg, self.html, self.js, self.n = [], [], [], 0
        self.lapis = []   # (t, d, x0, y0, x1, y1)

    def id(self, p="e"):
        self.n += 1
        return f"{p}{self.n}"

    # ---------- traço à mão ----------
    def rough(self, pts, closed=False, j=2.6):
        r = self.rng
        def one():
            q = [(x + r.uniform(-j, j), y + r.uniform(-j, j)) for x, y in pts]
            if closed: q.append(q[0])
            d = f"M{q[0][0]:.1f} {q[0][1]:.1f}"
            for a, b in zip(q, q[1:]):
                mx, my = (a[0] + b[0]) / 2 + r.uniform(-j, j), (a[1] + b[1]) / 2 + r.uniform(-j, j)
                d += f" Q{mx:.1f} {my:.1f} {b[0]:.1f} {b[1]:.1f}"
            return d
        return [one(), one()]

    def path(self, ds, t, d, cor=TINTA, esp=5, fill="none", fill_t=None, op=1):
        ids = []
        for k, dd in enumerate(ds):
            i = self.id("p")
            ids.append(i)
            o = op if k == 0 else op * 0.55
            self.svg.append(f'<path id="{i}" d="{dd}" fill="none" stroke="{cor}" stroke-width="{esp if k == 0 else esp * .6:.1f}" '
                            f'stroke-linecap="round" stroke-linejoin="round" opacity="0" pathLength="1" '
                            f'style="stroke-dasharray:1;stroke-dashoffset:1;stroke-opacity:{o}"/>')
            self.js.append(f'tl.set("#{i}",{{opacity:1}},{t:.3f});tl.to("#{i}",{{strokeDashoffset:0,duration:{d * (1 if k == 0 else .8):.3f},ease:"power1.inOut"}},{t + k * d * .15:.3f});')
        if fill != "none":
            i = self.id("f")
            self.svg.insert(len(self.svg) - len(ds), f'<path id="{i}" d="{ds[0]}" fill="{fill}" stroke="none" opacity="0"/>')
            self.js.append(f'tl.to("#{i}",{{opacity:1,duration:.35}},{(fill_t or t + d):.3f});')
        return ids

    # ---------- primitivas (coordenadas do mundo) ----------
    def linha(self, pts, t, d=.5, **k):
        self.path(self.rough(pts), t, d, **k)
        self.lapis.append((t, d, *pts[0], *pts[-1]))

    def circulo(self, cx, cy, r, t, d=.6, **k):
        pts = [(cx + r * math.cos(a / 24 * 2 * math.pi - 1.6), cy + r * math.sin(a / 24 * 2 * math.pi - 1.6)) for a in range(25)]
        self.path(self.rough(pts, j=2), t, d, **k)
        self.lapis.append((t, d, pts[0][0], pts[0][1], pts[-2][0], pts[-2][1]))

    def caixa(self, x, y, w, h, t, d=.6, **k):
        pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        self.path(self.rough(pts, closed=True, j=2), t, d, **k)
        self.lapis.append((t, d, x, y, x, y + h))

    def seta(self, x0, y0, x1, y1, t, d=.45, cor=VERDE, esp=4):
        mx, my = (x0 + x1) / 2 + (y1 - y0) * .12, (y0 + y1) / 2 - (x1 - x0) * .12
        self.path([f"M{x0} {y0} Q{mx:.0f} {my:.0f} {x1} {y1}"], t, d, cor=cor, esp=esp)
        a = math.atan2(y1 - my, x1 - mx)
        for s in (-1, 1):
            hx, hy = x1 - 22 * math.cos(a + s * .5), y1 - 22 * math.sin(a + s * .5)
            self.path([f"M{x1} {y1} L{hx:.0f} {hy:.0f}"], t + d * .9, .15, cor=cor, esp=esp)
        self.lapis.append((t, d, x0, y0, x1, y1))

    def onda(self, x0, y0, larg, alt, picos, t, d=1.2, cor=VERDE, esp=6):
        pts = []
        for k in range(picos * 16 + 1):
            u = k / (picos * 16)
            pts.append((x0 + u * larg, y0 - alt * (0.5 - 0.5 * math.cos(u * picos * 2 * math.pi))))
        dd = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        self.path([dd], t, d, cor=cor, esp=esp)
        self.lapis.append((t, d, *pts[0], *pts[-1]))

    def check(self, x, y, t, s=1, cor=VERDE):
        self.linha([(x, y), (x + 14 * s, y + 16 * s), (x + 40 * s, y - 20 * s)], t, .3, cor=cor, esp=6)

    def xis(self, x, y, s, t, cor="#b4473c"):
        self.linha([(x - s, y - s), (x + s, y + s)], t, .2, cor=cor, esp=7)
        self.linha([(x + s, y - s), (x - s, y + s)], t + .2, .2, cor=cor, esp=7)

    def texto(self, x, y, txt, t, tam=44, fonte="mao", cor=TINTA, d=None, peso=400, ancora="l"):
        """escrita: revela da esquerda para a direita (como se o lápis escrevesse)."""
        i = self.id("t")
        fam = {"mao": "'Caveat'", "sans": "'Montserrat'", "num": "'Source Serif 4'"}[fonte]
        tr = {"l": "", "c": "transform:translateX(-50%);", "r": "transform:translateX(-100%);"}[ancora]
        self.html.append(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;{tr}font-family:{fam};font-size:{tam}px;'
                         f'font-weight:{peso};color:{cor};white-space:nowrap;line-height:1.1;clip-path:inset(-20% 100% -20% 0)">{esc(txt)}</div>')
        d = d or min(1.0, .1 + .045 * len(txt))
        self.js.append(f'tl.to("#{i}",{{clipPath:"inset(-20% 0% -20% 0)",duration:{d:.3f},ease:"none"}},{t:.3f});')
        larg = len(txt) * tam * (.42 if fonte == "mao" else .58)
        x0 = x - (larg / 2 if ancora == "c" else larg if ancora == "r" else 0)
        self.lapis.append((t, d, x0, y + tam * .9, x0 + larg, y + tam * .9))
        return i, x0, larg

    def marca(self, x, y, w, h, t, cor=MOSTARDA, d=.35):
        i = self.id("m")
        self.html.insert(0, f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{cor};'
                            f'opacity:.85;border-radius:4px;transform-origin:0 50%"></div>')
        self.js.append(f'tl.set("#{i}",{{scaleX:0.001,rotation:-1}},0);tl.to("#{i}",{{scaleX:1,duration:{d},ease:"power2.out"}},{t:.3f});')

    def riscar(self, x, y, w, t):
        self.linha([(x - 6, y), (x + w + 6, y - 4)], t, .3, cor=TINTA, esp=5)

    def etiqueta(self, x, y, txt, t):
        """losango com ! + etiqueta cinza (marcador de capítulo)."""
        self.linha([(x, y + 22), (x + 22, y), (x + 44, y + 22), (x + 22, y + 44), (x, y + 22)], t, .35, cor=TINTA, esp=4, fill=MOSTARDA)
        i = self.id("g")
        self.html.append(f'<div id="{i}" style="position:absolute;left:{x + 56}px;top:{y + 2}px;font-family:Montserrat;font-size:34px;'
                         f'color:{TINTA};background:#d6d3c8;padding:2px 14px;border-radius:6px;opacity:0;transform:translateY(8px)">{esc(txt)}</div>')
        self.js.append(f'tl.to("#{i}",{{opacity:1,y:0,duration:.35,ease:"back.out(2)"}},{t + .3:.3f});')

    def foto(self, x, y, w, h, t, legenda="", video=None, dur=0, img=None):
        i = self.id("v")
        inner = ""
        if video:
            inner = (f'<video id="{i}x" class="clip" src="{esc(video)}" muted playsinline data-start="{t:.3f}" data-duration="{dur:.3f}" '
                     f'data-media-start="0" data-track-index="5" style="position:absolute;left:14px;top:14px;width:{w - 28}px;height:{h - 80}px;'
                     f'object-fit:cover;object-position:50% 18%"></video>')
        elif img:
            inner = f'<img src="{esc(img)}" style="position:absolute;left:14px;top:14px;width:{w - 28}px;height:{h - 80}px;object-fit:cover">'
        self.html.append(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#faf8f3;'
                         f'box-shadow:0 8px 22px rgba(60,40,30,.25);transform:rotate(-2deg) scale(.6);opacity:0">{inner}'
                         f'<div style="position:absolute;left:0;right:0;bottom:14px;text-align:center;font-family:Caveat;font-size:36px;color:{TINTA}">{esc(legenda)}</div></div>')
        self.js.append(f'tl.to("#{i}",{{opacity:1,scale:1,duration:.45,ease:"back.out(1.6)"}},{t - .05:.3f});')
        self.lapis.append((t - .3, .3, x + w, y + h, x + w - 30, y + h - 30))

    def botao(self, x, y, txt, t):
        i = self.id("b")
        self.html.append(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;font-family:Montserrat;font-size:40px;color:#223;'
                         f'background:#a9c3b0;border:3px solid {TINTA};padding:8px 26px;border-radius:40px;opacity:0;transform:scale(.4)">{esc(txt)}</div>')
        self.js.append(f'tl.to("#{i}",{{opacity:1,scale:1,duration:.4,ease:"back.out(2.4)"}},{t:.3f});'
                       f'tl.to("#{i}",{{scale:.92,duration:.08,yoyo:true,repeat:1}},{t + .7:.3f});')

    # ---------- desenhos prontos ----------
    def relogio(self, cx, cy, r, t, horas=12):
        self.circulo(cx, cy, r, t, .6, esp=6)
        a = (horas % 12) / 12 * 2 * math.pi - math.pi / 2
        self.linha([(cx, cy), (cx + r * .5 * math.cos(a), cy + r * .5 * math.sin(a))], t + .55, .2, esp=7)
        self.linha([(cx, cy), (cx, cy - r * .78)], t + .7, .2, esp=5)
        for k in range(12):
            b = k / 12 * 2 * math.pi
            self.linha([(cx + r * .86 * math.cos(b), cy + r * .86 * math.sin(b)), (cx + r * .94 * math.cos(b), cy + r * .94 * math.sin(b))], t + .4 + k * .02, .05, esp=3)

    def estomago(self, cx, cy, s, t):
        pts = [(-60, -110), (-40, -40), (-90, 20), (-70, 90), (10, 120), (90, 70), (100, -10), (40, -40), (10, -110)]
        self.path(self.rough([(cx + x * s, cy + y * s) for x, y in pts], closed=True), t, .7, cor=TINTA, esp=5, fill=PELE, fill_t=t + .5)
        self.lapis.append((t, .7, cx - 60 * s, cy - 110 * s, cx + 10 * s, cy - 110 * s))

    def bateria(self, x, y, w, h, t):
        self.caixa(x, y, w, h, t, .5, esp=6)
        self.caixa(x + w, y + h * .3, 18, h * .4, t + .45, .15, esp=5)
        i = self.id("bat")
        self.html.insert(0, f'<div id="{i}" style="position:absolute;left:{x + 10}px;top:{y + 10}px;width:{w - 20}px;height:{h - 20}px;'
                            f'background:#7fae8f;transform-origin:0 50%;transform:scaleX(0)"></div>')
        self.js.append(f'tl.to("#{i}",{{scaleX:1,duration:.6,ease:"power2.out"}},{t + .6:.3f});')

    def prato(self, cx, cy, s, t):
        self.circulo(cx, cy, 46 * s, t, .35, esp=4)
        self.circulo(cx, cy, 30 * s, t + .2, .25, esp=3)
        self.linha([(cx - 70 * s, cy - 30 * s), (cx - 70 * s, cy + 40 * s)], t + .3, .15, esp=4)
        self.linha([(cx + 70 * s, cy - 30 * s), (cx + 70 * s, cy + 40 * s)], t + .35, .15, esp=4)

    def copo(self, x, y, w, h, t):
        self.linha([(x, y), (x + w * .1, y + h), (x + w * .9, y + h), (x + w, y)], t, .6, esp=6)
        i = self.id("agua")
        self.html.insert(0, f'<div id="{i}" style="position:absolute;left:{x + w * .1}px;top:{y + h * .25}px;width:{w * .8}px;height:{h * .73}px;'
                            f'background:#a9c8d6;opacity:.8;transform-origin:50% 100%;transform:scaleY(0);clip-path:polygon(0 0,100% 0,96% 100%,4% 100%)"></div>')
        self.js.append(f'tl.to("#{i}",{{scaleY:1,duration:.8,ease:"power2.out"}},{t + .5:.3f});')

    def boneco(self, cx, cy, s, t, cor=PELE):
        self.circulo(cx, cy - 120 * s, 32 * s, t, .3, esp=4, fill=cor, fill_t=t + .3)
        pts = [(-40, -80), (40, -80), (50, 30), (30, 30), (28, 140), (6, 140), (0, 50), (-6, 140), (-28, 140), (-30, 30), (-50, 30)]
        self.path(self.rough([(cx + x * s, cy + y * s) for x, y in pts], closed=True, j=1.5), t + .25, .6, cor=TINTA, esp=4, fill=cor, fill_t=t + .7)


# ---------- montagem ----------
def montar(P, out):
    q = Q(P)
    for cena in P["cenas"]:
        ox, oy = cena["origem"]
        for el in cena["elementos"]:
            el = dict(el)
            tipo = el.pop("tipo")
            for k in ("x", "cx", "x0", "x1"):
                if k in el: el[k] += ox
            for k in ("y", "cy", "y0", "y1"):
                if k in el: el[k] += oy
            if "pts" in el: el["pts"] = [(a + ox, b + oy) for a, b in el["pts"]]
            getattr(q, tipo)(**el)
    # câmera: centro da cena -> (540, FOCO_Y)
    cam = []
    for cena in P["cenas"]:
        ox, oy = cena["origem"]
        cx, cy = ox + CENA_W / 2 + cena.get("dx", 0), oy + CENA_H / 2 + cena.get("dy", 0)
        cam.append((cena["t"], 540 - cx, FOCO_Y - cy, 1.0, cena.get("mov", .8)))
        for (tt, dx, dy) in cena.get("deriva", []):   # passeio dentro da cena (algo muda a cada 2-4 s)
            cam.append((tt, 540 - cx - dx, FOCO_Y - cy - dy, 1.0, 1.2))
    if P.get("afastar"):
        a = P["afastar"]
        s = a["escala"]
        cam.append((a["t"], 540 - a["cx"] * s, FOCO_Y - a["cy"] * s, s, a.get("mov", 1.1)))
        cam.sort(key=lambda c: c[0])
    js_cam = []
    x0, y0 = cam[0][1], cam[0][2]
    js_cam.append(f'tl.set("#mundo",{{x:{x0:.1f},y:{y0:.1f},scale:1}},0);')
    for (t, x, y, s, mv) in cam[1:]:
        js_cam.append(f'tl.to("#mundo",{{x:{x:.1f},y:{y:.1f},scale:{s},duration:{mv},ease:"power2.inOut"}},{max(0, t - mv * .6):.3f});')
    # lápis: vai até o início do traço e segue até o fim
    js_l = []
    for (t, d, xa, ya, xb, yb) in sorted(q.lapis):
        js_l.append(f'tl.to("#lapis",{{x:{xa:.0f},y:{ya:.0f},duration:.18,ease:"power1.out"}},{max(0, t - .18):.3f});'
                    f'tl.to("#lapis",{{x:{xb:.0f},y:{yb:.0f},duration:{d:.3f},ease:"none"}},{t:.3f});')
    fim_lapis = P.get("lapis_some", P["dur"] - .5)
    js_l.append(f'tl.to("#lapis",{{opacity:0,duration:.3}},{fim_lapis:.3f});')
    # legenda: caixinha branca embaixo à esquerda
    words = json.load(open(P["words"]))
    blocos, cur = [], []
    for w in words:
        cur.append(w)
        if w["w"][-1] in ".?!," and len(cur) >= 2 or len(cur) >= 5:
            blocos.append(cur); cur = []
    if cur: blocos.append(cur)
    leg_html, js_leg = [], []
    for k, b in enumerate(blocos):
        t0 = b[0]["s"] - .05
        t1 = blocos[k + 1][0]["s"] - .05 if k + 1 < len(blocos) else b[-1]["e"] + .4
        txt = " ".join(w["w"] for w in b)
        i = f"lg{k}"
        leg_html.append(f'<div id="{i}" class="leg">{esc(txt)}</div>')
        js_leg.append(f'tl.set("#{i}",{{opacity:1}},{t0:.3f});tl.set("#{i}",{{opacity:0}},{t1:.3f});')
    # câmera que respira: zoom lento de vai e volta o tempo todo (o papel nunca fica parado)
    per = P.get("respira", 3.2)
    js_resp = f'tl.fromTo("#resp",{{scale:1}},{{scale:1.045,duration:{per},ease:"sine.inOut",yoyo:true,repeat:{int(P["dur"] / per)}}},0);'
    sw = P.get("mundo", [3300, 3700])
    fontes = "".join(f"@font-face{{font-family:'{n}';src:url('assets/fonts/{f}.ttf')}}" for n, f in
                     [("Caveat", "Caveat"), ("Montserrat", "Montserrat"), ("Source Serif 4", "SourceSerif4")])
    lapis_svg = (f'<svg id="lapis" width="40" height="560" viewBox="0 0 40 560" style="position:absolute;left:0;top:0;margin-left:-6px;'
                 f'transform-origin:0 0;overflow:visible"><g transform="rotate(-28)"><polygon points="0,0 9,26 -9,26" fill="#d9c7a0"/>'
                 f'<polygon points="0,0 3,9 -3,9" fill="#555"/><rect x="-9" y="26" width="18" height="520" rx="6" fill="#f3efe4" stroke="#cfc6b3" stroke-width="2"/></g></svg>')
    doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{fontes}*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{PAPEL}}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{PAPEL}}}
#papel{{position:absolute;inset:0;background:radial-gradient(ellipse at 30% 20%,#f3eee6 0,{PAPEL} 55%,#e2dbcf 100%)}}
#grao{{position:absolute;inset:0;opacity:.18;mix-blend-mode:multiply;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.9' numOctaves='2'/%3E%3CfeColorMatrix values='0 0 0 0 .4 0 0 0 0 .35 0 0 0 0 .3 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)'/%3E%3C/svg%3E")}}
#mundo{{position:absolute;left:0;top:0;width:{sw[0]}px;height:{sw[1]}px;transform-origin:0 0}}
#mundo svg.tr{{position:absolute;left:0;top:0;overflow:visible}}
.leg{{position:absolute;left:44px;top:1330px;max-width:620px;background:#fbfaf6;color:#2b2522;font-family:Montserrat;font-weight:600;
font-size:38px;line-height:1.25;padding:12px 20px;border-radius:6px;box-shadow:0 4px 12px rgba(60,40,30,.18);opacity:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{P['dur']}" data-width="{W}" data-height="{H}"
 data-layout-allow-overflow data-layout-allow-overlap>
<div id="papel"></div>
<div id="resp" style="position:absolute;inset:0;transform-origin:540px {FOCO_Y}px">
<div id="mundo">
<svg class="tr" width="{sw[0]}" height="{sw[1]}">{''.join(q.svg)}</svg>
{chr(10).join(q.html)}
{lapis_svg}
</div>
</div>
<div id="grao"></div>
{chr(10).join(leg_html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(q.js)}
{chr(10).join(js_cam)}
{chr(10).join(js_l)}
{chr(10).join(js_leg)}
{js_resp}
tl.to({{}},{{duration:.01}},{P['dur'] - .01});
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(doc)
    for f in ("hyperframes.json", "package.json", "meta.json"):
        src = AQUI.parent / f
        if src.exists() and not (out / f).exists():
            (out / f).write_text(src.read_text())
    a = out / "assets"
    if not a.exists():
        a.symlink_to(AQUI.parent / "assets")
    print("ok", out / "index.html", len(q.svg), "traços", len(q.html), "blocos", len(blocos), "legendas")


if __name__ == "__main__":
    montar(json.load(open(sys.argv[1])), sys.argv[2])
