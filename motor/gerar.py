"""Motor de edição dos Reels (caso 006 do Hospital): plano.json -> projeto HyperFrames (index.html).

Estilo como dado: o plano lista camadas com tempo; cada tipo de camada vira HTML + tweens GSAP.
Áudio NÃO entra no HTML: o mix sai do mix.py (voz, trilha com ducking, efeitos) e é colado no MP4.
Uso: python3 gerar.py plano.json pasta_saida
"""
import json, math, random, sys, html
from pathlib import Path

W, H = 1080, 1920
AQUI = Path(__file__).resolve().parent
PAL = dict(lima="#c6ff3d", amarelo="#ffd400", vermelho="#ff2d3d", fundo="#0b1512", creme="#f6efdc",
           tinta="#1c1a17", azul="#2a6df4", rosa="#ff4fa3", ciano="#35e0ff")


def esc(s):
    return html.escape(str(s))


class Comp:
    def __init__(self, plano):
        self.p = plano
        self.dur = plano["dur"]
        self.html = []
        self.js = []
        self.css = []
        self.n = 0
        self.rng = random.Random(plano.get("seed", 7))
        self.z = 10

    def nid(self, pre="L"):
        self.n += 1
        return f"{pre}{self.n}"

    def clip(self, inner, t0, d, z=None, style="", cls=""):
        i = self.nid()
        z = z if z is not None else self.next_z()
        if self.p.get("camera") and z < 85:
            cls = (cls + " cam").strip()
        self.html.append(
            f'<div id="{i}" class="clip {cls}" data-start="{t0:.3f}" data-duration="{d:.3f}" data-track-index="{z}" '
            f'style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:{z};{style}">{inner}</div>')
        return i

    def next_z(self):
        self.z += 1
        return self.z

    def tw(self, s):
        self.js.append(s)

    # ---------- desenho à mão ----------
    def rough(self, pts, closed=False, jitter=3.0):
        r = self.rng
        def one():
            q = [(x + r.uniform(-jitter, jitter), y + r.uniform(-jitter, jitter)) for x, y in pts]
            if closed:
                q.append(q[0])
            d = f"M{q[0][0]:.1f} {q[0][1]:.1f}"
            for a, b in zip(q, q[1:]):
                mx, my = (a[0] + b[0]) / 2 + r.uniform(-jitter, jitter), (a[1] + b[1]) / 2 + r.uniform(-jitter, jitter)
                d += f" Q{mx:.1f} {my:.1f} {b[0]:.1f} {b[1]:.1f}"
            return d
        return one() + " " + one()

    def ellipse_pts(self, cx, cy, rx, ry, n=28):
        a0 = self.rng.uniform(0, 1)
        return [(cx + rx * math.cos(a0 + 2 * math.pi * k / n * 1.08), cy + ry * math.sin(a0 + 2 * math.pi * k / n * 1.08)) for k in range(n + 1)]


# ======================= camadas =======================

def L_fundo(c, L):
    cor = L.get("cor", PAL["fundo"])
    tex = L.get("textura", "")
    bg = cor
    extra = ""
    if tex == "papel":
        bg = f"radial-gradient(ellipse at 50% 40%, #f8f1de 0%, #e9dcbc 70%, #cdb98f 100%)"
    elif tex == "grade":
        bg = (f"linear-gradient(rgba(255,255,255,.05) 2px, transparent 2px) 0 0/90px 90px,"
              f"linear-gradient(90deg, rgba(255,255,255,.05) 2px, transparent 2px) 0 0/90px 90px, {cor}")
    elif tex == "gradiente":
        bg = f"radial-gradient(circle at 30% 20%, {L.get('cor2', '#1d3b2f')} 0%, {cor} 70%)"
    i = c.nid("f")
    if tex == "grade":
        # fundo vivo: a grade corre na diagonal sem emenda (anda exatamente 1 período de 90 px por volta).
        # Motivo (13/11): fundo escuro parado deixava a narração com cara de tela congelada.
        bg = (f"linear-gradient(rgba(255,255,255,.075) 2px, transparent 2px) 0 0/90px 90px,"
              f"linear-gradient(90deg, rgba(255,255,255,.075) 2px, transparent 2px) 0 0/90px 90px, {cor}")
        g = c.nid("fl")
        inner = (f'<div id="{i}" style="position:absolute;inset:-190px;background:{bg}"></div>'
                 f'<div id="{g}" style="position:absolute;left:-300px;top:200px;width:1100px;height:1100px;border-radius:50%;'
                 f'background:radial-gradient(circle,rgba(198,255,61,.16) 0%,rgba(198,255,61,0) 65%)"></div>')
        c.clip(inner, L["t"], L["d"], z=L.get("z", 1))
        volta = 3.2
        n = max(1, math.ceil(L["d"] / volta))
        c.tw(f'tl.fromTo("#{i}",{{x:0,y:0}},{{x:-90,y:-90,duration:{volta},ease:"none",repeat:{n - 1}}},{L["t"]:.3f});')
        c.tw(f'tl.fromTo("#{g}",{{x:0,y:0}},{{x:700,y:500,duration:{max(L["d"] / max(1, round(L["d"] / 5)), 1):.2f},ease:"sine.inOut",repeat:{max(1, round(L["d"] / 5)) - 1},yoyo:true}},{L["t"]:.3f});')
        return
    inner = f'<div id="{i}" style="position:absolute;inset:-80px;background:{bg}"></div>'
    c.clip(inner, L["t"], L["d"], z=L.get("z", 1))
    # leve deriva para nunca ficar parado
    c.tw(f'tl.fromTo("#{i}",{{x:-30,y:-20,scale:1.04}},{{x:30,y:20,scale:1.08,duration:{L["d"]:.2f},ease:"none"}},{L["t"]:.3f});')


def box_style(L):
    x, y, w, h = L.get("box", [0, 0, W, H])
    return x, y, w, h


def enter(c, sel, L, t):
    e = L.get("entra", "pop")
    if e == "pop":
        c.tw(f'tl.fromTo("{sel}",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:"back.out(2)"}},{t:.3f});')
    elif e == "desliza":
        dx = L.get("dx", 0); dy = L.get("dy", 300)
        c.tw(f'tl.fromTo("{sel}",{{x:{dx},y:{dy},opacity:0}},{{x:0,y:0,opacity:1,duration:.45,ease:"power3.out"}},{t:.3f});')
    elif e == "cai":
        c.tw(f'tl.fromTo("{sel}",{{y:-900,rotation:-14}},{{y:0,rotation:{L.get("rot", -3)},duration:.5,ease:"bounce.out"}},{t:.3f});')
    elif e == "zoom":
        c.tw(f'tl.fromTo("{sel}",{{scale:1.6,opacity:0,filter:"blur(18px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:.4,ease:"power3.out"}},{t:.3f});')
    elif e == "mascara":
        c.tw(f'tl.fromTo("{sel}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.5,ease:"power2.inOut"}},{t:.3f});')
    elif e == "whip":
        c.tw(f'tl.fromTo("{sel}",{{x:1200,filter:"blur(30px)"}},{{x:0,filter:"blur(0px)",duration:.3,ease:"power4.out"}},{t:.3f});')
    elif e == "nada":
        pass


