# plano_l4_corpo.py (14/11, lote 4, Caneta com Músculo): "meu corpo não escuta" (frase de uma famosa num programa de TV inglês).
# Viral: Good Morning Britain (via @goodmorningbritain), em inglês, dublado pela Murilo (original a 0,16 por baixo).
#   Trecho ÚNICO 27,72-39,20 s do original (1 quadro depois de 27,68, onde a legenda queimada ainda dizia "Yeah, but";
#   e o recorte y 40-1086 tira a legenda queimada inteira). Fora do corte: o remédio (16,9-19,9), a pergunta sobre
#   ela estar magra (20,5-25,6) e o marido (39,2 em diante). Conferido de ouvido (faster-whisper medium): começa no "But",
#   termina no "is." antes do "Interesting". Nome dela fora da fala e da tela (crédito só o @).
# Veredito: MEIA VERDADE (caixinha DEPENDE): o peso de cada um tem ritmo e só o médico avalia; o músculo escuta o treino.
# Voz: 4 create_speech por clima SEM <break> e SEM atempo (pausas abertas na edição, tmp_ne/voz.py):
#   indignado (abertura) | manso (aula + o que fazer) | neutro (estudo + fecho) | alegre (r1 + cobrança).
#   Rosto r1 6cd9 (HeyGen, áudio do bloco alegre "Escuta, sim. Só precisa do recado certo.").
# Entrada rk_ent ("Olha só essa notícia", banco) e CTA cta6 (banco).
# EDIÇÃO da aula: CELULAR COM MANCHETES (app "Plantão do Corpo", foto fixa tmp_ne/telas.py) na pele NOTÍCIA (vinho):
#   cartões de manchete caem na tela, notificação traz o "recado", modo noite no descanso; desenhos novos
#   fisio_extra/ne_planta_em_pe, ne_planta_murcha, ne_regador, ne_regador_haltere, ne_fibra, ne_fibra_tijolos saem da tela.
# Depois deste script:
#   python3 scripts/entrada.py react_l4_corpo assets/midia/rk_ent.mp4 assets/midia/rk_ent.mp4.words.json 2.07 \
#     '“MEU CORPO NÃO ESCUTA”?' 'a frase de uma famosa num programa de TV inglês' 'Plantão das Redes' && python3 scripts/pele.py react_l4_corpo noticia
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l4_corpo'; P = 'ne'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}ne_{k}_voz.words.json'))
WA, WB, WO, WC, WD, WE = W('a'), W('b'), W('o'), W('c'), W('d'), W('e')
DA, DB, DO, DC, DD, DE = [round(dur_de(f'{M}ne_{k}_voz.wav'), 3) for k in 'abocde']
vd = 11.48                                 # ne_viral.mp4
R1D = 3.70                                 # ne_rosto.mp4: "certo." termina em ~3,20 s; 0,5 s de folga
r1 = round(vd + R1D, 2)
tA = round(r1 + 0.15, 2)
tB = round(tA + DA + 0.7, 2)
tC = round(tB + DB + 0.75, 2)
tO = round(tC + DC + 0.65, 2)
tE = round(tO + DO + 0.6, 2)
c1 = round(tE + DE + 0.15, 2)              # CTA 6cd9 (banco cta6, 4,12 s)
c2 = round(c1 + 4.12, 2)
tD = round(c2 + 0.15, 2)
dur = round(tD + DD + 1.2, 2)
mk_ = lambda T0, WW: (lambda i: round(T0 + WW[i]['s'], 3))
a, b, o, e, q, f = mk_(tA, WA), mk_(tB, WB), mk_(tO, WO), mk_(tC, WC), mk_(tE, WE), mk_(tD, WD)
AF = tC                                    # fim visual da aula
BR, AMAR, VERDE, VERM, AZUL, TINTA = "#ffffff", "#ffd400", "#3ddc84", "#ff4d5a", "#5ec4d6", "#111111"
SH = "text-shadow:6px 6px 0 rgba(0,0,0,.35)"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}
def TT(t, d, txt, y=300, fz=130, cor=BR, **k):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SH, vel=0.09, **k); L["fixo"] = True; return L
def GIG(t, d, txt, y=700, tam=420, cont=False, cor="rgba(255,255,255,.07)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12, "fixo": True,
         "x": [1100, -int(len(txt) * tam * 0.5)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=40, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def DS(t, d, formas, cor=AMAR, lw=14, z=44, vel=0.45):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel, "fixo": True}
def PIL(t, d, txt, x, y, w=600, tam=90, cor=AMAR, fundo="rgba(20,7,10,.9)", z=47):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"{tam}px Anton", "cor": cor, "alinha": "center",
            "txt": txt, "z": z, "entra": "pop", "fixo": True, "css": f"border:7px solid {cor};border-radius:30px;padding:2px 0 8px;background:{fundo}"}
