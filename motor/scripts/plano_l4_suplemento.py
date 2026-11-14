import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
# plano_l4_suplemento.py (14/11, lote 4, Fertilidade a Dois): "suplemento certo melhora o esperma em até 40%?"
# Viral: médica de jaleco no TikTok (@dra.zulyvelasco), espanhol, dublado pela Murilo (original a 0,16 por baixo).
#   Trecho 0,00-8,28 s (um pedaço): "Cuatro suplementos que él debería de consumir para mejorar la fertilidad masculina.
#   ¿Sabías que se puede mejorar la calidad de la esperma hasta un 40% con los suplementos correctos?"
#   A lista dos nomes começa em 8,30 s: fica de fora. Recorte y 170-1350 (sem a legenda palavra a palavra e sem o logo do jaleco).
#   Colega sem nome (só o @ do crédito); logo do hospital não é comentado.
# Veredito: EXAGERO (caixinha DEPENDE): quem tem falta ganha repondo; 40% para qualquer homem, não.
# Voz: 3 create_speech por clima SEM <break> e SEM atempo (pausas de 0,7-0,85 s abertas na edição, tmp_sx/prep.py):
#   neutro (r1 + abertura + estudo + fecho), manso (aula + o que fazer), alegre (cobrança). r1 = rosto 6cd9 (HeyGen, áudio do neutro).
# EDIÇÃO: abertura, aula, o que fazer e fecho na pele DOSSIÊ (papel): a aula é uma PASTA com 4 FICHAS presas por clipe que caem
#   uma por vez (planta murcha + regador = com sede a água salva; terra molhada = poça, não cresce; tanque baixo + fábrica = com
#   falta ganha; tanque cheio transbordando = o excesso sobra). O ESTUDO vai na pele LAB (fundo escuro com grade, fixo) para não ficar
#   dossiê em cima de dossiê: duas colunas de casais, 34% x 35% com berço, selo PROVA FRACA.
#   Desenhos novos: fisio_extra/planta_murcha, planta_vicosa, regador, sx_poca, sx_tanque_baixo, sx_tanque_cheio, sx_casal,
#   sx_capsula, sx_berco, sx_pote; reusados dn_fabrica, cx_exame, cr_cofrinho. Pasta e clipe: assets/midia/sx_pasta.svg, sx_clipe.svg.
# Depois deste script:
#   python3 scripts/entrada.py react_l4_suplemento assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     '“ATÉ 40%” COM SUPLEMENTO?' 'a dica de suplemento que viralizou no TikTok' && python3 scripts/pele.py react_l4_suplemento dossie
PID = 'react_l4_suplemento'; P = 'sx'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def Wd(k): return json.load(open(f'{M}sx_{k}_voz.words.json'))
WA, WB, WE, WG, WC, WF = Wd('a'), Wd('b'), Wd('e'), Wd('g'), Wd('c'), Wd('f')
DA, DB, DE, DG, DC, DF = [round(dur_de(f'{M}sx_{k}_voz.wav'), 3) for k in 'abegcf']
vd = 8.28
R1D = 3.12                      # r1: última palavra ("estudo.") termina em 2,60 s no clipe; 0,5 s de folga
r1 = round(vd + R1D, 3)
tA = round(r1 + 0.15, 3)
tB = round(tA + DA + 0.45, 3)
tE = round(tB + DB + 0.45, 3)
tG = round(tE + DE + 0.5, 3)
tC = round(tG + DG + 0.4, 3)
c1 = round(tC + DC + 0.15, 3)   # CTA do banco (cta6, 4,12 s)
c2 = round(c1 + 4.12, 3)
tF = round(c2 + 0.15, 3)
dur = round(tF + DF + 1.5, 2)
a = lambda i: round(tA + WA[i]['s'], 3)
b = lambda i: round(tB + WB[i]['s'], 3)
e = lambda i: round(tE + WE[i]['s'], 3)
g = lambda i: round(tG + WG[i]['s'], 3)
h = lambda i: round(tF + WF[i]['s'], 3)
# paleta do papel (dossiê) e do laboratório
TINTA, VERM, AZUL, OURO, VERDE, CINZA = '#1c1a17', '#b3121f', '#1f5fa8', '#9a6400', '#2e7d32', '#5a5a5a'
BR, LIMA, AMAR, ROSA, VERML = '#ffffff', '#c6ff3d', '#ffd400', '#ff9fb4', '#ff2d3d'
SP = "text-shadow:5px 5px 0 rgba(0,0,0,.14)"
SH = "text-shadow:6px 6px 0 #000"
def TT(t, d, txt, y=330, fz=120, cor=TINTA, z=40, **k):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SP, vel=0.09, **k); L["z"] = z; return L
def TL(t, d, txt, y=300, fz=120, cor=BR, z=40, **k):      # texto do laboratório (fundo escuro)
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SH, vel=0.09, **k); L["z"] = z; return L
def GIG(t, d, txt, y=1250, tam=460, cont=False, cor="rgba(28,26,23,.08)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=30, cor_rotulo="#ffffff", **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "cor_rotulo": cor_rotulo}; L.update(k); return L
def XX(t, d, cx, cy, s=70, cor=VERM, z=45): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "x", "c": [cx, cy], "s": s}], "espessura": 18, "cor": cor, "z": z}
def CHECK(t, d, cx, cy, s=60, z=46, cor=VERDE): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 18, "cor": cor, "z": z}
def CARIMBO(t, d, txt, xy, tam=130, rot=-8, cor=VERM, z=60): return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": z, "cor": cor, "blend": "normal", "css": "background:rgba(255,255,255,.9);white-space:nowrap"}
def FONTE(t, d, txt): return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 196], "w": 1000, "fonte": "600 28px Montserrat", "cor": TINTA, "alinha": "center", "txt": txt, "z": 70, "css": "background:rgba(255,255,255,.55);border-radius:12px;padding:6px 0"}
def FONTEL(t, d, txt): return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 196], "w": 1000, "fonte": "600 28px Montserrat", "cor": BR, "alinha": "center", "txt": txt, "z": 70, "css": "background:rgba(0,0,0,.45);border-radius:12px;padding:6px 0"}
def NUM(t, d, valor, y=560, cor=VERM, sombra='#d9c49a', z=44, cor_rotulo=TINTA, sombra_rotulo="none", **k):
    L = {"tipo": "numero", "t": round(t, 3), "d": round(d, 3), "xy": [0, y], "valor": valor, "tam": 300, "cor": cor, "sombra": sombra, "cor_rotulo": cor_rotulo, "sombra_rotulo": sombra_rotulo, "z": z}
    L.update(k); return L
