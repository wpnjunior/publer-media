import sys, json, copy, wave; sys.path.insert(0, 'scripts')
from mk import T, F, B, M
# Paraguai com AULA, v2 (14/11 manhã): regras novas do Wagner.
# - Edição FULL na aula, sem b-roll: palavras gigantes Anton (cheias e só contorno), um desenho grande por cena
#   sobre fundo escuro com grão; número "ATÉ 39% A MAIS" com sombra 3D, artigo em perspectiva com grifo, carimbo,
#   celular com a manchete.
# - Voz em blocos por clima, sem atempo: pg2_b1_voz (indignado: "não sei a causa..." + fecho),
#   pg2_estudo_voz (neutro: o estudo), pg_aula_voz (aula: mesma tomada já paga, agora a 1,15 com pausas de 0,5 s).
# - Rostos (entrada, r1, CTA) e o viral ficam iguais ao react_paraguai.json (pele lab).
# A aula NÃO sugere que a caneta causou o caso da reportagem: sem paciente, hospital, sintoma.
SRC, PID = 'planos/react_paraguai.json', 'react_paraguai_aula'
p = json.load(open(SRC))
def W(f): return json.load(open(M + f + '.words.json'))
def dur(f):
    with wave.open(M + f + '.wav') as w: return round(w.getnframes() / w.getframerate(), 3)
def acha(ws, txt, depois=0.0):
    return next(w for w in ws if w['w'].strip('.,?:!%').lower() == txt.lower() and w['s'] >= depois)
WB, WA, WS = W('pg2_b1_voz'), W('pg_aula_voz'), W('pg2_estudo_voz')
LB, LA, LS = dur('pg2_b1_voz'), dur('pg_aula_voz'), dur('pg2_estudo_voz')
r = lambda v: round(v, 3)

# ---------- linha do tempo ----------
B0 = 14.25                                   # fim do rosto r1 (igual ao plano atual)
frio = acha(WB, 'frio')
dB = r(frio['e'] + 0.35)                     # bloco B: "Não sei a causa ... nem se viajou no frio."
A = r(B0 + frio['e'] + 0.8)                  # aula (respiro de 0,8 s depois de "frio.")
S = r(A + WA[-1]['e'] + 0.8)                 # estudo
C = r(S + WS[-1]['e'] + 0.6)                 # rosto CTA (arquivo antigo)
FC = r(C + 4.55 + 0.05)                      # fecho
can = acha(WB, 'caneta', 11.0)
msF = r(can['s'] - 0.12); dF = r(LB - msF)
DUR = r(FC + dF + 0.6)
b = lambda txt, depois=0.0: r(B0 + acha(WB, txt, depois)['s'])
a = lambda txt, depois=0.0: r(A + acha(WA, txt, depois)['s'])
s = lambda txt, depois=0.0: r(S + acha(WS, txt, depois)['s'])
f = lambda txt: r(FC - msF + acha(WB, txt, 11.0)['s'])
ae = lambda txt, depois=0.0: r(A + acha(WA, txt, depois)['e'])

# ---------- o que fica do plano atual ----------
ant = p['camadas']
base = [c for c in ant if c.get('tipo') == 'fundo' and c.get('t') == 0 and c.get('textura')][0]
base['d'] = DUR
inicio = [c for c in ant if c.get('t') is not None and c['t'] < B0 and c is not base]
cta_old = [c for c in ant if c.get('t') is not None and 36.4 <= c['t'] < 41.0]
OC = 36.5
for c in cta_old:
    c['t'] = r(c['t'] - OC + C)
    if 'zoom' in c: c['zoom'] = [[r(z[0] - OC + C)] + z[1:] for z in c['zoom']]
    c['d'] = min(c['d'], r(C + 4.55 - c['t']))
for c in inicio:
    if c.get('tipo') == 'manchete': c['txt'] = 'CANETA DO PARAGUAI: NEM O HOSPITAL CONSEGUIU ANALISAR'
    if c.get('tipo') == 'pergunta':
        c['txt'] = 'Caneta sem registro: ninguém garante o que tem dentro'; c['escolha'] = 1   # VERDADE
