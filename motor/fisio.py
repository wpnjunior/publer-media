"""Camada "fisio": aula rápida de fisiologia com desenho dos órgãos atuando (Wagner, 14/11 00h33).

Plano:
{"tipo":"fisio","t":T,"d":D,"z":40,
 "orgaos":[{"k":"musculo","xy":[cx,cy],"s":1.0,"t":0.0,"rotulo":"MÚSCULO","estado":"normal|murcha|forte"}],
 "fluxos":[{"de":[x,y],"para":[x,y],"curva":-160,"cor":"#ffd400","t":1.2,"d":3.0,"n":7,"rotulo":"aminoácidos","r":13}],
 "pulsos":[{"o":0,"t":2.0}],          # órgão (índice) dá um pulso no tempo relativo t
 "encolhe":[{"o":0,"t":3.0,"para":0.8}]}  # órgão encolhe (músculo perdendo)
Órgãos: musculo, figado, gordura, cerebro, neuronio, xicara, prato, haltere, celula.
Tudo respira devagar (nunca fica parado) e entra com mola.
"""
import math

ART = {
    "musculo": '''<g>
      <path d="M-170 0 C-120 -95 -40 -120 0 -118 C40 -120 120 -95 170 0 C120 95 40 120 0 118 C-40 120 -120 95 -170 0 Z" fill="#c8323a" stroke="#5c0f14" stroke-width="7"/>
      <path d="M-150 -18 C-80 -70 80 -70 150 -18" fill="none" stroke="#e8646a" stroke-width="6" opacity=".9"/>
      <path d="M-160 8 C-80 -38 80 -38 160 8" fill="none" stroke="#e8646a" stroke-width="6" opacity=".8"/>
      <path d="M-150 34 C-80 -6 80 -6 150 34" fill="none" stroke="#e8646a" stroke-width="6" opacity=".7"/>
      <path d="M-130 60 C-70 28 70 28 130 60" fill="none" stroke="#e8646a" stroke-width="6" opacity=".6"/>
      <path d="M-170 0 L-235 0" stroke="#efe2c8" stroke-width="26" stroke-linecap="round"/>
      <path d="M170 0 L235 0" stroke="#efe2c8" stroke-width="26" stroke-linecap="round"/>
      <ellipse cx="-40" cy="-62" rx="46" ry="14" fill="#fff" opacity=".22"/></g>''',
    "figado": '''<g>
      <path d="M-190 -40 C-170 -120 -40 -125 60 -110 C150 -96 210 -70 205 -30 C198 20 120 40 40 70 C-20 92 -70 120 -110 110 C-160 96 -205 30 -190 -40 Z" fill="#8a2f2a" stroke="#3d100d" stroke-width="7"/>
      <path d="M-10 -112 C-20 -40 -30 20 -60 95" fill="none" stroke="#3d100d" stroke-width="5" opacity=".6"/>
      <path d="M-30 50 C0 70 20 90 10 120" fill="none" stroke="#2f6a3a" stroke-width="10" stroke-linecap="round"/>
      <ellipse cx="-90" cy="-60" rx="55" ry="16" fill="#fff" opacity=".18"/></g>''',
    "gordura": '''<g>
      <circle cx="-70" cy="-30" r="62" fill="#f6d26b" stroke="#a77d12" stroke-width="6"/>
      <circle cx="50" cy="-50" r="56" fill="#f6d26b" stroke="#a77d12" stroke-width="6"/>
      <circle cx="-10" cy="55" r="66" fill="#f6d26b" stroke="#a77d12" stroke-width="6"/>
      <circle cx="105" cy="45" r="48" fill="#f6d26b" stroke="#a77d12" stroke-width="6"/>
      <circle cx="-120" cy="60" r="40" fill="#f6d26b" stroke="#a77d12" stroke-width="6"/>
      <circle cx="-88" cy="-50" r="14" fill="#fff" opacity=".45"/><circle cx="34" cy="-70" r="12" fill="#fff" opacity=".45"/>
      <circle cx="-28" cy="32" r="15" fill="#fff" opacity=".45"/></g>''',
    "cerebro": '''<g>
      <path d="M-170 10 C-190 -70 -120 -140 -40 -135 C0 -165 80 -150 110 -110 C175 -100 200 -30 175 30 C190 80 140 125 80 115 C40 145 -30 140 -60 110 C-130 125 -175 75 -170 10 Z" fill="#f2a3b3" stroke="#7a2b3e" stroke-width="7"/>
      <path d="M-120 -60 C-90 -90 -50 -70 -60 -40 C-70 -10 -30 0 -10 -25 M10 -110 C0 -70 40 -60 60 -80 M90 -40 C60 -20 80 20 120 10 M-130 40 C-100 20 -70 50 -90 80 M-20 40 C10 20 40 50 20 90 M60 60 C80 40 120 60 110 90" fill="none" stroke="#7a2b3e" stroke-width="6" stroke-linecap="round"/>
      <path d="M0 -150 C-6 -60 6 40 -4 130" fill="none" stroke="#7a2b3e" stroke-width="5" opacity=".5"/></g>''',
    "neuronio": '''<g>
      <circle cx="-120" cy="0" r="58" fill="#7fb7ff" stroke="#1f3f7a" stroke-width="7"/>
      <circle cx="-120" cy="0" r="20" fill="#1f3f7a"/>
      <path d="M-170 -40 L-220 -90 M-175 30 L-230 60 M-130 -58 L-140 -120 M-62 0 L60 0" stroke="#1f3f7a" stroke-width="12" stroke-linecap="round" fill="none"/>
      <path d="M60 -38 C90 -38 100 -20 100 0 C100 20 90 38 60 38 Z" fill="#7fb7ff" stroke="#1f3f7a" stroke-width="7"/>
      <path d="M150 -70 C130 -40 130 40 150 70 L220 70 L220 -70 Z" fill="#ffb37f" stroke="#7a3b10" stroke-width="7"/>
      <circle cx="180" cy="-30" r="9" fill="#7a3b10"/><circle cx="180" cy="30" r="9" fill="#7a3b10"/><circle cx="170" cy="0" r="9" fill="#7a3b10"/></g>''',
    "xicara": '''<g>
      <path d="M-110 -60 L110 -60 L90 90 C85 115 -85 115 -90 90 Z" fill="#f4f1e8" stroke="#3a2a1f" stroke-width="8"/>
      <ellipse cx="0" cy="-60" rx="110" ry="24" fill="#5a3418" stroke="#3a2a1f" stroke-width="8"/>
      <path d="M108 -30 C170 -30 170 50 96 50" fill="none" stroke="#3a2a1f" stroke-width="16"/>
      <path d="M-40 -100 C-60 -130 -20 -150 -40 -180 M10 -100 C-10 -130 30 -150 10 -180 M60 -100 C40 -130 80 -150 60 -180" fill="none" stroke="#bbb" stroke-width="8" stroke-linecap="round" opacity=".8"/></g>''',
    "prato": '''<g>
      <ellipse cx="0" cy="0" rx="190" ry="70" fill="#f4f1e8" stroke="#555" stroke-width="7"/>
      <ellipse cx="0" cy="-4" rx="130" ry="44" fill="none" stroke="#bbb" stroke-width="5"/>
      <ellipse cx="-30" cy="-12" rx="70" ry="26" fill="#b5651d" stroke="#6b3a10" stroke-width="5"/>
      <circle cx="60" cy="-10" r="20" fill="#3c9a4a"/><circle cx="85" cy="5" r="16" fill="#3c9a4a"/></g>''',
    "haltere": '''<g>
      <rect x="-150" y="-14" width="300" height="28" rx="12" fill="#9aa3ad" stroke="#333" stroke-width="6"/>
      <rect x="-190" y="-70" width="46" height="140" rx="12" fill="#2c2f36" stroke="#111" stroke-width="6"/>
      <rect x="144" y="-70" width="46" height="140" rx="12" fill="#2c2f36" stroke="#111" stroke-width="6"/>
      <rect x="-235" y="-50" width="40" height="100" rx="10" fill="#2c2f36" stroke="#111" stroke-width="6"/>
      <rect x="195" y="-50" width="40" height="100" rx="10" fill="#2c2f36" stroke="#111" stroke-width="6"/></g>''',
    "celula": '''<g>
      <ellipse cx="0" cy="0" rx="170" ry="120" fill="#a9e3c7" stroke="#1f5c42" stroke-width="7"/>
      <circle cx="-20" cy="-10" r="44" fill="#4f9c7a" stroke="#1f5c42" stroke-width="6"/>
      <ellipse cx="80" cy="50" rx="30" ry="14" fill="#f2c94c"/><ellipse cx="-90" cy="55" rx="26" ry="12" fill="#f2c94c"/></g>''',
}