def SELO(t, d, txt, cor="#ff2d3d", cor_txt="#ffffff"):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": cor_txt,
            "alinha": "center", "txt": txt, "css": f"letter-spacing:3px;background:{cor};border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}
def FN(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 214], "w": 1000, "fonte": "600 26px Montserrat", "cor": "#ffffff",
            "alinha": "center", "txt": txt, "z": 70, "fixo": True, "css": "text-shadow:0 2px 6px #000;background:rgba(0,0,0,.45);border-radius:10px;padding:4px 10px"}
# ---- o celular (foto fixa 900x1770, a 1,5x) e o que vai DENTRO da tela (tela x 123..957; cabeçalho y 336..465) ----
PH = [90, 210, 900, 1770]
def CEL(t, d, noite=False, entra="nada"):
    return {"tipo": "foto", "t": round(t, 3), "d": round(d, 3), "src": M + ("ne_cel_noite.png" if noite else "ne_cel_dia.png"), "box": PH,
            "fit": "contain", "raio": 100, "sombra": True, "entra": entra, "dy": 1300, "z": 30, "fixo": True}
from PIL import ImageFont
_FA = {}
def nlin(txt, tam, w):
    f = _FA.setdefault(tam, ImageFont.truetype('assets/fonts/Anton-Regular.ttf', tam))
    n, cur = 1, ''
    for wd in txt.split():
        tt = (cur + ' ' + wd).strip()
        if f.getlength(tt) > w and cur: n += 1; cur = wd
        else: cur = tt
    return n
CY0, CW = 490, 780                          # topo e largura dos cartões de manchete
def alt(txt, tam=104): return round(60 + 26 + nlin(txt, tam, CW - 60) * tam * 1.04)
def CARD(t, d, txt, cor=TINTA, tam=104, y=CY0, kicker="PLANTÃO DO CORPO · AGORA", kcor="#c8102e", fundo="#ffffff", z=36):
    """manchete que cai no feed do celular (cartão branco; a linha de cima é o 'chapéu' da notícia)"""
    base = dict(t=round(t, 3), d=round(d, 3), entra="desliza", dy=-150, dx=0, fixo=True)
    return [dict(base, tipo="texto", xy=[150, y], w=CW, fonte=f"{tam}px Anton", cor=cor, alinha="left", txt=txt, z=z,
                 css=f"box-sizing:border-box;background:{fundo};border-radius:28px;padding:60px 30px 26px;box-shadow:0 10px 26px rgba(0,0,0,.28);line-height:1.04"),
            dict(base, tipo="texto", xy=[180, y + 20], w=700, fonte="800 26px Montserrat", cor=kcor, alinha="left", txt=kicker, z=z + 1,
                 css="letter-spacing:2px")]
def NOTIF(t, d, app, txt, cor=TINTA, tam=100, y=262):
    base = dict(t=round(t, 3), d=round(d, 3), entra="desliza", dy=-300, dx=0, fixo=True)
    return [dict(base, tipo="texto", xy=[130, y], w=820, fonte=f"{tam}px Anton", cor=cor, alinha="left", txt=txt, z=48,
                 css="box-sizing:border-box;background:rgba(250,250,252,.97);border-radius:34px;padding:54px 30px 18px;box-shadow:0 14px 34px rgba(0,0,0,.45);line-height:1.04"),
            dict(base, tipo="texto", xy=[160, y + 18], w=700, fonte="800 24px Montserrat", cor="#777777", alinha="left", txt=f"{app} · agora", z=49,
                 css="letter-spacing:1px")]
CX = 540                                    # centro dos desenhos; a área livre vai de ~930 a ~1660