fim = [c for c in ant if c.get('t') is None]   # progresso, vinheta, grão
for c in fim:
    if c.get('tipo') == 'grao': c['op'] = 0.1

SOMBRA = "text-shadow:6px 6px 0 #000,0 0 18px rgba(0,0,0,.8)"
def TT(t, d, txt, y=250, fz="110px Anton", cor="#ffffff", **k):
    k.setdefault("css", SOMBRA)
    return T(t, d, txt, y=y, f=fz, cor=cor, vel=0.09, **k)
def G(t, d, txt, y, cor, cont=False, tam=380, x=None, z=14):
    larg = int(len(txt) * tam * 0.5)
    return {"tipo": "gigante", "t": r(t), "d": r(d), "txt": txt, "y": y, "tam": tam, "cor": cor, "contorno": cont,
            "x": x or [1080, -larg], "z": z}
def FS(t, d, k, xy, sc, rot=None, ry=None, cr=None, **extra):
    o = {"k": k, "xy": xy, "s": sc, "t": 0.0}
    if rot: o["rotulo"] = rot
    if ry: o["rot_y"] = ry
    if cr: o["cor_rotulo"] = cr
    L = {"tipo": "fisio", "t": r(t), "d": r(d), "z": 40, "orgaos": [o]}
    L.update(extra)
    return L
c = []

# ---------- B: "Não sei a causa do caso dela, tá?" + "Quem garante?" (fundo: viral borrado) ----------
qg = b('olha')
c += B('pg_viral_blur.mp4', B0, r(A - B0), 3.5)
c += [{"tipo": "flash", "t": B0, "d": 0.2, "max": 0.6},
      {"tipo": "celular", "t": r(B0 + 0.05), "d": r(qg - B0 - 0.05), "xy": [250, 250], "wh": [580, 1000], "img": M + "pg_filha.jpg", "z": 38,
       "notif": [{"t": r(B0 + 0.5), "app": "Plantão das Redes", "txt": "Caneta do Paraguai: nem o hospital conseguiu analisar"}]},
      TT(b('não'), r(qg - b('não')), "NÃO SEI A CAUSA", y=1300, fz="140px Anton"),
      {"tipo": "checklist", "t": qg, "d": r(A - qg), "box": [120, 260, 840, 520], "titulo": "Quem garante?", "entra": "cai",
       "itens": [{"txt": "o que tem dentro", "t": b('dentro')}, {"txt": "quanto tem", "t": b('quanto')}, {"txt": "se viajou no frio", "t": b('frio')}], "z": 40},
      {"tipo": "carimbo", "t": b('registro'), "d": r(A - b('registro')), "xy": [170, 900], "txt": "SEM REGISTRO", "tam": 120, "rot": -7, "z": 60,
       "blend": "normal", "css": "background:rgba(255,255,255,.9)"}]
for k_, w_ in enumerate(['dentro', 'quanto', 'frio']):
    t_ = r(b(w_) + 0.35)
    c.append({"tipo": "desenho", "t": t_, "d": r(A - t_), "formas": [{"k": "x", "c": [262, 412 + 94 * k_], "s": 34}], "espessura": 12, "z": 45})

# ---------- AULA: fundo escuro com grão, um desenho grande por cena, palavras gigantes ----------
FIM_A = r(S - 0.1)
aula = [{"tipo": "fundo", "t": r(A - 0.35), "d": r(FIM_A - A + 0.35), "cor": "#070d0b", "z": 9},
        {"tipo": "flash", "t": r(A - 0.35), "d": 0.2, "max": 0.5}]
# cena 0: gancho
e1 = a('você')
aula += [TT(r(A - 0.3), r(e1 + 0.6 - A), "QUAL O PROBLEMA?", y=780, fz="160px Anton", anim=None, entra="zoom"),
         G(A - 0.35, e1 + 0.65 - A, "PROBLEMA?", 1250, "#c6ff3d", cont=True, tam=360)]
