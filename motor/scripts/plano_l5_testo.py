import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
# plano_l5_testo.py (15/11, lote 5, Papo de Médico): "jejum de 13 a 15 horas aumenta a testosterona em 1.300%?"
# Viral: The Diary Of A CEO (TikTok @steven), inglês, convidada (nome FORA da fala e da tela; crédito só o @ do canal),
#   dublado pela Murilo (original a 0,16 por baixo). Trecho único 0,00-8,79 s ("We also see in men, 1,300% increase in
#   testosterone just from somewhere between a 13 to 15 hour fast.") -> MITO. Recorte só da parte de cima (a legenda
#   amarela em inglês, y 990-1075, fica fora). Não respondemos o resto do vídeo (inflamação, articulações, células).
# Entrada: banco rk_ent (6cd9, "Olha só essa notícia") com 0,5 s de folga (jt_ent) + manchete do roteiro.
# r1 SEM crédito novo: banco tb_rosto (6cd9, "Calma. Isso aí é mito, tá?"; usado só na Fertilidade) -> jt_rosto (+cauda).
# CTA: cta6_serio (sério; a piada fica só na cobrança "jejum de juízo").
# Aula: LOUSA (giz) com a padaria do corpo: padaria -> cérebro gerente manda bilhete pelo sangue -> forno = testículo ->
#   pão = testosterona -> despensa vazia, gerente risca o bilhete, forno fraco, menos pão. Desenhos novos em fisio_extra/jt_*.
# Pele: LAB (as últimas do Papo foram notícia e dossiê). Voz: 4 blocos HeyGen por clima, sem atempo e sem <break>
#   (pausas abertas na edição, tmp_jt/prep.py): A indignado (abertura), B manso (aula + o que fazer),
#   C neutro (estudo + fecho), D alegre (cobrança).
# Depois deste script (ele mesmo roda): entrada.py (jt_ent 2,28 s) e pele.py lab.
PID = 'react_l5_testo'; P = 'jt'
DU = json.load(open('tmp_jt/dur.json'))
WD = {k: json.load(open(f'assets/midia/{P}_{k}_voz.words.json')) for k in ('ab', 'au', 'es', 'oq', 'co', 'fe')}
vd = DU['vd']
R1D = 3.16                      # "tá?" acaba em 2,66 + 0,5 s de folga (jt_rosto tem 3,36 s)
r1 = round(vd + R1D, 2)
GAP = 0.55
tAB = r1
tAU = round(tAB + DU['ab'] + GAP, 3)
tES = round(tAU + DU['au'] + GAP, 3)
tOQ = round(tES + DU['es'] + GAP, 3)
tCO = round(tOQ + DU['oq'] + 0.5, 3)
c1 = round(tCO + DU['co'] + 0.35, 2)
CTAD = 3.01                     # cta6_serio: "curte." acaba em 2,42 (0,59 s de folga)
c2 = round(c1 + CTAD, 2)
dur = round(c2 + DU['fe'] + 0.6, 2)
A = lambda v: round(tAB + v, 3); U = lambda v: round(tAU + v, 3); E = lambda v: round(tES + v, 3)
O = lambda v: round(tOQ + v, 3); K = lambda v: round(tCO + v, 3); F = lambda v: round(c2 + v, 3)
def w(blk, palavra, n=0):
    k = 0
    for x in WD[blk]:
        if x['w'].strip('.,?:!').lower() == palavra.lower():
            if k == n: return x['s']
            k += 1
    raise SystemExit(f'sem {palavra} em {blk}')

TINTA, AMAR, VERM, VERDE, AZUL = '#1c1a17', '#ffd400', '#ff4d4d', '#3ddc84', '#7fd3ff'
GIZ, GAMAR, GROSA, GVERM = '#f4f1e8', '#ffe27a', '#ff9fb4', '#ff6b6b'
SOMBRA = "text-shadow:6px 6px 0 #000,0 0 18px rgba(0,0,0,.8)"
GZ = "text-shadow:0 0 3px rgba(255,255,255,.45),5px 6px 0 rgba(0,0,0,.4)"
def TT(t, d, txt, y=300, fz=120, cor="#ffffff", css=SOMBRA, **k):
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=css, vel=0.09, **k)
def TG(t, d, txt, y=300, fz=120, cor=GIZ, **k):       # texto em giz (lousa)
    return TT(t, d, txt, y=y, fz=fz, cor=cor, css=GZ, **k)
