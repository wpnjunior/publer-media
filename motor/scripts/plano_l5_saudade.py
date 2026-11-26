# plano_l5_saudade.py (14-15/11, lote 5, TDAH Adulto Real): "quem tem TDAH não sente saudade? fora da vista, fora da cabeça"
# (ex-participante de reality, TikTok @yuseffarahch, em espanhol). Veredito MITO (esquecer de dar notícia não é deixar de sentir).
# Trecho em 2 pedaços conferidos pelo volume e pela transcrição (faster-whisper medium, tmp_sd/):
#   A 0,00-3,20 "¿Por qué los TDAHchosos no extrañan a otras personas?"
#   B 7,84-15,86 "si no estás a la vista, literalmente estás fuera de nuestra cholla. Así de simple, es algo que los expertos
#     llaman permanencia de objetos." (o "TDAH" de "para nosotros con TDAH" acaba em 7,76; o "Si" seguinte começa em 15,96)
#   Fora: "para nós com TDAH", o "superpoder" de esquecer ex e a venda do fim. Nome dele fora da fala e da tela (só o @).
#   A faixa do post (bass house, 125 bpm) toca baixinho por baixo do pedaço B: tirada com passa-alta de 200 Hz no
#   sd_viral.mp4 (graves a -77 dB nos intervalos) + viral a 0,16 por baixo da dublagem Murilo (tmp_sd/dub.py).
# Rostos SEM crédito novo: entrada rk_ent (6cd9, "Olha só essa notícia", banco), r1 = pv_r1 (6cd9, "Mito, tá? E são dois
#   de uma vez.", feito no protetor do Papo; nunca usado no TDAH), CTA cta6 (banco).
# Voz: 4 blocos HeyGen por clima, SEM <break> e sem atempo; pausas de 0,7-0,8 s abertas na edição (tmp_sd/voz.py):
#   i indignado (abertura), b manso (aula) + f manso (o que fazer), c neutro (estudo) + d neutro (fecho), e alegre (cobrança).
# AULA em CELULAR COM CONVERSA (contato "Amor", "visto por último ontem"): vídeo do cadê-achou (bebê, pano, patinho e o
#   balão de pensamento), mensagem fixada "permanência do objeto", cérebro de perfil com a frente acesa que apaga,
#   notificação de lembrete, bilhete que cai da geladeira e o coração com "digitando...". Estudo no mesmo celular:
#   cartão UFMG 306 adultos e duas barras proporcionais 94,5 x 83,3 (Shaw 2014 só na tela).
# Pele DOSSIÊ (TDAH recentes: umemquatro e meninas = notícia, Cury = lab), legenda de máquina.
# Depois deste script (o próprio script roda):
#   python3 scripts/entrada.py react_l5_saudade assets/midia/sd_ent.mp4 assets/midia/sd_ent.mp4.words.json 2.07 \
#     'TDAH NÃO SENTE SAUDADE?' 'ex-participante de reality afirmou nas redes' && python3 scripts/pele.py react_l5_saudade dossie
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l5_saudade'; P = 'sd'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}sd_{k}_voz.words.json'))
WI, WB, WC, WF, WE, WD = W('i'), W('b'), W('c'), W('f'), W('e'), W('d')
DI, DB, DC, DF, DE, DD = [round(dur_de(f'{M}sd_{k}_voz.wav'), 3) for k in 'ibcfed']
vd = 11.22                               # A (3,20) + B (8,02)
VA = 3.20                                # emenda A|B
R1D = 3.46                               # sd_r1: "vez." termina em 2,96 s; arquivo 3,40 s (+0,06 dentro da trava)
CTA_D = 4.12
r1 = round(vd + R1D, 2)
tI = round(r1 + 0.15, 3)
tB = round(tI + DI + 0.45, 3)
tC = round(tB + DB + 0.8, 3)            # respiro depois da aula
tF = round(tC + DC + 0.8, 3)
tE = round(tF + DF + 0.5, 3)
c1 = round(tE + DE + 0.1, 3)
c2 = round(c1 + CTA_D, 3)
tD = round(c2 + 0.15, 3)
dur = round(tD + DD + 1.15, 2)
i_ = lambda k: round(tI + WI[k]['s'], 3); b_ = lambda k: round(tB + WB[k]['s'], 3); e_ = lambda k: round(tC + WC[k]['s'], 3)
f_ = lambda k: round(tF + WF[k]['s'], 3); q_ = lambda k: round(tE + WE[k]['s'], 3); d_ = lambda k: round(tD + WD[k]['s'], 3)
IF, AF, CF, FF, EF = round(tB - 0.05, 3), round(tC - 0.05, 3), round(tF - 0.1, 3), round(tE - 0.1, 3), c1
TINTA, VERM, VERDE, CINZA, CREME = "#1c1a17", "#b3121f", "#1d7a3e", "#9aa3ad", "#f6efdc"
SP = "text-shadow:5px 5px 0 rgba(0,0,0,.14)"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}

def TT(t0, t1, txt, y=240, fz=130, cor=TINTA, **k):
    """cartela Anton em tinta no papel; cabe em 1 linha (0,47 em por letra em 940 px) ou vai a 2 linhas"""
    if 0.47 * fz * len(txt) > 940:
        um = int(940 / (0.47 * len(txt)))
        if um >= 96: fz = um
        else: fz = min(fz, 116); y = min(y, 210)
    return T(t0, round(t1 - t0, 3), txt, y=y, f=f"{fz}px Anton", cor=cor, css=SP, vel=0.09, **k)