def CARD(t, d, aba, k, rot):
    """ficha creme que CAI dentro da pasta (a pilha cresce: z sobe a cada ficha; a de baixo some depois que a nova pousa)"""
    return {"tipo": "cartao", "t": round(t, 3), "d": round(d, 3), "box": [70, 400, 940, 1180], "aba": aba, "entra": "cai", "rot": rot, "z": 20 + 8 * k}
def CLIPE(t, d, k, rot):
    return {"tipo": "foto", "t": round(t, 3), "d": round(d, 3), "src": M + "sx_clipe.svg", "box": [838, 332, 72, 176], "raio": 0, "sombra": False, "fit": "contain", "entra": "cai", "rot": rot, "z": 20 + 8 * k + 6}
def ZC(k, j=1): return 20 + 8 * k + j       # z do conteúdo da ficha k
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4}
AGUA = "#4aa8ff"

# ================= abertura: viral em tela dividida + caixinha =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 1100], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 1027], "raio": 14, "pos": "center",
      "arroba": "via @dra.zulyvelasco", "respira": False, "zoom": [[0, 1.0, 0.01], [3.0, 1.05, 0.5], [vd - 2.5, 1.0, 0.5]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [90, 1190], "w": 900, "topo": "Mito ou verdade? 👇", "txt": "Suplemento certo melhora o esperma em até 40%?",
      "botoes": ["MITO", "VERDADE", "DEPENDE"], "vel": 0.022, "escolha": 2, "t_escolha": 3.3},
     {"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1265], "valor": 728, "suf": " MIL VIEWS", "tam": 120},
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 1027], "raio": 14, "sombra": False, "z": 29}]

# ================= r1: "Quarenta por cento? Vamos ver o maior estudo." =================
PAINEL = "background:rgba(239,228,201,.97);border-radius:14px;height:1027px;box-sizing:border-box;line-height:1.0;" + SP
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(R1D - 0.04, 2), "xy": [70, 190], "w": 940, "fonte": "330px Anton", "cor": VERM, "alinha": "center",
       "txt": "40%?", "z": 55, "entra": "pop", "css": PAINEL + ";padding:120px 40px 0"},
      CARIMBO(vd + 1.0, round(R1D - 1.02, 2), "DEPENDE", [255, 640], tam=150, rot=-7, z=56),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + P + "_rosto.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (neutro): abertura =================