def GIG(t, d, txt, y=1450, tam=420, cont=False, cor="rgba(255,212,0,.12)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos}; L.update(k); return L
def X(t, d, cx, cy, s=70, cor="#ff2d3d", z=45, lw=20): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "x", "c": [cx, cy], "s": s}], "espessura": lw, "cor": cor, "z": z}
def CHECK(t, d, cx, cy, s=60, cor=VERDE, z=46): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 20, "cor": cor, "z": z}
def CIRC(t, d, cx, cy, rx, ry, cor="#ff2d3d", lw=12, z=44): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "circulo", "c": [cx, cy], "r": [rx, ry]}], "espessura": lw, "cor": cor, "z": z}
def SETA(t, d, de, para, curva=0, cor=GAMAR, lw=16, z=44): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "seta", "de": de, "para": para, "curva": curva}], "espessura": lw, "cor": cor, "z": z}
def CARIMBO(t, d, txt, xy, tam=130, rot=-8, cor="#ff2d3d"): return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": 60, "cor": cor, "blend": "normal", "css": "background:rgba(255,255,255,.92)"}
def FONTE(t, d, txt): return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 210], "w": 1000, "fonte": "600 28px Montserrat", "cor": "#ffffff", "alinha": "center", "txt": txt, "z": 70, "css": "text-shadow:0 2px 6px #000;background:rgba(0,0,0,.35);border-radius:12px;padding:6px 0"}
def NUM(t, d, valor, y=1010, cor=AMAR, sombra='#7a5a00', **k):
    L = {"tipo": "numero", "t": round(t, 3), "d": round(d, 3), "xy": [0, y], "valor": valor, "tam": 280, "cor": cor, "sombra": sombra, "z": 44}
    L.update(k); return L
def BIG(t, d, txt, y, fz=260, cor=AMAR, sombra='#7a5a00', z=44, entra="zoom"):   # número escrito (1.300%) com 3D de sombra
    sh = ",".join(f"{k}px {k}px 0 {sombra}" for k in range(1, 18))
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, y], "w": 1000, "fonte": f"{fz}px Anton", "cor": cor, "alinha": "center",
            "txt": txt, "z": z, "css": f"text-shadow:{sh},0 30px 50px rgba(0,0,0,.6)", "entra": entra}
FL = lambda t, mx=0.45: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": mx}

# ================= viral em tela dividida + caixinha =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 933], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 853], "raio": 14, "pos": "center top",
      "arroba": "via @steven", "arroba_pos": "topo", "respira": False, "zoom": [[0, 1.0, 0.01], [3.6, 1.06, 0.4], [vd - 2.4, 1.0, 0.4]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [110, 1120], "w": 860, "topo": "Mito ou verdade? 👇", "txt": "Jejum de 14 horas multiplica a testosterona?",
      "botoes": ["MITO", "VERDADE"], "vel": 0.02},
     BIG(4.2, round(vd - 4.2, 2), "1.300%", 1090, fz=250),
     TT(5.5, round(vd - 5.5, 2), "EM 13 A 15 HORAS?", y=1400, fz=110, anim=None, entra="desliza"),
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 853], "raio": 14, "sombra": False, "z": 29}]
# r1: "Calma. Isso aí é mito, tá?"
r_mito = 1.76
c += [{"tipo": "texto", "t": vd + 0.05, "d": round(R1D - 0.05, 2), "xy": [110, 800], "w": 860, "fonte": "100px Anton", "cor": "#111111", "alinha": "center",
       "txt": "“1.300% EM 14 HORAS”", "z": 50, "css": "background:#ffffff;border-radius:16px;padding:12px 20px;box-shadow:0 14px 34px rgba(0,0,0,.45)", "entra": "pop"},
      CARIMBO(vd + r_mito, round(R1D - r_mito, 2), "MITO", [350, 740], tam=170, rot=-9),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + P + "_rosto.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= abertura (indignado) =================
a_mult, a_pulou, a_virou, a_eu, a_ele, a_nao = w('ab', 'multiplicar'), w('ab', 'pulou'), w('ab', 'virou'), w('ab', 'eu'), w('ab', 'ele'), w('ab', 'não')
A2, A3, A4 = round(a_pulou - 0.15, 3), round(a_eu - 0.15, 3), round(a_ele - 0.15, 3)
AF = round(tAU - tAB, 3)
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1),
      # 1.300% = ×14
      GIG(A(0), A2, "×14", y=1380, tam=520, cont=True, cor="rgba(255,212,0,.25)"),
      BIG(A(0.05), A2 - 0.05, "1.300%", 330, fz=240),
      BIG(A(a_mult - 0.1), round(A2 - a_mult + 0.1, 3), "= ×14", 820, fz=300, cor=VERM, sombra="#6b0f1a"),
      CIRC(A(w('ab', 'quatorze') + 0.1), round(A2 - w('ab', 'quatorze') - 0.1, 3), 540, 990, 300, 170, cor="#ffffff", lw=12, z=46),
      FL(A(A2)),
      # pulou o café e virou touro?
      GIG(A(A2), A3 - A2, "TOURO", y=1450, tam=440, ida=False),
      TT(A(A2 + 0.05), A3 - A2 - 0.05, "VIROU TOURO?", y=300, fz=170, cor=AMAR),
      FIS(A(A2 + 0.05), round(a_virou - 0.1 - A2, 3), [{"k": "xicara", "xy": [540, 1020], "s": 1.3, "t": 0.0}], z=30),
      X(A(a_pulou + 0.35), round(a_virou - a_pulou - 0.45, 3), 540, 1020, s=150, z=46),
      FIS(A(a_virou - 0.1), round(A3 - a_virou + 0.1, 3), [{"k": "jt_touro", "xy": [540, 1030], "s": 1.5, "t": 0.0}], z=32, pulsos=[{"o": 0, "t": 0.5}]),
      FL(A(A3)),
      # procurei esse número nos estudos
      GIG(A(A3), A4 - A3, "ESTUDOS", y=1450, tam=400, cont=True, cor="rgba(127,211,255,.22)"),
      TT(A(A3 + 0.05), A4 - A3 - 0.05, "PROCUREI NOS ESTUDOS", y=300, fz=140),
      FIS(A(A3 + 0.05), A4 - A3 - 0.05, [{"k": "jt_lupa", "xy": [540, 1050], "s": 1.4, "t": 0.0}], z=30, pulsos=[{"o": 0, "t": 1.4}]),
      FL(A(A4)),
      # ele não aparece
      GIG(A(A4), round(AF - A4, 3), "NADA", y=1450, tam=460, ida=False, cor="rgba(255,77,77,.16)"),
      BIG(A(A4 + 0.05), round(AF - A4 - 0.05, 3), "1.300%", 420, fz=260, cor=VERM, sombra="#6b0f1a"),
      X(A(a_nao), round(AF - a_nao, 3), 540, 560, s=170, cor="#ffffff", z=46),
      CARIMBO(A(a_nao + 0.2), round(AF - a_nao - 0.2, 3), "NÃO APARECE", [150, 930], tam=130, rot=-7)]