# ================= abertura: viral em tela dividida + caixinha =================
c = abertura(P, vd, "via @goodmorningbritain", "center", "Mito ou verdade?", "O corpo para de escutar?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 7.9, "dec": 1, "suf": " MI DE VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta":
        L["botoes"] = ["MITO", "VERDADE", "DEPENDE"]; L["escolha"] = 2; L["t_escolha"] = 3.3
# r1: "Escuta, sim. Só precisa do recado certo." (painel cobre o quadro parado dela)
PAINEL = "background:#2a0a10;border-radius:14px;height:909px;box-sizing:border-box;line-height:1.05;" + SH
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(R1D - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "200px Anton", "cor": AMAR, "alinha": "center",
       "txt": "ESCUTA,\\nSIM.", "z": 55, "entra": "pop", "fixo": True, "css": PAINEL + ";padding:90px 30px 0"},
      {"tipo": "texto", "t": round(vd + 1.45, 2), "d": round(R1D - 1.45, 2), "xy": [110, 700], "w": 860, "fonte": "110px Anton", "cor": BR, "alinha": "center",
       "txt": "PRECISA DO RECADO CERTO", "z": 56, "entra": "zoom", "fixo": True, "css": SH},
      FIS(vd + 1.6, round(R1D - 1.6, 2), [{"k": "raio", "xy": [915, 610], "s": 0.42}], z=57, pulsos=[{"o": 0, "t": 0.9}]),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + "ne_rosto.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (indignado): só a frase; peso tem ritmo; o músculo escuta =================
A2, A3, A4 = round(a(9) - 0.25, 3), round(a(16) - 0.25, 3), round(a(21) - 0.25, 3)
QUOTE = "background:#ffffff;border-radius:22px;padding:26px 30px 30px;box-shadow:0 20px 50px rgba(0,0,0,.5);transform:rotate(-2deg)"
c += [GL(r1), FL(r1), SELO(tA + 0.2, tB - tA - 0.25, "● CHECAGEM · O QUE A CIÊNCIA DIZ"),
      # A1 "Eu não examinei ninguém, tá? Falo só da frase."
      GIG(tA, A2 - tA, "FRASE", y=1260, tam=460, cont=True, cor="rgba(255,212,0,.30)"),
      TT(tA + 0.02, A2 - tA - 0.07, "NÃO EXAMINEI NINGUÉM", y=300, fz=140),
      {"tipo": "texto", "t": round(tA + 0.5, 3), "d": round(A2 - tA - 0.55, 3), "xy": [110, 640], "w": 860, "fonte": "italic 700 84px 'Source Serif 4'",
       "cor": TINTA, "alinha": "center", "txt": "“Meu corpo não escuta.”", "z": 42, "entra": "cai", "fixo": True, "css": "box-sizing:border-box;" + QUOTE},
      PIL(max(a(4) + 0.15, min(a(5) - 0.1, A2 - 1.9)), A2 - max(a(4) + 0.15, min(a(5) - 0.1, A2 - 1.9)) - 0.05, "SÓ DA FRASE", 240, 1060, w=600, tam=120),
      # A2 "Peso, cada corpo tem o seu ritmo."
      FL(A2),
      GIG(A2, A3 - A2, "RITMO", y=1300, tam=460, ida=False),
      TT(A2 + 0.02, A3 - A2 - 0.03, "PESO: CADA CORPO, SEU RITMO", y=300, fz=120),
      FIS(A2 + 0.05, A3 - A2 - 0.05, [{"k": "balanca", "xy": [330, 1000], "s": 0.85, "t": 0.1},
                                       {"k": "cy_relogio", "xy": [770, 1000], "s": 0.95, "t": round(a(14) - A2, 3)}],
          pulsos=[{"o": 1, "t": round(a(15) - A2 + 0.2, 3)}]),
      # A3 "Agora, corpo que não escuta?"
      FL(A3),
      TT(A3 + 0.02, A4 - A3 - 0.07, "CORPO QUE NÃO ESCUTA?", y=300, fz=140, cor=AMAR),
      {"tipo": "texto", "t": round(a(17), 3), "d": round(A4 - a(17) - 0.05, 3), "xy": [40, 600], "w": 1000, "fonte": "640px Anton", "cor": BR,
       "alinha": "center", "txt": "?", "z": 42, "entra": "zoom", "fixo": True, "css": "text-shadow:14px 14px 0 rgba(0,0,0,.35)"},
      # A4 "O músculo escuta. Em qualquer idade."
      FL(A4),
      GIG(A4, tB - A4, "QUALQUER IDADE", y=1420, tam=380, cont=True, cor="rgba(61,220,132,.35)"),
      TT(A4 + 0.02, tB - A4 - 0.05, "O MÚSCULO ESCUTA", y=300, fz=160, cor=VERDE),
      FIS(A4 + 0.05, tB - A4 - 0.05, [{"k": "musculo", "xy": [540, 900], "s": 1.25, "t": 0.1}],
          pulsos=[{"o": 0, "t": round(a(23) - A4, 3)}, {"o": 0, "t": round(a(26) - A4, 3)}]),
      PIL(a(24) - 0.05, tB - a(24), "EM QUALQUER IDADE", 170, 1180, w=740, tam=104, cor=VERDE)]
SFX_A = [{"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45},
         {"src": "papel", "t": tA + 0.5, "gain": 0.4}, {"src": "boing", "t": a(5), "gain": 0.25},
         {"src": "whoosh2", "t": A2, "gain": 0.3}, {"src": "boing", "t": a(14), "gain": 0.25},
         {"src": "whoosh2", "t": A3, "gain": 0.3}, {"src": "scratch", "t": a(17), "gain": 0.22},
         {"src": "whoosh", "t": A4, "gain": 0.35, "pico": 0.45}, {"src": "boom", "t": a(22), "gain": 0.4, "pico": 0.3, "d": 1.2},
         {"src": "notif", "t": a(24), "gain": 0.3}]

# ================= B (manso): AULA no CELULAR COM MANCHETES =================
S2, S3, S4, S5, S6 = [round(b(i) - 0.25, 3) for i in (7, 10, 15, 22, 32)]
c += [GL(tB), FL(tB), SELO(tB + 0.2, AF - tB - 0.25, "● AULA RÁPIDA", cor=AMAR, cor_txt="#1a0508"),
      CEL(tB, S6 - tB + 0.02, entra="desliza")]
# S1 "O músculo é como planta no vaso."
c += [*CARD(tB + 0.1, S2 - tB - 0.12, "MÚSCULO É COMO PLANTA"),
      FIS(b(4) - 0.05, b(9) - b(4), [{"k": "ne_planta_em_pe", "xy": [CX, 1290], "s": 1.35}])]
# S2 "Sem água, murcha."
c += [*CARD(S2, S3 - S2 - 0.02, "SEM ÁGUA: MURCHA", cor="#b3121f"),
      FIS(b(9) - 0.05, S3 - b(9) + 0.05, [{"k": "ne_planta_murcha", "xy": [CX, 1290], "s": 1.35}])]
# S3 "Com água, volta a crescer." (o regador entra no alto à direita e rega pela esquerda; a planta levanta)
PLX, PLY = 400, 1370
c += [*CARD(S3, S4 - S3 - 0.02, "COM ÁGUA: CRESCE", cor="#16803c"),
      FIS(S3, b(12) - S3, [{"k": "ne_planta_murcha", "xy": [PLX, PLY], "s": 1.1}]),
      FIS(b(12) - 0.05, b(16) - b(12), [{"k": "ne_planta_em_pe", "xy": [PLX, PLY], "s": 1.1}], z=40),
      FIS(S3 + 0.1, b(21) - S3 - 0.18, [{"k": "ne_regador", "xy": [720, 1010], "s": 0.78}], z=41,
          fluxos=[{"de": [575, 1050], "para": [440, 1200], "curva": 10, "cor": "#7fd3ff", "t": 0.3, "d": 1.9, "n": 6, "r": 12, "viagem": 0.6}])]
# S4 "Pro músculo, a água é o esforço." (a planta vira músculo; o regador vira haltere)
c += [*CARD(S4, S5 - S4 - 0.02, "PRO MÚSCULO, ÁGUA = ESFORÇO"),
      FIS(b(16) - 0.05, S5 - b(16) + 0.05, [{"k": "musculo", "xy": [PLX, PLY - 20], "s": 1.0, "rotulo": "MÚSCULO", "rot_y": 190}], z=42),
      FIS(b(21) - 0.08, S5 - b(21) + 0.08, [{"k": "ne_regador_haltere", "xy": [720, 1010], "s": 0.82}], z=43,
          pulsos=[{"o": 0, "t": 0.5}],
          fluxos=[{"de": [585, 1130], "para": [450, 1280], "curva": 10, "cor": "#7fd3ff", "t": 0.25, "d": 1.2, "n": 4, "r": 12, "viagem": 0.55}])]
# S5 "O treino de força dá o recado: fica mais forte." (a notificação traz o recado até a fibra)
c += [*CARD(S5, S6 - S5 - 0.02, "TREINO DE FORÇA DÁ O RECADO"),
      FIS(S5 + 0.1, S6 - S5 - 0.1, [{"k": "ne_fibra", "xy": [CX, 1300], "s": 1.3, "rotulo": "FIBRA DO MÚSCULO", "rot_y": 175, "t": 0.0}],
          pulsos=[{"o": 0, "t": round(b(29) - S5 + 0.5, 3)}, {"o": 0, "t": round(b(31) - S5 + 0.2, 3)}],
          fluxos=[{"de": [900, 840], "para": [760, 1230], "curva": -90, "cor": AMAR, "t": round(b(29) - S5, 3), "d": 1.3, "n": 4, "r": 15,
                   "viagem": 0.55, "rotulo": "RECADO"}]),
      *NOTIF(b(28) - 0.3, S6 - b(28) + 0.25, "Treino de força", "FICA MAIS FORTE!"),
      FIS(b(30), S6 - b(30), [{"k": "raio", "xy": [830, 1110], "s": 0.42}], z=44, pulsos=[{"o": 0, "t": 0.5}])]
# S6 "Com descanso e proteína, ele se refaz um pouco maior." (modo noite, tijolinhos entram, a fibra engrossa)
PROT = "#f0a640"
c += [FL(S6), CEL(S6, AF - S6, noite=True),
      *CARD(S6 + 0.05, b(39) - S6 - 0.4, "DESCANSO + PROTEÍNA", kicker="MODO NOITE · 23:40", kcor="#2a3a8a"),
      FIS(S6 + 0.2, AF - S6 - 0.2, [{"k": "cf_lua", "xy": [840, 990], "s": 0.3}], z=39),
      FIS(S6 + 0.05, b(38) - S6 + 0.25, [{"k": "ne_fibra", "xy": [CX, 1320], "s": 1.15, "t": 0.0}],
          fluxos=[{"de": [230, 1660], "para": [440, 1330], "curva": -80, "cor": PROT, "t": round(b(35) - S6 - 0.1, 3), "d": 1.4, "n": 4, "r": 16, "viagem": 0.6,
                   "rotulo": "PROTEÍNA"},
                  {"de": [850, 1660], "para": [640, 1330], "curva": -80, "cor": PROT, "t": round(b(35) - S6 + 0.1, 3), "d": 1.4, "n": 4, "r": 16, "viagem": 0.6}]),
      FIS(b(38) + 0.15, AF - b(38) - 0.15, [{"k": "ne_fibra_tijolos", "xy": [CX, 1320], "s": 1.22, "t": 0.0}], z=41, pulsos=[{"o": 0, "t": 0.5}]),
      *CARD(b(39) - 0.4, AF - b(39) + 0.38, "UM POUCO MAIOR", cor="#16803c", kicker="MODO NOITE · 23:40", kcor="#2a3a8a"),
      DS(b(40), AF - b(40), [{"k": "seta", "de": [890, 1640], "para": [890, 1470], "curva": 0}], cor=VERDE, lw=16, z=45)]
SFX_AULA = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "notif", "t": tB + 0.25, "gain": 0.3},
            {"src": "boing", "t": b(4), "gain": 0.25},
            {"src": "whoosh2", "t": S2, "gain": 0.3}, {"src": "scratch", "t": b(9), "gain": 0.2},
            {"src": "whoosh2", "t": S3, "gain": 0.3}, {"src": "boing", "t": b(12), "gain": 0.25},
            {"src": "whoosh2", "t": S4, "gain": 0.3}, {"src": "boing", "t": b(16), "gain": 0.22}, {"src": "boom", "t": b(21), "gain": 0.38, "pico": 0.3, "d": 1.0},
            {"src": "whoosh2", "t": S5, "gain": 0.3}, {"src": "notif", "t": b(28) - 0.3, "gain": 0.45}, {"src": "riser", "t": b(29) - 0.2, "gain": 0.16, "d": 1.0},
            {"src": "whoosh", "t": S6, "gain": 0.3, "pico": 0.45}, {"src": "papel", "t": b(35), "gain": 0.3}, {"src": "boing", "t": b(38) + 0.15, "gain": 0.25}]

