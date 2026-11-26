# plano_l3_bumbum.py (14/11, lote 3, Caneta com Músculo): "bumbum de caneta" (perde o bumbum com as canetas?).
# Viral: programa de rádio dos EUA (via @breakfastclubam), em inglês, dublado pela Murilo (original a 0,16 por baixo).
# Trecho A 16,40-20,40 "When you take these shots... you lose your ass. And it's a real thing." + trecho B 43,88-47,75
# "You got to ask yourself what you want... a flat stomach or a flat ass?" -> MEIA VERDADE.
# A MARCA está queimada no topo do viral: o cartão usa só a faixa do estúdio (y 640-1328 de 1920), crachás com nome dos
# apresentadores borrados (tmp_bb/prep_viral.py). Na fala, caixinha e legenda: "bumbum de caneta", nunca a marca.
# Rosto r1 novo (6cd9, "Escolher? Calma. Não é bem assim.") com o áudio do bloco manso. Entrada ent6 e CTA cta6 do banco.
# Voz em 4 blocos por clima, sem atempo e sem <break> (pausas abertas na edição, tmp_bb/voz.py):
#   a indignado (abertura) | b manso (aula) + o manso (o que fazer) | c neutro (estudos) | e + d alegre (cobrança, fecho).
# Aula: edição LOUSA (giz, legenda manuscrita): desenho de giz das duas camadas (travesseiro de gordura por fora, glúteo
# por baixo), uma ideia por cena; desenhos em assets/midia/bb_giz_*.svg (fotos alinhadas) e fisio_extra/bb_giz_*.svg.
# Depois deste script:
#   python3 scripts/entrada.py react_l3_bumbum assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     '“BUMBUM DE CANETA”?' 'a fala que viralizou no programa de rádio' 'Plantão das Redes' && python3 scripts/pele.py react_l3_bumbum lousa
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l3_bumbum'; P = 'bb'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}bb_{k}_voz.words.json'))
WA, WB, WO, WC, WE, WD = W('a'), W('b'), W('o'), W('c'), W('e'), W('d')
DA, DB, DO, DC, DE, DD = [round(dur_de(f'{M}bb_{k}_voz.wav'), 3) for k in 'aboced']
vd = 7.93                                 # bb_viral.mp4 (4,00 + 3,87)
r1 = round(vd + 3.073 + 0.5, 2)           # bb_r1: última palavra termina em 3,07 s; 0,5 s de folga
tA = round(r1 + 0.15, 2)
tB = round(tA + DA + 0.7, 2)
tC = round(tB + DB + 0.75, 2)             # respiro depois da aula (trilha por baixo)
tO = round(tC + DC + 0.6, 2)
tE = round(tO + DO + 0.55, 2)
c1 = round(tE + DE + 0.15, 2)             # CTA 6cd9 (banco cta6, 4,12 s)
c2 = round(c1 + 4.12, 2)
tD = round(c2 + 0.15, 2)
dur = round(tD + DD + 0.9, 2)
mk_ = lambda T0, WW: (lambda i: round(T0 + WW[i]['s'], 3))
a, b, o, e, q, f = mk_(tA, WA), mk_(tB, WB), mk_(tO, WO), mk_(tC, WC), mk_(tE, WE), mk_(tD, WD)
AF = tC                                   # fim visual da aula
GIZ, AMAR, ROSA, VERM, VERDE = "#f4f1e8", "#ffe27a", "#ff9fb4", "#ff6b6b", "#a8f0b4"
GZ = "text-shadow:0 0 3px rgba(255,255,255,.45),4px 5px 0 rgba(0,0,0,.35)"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.45}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}
def TT(t, d, txt, y=290, fz=130, cor=GIZ, **k):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=GZ, vel=0.09, **k); L["fixo"] = True; return L
def NOTA(t, d, txt, x, y, w=420, tam=100, cor=GIZ, rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "fixo": True, "css": f"transform:rotate({rot}deg);{GZ}"}
def PIL(t, d, txt, x, y, w=300, tam=120, cor=ROSA):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"{tam}px Anton", "cor": cor, "alinha": "center",
            "txt": txt, "z": 47, "entra": "pop", "fixo": True,
            "css": f"border:7px solid {cor};border-radius:34px;padding:4px 0 10px;background:rgba(28,48,39,.88);{GZ}"}
