# plano_l6_pilula.py (15/11, lote 6, Fertilidade a Dois): "anos de pílula deixam infértil?"
# Viral: The Diary Of A CEO (TikTok @steven, 04/06/2024, 2,8 mi), inglês, dublado pela Murilo (original a 0,16 por baixo).
#   Convidada médica de fertilidade: nome FORA da fala e da tela (crédito só o @ do canal). Trecho em 3 pedaços (10,52 s):
#   A 0,00-1,40 "Is the pill healthy?" (apresentador) | B 47,56-52,16 "The birth control pill itself does not cause infertility.
#   It changes nothing about the vault." | C 62,32-66,84 "So it's not impacting the quality or the quantity of the eggs that you have."
#   Recorte só da parte de cima (crop 540x522 do 576x1024): a legenda queimada em inglês (y >= 553) e a caixa do título ficam fora.
#   Veredito: ela acerta -> caixinha "Anos de pílula deixam infértil?" = MITO. Respondemos só ao que ela disse no corte.
# Rostos SEM crédito novo: entrada rk_ent (banco), r1 = mx_r1 (6cd9, "Nisso ela tem razão. E tem número.", feito no
#   react_l4_magro da Caneta; nunca usado na Fertilidade), virada jp_rosto (banco, "Sou médico. E quero muito que você saiba.";
#   usado só no Papo), CTA cta6 (banco).
# Voz: 4 áudios HeyGen por clima, sem <break> e sem atempo; pausas de 0,8-0,85 s abertas na edição (tmp_pc/voz.py):
#   i indignado (abertura) | b manso (aula) + f manso (o que fazer) | c neutro (estudo) + d neutro (fecho) | e alegre (cobrança).
# AULA em CELULAR COM GRUPO "Ciclo do mês" (Cérebro, Ovário com o cofre na foto, e a Pílula que entra e sai do grupo):
#   cofre aberto com óvulos -> cérebro manda o recado (partículas) e um óvulo sai -> a cartela avisa "já tem hormônio" ->
#   cérebro silenciado, cofre fechado, nenhum sai -> Pílula sai do grupo, o recado volta. Desenhos novos fisio_extra/pc_*.svg.
# ESTUDO fora do celular, em cartão de notícia: QUASE 18 MIL mulheres (Boston, 2020) -> ~3 CICLOS (3 calendários) ->
#   duas barras iguais "anos de uso não mudaram a chance". Yland 2020 BMJ doi 10.1136/bmj.m3966.
# Pele NOTÍCIA (vinho; Fertilidade recentes: suplemento dossiê, corrida papel antigo). Camadas depois do viral são "fixo".
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l6_pilula'; P = 'pc'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}pc_{k}_voz.words.json'))
WI, WB, WC, WF, WE, WD = W('i'), W('b'), W('c'), W('f'), W('e'), W('d')
DI, DB, DC, DF, DE, DD = [round(dur_de(f'{M}pc_{k}_voz.wav'), 3) for k in 'ibcfed']
vd = 10.52                               # A 1,40 + B 4,60 + C 4,52
VA, VB = 1.40, 6.00                      # emendas
R1D = 2.82                               # pc_r1: "número." termina em 2,32; arquivo 2,76 (+0,06 dentro da trava)
VD = 3.33                                # pc_vir: "saiba." termina em 2,83
CTA_D = 4.12
r1 = round(vd + R1D, 2)
tI = round(r1 + 0.15, 3)
tV = round(tI + DI + 0.5, 3)
tB = round(tV + VD + 0.35, 3)
tC = round(tB + DB + 1.1, 3)            # respiro depois da aula
tE = round(tC + DC + 1.0, 3)            # cobrança logo depois da entrega (estudo)
tF = round(tE + DE + 0.8, 3)
c1 = round(tF + DF + 0.3, 3)
c2 = round(c1 + CTA_D, 3)
tD = round(c2 + 0.15, 3)
dur = round(tD + DD + 1.9, 2)
i_ = lambda k: round(tI + WI[k]['s'], 3); b_ = lambda k: round(tB + WB[k]['s'], 3); e_ = lambda k: round(tC + WC[k]['s'], 3)
f_ = lambda k: round(tF + WF[k]['s'], 3); q_ = lambda k: round(tE + WE[k]['s'], 3); d_ = lambda k: round(tD + WD[k]['s'], 3)
IF, VF, AF, CF, EF, FF = round(tV - 0.05, 3), round(tB - 0.05, 3), round(tC - 0.1, 3), round(tE - 0.3, 3), round(tF - 0.35, 3), c1
BR, AMAR, VERM, VERDE, CINZA, VINHO = "#ffffff", "#ffd400", "#ff2d3d", "#3ddc84", "#9aa3ad", "#5a0d10"
SP = "text-shadow:0 6px 0 rgba(0,0,0,.35),0 10px 26px rgba(0,0,0,.45)"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}

def TT(t0, t1, txt, y=240, fz=130, cor=BR, **k):
    """cartela Anton branca com sombra; cabe em 1 linha (0,47 em por letra em 940 px) ou vai a 2 linhas"""
    if 0.47 * fz * len(txt) > 940:
        um = int(940 / (0.47 * len(txt)))
        if um >= 100: fz = um
        else: fz = min(fz, 116); y = min(y, 210)
    return T(t0, round(t1 - t0, 3), txt, y=y, f=f"{fz}px Anton", cor=cor, css=SP, vel=0.09, **k)