# ================= AULA (manso): LOUSA, a padaria do corpo =================
u_pensa, u_O1, u_manda, u_O2, u_E, u_pao, u_quando, u_gerente2, u_menos = (w('au', 'pensa'), w('au', 'o', 0), w('au', 'manda', 0), w('au', 'o', 2),
    w('au', 'e', 1), w('au', 'pão', 0), w('au', 'quando'), w('au', 'gerente', 1), w('au', 'e', 2))
# 'o'(0) = "O cérebro"; 'o'(2) = "O testículo"; 'e'(1) = "E o pão"; 'e'(2) = "e manda assar menos"; 'gerente'(1) = "o gerente acha"
EB = round(tES - tAU, 3)
S2, S3, S4, S5, S5b, S5c = (round(u_O1 - 0.15, 3), round(u_O2 - 0.15, 3), round(u_E - 0.15, 3), round(u_quando - 0.15, 3),
                            round(u_gerente2 - 0.35, 3), round(u_menos - 0.1, 3))
c += [{"tipo": "fundo", "t": U(-0.05), "d": round(EB + 0.1, 3), "cor": "#22392f", "textura": "lousa", "z": 9}, FL(tAU),
      TG(U(0.05), round(EB - 0.1, 3), "COMO NASCE A TESTOSTERONA?", y=150, fz=100, cor=GAMAR, z=48)]
# S1 padaria
c += [GIG(U(0), S2, "PADARIA", y=1480, tam=400, cont=True, cor="rgba(244,241,232,.20)"),
      FIS(U(0.1), S2 - 0.1, [{"k": "jt_padaria", "xy": [540, 1020], "s": 1.5, "t": 0.0}], pulsos=[{"o": 0, "t": u_pensa + 0.4}]),
      TG(U(w('au', 'nasce') + 0.15), round(S2 - w('au', 'nasce') - 0.15, 3), "PADARIA DO CORPO", y=400, fz=130),
      FL(U(S2))]
# S2 cérebro = gerente, bilhete pelo sangue
rio = [[540, 925], [516, 1000], [562, 1075], [516, 1150], [562, 1225], [522, 1290], [540, 1345]]
c += [GIG(U(S2), S3 - S2, "BILHETE", y=1560, tam=300, ida=False),
      FIS(U(S2 + 0.05), S3 - S2 - 0.05, [{"k": "jt_gerente", "xy": [540, 745], "s": 0.85, "t": 0.0},
                                        {"k": "jt_forno", "xy": [540, 1440], "s": 0.5, "t": u_manda - S2 - 0.4}],
          fluxos=[{"de": [540, 925], "para": [540, 1345], "curva": 0, "cor": GIZ, "t": u_manda - S2 + 0.05, "d": 1.7, "n": 6, "r": 21, "viagem": 0.8, "fica": True}],
          pulsos=[{"o": 0, "t": 0.6}, {"o": 1, "t": u_manda - S2 + 1.2}]),
      {"tipo": "desenho", "t": U(u_manda - 0.25), "d": round(S3 - u_manda + 0.25, 3), "formas": [{"k": "linha", "pts": rio, "j": 2}],
       "espessura": 30, "cor": GVERM, "z": 26, "vel": 0.6},
      TG(U(S2 + 0.05), round(u_manda - 0.1 - S2 - 0.05, 3), "CÉREBRO = GERENTE", y=400, fz=130, cor=GROSA),
      TG(U(u_manda - 0.1), round(S3 - u_manda + 0.1, 3), "BILHETE PELO SANGUE", y=405, fz=106),
      FL(U(S3))]