A2, A3, A4 = round(a(6) - 0.05, 3), round(a(14) - 0.1, 3), round(a(21) - 0.2, 3)
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1),
      # A1 tem fundo de verdade
      GIG(tA, round(A2 - tA, 3), "VERDADE", y=1420, tam=420, cont=True, cor="rgba(46,125,50,.30)"),
      TT(r1 + 0.05, round(A2 - r1 - 0.05, 3), "TEM FUNDO DE VERDADE", y=520, fz=150, cor=VERDE),
      CHECK(tA + 0.5, round(A2 - tA - 0.5, 3), 540, 1080, s=90),
      FL(A2),
      # A2 quem tem falta de vitamina pode melhorar repondo
      GIG(A2, round(A3 - A2, 3), "FALTA", y=1450, tam=480, cor="rgba(154,100,0,.14)", ida=False),
      TT(A2 + 0.03, round(A3 - A2 - 0.03, 3), "FALTA VITAMINA? REPOR AJUDA", y=300, fz=125),
      FIS(A2, round(A3 - A2, 3), [{"k": "sx_tanque_baixo", "xy": [540, 1080], "s": 1.0, "t": 0.15, "rotulo": "VITAMINA", "rot_y": 240}],
          fluxos=[{"de": [200, 640], "para": [520, 960], "curva": -60, "cor": "#f2b51d", "t": round(a(12) - A2, 3), "d": 1.3, "n": 6, "viagem": 0.7}],
          pulsos=[{"o": 0, "t": round(a(13) - A2, 3)}]),
      FL(A3),
      # A3 40% pra qualquer homem?
      GIG(A3, round(A4 - A3, 3), "40%", y=1450, tam=520, cont=True, cor="rgba(179,18,31,.26)"),
      NUM(A3, round(A4 - A3, 3), 40, y=420, suf="%", tam=360, de=0),
      TT(A3 + 0.5, round(A4 - A3 - 0.5, 3), "PRA QUALQUER HOMEM?", y=1000, fz=140),
      FL(A4),
      # A4 aí, não
      GIG(A4, round(tB - A4, 3), "NÃO", y=1300, tam=560, cont=True, cor="rgba(179,18,31,.30)", ida=False),
      TT(A4 + 0.03, round(tB - A4 - 0.03, 3), "AÍ, NÃO.", y=640, fz=280, cor=VERM, anim=None, entra="zoom"),
      XX(A4 + 0.35, round(tB - A4 - 0.35, 3), 540, 1260, s=110)]

# ================= B (manso): AULA na PASTA, uma ficha por ideia =================
K1, K2, K3, K4, KF = tB, round(b(8) - 0.35, 3), round(b(18) - 0.3, 3), round(b(30) - 0.35, 3), tE
POUSA = 0.55
PX, PY, PS = 430, 1190, 1.2                  # planta
RX, RY, RS = 790, 860, 0.8                   # regador (bico em ~(660, 950))
BICO, TERRA = [655, 950], [470, 1180]
TX, TY, TS = 300, 1180, 0.85                 # tanque
FX, FY, FS = 735, 1190, 0.9                  # fábrica (testículo)
SAIDA = [890, 1268]
c += [FL(tB),
      {"tipo": "foto", "t": tB, "d": round(KF - tB, 3), "src": M + "sx_pasta.svg", "box": [30, 300, 1020, 1340], "raio": 0, "sombra": True, "fit": "fill", "entra": "desliza", "z": 14},
      {"tipo": "texto", "t": round(tB + 0.3, 3), "d": round(KF - tB - 0.3, 3), "xy": [60, 322], "w": 440, "fonte": "800 30px Montserrat", "cor": "#4a2e0e",
       "alinha": "center", "txt": "O CASO DO POTE", "z": 15, "css": "letter-spacing:2px"}]
# Ficha 1: "Pensa numa planta. Com sede, a água salva."
c += [CARD(K1, K2 + POUSA - K1, "ficha 1 · com sede", 0, -1.2), CLIPE(K1, K2 + POUSA - K1, 0, -1.2),
      TT(K1 + 0.2, round(b(3) - 0.03 - K1 - 0.2, 3), "UMA PLANTA", y=470, fz=130, z=ZC(0)),
      TT(b(3) - 0.03, round(K2 + POUSA - b(3) + 0.03, 3), "COM SEDE, A ÁGUA SALVA", y=470, fz=112, cor=AZUL, z=ZC(0), anim=None, entra="zoom"),
      FIS(K1, round(b(7) - 0.1 - K1, 3), [{"k": "planta_murcha", "xy": [PX, PY], "s": PS, "t": 0.45}], z=ZC(0, 2)),
      FIS(b(3), round(K2 + POUSA - b(3), 3), [{"k": "regador", "xy": [RX, RY], "s": RS, "t": 0.0}], z=ZC(0, 3),
          fluxos=[{"de": BICO, "para": TERRA, "curva": -50, "cor": AGUA, "t": round(b(5) - 0.15 - b(3), 3), "d": 1.4, "n": 8, "viagem": 0.6, "r": 11}]),
      FIS(b(7) - 0.15, round(K2 + POUSA - b(7) + 0.15, 3), [{"k": "planta_vicosa", "xy": [PX, PY], "s": PS, "t": 0.0}], z=ZC(0, 2), pulsos=[{"o": 0, "t": 0.35}]),
      CARIMBO(b(7) + 0.2, round(K2 + POUSA - b(7) - 0.2, 3), "AJUDA", [610, 1270], tam=110, rot=-8, cor=VERDE, z=ZC(0, 5))]