# ================= C (neutro): o estudo de 1990 no celular =================
E2, E4, E5, E6 = round(e(3) - 0.2, 3), round(e(24) - 0.2, 3), round(e(28) - 0.15, 3), round(e(34) - 0.2, 3)
FONTE1 = "Fiatarone e col., JAMA 1990 · 10 idosos, estudo pequeno e sem grupo de comparação · doi 10.1001/jama.1990.03440220053029"
N3 = round(min(e(25), E5 - 2.15), 3)        # "QUASE 3x" (com tempo de leitura até o fim da frase)
c += [GL(AF), FL(AF), CEL(AF, tO - AF + 0.02, entra="nada"),
      SELO(AF + 0.2, tO - AF - 0.25, "● CHECAGEM · O QUE A CIÊNCIA DIZ"),
      FN(E2, tO - E2, FONTE1),
      # E1 "Olha que coisa." -> a notificação do arquivo fica até o resultado
      *NOTIF(AF + 0.1, E4 - AF - 0.12, "Arquivo", "ARQUIVO DE 1990", cor="#b3121f", y=300),
      # E2/E3 "Em 1990, em Boston, a médica Maria Fiatarone pôs 10 idosos de 90 anos pra treinar a perna por 8 semanas."
      {"tipo": "artigo", "t": E2, "d": round(E4 - E2 - 0.02, 3), "box": [150, 500, 780, 790], "z": 36, "fixo": True,
       "revista": "JAMA · Boston · 1990", "titulo": "Treino de força pesado aos 90 anos", "autores": "Fiatarone e col. · casa de repouso", "rola": 0,
       "linhas": [{"txt": "10 idosos frágeis.", "grifo": e(12)}, {"txt": "Média de 90 anos.", "grifo": e(15)},
                  {"txt": "8 semanas de treino de perna.", "grifo": e(22)}],
       "rodape": "doi 10.1001/jama.1990.03440220053029"},
      PIL(e(15) - 0.05, E4 - e(15) + 0.03, "90 ANOS", 300, 1330, w=480, tam=110, cor=AMAR),
      PIL(e(22) - 0.25, E4 - e(22) + 0.23, "8 SEMANAS", 270, 1490, w=540, tam=104, cor=BR),
      # E4 "A força quase triplicou,"
      FL(E4),
      *CARD(E4 + 0.02, E5 - E4 - 0.04, "FORÇA DA PERNA", kicker="RESULTADO · 8 SEMANAS"),
      {"tipo": "numero", "t": N3, "d": round(E5 - N3 + 0.03, 3), "xy": [0, 720], "valor": 3, "pre": "QUASE ", "suf": "x",
       "tam": 250, "cor": AMAR, "sombra": "#5a0d10", "rotulo": "+174%", "z": 46, "fixo": True, "conta": 0.6, "de": 1},
      FIS(E4 + 0.1, E5 - E4 - 0.1, [{"k": "haltere", "xy": [CX, 1340], "s": 0.6}], z=40, pulsos=[{"o": 0, "t": 0.9}]),
      # E5 "e o músculo da coxa cresceu."
      FL(E5),
      *CARD(E5 + 0.02, E6 - E5 - 0.04, "MÚSCULO DA COXA CRESCEU", cor="#16803c", kicker="RESULTADO · 8 SEMANAS"),
      FIS(E5 + 0.1, round(e(33) - E5 + 0.05, 3), [{"k": "musculo", "xy": [CX, 1230], "s": 0.95}], z=40),
      FIS(e(33) + 0.05, E6 - e(33) - 0.05, [{"k": "musculo", "xy": [CX, 1230], "s": 1.12}], z=40, pulsos=[{"o": 0, "t": 0.45}]),
      DS(e(33) + 0.1, E6 - e(33) - 0.15, [{"k": "seta", "de": [870, 1520], "para": [870, 1320], "curva": 0}], cor=VERDE, lw=16, z=45),
      # E6 "Num teste de caminhada, ficaram quase 50% mais rápidos."
      FL(E6),
      *CARD(E6 + 0.02, tO - E6 - 0.04, "NUM TESTE DE CAMINHADA", kicker="RESULTADO · 8 SEMANAS"),
      {"tipo": "numero", "t": round(e(39) - 0.05, 3), "d": round(tO - e(39) + 0.03, 3), "xy": [0, 830], "valor": 48, "pre": "+", "suf": "%",
       "tam": 250, "cor": VERDE, "sombra": "#0b3d22", "rotulo": "mais rápidos", "z": 46, "fixo": True, "conta": 0.7, "de": 0},
      FIS(E6 + 0.1, tO - E6 - 0.1, [{"k": "cy_relogio", "xy": [CX, 1440], "s": 0.7}], z=40)]