# S3 forno = testículo
c += [GIG(U(S3), S4 - S3, "FORNO", y=1520, tam=420),
      FIS(U(S3 + 0.05), S4 - S3 - 0.05, [{"k": "jt_forno", "xy": [540, 1000], "s": 1.35, "t": 0.0, "rotulo": "TESTÍCULO", "rot_y": 225, "cor_rotulo": GAMAR}],
          pulsos=[{"o": 0, "t": 1.0}]),
      TG(U(S3 + 0.1), S4 - S3 - 0.1, "FORNO = TESTÍCULO", y=400, fz=130),
      FL(U(S4))]
# S4 pão = testosterona
c += [GIG(U(S4), S5 - S4, "PÃO", y=1560, tam=440, ida=False),
      FIS(U(S4 + 0.05), S5 - S4 - 0.05, [{"k": "jt_forno", "xy": [540, 880], "s": 0.95, "t": 0.0},
                                        {"k": "jt_paes6", "xy": [540, 1280], "s": 0.95, "t": u_pao - S4 - 0.1, "rotulo": "TESTOSTERONA", "rot_y": 175, "cor_rotulo": GAMAR}],
          pulsos=[{"o": 1, "t": u_pao - S4 + 0.9}]),
      TG(U(S4 + 0.1), S5 - S4 - 0.1, "PÃO = TESTOSTERONA", y=405, fz=110, cor=GAMAR),
      FL(U(S5))]
# S5 sem comida por dias -> tempo de aperto -> menos pão
c += [GIG(U(S5), S5b - S5, "DIAS", y=1540, tam=440),
      FIS(U(S5 + 0.05), S5b - S5 - 0.05, [{"k": "jt_despensa", "xy": [540, 1020], "s": 1.4, "t": 0.0, "rotulo": "VAZIA", "rot_y": 240, "cor_rotulo": GROSA}],
          pulsos=[{"o": 0, "t": 1.2}]),
      TG(U(S5 + 0.1), S5b - S5 - 0.1, "SEM COMIDA", y=400, fz=150, cor=GROSA),
      FL(U(S5b)),
      GIG(U(S5b), S5c - S5b, "APERTO", y=1540, tam=400, ida=False, cor="rgba(255,159,180,.16)"),
      FIS(U(S5b + 0.05), S5c - S5b - 0.05, [{"k": "jt_gerente", "xy": [540, 960], "s": 1.15, "t": 0.0}], pulsos=[{"o": 0, "t": 0.8}]),
      X(U(S5b + 0.75), round(S5c - S5b - 0.75, 3), 742, 1075, s=62, cor=GVERM, z=46, lw=16),
      TG(U(S5b + 0.1), S5c - S5b - 0.1, "TEMPO DE APERTO", y=400, fz=135),
      FL(U(S5c)),
      GIG(U(S5c), round(EB - S5c, 3), "MENOS", y=1540, tam=440),
      FIS(U(S5c + 0.05), round(EB - S5c - 0.05, 3), [{"k": "jt_forno_fraco", "xy": [500, 880], "s": 0.95, "t": 0.0},
                                                      {"k": "jt_paes4", "xy": [500, 1280], "s": 0.95, "t": 0.35}]),
      SETA(U(S5c + 0.9), round(EB - S5c - 0.9, 3), [920, 960], [920, 1320], cor=GAMAR, lw=18, z=46),
      TG(U(S5c + 0.1), round(EB - S5c - 0.1, 3), "MENOS PÃO", y=400, fz=170, cor=GAMAR)]

# ================= estudo (neutro) =================
e_dez, e_dois, e_A, e_caiu, e_Em2, e_hom, e_jejum, e_Caiu, e_E, e_mant = (w('es', 'dez'), w('es', 'dois', 0), w('es', 'a'), w('es', 'caiu', 0),
    w('es', 'em', 1), w('es', 'homens', 1), w('es', 'jejum'), w('es', 'caiu', 1), w('es', 'e', 3), w('es', 'mantiveram'))