# Ficha 2: "Com a terra já molhada, mais água não faz crescer."
c += [CARD(K2, K3 + POUSA - K2, "ficha 2 · terra molhada", 1, 1.0), CLIPE(K2, K3 + POUSA - K2, 1, 1.0),
      TT(K2 + 0.35, round(K3 + POUSA - K2 - 0.35, 3), "TERRA MOLHADA: NÃO CRESCE MAIS", y=470, fz=105, z=ZC(1)),
      FIS(b(15), round(K3 + POUSA - b(15), 3), [{"k": "sx_poca", "xy": [560, 1428], "s": 0.75, "t": 0.0}], z=ZC(1, 1)),
      FIS(K2, round(K3 + POUSA - K2, 3), [{"k": "planta_vicosa", "xy": [PX, PY], "s": PS, "t": 0.45}], z=ZC(1, 2)),
      FIS(b(13) - 0.3, round(K3 + POUSA - b(13) + 0.3, 3), [{"k": "regador", "xy": [RX, RY], "s": RS, "t": 0.0}], z=ZC(1, 3),
          fluxos=[{"de": BICO, "para": [520, 1300], "curva": -50, "cor": AGUA, "t": 0.3, "d": 1.8, "n": 10, "viagem": 0.7, "r": 11}]),
      CARIMBO(b(16), round(K3 + POUSA - b(16), 3), "NÃO MUDA", [610, 1255], tam=78, rot=-8, cor=CINZA, z=ZC(1, 5))]
# Ficha 3: "O corpo é parecido com vitamina e mineral: quem tem falta, ganha."
c += [CARD(K3, K4 + POUSA - K3, "ficha 3 · no corpo", 2, -0.9), CLIPE(K3, K4 + POUSA - K3, 2, -0.9),
      TT(K3 + 0.35, round(b(26) - 0.05 - K3 - 0.35, 3), "VITAMINA E MINERAL", y=470, fz=125, z=ZC(2)),
      TT(b(26) - 0.05, round(K4 + POUSA - b(26) + 0.05, 3), "COM FALTA: GANHA", y=470, fz=135, cor=VERDE, z=ZC(2), anim=None, entra="zoom"),
      FIS(K3, round(K4 + POUSA - K3, 3),
          [{"k": "sx_tanque_baixo", "xy": [TX, TY], "s": TS, "t": 0.45, "rotulo": "VITAMINA", "rot_y": 240},
           {"k": "dn_fabrica", "xy": [FX, FY], "s": FS, "t": round(b(21) - K3, 3), "rotulo": "TESTÍCULO", "rot_y": 225}], z=ZC(2, 2),
          fluxos=[{"de": [130, 720], "para": [285, 1050], "curva": -40, "cor": "#f2b51d", "t": round(b(26) - K3, 3), "d": 1.3, "n": 6, "viagem": 0.7},
                  {"de": [390, 1180], "para": [610, 1180], "curva": -70, "cor": "#f2b51d", "t": round(b(28) - K3, 3), "d": 1.4, "n": 6, "viagem": 0.6},
                  {"de": SAIDA, "para": [985, 1080], "curva": -20, "cor": "#ffffff", "t": round(b(29) - K3, 3), "d": 1.3, "n": 9, "viagem": 0.45, "r": 10}],
          pulsos=[{"o": 0, "t": round(b(27) - K3, 3)}, {"o": 1, "t": round(b(29) - K3, 3)}]),
      CHECK(b(29) + 0.1, round(K4 + POUSA - b(29) - 0.1, 3), 545, 1480, s=55, z=ZC(2, 4))]
# Ficha 4: "Pra quem não tem falta, o excesso não vira espermatozoide a mais."
c += [CARD(K4, KF - K4 + 0.02, "ficha 4 · sem falta", 3, 1.1), CLIPE(K4, KF - K4 + 0.02, 3, 1.1),
      TT(K4 + 0.25, round(b(35) - K4 - 0.25, 3), "SEM FALTA?", y=470, fz=150, z=ZC(3)),
      TT(b(35), round(KF - b(35), 3), "O EXCESSO NÃO VIRA ESPERMATOZOIDE", y=470, fz=105, cor=VERM, z=ZC(3), anim=None, entra="zoom"),
      FIS(K4, round(KF - K4, 3),
          [{"k": "sx_tanque_cheio", "xy": [TX, TY], "s": TS, "t": 0.45, "rotulo": "VITAMINA", "rot_y": 240},
           {"k": "dn_fabrica", "xy": [FX, FY], "s": FS, "t": 0.6, "rotulo": "TESTÍCULO", "rot_y": 225}], z=ZC(3, 2),
          fluxos=[{"de": SAIDA, "para": [985, 1080], "curva": -20, "cor": "#ffffff", "t": 0.9, "d": 3.4, "n": 5, "viagem": 0.5, "r": 10},
                  {"de": [300, 700], "para": [290, 1000], "curva": 0, "cor": "#f2b51d", "t": round(b(36) - K4, 3), "d": 1.5, "n": 6, "viagem": 0.5},
                  {"de": [385, 1050], "para": [470, 1330], "curva": -30, "cor": "#f2b51d", "t": round(b(36) + 0.4 - K4, 3), "d": 1.6, "n": 7, "viagem": 0.6}],
          pulsos=[{"o": 0, "t": round(b(36) - K4, 3)}]),
      CARIMBO(b(39), round(KF - b(39), 3), "NÃO VIRA A MAIS", [150, 1425], tam=86, rot=-6, cor=VERM, z=ZC(3, 5))]