SFX_EST = [{"src": "whoosh", "t": AF + 0.05, "gain": 0.35, "pico": 0.45}, {"src": "notif", "t": AF + 0.12, "gain": 0.4},
           {"src": "pagina", "t": E2 + 0.05, "gain": 0.45}, {"src": "boing", "t": e(15), "gain": 0.25}, {"src": "boing", "t": e(22) - 0.2, "gain": 0.25},
           {"src": "whoosh2", "t": E4, "gain": 0.3}, {"src": "riser", "t": N3 - 0.9, "gain": 0.16, "d": 1.0}, {"src": "boom", "t": N3, "gain": 0.45, "pico": 0.3, "d": 1.2},
           {"src": "whoosh2", "t": E5, "gain": 0.3}, {"src": "boing", "t": e(33) + 0.05, "gain": 0.25},
           {"src": "whoosh2", "t": E6, "gain": 0.3}, {"src": "boom", "t": e(39), "gain": 0.4, "pico": 0.3, "d": 1.2}]

# ================= O (manso): o que fazer (com ou sem caneta, sem indicar nem contraindicar) =================
O2, O3 = round(o(6) - 0.15, 3), round(o(12) - 0.2, 3)
YP = CY0 + max(alt("EMAGRECEU MUITO?"), alt("GANHAR PESO COM SAÚDE?")) + 34
c += [GL(tO), FL(tO), CEL(tO, tE - tO + 0.02, entra="nada"),
      SELO(tO + 0.2, tE - tO - 0.25, "● O QUE FAZER", cor=VERDE, cor_txt="#06220f"),
      *CARD(tO + 0.05, O2 - tO - 0.07, "EMAGRECEU MUITO?"),
      PIL(o(2) - 0.05, O3 - o(2) + 0.03, "COM OU SEM CANETA", 120, YP, w=840, tam=100, cor=AMAR),
      *CARD(O2, O3 - O2 - 0.02, "GANHAR PESO COM SAÚDE?"),
      FIS(O2 + 0.1, O3 - O2 - 0.1, [{"k": "ne_planta_em_pe", "xy": [CX, 1400], "s": 1.0}]),
      FL(O3),
      {"tipo": "checklist", "t": O3, "d": round(tE - O3 - 0.02, 3), "box": [150, 500, 780, 520], "z": 36, "fixo": True, "entra": "desliza",
       "titulo": "Com seu médico:", "itens": [{"t": o(18), "txt": "músculo", "marca": round(o(18) + 0.35, 3)},
                                              {"t": o(19), "txt": "treino de força", "marca": o(21)}, {"t": o(22), "txt": "proteína", "marca": o(23)}]},
      FIS(o(18), tE - o(18), [{"k": "musculo", "xy": [CX, 1330], "s": 0.7}], z=40, pulsos=[{"o": 0, "t": 0.6}])]