# 'em'(1) = "Em dois mil e dezesseis"; 'homens'(1) = "homens que treinavam" (o "trinta e quatro" foi cortado do áudio: só 17 dos 34 jejuaram)
# 'caiu'(1) = "Caiu também"; 'e'(3) = "E o músculo" (0-2: oitenta e / e sete / mil e)
ES_FIM = round(tOQ - tES, 3)
E2, E3, E4, E5 = round(e_A - 0.1, 3), round(e_Em2 - 0.15, 3), round(e_Caiu - 0.2, 3), round(e_E - 0.15, 3)
N1 = round(e_dois - 0.3, 3)
N2 = round(w('es', 'subiu') + 0.3, 3)
c += [FL(tES),
      {"tipo": "texto", "t": E(0.1), "d": round(ES_FIM - 0.1, 3), "xy": [40, 128], "w": 1000, "fonte": "900 34px Montserrat", "cor": "#ffffff", "alinha": "center",
       "txt": "● CHECAGEM · O QUE OS ESTUDOS MEDIRAM", "css": "letter-spacing:3px;background:#ff2d3d;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"},
      {"tipo": "artigo", "t": E(0.2), "d": round(E3 - 0.25, 3), "box": [100, 290, 880, 640], "z": 34,
       "revista": "Hormone Research · 1987", "titulo": "Jejum curto e o eixo cérebro-testículo em homens saudáveis",
       "autores": "Röjdmark · 10 homens, antes e depois do jejum", "rola": 0,
       "linhas": [{"txt": "10 homens saudáveis, de peso normal.", "grifo": E(e_dez + 0.1)},
                  {"txt": "Mais de 2 dias sem comer (56 horas).", "grifo": E(e_dois + 0.1)},
                  {"txt": "Testosterona: de 8,7 para 5,7 µg/L.", "grifo": E(e_caiu + 0.1)}],
       "rodape": "doi 10.1159/000180645"},
      GIG(E(0), round(N1 - 2.15, 3), "1987", y=1450, tam=440, cor="rgba(255,212,0,.12)"),
      TT(E(0.9), round(N1 - 2.15 - 0.9, 3), "1987", y=1060, fz=200, cor=AMAR, anim=None, entra="zoom"),
      FL(E(N1 - 2.15)),
      NUM(E(N1 - 2.15), 2.15, 10, rotulo="homens saudáveis", conta=0.6, y=1010),
      FL(E(N1)),
      GIG(E(N1), round(E2 - N1, 3), "2 DIAS", y=1450, tam=420, cont=True, cor="rgba(127,211,255,.22)", ida=False),
      NUM(E(N1), round(E2 - N1, 3), 2, suf=" DIAS", cor=AZUL, sombra="#0d4f78", conta=0.4, tam=300, y=1040),
      FL(E(E2)),
      GIG(E(E2), N2 - E2, "SUBIU?", y=1450, tam=400, cont=True, cor="rgba(255,212,0,.25)", ida=False),
      TT(E(E2 + 0.05), N2 - E2 - 0.05, "NÃO SUBIU", y=1050, fz=190, cor=AMAR, anim=None, entra="zoom"),
      SETA(E(E2 + 0.2), N2 - E2 - 0.2, [540, 1480], [540, 1290], cor=VERDE, lw=18, z=46),
      X(E(E2 + 0.7), N2 - E2 - 0.7, 540, 1385, s=85, z=47),
      FL(E(N2)),
      GIG(E(N2), E3 - N2, "CAIU", y=1450, tam=460, cor="rgba(255,77,77,.18)"),
      NUM(E(N2), round(E3 - N2, 3), 5.7, dec=1, de=8.7, conta=1.3, cor=VERM, sombra="#6b0f1a", rotulo="caiu um terço", tam=280, y=1000),
      FONTE(E(0.2), round(E3 - 0.2, 3), "Röjdmark, Horm Res 1987 · doi 10.1159/000180645"),
      FL(E(E3)),
      {"tipo": "artigo", "t": E(E3), "d": round(ES_FIM - E3, 3), "box": [100, 290, 880, 640], "z": 34,
       "revista": "Journal of Translational Medicine · 2016", "titulo": "Jejum de 16 horas por 8 semanas em homens que treinam",
       "autores": "Moro e col. · ensaio randomizado, 17 + 17 homens", "rola": 0,
       "linhas": [{"txt": "34 homens treinados: 17 em jejum, 17 sem.", "grifo": E(e_hom + 0.1)},
                  {"txt": "Comiam em 8 horas: 16 horas de jejum.", "grifo": E(e_jejum + 0.1)},
                  {"txt": "Testosterona caiu no grupo do jejum.", "grifo": E(e_Caiu + 0.1)},
                  {"txt": "Músculo e força: mantidos.", "grifo": E(e_E + 0.3)}],
       "rodape": "doi 10.1186/s12967-016-1044-0"},
      GIG(E(E3), round(e_jejum - 0.3 - E3, 3), "2016", y=1450, tam=440, ida=False),
      TT(E(E3 + 0.05), round(e_jejum - 0.3 - E3 - 0.05, 3), "2016", y=1060, fz=200, cor=AMAR, anim=None, entra="zoom"),
      {"tipo": "texto", "t": E(e_hom - 0.1), "d": round(E4 - e_hom + 0.1, 3), "xy": [70, 1440], "w": 940, "fonte": "100px Anton", "cor": TINTA, "alinha": "center",
       "txt": "17 EM JEJUM × 17 SEM", "css": "letter-spacing:1px;background:#ffd400;border-radius:18px;padding:8px 0;box-shadow:0 8px 24px rgba(0,0,0,.6)", "z": 62, "entra": "desliza"},
      FL(E(e_jejum - 0.3)),
      GIG(E(e_jejum - 0.3), round(E4 - e_jejum + 0.3, 3), "16 HORAS", y=1450, tam=380, cont=True, cor="rgba(127,211,255,.22)"),
      TT(E(e_jejum - 0.25), round(E4 - e_jejum + 0.25, 3), "16 H DE JEJUM\\nPOR 8 SEMANAS", y=1010, fz=150, cor=AZUL, anim=None, entra="zoom"),
      FL(E(E4)),
      GIG(E(E4), E5 - E4, "CAIU", y=1450, tam=460, cor="rgba(255,77,77,.18)", ida=False),
      TT(E(E4), E5 - E4, "CAIU TAMBÉM", y=1040, fz=190, cor=VERM, anim=None, entra="zoom"),
      SETA(E(E4 + 0.3), E5 - E4 - 0.3, [985, 1230], [985, 1480], cor=VERM, lw=18, z=46),
      FL(E(E5)),
      GIG(E(E5), round(ES_FIM - E5, 3), "FORÇA", y=1450, tam=440, cont=True, cor="rgba(61,220,132,.25)"),
      TT(E(E5 + 0.05), round(ES_FIM - E5 - 0.05, 3), "MÚSCULO E FORÇA", y=985, fz=128),
      FIS(E(E5 + 0.1), round(ES_FIM - E5 - 0.1, 3), [{"k": "bb_giz_musculo", "xy": [540, 1270], "s": 0.75, "t": 0.0}], z=38, pulsos=[{"o": 0, "t": 1.0}]),
      CARIMBO(E(e_mant), round(ES_FIM - e_mant, 3), "MANTIDOS", [300, 1440], tam=110, rot=-6, cor="#138a3e"),
      FONTE(E(E3), round(ES_FIM - E3, 3), "Moro e col., J Transl Med 2016 · doi 10.1186/s12967-016-1044-0")]