# ================= E (neutro): o estudo, pele LAB (fundo escuro fixo) =================
E3, E4, E5, E6, E7 = round(e(19) - 0.15, 3), round(e(32) - 0.15, 3), round(e(39) - 0.15, 3), round(e(43) - 0.15, 3), round(e(58) - 0.15, 3)
c += [{"tipo": "fundo", "t": tE, "d": round(tG - tE + 0.05, 3), "cor": "#0b1512", "textura": "grade", "z": 2},
      {"tipo": "flash", "t": tE, "d": 0.3, "max": 0.7},
      # E2 o maior estudo, 2020, 2.370 casais
      GIG(tE, round(E3 - tE, 3), "JAMA 2020", y=1480, tam=380, cont=True, cor="rgba(198,255,61,.30)"),
      TL(tE + 0.05, round(e(8) - 0.1 - tE - 0.05, 3), "O MAIOR ESTUDO", y=640, fz=170, cor=LIMA, anim=None, entra="zoom"),
      TL(e(3) - 0.05, round(E3 - e(3) + 0.05, 3), "EM 2020", y=300, fz=130),
      NUM(e(8) - 0.1, round(E3 - e(8) + 0.1, 3), 370, y=480, pre="2.", de=100, conta=0.9, cor=AMAR, sombra="#5a4600", cor_rotulo=BR, sombra_rotulo="0 3px 8px #000",
          rotulo="casais em tratamento", tam=300),
      FIS(e(13) - 0.1, round(E3 - e(13) + 0.1, 3), [{"k": "sx_casal", "xy": [540, 1260], "s": 0.95, "t": 0.0}], pulsos=[{"o": 0, "t": 0.6}]),
      FL(E3),
      # E3 metade: zinco + ácido fólico (que aparecem nessas fórmulas)
      GIG(E3, round(E5 - E3, 3), "METADE", y=1500, tam=400, cor="rgba(255,255,255,.07)", ida=False),
      TL(E3 + 0.03, round(E4 - E3 - 0.03, 3), "METADE: ZINCO + ÁCIDO FÓLICO", y=290, fz=112, cor=AMAR),
      FIS(E3, round(E6 - E3, 3), [{"k": "sx_casal", "xy": [290, 980], "s": 0.75, "t": 0.1, "rotulo": "SUPLEMENTO", "rot_y": 215},
                                  {"k": "sx_capsula", "xy": [290, 1330], "s": 0.55, "t": round(e(23) - E3, 3)}],
          pulsos=[{"o": 1, "t": round(e(25) - E3, 3)}]),
      FIS(e(28) - 0.1, round(E4 - e(28) + 0.1, 3), [{"k": "sx_pote", "xy": [790, 1130], "s": 0.85, "t": 0.0}], pulsos=[{"o": 0, "t": 0.9}]),
      FL(E4),
      # E4 outra metade: comprimido sem nada
      TL(E4 + 0.03, round(E5 - E4 - 0.03, 3), "OUTRA METADE: COMPRIMIDO SEM NADA", y=290, fz=105),
      FIS(E4, round(E6 - E4, 3), [{"k": "sx_casal", "xy": [790, 980], "s": 0.75, "t": 0.1, "rotulo": "SEM NADA", "rot_y": 215},
                                  {"k": "sx_capsula", "xy": [790, 1330], "s": 0.55, "t": round(e(36) - E4, 3)}],
          pulsos=[{"o": 1, "t": round(e(38) - E4, 3)}]),
      FL(E5),
      # E5 resultado: esperma praticamente igual
      TL(E5 + 0.03, round(E6 - E5 - 0.03, 3), "ESPERMA: PRATICAMENTE IGUAL", y=290, fz=118, cor=LIMA),
      TL(e(40) - 0.1, round(E6 - e(40) + 0.1, 3), "=", y=1000, fz=300, cor=AMAR, anim=None, entra="zoom"),
      FL(E6),
      # E6 nasceu bebê: 34% x 35%
      GIG(E6, round(E7 - E6, 3), "34 × 35", y=1500, tam=380, cont=True, cor="rgba(255,212,0,.28)"),
      TL(E6 + 0.03, round(E7 - E6 - 0.03, 3), "NASCEU BEBÊ", y=290, fz=150),
      NUM(e(47) - 0.1, round(E7 - e(47) + 0.1, 3), 34, y=560, suf="%", tam=200, w=540, cor=AMAR, sombra="#5a4600", cor_rotulo=BR, sombra_rotulo="0 3px 8px #000", rotulo="com suplemento"),
      NUM(e(53) + 0.48, round(E7 - e(53) - 0.48, 3), 35, y=560, suf="%", tam=200, w=540, xy=[540, 560], cor=BR, sombra="#444", cor_rotulo=BR, sombra_rotulo="0 3px 8px #000", rotulo="sem nada"),
      {"tipo": "numero", "t": 0, "d": 0.01, "xy": [-5000, 0], "valor": 0, "z": 1, "tam": 10},  # (nada: só mantém a ordem)
      FIS(e(45) - 0.1, round(E7 - e(45) + 0.1, 3), [{"k": "sx_berco", "xy": [270, 1260], "s": 0.62, "t": 0.0}], pulsos=[{"o": 0, "t": round(e(49) - e(45) + 0.1, 3)}]),
      FIS(e(55) - 0.1, round(E7 - e(55) + 0.1, 3), [{"k": "sx_berco", "xy": [810, 1260], "s": 0.62, "t": 0.0}], pulsos=[{"o": 0, "t": 0.5}]),
      FONTEL(tE, round(E7 - tE, 3), "Schisterman e col., JAMA 2020 · 2.370 casais · doi 10.1001/jama.2019.18714"),
      FL(E7),
      # E7 antioxidantes: prova fraca (Cochrane, 61 estudos)
      GIG(E7, round(tG - E7, 3), "PROVA", y=1480, tam=460, cont=True, cor="rgba(255,45,61,.35)", ida=False),
      TL(E7 + 0.03, round(e(64) - 0.1 - E7 - 0.03, 3), "E OS ANTIOXIDANTES?", y=300, fz=135, cor=ROSA),
      NUM(e(60) - 0.1, round(tG - e(60) + 0.1, 3), 61, y=600, suf=" ESTUDOS", tam=260, cor=AMAR, sombra="#5a4600", cor_rotulo=BR, sombra_rotulo="0 3px 8px #000", rotulo="revisão sobre antioxidantes"),
      CARIMBO(e(65) - 0.05, round(tG - e(65) + 0.05, 3), "PROVA FRACA", [170, 1150], tam=140, rot=-7, cor=VERML),
      FONTEL(E7, round(tG - E7, 3), "Smits e col., Cochrane 2019 · 61 estudos · doi 10.1002/14651858.CD007411.pub4")]