def TX(t0, t1, txt, x, y, w, fonte="700 80px Montserrat", cor=BR, css="", z=40, entra="pop", alinha="left", **k):
    L = {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": w, "fonte": fonte, "cor": cor,
         "alinha": alinha, "txt": txt, "z": z, "entra": entra, "css": css}
    L.update(k); return L
def CAIXA(t0, t1, x, y, w, h, css, z=20, entra="pop", **k):
    return TX(t0, t1, " ", x, y, w, fonte="10px Montserrat", css=f"height:{h}px;{css}", z=z, entra=entra, **k)
def GIG(t0, t1, txt, y=1300, tam=420, cor="rgba(255,212,0,.12)", ida=True):
    return {"tipo": "gigante", "t": round(t0, 3), "d": round(t1 - t0, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
            "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
def FIS(t0, t1, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t0, 3), "d": round(t1 - t0, 3), "z": z, "orgaos": orgaos}; L.update(k); return L
def DS(t0, t1, formas, cor=VERM, lw=14, z=45, vel=0.45):
    return {"tipo": "desenho", "t": round(t0, 3), "d": round(t1 - t0, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel}
def CARD(t0, t1, txt, x, y, w, cor, rot=-3, tam=100, cor_txt="#1c1a17", z=36):
    return TX(t0, t1, txt, x, y, w, fonte=f"{tam}px Anton", cor=cor_txt, alinha="center", z=z,
              css=f"background:{cor};padding:22px 18px 18px;border-radius:18px;box-shadow:0 14px 28px rgba(0,0,0,.40);transform:rotate({rot}deg);line-height:1.05")
def EMO(t0, t1, ch, x, y, tam=170, z=38):
    return TX(t0, t1, ch, x, y, tam + 60, fonte=f"{tam}px Montserrat", cor="#000", alinha="center", z=z, css="filter:drop-shadow(0 10px 12px rgba(0,0,0,.40))")
def SELO(t0, t1, txt):
    return TX(t0, t1, txt, 60, 128, 960, fonte="900 32px Montserrat", cor="#ffffff", alinha="center", z=69, entra="desliza",
              css="letter-spacing:3px;background:#ff2d3d;border-radius:14px;padding:12px 0")
def RODAPE(t0, t1, txt, y=1648):
    L = F(t0, round(t1 - t0, 3), txt); L["xy"] = [40, y]; L["z"] = 86; return L
def CARIMBO(t0, t1, txt, xy, tam=170, rot=-7):
    return {"tipo": "carimbo", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": 60,
            "cor": VERM, "blend": "normal", "css": "background:rgba(255,255,255,.93)"}
def COMENT(t0, t1, txt, y, x=110, w=860, rot=-1.5):
    """comentário de rede (o mito circulando), cartão branco com avatar cinza"""
    return [CAIXA(t0, t1, x, y, w, 210, f"background:#fff;border-radius:28px;box-shadow:0 12px 30px rgba(0,0,0,.35);transform:rotate({rot}deg)", z=33, entra="desliza", dx=-500, dy=0),
            TX(t0, t1, "👤", x + 22, y + 28, 110, fonte="80px Montserrat", cor="#000", z=34, entra="desliza", dx=-500, dy=0),
            TX(t0, t1, txt, x + 140, y + 22, w - 170, fonte="800 80px Montserrat", cor="#16181b", z=34, entra="desliza", dx=-500, dy=0,
               css=f"line-height:1.05;transform:rotate({rot}deg)")]

# ---------- celular com grupo (aula) ----------
PX, PY, PW, PH = 150, 420, 780, 1180
SX, SY, SW, SH = 168, 438, 744, 1144     # tela
def BOLHA(t0, t1, txt, y, lado="esq", w=640, tam=80, z=33, entra="desliza", quem=None, **k):
    x = SX + 28 if lado == "esq" else SX + SW - 28 - w
    raio = "12px 40px 40px 40px" if lado == "esq" else "40px 12px 40px 40px"
    bg = "#ffffff" if lado == "esq" else "#d9fdd3"
    L = [TX(t0, t1, txt, x, y, w, fonte=f"700 {tam}px Montserrat", cor="#111", z=z, entra=entra, dy=90,
            css=f"background:{bg};border-radius:{raio};padding:28px 34px;box-shadow:0 6px 16px rgba(0,0,0,.16);line-height:1.12", **k)]
    if quem:
        L.append(TX(t0, t1, quem, x + 8, y - 40, w, fonte="800 30px Montserrat", cor=quem_cor(quem), z=z, entra=entra, dy=90,
                    alinha="left" if lado == "esq" else "right"))
    return L
def quem_cor(q): return {"🧠 Cérebro": "#c2185b", "🔐 Ovário": "#8d5a00", "💊 Pílula": "#1565c0"}.get(q, "#444")
def SISTEMA(t0, t1, txt, y):
    """aviso do grupo ('Pílula entrou no grupo'): pílula cinza no centro"""
    return TX(t0, t1, txt, SX + 90, y, SW - 180, fonte="700 32px Montserrat", cor="#3c4146", alinha="center", z=33, entra="pop",
              css="background:#fff6c9;border-radius:22px;padding:12px 10px;box-shadow:0 3px 8px rgba(0,0,0,.12)")
def CELULAR(t0, t1):
    D = dict(entra="desliza", dy=1400)
    return [CAIXA(t0, t1, PX, PY, PW, PH, "border-radius:86px;background:#15171a;box-shadow:0 40px 80px rgba(0,0,0,.55),inset 0 0 0 5px #3a3d42", z=20, **D),
            CAIXA(t0, t1, SX, SY, SW, SH, "border-radius:68px;background:#efe7dd;background-image:radial-gradient(rgba(120,100,80,.12) 2px,transparent 2px);background-size:30px 30px", z=21, **D),
            CAIXA(t0, t1, SX, SY, SW, 170, "border-radius:68px 68px 0 0;background:#2d3e45", z=22, **D),
            CAIXA(t0, t1, 465, 452, 150, 36, "border-radius:18px;background:#000", z=24, **D),
            TX(t0, t1, "‹", SX + 22, SY + 52, 60, fonte="300 90px Montserrat", cor="#ffffff", z=23, **D),
            TX(t0, t1, "💗", SX + 86, SY + 66, 84, fonte="32px Montserrat", cor="#e8415a", alinha="center", z=23,
               css="height:84px;padding-top:22px;border-radius:50%;background:#ffd8e0", **D),
            TX(t0, t1, "Ciclo do mês", SX + 190, SY + 66, 420, fonte="800 32px Montserrat", cor="#ffffff", z=23, **D)]
def STATUS(t0, t1, txt, cor="#cfe3e8", entra="nada"):
    return TX(t0, t1, txt, SX + 190, SY + 112, 520, fonte="500 28px Montserrat", cor=cor, z=23, entra=entra)
def PAINEL(t0, t1, y=630, h=430):
    """quadro branco no topo da conversa onde o desenho dos órgãos trabalha"""
    return CAIXA(t0, t1, SX + 24, y, SW - 48, h, "border-radius:34px;background:#fffdf8;box-shadow:0 8px 22px rgba(0,0,0,.16)", z=30, entra="pop")

# ================= abertura: viral em tela dividida + caixinha de pergunta =================
c = abertura(P, vd, "@steven", "center", "Mito ou verdade? 💊", "Anos de pílula deixam infértil?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 2.8, "dec": 1, "suf": " MILHÕES", "tam": 130,
               "rotulo": "de views no TikTok"},
              {"tipo": "glitch", "t": VA - 0.04, "d": 0.18}, {"tipo": "flash", "t": VA, "d": 0.18, "max": 0.35},
              {"tipo": "glitch", "t": VB - 0.04, "d": 0.18}, {"tipo": "flash", "t": VB, "d": 0.18, "max": 0.35}])