def kenburns(c, sel, L):
    kb = L.get("kb")
    if not kb:
        return
    s0, s1 = kb.get("s", [1.0, 1.12])
    x0, x1 = kb.get("x", [0, 0])
    y0, y1 = kb.get("y", [0, 0])
    c.tw(f'tl.fromTo("{sel}",{{scale:{s0},x:{x0},y:{y0}}},{{scale:{s1},x:{x1},y:{y1},duration:{L["d"]:.2f},ease:"none"}},{L["t"]:.3f});')


def L_foto(c, L):
    x, y, w, h = box_style(L)
    i = c.nid("p")
    raio = L.get("raio", 26)
    borda = L.get("borda", "")
    sombra = "box-shadow:0 30px 60px rgba(0,0,0,.45);" if L.get("sombra", True) else ""
    leg = ""
    if L.get("credito"):
        leg = f'<div style="position:absolute;left:14px;bottom:10px;font:600 20px Montserrat;color:#fff;text-shadow:0 2px 4px #000;opacity:.85">{esc(L["credito"])}</div>'
    rot = L.get("rot", 0)
    inner = (f'<div id="{i}w" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">'
             f'<div id="{i}" style="position:absolute;inset:0;overflow:hidden;border-radius:{raio}px;{sombra}{borda}">'
             f'<img id="{i}i" src="{esc(L["src"])}" style="width:100%;height:100%;object-fit:{L.get("fit", "cover")};object-position:{L.get("pos", "center")}">{leg}</div></div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    enter(c, f"#{i}", L, L["t"])
    kenburns(c, f"#{i}i", L)
    if L.get("sai"):
        c.tw(f'tl.to("#{i}",{{x:-1300,filter:"blur(20px)",duration:.25,ease:"power3.in"}},{L["t"] + L["d"] - .25:.3f});')


_DUR = {}


def dur_midia(src):
    if src not in _DUR:
        import subprocess
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True)
        try:
            _DUR[src] = float(r.stdout.strip())
        except ValueError:
            _DUR[src] = None
    return _DUR[src]


def trava_congelada(L):
    """Regra do Wagner (13/11): clipe nunca fica na tela depois de acabar (rosto congelado de boca aberta).
    Se o slot passa do fim do arquivo, encurta e avisa; o plano deve pôr o corte com efeito ali."""
    md = dur_midia(L["src"])
    if md is None:
        return L
    sobra = md - L.get("ms", 0)
    # até 0,12 s (3 quadros) segurando o último quadro some debaixo do flash/glitch do corte; mais que isso congela
    if L["d"] > sobra + 0.12:
        print(f"AVISO congelaria: {L['src']} t={L['t']} slot {L['d']:.2f}s > arquivo {sobra:.2f}s; encurtado", file=sys.stderr)
        L = dict(L, d=round(sobra, 3))
    return L


def L_video(c, L):
    """vídeo (viral ou rosto). Tempo no próprio <video>; transform num wrapper sem tempo."""
    L = trava_congelada(L)
    x, y, w, h = box_style(L)
    i = c.nid("v")
    z = L.get("z") or c.next_z()
    raio = L.get("raio", 0)
    borda = L.get("borda", "")
    fit = L.get("fit", "cover")
    pos = L.get("pos", "center")
    c.html.append(
        f'<div id="{i}w" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};overflow:hidden;border-radius:{raio}px;{borda}">'
        f'<video id="{i}" class="clip" src="{esc(L["src"])}" muted playsinline data-start="{L["t"]:.3f}" data-duration="{L["d"]:.3f}" '
        f'data-media-start="{L.get("ms", 0):.3f}" data-track-index="{z}" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:{fit};object-position:{pos}"></video></div>')
    # o wrapper não tem tempo: some quando o vídeo some porque não tem fundo; borda só via vídeo
    zs = L.get("zoom")  # [[t,escala],...]
    if zs:
        for (tz, s, dd) in zs:
            c.tw(f'tl.to("#{i}w",{{scale:{s},duration:{dd},ease:"power2.out"}},{tz:.3f});')
    elif L.get("respira", True):
        c.tw(f'tl.fromTo("#{i}w",{{scale:1}},{{scale:1.06,duration:{L["d"]:.2f},ease:"none"}},{L["t"]:.3f});')
    if L.get("entra"):
        enter(c, f"#{i}w", L, L["t"])
    if L.get("pausa"):  # ícone de pausa sobre o viral
        tp = L["pausa"]
        pid = c.nid("pz")
        c.clip(f'<div id="{pid}" style="position:absolute;left:{x + w / 2 - 70}px;top:{y + h / 2 - 70}px;width:140px;height:140px;border-radius:50%;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;gap:18px"><i style="width:22px;height:64px;background:#fff;display:block"></i><i style="width:22px;height:64px;background:#fff;display:block"></i></div>',
               tp, L["t"] + L["d"] - tp, z=z + 1)
        c.tw(f'tl.fromTo("#{pid}",{{scale:2,opacity:0}},{{scale:1,opacity:1,duration:.25,ease:"back.out(2)"}},{tp:.3f});')
    if L.get("arroba"):
        aid = c.nid("at")
        atop = y + 22 if L.get("arroba_pos") == "topo" else y + h - 86
        c.clip(f'<div id="{aid}" style="position:absolute;left:{x + 24}px;top:{atop}px;padding:10px 20px;border-radius:40px;background:rgba(0,0,0,.65);font:800 30px Montserrat;color:#fff">{esc(L["arroba"])}</div>',
               L["t"], L["d"], z=z + 1)
        c.tw(f'tl.fromTo("#{aid}",{{x:-300,opacity:0}},{{x:0,opacity:1,duration:.35,ease:"power3.out"}},{L["t"] + .2:.3f});')
    return i


def L_recorte(c, L):
    L = dict(L)
    L.setdefault("respira", False)
    L_video(c, L)