# ================= G (manso): o que fazer, de volta ao papel =================
G2, G3 = round(g(4) - 0.15, 3), round(g(12) - 0.15, 3)
c += [{"tipo": "flash", "t": tG, "d": 0.3, "max": 0.6},
      GIG(tG, round(G2 - tG, 3), "POTE", y=1450, tam=520, cor="rgba(179,18,31,.10)"),
      TT(tG + 0.05, round(G2 - tG - 0.05, 3), "ANTES DO POTE:", y=330, fz=150),
      FIS(tG, round(G2 - tG, 3), [{"k": "sx_pote", "xy": [540, 1060], "s": 1.15, "t": 0.15}]),
      FL(G2),
      {"tipo": "checklist", "t": G2, "d": round(G3 - G2, 3), "box": [90, 330, 900, 880], "titulo": "antes, com os dois:", "z": 40,
       "itens": [{"txt": "Espermograma dele", "t": round(g(4), 3), "marca": round(g(5) + 0.2, 3)},
                 {"txt": "Exames", "t": round(g(6), 3), "marca": round(g(6) + 0.5, 3)},
                 {"txt": "Consulta com vocês dois", "t": round(g(8), 3), "marca": round(g(11), 3)}]},
      FIS(g(9), round(G3 - g(9), 3), [{"k": "sx_casal", "xy": [540, 1400], "s": 0.8, "t": 0.0}], pulsos=[{"o": 0, "t": round(g(11) - g(9), 3)}]),
      FL(G3),
      GIG(G3, round(tC - G3, 3), "MÉDICO", y=1460, tam=440, cont=True, cor="rgba(28,26,23,.2)", ida=False),
      TT(G3 + 0.03, round(tC - G3 - 0.03, 3), "FALTOU ALGO? O MÉDICO REPÕE", y=300, fz=125),
      FIS(G3, round(tC - G3, 3), [{"k": "sx_tanque_baixo", "xy": [540, 1110], "s": 1.0, "t": 0.15}],
          fluxos=[{"de": [230, 640], "para": [520, 990], "curva": -60, "cor": "#f2b51d", "t": round(g(18) - G3 - 0.1, 3), "d": 1.3, "n": 6, "viagem": 0.7, "rotulo": "NA MEDIDA"}],
          pulsos=[{"o": 0, "t": round(g(20) - G3, 3)}]),
      CHECK(g(21), round(tC - g(21), 3), 840, 1300, s=60)]