def _rotulo(txt, y, cor):
    return (f'<text x="0" y="{y}" text-anchor="middle" font-family="Anton" font-size="56" fill="{cor}" '
            f'stroke="#000" stroke-width="10" paint-order="stroke fill" letter-spacing="2">{txt}</text>')


def L_fisio(c, L, W=1080, H=1920):
    i = c.nid("fs")
    t0, d = L["t"], L["d"]
    cor_rot = L.get("cor_rotulo", "#ffffff")
    corpo = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0;overflow:visible">'
    # fluxos: caminho + partículas (offset-path, avançam no tempo da timeline)
    css = ""
    for k, f in enumerate(L.get("fluxos", [])):
        (x0, y0), (x1, y1) = f["de"], f["para"]
        cv = f.get("curva", -140)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + cv
        pth = f"M{x0} {y0} Q{mx} {my} {x1} {y1}"
        cor = f.get("cor", "#ffd400")
        corpo += (f'<path id="{i}f{k}" d="{pth}" fill="none" stroke="{cor}" stroke-width="5" stroke-dasharray="14 16" '
                  f'opacity="0" stroke-linecap="round"/>')
        if f.get("rotulo"):
            corpo += (f'<g transform="translate({mx:.0f},{(y0 + y1) / 2 + cv * 0.5 - 26:.0f})"><g id="{i}fr{k}" opacity="0">'
                      f'<text x="0" y="0" text-anchor="middle" font-family="Anton" font-size="50" letter-spacing="1" '
                      f'fill="{cor}" stroke="#000" stroke-width="9" paint-order="stroke fill">{f["rotulo"]}</text></g></g>')
    corpo += "</svg>"
    parts = ""
    for k, f in enumerate(L.get("fluxos", [])):
        (x0, y0), (x1, y1) = f["de"], f["para"]
        cv = f.get("curva", -140)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + cv
        r = f.get("r", 13)
        for j in range(f.get("n", 7)):
            parts += (f'<div class="{i}p{k}" id="{i}p{k}_{j}" style="position:absolute;left:0;top:0;width:{2 * r}px;height:{2 * r}px;'
                      f'margin:-{r}px 0 0 -{r}px;border-radius:50%;background:{f.get("cor", "#ffd400")};border:4px solid #000;opacity:0;'
                      f"offset-path:path('M{x0} {y0} Q{mx} {my} {x1} {y1}');offset-rotate:0deg;offset-distance:0%\"></div>")
    orgs = ""
    for k, o in enumerate(L.get("orgaos", [])):
        cx, cy = o["xy"]
        s = o.get("s", 1.0)
        rot = (_rotulo(o["rotulo"], o.get("rot_y", 190), o.get("cor_rotulo", cor_rot)) if o.get("rotulo") else "")
        orgs += (f'<div id="{i}o{k}" style="position:absolute;left:{cx - 300}px;top:{cy - 300}px;width:600px;height:600px;transform:scale(0);opacity:0">'
                 f'<svg width="600" height="600" viewBox="-300 -300 600 600" style="overflow:visible">'
                 f'<g id="{i}og{k}" transform="scale({s})">{ART[o["k"]]}{rot}</g></svg></div>')
    c.clip(corpo + orgs + parts, t0, d, z=L.get("z", 40))
    # animações
    for k, o in enumerate(L.get("orgaos", [])):
        ta = t0 + o.get("t", 0)
        c.tw(f'tl.fromTo("#{i}o{k}",{{scale:0,opacity:0,rotation:-8}},{{scale:1,opacity:1,rotation:0,duration:.45,ease:"back.out(2.2)"}},{ta:.3f});')
        resto = t0 + d - ta - 0.45
        if resto > 0.4:
            n = max(1, int(resto / 1.1))
            c.tw(f'tl.to("#{i}o{k}",{{y:-10,scale:1.04,duration:{resto / n:.3f},ease:"sine.inOut",yoyo:true,repeat:{n - 1}}},{ta + 0.45:.3f});')
    for p in L.get("pulsos", []):
        c.tw(f'tl.fromTo("#{i}og{p["o"]}",{{filter:"brightness(1.6) drop-shadow(0 0 30px #fff)"}},'
             f'{{filter:"brightness(1) drop-shadow(0 0 0px #fff)",duration:.6,ease:"power2.out",immediateRender:false}},{t0 + p["t"]:.3f});')
    for e in L.get("encolhe", []):
        k = e["o"]
        c.tw(f'tl.to("#{i}og{k}",{{attr:{{transform:"scale({e.get("para", .75)})"}},duration:{e.get("d", 1.2)},ease:"power2.inOut"}},{t0 + e["t"]:.3f});')
        c.tw(f'tl.to("#{i}og{k}",{{filter:"saturate(.45)",duration:{e.get("d", 1.2)}}},{t0 + e["t"]:.3f});')
    for k, f in enumerate(L.get("fluxos", [])):
        tf, df = t0 + f.get("t", 0), f.get("d", 3.0)
        df = min(df, t0 + d - tf - 0.05)
        c.tw(f'tl.to("#{i}f{k}",{{opacity:.9,duration:.25}},{tf:.3f});')
        if f.get("rotulo"):
            c.tw(f'tl.fromTo("#{i}fr{k}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,immediateRender:false}},{tf + 0.2:.3f});')
        n = f.get("n", 7)
        viagem = f.get("viagem", 1.3)
        # o caminho e o rótulo somem depois da viagem (Cariani v2: setas velhas poluíam a cena seguinte)
        if not f.get("fica"):
            tsome = tf + df + 0.35
            if tsome < t0 + d - 0.3:
                c.tw(f'tl.to(["#{i}f{k}","#{i}fr{k}"],{{opacity:0,duration:.35,immediateRender:false}},{tsome:.3f});')
        for j in range(n):
            ts = tf + j * max(0.12, (df - viagem) / max(1, n - 1)) if df > viagem else tf + j * 0.15
            if ts + viagem > t0 + d:
                continue
            c.tw(f'tl.fromTo("#{i}p{k}_{j}",{{offsetDistance:"0%",opacity:1}},{{offsetDistance:"100%",duration:{viagem},ease:"none",immediateRender:false}},{ts:.3f});'
                 f'tl.set("#{i}p{k}_{j}",{{opacity:0}},{ts + viagem:.3f});')