SFX_O = [{"src": "whoosh", "t": tO + 0.05, "gain": 0.35, "pico": 0.45}, {"src": "notif", "t": tO + 0.15, "gain": 0.3},
         {"src": "boing", "t": o(2), "gain": 0.22}, {"src": "whoosh2", "t": O2, "gain": 0.3},
         {"src": "papel", "t": O3 + 0.05, "gain": 0.4}, {"src": "notif", "t": o(18) + 0.35, "gain": 0.25},
         {"src": "notif", "t": o(21), "gain": 0.25}, {"src": "notif", "t": o(23), "gain": 0.25}]

# ================= E (alegre): cobrança com o botão SEGUIR =================
E_2, E_3 = round(q(6) - 0.15, 3), round(q(11) + 0.15, 3)
K1, K2 = "SE AOS 90 O MÚSCULO ESCUTA...", "...O SEU DEDÃO TAMBÉM ESCUTA"
Y2 = CY0 + alt(K1) + 24
YB = Y2 + alt(K2) + 40
BOT = "border-radius:30px;padding:16px 0 24px;box-shadow:0 12px 26px rgba(0,0,0,.3)"
c += [GL(tE), FL(tE), CEL(tE, c1 - tE + 0.02, entra="nada"),
      *CARD(tE + 0.05, c1 - tE - 0.03, K1),
      *CARD(E_2, c1 - E_2 + 0.02, K2, y=Y2, cor="#b3121f", kicker="PLANTÃO DO CORPO · URGENTE"),
      {"tipo": "texto", "t": E_2 + 0.2, "d": round(E_3 - E_2 - 0.2, 3), "xy": [270, YB], "w": 540, "fonte": "900 84px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": "SEGUIR", "z": 40, "entra": "pop", "fixo": True, "css": "background:#1f6fe5;" + BOT},
      {"tipo": "texto", "t": E_3, "d": round(c1 - E_3 + 0.02, 3), "xy": [210, YB], "w": 660, "fonte": "900 84px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": "SEGUINDO", "z": 40, "entra": "pop", "fixo": True, "css": "background:#16a34a;" + BOT},
      DS(q(11), round(E_3 - q(11) + 0.4, 3), [{"k": "circulo", "c": [540, YB + 66], "r": [330, 100]}], cor=AMAR, lw=12, z=45),
      DS(E_3 + 0.15, round(c1 - E_3 - 0.13, 3), [{"k": "check", "c": [540, YB + 220], "s": 46}], cor=VERDE, lw=20, z=45)]