# ================= C (alegre): cobrança =================
c += [FL(tC),
      GIG(tC, round(c1 - tC, 3), "ECONOMIA", y=1460, tam=400, cor="rgba(46,125,50,.14)"),
      TT(tC + 0.05, round(c1 - tC - 0.05, 3), "ECONOMIZEI O DINHEIRO DO POTE", y=330, fz=125, cor=VERDE),
      FIS(tC, round(c1 - tC, 3), [{"k": "cr_cofrinho", "xy": [540, 1130], "s": 1.15, "t": 0.1}],
          fluxos=[{"de": [540, 640], "para": [520, 960], "curva": 0, "cor": "#ffd400", "t": 0.5, "d": 1.8, "n": 6, "viagem": 0.5, "r": 18}],
          pulsos=[{"o": 0, "t": 1.2}, {"o": 0, "t": 2.2}])]

# ================= CTA (banco cta6) + fecho (F, neutro) =================
F2 = h(4)
TAIL = round(tF + WF[-1]['e'] + 0.06, 3)
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(c2, round(F2 - c2, 3), "ATALHO", y=1400, tam=460, cont=True, cor="rgba(28,26,23,.22)"),
      TT(c2 + 0.05, round(F2 - c2 - 0.05, 3), "VITAMINA NÃO É ATALHO", y=560, fz=140),
      FL(F2),
      GIG(F2, round(dur - F2, 3), "EXAME", y=1480, tam=480, cor="rgba(31,95,168,.14)", ida=False),
      TT(F2 + 0.03, round(dur - F2 - 0.03, 3), "O EXAME MOSTRA O CAMINHO", y=300, fz=125, cor=AZUL),
      FIS(F2, round(dur - F2, 3), [{"k": "cx_exame", "xy": [540, 900], "s": 0.8, "t": 0.15}], pulsos=[{"o": 0, "t": 1.0}]),
      TT(TAIL, round(dur - TAIL, 3), "“ATÉ 40%”", y=1150, fz=130, cor=TINTA, z=58, anim=None, entra="pop"),
      CARIMBO(TAIL + 0.3, round(dur - TAIL - 0.3, 3), "EXAGERO", [250, 1330], tam=140, rot=-8, cor=VERM, z=61),
      FONTE(c2, round(dur - c2, 3), "Schisterman e col., JAMA 2020 · Smits e col., Cochrane 2019 · conteúdo educativo")]