# órgãos extras (fígado/limpeza hepática, 14/11): intestino, vesícula, gota de azeite, bolinha de sabão
ART["intestino"] = '''<g>
      <path d="M-190 -120 C-190 -170 190 -170 190 -120 C190 -70 -150 -80 -150 -30 C-150 20 190 10 190 60 C190 110 -170 100 -170 150 C-170 185 -60 190 0 175" fill="none" stroke="#7a2b3e" stroke-width="64" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M-190 -120 C-190 -170 190 -170 190 -120 C190 -70 -150 -80 -150 -30 C-150 20 190 10 190 60 C190 110 -170 100 -170 150 C-170 185 -60 190 0 175" fill="none" stroke="#f0a0a8" stroke-width="48" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M-160 -132 C-60 -150 60 -150 160 -132" fill="none" stroke="#fff" stroke-width="8" opacity=".3" stroke-linecap="round"/></g>'''
ART["vesicula"] = '''<g>
      <path d="M0 -150 C10 -110 10 -80 30 -60 C110 -10 120 110 40 150 C-30 180 -110 130 -100 50 C-92 -10 -40 -40 -20 -70 C-10 -90 -10 -120 0 -150 Z" fill="#4f9c3a" stroke="#1f4a14" stroke-width="7"/>
      <ellipse cx="-30" cy="40" rx="30" ry="50" fill="#fff" opacity=".18"/></g>'''