def TX(t0, t1, txt, x, y, w, fonte="700 48px Montserrat", cor=TINTA, css="", z=40, entra="pop", alinha="left", **k):
    L = {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": w, "fonte": fonte, "cor": cor,
         "alinha": alinha, "txt": txt, "z": z, "entra": entra, "css": css}
    L.update(k); return L
def CAIXA(t0, t1, x, y, w, h, css, z=20, entra="pop", **k):
    return TX(t0, t1, " ", x, y, w, fonte="10px Montserrat", css=f"height:{h}px;{css}", z=z, entra=entra, **k)
def GIG(t0, t1, txt, y=1300, tam=420, cor="rgba(179,18,31,.10)", ida=True):
    return {"tipo": "gigante", "t": round(t0, 3), "d": round(t1 - t0, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
            "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
def FIS(t0, t1, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t0, 3), "d": round(t1 - t0, 3), "z": z, "orgaos": orgaos}; L.update(k); return L
def DS(t0, t1, formas, cor=VERM, lw=14, z=45, vel=0.45):
    return {"tipo": "desenho", "t": round(t0, 3), "d": round(t1 - t0, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel}
def CARD(t0, t1, txt, x, y, w, cor, rot=-3, tam=100, cor_txt=TINTA, z=36):
    """cartão colorido preso com fita (dossiê)"""
    return [TX(t0, t1, txt, x, y, w, fonte=f"{tam}px Anton", cor=cor_txt, alinha="center", z=z,
               css=f"background:{cor};padding:22px 18px 18px;border-radius:6px;box-shadow:0 14px 28px rgba(0,0,0,.30);transform:rotate({rot}deg);line-height:1.05"),
            CAIXA(t0 + 0.12, t1, x + w // 2 - 80, y - 26, 160, 52, f"background:rgba(244,232,196,.85);box-shadow:0 2px 5px rgba(0,0,0,.25);transform:rotate({-rot * 2 + 4}deg)", z=z + 1)]
def EMO(t0, t1, ch, x, y, tam=170, z=38):
    return TX(t0, t1, ch, x, y, tam + 60, fonte=f"{tam}px Montserrat", cor="#000", alinha="center", z=z, css="filter:drop-shadow(0 10px 12px rgba(0,0,0,.30))")
def SELO(t0, t1, txt):
    return TX(t0, t1, txt, 60, 128, 960, fonte="900 32px Montserrat", cor="#ffffff", alinha="center", z=69, entra="desliza",
              css="letter-spacing:3px;background:#b3121f;border-radius:14px;padding:12px 0")
def RODAPE(t0, t1, txt, y=1648):
    L = F(t0, round(t1 - t0, 3), txt); L["xy"] = [40, y]; L["z"] = 86; L["cor"] = TINTA; L["css"] = "text-shadow:0 1px 0 rgba(255,255,255,.6)"; return L
def NOTA(t0, t1, x, y, rot=-4, entra="pop", w=200, h=180, z=34, **k):
    """bilhete amarelo de geladeira, só desenhado (CSS, para poder cair com 'desliza'); o texto fica na notificação"""
    return CAIXA(t0, t1, x, y, w, h, f"background:repeating-linear-gradient(180deg,transparent 0 44px,rgba(90,70,20,.45) 44px 50px) content-box,#fff27a;"
                 f"padding:40px 26px 20px;border:4px solid #b8a52a;box-shadow:0 10px 16px rgba(0,0,0,.28);transform:rotate({rot}deg)",
                 z=z, entra=entra, **k)

# ---------- celular com conversa (aula + estudo) ----------
PX, PY, PW, PH = 150, 420, 780, 1180
SX, SY, SW, SH = 168, 438, 744, 1144     # tela
def FONTE_CEL(t0, t1, txt, y):
    """fonte do estudo em letra de rodapé, dentro da tela do celular (não encosta na borda)"""
    return TX(t0, t1, txt, SX + 24, y, SW - 48, fonte="600 24px Montserrat", cor="#5b6770", alinha="center", z=33, css="line-height:1.25")
def BOLHA(t0, t1, txt, y, lado="esq", w=640, tam=56, z=33, entra="desliza", **k):
    x = SX + 28 if lado == "esq" else SX + SW - 28 - w
    raio = "12px 40px 40px 40px" if lado == "esq" else "40px 12px 40px 40px"
    bg = "#ffffff" if lado == "esq" else "#d6efff"
    return TX(t0, t1, txt, x, y, w, fonte=f"700 {tam}px Montserrat", cor="#111", z=z, entra=entra, dy=90,
              css=f"background:{bg};border-radius:{raio};padding:28px 34px;box-shadow:0 6px 16px rgba(0,0,0,.16);line-height:1.15", **k)
def CELULAR(t0, t1):
    D = dict(entra="desliza", dy=1400)
    return [CAIXA(t0, t1, PX, PY, PW, PH, "border-radius:86px;background:#15171a;box-shadow:0 40px 80px rgba(0,0,0,.42),inset 0 0 0 5px #3a3d42", z=20, **D),
            CAIXA(t0, t1, SX, SY, SW, SH, "border-radius:68px;background:#ece5dc;background-image:radial-gradient(rgba(120,100,80,.12) 2px,transparent 2px);background-size:30px 30px", z=21, **D),
            CAIXA(t0, t1, SX, SY, SW, 170, "border-radius:68px 68px 0 0;background:#2d3e45", z=22, **D),
            CAIXA(t0, t1, 465, 452, 150, 36, "border-radius:18px;background:#000", z=24, **D),
            TX(t0, t1, "‹", SX + 22, SY + 52, 60, fonte="300 90px Montserrat", cor="#ffffff", z=23, **D),
            TX(t0, t1, "❤", SX + 86, SY + 66, 84, fonte="32px Montserrat", cor="#e8415a", alinha="center", z=23,
               css="height:84px;padding-top:22px;border-radius:50%;background:#ffd8e0", **D),
            TX(t0, t1, "Amor ❤", SX + 190, SY + 66, 400, fonte="800 32px Montserrat", cor="#ffffff", z=23, **D)]
def STATUS(t0, t1, txt, cor="#cfe3e8", entra="nada"):
    return TX(t0, t1, txt, SX + 190, SY + 112, 500, fonte="500 28px Montserrat", cor=cor, z=23, entra=entra)

# ================= abertura: viral em tela dividida + caixinha de pergunta =================
c = abertura(P, vd, "@yuseffarahch", "center 30%", "Mito ou verdade? 🧠", "Quem tem TDAH não sente saudade?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 1.3, "dec": 1, "suf": " MILHÃO", "tam": 130,
               "rotulo": "de views no TikTok"},
              {"tipo": "glitch", "t": VA - 0.04, "d": 0.18}, {"tipo": "flash", "t": VA, "d": 0.18, "max": 0.35}])
c += [TX(vd + 0.02, r1, "TDAH NÃO\\nSENTE SAUDADE?", 70, 190, 940, fonte="118px Anton", cor=TINTA, alinha="center", z=55,
         css="height:909px;background:#f6efdc;border:6px solid #8a7650;border-radius:14px;padding:70px 30px 0;line-height:1.1;" + SP),
      {"tipo": "carimbo", "t": round(vd + 0.12, 3), "d": round(r1 - vd - 0.12, 2), "xy": [300, 560], "txt": "MITO", "tam": 190, "rot": -8, "z": 60,
       "cor": VERM, "blend": "normal", "css": "background:rgba(255,255,255,.92)"},
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + "sd_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= I (indignado): não examinei ninguém / esquecer pode / dois mitos / aí não =================
Ia, I2, I3, I4 = round(i_(4) - 0.1, 3), round(i_(8) - 0.15, 3), round(i_(17) - 0.15, 3), round(i_(23) - 0.15, 3)
c += [GL(r1), FL(r1),
      # I1 não examinei ninguém, falo só da frase (cartão com a frase, circulado, lupa)
      TT(r1, I2, "NÃO EXAMINEI NINGUÉM. SÓ A FRASE.", y=230),
      *CARD(r1 + 0.2, I2, "A FRASE:\\nFORA DA VISTA,\\nFORA DA CABEÇA", 130, 700, 820, "#fff27a", rot=-3, tam=104),
      EMO(i_(3), I2, "🔍", 760, 1080, tam=170),
      DS(i_(7), I2, [{"k": "circulo", "c": [540, 890], "r": [470, 245]}], lw=12, vel=0.5),
      FL(I2),
      # I2 esquecer de dar notícia pode acontecer, sim
      GIG(I2, I3, "SAUDADE?", y=1330, tam=420),
      TT(I2, I3, "ESQUECER? PODE ACONTECER", y=250, cor=VERDE),
      BOLHA(i_(8) + 0.2, I3, "Esqueci de te responder 😅", 700, lado="dir", w=760, tam=80, z=36),
      TX(i_(10), I3, "visto por último: ontem", 300, 1000, 620, fonte="600 32px Montserrat", cor="#6b6250", alinha="right", z=36, entra="desliza"),
      DS(i_(16), I3, [{"k": "check", "c": [540, 1200], "s": 90}], cor=VERDE, lw=26),
      FL(I3),
      # I3-I4 dois mitos
      TT(I3, IF, "SÃO DOIS MITOS", y=250, fz=150, cor=VERM),
      *CARD(I3 + 0.05, IF, "1. NÃO SENTE\\nSAUDADE?", 110, 560, 860, "#ffb3c7", rot=-2, tam=112),
      DS(i_(22) + 0.15, IF, [{"k": "x", "c": [540, 690], "s": 105}], lw=22),
      *CARD(I4 + 0.05, IF, "2. “PERMANÊNCIA\\nDO OBJETO”?", 110, 960, 860, "#fff27a", rot=2, tam=112),
      DS(i_(29) + 0.15, IF, [{"k": "x", "c": [540, 1095], "s": 105}], lw=22),
      {"tipo": "carimbo", "t": i_(30), "d": round(IF - i_(30), 3), "xy": [215, 1310], "txt": "AÍ NÃO", "tam": 170, "rot": -6, "z": 60,
       "cor": VERM, "blend": "normal", "css": "background:rgba(255,255,255,.93)"}]
SFX_I = [{"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": i_(0) + 0.15, "gain": 0.3},
         {"src": "scratch", "t": i_(2), "gain": 0.3}, {"src": "whoosh2", "t": Ia, "gain": 0.35}, {"src": "papel", "t": Ia + 0.05, "gain": 0.45},
         {"src": "boing", "t": i_(5), "gain": 0.25}, {"src": "scratch", "t": i_(7), "gain": 0.25},
         {"src": "whoosh2", "t": I2, "gain": 0.35}, {"src": "notif", "t": i_(8) + 0.2, "gain": 0.35}, {"src": "boing", "t": i_(16), "gain": 0.3},
         {"src": "whoosh", "t": I3, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": I3 + 0.05, "gain": 0.45}, {"src": "scratch", "t": i_(22) + 0.15, "gain": 0.3},
         {"src": "papel", "t": I4 + 0.05, "gain": 0.45}, {"src": "scratch", "t": i_(29) + 0.15, "gain": 0.3},
         {"src": "boom", "t": i_(30) + 0.02, "gain": 0.5, "pico": 0.3, "d": 1.4}]

# ================= B (manso): AULA no celular com conversa =================
B1b, B1c, B2, B2b, B3, B3b, B4 = [round(b_(k) - dt, 3) for k, dt in ((4, 0.1), (13, 0.1), (16, 0.15), (21, 0.15), (26, 0.15), (33, 0.15), (39, 0.15))]
c += [GL(tB), FL(tB), SELO(tB + 0.2, AF, "● AULA RÁPIDA · SEM DIAGNÓSTICO"), *CELULAR(tB, CF),
      STATUS(tB + 0.3, B4, "visto por último ontem", entra="pop")]
# cartelas (cada uma >= tempo de leitura)
for t0, t1, txt, cor in [(tB, B1b, "CADÊ? ACHOU!", TINTA), (B1b, B1c, "AINDA BEBÊ, JÁ SABE", TINTA), (B1c, B2, "CONTINUA LÁ!", VERDE),
                         (B2, B2b, "COISA DE BEBÊ", TINTA), (B2b, B3, "ADULTO TAMBÉM TEM", VERDE),
                         (B3, B3b, "LEMBRETE PODE FALHAR", VERM), (B3b, B4, "BILHETE QUE CAI", TINTA), (B4, AF, "O SENTIMENTO FICA", VERM)]:
    c.append(TT(t0 + 0.02, t1 - 0.03, txt, y=240, fz=140, cor=cor))
# B1: vídeo do cadê-achou chegando na conversa
c += [CAIXA(tB + 0.5, B2, SX + 28, 650, 600, 610, "border-radius:12px 36px 36px 36px;background:#fff;box-shadow:0 6px 18px rgba(0,0,0,.18)", z=30, entra="desliza", dy=120),
      CAIXA(tB + 0.5, B2, SX + 44, 666, 568, 530, "border-radius:24px;background:linear-gradient(180deg,#d8efff 0%,#fff6dc 100%)", z=31, entra="desliza", dy=120),
      TX(tB + 0.5, B2, "▶ 0:07", SX + 56, 1206, 300, fonte="700 32px Montserrat", cor="#5b6770", z=31, entra="desliza", dy=120),
      FIS(tB + 0.7, B2, [{"k": "sd_bebe", "xy": [350, 940], "s": 1.0, "t": 0.0}], z=32, pulsos=[{"o": 0, "t": round(WB[5]['s'] - 0.6, 2)}]),
      FIS(tB + 0.75, B2, [{"k": "sd_brinquedo", "xy": [640, 1050], "s": 0.62, "t": 0.0}], z=33,
          pulsos=[{"o": 0, "t": round(WB[3]['s'] + 0.1 - 0.75, 2)}, {"o": 0, "t": round(WB[12]['s'] - 0.75, 2)}]),
      FIS(tB + 0.75, b_(3), [{"k": "sd_pano", "xy": [640, 1040], "s": 0.70, "t": 0.0}], z=34),          # pano cobre ("cadê")
      TX(b_(3) + 0.05, b_(4) + 0.4, "ACHOU!", 460, 730, 330, fonte="110px Anton", cor=VERM, alinha="center", z=35, css=SP),
      FIS(b_(13), B2, [{"k": "sd_pano", "xy": [640, 1040], "s": 0.70, "t": 0.0}], z=34),                # escondido de novo
      FIS(b_(14), B2, [{"k": "sd_balao", "xy": [600, 790], "s": 0.6, "t": 0.0}], z=35, pulsos=[{"o": 0, "t": 0.7}]),
      FL(B2)]
# B2: mensagem fixada + bebê tem / adulto com TDAH também tem
c += [TX(B2 + 0.05, B3, "PERMANÊNCIA\\nDO OBJETO", SX, 608, SW, fonte="800 80px Montserrat", cor="#3a3220", alinha="center", z=32, entra="desliza", dy=-60,
         css="background:#fff8d6;border-bottom:4px solid #e2d29a;padding:22px 20px;line-height:1.08"),
      BOLHA(b_(16) + 0.1, B3, "👶 Bebê tem", 870, lado="esq", w=630, tam=80),
      DS(b_(20), B3, [{"k": "check", "c": [866, 935], "s": 42}], cor=VERDE, lw=20),
      BOLHA(b_(21) - 0.05, B3, "Adulto com TDAH também ✓✓", 1110, lado="dir", w=640, tam=80),
      FL(B3)]
# B3a: o lembrete pode falhar (frente do cérebro acende, pisca e apaga; notificação desce)
c += [FIS(B3, b_(32), [{"k": "cerebro_lado", "xy": [560, 1080], "s": 1.45, "t": 0.0}], z=33,
          pulsos=[{"o": 0, "t": round(b_(28) - B3, 2)}, {"o": 0, "t": round(b_(29) - B3, 2)}, {"o": 0, "t": round(b_(29) - B3 + 0.45, 2)}]),
      DS(b_(29) + 0.2, b_(32), [{"k": "seta", "de": [235, 760], "para": [345, 960], "curva": -30}], cor=VERM, lw=14),
      FIS(b_(32), B3b, [{"k": "sd_cerebro_off", "xy": [560, 1080], "s": 1.45, "t": 0.0}], z=33),
      TX(b_(29), b_(36), "🔔 Lembrete:\\ndar notícia", SX + 22, SY + 22, SW - 44, fonte="800 80px Montserrat", cor="#111", z=36, entra="desliza", dy=-300,
         css="background:rgba(250,250,250,.97);border-radius:34px;padding:22px 30px;box-shadow:0 10px 30px rgba(0,0,0,.35);line-height:1.08"),
      FL(B3b)]
# B3b: igual bilhete que cai da geladeira (o ímã fica, o bilhete cai)
c += [FIS(B3b, B4, [{"k": "sd_geladeira", "xy": [540, 1110], "s": 1.35, "t": 0.0}], z=32),
      NOTA(B3b + 0.15, b_(36), 440, 1110, rot=-4, z=34),
      FIS(B3b + 0.3, B4, [{"k": "sd_ima", "xy": [535, 1128], "s": 1.0, "t": 0.0}], z=35),
      NOTA(b_(36), B4, 470, 1380, rot=24, entra="desliza", dy=-270, z=34),
      FL(B4)]
# B4: o sentimento fica (coração aceso, "digitando...")
c += [STATUS(B4, AF, "digitando...", cor="#7cf0a8", entra="pop"),
      FIS(B4 + 0.05, AF, [{"k": "coracao_afeto", "xy": [540, 1030], "s": 1.3, "t": 0.0}], z=33,
          pulsos=[{"o": 0, "t": round(b_(40) - B4, 2)}, {"o": 0, "t": round(b_(41) - B4, 2)}, {"o": 0, "t": round(b_(41) - B4 + 0.9, 2)}]),
      TX(B4 + 0.3, AF, "● ● ●", SX + 28, 1330, 200, fonte="900 32px Montserrat", cor="#8a939c", alinha="center", z=33, entra="desliza", dy=90,
         css="background:#ffffff;border-radius:12px 40px 40px 40px;padding:30px 0;letter-spacing:6px;box-shadow:0 6px 16px rgba(0,0,0,.16)")]
SFX_B = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.45, "pico": 0.45}, {"src": "notif", "t": tB + 0.5, "gain": 0.4},
         {"src": "boing", "t": tB + 0.75, "gain": 0.25}, {"src": "whoosh2", "t": b_(3), "gain": 0.35}, {"src": "boing", "t": b_(3) + 0.05, "gain": 0.3},
         {"src": "papel", "t": b_(13), "gain": 0.4}, {"src": "boing", "t": b_(14), "gain": 0.28},
         {"src": "whoosh2", "t": B2, "gain": 0.35}, {"src": "notif", "t": b_(16) + 0.1, "gain": 0.3}, {"src": "notif", "t": b_(21), "gain": 0.3},
         {"src": "boing", "t": b_(23), "gain": 0.22},
         {"src": "whoosh2", "t": B3, "gain": 0.35}, {"src": "riser", "t": b_(28) - 0.3, "gain": 0.14, "d": 1.2}, {"src": "glitch", "t": b_(32) - 0.05, "gain": 0.2},
         {"src": "notif", "t": b_(32), "gain": 0.4},
         {"src": "whoosh2", "t": B3b, "gain": 0.35}, {"src": "papel", "t": B3b + 0.15, "gain": 0.4}, {"src": "whoosh", "t": b_(36), "gain": 0.35, "pico": 0.2},
         {"src": "boing", "t": b_(36) + 0.4, "gain": 0.3},
         {"src": "whoosh2", "t": B4, "gain": 0.3}, {"src": "teclado", "t": B4 + 0.3, "gain": 0.22, "d": 1.0}]

# ================= C (neutro): estudo no mesmo celular =================
C2, C3, C4 = round(e_(5) - 0.15, 3), round(e_(19) - 0.15, 3), round(e_(27) - 0.1, 3)
LB = 608                                     # largura da barra cheia (94,5); a de 83,3 é proporcional
L2 = round(LB * 83.27 / 94.51)
c += [GL(AF), FL(AF), SELO(tC + 0.2, CF, "● O QUE A PESQUISA ACHOU"), STATUS(AF, CF, "online", cor="#7cf0a8"),
      TT(tC + 0.02, C2 - 0.03, "UMA PESQUISA DE 2021", y=240),
      BOLHA(tC + 0.15, C2, "📄 Pesquisa\\nde 2021", 660, lado="esq", w=600, tam=80),
      FL(C2),
      # C2 UFMG, 306 adultos, sobre paixão
      TT(C2 + 0.02, e_(15) - 0.13, "PESQUISA DA UFMG", y=240),
      TT(e_(15) - 0.1, C3 - 0.03, "306 ADULTOS", y=240, fz=150, cor=VERM),
      CAIXA(C2, C3, SX + 28, 790, SW - 56, 640, "border-radius:30px;background:#fff;box-shadow:0 8px 22px rgba(0,0,0,.18)", z=31),
      TX(C2 + 0.05, C3, "UFMG", SX + 28, 812, SW - 56, fonte="900 90px Montserrat", cor=TINTA, alinha="center", z=32),
      {"tipo": "numero", "t": e_(15), "d": round(C3 - e_(15), 3), "xy": [SX + 28, 880], "w": SW - 56, "valor": 306, "tam": 230, "cor": VERM,
       "sombra": "#e9c3c3", "rotulo": "adultos responderam", "cor_rotulo": TINTA, "sombra_rotulo": "none", "z": 33},
      TX(e_(15) + 0.7, C3, "sobre PAIXÃO", SX + 40, 1302, SW - 80, fonte="800 80px Montserrat", cor="#ffffff", alinha="center", z=33,
         css="background:#b3121f;border-radius:44px;padding:14px 0"),
      EMO(C2 + 0.15, e_(15) - 0.05, "🏛️", 410, 950, tam=200, z=33),
      FONTE_CEL(C2, C3, "Soares e col., Front Psychiatry 2021 · UFMG · 306 adultos · questionário de sintomas, sem diagnóstico", 1462),
      FL(C3),
      # C3-C4 barras proporcionais (zero na base)
      TT(C3 + 0.02, C4 - 0.03, "MAIS PAIXÃO", y=240, fz=150, cor=VERM),
      TT(C4, CF, "94,5 × 83,3", y=240, fz=150, cor=TINTA),
      CAIXA(C3, CF, SX + 28, 640, SW - 56, 862, "border-radius:30px;background:#fff;box-shadow:0 8px 22px rgba(0,0,0,.18)", z=31),
      TX(C3 + 0.05, CF, "PONTOS DE PAIXÃO", SX + 28, 662, SW - 56, fonte="800 30px Montserrat", cor="#7a8288", alinha="center", z=32, css="letter-spacing:3px"),
      TX(e_(21) - 0.2, CF, "COM SINTOMAS\\nDE TDAH", 236, 700, 608, fonte="100px Anton", cor=TINTA, z=32, css="line-height:1.0"),
      CAIXA(e_(21) - 0.2, CF, 236, 912, LB, 112, "border-radius:18px;background:#e7e1d3", z=32),
      CAIXA(e_(28) - 0.05, CF, 236, 912, LB, 112, "border-radius:18px;background:#2fbf71", z=33, entra="mascara"),
      TX(e_(28) + 0.3, CF, "94,5", 236, 912, LB - 24, fonte="100px Anton", cor="#ffffff", alinha="right", z=34, css="line-height:1.12"),
      TX(e_(21) + 0.3, CF, "SEM SINTOMAS", 236, 1050, 608, fonte="100px Anton", cor=TINTA, z=32, css="line-height:1.0"),
      CAIXA(e_(21) + 0.3, CF, 236, 1162, LB, 112, "border-radius:18px;background:#e7e1d3", z=32),
      CAIXA(e_(31) - 0.05, CF, 236, 1162, L2, 112, "border-radius:18px;background:#8a939c", z=33, entra="mascara"),
      TX(e_(31) + 0.3, CF, "83,3", 236, 1162, L2 - 24, fonte="100px Anton", cor="#ffffff", alinha="right", z=34, css="line-height:1.12"),
      TX(C3 + 0.4, CF, "questionário,\\nsem diagnóstico", SX + 28, 1298, SW - 56, fonte="700 80px Montserrat", cor="#7a8288", alinha="center", z=32,
         css="line-height:1.05;letter-spacing:-1px"),
      FONTE_CEL(C3, CF, "Shaw 2014 (Am J Psychiatry): em clínica, 3 a 7 em cada 10 adultos com TDAH têm emoção forte demais", 1512)]
SFX_C = [{"src": "whoosh", "t": AF + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "notif", "t": tC + 0.15, "gain": 0.35},
         {"src": "whoosh2", "t": C2, "gain": 0.35}, {"src": "pagina", "t": C2 + 0.05, "gain": 0.4},
         {"src": "riser", "t": e_(15) - 1.0, "gain": 0.16, "d": 1.0}, {"src": "boom", "t": e_(15), "gain": 0.45, "pico": 0.3, "d": 1.3},
         {"src": "boing", "t": e_(18), "gain": 0.3},
         {"src": "whoosh2", "t": C3, "gain": 0.35}, {"src": "papel", "t": C3 + 0.05, "gain": 0.4},
         {"src": "riser", "t": e_(28) - 1.0, "gain": 0.16, "d": 1.0}, {"src": "boom", "t": e_(28) - 0.05, "gain": 0.45, "pico": 0.3, "d": 1.3},
         {"src": "boing", "t": e_(26), "gain": 0.22}, {"src": "boing", "t": e_(31) - 0.05, "gain": 0.3}]

# ================= F (manso): vídeo não fecha diagnóstico; pesando na relação, conversa com o médico =================
F1b, F2 = round(f_(6) - 0.1, 3), round(f_(9) - 0.15, 3)
c += [GL(CF + 0.1), FL(CF + 0.1),
      TT(tF + 0.02, F2, "VÍDEO NÃO FECHA DIAGNÓSTICO", y=230),
      EMO(tF + 0.1, F2, "📱", 395, 700, tam=230),
      DS(f_(5), F2, [{"k": "x", "c": [540, 840], "s": 125}], lw=24),
      {"tipo": "carimbo", "t": F1b, "d": round(F2 + 0.25 - F1b, 3), "xy": [330, 1140], "txt": "NEM O MEU", "tam": 110, "rot": -7, "z": 60,
       "cor": VERM, "blend": "normal", "css": "background:rgba(255,255,255,.93)"},
      FL(F2),
      TT(F2 + 0.02, FF, "PESANDO NA RELAÇÃO?", y=250),
      FIS(F2 + 0.05, FF, [{"k": "jp_pessoa", "xy": [370, 900], "s": 0.85, "t": 0.0}, {"k": "jp_pessoa", "xy": [710, 900], "s": 0.85, "t": 0.15},
                         {"k": "coracao_afeto", "xy": [540, 720], "s": 0.42, "t": 0.4}], z=30, pulsos=[{"o": 2, "t": 1.0}, {"o": 2, "t": 2.0}]),
      *CARD(f_(16) - 1.0, FF, "CONVERSA COM\\nO SEU MÉDICO", 110, 1180, 860, "#9be3a8", rot=-2, tam=110),
      EMO(f_(16) - 0.6, FF, "🩺", 760, 1470, tam=150, z=40)]
SFX_F = [{"src": "whoosh", "t": tF, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": tF + 0.15, "gain": 0.3}, {"src": "scratch", "t": f_(5), "gain": 0.3},
         {"src": "whoosh2", "t": F1b, "gain": 0.3}, {"src": "whoosh2", "t": F2, "gain": 0.35}, {"src": "boing", "t": F2 + 0.1, "gain": 0.2},
         {"src": "boing", "t": F2 + 0.25, "gain": 0.2}, {"src": "papel", "t": f_(16) - 1.0, "gain": 0.45}, {"src": "boing", "t": f_(16) - 0.6, "gain": 0.25}]

# ================= E (alegre): cobrança (o lembrete que não cai) =================
E2 = round(q_(3) - 0.15, 3)
c += [GL(FF + 0.1), FL(FF + 0.1),
      TT(tE + 0.02, tE + 1.87, "APERTA O SEGUIR", y=250, fz=150),
      TT(tE + 1.87, EF, "O LEMBRETE QUE NÃO CAI", y=210),
      TX(tE + 0.1, EF, "Seguir", 290, 520, 500, fonte="900 100px Montserrat", cor="#ffffff", alinha="center", z=44,
         css="background:#0095f6;border-radius:34px;padding:22px 0;box-shadow:0 16px 40px rgba(0,0,0,.30)"),
      EMO(tE + 0.3, E2 + 0.5, "👆", 650, 600, tam=150, z=45),
      FL(E2),
      FIS(E2, EF, [{"k": "sd_geladeira", "xy": [540, 1110], "s": 1.35, "t": 0.0}], z=32),
      NOTA(E2 + 0.15, EF, 395, 1030, rot=-3, w=300, h=250, z=34),
      TX(E2 + 0.25, EF, "seguir ✓", 395, 1135, 300, fonte="700 80px Caveat", cor="#3a3220", alinha="center", z=35, css="transform:rotate(-3deg)"),
      FIS(E2 + 0.3, EF, [{"k": "sd_ima", "xy": [545, 1048], "s": 1.0, "t": 0.0}], z=35, pulsos=[{"o": 0, "t": round(q_(10) - E2 - 0.3, 2)}]),
      DS(q_(11), EF, [{"k": "check", "c": [800, 1300], "s": 60}], cor=VERDE, lw=22)]
SFX_E = [{"src": "whoosh2", "t": tE, "gain": 0.35}, {"src": "notif", "t": tE + 0.15, "gain": 0.35}, {"src": "boing", "t": tE + 0.3, "gain": 0.3},
         {"src": "whoosh", "t": E2, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": E2 + 0.15, "gain": 0.4}, {"src": "boing", "t": q_(10), "gain": 0.3},
         {"src": "scratch", "t": q_(11), "gain": 0.22}]

# ================= CTA (banco cta6) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": CTA_D, "ms": 0, "src": M + "sd_cta.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 2.2, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": round(CTA_D - 0.25, 2), "y": 215, "txt": "TE AJUDOU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (neutro): fecho =================
D2 = round(d_(3) - 0.15, 3)
c += [GL(c2), FL(c2),
      TT(c2 + 0.03, D2, "A MENSAGEM ATRASA", y=260),
      TX(c2 + 0.15, D2 + 0.4, "3 dias depois", 110, 770, 760, fonte="700 32px Montserrat", cor="#6b6250", z=40, entra="desliza"),
      TX(c2 + 0.15, D2 + 0.4, "Foi mal a demora!", 110, 830, 860, fonte="700 80px Montserrat", cor="#111", z=40, entra="desliza", dy=90,
         css="background:#ffffff;border-radius:12px 44px 44px 44px;padding:30px 36px;box-shadow:0 10px 26px rgba(0,0,0,.2)"),
      FL(D2),
      GIG(D2, dur, "O SENTIMENTO FICA", y=1330, tam=400),
      TT(D2 + 0.02, dur, "O SENTIMENTO FICA", y=260, cor=VERM),
      {"tipo": "carimbo", "t": round(D2 + 0.35, 3), "d": round(dur - D2 - 0.35, 3), "xy": [300, 560], "txt": "MITO", "tam": 170, "rot": -6, "z": 60,
       "cor": VERM, "blend": "normal", "css": "background:rgba(255,255,255,.93)"},
      TX(D2 + 0.4, dur, "ESQUECER\\nNÃO É NÃO SENTIR", 90, 960, 900, fonte="110px Anton", cor=TINTA, alinha="center", z=45,
         css="background:#ffffff;border-radius:26px;padding:20px 0;box-shadow:0 14px 30px rgba(0,0,0,.25);line-height:1.05"),
      RODAPE(c2, dur, "Soares 2021 doi 10.3389/fpsyt.2021.593150 · Shaw 2014 doi 10.1176/appi.ajp.2013.13070966 · Conteúdo educativo", y=1600)]
SFX_D = [{"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": c2 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "notif", "t": c2 + 0.3, "gain": 0.35},
         {"src": "whoosh2", "t": D2, "gain": 0.35}, {"src": "boom", "t": D2 + 0.35, "gain": 0.5, "pico": 0.3, "d": 1.5}, {"src": "boing", "t": D2 + 0.4, "gain": 0.3}]

voz = [{"src": M + "sd_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "sd_viral.words.json", "gain": 0.16},
       {"src": M + "sd_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "sd_r1.mp4", "t": vd, "ms": 0, "d": 3.40, "palavras": M + "sd_r1.words.json"},
       {"src": M + "sd_i_voz.wav", "t": tI, "ms": 0, "d": DI, "palavras": M + "sd_i_voz.words.json"},
       {"src": M + "sd_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "sd_b_voz.words.json"},
       {"src": M + "sd_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "sd_c_voz.words.json"},
       {"src": M + "sd_f_voz.wav", "t": tF, "ms": 0, "d": DF, "palavras": M + "sd_f_voz.words.json"},
       {"src": M + "sd_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "sd_e_voz.words.json"},
       {"src": M + "sd_cta.mp4", "t": c1, "ms": 0, "d": CTA_D, "palavras": M + "sd_cta.words.json"},
       {"src": M + "sd_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "sd_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "glitch", "t": VA - 0.06, "gain": 0.28}, {"src": "boing", "t": 3.6, "gain": 0.3}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.15, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, *SFX_I,
       {"src": "glitch", "t": tB - 0.05, "gain": 0.4}, *SFX_B,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.4}, *SFX_C,
       {"src": "glitch", "t": CF + 0.05, "gain": 0.4}, *SFX_F,
       {"src": "glitch", "t": FF + 0.05, "gain": 0.4}, *SFX_E,
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, *SFX_D]
for L in c:
    if vd <= L.get("t", 0) < dur: L["fixo"] = True
salvar(PID, dur, 515, c, voz, sfx, {"r1_fim": r1, "esconde": [],
                                    "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 950], [r1, tB, 1700], [tB, CF, 1712], [CF, dur, 1700]]})
p = json.load(open(f'planos/{PID}.json'))
# trilha contínua por baixo de tudo depois do viral (nenhuma pausa muda); uma faixa por bloco, emenda cruzada
p['audio']['musica'] = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.2, "fade": 0.6},
                        {"src": "m_emocao", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tC - tB + 0.8, 2), "gain": 0.17, "fade": 0.6},
                        {"src": "m_investiga", "t": round(tC - 0.4, 2), "ms": 0, "d": round(tF - tC + 0.8, 2), "gain": 0.2, "fade": 0.6},
                        {"src": "m_viagem", "t": round(tF - 0.4, 2), "ms": 0, "d": round(tE - tF + 0.8, 2), "gain": 0.16, "fade": 0.6},
                        {"src": "m_humor", "t": round(tE - 0.4, 2), "ms": 0, "d": round(c2 - tE + 0.7, 2), "gain": 0.16, "fade": 0.6},
                        {"src": "m_emocao", "t": round(c2 - 0.3, 2), "ms": 22, "d": round(dur - c2 + 0.3, 2), "gain": 0.18, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tI", tI, "tB", tB, "tC", tC, "tF", tF, "tE", tE, "c1", c1, "c2", c2, "tD", tD)
if '--sem-pos' not in sys.argv:
    subprocess.run(["python3", "scripts/entrada.py", PID, M + "sd_ent.mp4", M + "sd_ent.mp4.words.json", "2.07",
                    "TDAH NÃO SENTE SAUDADE?", "ex-participante de reality afirmou nas redes"], check=True)
    subprocess.run(["python3", "scripts/pele.py", PID, "dossie"], check=True)