# tira a camada vazia de ordem
c = [L for L in c if not (L.get("tipo") == "numero" and L.get("xy", [0])[0] == -5000)]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json", "gain": 0.16},
       {"src": M + P + "_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + P + "_rosto.mp4", "t": vd, "ms": 0, "d": R1D, "palavras": M + P + "_r1.words.json"},
       {"src": M + P + "_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + P + "_a_voz.words.json"},
       {"src": M + P + "_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + P + "_b_voz.words.json"},
       {"src": M + P + "_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + P + "_e_voz.words.json"},
       {"src": M + P + "_g_voz.wav", "t": tG, "ms": 0, "d": DG, "palavras": M + P + "_g_voz.words.json"},
       {"src": M + P + "_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + P + "_c_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + P + "_f_voz.wav", "t": tF, "ms": 0, "d": DF, "palavras": M + P + "_f_voz.words.json"}]
# trilha contínua por baixo de TUDO depois do viral (nenhuma pausa muda); uma faixa por bloco, emenda cruzada
musica = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.22, "fade": 0.6},
          {"src": "m_viagem", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tE - tB + 0.8, 2), "gain": 0.16, "fade": 0.6},
          {"src": "m_investiga", "t": round(tE - 0.4, 2), "ms": 0, "d": round(tG - tE + 0.8, 2), "gain": 0.22, "fade": 0.6},
          {"src": "m_emocao", "t": round(tG - 0.4, 2), "ms": 0, "d": round(dur - tG + 0.4, 2), "gain": 0.2, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "boing", "t": 3.3, "gain": 0.35},
       {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": vd + 0.05, "gain": 0.35},
       {"src": "boom", "t": vd + 1.0, "gain": 0.45, "pico": 0.3, "d": 1.2},
       # A
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1, "gain": 0.45, "pico": 0.45},
       {"src": "boing", "t": tA + 0.5, "gain": 0.3}, {"src": "whoosh2", "t": A2, "gain": 0.35}, {"src": "riser", "t": a(12) - 0.2, "gain": 0.18, "d": 1.3},
       {"src": "whoosh2", "t": A3, "gain": 0.35}, {"src": "boom", "t": A3 + 0.05, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "whoosh", "t": A4, "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": A4 + 0.35, "gain": 0.3},
       # aula (pasta e fichas caindo)
       {"src": "pagina", "t": tB + 0.05, "gain": 0.45},
       {"src": "papel", "t": K1 + 0.25, "gain": 0.45}, {"src": "whoosh2", "t": b(5) - 0.15, "gain": 0.22}, {"src": "boing", "t": b(7) - 0.1, "gain": 0.25},
       {"src": "boom", "t": b(7) + 0.2, "gain": 0.3, "pico": 0.3, "d": 1.0},
       {"src": "papel", "t": K2 + 0.25, "gain": 0.45}, {"src": "whoosh2", "t": b(13) - 0.2, "gain": 0.22}, {"src": "boom", "t": b(16), "gain": 0.3, "pico": 0.3, "d": 1.0},
       {"src": "papel", "t": K3 + 0.25, "gain": 0.45}, {"src": "boing", "t": b(21), "gain": 0.22}, {"src": "riser", "t": b(26), "gain": 0.15, "d": 1.3}, {"src": "boing", "t": b(29) + 0.1, "gain": 0.25},
       {"src": "papel", "t": K4 + 0.25, "gain": 0.45}, {"src": "whoosh2", "t": b(36), "gain": 0.22}, {"src": "boom", "t": b(39), "gain": 0.3, "pico": 0.3, "d": 1.0},
       # estudo (lab)
       {"src": "whoosh", "t": tE, "gain": 0.45, "pico": 0.45}, {"src": "whoosh2", "t": e(8) - 0.1, "gain": 0.3}, {"src": "boom", "t": e(8), "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "boing", "t": e(13), "gain": 0.25},
       {"src": "whoosh2", "t": E3, "gain": 0.3}, {"src": "boing", "t": e(23), "gain": 0.25}, {"src": "boing", "t": e(28), "gain": 0.22},
       {"src": "whoosh2", "t": E4, "gain": 0.3}, {"src": "boing", "t": e(36), "gain": 0.22},
       {"src": "whoosh2", "t": E5, "gain": 0.3}, {"src": "boom", "t": e(40) - 0.1, "gain": 0.4, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": E6, "gain": 0.3}, {"src": "riser", "t": e(45), "gain": 0.18, "d": 1.2}, {"src": "boom", "t": e(47) - 0.1, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "boom", "t": e(53) + 0.48, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "whoosh", "t": E7, "gain": 0.4, "pico": 0.45}, {"src": "boom", "t": e(60) - 0.1, "gain": 0.4, "pico": 0.3, "d": 1.2}, {"src": "boom", "t": e(65) - 0.05, "gain": 0.5, "pico": 0.3, "d": 1.4},
       # o que fazer
       {"src": "whoosh", "t": tG, "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": G2 + 0.05, "gain": 0.4},
       {"src": "teclado", "t": g(5) + 0.15, "gain": 0.12, "d": 0.4}, {"src": "boing", "t": g(11), "gain": 0.25},
       {"src": "whoosh2", "t": G3, "gain": 0.3}, {"src": "boing", "t": g(21), "gain": 0.25},
       # cobrança
       {"src": "whoosh2", "t": tC, "gain": 0.3}, {"src": "boing", "t": tC + 1.2, "gain": 0.3}, {"src": "boing", "t": tC + 2.2, "gain": 0.25},
       # CTA e fecho
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.4}, {"src": "notif", "t": c1 + 0.2, "gain": 0.35}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.4},
       {"src": "whoosh2", "t": F2, "gain": 0.3}, {"src": "pagina", "t": TAIL, "gain": 0.3}, {"src": "boom", "t": TAIL + 0.3, "gain": 0.5, "pico": 0.3, "d": 1.3}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar(PID, dur, 1415, c, voz, sfx,
       {"r1_fim": r1, "esconde": [[0, 4.1]], "ys": [[4.1, vd, 1480], [vd, r1, 1040], [r1, c1, 1720], [c1, c2, 1560], [c2, dur, 1720]]})
p = json.load(open(f'planos/{PID}.json')); p['audio']['musica'] = musica
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
fala = sum(len(W) for W in (WA, WB, WE, WG, WC, WF))
print("ok dur", dur, "(+1,88 da entrada =", round(dur + 1.88, 2), ") r1", r1, "tA", tA, "tB", tB, "tE", tE, "tG", tG, "tC", tC, "c1", c1, "c2", c2, "tF", tF,
      "| aula", round(tE - tB, 2), "s | narração", fala, "palavras em", round(DA + DB + DE + DG + DC + DF, 1), "s")