# ================= o que fazer (manso) =================
o_pedem, o_nao = w('oq', 'pedem'), w('oq', 'não')
O2, O3 = round(o_pedem - 0.15, 3), round(o_nao - 0.15, 3)
OQ_FIM = round(tCO - tOQ, 3)
c += [FL(tOQ),
      GIG(O(0), O2, "CANSAÇO", y=1450, tam=400, cont=True, cor="rgba(255,212,0,.22)"),
      TT(O(0.05), O2 - 0.05, "CANSAÇO? POUCA VONTADE?", y=300, fz=135),
      FIS(O(0.1), O2 - 0.1, [{"k": "cf_bateria", "xy": [540, 1050], "s": 1.3, "t": 0.0}], z=30, pulsos=[{"o": 0, "t": 0.9}]),
      FL(O(O2)),
      GIG(O(O2), O3 - O2, "EXAME", y=1450, tam=440, ida=False),
      TT(O(O2 + 0.05), O3 - O2 - 0.05, "CONSULTA E EXAME", y=300, fz=150, cor=AMAR),
      FIS(O(O2 + 0.1), O3 - O2 - 0.1, [{"k": "cx_exame", "xy": [540, 1060], "s": 1.25, "t": 0.0}], z=30),
      CHECK(O(O2 + 0.6), O3 - O2 - 0.6, 820, 800, s=70),
      FL(O(O3)),
      GIG(O(O3), round(OQ_FIM - O3, 3), "RELÓGIO", y=1450, tam=400, cor="rgba(255,77,77,.16)"),
      TT(O(O3 + 0.05), round(OQ_FIM - O3 - 0.05, 3), "RELÓGIO? NÃO.", y=300, fz=170),
      FIS(O(O3 + 0.1), round(OQ_FIM - O3 - 0.1, 3), [{"k": "cy_relogio", "xy": [560, 1060], "s": 1.3, "t": 0.0}], z=30),
      X(O(O3 + 0.6), round(OQ_FIM - O3 - 0.6, 3), 590, 1060, s=170, z=46)]

# ================= cobrança (alegre) =================
k_nao = w('co', 'não')
CO_FIM = round(c1 - tCO, 3)
c += [FL(tCO),
      GIG(K(0), k_nao - 0.1, "FOME", y=1450, tam=460, cont=True, cor="rgba(255,212,0,.22)"),
      TT(K(0.05), k_nao - 0.15, "TE POUPEI DA FOME", y=300, fz=150, cor=AMAR),
      FIS(K(0.1), k_nao - 0.2, [{"k": "jt_touro", "xy": [540, 1040], "s": 1.35, "t": 0.0}], z=30),
      X(K(w('co', 'touro') + 0.1), round(k_nao - w('co', 'touro') - 0.2, 3), 540, 1040, s=190, z=46),
      FL(K(k_nao - 0.1)),
      GIG(K(k_nao - 0.1), round(CO_FIM - k_nao + 0.1, 3), "SEGUE", y=1450, tam=460, ida=False),
      TT(K(k_nao - 0.05), round(CO_FIM - k_nao + 0.05, 3), "JEJUM DE JUÍZO", y=300, fz=170),
      {"tipo": "texto", "t": K(k_nao + 0.3), "d": round(CO_FIM - k_nao - 0.3, 3), "xy": [340, 1000], "w": 400, "fonte": "800 80px Montserrat", "cor": "#ffffff", "alinha": "center",
       "txt": "Seguir", "z": 45, "css": "background:#0095f6;border-radius:24px;padding:18px 0;box-shadow:0 12px 30px rgba(0,0,0,.45)", "entra": "pop"}]