def L_cartao(c, L):
    """caixinha creme com aba verde-limão (padrão Rosenhan)."""
    x, y, w, h = box_style(L)
    i = c.nid("c")
    aba = L.get("aba", "")
    cor = L.get("cor", PAL["creme"])
    inner = (f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{cor};border-radius:22px;'
             f'box-shadow:0 26px 50px rgba(0,0,0,.45);background-image:repeating-linear-gradient(0deg,transparent 0 58px,rgba(40,90,160,.10) 58px 60px)">'
             f'<div id="{i}a" style="position:absolute;left:34px;top:-30px;padding:10px 30px;background:{PAL["lima"]};border-radius:14px;font:900 36px Montserrat;color:#10210f;letter-spacing:.5px;text-transform:uppercase">{esc(aba)}</div></div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    enter(c, f"#{i}", dict(L, entra=L.get("entra", "pop")), L["t"])
    if aba:
        c.tw(f'tl.fromTo("#{i}a",{{scaleX:0,transformOrigin:"left center"}},{{scaleX:1,duration:.3,ease:"power3.out"}},{L["t"] + .2:.3f});')
    # trocas de aba (nova cena da caixinha): [[t,"TEXTO"],...]
    for k, (ta, txt) in enumerate(L.get("abas", [])):
        c.tw(f'tl.set("#{i}a",{{textContent:{json.dumps(txt)}}},{ta:.3f});tl.fromTo("#{i}a",{{scaleX:0}},{{scaleX:1,duration:.25,ease:"power3.out"}},{ta:.3f});')


def L_desenho(c, L):
    """traços à mão que se desenham: seta, circulo, sublinhado, x, check, caixa, linha."""
    i = c.nid("d")
    cor = L.get("cor", PAL["vermelho"])
    lw = L.get("espessura", 9)
    paths = []
    for f in L["formas"]:
        k = f["k"]
        if k == "circulo":
            d = c.rough(c.ellipse_pts(*f["c"], *f["r"]), jitter=4)
        elif k == "seta":
            (x0, y0), (x1, y1) = f["de"], f["para"]
            mx, my = (x0 + x1) / 2 + f.get("curva", 60), (y0 + y1) / 2 - f.get("curva", 60)
            d = c.rough([(x0, y0), (mx, my), (x1, y1)], jitter=3)
            ang = math.atan2(y1 - my, x1 - mx)
            for s in (2.6, -2.6):
                hx, hy = x1 - 46 * math.cos(ang + s / 6), y1 - 46 * math.sin(ang + s / 6)
                d += " " + c.rough([(x1, y1), (hx, hy)], jitter=2)
        elif k == "sublinhado":
            (x0, y0), x1 = f["de"], f["ate"]
            d = c.rough([(x0, y0), ((x0 + x1) / 2, y0 + 6), (x1, y0 - 4)], jitter=3)
        elif k == "x":
            x0, y0, s = f["c"][0], f["c"][1], f.get("s", 80)
            d = c.rough([(x0 - s, y0 - s), (x0 + s, y0 + s)]) + " " + c.rough([(x0 + s, y0 - s), (x0 - s, y0 + s)])
        elif k == "check":
            x0, y0, s = f["c"][0], f["c"][1], f.get("s", 40)
            d = c.rough([(x0 - s, y0), (x0 - s * .2, y0 + s * .8), (x0 + s * 1.3, y0 - s)], jitter=2)
        elif k == "caixa":
            x0, y0, w, h = f["b"]
            d = c.rough([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], closed=True, jitter=4)
        elif k == "linha":
            d = c.rough(f["pts"], jitter=f.get("j", 3))
        else:
            continue
        paths.append((d, f.get("t", 0), f.get("cor", cor), f.get("lw", lw)))
    svg = f'<svg id="{i}" width="{W}" height="{H}" style="position:absolute;left:0;top:0" viewBox="0 0 {W} {H}">'
    for k, (d, _, cc, ll) in enumerate(paths):
        svg += f'<path id="{i}p{k}" d="{d}" fill="none" stroke="{cc}" stroke-width="{ll}" stroke-linecap="round" stroke-linejoin="round" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000"/>'
    svg += "</svg>"
    c.clip(svg, L["t"], L["d"], z=L.get("z"))
    for k, (d, tt, _, _) in enumerate(paths):
        c.tw(f'tl.fromTo("#{i}p{k}",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:{L.get("vel", .45)},ease:"power2.inOut"}},{L["t"] + tt:.3f});')


def L_texto(c, L):
    i = c.nid("t")
    x, y = L.get("xy", [60, 200])
    w = L.get("w", W - 120)
    fonte = L.get("fonte", "900 70px Montserrat")
    cor = L.get("cor", "#fff")
    al = L.get("alinha", "left")
    extra = L.get("css", "")
    if L.get("contorno"):
        extra += f"-webkit-text-stroke:{L['contorno']}px #000;paint-order:stroke fill;"
    txt = L["txt"]
    if L.get("anim") == "digita":
        spans = "".join(f'<span class="{i}c" style="opacity:0">{esc(ch)}</span>' for ch in txt)
    elif L.get("anim") == "palavras":
        spans = " ".join(f'<span class="{i}c" style="display:inline-block;opacity:0">{esc(wd)}</span>' for wd in txt.split(" "))
    else:
        spans = esc(txt).replace("\\n", "<br>")
    inner = f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font:{fonte};color:{cor};text-align:{al};line-height:1.08;{extra}">{spans}</div>'
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    if L.get("anim") == "digita":
        c.tw(f'tl.to(".{i}c",{{opacity:1,duration:.01,stagger:{L.get("vel", .035)}}},{L["t"]:.3f});')
    elif L.get("anim") == "palavras":
        c.tw(f'tl.fromTo(".{i}c",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.22,stagger:{L.get("vel", .12)},ease:"back.out(2)"}},{L["t"]:.3f});')
    else:
        enter(c, f"#{i}", L, L["t"])


def L_gigante(c, L):
    """palavra gigante atrás do rosto, cruzando a tela."""
    i = c.nid("g")
    cor = L.get("cor", PAL["lima"])
    cont = L.get("contorno", False)
    st = f"color:transparent;-webkit-text-stroke:6px {cor};" if cont else f"color:{cor};"
    y = L.get("y", 1000)
    tam = L.get("tam", 420)
    inner = f'<div id="{i}" style="position:absolute;left:0;top:{y}px;white-space:nowrap;font:{tam}px Anton;line-height:.9;{st}text-transform:uppercase">{esc(L["txt"])}</div>'
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    x0, x1 = L.get("x", [300, -900])
    c.tw(f'tl.fromTo("#{i}",{{x:{x0}}},{{x:{x1},duration:{L["d"]:.2f},ease:"none"}},{L["t"]:.3f});')


def L_carimbo(c, L):
    i = c.nid("s")
    x, y = L.get("xy", [200, 400])
    cor = L.get("cor", PAL["vermelho"])
    rot = L.get("rot", -12)
    tam = L.get("tam", 120)
    inner = (f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;padding:10px 34px;border:12px solid {cor};border-radius:18px;color:{cor};'
             f'font:{tam}px Anton;letter-spacing:4px;text-transform:uppercase;transform:rotate({rot}deg);mix-blend-mode:multiply;'
             f'mask-image:repeating-radial-gradient(circle at 30% 40%,#000 0 3px,rgba(0,0,0,.78) 3px 5px)">{esc(L["txt"])}</div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z", 80))
    c.tw(f'tl.fromTo("#{i}",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:.18,ease:"power4.in"}},{L["t"]:.3f});')
    c.tw(f'tl.fromTo("#{i}",{{x:-8}},{{x:8,duration:.04,repeat:5,yoyo:true}},{L["t"] + .18:.3f});')


def L_numero(c, L):
    """número grande com contador e 3D por camadas de sombra."""
    i = c.nid("n")
    x, y = L.get("xy", [0, 300])
    cor = L.get("cor", PAL["amarelo"])
    tam = L.get("tam", 300)
    sh = ",".join(f"{k}px {k}px 0 {L.get('sombra', '#7a5a00')}" for k in range(1, 22))
    pre, suf = L.get("pre", ""), L.get("suf", "")
    inner = (f'<div id="{i}w" style="position:absolute;left:{x}px;top:{y}px;width:{L.get("w", W)}px;text-align:center;perspective:900px">'
             f'<div id="{i}" style="display:inline-block;font:{tam}px Anton;color:{cor};text-shadow:{sh},0 40px 60px rgba(0,0,0,.6)">'
             f'{esc(pre)}<span id="{i}v">0</span>{esc(suf)}</div>'
             + (f'<div style="font:800 44px Montserrat;color:{L.get("cor_rotulo", "#fff")};margin-top:6px;text-shadow:{L.get("sombra_rotulo", "0 3px 8px #000")}">{esc(L["rotulo"])}</div>' if L.get("rotulo") else "")
             + '</div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    v = L["valor"]
    dec = L.get("dec", 0)
    c.tw(f'(function(){{var o={{v:{L.get("de", 0)}}};tl.to(o,{{v:{v},duration:{L.get("conta", 1.0)},ease:"power2.out",onUpdate:function(){{document.getElementById("{i}v").textContent=o.v.toFixed({dec}).replace(".",",")}}}},{L["t"]:.3f});}})();')
    c.tw(f'tl.fromTo("#{i}",{{rotationY:-70,rotationX:20,scale:.4}},{{rotationY:-12,rotationX:8,scale:1,duration:.7,ease:"back.out(1.6)"}},{L["t"]:.3f});')
    c.tw(f'tl.to("#{i}",{{rotationY:12,duration:{max(.1, L["d"] - .7):.2f},ease:"sine.inOut"}},{L["t"] + .7:.3f});')


def L_celular(c, L):
    """celular com imagem ou vídeo dentro + notificação."""
    x, y = L.get("xy", [240, 120])
    w, h = L.get("wh", [600, 1180])
    i = c.nid("cel")
    z = L.get("z") or c.next_z()
    inner = (f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:70px;background:#111;'
             f'box-shadow:0 40px 80px rgba(0,0,0,.6),inset 0 0 0 4px #333;padding:22px">'
             f'<div style="position:absolute;inset:22px;border-radius:52px;overflow:hidden;background:radial-gradient(circle at 30% 25%,#3a6b8f 0%,#1b2a4a 55%,#0d1222 100%)">'
             + (f'<img src="{esc(L["img"])}" style="width:100%;height:100%;object-fit:cover">' if L.get("img") else "")
             + f'</div><div style="position:absolute;left:50%;top:34px;width:150px;height:40px;margin-left:-75px;border-radius:20px;background:#000"></div></div>')
    c.clip(inner, L["t"], L["d"], z=z)
    enter(c, f"#{i}", dict(L, entra=L.get("entra", "desliza"), dy=1400), L["t"])
    c.tw(f'tl.fromTo("#{i}",{{rotation:-4}},{{rotation:3,duration:{L["d"]:.2f},ease:"sine.inOut"}},{L["t"]:.3f});')
    if L.get("video"):
        V = dict(L["video"])
        V.update(t=L["t"], d=L["d"], box=[x + 22, y + 22, w - 44, h - 44], raio=52, z=z + 1, respira=False)
        vid = L_video(c, V)
        c.tw(f'tl.fromTo("#{vid}w",{{y:1400}},{{y:0,duration:.45,ease:"power3.out"}},{L["t"]:.3f});')
    for nt in L.get("notif", []):
        nid = c.nid("nt")
        c.clip(f'<div id="{nid}" style="position:absolute;left:{x + 40}px;top:{y + 90}px;width:{w - 80}px;padding:22px 26px;border-radius:30px;background:rgba(245,245,245,.96);box-shadow:0 10px 30px rgba(0,0,0,.35);font:700 30px Montserrat;color:#111">'
               f'<div style="font:800 24px Montserrat;color:#777;margin-bottom:6px">{esc(nt.get("app", "Notícias"))} · agora</div>{esc(nt["txt"])}</div>',
               nt["t"], L["t"] + L["d"] - nt["t"], z=z + 3)
        c.tw(f'tl.fromTo("#{nid}",{{y:-250,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"back.out(1.6)"}},{nt["t"]:.3f});')


def miller(lat, lon, wpx=2000, hpx=1002):
    f = lambda la: 1.25 * math.log(math.tan(math.pi / 4 + 0.4 * math.radians(la)))
    ymax, ymin = f(84), f(-58)
    return (lon + 180) / 360 * wpx, (ymax - f(lat)) / (ymax - ymin) * hpx


def L_mapa(c, L):
    """mapa em papel antigo ou escuro; câmera (zoom em lugares), pinos, rotas com avião."""
    mapa = json.load(open(AQUI / "mapa_mundo.json"))
    i = c.nid("m")
    tema = L.get("tema", "papel")
    terra, mar, linha = ("#d9c7a0", "#efe4c9", "#8a7650") if tema == "papel" else ("#1f3a32", "#0b1512", "#3d6b5c")
    destaque = L.get("destaque", {})
    paths = []
    for nome, p in mapa["paises"].items():
        cor = destaque.get(nome, terra)
        paths.append(f'<path d="{p["d"]}" fill="{cor}" stroke="{linha}" stroke-width="1.2"/>')
    g = "".join(paths)
    # rotas
    rotas_svg, pinos_svg = "", ""
    for k, r in enumerate(L.get("rotas", [])):
        x0, y0 = miller(*r["de"]); x1, y1 = miller(*r["para"])
        mx, my = (x0 + x1) / 2, min(y0, y1) - abs(x1 - x0) * .25 - 30
        r["_pts"] = (x0, y0, mx, my, x1, y1)
        rotas_svg += (f'<path id="{i}r{k}" d="M{x0:.1f} {y0:.1f} Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{r.get("cor", PAL["vermelho"])}" '
                      f'stroke-width="{r.get("lw", 4)}" stroke-dasharray="1000" stroke-dashoffset="1000" pathLength="1000" stroke-linecap="round"/>')
        if r.get("aviao", True):
            rotas_svg += (f'<g id="{i}a{k}" opacity="0"><path d="M0 -14 L5 -4 L22 4 L22 8 L5 4 L4 16 L9 20 L9 23 L0 20 L-9 23 L-9 20 L-4 16 L-5 4 L-22 8 L-22 4 L-5 -4 Z" '
                          f'fill="{r.get("cor_aviao", "#1b1b1b")}" transform="rotate(90) scale(1.3)"/></g>')
    for k, pn in enumerate(L.get("pinos", [])):
        px, py = miller(*pn["ll"])
        pinos_svg += (f'<g transform="translate({px:.1f},{py:.1f})"><g id="{i}p{k}" opacity="0"><circle r="16" fill="{pn.get("cor", PAL["vermelho"])}" opacity=".35"/>'
                      f'<circle r="7" fill="{pn.get("cor", PAL["vermelho"])}" stroke="#fff" stroke-width="2"/>'
                      f'<text x="14" y="-12" font-family="Montserrat" font-weight="900" font-size="{pn.get("fs", 26)}" fill="{pn.get("cor_txt", "#1b1b1b")}" stroke="{pn.get("stroke", "#fff")}" stroke-width="{pn.get("sw", 5)}" paint-order="stroke">{esc(pn.get("txt", ""))}</text></g></g>')
    inner = (f'<div id="{i}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:{mar};overflow:hidden">'
             f'<svg id="{i}s" width="2000" height="1002" viewBox="0 0 2000 1002" style="position:absolute;left:0;top:0;transform-origin:0 0">'
             f'<g>{g}</g>{rotas_svg}{pinos_svg}</svg>'
             + ('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 45%,rgba(60,40,10,.45) 100%)"></div>' if tema == "papel" else "")
             + '</div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z", 2))
    # câmera: lista de [t, lat, lon, zoom, dur]; a área útil vertical é a box
    bx, by, bw, bh = L.get("area", [0, 0, W, H])
    for (tc, la, lo, zm, dd) in L["camera"]:
        px, py = miller(la, lo)
        tx, ty = bx + bw / 2 - px * zm, by + bh / 2 - py * zm
        if tc <= L["t"] + 0.001:
            c.tw(f'tl.set("#{i}s",{{x:{tx:.1f},y:{ty:.1f},scale:{zm}}},{L["t"]:.3f});')
        else:
            c.tw(f'tl.to("#{i}s",{{x:{tx:.1f},y:{ty:.1f},scale:{zm},duration:{dd},ease:"power2.inOut"}},{tc:.3f});')
    for k, pn in enumerate(L.get("pinos", [])):
        c.tw(f'tl.fromTo("#{i}p{k}",{{opacity:0,scale:3}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)",transformOrigin:"0px 0px"}},{pn["t"]:.3f});')
    for k, r in enumerate(L.get("rotas", [])):
        dd = r.get("dur", 1.4)
        c.tw(f'tl.to("#{i}r{k}",{{strokeDashoffset:0,duration:{dd},ease:"power1.inOut"}},{r["t"]:.3f});')
        if r.get("aviao", True):
            x0, y0, mx, my, x1, y1 = r["_pts"]
            kf = []
            n = 24
            for s in range(n + 1):
                u = s / n
                bxp = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1
                byp = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1
                dx = 2 * (1 - u) * (mx - x0) + 2 * u * (x1 - mx)
                dy = 2 * (1 - u) * (my - y0) + 2 * u * (y1 - my)
                kf.append(f'{{x:{bxp:.1f},y:{byp:.1f},rotation:{math.degrees(math.atan2(dy, dx)):.1f}}}')
            c.tw(f'tl.set("#{i}a{k}",{{opacity:1}},{r["t"]:.3f});tl.to("#{i}a{k}",{{keyframes:[{",".join(kf)}],duration:{dd},ease:"power1.inOut"}},{r["t"]:.3f});')


def L_regua(c, L):
    """linha do tempo: régua de anos correndo + ano gigante."""
    i = c.nid("rg")
    y = L.get("y", 120)
    anos = L["anos"]  # [[t, ano, rotulo]]
    a0, a1 = L.get("de", anos[0][1] - 5), L.get("ate", anos[-1][1] + 5)
    px_ano = L.get("px_ano", 60)
    ticks = ""
    for a in range(a0, a1 + 1):
        x = (a - a0) * px_ano
        big = a % 10 == 0
        ticks += f'<div style="position:absolute;left:{x}px;top:{0 if big else 18}px;width:4px;height:{60 if big else 24}px;background:{L.get("cor", "#f6efdc")}"></div>'
        if big:
            ticks += f'<div style="position:absolute;left:{x - 60}px;top:66px;width:124px;text-align:center;font:800 30px Montserrat;color:{L.get("cor", "#f6efdc")}">{a}</div>'
    inner = (f'<div id="{i}" style="position:absolute;left:0;top:{y}px;width:{W}px;height:240px;overflow:hidden">'
             f'<div id="{i}r" style="position:absolute;left:0;top:30px;width:{(a1 - a0) * px_ano + 10}px;height:120px">{ticks}</div>'
             f'<div style="position:absolute;left:{W / 2 - 3}px;top:0;width:6px;height:150px;background:{PAL["vermelho"]}"></div></div>'
             f'<div id="{i}y" style="position:absolute;left:0;top:{y + 150}px;width:{W}px;text-align:center;font:230px Anton;color:{L.get("cor_ano", PAL["amarelo"])};'
             f'text-shadow:6px 6px 0 #000,0 30px 60px rgba(0,0,0,.6)"><span id="{i}yv">{anos[0][1]}</span></div>'
             f'<div id="{i}l" style="position:absolute;left:60px;top:{y + 400}px;width:{W - 120}px;text-align:center;font:800 46px Montserrat;color:#fff;text-shadow:0 3px 10px #000"></div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    for k, (ta, ano, rot) in enumerate(anos):
        xr = W / 2 - (ano - a0) * px_ano
        dd = .8 if k else .01
        c.tw(f'tl.to("#{i}r",{{x:{xr:.1f},duration:{dd},ease:"power3.inOut"}},{ta:.3f});')
        c.tw(f'(function(){{var o={{v:{anos[k - 1][1] if k else ano}}};tl.to(o,{{v:{ano},duration:{dd},ease:"power3.inOut",onUpdate:function(){{document.getElementById("{i}yv").textContent=Math.round(o.v)}}}},{ta:.3f});}})();')
        c.tw(f'tl.set("#{i}l",{{textContent:{json.dumps(rot)}}},{ta + dd:.3f});tl.fromTo("#{i}l",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.3}},{ta + dd:.3f});')
        c.tw(f'tl.fromTo("#{i}y",{{scale:1.25}},{{scale:1,duration:.35,ease:"back.out(2)"}},{ta + dd:.3f});')


def L_artigo(c, L):
    """página do artigo (reconstruída a partir do PubMed) inclinada em 3D, rolando, com grifo que varre."""
    i = c.nid("ar")
    x, y, w, h = box_style(L)
    linhas = "".join(
        f'<p style="margin:0 0 18px 0;position:relative">' + (f'<span id="{i}g{k}" style="position:absolute;left:-6px;top:4px;height:1.05em;width:0;background:rgba(255,230,0,.75);z-index:0"></span>' if ln.get("grifo") else "")
        + f'<span style="position:relative;z-index:1">{esc(ln["txt"])}</span></p>' for k, ln in enumerate(L["linhas"]))
    inner = (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;perspective:1400px">'
             f'<div id="{i}" style="position:absolute;inset:0;background:#fff;border-radius:8px;box-shadow:0 40px 80px rgba(0,0,0,.55);padding:46px 50px;overflow:hidden;transform-origin:50% 0">'
             f'<div style="font:700 24px Montserrat;color:#8a1c1c;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px">{esc(L.get("revista", ""))}</div>'
             f'<div style="font:700 44px \'Source Serif 4\',serif;color:#111;line-height:1.15;margin-bottom:16px">{esc(L["titulo"])}</div>'
             f'<div style="font:400 24px \'Source Serif 4\',serif;color:#444;margin-bottom:26px">{esc(L.get("autores", ""))}</div>'
             f'<div id="{i}t" style="font:400 31px \'Source Serif 4\',serif;color:#222;line-height:1.4">{linhas}</div>'
             f'<div style="position:absolute;right:30px;bottom:20px;font:600 20px Montserrat;color:#999">{esc(L.get("rodape", ""))}</div></div></div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    c.tw(f'tl.fromTo("#{i}",{{rotationX:40,rotationZ:-8,y:500,opacity:0}},{{rotationX:18,rotationZ:-4,y:0,opacity:1,duration:.6,ease:"power3.out"}},{L["t"]:.3f});')
    c.tw(f'tl.to("#{i}",{{rotationX:8,rotationZ:-2,duration:{L["d"] - .6:.2f},ease:"none"}},{L["t"] + .6:.3f});')
    c.tw(f'tl.fromTo("#{i}t",{{y:0}},{{y:{L.get("rola", -120)},duration:{L["d"]:.2f},ease:"none"}},{L["t"]:.3f});')
    for k, ln in enumerate(L["linhas"]):
        if ln.get("grifo"):
            c.tw(f'tl.to("#{i}g{k}",{{width:"102%",duration:.6,ease:"power2.inOut"}},{ln["grifo"]:.3f});')


def L_pergunta(c, L):
    """caixinha de pergunta do Instagram (gancho do 1º segundo)."""
    i = c.nid("q")
    x, y = L.get("xy", [140, 300])
    w = L.get("w", 800)
    botoes = ""
    if L.get("botoes"):
        botoes = (f'<div style="display:flex;gap:20px;margin-top:26px">'
                  + "".join(f'<div id="{i}b{k}" style="flex:1;padding:22px 0;border-radius:24px;background:{cor};font:900 44px Montserrat;color:#fff;text-align:center">{esc(b)}</div>'
                            for k, (b, cor) in enumerate(zip(L["botoes"], [PAL["vermelho"], "#1fbf5b", "#f39c12"])))
                  + '</div>')
    inner = (f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;border-radius:40px;overflow:hidden;background:#fff;box-shadow:0 30px 70px rgba(0,0,0,.5)">'
             f'<div style="padding:30px 36px;background:linear-gradient(90deg,#f9ce34,#ee2a7b,#6228d7);font:800 40px Montserrat;color:#fff;text-align:center">{esc(L.get("topo", "Faça uma pergunta"))}</div>'
             f'<div style="padding:34px 40px 40px">'
             f'<div id="{i}t" style="font:700 52px Montserrat;color:#111;line-height:1.15;text-align:center">'
             + "".join(f'<span class="{i}c" style="opacity:0">{esc(ch)}</span>' for ch in L["txt"]) + f'</div>{botoes}</div></div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z", 70))
    c.tw(f'tl.fromTo("#{i}",{{scale:.2,rotation:-10,opacity:0}},{{scale:1,rotation:-2,opacity:1,duration:.35,ease:"back.out(2.2)"}},{L["t"]:.3f});')
    c.tw(f'tl.to(".{i}c",{{opacity:1,duration:.01,stagger:{L.get("vel", .03)}}},{L["t"] + .25:.3f});')
    if L.get("botoes"):
        tb = L.get("t_botoes", L["t"] + .25 + len(L["txt"]) * L.get("vel", .03))
        c.tw(f'tl.fromTo("#{i} [id^={i}b]",{{scale:0}},{{scale:1,duration:.25,stagger:.08,ease:"back.out(3)"}},{tb:.3f});')
        if L.get("escolha") is not None:
            c.tw(f'tl.to("#{i}b{L["escolha"]}",{{scale:1.15,boxShadow:"0 0 0 8px #fff,0 0 0 16px #111",duration:.2,yoyo:true,repeat:1}},{L.get("t_escolha", tb + .8):.3f});')


def L_comentario(c, L):
    i = c.nid("cm")
    x, y = L.get("xy", [60, 260])
    w = L.get("w", 960)
    inner = (f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:28px 32px;border-radius:34px;background:#fff;box-shadow:0 20px 50px rgba(0,0,0,.45);display:flex;gap:24px;align-items:flex-start">'
             f'<div style="flex:0 0 90px;height:90px;border-radius:50%;background:linear-gradient(135deg,#f9ce34,#ee2a7b)"></div>'
             f'<div><div style="font:800 32px Montserrat;color:#111">{esc(L.get("user", "@seguidor"))} <span style="font-weight:500;color:#999">· agora</span></div>'
             f'<div style="font:500 44px Montserrat;color:#111;line-height:1.2;margin-top:8px">'
             + "".join(f'<span class="{i}c" style="opacity:0">{esc(ch)}</span>' for ch in L["txt"]) + '</div>'
             f'<div style="font:700 28px Montserrat;color:#999;margin-top:14px">Responder &nbsp; ♥ {esc(L.get("curtidas", "1.204"))}</div></div></div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z", 70))
    c.tw(f'tl.fromTo("#{i}",{{y:300,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"back.out(1.6)"}},{L["t"]:.3f});')
    c.tw(f'tl.to(".{i}c",{{opacity:1,duration:.01,stagger:{L.get("vel", .035)}}},{L["t"] + .2:.3f});')


def L_manchete(c, L):
    i = c.nid("mc")
    x, y = L.get("xy", [40, 300])
    w = L.get("w", 1000)
    inner = (f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:26px 34px 30px;background:#f3efe6;box-shadow:0 26px 60px rgba(0,0,0,.5);'
             f'background-image:radial-gradient(rgba(0,0,0,.06) 1px,transparent 1px);background-size:6px 6px">'
             f'<div style="font:900 30px \'Source Serif 4\',serif;color:#111;border-bottom:4px double #111;padding-bottom:8px;margin-bottom:14px;letter-spacing:3px;text-transform:uppercase">{esc(L.get("jornal", "Jornal"))} <span style="float:right;font:600 22px Montserrat">{esc(L.get("data", ""))}</span></div>'
             f'<div style="font:900 70px \'Source Serif 4\',serif;color:#111;line-height:1.02">{esc(L["txt"])}</div>'
             + (f'<div style="font:400 30px \'Source Serif 4\',serif;color:#333;margin-top:12px">{esc(L["sub"])}</div>' if L.get("sub") else "")
             + '</div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    enter(c, f"#{i}", dict(L, entra=L.get("entra", "cai")), L["t"])


def L_checklist(c, L):
    """bloco de notas com itens que entram e são marcados."""
    i = c.nid("ck")
    x, y, w, h = box_style(L)
    itens = ""
    for k, it in enumerate(L["itens"]):
        itens += (f'<div id="{i}i{k}" style="display:flex;align-items:center;gap:24px;margin:0 0 30px 0;opacity:0">'
                  f'<div style="position:relative;flex:0 0 64px;height:64px;border:5px solid #1c1a17;border-radius:12px">'
                  f'<svg width="80" height="80" viewBox="0 0 80 80" style="position:absolute;left:-4px;top:-14px"><path id="{i}k{k}" d="M12 42 L32 62 L74 8" fill="none" stroke="{PAL["vermelho"]}" stroke-width="10" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/></svg></div>'
                  f'<div style="font:64px Caveat;color:#1c1a17;line-height:1">{esc(it["txt"])}</div></div>')
    inner = (f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff8c9;border-radius:10px;box-shadow:0 26px 60px rgba(0,0,0,.45);'
             f'background-image:repeating-linear-gradient(0deg,transparent 0 93px,rgba(70,120,200,.35) 93px 95px);padding:120px 50px 40px 110px">'
             f'<div style="position:absolute;left:84px;top:0;bottom:0;width:3px;background:rgba(220,60,60,.5)"></div>'
             f'<div style="position:absolute;left:110px;top:28px;font:900 44px Montserrat;color:#1c1a17;text-transform:uppercase">{esc(L.get("titulo", ""))}</div>{itens}</div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z"))
    enter(c, f"#{i}", dict(L, entra=L.get("entra", "desliza")), L["t"])
    for k, it in enumerate(L["itens"]):
        c.tw(f'tl.fromTo("#{i}i{k}",{{x:-80,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"power3.out"}},{it["t"]:.3f});')
        if it.get("marca"):
            c.tw(f'tl.to("#{i}k{k}",{{strokeDashoffset:0,duration:.3,ease:"power2.out"}},{it["marca"]:.3f});')


def L_barra(c, L):
    """barra fixa no topo com a pergunta (padrão Sermed/Johnny)."""
    i = c.nid("bt")
    inner = (f'<div id="{i}" style="position:absolute;left:40px;top:{L.get("y", 60)}px;width:{W - 80}px;padding:20px 30px;border-radius:24px;background:{L.get("cor", "#fff")};'
             f'font:900 40px Montserrat;color:{L.get("cor_txt", "#111")};text-align:center;box-shadow:0 12px 30px rgba(0,0,0,.35)">{esc(L["txt"])}</div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z", 85))
    c.tw(f'tl.fromTo("#{i}",{{y:-200}},{{y:0,duration:.4,ease:"back.out(1.6)"}},{L["t"]:.3f});')


def L_flash(c, L):
    i = c.nid("fl")
    cor = L.get("cor", "#fff")
    c.clip(f'<div id="{i}" style="position:absolute;inset:0;background:{cor};opacity:0"></div>', L["t"], L.get("d", .3), z=L.get("z", 95))
    c.tw(f'tl.fromTo("#{i}",{{opacity:{L.get("max", .85)}}},{{opacity:0,duration:{L.get("d", .3)},ease:"power2.out"}},{L["t"]:.3f});')


def L_glitch(c, L):
    i = c.nid("gl")
    d = L.get("d", .35)
    bars = "".join(f'<div style="position:absolute;left:0;top:{c.rng.randint(0, H)}px;width:{W}px;height:{c.rng.randint(8, 70)}px;background:{c.rng.choice(["#ff2d3d", "#35e0ff", "#c6ff3d", "#fff"])};mix-blend-mode:screen;opacity:.8"></div>' for _ in range(14))
    c.clip(f'<div id="{i}" style="position:absolute;inset:0">{bars}</div>', L["t"], d, z=L.get("z", 96))
    c.tw(f'tl.fromTo("#{i}",{{x:-40}},{{x:40,duration:.05,repeat:{int(d / .05)},yoyo:true}},{L["t"]:.3f});')


def L_progresso(c, L):
    i = c.nid("pg")
    c.clip(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:12px;background:rgba(0,0,0,.35)"><div id="{i}" style="width:100%;height:100%;background:{L.get("cor", PAL["lima"])};transform-origin:0 0;transform:scaleX(0)"></div></div>', 0, c.dur, z=99)
    c.tw(f'tl.fromTo("#{i}",{{scaleX:0}},{{scaleX:1,duration:{c.dur},ease:"none"}},0);')


def L_vinheta(c, L):
    c.clip('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.55) 100%);pointer-events:none"></div>', 0, c.dur, z=97)


def L_grao(c, L):
    i = c.nid("gr")
    svg = ("data:image/svg+xml;utf8," + "<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='.55'/></svg>")
    c.clip(f'<div id="{i}" style="position:absolute;inset:-100px;background-image:url(&quot;{svg}&quot;);opacity:{L.get("op", .10)};mix-blend-mode:overlay"></div>', 0, c.dur, z=98)
    c.tw(f'tl.fromTo("#{i}",{{x:0,y:0}},{{x:-90,y:-60,duration:{c.dur},ease:"steps({int(c.dur * 12)})"}},0);')


def L_cta(c, L):
    """tela final com marca e referência."""
    i = c.nid("ct")
    inner = (f'<div id="{i}" style="position:absolute;inset:0;background:{PAL["fundo"]};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px">'
             f'<div style="font:150px Anton;color:{PAL["lima"]};letter-spacing:4px">{esc(L.get("marca", "PAPO DE MÉDICO"))}</div>'
             f'<div style="font:800 46px Montserrat;color:#fff">{esc(L.get("frase", ""))}</div>'
             f'<div style="font:500 30px Montserrat;color:#bbb;max-width:900px;text-align:center;line-height:1.35">{esc(L.get("ref", ""))}</div></div>')
    c.clip(inner, L["t"], L["d"], z=L.get("z", 90))
    c.tw(f'tl.fromTo("#{i}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(80% at 50% 50%)",duration:.5,ease:"power3.inOut"}},{L["t"]:.3f});')


# ======================= legendas =======================

LEG_KEY = set()


def legendas(c, P):
    LG = P.get("legenda")
    if not LG:
        return
    words = []
    for seg in P["audio"].get("voz", []):
        if not seg.get("palavras"):
            continue
        ws = json.load(open(seg["palavras"]))
        a, b = seg.get("ms", 0), seg.get("ms", 0) + seg["d"]
        for w in ws:
            if w["s"] >= a - .05 and w["e"] <= b + .2:
                words.append(dict(w=w["w"], s=w["s"] - a + seg["t"], e=min(w["e"], b) - a + seg["t"]))
    words = [w for w in words if w["w"]]
    juntas = []  # o "%" que o transcritor solta sozinho volta para o número
    for w in words:
        if juntas and w["w"].strip().rstrip(".,") == "%":
            juntas[-1] = dict(juntas[-1], w=juntas[-1]["w"] + w["w"].strip(), e=w["e"])
        else:
            juntas.append(w)
    words = juntas
    for (a, b) in LG.get("esconde", []):
        words = [w for w in words if not (a <= w["s"] < b)]
    estilo = LG.get("estilo", "lima")
    chave = set(k.lower() for k in LG.get("chave", []))
    y = LG.get("y", 1500)
    y_base, ys = y, LG.get("ys", [])  # ys: [[t0, t1, y], ...] muda a altura da legenda por trecho

    def y_em(t):
        for (a, b, yy) in ys:
            if a <= t < b:
                return yy
        return y_base
    if estilo == "gigante":
        cores = [PAL["lima"], PAL["amarelo"], PAL["ciano"], "#ffffff", PAL["rosa"]]
        for k, w in enumerate(words):
            d = (words[k + 1]["s"] if k + 1 < len(words) else w["e"] + .3) - w["s"]
            d = max(.08, min(d, 1.2))
            i = c.nid("lg")
            cor = cores[k % len(cores)]
            c.clip(f'<div id="{i}" style="position:absolute;left:0;top:{y}px;width:{W}px;text-align:center;font:150px Anton;color:{cor};text-transform:uppercase;-webkit-text-stroke:10px #000;paint-order:stroke fill">{esc(w["w"].strip(".,?!"))}</div>',
                   w["s"], d, z=88)
            c.tw(f'tl.fromTo("#{i}",{{scale:.5}},{{scale:1,duration:.12,ease:"back.out(3)"}},{w["s"]:.3f});')
        return
    if estilo == "maquina":
        grp = 6
    elif estilo in ("serif", "manuscrita"):
        grp = 4
    else:
        grp = 3
    grupos, cur = [], []
    for w in words:
        # grupo novo: encheu, houve pausa, ou a palavra anterior fechou a frase (a legenda não adianta a frase seguinte)
        if cur and (len(cur) >= grp or w["s"] - cur[-1]["e"] > .45 or cur[-1]["w"].strip().endswith((".", "?", "!", "…"))):
            grupos.append(cur); cur = []
        cur.append(w)
    if cur:
        grupos.append(cur)
    for gi, g in enumerate(grupos):
        t0 = g[0]["s"]
        y = y_em(t0)
        t1 = grupos[gi + 1][0]["s"] if gi + 1 < len(grupos) else g[-1]["e"] + .4
        t1 = min(t1, g[-1]["e"] + .6)
        i = c.nid("lg")
        if estilo == "lima":
            spans = " ".join(f'<span id="{i}w{k}" style="color:{PAL["amarelo"] if w["w"].lower().strip(".,?!") in chave else "#fff"}">{esc(w["w"].upper())}</span>' for k, w in enumerate(g))
            box = f'font:900 70px Montserrat;-webkit-text-stroke:12px #000;paint-order:stroke fill;'
        elif estilo == "serif":
            spans = " ".join(f'<span id="{i}w{k}" style="opacity:0">{esc(w["w"])}</span>' for k, w in enumerate(g))
            box = "font:italic 600 66px 'Source Serif 4',serif;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.9);"
        elif estilo == "pilula":
            spans = " ".join(f'<span id="{i}w{k}" style="padding:2px 10px;border-radius:12px">{esc(w["w"])}</span>' for k, w in enumerate(g))
            box = "display:inline-block;font:800 58px Montserrat;color:#111;background:#fff;border-radius:26px;padding:14px 26px;box-shadow:0 10px 24px rgba(0,0,0,.35);"
        elif estilo == "manuscrita":
            spans = " ".join(f'<span id="{i}w{k}" style="opacity:0">{esc(w["w"])}</span>' for k, w in enumerate(g))
            box = "font:88px Caveat;color:#fff;text-shadow:0 3px 0 #000,0 0 18px rgba(0,0,0,.8);"
        else:  # maquina
            txt = " ".join(w["w"] for w in g)
            spans = "".join(f'<span class="{i}c" style="opacity:0">{esc(ch)}</span>' for ch in txt)
            box = "display:inline-block;font:700 54px 'Courier Prime',monospace;color:#111;background:#f6efdc;padding:12px 22px;"
        inner = f'<div style="position:absolute;left:60px;top:{y}px;width:{W - 120}px;text-align:center"><div id="{i}" style="{box}line-height:1.15">{spans}</div></div>'
        c.clip(inner, t0, max(.1, t1 - t0), z=88)
        for k, w in enumerate(g):
            if estilo == "lima":
                cor = PAL["lima"]
                base = PAL["amarelo"] if w["w"].lower().strip(".,?!") in chave else "#fff"
                c.tw(f'tl.set("#{i}w{k}",{{color:"{cor}"}},{w["s"]:.3f});tl.set("#{i}w{k}",{{color:"{base}"}},{w["e"]:.3f});')
            elif estilo in ("serif", "manuscrita"):
                c.tw(f'tl.fromTo("#{i}w{k}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:.12}},{w["s"]:.3f});')
            elif estilo == "pilula":
                c.tw(f'tl.set("#{i}w{k}",{{backgroundColor:"{PAL["amarelo"]}"}},{w["s"]:.3f});tl.set("#{i}w{k}",{{backgroundColor:"transparent"}},{w["e"]:.3f});')
        if estilo == "lima":
            c.tw(f'tl.fromTo("#{i}",{{scale:.85}},{{scale:1,duration:.1,ease:"back.out(3)"}},{t0:.3f});')
        if estilo == "maquina":
            n = len(" ".join(w["w"] for w in g))
            c.tw(f'tl.to(".{i}c",{{opacity:1,duration:.01,stagger:{min(.04, (g[-1]["e"] - t0) / max(n, 1)):.4f}}},{t0:.3f});')


def camera(c, P):
    """Câmera na mão: deriva lenta de escala/posição/giro em tudo abaixo da legenda.
    Motivo (13/11): telas de narração paradas reprovavam no portão (37% parado no react da cúrcuma)."""
    cam = P.get("camera")
    if not cam:
        return
    amp = cam.get("amp", 1.0) if isinstance(cam, dict) else 1.0
    r = random.Random(P.get("seed", 7) + 99)
    c.tw('gsap.set(".cam",{transformOrigin:"50% 45%",scale:1.08});')
    # cada eixo no seu período: a velocidade nunca zera em todos ao mesmo tempo (câmera na mão, não vai e volta)
    for prop, lo, hi, p0, p1 in (("scale", 1.06, 1.12, 2.6, 3.4), ("x", -18 * amp, 18 * amp, 2.1, 2.9),
                                 ("y", -16 * amp, 16 * amp, 1.7, 2.5), ("rotation", -.55 * amp, .55 * amp, 3.1, 3.9)):
        t, lado = 0.0, r.choice([0, 1])
        while t < c.dur:
            d = r.uniform(p0, p1)
            alvo = (hi if lado else lo) * 1.0
            if prop != "scale":
                alvo *= r.uniform(.6, 1.0)
            c.tw(f'tl.to(".cam",{{{prop}:{alvo:.3f},duration:{min(d, c.dur - t):.2f},ease:"sine.inOut"}},{t:.2f});')
            t += d
            lado = 1 - lado


TIPOS = dict(fundo=L_fundo, foto=L_foto, video=L_video, recorte=L_recorte, cartao=L_cartao, desenho=L_desenho,
             texto=L_texto, gigante=L_gigante, carimbo=L_carimbo, numero=L_numero, celular=L_celular, mapa=L_mapa,
             regua=L_regua, artigo=L_artigo, pergunta=L_pergunta, comentario=L_comentario, manchete=L_manchete,
             checklist=L_checklist, barra=L_barra, flash=L_flash, glitch=L_glitch, progresso=L_progresso,
             vinheta=L_vinheta, grao=L_grao, cta=L_cta)


def gerar(plano_path, out):
    P = json.load(open(plano_path))
    c = Comp(P)
    for L in P["camadas"]:
        TIPOS[L["tipo"]](c, L)
    legendas(c, P)
    camera(c, P)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fontes = "".join(f"@font-face{{font-family:'{n}';src:url('assets/fonts/{f}.ttf')}}" for n, f in
                     [("Anton", "Anton-Regular"), ("Caveat", "Caveat"), ("Courier Prime", "CourierPrime"), ("Source Serif 4", "SourceSerif4")])
    doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{fontes}*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
#root{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{P.get("fundo", "#0b1512")}}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{c.dur}" data-width="{W}" data-height="{H}"
 data-layout-allow-overflow data-layout-allow-overlap>
{chr(10).join(c.html)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(c.js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
    (out / "index.html").write_text(doc)
    for f in ("hyperframes.json", "package.json", "meta.json"):
        src = AQUI / f
        if src.exists() and not (out / f).exists():
            (out / f).write_text(src.read_text())
    a = out / "assets"
    if not a.exists():
        a.symlink_to(AQUI / "assets")
    print("ok", out / "index.html", len(c.html), "elementos")


if __name__ == "__main__":
    gerar(sys.argv[1], sys.argv[2])