def GIG(t, d, txt, y=1450, tam=420, cont=False, cor="rgba(244,241,232,.10)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12, "fixo": True,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FO(t, d, src, box, entra="pop", z=30):
    return {"tipo": "foto", "t": round(t, 3), "d": round(d, 3), "src": M + src, "box": box, "fit": "contain", "raio": 0, "sombra": False,
            "entra": entra, "z": z, "fixo": True}
def FIS(t, d, orgaos, z=33, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def DS(t, d, formas, cor=AMAR, lw=13, z=45, vel=0.45):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel, "fixo": True}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#1c2b24",
            "alinha": "center", "txt": txt, "css": f"letter-spacing:3px;background:{AMAR};border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}
def FN(t, d, txt):
    L = F(t, d, txt); L["fixo"] = True; return L
BX = [190, 560, 820, 820]                       # corte do quadril (viewBox 440 -> escala 1,864; centro 600,970)
BC = [240, 640, 720, 720]                       # corpo de frente (escala 1,636; centro 600,1000)
cp = lambda u, v: [round(600 + 1.636 * u), round(1000 + 1.636 * v)]
MUS = (540, 980)

# ================= abertura: viral em tela dividida + caixinha =================
c = abertura(P, vd, "via @breakfastclubam", "center", "Mito ou verdade?", "Tem que escolher: barriga ou bumbum?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 278.9, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta": L["escolha"] = 0
c += [{"tipo": "glitch", "t": 3.98, "d": 0.18}]          # emenda dos dois pedaços do viral
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(r1 - vd - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "104px Anton", "cor": GIZ, "alinha": "center",
       "txt": "BUMBUM MURCHAR:\\nPODE.\\nTER QUE ESCOLHER:\\nMITO.", "z": 55, "entra": "pop", "fixo": True,
       "css": f"background:#22392f;border-radius:14px;height:909px;box-sizing:border-box;padding:46px 30px 0;line-height:1.12;{GZ}"},
      {"tipo": "carimbo", "t": vd + 0.45, "d": round(r1 - vd - 0.45, 2), "xy": [150, 715], "txt": "MEIA VERDADE", "tam": 112, "rot": -6, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92)", "fixo": True},
      {"tipo": "video", "t": vd, "d": round(r1 - vd, 2), "ms": 0, "src": M + "bb_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (indignado): o pedaço certo e o mito =================
A2, A3 = round(a(5) - 0.2, 3), round(a(15) - 0.25, 3)
c += [GL(r1), FL(r1),
      GIG(r1, A2 - r1, "METADE", y=1180, tam=520, cont=True, cor="rgba(255,226,122,.35)"),
      TT(tA + 0.02, A2 - tA - 0.07, "METADE É VERDADE", y=380, fz=160),
      DS(a(3), A2 - a(3) - 0.05, [{"k": "check", "c": [540, 1150], "s": 110}], cor=VERDE, lw=26),
      FL(A2),
      GIG(A2, A3 - A2, "MURCHAR", y=1430, tam=420, ida=False),
      TT(A2 + 0.02, A3 - A2 - 0.05, "EMAGRECEU BASTANTE?", y=300, fz=130),
      PIL(a(7), A3 - a(7) - 0.05, "COM OU SEM INJEÇÃO", 90, 640, w=900, tam=100, cor=AMAR),
      TT(a(10), A3 - a(10) - 0.05, "BUMBUM PODE MURCHAR", y=930, fz=150, cor=GIZ),
      DS(a(13), A3 - a(13) - 0.05, [{"k": "seta", "de": [540, 1250], "para": [540, 1480], "curva": 0}], cor=AMAR, lw=18),
      FL(A3),
      GIG(A3, tB - A3, "ESCOLHER", y=1450, tam=400, cont=True, cor="rgba(244,241,232,.3)"),
      TT(A3 + 0.02, tB - A3 - 0.05, "TER QUE ESCOLHER?", y=300, fz=140),
      PIL(a(20), tB - a(20) - 0.05, "BARRIGA", 40, 640, w=420, tam=110, cor=GIZ),
      NOTA(a(21), tB - a(21) - 0.05, "ou", 470, 650, w=140, tam=110, cor=AMAR, rot=0),
      PIL(a(22), tB - a(22) - 0.05, "BUMBUM", 620, 640, w=420, tam=110, cor=GIZ),
      DS(a(23), tB - a(23) - 0.05, [{"k": "x", "c": [540, 720], "s": 260}], cor=ROSA, lw=22),
      TT(a(22) + 0.25, tB - a(22) - 0.25, "NÃO.", y=1000, fz=300, cor=ROSA, anim=None, entra="zoom")]

# ================= B (manso): AULA na LOUSA =================
S2, S3, S4, S4b, S5, S6 = [round(b(i) - 0.2, 3) for i in (5, 13, 24, 31, 36, 43)]
c += [GL(tB), FL(tB), SELO(tB + 0.2, AF - tB - 0.2, "● AULA RÁPIDA")]
# S1 o bumbum tem duas camadas (o contorno de giz se desenha)
c += [GIG(tB, S2 - tB, "CAMADAS", y=1460, tam=420),
      TT(tB + 0.05, S2 - tB - 0.1, "BUMBUM: 2 CAMADAS", y=290, fz=150),
      FO(tB + 0.15, S4 - tB - 0.15, "bb_giz_pele.svg", BX, entra="mascara", z=30)]
# S2 por fora, a gordura = travesseiro
c += [FL(S2),
      GIG(S2, S3 - S2, "TRAVESSEIRO", y=1460, tam=360, cont=True, cor="rgba(255,226,122,.35)", ida=False),
      dict(TT(S2 + 0.05, S3 - S2 - 0.1, "POR FORA: GORDURA = TRAVESSEIRO", y=290, fz=120, cor=AMAR), vel=round((b(12) - S2 - 0.05) / 4, 2)),
      FO(b(7), S4 - b(7), "bb_giz_gordura.svg", BX, entra="pop", z=31),
      NOTA(b(7) + 0.1, S3 - b(7) - 0.15, "1", 860, 700, w=120, tam=130, cor=AMAR, rot=0),
      FIS(b(11) + 0.1, S3 - b(11) - 0.15, [{"k": "bb_giz_travesseiro", "xy": [880, 1330], "s": 0.42}], z=34)]
# S3 por baixo, o glúteo = músculo que te levanta da cadeira
c += [FL(S3),
      GIG(S3, S4 - S3, "GLÚTEO", y=1460, tam=440),
      dict(TT(S3 + 0.05, S4 - S3 - 0.1, "POR BAIXO: GLÚTEO = MÚSCULO", y=290, fz=120, cor=ROSA), vel=round((b(18) - S3 - 0.05) / 4, 2)),
      FO(b(15), S4 - b(15), "bb_giz_gluteo.svg", BX, entra="pop", z=32),
      NOTA(b(15) + 0.1, S4 - b(15) - 0.15, "2", 640, 900, w=120, tam=130, cor=GIZ, rot=0),
      FIS(b(19), S4 - b(19), [{"k": "bb_giz_cadeira", "xy": [890, 1380], "s": 0.5}], z=34, pulsos=[{"o": 0, "t": 0.6}]),
      NOTA(b(19), S4 - b(19) - 0.05, "te levanta!", 30, 1330, w=420, tam=96, cor=AMAR, rot=-5)]
# S4 emagreceu: a gordura sai do corpo todo (pontos amarelos saindo de todo lado ao mesmo tempo)
PT = [(-90, -30, -60, -10), (90, -30, 60, -10), (0, -40, 0, -70), (-60, 20, -70, 10), (60, 20, 70, 10), (-35, 120, -70, 20), (35, 120, 70, 20)]
FLX = [{"de": cp(u, v), "para": cp(u + du * 1.6, v + dv * 1.6), "curva": 0, "cor": AMAR, "t": round(b(26) - S4 - 0.1 + 0.08 * k, 2), "d": 2.2,
        "n": 3, "r": 11, "viagem": 0.85} for k, (u, v, du, dv) in enumerate(PT)]
c += [FL(S4),
      GIG(S4, S4b - S4, "CORPO TODO", y=1460, tam=380, cont=True, cor="rgba(255,226,122,.35)"),
      TT(S4 + 0.02, S4b - S4 - 0.05, "SAI DO CORPO TODO", y=290, fz=140, cor=AMAR),
      FO(S4 + 0.05, S4b - S4 - 0.05, "bb_giz_corpo.svg", BC, entra="pop", z=30),
      FIS(S4 + 0.1, S4b - S4 - 0.1, [], z=34, fluxos=FLX),
      NOTA(S4 + 0.4, S4b - S4 - 0.45, "você não escolhe onde", 140, 1420, w=800, tam=96, cor=GIZ, rot=-3)]
# S4b e o travesseiro murcha junto (o bumbum fica menor; o músculo continua)
c += [FL(S4b),
      TT(S4b + 0.02, S5 - S4b - 0.05, "O TRAVESSEIRO MURCHA", y=290, fz=130, cor=AMAR),
      FO(S4b + 0.05, S5 - S4b - 0.05, "bb_giz_pele_fina.svg", BX, entra="nada", z=30),
      FO(S4b + 0.05, S5 - S4b - 0.05, "bb_giz_gordura_murcha.svg", BX, entra="pop", z=31),
      FO(S4b + 0.05, S5 - S4b - 0.05, "bb_giz_gluteo.svg", BX, entra="nada", z=32),
      DS(S4b + 0.3, S5 - S4b - 0.35, [{"k": "seta", "de": [960, 860], "para": [880, 980], "curva": 20}], cor=AMAR, lw=13),
      NOTA(S4b + 0.3, S5 - S4b - 0.35, "murchou", 700, 700, w=360, tam=100, cor=AMAR, rot=6)]
# S5 o músculo obedece: com serviço, cresce
c += [FL(S5),
      GIG(S5, S6 - S5, "CRESCE", y=1480, tam=440),
      TT(S5 + 0.02, b(40) - S5 - 0.07, "O MÚSCULO OBEDECE", y=290, fz=140, cor=ROSA),
      TT(b(40), S6 - b(40) - 0.05, "COM SERVIÇO: CRESCE", y=290, fz=140, cor=AMAR, anim=None, entra="zoom"),
      FIS(S5 + 0.05, b(42) - S5 - 0.05, [{"k": "bb_giz_musculo", "xy": list(MUS), "s": 1.05}], z=33),
      FIS(b(40), S6 - b(40), [{"k": "haltere", "xy": [540, 1390], "s": 0.7}], z=34, pulsos=[{"o": 0, "t": 0.5}, {"o": 0, "t": 1.1}]),
      FIS(b(42), AF - b(42), [{"k": "bb_giz_musculo", "xy": list(MUS), "s": 1.5}], z=33,
          encolhe=[{"o": 0, "t": round(b(44) - b(42), 2), "para": 0.95, "d": 1.3}]),
      DS(b(42) + 0.1, S6 - b(42) - 0.15, [{"k": "seta", "de": [900, 1160], "para": [900, 820], "curva": 0}], cor=AMAR, lw=18)]
# S6 ficou parado: encolhe (o mesmo músculo grande encolhe e perde a cor; sofá no lugar do haltere)
c += [FL(S6),
      GIG(S6, AF - S6, "PARADO", y=1480, tam=440, ida=False),
      TT(S6 + 0.02, AF - S6 - 0.05, "PARADO: ENCOLHE", y=290, fz=150, cor=ROSA, anim=None, entra="zoom"),
      FIS(S6 + 0.05, AF - S6 - 0.05, [{"k": "bb_giz_sofa", "xy": [540, 1400], "s": 0.62}], z=34),
      DS(b(45), AF - b(45), [{"k": "seta", "de": [900, 820], "para": [900, 1160], "curva": 0}], cor=ROSA, lw=18)]
SFX_AULA = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": tB + 0.2, "gain": 0.22},
            {"src": "whoosh2", "t": S2, "gain": 0.3}, {"src": "boing", "t": b(7), "gain": 0.28}, {"src": "boing", "t": b(11) + 0.1, "gain": 0.25},
            {"src": "whoosh2", "t": S3, "gain": 0.3}, {"src": "boing", "t": b(15), "gain": 0.28}, {"src": "notif", "t": b(21) + 0.1, "gain": 0.28},
            {"src": "whoosh", "t": S4, "gain": 0.35, "pico": 0.45}, {"src": "riser", "t": b(26) - 0.3, "gain": 0.18, "d": 1.6},
            {"src": "whoosh2", "t": S4b, "gain": 0.3}, {"src": "papel", "t": b(34), "gain": 0.35},
            {"src": "whoosh2", "t": S5, "gain": 0.3}, {"src": "boing", "t": b(40), "gain": 0.28}, {"src": "boom", "t": b(42), "gain": 0.45, "pico": 0.3, "d": 1.2},
            {"src": "whoosh2", "t": S6, "gain": 0.3}, {"src": "boing", "t": b(45), "gain": 0.22}]

# ================= C (neutro): os dois estudos =================
E2, E3, E4, E5, E6 = [round(e(i) - 0.2, 3) for i in (11, 19, 24, 27, 44)]
E4 = round(e(24) - 0.05, 3)
E5b = round(e(35) - 0.15, 3)
c += [GL(AF), FL(AF),
      # E1 um estudo: 11 jovens treinaram só uma perna por 12 semanas
      GIG(AF, E2 - AF, "ESTUDO", y=1460, tam=440, cont=True, cor="rgba(244,241,232,.3)"),
      TT(AF + 0.05, E2 - AF - 0.1, "TREINARAM SÓ 1 PERNA", y=290, fz=130),
      FO(AF + 0.1, E4 - AF - 0.1, "bb_giz_corpo.svg", BC, entra="pop", z=30),
      NOTA(e(2), E2 - e(2) - 0.05, "11 jovens", 20, 1080, w=380, tam=100, cor=GIZ, rot=-4),
      FO(e(4), E4 - e(4), "bb_giz_perna.svg", BC, entra="zoom", z=31),
      NOTA(e(8), E2 - e(8) - 0.05, "12 semanas", 20, 1210, w=440, tam=96, cor=AMAR, rot=4),
      FL(E2),
      # E2 a gordura caiu nos braços (-10%) e no tronco (-7%)
      TT(E2 + 0.02, E3 - E2 - 0.05, "A GORDURA CAIU AQUI", y=290, fz=130, cor=AMAR),
      PIL(e(15), E4 - e(15) - 0.05, "-10%", 80, 700, w=290, tam=108, cor=ROSA),
      NOTA(e(15), E4 - e(15) - 0.05, "braços", 80, 860, w=290, tam=96, cor=GIZ, rot=-3),
      DS(e(15) + 0.1, E4 - e(15) - 0.15, [{"k": "seta", "de": [250, 980], "para": [430, 960], "curva": 20}], cor=ROSA, lw=12),
      PIL(e(18), E4 - e(18) - 0.05, "-7%", 720, 700, w=280, tam=108, cor=ROSA),
      NOTA(e(18), E4 - e(18) - 0.05, "tronco", 720, 860, w=280, tam=96, cor=GIZ, rot=3),
      DS(e(18) + 0.1, E4 - e(18) - 0.15, [{"k": "seta", "de": [800, 980], "para": [640, 920], "curva": -20}], cor=ROSA, lw=12),
      FIS(e(13), E3 - e(13), [], z=34, fluxos=[{"de": cp(-90, -30), "para": cp(-150, -70), "curva": 0, "cor": AMAR, "t": 0.1, "d": 1.8, "n": 3, "r": 10, "viagem": 0.8},
                                                {"de": cp(90, -30), "para": cp(150, -70), "curva": 0, "cor": AMAR, "t": 0.2, "d": 1.8, "n": 3, "r": 10, "viagem": 0.8},
                                                {"de": cp(0, -60), "para": cp(0, -110), "curva": 0, "cor": AMAR, "t": 0.9, "d": 1.4, "n": 3, "r": 10, "viagem": 0.8}]),
      FL(E3),
      # E3 na perna treinada: sem mudança
      TT(E3 + 0.02, E4 - E3 - 0.05, "E NA PERNA TREINADA?", y=290, fz=130),
      PIL(e(21), E4 - e(21) - 0.05, "SEM MUDANÇA", 380, 1390, w=640, tam=104, cor=AMAR),
      DS(e(21), E4 - e(21) - 0.05, [{"k": "seta", "de": [700, 1390], "para": [680, 1300], "curva": 10}], cor=AMAR, lw=12),
      FN(AF, E5 - AF, "Ramírez-Campillo e col., J Strength Cond Res 2013 · 11 jovens, 12 semanas · doi 10.1519/JSC.0b013e31827e8681"),
      FL(E4),
      # E4 agora, o músculo
      GIG(E4, E5 - E4, "GLÚTEO", y=1300, tam=520, ida=False),
      TT(E4 + 0.02, E5 - E4 - 0.05, "E O MÚSCULO?", y=640, fz=230, cor=AMAR, anim=None, entra="zoom"),
      FL(E5),
      # E5 outro estudo: 9 semanas de agachamento ou elevação de quadril
      TT(E5 + 0.02, E5b - E5 - 0.05, "JOVENS QUE NUNCA TREINAVAM", y=290, fz=120),
      {"tipo": "artigo", "t": E5 + 0.05, "d": round(E6 - E5 - 0.1, 2), "box": [100, 820, 880, 600], "z": 34, "fixo": True,
       "revista": "Frontiers in Physiology · 2023", "titulo": "Agachamento ou elevação de quadril: o glúteo cresceu igual",
       "autores": "Plotkin e col. · 34 jovens sem treino · área do glúteo na ressonância", "rola": 0,
       "linhas": [{"txt": "9 semanas de treino com supervisão.", "grifo": e(35)},
                  {"txt": "Glúteo medido antes e depois.", "grifo": e(41)}],
       "rodape": "doi 10.3389/fphys.2023.1279170"},
      {"tipo": "numero", "t": E5b, "d": round(E6 - E5b - 0.05, 2), "xy": [0, 330], "valor": 9, "suf": " SEMANAS", "tam": 230, "z": 44, "fixo": True,
       "cor": AMAR, "sombra": "#0e1a14", "conta": 0.4},
      FL(E6),
      # E6 na ressonância, o glúteo cresceu
      GIG(E6, tO - E6, "CRESCEU", y=1480, tam=440),
      TT(E6 + 0.02, tO - E6 - 0.05, "NA RESSONÂNCIA: O GLÚTEO CRESCEU", y=290, fz=120, cor=AMAR),
      FIS(E6 + 0.05, e(48) - E6 - 0.05, [{"k": "bb_giz_musculo", "xy": list(MUS), "s": 1.05}], z=33),
      FIS(e(48), tO - e(48), [{"k": "bb_giz_musculo", "xy": list(MUS), "s": 1.5}], z=33, pulsos=[{"o": 0, "t": 0.5}]),
      DS(e(48) + 0.1, tO - e(48) - 0.15, [{"k": "seta", "de": [900, 1160], "para": [900, 820], "curva": 0}], cor=AMAR, lw=18),
      FN(E5, tO - E5, "Plotkin e col., Front Physiol 2023 · 34 jovens sem treino, 9 semanas · doi 10.3389/fphys.2023.1279170")]
SFX_EST = [{"src": "pagina", "t": AF + 0.1, "gain": 0.4}, {"src": "boing", "t": e(2), "gain": 0.25}, {"src": "whoosh2", "t": e(4), "gain": 0.3},
           {"src": "boing", "t": e(9), "gain": 0.25}, {"src": "whoosh2", "t": E2, "gain": 0.3}, {"src": "notif", "t": e(15), "gain": 0.3},
           {"src": "notif", "t": e(18), "gain": 0.3}, {"src": "whoosh2", "t": E3, "gain": 0.3}, {"src": "boing", "t": e(22), "gain": 0.3},
           {"src": "whoosh", "t": E4, "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": E5 + 0.05, "gain": 0.45},
           {"src": "riser", "t": E5b - 1.1, "gain": 0.18, "d": 1.2}, {"src": "boom", "t": E5b, "gain": 0.45, "pico": 0.3, "d": 1.3},
           {"src": "whoosh2", "t": E6, "gain": 0.3}, {"src": "boom", "t": e(48), "gain": 0.45, "pico": 0.3, "d": 1.2}]

# ================= O (manso): o que fazer (sem indicar nem contraindicar) =================
O2 = round(o(13) - 0.2, 3)
c += [GL(tO), FL(tO),
      GIG(tO, O2 - tO, "MÉDICO", y=1460, tam=440, cont=True, cor="rgba(244,241,232,.3)"),
      TT(tO + 0.05, O2 - tO - 0.1, "USA CANETA?", y=330, fz=180, cor=AMAR, anim=None, entra="zoom"),
      TT(o(5) - 0.2, O2 - o(5) + 0.15, "CONVERSA COM O MÉDICO", y=640, fz=130),
      FL(O2),
      GIG(O2, tE - O2, "FORÇA", y=1460, tam=460, ida=False),
      TT(O2 + 0.02, tE - O2 - 0.05, "NA CONSULTA:", y=290, fz=140),
      NOTA(o(13), tE - o(13) - 0.05, "treino de força", 150, 560, w=700, tam=120, cor=GIZ, rot=-2),
      DS(o(15), tE - o(15) - 0.05, [{"k": "check", "c": [110, 640], "s": 40}], cor=VERDE, lw=16),
      NOTA(o(16), tE - o(16) - 0.05, "proteína", 150, 760, w=700, tam=120, cor=GIZ, rot=-2),
      DS(o(17), tE - o(17) - 0.05, [{"k": "check", "c": [110, 840], "s": 40}], cor=VERDE, lw=16),
      FIS(o(18), tE - o(18), [{"k": "bb_giz_musculo", "xy": [540, 1180], "s": 0.85}], z=33, pulsos=[{"o": 0, "t": 0.5}]),
      NOTA(o(18), tE - o(18) - 0.05, "pra segurar o músculo", 140, 1390, w=800, tam=96, cor=AMAR, rot=-3)]
SFX_O = [{"src": "whoosh", "t": tO + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "whoosh2", "t": o(5), "gain": 0.3},
         {"src": "papel", "t": O2 + 0.05, "gain": 0.4}, {"src": "notif", "t": o(15), "gain": 0.3}, {"src": "notif", "t": o(17), "gain": 0.3},
         {"src": "boing", "t": o(18), "gain": 0.25}]

# ================= E (alegre): cobrança =================
c += [GL(tE), FL(tE),
      TT(tE + 0.02, c1 - tE + 0.02, "BARRIGA E BUMBUM", y=360, fz=160, cor=GIZ),
      DS(q(5), c1 - q(5), [{"k": "check", "c": [330, 870], "s": 70}], cor=VERDE, lw=22),
      DS(q(7), c1 - q(7), [{"k": "check", "c": [750, 870], "s": 70}], cor=VERDE, lw=22),
      NOTA(tE + 0.1, c1 - tE - 0.08, "sem escolher!", 240, 1010, w=600, tam=110, cor=AMAR, rot=-4)]

# ================= CTA (banco cta6) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (alegre): fecho + carimbo =================
D2 = round(f(4) - 0.2, 3)
FLX_D = [{"de": cp(u, v), "para": cp(u + du * 1.4, v + dv * 1.4), "curva": 0, "cor": AMAR, "t": 0.15 + 0.06 * k, "d": 1.6, "n": 2, "r": 9, "viagem": 0.75}
         for k, (u, v, du, dv) in enumerate(PT)]
c += [GL(c2), FL(c2),
      TT(c2 + 0.05, dur - c2 - 0.05, "GORDURA NÃO ESCOLHE LUGAR.", y=280, fz=130, cor=GIZ),
      FO(tD, D2 - tD, "bb_giz_corpo.svg", [330, 560, 420, 420], entra="pop", z=30),
      FIS(tD + 0.05, D2 - tD - 0.05, [], z=34, fluxos=[dict(fx, de=[round(540 + (fx["de"][0] - 600) * 420 / 720), round(770 + (fx["de"][1] - 1000) * 420 / 720)],
                                                            para=[round(540 + (fx["para"][0] - 600) * 420 / 720), round(770 + (fx["para"][1] - 1000) * 420 / 720)]) for fx in FLX_D]),
      FL(D2),
      GIG(D2, dur - D2, "VOCÊ ESCOLHE", y=1480, tam=380, cont=True, cor="rgba(255,226,122,.35)"),
      FIS(D2 + 0.05, dur - D2 - 0.05, [{"k": "bb_giz_musculo", "xy": [540, 860], "s": 1.0}], z=33, pulsos=[{"o": 0, "t": 0.9}]),
      TT(f(4), dur - f(4), "MÚSCULO, VOCÊ ESCOLHE.", y=1110, fz=140, cor=AMAR, anim=None, entra="zoom"),
      {"tipo": "carimbo", "t": round(f(6) + 0.1, 3), "d": round(dur - f(6) - 0.1, 3), "xy": [190, 1470], "txt": "MEIA VERDADE", "tam": 110, "rot": -6,
       "z": 60, "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92)", "fixo": True},
      FN(c2, dur - c2, "Ramírez-Campillo e col. 2013 · Plotkin e col. 2023 · Conteúdo educativo. Converse com o seu médico.")]

voz = [{"src": M + "bb_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "bb_viral.words.json", "gain": 0.16},
       {"src": M + "bb_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "bb_r1.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "bb_r1.words.json"},
       {"src": M + "bb_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "bb_a_voz.words.json"},
       {"src": M + "bb_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "bb_b_voz.words.json"},
       {"src": M + "bb_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "bb_c_voz.words.json"},
       {"src": M + "bb_o_voz.wav", "t": tO, "ms": 0, "d": DO, "palavras": M + "bb_o_voz.words.json"},
       {"src": M + "bb_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "bb_e_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "bb_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "bb_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "glitch", "t": 3.98, "gain": 0.25}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.45, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45},
       {"src": "notif", "t": a(3), "gain": 0.35}, {"src": "whoosh2", "t": A2, "gain": 0.35}, {"src": "boing", "t": a(7), "gain": 0.28},
       {"src": "whoosh2", "t": a(13), "gain": 0.3}, {"src": "whoosh2", "t": A3, "gain": 0.35}, {"src": "boing", "t": a(20), "gain": 0.25},
       {"src": "boing", "t": a(22), "gain": 0.25}, {"src": "boom", "t": a(23), "gain": 0.5, "pico": 0.3, "d": 1.3},
       {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, *SFX_EST,
       {"src": "glitch", "t": tO - 0.05, "gain": 0.45}, *SFX_O,
       {"src": "glitch", "t": tE - 0.05, "gain": 0.45}, {"src": "notif", "t": q(5), "gain": 0.3}, {"src": "notif", "t": q(7), "gain": 0.3},
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
       {"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": tD + 0.05, "gain": 0.3},
       {"src": "whoosh", "t": D2, "gain": 0.35, "pico": 0.45}, {"src": "boom", "t": f(6) + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 1114, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": round(r1 - 0.3, 2), "d": round(c1 - r1 + 0.6, 2), "gain": 0.16, "fade": 0.8},
                        {"src": "m_emocao", "t": round(c2 - 0.2, 2), "d": round(dur - c2 + 0.2, 2), "gain": 0.15, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "AF", AF, "tO", tO, "tE", tE, "c1", c1, "c2", c2, "tD", tD)