# ================= CTA (banco cta6_serio) + fecho (neutro) =================
f_test = w('fe', 'testosterona')
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": CTAD, "ms": 0, "src": M + "cta6_serio.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": round(CTAD - 0.25, 2), "y": 215, "txt": "TE AJUDOU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(F(0), f_test - 0.15, "GORDURA", y=1450, tam=400, cont=True, cor="rgba(255,212,0,.22)"),
      TT(F(0.05), f_test - 0.2, "PODE AJUDAR A EMAGRECER", y=300, fz=135),
      FIS(F(0.1), f_test - 0.25, [{"k": "balanca", "xy": [540, 1060], "s": 1.2, "t": 0.0}], z=30),
      CHECK(F(0.8), f_test - 0.95, 860, 830, s=70),
      FL(F(f_test - 0.15)),
      GIG(F(f_test - 0.15), round(dur - F(f_test - 0.15), 3), "MITO", y=1450, tam=460, ida=False, cor="rgba(255,77,77,.16)"),
      TT(F(f_test - 0.1), round(dur - F(f_test - 0.1), 3), "TESTOSTERONA: NÃO TURBINA", y=300, fz=135, cor=AMAR),
      FIS(F(f_test), round(dur - F(f_test), 3), [{"k": "jt_touro", "xy": [540, 1080], "s": 1.15, "t": 0.0}], z=30),
      CARIMBO(F(w('fe', 'turbina') - 0.1), round(dur - F(w('fe', 'turbina') - 0.1), 3), "MITO", [330, 1150], tam=190, rot=-8),
      FONTE(F(0), round(dur - F(0), 3), "Röjdmark, Horm Res 1987 · Moro e col., J Transl Med 2016 · conteúdo educativo")]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json", "gain": 0.16},
       {"src": M + P + "_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + P + "_rosto.mp4", "t": vd, "ms": 0, "d": R1D, "palavras": M + P + "_r1.words.json"},
       {"src": M + P + "_ab_voz.wav", "t": tAB, "ms": 0, "d": DU['ab'], "palavras": M + P + "_ab_voz.words.json"},
       {"src": M + P + "_au_voz.wav", "t": tAU, "ms": 0, "d": DU['au'], "palavras": M + P + "_au_voz.words.json"},
       {"src": M + P + "_es_voz.wav", "t": tES, "ms": 0, "d": DU['es'], "palavras": M + P + "_es_voz.words.json"},
       {"src": M + P + "_oq_voz.wav", "t": tOQ, "ms": 0, "d": DU['oq'], "palavras": M + P + "_oq_voz.words.json"},
       {"src": M + P + "_co_voz.wav", "t": tCO, "ms": 0, "d": DU['co'], "palavras": M + P + "_co_voz.words.json"},
       {"src": M + "cta6_serio.mp4", "t": c1, "ms": 0, "d": CTAD, "palavras": M + "cta6_serio.mp4.words.json"},
       {"src": M + P + "_fe_voz.wav", "t": c2, "ms": 0, "d": DU['fe'], "palavras": M + P + "_fe_voz.words.json"}]
# trilha contínua por baixo de TODA a narração (um trecho por clima, emendas cruzadas; nenhum arquivo acaba antes do fim)
musica = [{"src": "m_tensao", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tAU - vd + 0.7, 2), "gain": 0.22, "fade": 0.6},       # r1 + abertura (indignado)
          {"src": "m_emocao", "t": round(tAU - 0.4, 2), "ms": 0, "d": round(tES - tAU + 0.9, 2), "gain": 0.26, "fade": 0.6},    # aula (manso, lousa)
          {"src": "m_investiga", "t": round(tES - 0.3, 2), "ms": 0, "d": round(tOQ - tES + 0.9, 2), "gain": 0.24, "fade": 0.6},                        # estudo (neutro)
          {"src": "m_emocao", "t": round(tOQ - 0.5, 2), "ms": 20.0, "d": round(tCO - tOQ + 0.9, 2), "gain": 0.26, "fade": 0.6},  # o que fazer (manso)
          {"src": "m_humor", "t": round(tCO - 0.3, 2), "ms": 0, "d": round(c1 - tCO + 0.6, 2), "gain": 0.24, "fade": 0.5},       # cobrança (alegre)
          {"src": "m_emocao", "t": round(c1 - 0.2, 2), "ms": 2.0, "d": round(dur - c1 + 0.2, 2), "gain": 0.24, "fade": 0.8}]     # CTA + fecho
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "boom", "t": 4.2, "gain": 0.4, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": 5.5, "gain": 0.3},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "scratch", "t": vd + r_mito - 0.1, "gain": 0.35}, {"src": "boom", "t": vd + r_mito, "gain": 0.45, "pico": 0.3, "d": 1.2},
       # abertura
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1, "gain": 0.5, "pico": 0.45},
       {"src": "boom", "t": A(a_mult - 0.1), "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": A(A2), "gain": 0.4}, {"src": "scratch", "t": A(a_pulou + 0.35), "gain": 0.3}, {"src": "boing", "t": A(a_virou), "gain": 0.4},
       {"src": "whoosh2", "t": A(A3), "gain": 0.4}, {"src": "pagina", "t": A(A3 + 0.1), "gain": 0.4},
       {"src": "whoosh", "t": A(A4), "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": A(a_nao), "gain": 0.3}, {"src": "boom", "t": A(a_nao + 0.2), "gain": 0.5, "pico": 0.3, "d": 1.3},
       # aula (lousa): giz e papel
       {"src": "whoosh", "t": tAU, "gain": 0.4, "pico": 0.45}]