c += [TX(vd + 0.02, r1, "ANOS DE PÍLULA\\nDEIXAM INFÉRTIL?", 70, 190, 940, fonte="118px Anton", cor=BR, alinha="center", z=55,
         css="height:909px;background:linear-gradient(180deg,#2a0a10 0%,#5a0d10 100%);border:6px solid #ffd400;border-radius:14px;padding:90px 30px 0;line-height:1.1;" + SP),
      CARIMBO(vd + 0.12, r1, "MITO", [300, 600], tam=190, rot=-8),
      DS(vd + 0.6, r1, [{"k": "check", "c": [800, 930], "s": 70}], cor=VERDE, lw=24, z=61),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + "pc_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= I (indignado): o medo corre solto / anos de pílula? / não deixam / não gasta, não guarda =================
I2, I3, I4 = round(i_(8) - 0.15, 3), round(i_(15) - 0.25, 3), round(i_(17) - 0.05, 3)
c += [GL(r1), FL(r1),
      # I1 o medo corre solto: comentários do mito chegando
      TT(r1, I2, "ESSE MEDO CORRE SOLTO", y=230),
      *COMENT(r1 + 0.15, I2, "Pílula seca o útero 😱", 640, rot=-2),
      *COMENT(r1 + 0.45, I2, "Pílula = infértil? 😨", 900, rot=1.5),
      *COMENT(r1 + 0.7, I2, "Nunca mais volta? 😰", 1160, rot=-1),
      FL(I2),
      # I2 a pergunta
      GIG(I2, I3, "INFÉRTIL?", y=1330, tam=420),
      TT(I2, I3, "ANOS DE PÍLULA...", y=250, cor=AMAR),
      TX(i_(10), I3, "DEIXAM\\nINFÉRTIL?", 90, 640, 900, fonte="170px Anton", cor=BR, alinha="center", z=40, css=SP + ";line-height:1.0"),
      EMO(i_(11), I3, "🤔", 790, 1010, tam=150),
      # I3 não deixam
      TT(I3, I4, "NÃO DEIXAM", y=250, fz=170, cor=VERM),
      DS(i_(15) + 0.05, I4, [{"k": "x", "c": [540, 820], "s": 170}], lw=30),
      CARIMBO(i_(16), I4, "NÃO", [360, 1080], tam=210, rot=-6),
      FL(I4),
      # I4 não gasta, não guarda (o cofre fica igual)
      TT(I4, IF, "NÃO GASTA. NÃO GUARDA.", y=240),
      FIS(I4 + 0.05, IF, [{"k": "pc_cofre", "xy": [540, 860], "s": 1.15, "t": 0.0}], z=30, pulsos=[{"o": 0, "t": round(i_(20) - I4, 2)}, {"o": 0, "t": round(i_(25) - I4, 2)}]),
      CARD(i_(19), IF, "GASTA ÓVULO? ✗", 90, 1150, 430, "#ffb3c7", rot=-3, tam=100),
      CARD(i_(23), IF, "GUARDA? ✗", 560, 1150, 430, "#fff27a", rot=3, tam=100)]
SFX_I = [{"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "notif", "t": r1 + 0.15, "gain": 0.35},
         {"src": "notif", "t": r1 + 0.45, "gain": 0.3}, {"src": "notif", "t": r1 + 0.7, "gain": 0.3},
         {"src": "whoosh2", "t": I2, "gain": 0.35}, {"src": "boing", "t": i_(11), "gain": 0.28},
         {"src": "scratch", "t": i_(15) + 0.05, "gain": 0.32}, {"src": "boom", "t": i_(16), "gain": 0.45, "pico": 0.3, "d": 1.3},
         {"src": "whoosh", "t": I4, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": I4 + 0.1, "gain": 0.28},
         {"src": "papel", "t": i_(19), "gain": 0.42}, {"src": "papel", "t": i_(23), "gain": 0.42}]

# ================= V (rosto banco jp_rosto): "Sou médico. E quero muito que você saiba." =================
c += [GL(IF + 0.05),
      {"tipo": "video", "t": tV, "d": VD, "ms": 0, "src": M + "pc_vir.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[tV, 1.0, 0.01], [tV + 2.0, 1.08, 0.35]], "z": 40},
      {"tipo": "barra", "t": round(tV + 0.25, 3), "d": round(VD - 0.3, 2), "y": 215, "txt": "AULA RÁPIDA 👇", "cor": "#ffd400", "cor_txt": "#1a0508"}]
SFX_V = [{"src": "whoosh2", "t": tV, "gain": 0.35}]

# ================= B (manso): AULA no celular com o grupo "Ciclo do mês" =================
B2, B3, B4, B5 = [round(b_(k) - dt, 3) for k, dt in ((14, 0.15), (25, 0.15), (33, 0.15), (39, 0.15))]
CERX, CERY, OVX, OVY = 380, 790, 720, 860          # cérebro (esq) e cofre/ovário (dir) no painel
c += [GL(tB), FL(tB), SELO(tB + 0.2, AF, "● AULA RÁPIDA · SEM MARCA, SEM DOSE"), *CELULAR(tB, AF),
      STATUS(tB + 0.3, B3, "Cérebro, Ovário", entra="pop"), PAINEL(tB + 0.35, AF)]
for t0, t1, txt, cor in [(tB, B2, "O OVÁRIO É UM COFRE", BR), (B2, B3, "TODO MÊS: UM RECADO", AMAR),
                         (B3, B4, "A PÍLULA AVISA", BR), (B4, B5, "NENHUM ÓVULO SAI", VERM), (B5, AF, "O RECADO VOLTA", VERDE)]:
    c.append(TT(t0 + 0.02, t1 - 0.03, txt, y=240, fz=130, cor=cor))
# B1 o cofre: a mulher já nasce com os óvulos ali
c += [FIS(tB + 0.5, B2, [{"k": "pc_cofre", "xy": [540, 845], "s": 0.95, "t": 0.0}], z=31,
          pulsos=[{"o": 0, "t": round(WB[5]['s'] - 0.5, 2)}, {"o": 0, "t": round(WB[12]['s'] - 0.5, 2)}]),
      *BOLHA(b_(6) - 0.1, B2, "Já nasço com eles 🥚", 1130, lado="dir", w=620, quem="🔐 Ovário"),
      FL(B2)]
# B2 todo mês o cérebro manda o recado e um óvulo sai
c += [FIS(B2, B3, [{"k": "cerebro_lado", "xy": [CERX, CERY], "s": 0.62, "t": 0.0}, {"k": "pc_ovario_sai", "xy": [OVX, OVY + 40], "s": 0.62, "t": 0.15}], z=31,
          fluxos=[{"de": [CERX + 90, CERY + 40], "para": [OVX - 80, OVY + 20], "curva": -120, "cor": "#c2185b", "t": round(WB[18]['s'] - (B2 - tB), 2), "d": 2.4, "n": 6, "r": 12}],
          pulsos=[{"o": 0, "t": round(WB[17]['s'] - (B2 - tB), 2)}, {"o": 1, "t": round(WB[24]['s'] - (B2 - tB), 2)}]),
      *BOLHA(b_(16), B3, "Libera um óvulo aí!", 1130, lado="esq", w=620, quem="🧠 Cérebro"),
      *BOLHA(b_(21) - 0.1, B3, "Saindo! ✓✓", 1395, lado="dir", w=600, quem="🔐 Ovário"),
      FL(B3)]
# B3 a pílula entra no grupo e avisa: já tem hormônio
c += [STATUS(B3, AF, "Cérebro, Ovário, Pílula", entra="pop"),
      SISTEMA(b_(25), B4, "💊 Pílula entrou no grupo", 1100),
      FIS(B3, B4, [{"k": "cerebro_lado", "xy": [CERX, CERY], "s": 0.62, "t": 0.0}, {"k": "pc_cartela", "xy": [OVX, OVY - 10], "s": 0.62, "t": 0.2}], z=31,
          fluxos=[{"de": [OVX - 90, OVY - 30], "para": [CERX + 100, CERY + 10], "curva": -110, "cor": "#1565c0", "t": round(WB[27]['s'] - (B3 - tB), 2), "d": 2.2, "n": 6, "r": 12}],
          pulsos=[{"o": 0, "t": round(WB[29]['s'] - (B3 - tB), 2)}]),
      *BOLHA(b_(29), B4, "Já tem hormônio 👍", 1220, lado="dir", w=640, quem="💊 Pílula"),
      FL(B4)]
# B4 o cérebro fica quieto e nenhum sai (cofre fechado)
c += [FIS(B4, B5, [{"k": "sd_cerebro_off", "xy": [CERX, CERY], "s": 0.62, "t": 0.0}, {"k": "pc_cofre_fechado", "xy": [OVX, OVY - 10], "s": 0.62, "t": 0.15}], z=31),
      DS(b_(35), B5, [{"k": "x", "c": [550, 830], "s": 60}], lw=22, z=46),
      *BOLHA(b_(33), B5, "Ok, fico quieto 🤫", 1130, lado="esq", w=600, quem="🧠 Cérebro"),
      TX(b_(37) - 0.1, B5, "🔕 nenhum óvulo sai", SX + 120, 1420, SW - 240, fonte="800 32px Montserrat", cor="#3c4146", alinha="center", z=33,
         entra="pop", css="background:#ffe0e0;border-radius:22px;padding:14px 10px"),
      FL(B5)]
# B5 a pílula sai do grupo e o recado volta
c += [SISTEMA(b_(39), AF, "💊 Pílula saiu do grupo", 1100),
      FIS(B5, AF, [{"k": "cerebro_lado", "xy": [CERX, CERY], "s": 0.62, "t": 0.0}, {"k": "pc_ovario_sai", "xy": [OVX, OVY + 40], "s": 0.62, "t": 0.1}], z=31,
          fluxos=[{"de": [CERX + 90, CERY + 40], "para": [OVX - 80, OVY + 20], "curva": -120, "cor": "#c2185b", "t": round(WB[43]['s'] - (B5 - tB), 2), "d": 1.6, "n": 6, "r": 12, "fica": True}],
          pulsos=[{"o": 0, "t": round(WB[42]['s'] - (B5 - tB), 2)}, {"o": 1, "t": round(WB[44]['s'] - (B5 - tB), 2)}]),
      *BOLHA(b_(42), AF, "Voltei! Pode liberar 😄", 1220, lado="esq", w=640, quem="🧠 Cérebro"),
      DS(b_(44), AF, [{"k": "check", "c": [800, 1500], "s": 50}], cor=VERDE, lw=20, z=46)]
SFX_B = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.45, "pico": 0.45}, {"src": "papel", "t": tB + 0.5, "gain": 0.35},
         {"src": "boing", "t": b_(5), "gain": 0.25}, {"src": "notif", "t": b_(6) - 0.1, "gain": 0.32},
         {"src": "whoosh2", "t": B2, "gain": 0.35}, {"src": "notif", "t": b_(16), "gain": 0.32}, {"src": "riser", "t": b_(18) - 0.3, "gain": 0.12, "d": 1.2},
         {"src": "notif", "t": b_(21) - 0.1, "gain": 0.32}, {"src": "boing", "t": b_(24), "gain": 0.28},
         {"src": "whoosh2", "t": B3, "gain": 0.35}, {"src": "notif", "t": b_(25), "gain": 0.35}, {"src": "notif", "t": b_(29), "gain": 0.32},
         {"src": "whoosh2", "t": B4, "gain": 0.3}, {"src": "notif", "t": b_(33), "gain": 0.3}, {"src": "scratch", "t": b_(35), "gain": 0.28},
         {"src": "glitch", "t": b_(37) - 0.1, "gain": 0.18},
         {"src": "whoosh2", "t": B5, "gain": 0.35}, {"src": "notif", "t": b_(39), "gain": 0.35}, {"src": "notif", "t": b_(42), "gain": 0.32},
         {"src": "boing", "t": b_(44), "gain": 0.28}]

# ================= C (neutro): estudo no cartão de notícia =================
C2, C3 = round(e_(9) - 0.15, 3), round(e_(20) - 0.1, 3)
CX0, CY0, CW, CH = 90, 560, 900, 960
c += [GL(AF), FL(AF), SELO(tC + 0.2, CF, "● O QUE A PESQUISA ACHOU"),
      CAIXA(tC, CF, CX0, CY0, CW, CH, "border-radius:34px;background:#fffaf2;box-shadow:0 30px 70px rgba(0,0,0,.55)", z=30, entra="desliza", dy=1300),
      CAIXA(tC, CF, CX0, CY0, CW, 120, "border-radius:34px 34px 0 0;background:#5a0d10", z=31, entra="desliza", dy=1300),
      TX(tC, CF, "📰  REVISTA MÉDICA BMJ · 2020", CX0, CY0 + 38, CW, fonte="800 32px Montserrat", cor="#ffd400", alinha="center", z=32, entra="desliza", dy=1300,
         css="letter-spacing:2px"),
      RODAPE(tC, CF, "Yland e col., BMJ 2020 · 17.954 mulheres da Dinamarca e da América do Norte · doi 10.1136/bmj.m3966", y=1604)]
# C1 Boston, 2020, quase 18 mil mulheres
c += [TT(tC + 0.02, C2 - 0.03, "BOSTON, 2020", y=240, fz=150),
      TX(tC + 0.25, C2, "pesquisa da Universidade de Boston", CX0 + 40, CY0 + 160, CW - 80, fonte="700 32px Montserrat", cor="#5b6770", alinha="center", z=32),
      {"tipo": "numero", "t": e_(6) - 0.15, "d": round(C2 - e_(6) + 0.15, 3), "xy": [CX0, CY0 + 260], "w": CW, "valor": 18, "pre": "QUASE ", "suf": " MIL", "tam": 170,
       "cor": "#b3121f", "sombra": "#e9c3c3", "rotulo": "mulheres acompanhadas", "cor_rotulo": "#1c1a17", "sombra_rotulo": "none", "z": 33},
      TX(tC + 0.3, C2, "👩👩👩", CX0, 1180, CW, fonte="150px Montserrat", cor="#000", alinha="center", z=33, css="filter:drop-shadow(0 10px 12px rgba(0,0,0,.30))"),
      FL(C2)]
# C2 quem parou voltou ao normal em uns 3 ciclos
c += [TT(C2 + 0.02, C3 - 0.03, "VOLTOU AO NORMAL", y=240, fz=140, cor=VERDE),
      TX(C2 + 0.1, C3, "PAROU A PÍLULA?", CX0 + 40, CY0 + 160, CW - 80, fonte="900 80px Montserrat", cor="#1c1a17", alinha="center", z=32),
      FIS(e_(16) - 0.2, C3, [{"k": "calendario", "xy": [290, 1020], "s": 0.5, "t": 0.0}, {"k": "calendario", "xy": [540, 1020], "s": 0.5, "t": 0.25},
                              {"k": "calendario", "xy": [790, 1020], "s": 0.5, "t": 0.5}], z=33),
      TX(e_(18) - 0.15, C3, "~3 CICLOS", CX0, CY0 + 640, CW, fonte="190px Anton", cor="#b3121f", alinha="center", z=34, entra="zoom",
         css="text-shadow:6px 6px 0 #e9c3c3"),
      FL(C3)]
# C3 anos de uso não mudaram a chance (duas barras iguais)
c += [TT(C3 + 0.02, CF, "ANOS DE USO?", y=240, fz=150, cor=AMAR),
      CAIXA(C3 + 0.4, CF, 230, 840, 180, 300, "border-radius:18px 18px 6px 6px;background:#3ddc84;box-shadow:0 8px 18px rgba(0,0,0,.25)", z=34),
      CAIXA(C3 + 0.7, CF, 670, 840, 180, 300, "border-radius:18px 18px 6px 6px;background:#3ddc84;box-shadow:0 8px 18px rgba(0,0,0,.25)", z=34),
      TX(C3 + 0.9, CF, "=", 440, 880, 200, fonte="170px Anton", cor="#1c1a17", alinha="center", z=34),
      TX(C3 + 0.3, CF, "POUCOS", CX0 + 40, CY0 + 140, 380, fonte="100px Anton", cor="#1c1a17", alinha="center", z=34),
      TX(C3 + 0.5, CF, "MUITOS", CX0 + CW - 420, CY0 + 140, 380, fonte="100px Anton", cor="#1c1a17", alinha="center", z=34),
      TX(C3 + 0.4, CF, "chance de engravidar", CX0, 1150, CW, fonte="700 32px Montserrat", cor="#5b6770", alinha="center", z=34),
      TX(e_(24) - 0.1, CF, "NÃO MUDOU\\nA CHANCE", CX0 + 40, CY0 + 650, CW - 80, fonte="120px Anton", cor="#ffffff", alinha="center", z=35, entra="zoom",
         css="background:#1d7a3e;border-radius:26px;padding:16px 0;line-height:1.02;box-shadow:0 10px 24px rgba(0,0,0,.3)")]
SFX_C = [{"src": "whoosh", "t": AF + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": tC + 0.1, "gain": 0.4},
         {"src": "riser", "t": e_(6) - 1.0, "gain": 0.16, "d": 1.0}, {"src": "boom", "t": e_(6), "gain": 0.45, "pico": 0.3, "d": 1.3},
         {"src": "whoosh2", "t": C2, "gain": 0.35}, {"src": "boing", "t": e_(16) - 0.2, "gain": 0.22}, {"src": "boing", "t": e_(16) + 0.05, "gain": 0.22},
         {"src": "boing", "t": e_(16) + 0.3, "gain": 0.22}, {"src": "boom", "t": e_(18) - 0.15, "gain": 0.42, "pico": 0.3, "d": 1.2},
         {"src": "whoosh2", "t": C3, "gain": 0.35}, {"src": "boing", "t": C3 + 0.4, "gain": 0.25}, {"src": "boing", "t": C3 + 0.7, "gain": 0.25}, {"src": "boing", "t": e_(24) - 0.1, "gain": 0.3}]

# ================= E (alegre): cobrança (a tia do almoço de domingo) =================
E2 = round(q_(8) - 0.15, 3)
c += [GL(CF + 0.05), FL(CF + 0.05),
      TT(CF + 0.05, E2, "QUEM NÃO SEGUIR...", y=250, fz=150),
      TX(tE + 0.1, EF, "Seguir", 290, 470, 500, fonte="900 100px Montserrat", cor="#ffffff", alinha="center", z=44,
         css="background:#0095f6;border-radius:34px;padding:22px 0;box-shadow:0 16px 40px rgba(0,0,0,.30)"),
      EMO(tE + 0.3, E2 + 0.4, "👆", 650, 560, tam=150, z=45),
      FL(E2),
      TT(E2 + 0.02, EF, "...EXPLICA PRA TIA", y=250, fz=150, cor=AMAR),
      EMO(E2 + 0.05, EF, "👵", 120, 860, tam=260, z=40),
      TX(E2 + 0.2, EF, "“Pílula seca\\no útero!”", 430, 820, 560, fonte="800 80px Montserrat", cor="#111", z=41, entra="pop",
         css="background:#ffffff;border-radius:40px 40px 40px 12px;padding:26px 30px;box-shadow:0 10px 24px rgba(0,0,0,.3);line-height:1.08"),
      EMO(q_(9) - 0.05, EF, "🍗", 160, 1180, tam=150, z=40),
      FIS(q_(6) - 0.1, EF, [{"k": "pc_cofre", "xy": [700, 1330], "s": 0.7, "t": 0.0}], z=39)]
SFX_E = [{"src": "whoosh2", "t": CF + 0.05, "gain": 0.35}, {"src": "notif", "t": tE + 0.15, "gain": 0.35}, {"src": "boing", "t": tE + 0.3, "gain": 0.3},
         {"src": "whoosh", "t": E2, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": E2 + 0.2, "gain": 0.3}, {"src": "papel", "t": q_(6) - 0.1, "gain": 0.3}]

# ================= F (manso): um porém (ciclo bagunçado antes) e conversem com o médico =================
F2 = round(f_(11) - 0.15, 3)
c += [GL(EF + 0.05), FL(EF + 0.05),
      TT(EF + 0.05, f_(4) - 0.1, "UM PORÉM", y=240, fz=170, cor=AMAR),
      TT(f_(4) - 0.08, F2, "CICLO BAGUNÇADO ANTES?", y=240),
      FIS(tF + 0.2, F2, [{"k": "calendario", "xy": [540, 900], "s": 1.15, "t": 0.0}], z=31),
      DS(f_(6), F2, [{"k": "circulo", "c": [410, 860], "r": [46, 40]}, {"k": "circulo", "c": [640, 980], "r": [46, 40]}], cor=VERM, lw=12, z=46),
      CARD(f_(8) - 0.05, F2, "PODE VOLTAR IGUAL", 110, 1220, 860, "#fff27a", rot=-2, tam=110),
      FL(F2),
      TT(F2 + 0.02, FF, "VOCÊS DOIS", y=240, fz=170),
      FIS(F2 + 0.05, FF, [{"k": "sx_casal", "xy": [540, 860], "s": 1.15, "t": 0.0}], z=30, pulsos=[{"o": 0, "t": round(WF[12]['s'] - (F2 - tF), 2)}]),
      CARD(f_(14) - 0.2, FF, "CONVERSEM COM\\nO MÉDICO ANTES", 110, 1180, 860, "#9be3a8", rot=-2, tam=110),
      EMO(f_(17) - 0.3, FF, "🩺", 790, 1440, tam=150, z=40)]
SFX_F = [{"src": "whoosh", "t": EF + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": tF + 0.2, "gain": 0.28}, {"src": "scratch", "t": f_(6), "gain": 0.28},
         {"src": "papel", "t": f_(8) - 0.05, "gain": 0.42}, {"src": "whoosh2", "t": F2, "gain": 0.35}, {"src": "boing", "t": F2 + 0.1, "gain": 0.22},
         {"src": "papel", "t": f_(14) - 0.2, "gain": 0.42}, {"src": "boing", "t": f_(17) - 0.3, "gain": 0.25}]

# ================= CTA (banco cta6) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": CTA_D, "ms": 0, "src": M + "pc_cta.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 2.2, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": round(CTA_D - 0.25, 2), "y": 215, "txt": "TE AJUDOU? SEGUE + CURTE", "cor": "#ffd400", "cor_txt": "#1a0508"}]

# ================= D (neutro): fecho =================
D2 = round(d_(7) - 0.05, 3)
c += [GL(c2), FL(c2),
      TT(c2 + 0.03, D2, "A PÍLULA PÕE EM PAUSA", y=250),
      EMO(c2 + 0.15, D2, "⏸️", 400, 700, tam=230),
      FL(D2),
      GIG(D2, dur, "COFRE", y=1330, tam=440),
      TT(D2 + 0.02, dur, "QUEM MEXE NO COFRE É O TEMPO", y=230, cor=AMAR),
      FIS(D2 + 0.05, dur, [{"k": "pc_cofre_fechado", "xy": [400, 830], "s": 0.85, "t": 0.0}, {"k": "cy_relogio", "xy": [760, 790], "s": 0.6, "t": 0.2}], z=30),
      CARIMBO(D2 + 0.35, dur, "MITO", [300, 1060], tam=170, rot=-6),
      RODAPE(c2, dur, "Yland e col., BMJ 2020 · doi 10.1136/bmj.m3966 · Vídeo original: @steven · Conteúdo educativo", y=1560)]
SFX_D = [{"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": c2 + 0.05, "gain": 0.4, "pico": 0.45},
         {"src": "whoosh2", "t": D2, "gain": 0.35}, {"src": "boom", "t": D2 + 0.35, "gain": 0.5, "pico": 0.3, "d": 1.5}, {"src": "boing", "t": D2 + 0.4, "gain": 0.3}]

voz = [{"src": M + "pc_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "pc_viral.words.json", "gain": 0.16},
       {"src": M + "pc_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "pc_r1.mp4", "t": vd, "ms": 0, "d": 2.76, "palavras": M + "pc_r1.words.json"},
       {"src": M + "pc_i_voz.wav", "t": tI, "ms": 0, "d": DI, "palavras": M + "pc_i_voz.words.json"},
       {"src": M + "pc_vir.mp4", "t": tV, "ms": 0, "d": VD, "palavras": M + "pc_vir.words.json"},
       {"src": M + "pc_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "pc_b_voz.words.json"},
       {"src": M + "pc_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "pc_c_voz.words.json"},
       {"src": M + "pc_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "pc_e_voz.words.json"},
       {"src": M + "pc_f_voz.wav", "t": tF, "ms": 0, "d": DF, "palavras": M + "pc_f_voz.words.json"},
       {"src": M + "pc_cta.mp4", "t": c1, "ms": 0, "d": CTA_D, "palavras": M + "pc_cta.words.json"},
       {"src": M + "pc_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "pc_d_voz.words.json"},
       # mix.py corta a trilha quando o barramento de fala acaba (sidechain): este trecho a -70 dB (inaudível) mantém a fala
       # "viva" até o fim, e a trilha do fecho termina com o próprio fade em vez de sumir na última palavra.
       {"src": M + "pc_b_voz.wav", "t": round(tD + DD - 0.05, 3), "ms": 0, "d": round(dur - tD - DD + 0.05, 2), "gain": 0.0003}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "glitch", "t": VA - 0.06, "gain": 0.28}, {"src": "boing", "t": 3.6, "gain": 0.3}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": VB - 0.06, "gain": 0.28},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.15, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, *SFX_I, {"src": "glitch", "t": IF, "gain": 0.4}, *SFX_V,
       {"src": "glitch", "t": tB - 0.05, "gain": 0.4}, *SFX_B,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.4}, *SFX_C,
       {"src": "glitch", "t": CF + 0.05, "gain": 0.4}, *SFX_E,
       {"src": "glitch", "t": EF + 0.05, "gain": 0.4}, *SFX_F,
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, *SFX_D]
for L in c:
    if vd <= L.get("t", 0) < dur: L["fixo"] = True
salvar(PID, dur, 616, c, voz, sfx, {"r1_fim": r1, "esconde": [[tV, tV + VD], [c1, c2]],
                                    "ys": [[0, 4.0, 1720], [4.0, vd, 1620], [vd, r1, 1780], [r1, tV, 1700], [tB, CF, 1712], [CF, dur, 1700]]})
p = json.load(open(f'planos/{PID}.json'))
# trilha contínua por baixo de tudo depois do viral (nenhuma pausa muda); uma faixa por bloco, emenda cruzada
p['audio']['musica'] = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.2, "fade": 0.6},
                        {"src": "m_emocao", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tC - tB + 0.8, 2), "gain": 0.17, "fade": 0.6},
                        {"src": "m_investiga", "t": round(tC - 0.4, 2), "ms": 0, "d": round(tE - tC + 0.8, 2), "gain": 0.2, "fade": 0.6},
                        {"src": "m_humor", "t": round(tE - 0.4, 2), "ms": 0, "d": round(tF - tE + 0.8, 2), "gain": 0.16, "fade": 0.6},
                        {"src": "m_viagem", "t": round(tF - 0.4, 2), "ms": 0, "d": round(c2 - tF + 0.7, 2), "gain": 0.16, "fade": 0.6},
                        {"src": "m_emocao", "t": round(c2 - 0.3, 2), "ms": 22, "d": round(dur - c2 + 0.3, 2), "gain": 0.18, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tI", tI, "tV", tV, "tB", tB, "tC", tC, "tE", tE, "tF", tF, "c1", c1, "c2", c2, "tD", tD)
if '--sem-pos' not in sys.argv:
    subprocess.run(["python3", "scripts/entrada.py", PID, M + "pc_ent.mp4", M + "pc_ent.mp4.words.json", "2.07",
                    "ANOS DE PÍLULA DEIXAM INFÉRTIL?", "especialista em fertilidade respondeu num podcast"], check=True)
    subprocess.run(["python3", "scripts/pele.py", PID, "noticia"], check=True)