# cena 1: você come -> o intestino solta um hormônio
c2 = r(a('ele') - 0.15)
aula += [TT(e1 + 0.3, c2 - e1 - 0.3, "O HORMÔNIO DO INTESTINO", cor="#c6ff3d"),
         G(e1, c2 - e1, "VOCÊ COME", 1520, "rgba(198,255,61,.16)", tam=330),
         FS(e1, c2 - e1, "intestino", [540, 980], 1.15, "INTESTINO", 230,
            fluxos=[{"de": [540, 800], "para": [540, 560], "curva": 0, "cor": "#c6ff3d", "t": a('hormônio') - e1 - 0.2, "d": 1.3, "n": 6, "viagem": 0.8, "rotulo": "HORMÔNIO", "fica": True}],
            pulsos=[{"o": 0, "t": a('intestino') - e1}, {"o": 0, "t": a('hormônio') - e1}])]
# cena 2: ele avisa o cérebro: tô cheio
c3 = r(ae('cheio') - 0.05)
aula += [{"tipo": "flash", "t": c2, "d": 0.18, "max": 0.35},
         TT(c2 + 0.05, c3 - c2 - 0.05, "AVISA O CÉREBRO"),
         FS(c2, c3 - c2, "cerebro", [540, 900], 1.2, None, None,
            fluxos=[{"de": [540, 1500], "para": [540, 1130], "curva": 0, "cor": "#c6ff3d", "t": 0.15, "d": 1.3, "n": 6, "viagem": 0.8}],
            pulsos=[{"o": 0, "t": a('cérebro') - c2}, {"o": 0, "t": a('tô') - c2}]),
         G(a('tô') - 0.1, c3 - a('tô') + 0.1, "TÔ CHEIO", 1330, "#ffd400", tam=300, z=42)]
# cena 3: segura o estômago
c4 = r(a('ajuda') + 0.05)
aula += [{"tipo": "flash", "t": c3, "d": 0.18, "max": 0.35},
         TT(c3, c4 - c3, "SEGURA O ESTÔMAGO", cor="#ff8a3d"),
         G(c3, c4 - c3, "DEVAGAR", 1500, "#ff8a3d", cont=True, tam=330),
         FS(c3, c4 - c3, "estomago_pg", [560, 930], 1.35, None, None, pulsos=[{"o": 0, "t": a('estômago') - c3}])]
# cena 4: e ajuda o pâncreas com o açúcar
c5 = r(a('o', a('açúcar') - A + 0.3) - 0.15)       # "O seu dura minutos"
aula += [{"tipo": "flash", "t": c4, "d": 0.18, "max": 0.35},
         TT(c4, c5 - c4, "AJUDA NO AÇÚCAR", cor="#4dd8ff"),
         G(c4, c5 - c4, "AÇÚCAR", 1500, "rgba(77,216,255,.18)", tam=360),
         FS(c4, c5 - c4, "pancreas", [540, 930], 1.3, None, None, pulsos=[{"o": 0, "t": a('pâncreas') - c4}])]
# cena 5: o seu dura minutos / o da caneta pode durar dias
c6 = r(a('veio') - 0.15)
o2 = a('o', a('minutos') - A + 0.3)
aula += [{"tipo": "flash", "t": c5, "d": 0.18, "max": 0.35},
         TT(c5 + 0.05, c6 - c5 - 0.05, "QUANTO TEMPO DURA?"),
         TT(c5 + 0.1, c6 - c5 - 0.1, "O SEU", fz="100px Anton", xy=[10, 470], w=520),
         TT(a('minutos') - 0.05, c6 - a('minutos') + 0.05, "MINUTOS", fz="120px Anton", xy=[30, 1240], w=500, anim=None, entra="zoom"),
         TT(o2 - 0.05, c6 - o2 + 0.05, "O DA CANETA", fz="100px Anton", xy=[600, 400], w=420),
         TT(r(a('dias') - 0.5), r(c6 - a('dias') + 0.5), "DIAS", fz="170px Anton", cor="#f2c230", xy=[550, 1200], w=500, anim=None, entra="zoom",
            css="text-shadow:" + ",".join(f"{k}px {k}px 0 #6b4a00" for k in range(1, 14)) + ",0 30px 40px rgba(0,0,0,.6)"),
         {"tipo": "fisio", "t": c5, "d": r(c6 - c5), "z": 40,
          "orgaos": [{"k": "intestino", "xy": [285, 860], "s": 0.62, "t": 0.1},
                     {"k": "caneta", "xy": [810, 860], "s": 0.85, "t": r(a('caneta') - c5 - 0.3)}],
          "fluxos": [{"de": [285, 1010], "para": [285, 1210], "curva": -10, "cor": "#c6ff3d", "t": 0.4, "d": 1.0, "n": 3, "viagem": 0.5},
                     {"de": [810, 1010], "para": [810, 1170], "curva": -10, "cor": "#c6ff3d", "t": r(a('caneta') - c5), "d": r(c6 - a('caneta') - 0.1), "n": 8, "viagem": 1.4, "fica": True}]}]