for t0 in (0, S2, S3, S4, S5, S5b, S5c):
    sfx.append({"src": "whoosh2", "t": U(t0), "gain": 0.35})
    sfx.append({"src": "papel", "t": U(t0 + 0.12), "gain": 0.3})
sfx += [{"src": "boing", "t": U(u_pensa + 0.4), "gain": 0.3}, {"src": "riser", "t": U(u_manda - 0.2), "gain": 0.2, "d": 1.4}, {"src": "boing", "t": U(u_pao - 0.1), "gain": 0.3},
        {"src": "scratch", "t": U(S5b + 0.75), "gain": 0.3}, {"src": "boing", "t": U(S5c + 0.9), "gain": 0.25},
        # estudo
        {"src": "whoosh", "t": tES, "gain": 0.45, "pico": 0.45}, {"src": "pagina", "t": E(0.3), "gain": 0.5},
        {"src": "boom", "t": E(e_dez - 0.1), "gain": 0.45, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": E(e_dois - 0.25), "gain": 0.35},
        {"src": "whoosh2", "t": E(E2), "gain": 0.35}, {"src": "scratch", "t": E(E2 + 0.7), "gain": 0.3},
        {"src": "boom", "t": E(N2), "gain": 0.5, "pico": 0.3, "d": 1.3},
        {"src": "whoosh", "t": E(E3), "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": E(E3 + 0.1), "gain": 0.45},
        {"src": "whoosh2", "t": E(e_hom - 0.1), "gain": 0.35}, {"src": "whoosh2", "t": E(e_jejum - 0.3), "gain": 0.35},
        {"src": "whoosh", "t": E(E4), "gain": 0.4, "pico": 0.45}, {"src": "whoosh2", "t": E(E5), "gain": 0.35},
        {"src": "boom", "t": E(e_mant), "gain": 0.5, "pico": 0.3, "d": 1.3},
        # o que fazer
        {"src": "whoosh", "t": tOQ, "gain": 0.4, "pico": 0.45}, {"src": "whoosh2", "t": O(O2), "gain": 0.35}, {"src": "boing", "t": O(O2 + 0.6), "gain": 0.3},
        {"src": "whoosh2", "t": O(O3), "gain": 0.35}, {"src": "scratch", "t": O(O3 + 0.6), "gain": 0.3},
        # cobrança
        {"src": "whoosh2", "t": tCO, "gain": 0.35}, {"src": "scratch", "t": K(w('co', 'touro') + 0.1), "gain": 0.3},
        {"src": "whoosh", "t": K(k_nao - 0.1), "gain": 0.4, "pico": 0.45}, {"src": "notif", "t": K(k_nao + 0.3), "gain": 0.4},
        # CTA e fecho
        {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.5},
        {"src": "boing", "t": F(0.8), "gain": 0.3}, {"src": "whoosh", "t": F(f_test - 0.15), "gain": 0.4, "pico": 0.45},
        {"src": "boom", "t": F(w('fe', 'turbina') - 0.1), "gain": 0.55, "pico": 0.3, "d": 1.5}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
    if L.get("z", 0) is None: L.pop("z")
salvar(PID, dur, 515, c, voz, sfx,
       {"r1_fim": r1, "esconde": [[0, 4.1]], "ys": [[4.1, vd, 1640], [vd, r1, 1060], [r1, tAU, 1720], [tAU, tES, 1735], [tES, c1, 1720], [c1, c2, 1560], [c2, dur, 1720]]})
p = json.load(open(f'planos/{PID}.json')); p['audio']['musica'] = musica
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tAB", tAB, "tAU", tAU, "tES", tES, "tOQ", tOQ, "tCO", tCO, "c1", c1, "c2", c2)
subprocess.run(["python3", "scripts/entrada.py", PID, "assets/midia/jt_ent.mp4", "assets/midia/jt_ent.words.json", "2.28",
                "“1.300% MAIS TESTOSTERONA” COM 14 HORAS DE JEJUM?", "a fala que viralizou num podcast gringo"], check=True)
subprocess.run(["python3", "scripts/pele.py", PID, "lab"], check=True)