ART["azeite"] = '''<g>
      <path d="M0 -150 C40 -80 110 -10 110 60 C110 125 60 160 0 160 C-60 160 -110 125 -110 60 C-110 -10 -40 -80 0 -150 Z" fill="#c9b52a" stroke="#6b5a08" stroke-width="7"/>
      <ellipse cx="-40" cy="40" rx="22" ry="44" fill="#fff" opacity=".35"/></g>'''
ART["sabao"] = '''<g>
      <circle cx="-70" cy="-20" r="58" fill="#b9c94a" stroke="#5d6a12" stroke-width="6"/>
      <circle cx="55" cy="-45" r="48" fill="#c8d65a" stroke="#5d6a12" stroke-width="6"/>
      <circle cx="10" cy="60" r="64" fill="#a9bb3c" stroke="#5d6a12" stroke-width="6"/>
      <circle cx="110" cy="50" r="38" fill="#c8d65a" stroke="#5d6a12" stroke-width="6"/>
      <circle cx="-88" cy="-40" r="14" fill="#fff" opacity=".5"/><circle cx="40" cy="-62" r="11" fill="#fff" opacity=".5"/><circle cx="-8" cy="38" r="15" fill="#fff" opacity=".5"/></g>'''


# Órgãos extras sem editar este arquivo (vários ajudantes trabalham ao mesmo tempo):
# cada fisio_extra/<nome>.svg contém só o <g>...</g> do desenho (centro em 0,0; cabe em ±200).
import glob as _glob, os as _os
for _f in _glob.glob(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "fisio_extra", "*.svg")):
    ART[_os.path.splitext(_os.path.basename(_f))[0]] = open(_f, encoding="utf-8").read()