# cena 6: veio a mais? não desliga
c7 = r(a('e', a('desliga') - A) - 0.1)
nd = a('não', a('mais') - A)
aula += [{"tipo": "flash", "t": c6, "d": 0.18, "max": 0.35},
         TT(c6, c7 - c6, "A MAIS? NÃO DESLIGA", cor="#ff5a5f"),
         FS(c6, c7 - c6, "caneta", [540, 820], 1.3, None, None,
            fluxos=[{"de": [470, 1000], "para": [540, 1290], "curva": 30, "cor": "#ff2d3d", "t": 0.3, "d": 1.5, "n": 10, "viagem": 0.7, "rotulo": "A MAIS", "fica": True}],
            pulsos=[{"o": 0, "t": a('desliga') - c6}]),
         G(nd - 0.1, c7 - nd + 0.1, "NÃO DESLIGA", 1400, "#ff2d3d", cont=True, tam=330, z=12)]
# cena 7: é igual iogurte: pegou calor, estraga
aula += [{"tipo": "flash", "t": c7, "d": 0.18, "max": 0.35},
         TT(c7 + 0.05, r(a('pegou') - c7 - 0.15), "IGUAL IOGURTE", cor="#ff8fb3"),
         TT(r(a('pegou') - 0.1), r(FIM_A - a('pegou') + 0.1), "PEGOU CALOR, ESTRAGA", cor="#ff5a5f"),
         G(a('calor') - 0.1, FIM_A - a('calor') + 0.1, "CALOR", 1550, "#ff3b30", cont=True, tam=360, z=12),
         {"tipo": "fisio", "t": c7, "d": r(FIM_A - c7), "z": 40,
          "orgaos": [{"k": "iogurte", "xy": [540, 1000], "s": 1.25, "t": 0.1, "rotulo": "= A CANETA", "rot_y": 245},
                     {"k": "termometro", "xy": [860, 680], "s": 0.95, "t": r(a('calor') - c7 - 0.25)}],
          "pulsos": [{"o": 1, "t": r(a('calor') - c7 + 0.1)}],
          "encolhe": [{"o": 0, "t": r(a('estraga') - c7), "para": 0.92, "d": 0.9}]}]
for L in aula: L['fixo'] = True
c += aula