SFX_E = [{"src": "whoosh", "t": tE + 0.05, "gain": 0.35, "pico": 0.45}, {"src": "boing", "t": E_2 + 0.2, "gain": 0.28},
         {"src": "notif", "t": E_3, "gain": 0.45}]
print("alturas: O pílula y", YP, "| E cartão2 y", Y2, "botão y", YB, "check y", YB + 220, "| linhas K1", nlin(K1, 104, CW - 60), "K2", nlin(K2, 104, CW - 60))

# ================= CTA (banco cta6) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "SEGUE + CURTE = TREINO DO DEDÃO", "cor": "#ffd400", "cor_txt": "#1a0508"}]

# ================= D (neutro): fecho + carimbo =================
D2 = round(f(5) - 0.2, 3)
FONTE2 = "Fiatarone e col., JAMA 1990 · Peterson e col., Med Sci Sports Exerc 2011: 49 estudos, +1,1 kg de massa magra com treino de força depois dos 50 · Conteúdo educativo. Converse com o seu médico."
c += [GL(c2), FL(c2),
      GIG(c2, D2 - c2, "PESO", y=1300, tam=520, ida=False),
      TT(c2 + 0.03, D2 - c2 - 0.04, "PESO NEM SEMPRE ESCUTA.", y=330, fz=120),
      FIS(tD + 0.05, D2 - tD - 0.05, [{"k": "balanca", "xy": [540, 960], "s": 0.95, "t": 0.1}]),
      FL(D2),
      GIG(D2, dur - D2, "TREINO", y=1320, tam=480, cont=True, cor="rgba(61,220,132,.35)"),
      TT(D2 + 0.02, dur - D2 - 0.02, "O MÚSCULO ESCUTA O TREINO.", y=330, fz=120, cor=VERDE),
      FIS(D2 + 0.05, dur - D2 - 0.05, [{"k": "musculo", "xy": [540, 860], "s": 1.0, "t": 0.1}, {"k": "haltere", "xy": [540, 1120], "s": 0.55, "t": round(f(7) - D2, 3)}],
          pulsos=[{"o": 0, "t": round(f(7) - D2 + 0.3, 3)}]),
      {"tipo": "carimbo", "t": round(f(9) + 0.1, 3), "d": round(dur - f(9) - 0.1, 3), "xy": [190, 1360], "txt": "MEIA VERDADE", "tam": 110, "rot": -6,
       "z": 60, "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92)", "fixo": True},
      FN(c2, dur - c2, FONTE2)]