# ---------- ESTUDO (fundo: viral borrado) ----------
c += B('pg_viral_blur.mp4', r(S - 0.1), r(C - S + 0.1), 12.0)
p99, t8, q39, so3 = s('o'), s('tinha'), s('e', 9.5), s('só')
c += [{"tipo": "flash", "t": r(S - 0.1), "d": 0.2, "max": 0.5},
      TT(r(S + 0.05), r(p99 - S - 0.15), "COMPRARAM NA INTERNET", y=290, fz="112px Anton"),
      {"tipo": "artigo", "t": r(S + 0.1), "d": r(p99 - S - 0.25), "box": [90, 560, 900, 820], "revista": "J Med Internet Res · 2024",
       "titulo": "Multifactor Quality and Safety Analysis of (…) Products Sold by Online Sellers Without a Prescription",
       "autores": "Ashraf AR, Mackey TK, … Fittler A · Universidade de Pécs, Hungria",
       "linhas": [{"txt": "6 compras-teste em farmácias on-line ilegais, sem receita.", "grifo": r(s('sem') - 0.1)},
                  {"txt": "Chegaram 3 frascos. As 3 canetas nunca chegaram."},
                  {"txt": "Pureza medida: de 7,7% a 14,4% (o rótulo dizia 99%)."}],
       "rodape": "doi 10.2196/65440", "rola": -40, "z": 40},
      {"tipo": "carimbo", "t": s('sem'), "d": r(p99 - s('sem') - 0.15), "xy": [230, 1250], "txt": "SEM RECEITA", "tam": 120, "rot": -8, "z": 60,
       "blend": "normal", "css": "background:rgba(255,255,255,.9)"},
      {"tipo": "flash", "t": r(p99 - 0.1), "d": 0.2, "max": 0.45},
      {"tipo": "numero", "t": r(p99 - 0.05), "d": r(t8 - p99 - 0.1), "xy": [0, 420], "valor": 99, "suf": "%", "rotulo": "de pureza no rótulo", "tam": 280,
       "cor": "#3ddc84", "sombra": "#0d5a2c", "z": 44},
      {"tipo": "flash", "t": r(t8 - 0.1), "d": 0.2, "max": 0.45},
      TT(r(t8 - 0.05), r(q39 - t8 - 0.1), "TINHA 8 A 14%", y=520, fz="170px Anton", cor="#ff2d3d", anim=None, entra="zoom"),
      G(t8 - 0.05, q39 - t8 - 0.1, "PUREZA", 1050, "#ff2d3d", cont=True, tam=360, z=20),
      {"tipo": "flash", "t": r(q39 - 0.1), "d": 0.2, "max": 0.45},
      TT(r(q39 - 0.05), r(so3 - q39 - 0.1), "QUANTIDADE:", y=330, fz="120px Anton", cor="#ffffff", anim=None),
      {"tipo": "numero", "t": r(s('39') - 0.3), "d": r(so3 - s('39') + 0.2), "xy": [0, 560], "valor": 39, "pre": "ATÉ ", "suf": "% A MAIS", "tam": 230,
       "cor": "#f2c230", "sombra": "#6b4a00", "z": 44},
      {"tipo": "flash", "t": r(so3 - 0.1), "d": 0.2, "max": 0.45},
      TT(r(so3 - 0.05), r(C - so3 - 0.05), "SÓ 3 FRASCOS", y=480, fz="170px Anton", anim=None, entra="zoom"),
      TT(r(s('nenhum') - 0.15), r(C - s('nenhum') + 0.1), "NENHUM DO PARAGUAI", y=900, fz="120px Anton", cor="#f2c230", anim=None, entra="zoom"),
      F(r(S + 0.05), r(C - S - 0.1), "Ashraf et al., J Med Internet Res 2024 · doi 10.2196/65440")]

# ---------- CTA (rosto antigo) ----------
c += cta_old

# ---------- FECHO (fundo: viral borrado) ----------
c += B('pg_viral_blur.mp4', FC, r(DUR - FC), 13.0)
c += [{"tipo": "glitch", "t": r(FC - 0.05), "d": 0.25}, {"tipo": "flash", "t": FC, "d": 0.2, "max": 0.5},
      TT(r(f('caneta') - 0.05), r(f('sem') - f('caneta') - 0.1), "CANETA?", y=380, fz="200px Anton", anim=None, entra="zoom"),
      TT(r(f('conversa') - 0.15), r(f('sem') - f('conversa') + 0.0), "CONVERSA COM SEU MÉDICO", y=700, fz="140px Anton", cor="#3ddc84"),
      G(f('sem') - 0.1, f('não') - f('sem') + 0.1, "DE ONDE VEIO?", 700, "#c6ff3d", tam=300, z=42),
      TT(r(f('não') - 0.05), r(DUR - f('não') + 0.05), "NÃO É TRATAMENTO", y=380, fz="150px Anton"),
      {"tipo": "carimbo", "t": f('loteria'), "d": r(DUR - f('loteria')), "xy": [200, 760], "txt": "LOTERIA", "tam": 190, "rot": -8, "z": 60},
      F(r(f('loteria')), r(DUR - f('loteria')), "Ashraf et al., J Med Internet Res 2024 · doi 10.2196/65440")]

p['camadas'] = [base] + inicio + c + fim
p['dur'] = DUR; p['id'] = PID

# ---------- áudio ----------
V = M + 'pg_voz.wav'; VW = M + 'pg_voz.words.json'
voz = [v for v in p['audio']['voz'] if v['src'] != V]     # entrada + viral
voz += [{"src": V, "t": 11.1, "ms": 0, "d": 3.15, "palavras": VW},                          # rosto r1 (áudio do rosto)
        {"src": M + "pg2_b1_voz.wav", "t": B0, "ms": 0, "d": dB, "palavras": M + "pg2_b1_voz.words.json"},
        {"src": M + "pg_aula_voz.wav", "t": A, "ms": 0, "d": LA, "palavras": M + "pg_aula_voz.words.json"},
        {"src": M + "pg2_estudo_voz.wav", "t": S, "ms": 0, "d": LS, "palavras": M + "pg2_estudo_voz.words.json"},
        {"src": V, "t": C, "ms": 26.1, "d": 4.55, "palavras": VW},                             # rosto CTA (áudio do rosto)
        {"src": M + "pg2_b1_voz.wav", "t": FC, "ms": msF, "d": dF, "palavras": M + "pg2_b1_voz.words.json"}]
p['audio']['voz'] = voz
sfx = [x for x in p['audio']['sfx'] if x['t'] < B0 - 0.06 or abs(x['t'] - 14.2) < 0.01]
sfx += [{"src": "whoosh", "t": B0, "gain": 0.5, "pico": 0.45}, {"src": "notif", "t": r(B0 + 0.5), "gain": 0.4},
        {"src": "papel", "t": qg, "gain": 0.5}, {"src": "boom", "t": b('registro'), "gain": 0.5, "pico": 0.3, "d": 1.2}]
sfx += [{"src": "boing", "t": r(b(w_) + 0.35), "gain": 0.3} for w_ in ['dentro', 'quanto', 'frio']]
sfx += [{"src": "whoosh2", "t": r(A - 0.1), "gain": 0.45}]
sfx += [{"src": "whoosh2" if k_ % 2 else "boing", "t": t_, "gain": 0.3} for k_, t_ in enumerate([e1, c2, c3, c4, c5, c6, c7])]
sfx += [{"src": "riser", "t": r(c6 + 0.2), "gain": 0.22, "d": 1.6}]
sfx += [{"src": "whoosh", "t": r(S - 0.1), "gain": 0.45, "pico": 0.45}, {"src": "pagina", "t": r(S + 0.1), "gain": 0.4},
        {"src": "boom", "t": s('sem'), "gain": 0.5, "pico": 0.3, "d": 1.2}, {"src": "boom", "t": r(p99 - 0.05), "gain": 0.55, "pico": 0.3, "d": 1.4},
        {"src": "boom", "t": r(t8 - 0.05), "gain": 0.5, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": r(q39 - 0.05), "gain": 0.45},
        {"src": "boom", "t": r(s('39') - 0.3), "gain": 0.5, "pico": 0.3, "d": 1.2},
        {"src": "whoosh", "t": r(so3 - 0.05), "gain": 0.45, "pico": 0.45}, {"src": "boing", "t": r(s('nenhum') - 0.05), "gain": 0.35},
        {"src": "glitch", "t": r(C - 0.05), "gain": 0.5}, {"src": "notif", "t": r(C + 0.2), "gain": 0.4},
        {"src": "glitch", "t": r(FC - 0.05), "gain": 0.5}, {"src": "whoosh2", "t": r(f('conversa') - 0.05), "gain": 0.4},
        {"src": "whoosh", "t": r(f('sem') - 0.1), "gain": 0.45, "pico": 0.45}, {"src": "boom", "t": f('loteria'), "gain": 0.65, "pico": 0.3, "d": 1.5}]
p['audio']['sfx'] = sorted(sfx, key=lambda x: x['t'])
p['audio']['musica'] = [{"src": "m_investiga", "t": r(A - 0.3), "ms": 0, "d": r(S - A + 0.3), "gain": 0.32, "fade": 0.8}]

# ---------- legenda ----------
lg = p['legenda']
lg['ys'] = [[a_, b_, y] for a_, b_, y in lg.get('ys', []) if b_ <= B0 + 0.01] + [[B0, C, 1730], [FC, DUR, 1730]]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print('ok', PID, {'B0': B0, 'A': A, 'S': S, 'C': C, 'FC': FC, 'DUR': DUR, 'LA': LA, 'cenas': [e1, c2, c3, c4, c5, c6, c7, FIM_A]})