voz = [{"src": M + "ne_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "ne_viral.words.json", "gain": 0.16},
       {"src": M + "ne_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "ne_rosto.mp4", "t": vd, "ms": 0, "d": R1D, "palavras": M + "ne_rosto.words.json"},
       {"src": M + "ne_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "ne_a_voz.words.json"},
       {"src": M + "ne_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "ne_b_voz.words.json"},
       {"src": M + "ne_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "ne_c_voz.words.json"},
       {"src": M + "ne_o_voz.wav", "t": tO, "ms": 0, "d": DO, "palavras": M + "ne_o_voz.words.json"},
       {"src": M + "ne_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "ne_e_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "ne_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "ne_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "whoosh2", "t": vd + 0.05, "gain": 0.35}, {"src": "boing", "t": vd + 1.45, "gain": 0.25},
       *SFX_A, {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, *SFX_EST,
       {"src": "glitch", "t": tO - 0.05, "gain": 0.45}, *SFX_O,
       {"src": "glitch", "t": tE - 0.05, "gain": 0.45}, *SFX_E,
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
       {"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": D2, "gain": 0.3},
       {"src": "boom", "t": f(9) + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.5}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar(PID, dur, 1114, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, c1, 1730], [c1, c2, 1640], [c2, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json'))
# trilha contínua por baixo de toda a narração (nenhuma pausa muda); emendas cruzadas
p['audio']['musica'] = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.2, "fade": 0.6},
                        {"src": "m_investiga", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tO - tB + 0.8, 2), "gain": 0.16, "fade": 0.6},
                        {"src": "m_emocao", "t": round(tO - 0.4, 2), "ms": 0, "d": round(dur - tO + 0.4, 2), "gain": 0.15, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "AF", AF, "tO", tO, "tE", tE, "c1", c1, "c2", c2, "tD", tD, "| aula", round(AF - tB, 2), "s")
