# plano_l4_umemquatro.py (14/11, lote 4, TDAH Adulto Real): "1 em cada 4 adultos desconfia que tem TDAH" (reportagem CBC News, TikTok @cbcnews).
# Trecho em 2 pedaços (dublagem Murilo, original a 0,16): A 22,10-28,55 (repórter, cartão "1 in 4 adults"; os 0,9 s iniciais do vídeo
# são o 1º quadro limpo do cartão congelado, porque até 23,0 s ainda aparece o cartão de receita de remédio no Canadá) e
# B 32,02-36,08 (psicóloga). Fora: 0-22 s (remédio) e 28,6-32 s (TikTok de pessoa comum). Veredito VERDADE ("desconfia").
# r1 SEM crédito novo: banco ca2_r1 (6cd9, "É verdade, tá? E eu te mostro o porquê."), copiado para uq_r1.
# Voz: 4 blocos HeyGen sem <break> (pausas abertas na edição em tmp_uq/voz.py): I indignado (resposta), M manso (aula + o que fazer),
# N neutro (estudo + fecho), A alegre (cobrança). Aula em MAPEAMENTO: quadro de papel antigo (braçadeira de pressão, linha do dia
# manhã/tarde/noite subindo e descendo, depois a linha do TDAH baixa desde criança), mapa-múndi com alfinetes e bolinhas de 100
# no estudo. Pele NOTÍCIA (TDAH: Cury lab, meninas cartões), legenda serifada.
# Depois deste script (o próprio script roda):
#   python3 scripts/entrada.py react_l4_umemquatro assets/midia/uq_ent.mp4 assets/midia/uq_ent.mp4.words.json 2.07 \
#     '1 EM 4 ACHA QUE TEM TDAH?' 'o que as pesquisas grandes dizem' && python3 scripts/pele.py react_l4_umemquatro noticia
import sys, json, math, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l4_umemquatro'; P = 'uq'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}uq_{k}_voz.words.json'))
WI, WB, WC, WF, WE, WD = W('i'), W('b'), W('c'), W('f'), W('e'), W('d')
DI, DB, DC, DF, DE, DD = [round(dur_de(f'{M}uq_{k}_voz.wav'), 3) for k in 'ibcfed']
vd = 10.51
r1 = round(vd + 2.206 + 0.5, 2)          # uq_r1: última palavra termina em 2,206 s; 0,5 s de folga
tI = round(r1 + 0.15, 2)
tB = round(tI + DI + 0.45, 2)
tC = round(tB + DB + 0.8, 2)            # respiro depois da aula
tF = round(tC + DC + 0.8, 2)
tE = round(tF + DF + 0.5, 2)
c1 = round(tE + DE + 0.1, 2)            # CTA 6cd9 (banco cta6_serio, 3,01 s)
c2 = round(c1 + 3.01, 2)
tD = round(c2 + 0.15, 2)
dur = round(tD + DD + 0.85, 2)
i_ = lambda k: round(tI + WI[k]['s'], 3); b_ = lambda k: round(tB + WB[k]['s'], 3); e_ = lambda k: round(tC + WC[k]['s'], 3)
f_ = lambda k: round(tF + WF[k]['s'], 3); q_ = lambda k: round(tE + WE[k]['s'], 3); d_ = lambda k: round(tD + WD[k]['s'], 3)
IF, AF, CF, FF, EF = round(tB - 0.05, 3), round(tC - 0.05, 3), round(tF - 0.1, 3), round(tE - 0.1, 3), c1
VERDE, AMAR, VERM, TINTA, CINZA = "#3ddc84", "#ffd400", "#ff2d3d", "#1c1a17", "#9aa3ad"
SOMBRA = "text-shadow:7px 7px 0 #000"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.45}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}
def TT(t0, t1, txt, y=250, fz=120, cor="#ffffff", **k):
    # cabe em 1 linha (Anton ~0,47 em por letra em 940 px) ou vai a 2 linhas um pouco mais alto
    if 0.47 * fz * len(txt) > 940:
        um = int(940 / (0.47 * len(txt)))
        if um >= 108: fz = um
        else: fz = min(fz, 116); y = min(y, 230)
    return T(t0, round(t1 - t0, 3), txt, y=y, f=f"{fz}px Anton", cor=cor, css=SOMBRA, vel=0.09, **k)
def GIG(t0, t1, txt, y=1250, tam=430, cont=False, cor="rgba(255,212,0,.16)", ida=True):
    L = {"tipo": "gigante", "t": round(t0, 3), "d": round(t1 - t0, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t0, t1, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t0, 3), "d": round(t1 - t0, 3), "z": z, "orgaos": orgaos}; L.update(k); return L
def DS(t0, t1, formas, cor=VERM, lw=14, z=45, vel=0.45):
    return {"tipo": "desenho", "t": round(t0, 3), "d": round(t1 - t0, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel}
def PAPEL(t0, t1, y=490, h=1090):
    """quadro de papel antigo do Mapeamento (o fundo da pele aparece em volta)"""
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [50, y], "w": 980, "fonte": "120px Anton", "cor": TINTA,
            "alinha": "center", "txt": " ", "z": 15, "entra": "pop",
            "css": f"height:{h}px;border-radius:12px;border:6px solid #8a7650;box-shadow:0 34px 70px rgba(0,0,0,.6);"
                   "background:radial-gradient(ellipse at 50% 40%,#f8f1de 0%,#e9dcbc 70%,#cdb98f 100%)"}
def MOLDURA(t0, t1, y=490, h=1090):
    """janela do quadro por cima do mapa: o resto do mapa fica escurecido (spotlight)"""
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [50, y], "w": 980, "fonte": "120px Anton", "cor": TINTA,
            "alinha": "center", "txt": " ", "z": 25, "entra": "nada",
            "css": f"height:{h}px;border-radius:12px;border:6px solid #8a7650;box-shadow:0 0 0 2400px rgba(22,6,10,.86)"}
def CARD(t0, t1, txt, x, y, w, cor, rot=-3, tam=100, cor_txt=TINTA, z=36):
    """cartão colorido preso com fita (Mapeamento)"""
    return [{"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": w, "fonte": f"{tam}px Anton", "cor": cor_txt,
             "alinha": "center", "txt": txt, "z": z, "entra": "pop",
             "css": f"background:{cor};padding:22px 18px 18px;border-radius:6px;box-shadow:0 14px 28px rgba(0,0,0,.35);transform:rotate({rot}deg);line-height:1.05"},
            {"tipo": "texto", "t": round(t0 + 0.12, 3), "d": round(t1 - t0 - 0.12, 3), "xy": [x + w // 2 - 80, y - 26], "w": 160, "fonte": "120px Anton",
             "cor": TINTA, "alinha": "center", "txt": " ", "z": z + 1, "entra": "pop",
             "css": f"height:52px;background:rgba(244,232,196,.85);box-shadow:0 2px 5px rgba(0,0,0,.25);transform:rotate({-rot * 2 + 4}deg)"}]
def EMO(t0, t1, ch, x, y, tam=170, z=38):
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": tam + 60, "fonte": f"{tam}px Montserrat", "cor": "#000",
            "alinha": "center", "txt": ch, "z": z, "entra": "pop", "css": "filter:drop-shadow(0 10px 12px rgba(0,0,0,.35))"}
def PILULA(t0, t1, txt, y, cor=AMAR, cor_txt="#111", x=140, w=800, tam=100, z=45):
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": w, "fonte": f"{tam}px Anton", "cor": cor_txt,
            "alinha": "center", "txt": txt, "z": z, "entra": "pop", "css": f"background:{cor};border-radius:26px;padding:14px 0;box-shadow:0 14px 30px rgba(0,0,0,.4)"}
def SELO(t0, t1, txt):
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [60, 128], "w": 960, "fonte": "900 32px Montserrat", "cor": "#ffffff",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ff2d3d;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"}
def ROT(txt, x, y, cor="#ffffff", t=0.0):
    """rótulo grande (Anton 56, contorno preto) num órgão vazio: não é cartela, é etiqueta do desenho"""
    return {"k": "uq_vazio", "xy": [x, y], "s": 1.0, "t": t, "rotulo": txt, "rot_y": 20, "cor_rotulo": cor}
def RODAPE(t0, t1, txt, y=1592):
    # z 86: fora da câmera na mão (senão o zoom de 1,12 empurra a nota para cima da legenda)
    L = F(t0, round(t1 - t0, 3), txt); L["xy"] = [40, y]; L["z"] = 86; return L

# ---------- linha do dia (fisio_extra/linha_do_dia.svg) e as curvas desenhadas por cima ----------
LX, LY, LS = 540, 1060, 2.1
def scr(x, y): return [round(LX + LS * x, 1), round(LY + LS * y, 1)]
def onda(u): return 0.9 * math.sin(math.pi * u) - 0.45 + 0.15 * math.sin(5 * math.pi * u)
def curva(u0, u1, f, n=26):
    return [scr(-185 + 370 * (u0 + (u1 - u0) * j / n), -11 - 30 * f(u0 + (u1 - u0) * j / n)) for j in range(n + 1)]
cai = lambda u: onda(u) - 1.9 * math.exp(-((u - 0.78) / 0.085) ** 2)

# ================= abertura: viral em tela dividida + caixinha de pergunta =================
c = abertura(P, vd, "@cbcnews", "center 34%", "Mito ou verdade? 🧠", "1 em cada 4 adultos desconfia que tem TDAH?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 245.1, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta": L["botoes"] = ["MITO", "VERDADE"]; L["escolha"] = 1
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(r1 - vd - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "128px Anton", "cor": "#ffffff", "alinha": "center",
       "txt": "É VERDADE:\\n1 EM 4\\nDESCONFIA.", "z": 55, "entra": "pop",
       "css": "background:rgba(20,6,10,.93);border-radius:14px;height:909px;box-sizing:border-box;padding:90px 40px 0;line-height:1.12;text-shadow:6px 6px 0 #000"},
      {"tipo": "carimbo", "t": vd + 0.45, "d": round(r1 - vd - 0.45, 2), "xy": [215, 690], "txt": "VERDADE", "tam": 140, "rot": -7, "z": 60,
       "cor": "#14964a", "blend": "normal", "css": "background:rgba(255,255,255,.92)"},
      {"tipo": "video", "t": vd, "d": round(r1 - vd, 2), "ms": 0, "src": M + "uq_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= I (indignado): desconfiar tudo bem / todo mundo se distrai / desconfiar não é ter =================
I2, I3, I4 = round(i_(3) - 0.15, 3), round(i_(12) - 0.15, 3), round(i_(16) - 0.15, 3)
c += [GL(r1), FL(r1),
      # I1 desconfiar, tudo bem
      GIG(r1, I2, "DESCONFIAR", y=1250, tam=430, cont=True, cor="rgba(255,212,0,.4)"),
      TT(i_(0), i_(0) + 2.2, "DESCONFIAR? TUDO BEM.", y=300, fz=140),
      EMO(i_(0) + 0.15, I2, "🤔", 395, 760, tam=230),
      DS(i_(1), I2, [{"k": "check", "c": [540, 1300], "s": 90}], cor=VERDE, lw=24),
      FL(I2),
      # I2 um sintoma aqui, outro ali... é normal
      TT(i_(0) + 2.2, i_(10) - 0.05, "UM SINTOMA AQUI, OUTRO ALI", y=280, fz=120),
      *CARD(i_(7) - 0.25, I3, "ESQUECI\\nA CHAVE", 90, 700, 440, "#fff27a", rot=-5),
      *CARD(i_(8), I3, "ME\\nDISTRAÍ", 560, 900, 420, "#ffb3c7", rot=4),
      DS(i_(10), I3, [{"k": "check", "c": [560, 1400], "s": 85}], cor=VERDE, lw=24),
      TT(i_(10) - 0.05, I4, "NORMAL: TODO MUNDO SE DISTRAI", y=280, fz=120, cor=AMAR),
      FL(I3),
      # I3 todo mundo
      GIG(I3, I4, "TODO MUNDO", y=1380, tam=400, ida=False),
      FIS(I3 + 0.05, I4, [{"k": "jp_pessoa", "xy": [250, 1050], "s": 0.95, "t": 0.0}, {"k": "jp_pessoa", "xy": [540, 1030], "s": 1.05, "t": 0.15},
                         {"k": "jp_pessoa", "xy": [830, 1050], "s": 0.95, "t": 0.3},
                         {"k": "cy_nuvem", "xy": [250, 760], "s": 0.4, "t": 0.5}, {"k": "cf_lua", "xy": [830, 760], "s": 0.35, "t": 0.7}],
          pulsos=[{"o": 0, "t": 0.6}, {"o": 1, "t": 0.9}, {"o": 2, "t": 1.2}]),
      FL(I4),
      # I4 desconfiar ≠ ter (o ≠ desenhado à mão)
      TT(I4, IF, "DESCONFIAR", y=520, fz=190, anim=None, entra="zoom"),
      DS(i_(18) - 0.1, IF, [{"k": "linha", "pts": [[380, 830], [700, 830]], "j": 2}, {"k": "linha", "pts": [[380, 900], [700, 900]], "j": 2, "t": 0.15},
                             {"k": "linha", "pts": [[470, 990], [610, 740]], "j": 2, "t": 0.3}], cor=VERM, lw=26, vel=0.3),
      TT(I4 + 0.35, IF, "TER", y=1000, fz=260, cor=AMAR, anim=None, entra="zoom")]
SFX_I = [{"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": i_(0) + 0.2, "gain": 0.3},
         {"src": "notif", "t": i_(1), "gain": 0.3}, {"src": "whoosh2", "t": I2, "gain": 0.35},
         {"src": "papel", "t": i_(7) - 0.25, "gain": 0.4}, {"src": "papel", "t": i_(8), "gain": 0.4}, {"src": "notif", "t": i_(10), "gain": 0.3},
         {"src": "whoosh2", "t": I3, "gain": 0.35}, {"src": "boing", "t": I3 + 0.1, "gain": 0.22}, {"src": "boing", "t": I3 + 0.4, "gain": 0.22},
         {"src": "whoosh", "t": I4, "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": i_(18) - 0.05, "gain": 0.3},
         {"src": "boom", "t": i_(19) + 0.05, "gain": 0.5, "pico": 0.3, "d": 1.4}]

# ================= B (manso): AULA em Mapeamento =================
B2, B3, B4, B5, B6, B7 = [round(b_(k) - 0.15, 3) for k in (5, 10, 15, 24, 28, 33)]   # trocas visuais junto da fala
c += [GL(tB), FL(tB), SELO(tB + 0.2, AF, "● AULA RÁPIDA · SEM DIAGNÓSTICO"), PAPEL(tB, AF)]
# cartelas (cada uma >= tempo de leitura; podem atrasar um pouco da fala)
TB = [tB, tB + 2.1, tB + 3.96, tB + 5.82, tB + 7.68, B5, tB + 13.02, tB + 15.4, tB + 17.25, AF]
for k, (txt, cor) in enumerate([("PENSA NA PRESSÃO", "#ffffff"), ("TODO MUNDO TEM", "#ffffff"), ("SOBE E DESCE", AMAR),
                                ("A ATENÇÃO TAMBÉM", "#ffffff"), ("DORMIU MAL? ELA\u00a0CAI", AMAR), ("TDAH É OUTRA COISA", VERM),
                                ("DESDE CRIANÇA", AMAR), ("EM TODO CANTO", AMAR), ("ATRAPALHA A VIDA", VERM)]):
    c.append(TT(TB[k] + 0.02, TB[k + 1] - 0.03, txt, y=250, fz=130, cor=cor))
# B1-B2: braçadeira de pressão (grande), todo mundo tem
c += [FIS(tB + 0.1, B3 + 0.05, [{"k": "bracadeira_pressao", "xy": [540, 1000], "s": 2.0, "t": 0.0}],
          pulsos=[{"o": 0, "t": round(WB[2]['s'] + 0.1, 2)}, {"o": 0, "t": round(WB[5]['s'] + 0.1, 2)}]),
      FIS(B2, B3 + 0.05, [{"k": "jp_pessoa", "xy": [190, 1440], "s": 0.32, "t": 0.0}, {"k": "jp_pessoa", "xy": [330, 1440], "s": 0.32, "t": 0.1},
                         {"k": "jp_pessoa", "xy": [750, 1440], "s": 0.32, "t": 0.2}, {"k": "jp_pessoa", "xy": [890, 1440], "s": 0.32, "t": 0.3}], z=31),
      FL(B3)]
# B2-B3: linha do dia (manhã, tarde, noite), a pressão sobe e desce dentro da faixa verde
c += [FIS(B3, B5 + 0.05, [{"k": "linha_do_dia", "xy": [LX, LY], "s": LS, "t": 0.0}], z=28),
      FIS(B3 + 0.05, B4, [{"k": "bracadeira_pressao", "xy": [255, 640], "s": 0.62, "t": 0.0}], z=31),
      FIS(B3 + 0.1, B4, [ROT("PRESSÃO", 690, 640, cor="#ffffff")], z=32),
      DS(b_(10) - 0.05, B4, [{"k": "linha", "pts": curva(0, 1, onda), "j": 1.2}], cor="#2a6df4", lw=16, vel=2.6),
      FL(B4)]
# B3: a atenção também: dormiu mal, se preocupou, ela cai (e volta)
SETA = lambda t0, x: DS(t0, B5, [{"k": "seta", "de": [x, 868], "para": [x + 20, 980], "curva": 0}], cor="#5a4a35", lw=12, vel=0.35)
c += [FIS(B4, B5, [{"k": "cerebro_lado", "xy": [255, 640], "s": 0.55, "t": 0.0}], z=31, pulsos=[{"o": 0, "t": 0.5}]),
      FIS(B4 + 0.05, B5, [ROT("ATENÇÃO", 690, 640, cor=AMAR)], z=32),
      DS(b_(16) - 0.05, B5, [{"k": "linha", "pts": curva(0, 0.6, onda, 16), "j": 1.2}], cor="#2a6df4", lw=16, vel=1.6),
      FIS(b_(18) - 0.05, B5, [{"k": "cf_lua", "xy": [690, 790], "s": 0.32, "t": 0.0}], z=33, pulsos=[{"o": 0, "t": 0.5}]),
      SETA(b_(19), 690),
      FIS(b_(20) - 0.05, B5, [{"k": "cy_nuvem", "xy": [840, 790], "s": 0.34, "t": 0.0}], z=33, pulsos=[{"o": 0, "t": 0.5}]),
      SETA(b_(21) + 0.1, 800),
      DS(b_(22) - 0.1, B5, [{"k": "linha", "pts": curva(0.6, 1, cai, 18), "j": 1.2}], cor=VERM, lw=16, vel=1.6),
      FL(B5)]
# B4: TDAH é outra coisa (cartão grande)
c += [*CARD(B5 + 0.05, B6, "TDAH", 260, 760, 560, "#ff7a6b", rot=-3, tam=230, cor_txt="#3a0a06"),
      FL(B6)]
# B5-B7: linha da vida: criança, jovem, adulto; a linha da atenção baixa o tempo todo; casa, escola, trabalho
HX = [250, 540, 830]
c += [FIS(B6 + 0.02, AF, [{"k": "cerebro_lado", "xy": [HX[0], 650], "s": 0.42, "t": 0.0}, {"k": "cerebro_lado", "xy": [HX[1], 640], "s": 0.55, "t": 0.35},
                          {"k": "cerebro_lado", "xy": [HX[2], 630], "s": 0.68, "t": 0.7}], z=30,
          pulsos=[{"o": 0, "t": 1.2}, {"o": 1, "t": 1.6}, {"o": 2, "t": 2.0}, {"o": 0, "t": 3.6}, {"o": 1, "t": 3.9}, {"o": 2, "t": 4.2}]),
      FIS(B6 + 0.1, AF, [ROT("CRIANÇA", HX[0], 800, t=0.0), ROT("JOVEM", HX[1], 800, t=0.35), ROT("ADULTO", HX[2], 800, t=0.7)], z=31),
      {"tipo": "texto", "t": round(B6 + 0.2, 3), "d": round(AF - B6 - 0.2, 3), "xy": [100, 865], "w": 880, "fonte": "120px Anton", "cor": TINTA, "alinha": "center",
       "txt": " ", "z": 26, "entra": "mascara", "css": "height:120px;background:rgba(60,179,90,.22);border-top:9px solid #2f8f4a;border-bottom:9px solid #2f8f4a"},
      DS(B6 + 0.3, AF, [{"k": "seta", "de": [110, 1150], "para": [975, 1150], "curva": 0}], cor="#5a4a35", lw=10, vel=0.6),
      DS(b_(30) - 0.1, AF, [{"k": "linha", "pts": [[125 + 835 * j / 24, round(1070 + 14 * math.sin(j * 1.3), 1)] for j in range(25)], "j": 1.2}],
         cor=VERM, lw=16, vel=2.6),
      EMO(b_(33) - 0.05, AF, "🏠", HX[0] - 115, 1205, tam=150), EMO(b_(34) - 0.05, AF, "🏫", HX[1] - 115, 1205, tam=150),
      EMO(b_(35) - 0.05, AF, "💼", HX[2] - 115, 1205, tam=150),
      {"tipo": "carimbo", "t": round(b_(37), 3), "d": round(AF - b_(37), 3), "xy": [150, 1390], "txt": "ATRAPALHA A VIDA", "tam": 104, "rot": -5, "z": 60,
       "blend": "normal", "css": "background:rgba(255,255,255,.93)"}]
SFX_B = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.45, "pico": 0.45}, {"src": "papel", "t": tB + 0.1, "gain": 0.45}, {"src": "boing", "t": b_(2) + 0.1, "gain": 0.3},
         {"src": "boing", "t": B2 + 0.05, "gain": 0.22}, {"src": "boing", "t": B2 + 0.35, "gain": 0.22},
         {"src": "whoosh2", "t": B3, "gain": 0.35}, {"src": "riser", "t": b_(10) - 0.1, "gain": 0.16, "d": 1.4},
         {"src": "whoosh2", "t": B4, "gain": 0.35}, {"src": "boing", "t": b_(18), "gain": 0.25}, {"src": "boing", "t": b_(20), "gain": 0.25},
         {"src": "scratch", "t": b_(22), "gain": 0.25}, {"src": "whoosh", "t": B5, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": B5 + 0.05, "gain": 0.45},
         {"src": "whoosh2", "t": B6, "gain": 0.35}, {"src": "boing", "t": B6 + 0.05, "gain": 0.22}, {"src": "boing", "t": B6 + 0.4, "gain": 0.22},
         {"src": "boing", "t": B6 + 0.75, "gain": 0.22}, {"src": "riser", "t": b_(30) - 0.1, "gain": 0.16, "d": 1.5},
         {"src": "notif", "t": b_(33), "gain": 0.28}, {"src": "notif", "t": b_(34), "gain": 0.28}, {"src": "notif", "t": b_(35), "gain": 0.28},
         {"src": "boom", "t": b_(37), "gain": 0.5, "pico": 0.3, "d": 1.4}]

HC = 980   # quadro mais baixo na C: com o zoom de 1,12 da câmera ele não invade a nota de rodapé
# ================= C (neutro): estudos (mapa-múndi com alfinetes + bolinhas de 100) =================
C3, C4, C5, C6, C7 = round(e_(18) - 0.15, 3), round(e_(27) - 0.15, 3), round(e_(32), 3), round(e_(38) - 0.15, 3), round(e_(46) - 0.15, 3)
PIN = dict(fs=36, stroke="#fff", sw=7, cor_txt="#1b1b1b")
OMS = [([39.0, -98.0], "EUA"), ([19.4, -99.1], "MÉXICO"), ([4.6, -74.1], ""), ([-12.0, -77.0], ""), ([-23.5, -46.6], "BRASIL"),
       ([40.4, -3.7], ""), ([38.7, -9.1], ""), ([48.9, 2.3], ""), ([50.8, 4.4], ""), ([52.1, 5.1], ""), ([52.5, 13.4], ""), ([41.9, 12.5], ""),
       ([44.4, 26.1], ""), ([52.2, 21.0], ""), ([33.9, 35.5], ""), ([33.3, 44.4], ""), ([7.4, 3.9], ""), ([22.5, 114.1], "CHINA"), ([54.6, -5.9], "")]
pinos = []
for k, (ll, txt) in enumerate(OMS):
    pn = dict(ll=ll, t=round(e_(3) + 0.12 * k, 3), txt=txt, **PIN)
    if txt == "BRASIL": pn["cor"] = "#b3121f"
    pinos.append(pn)
MUNDO = [[60, -110], [35, -85], [-34, -58], [-15, -47], [10, -66], [51, 0], [59, 18], [37, -6], [30, 31], [-26, 28], [6, 3], [-1, 37],
         [28, 77], [13, 100], [35, 139], [37, 127], [31, 121], [-6, 107], [-33, 151], [-37, 175], [55, 37], [41, 29], [24, 46], [14, -87]]
c += [GL(AF), FL(AF), SELO(tC + 0.2, CF, "● O QUE AS PESQUISAS GRANDES ACHARAM"),
      # C1-C2 OMS: 20 pesquisas pelo mundo, quase 27 mil adultos
      {"tipo": "mapa", "t": tC, "d": round(C3 - tC + 0.05, 3), "tema": "papel", "area": [50, 490, 980, HC],
       "camera": [[tC, 22, -15, 0.5, 0], [e_(3), 25, -10, 0.56, 4.0]], "pinos": pinos, "z": 20},
      MOLDURA(tC, C3 + 0.05, h=HC),
      TT(tC + 0.02, e_(10) - 0.1, "PESQUISAS DA OMS PELO MUNDO", y=235, fz=112),
      {"tipo": "numero", "t": round(e_(10) - 0.1, 3), "d": round(C3 - e_(10) + 0.1, 3), "xy": [0, 200], "valor": 27, "pre": "QUASE ", "suf": " MIL",
       "tam": 170, "rotulo": "adultos ouvidos", "z": 44},
      RODAPE(tC + 0.2, C3, "Fayyad e col., Atten Defic Hyperact Disord 2017 · 20 pesquisas da OMS · 26.744 adultos"),
      FL(C3),
      # C3-C4 bolinhas de 100: uns 3 têm; e muitos nem sabem
      PAPEL(C3, C5 + 0.05, h=HC),
      FIS(C3 + 0.05, C5 + 0.05, [{"k": "uq_bol100", "xy": [540, 1020], "s": 2.4, "t": 0.0}], z=30),
      FIS(e_(23) - 0.05, C5 + 0.05, [{"k": "uq_bol3", "xy": [540, 1020], "s": 2.4, "t": 0.0}], z=31, pulsos=[{"o": 0, "t": 0.5}, {"o": 0, "t": 1.3}]),
      TT(C3 + 0.02, C4 - 0.03, "UNS 3 EM CADA 100", y=250, fz=135, cor=AMAR),
      DS(e_(28) - 0.05, C5 + 0.05, [{"k": "circulo", "c": [238, 631], "r": [165, 70]}], cor=VERM, lw=14, vel=0.5),
      TT(C4 + 0.02, C5 - 0.03, "E MUITOS NEM SABEM", y=250, fz=135),
      RODAPE(C3, C5, "Fayyad e col., 2017 · TDAH adulto em 2,8% · “pouco reconhecido e pouco tratado”"),
      FL(C5),
      # C5 outro estudo juntou pesquisas do mundo todo
      {"tipo": "mapa", "t": C5, "d": round(C6 - C5 + 0.05, 3), "tema": "papel", "area": [50, 490, 980, HC],
       "camera": [[C5, 15, 10, 0.75, 0], [C5 + 0.3, 15, 10, 0.45, 2.2]],
       "pinos": [dict(ll=ll, t=round(C5 + 0.2 + 0.07 * k, 3), txt="", cor="#2a6df4", **PIN) for k, ll in enumerate(MUNDO)], "z": 20},
      MOLDURA(C5, C6 + 0.05, h=HC),
      TT(C5 + 0.02, C6 - 0.03, "OUTRO ESTUDO: O\u00a0MUNDO\u00a0TODO", y=235, fz=118),
      RODAPE(C5, C6, "Song e col., J Glob Health 2021 · revisão de estudos com adultos do mundo todo"),
      FL(C6),
      # C6 com algum sintoma: uns 7 em 100
      PAPEL(C6, CF, h=HC),
      FIS(C6 + 0.05, CF, [{"k": "uq_bol100", "xy": [540, 1020], "s": 2.4, "t": 0.0}], z=30),
      FIS(e_(42) - 0.05, C7, [{"k": "uq_bol7", "xy": [540, 1020], "s": 2.4, "t": 0.0}], z=31, pulsos=[{"o": 0, "t": 0.5}]),
      TT(C6 + 0.02, C7 - 0.03, "COM ALGUM SINTOMA: 7 EM 100", y=235, fz=118, cor=AMAR),
      # C7 o TDAH que vem desde criança: menos de 3
      FIS(e_(53) - 0.1, CF, [{"k": "uq_bol2m", "xy": [540, 1020], "s": 2.4, "t": 0.0}], z=31, pulsos=[{"o": 0, "t": 0.5}]),
      TT(C7 + 0.02, CF, "O TDAH QUE VEM DESDE CRIANÇA", y=235, fz=118, cor=VERM),
      PILULA(e_(53) - 0.12, CF, "MENOS DE 3", y=1300, cor="#ffffff", cor_txt="#b3121f", x=240, w=600, tam=130),
      RODAPE(C6, CF, "Song e col., J Glob Health 2021 · com algum sintoma 6,76% · desde a infância 2,58%")]
SFX_C = [{"src": "pagina", "t": tC + 0.05, "gain": 0.5}, {"src": "whoosh2", "t": e_(3), "gain": 0.3},
         *[{"src": "boing", "t": round(e_(3) + 0.12 * k, 3), "gain": 0.12} for k in range(0, 19, 3)],
         {"src": "riser", "t": e_(10) - 1.0, "gain": 0.18, "d": 1.1}, {"src": "boom", "t": e_(10) - 0.05, "gain": 0.45, "pico": 0.3, "d": 1.3},
         {"src": "whoosh2", "t": C3, "gain": 0.35}, {"src": "papel", "t": C3 + 0.05, "gain": 0.4}, {"src": "boing", "t": e_(23), "gain": 0.35},
         {"src": "scratch", "t": e_(28), "gain": 0.28}, {"src": "whoosh", "t": C5, "gain": 0.4, "pico": 0.45},
         *[{"src": "boing", "t": round(C5 + 0.2 + 0.07 * k, 3), "gain": 0.1} for k in range(0, 24, 4)],
         {"src": "whoosh2", "t": C6, "gain": 0.35}, {"src": "papel", "t": C6 + 0.05, "gain": 0.4}, {"src": "boing", "t": e_(42), "gain": 0.35},
         {"src": "whoosh2", "t": C7, "gain": 0.3}, {"src": "boom", "t": e_(53) - 0.1, "gain": 0.45, "pico": 0.3, "d": 1.3}]

# ================= F (manso): desconfiou? não decide sozinho; conversa com o médico =================
F2, F3 = round(tF + 1.56, 3), round(f_(9) - 0.15, 3)
c += [GL(CF + 0.1), FL(CF + 0.1),
      GIG(tF, F2, "DESCONFIOU", y=1300, tam=400, cont=True),
      TT(tF + 0.02, F2, "DESCONFIOU?", y=300, fz=170, cor=AMAR, anim=None, entra="zoom"),
      EMO(tF + 0.1, F3, "🤔", 395, 700, tam=230),
      TT(F2, F3 - 0.03, "NÃO DECIDE SOZINHO", y=300, fz=135),
      {"tipo": "texto", "t": round(tF + 2.2, 3), "d": round(F3 - tF - 2.2, 3), "xy": [100, 1100], "w": 820, "fonte": "700 84px Montserrat", "cor": "#111",
       "alinha": "left", "txt": "🔍 teste de TDAH", "anim": "digita", "vel": 0.03, "z": 44,
       "css": "white-space:nowrap;background:#ffffff;border-radius:60px;padding:30px 30px;box-shadow:0 20px 50px rgba(0,0,0,.5)"},
      DS(f_(8) - 0.1, F3, [{"k": "x", "c": [540, 1165], "s": 120}], cor=VERM, lw=24),
      FL(F3),
      PAPEL(F3, FF),
      TT(F3 + 0.02, FF, "NA CONSULTA:", y=270, fz=150, cor=AMAR),
      *CARD(f_(9), FF, "CONVERSA COM\\nO SEU MÉDICO", 110, 640, 860, "#9be3a8", rot=-2, tam=110),
      *CARD(f_(14), FF, "CONTA COMO ERA\\nNA ESCOLA", 110, 1040, 860, "#fff27a", rot=2, tam=110),
      FIS(f_(18), FF, [{"k": "cf_livro", "xy": [880, 1420], "s": 0.5, "t": 0.0}], z=40, pulsos=[{"o": 0, "t": 0.4}])]
SFX_F = [{"src": "whoosh", "t": tF, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": tF + 0.15, "gain": 0.3}, {"src": "whoosh2", "t": F2, "gain": 0.3},
         {"src": "teclado", "t": tF + 2.25, "gain": 0.3, "d": 0.8}, {"src": "scratch", "t": f_(8) - 0.05, "gain": 0.3},
         {"src": "whoosh2", "t": F3, "gain": 0.35}, {"src": "papel", "t": f_(9), "gain": 0.45}, {"src": "papel", "t": f_(14), "gain": 0.45},
         {"src": "boing", "t": f_(18), "gain": 0.25}]

# ================= E (alegre): cobrança leve =================
E2 = round(q_(6) - 0.15, 3)
c += [GL(FF + 0.1), FL(FF + 0.1),
      TT(tE + 0.02, E2 - 0.03, "1 EM 4 DESCONFIA", y=300, fz=150),
      FIS(tE + 0.1, E2, [{"k": "jp_pessoa", "xy": [180, 1050], "s": 0.75, "t": 0.0}, {"k": "jp_pessoa", "xy": [420, 1050], "s": 0.75, "t": 0.12},
                        {"k": "jp_pessoa", "xy": [660, 1050], "s": 0.75, "t": 0.24}, {"k": "jp_pessoa", "xy": [900, 1050], "s": 0.75, "t": 0.36}],
          pulsos=[{"o": 2, "t": 1.9}, {"o": 2, "t": 2.6}]),
      EMO(q_(4) - 0.1, E2, "🤔", 545, 720, tam=150),
      FL(E2),
      TT(E2 + 0.02, EF, "SEGUIR? DISSO EU NÃO DESCONFIO 😉", y=280, fz=125, cor=AMAR),
      {"tipo": "texto", "t": round(E2 + 0.1, 3), "d": round(EF - E2 - 0.1, 3), "xy": [240, 960], "w": 600, "fonte": "900 120px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": "Seguir", "z": 44, "entra": "pop", "css": "background:#0095f6;border-radius:34px;padding:26px 0;box-shadow:0 20px 50px rgba(0,0,0,.5)"},
      DS(q_(10) - 0.05, EF, [{"k": "circulo", "c": [540, 1045], "r": [370, 150]}], cor=AMAR, lw=14, vel=0.5),
      EMO(q_(12) - 0.1, EF, "👆", 425, 1240, tam=170)]
SFX_E = [{"src": "whoosh2", "t": tE, "gain": 0.35}, *[{"src": "boing", "t": round(tE + 0.1 + 0.12 * k, 3), "gain": 0.18} for k in range(4)],
         {"src": "boing", "t": q_(4) - 0.1, "gain": 0.3}, {"src": "whoosh", "t": E2, "gain": 0.4, "pico": 0.45}, {"src": "notif", "t": E2 + 0.1, "gain": 0.35},
         {"src": "scratch", "t": q_(10) - 0.05, "gain": 0.25}, {"src": "boing", "t": q_(12) - 0.1, "gain": 0.3}]

# ================= CTA (banco cta6_serio) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": 3.01, "ms": 0, "src": M + "uq_cta.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 1.8, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 2.76, "y": 215, "txt": "TE AJUDOU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (neutro): fecho =================
D2 = round(d_(4) - 0.15, 3)
c += [GL(c2), FL(c2),
      GIG(c2, D2, "DISTRAÇÃO", y=1300, tam=420),
      TT(c2 + 0.03, D2, "DISTRAÇÃO: TODO\u00a0MUNDO\u00a0TEM", y=320, fz=140, cor="#ffffff"),
      FL(D2),
      TT(D2 + 0.02, dur, "TRANSTORNO: SÓ\u00a0A\u00a0AVALIAÇÃO\u00a0DIZ", y=300, fz=130, cor=AMAR),
      {"tipo": "carimbo", "t": round(D2 + 0.4, 3), "d": round(dur - D2 - 0.4, 3), "xy": [255, 860], "txt": "VERDADE", "tam": 150, "rot": -6, "z": 60,
       "cor": "#14964a", "blend": "normal", "css": "background:rgba(255,255,255,.93)"},
      PILULA(d_(5), dur, "DESCONFIAR\\nNÃO É TER", y=1170, cor="#ffffff", cor_txt="#14070a", x=170, w=740, tam=110),
      RODAPE(c2, dur, "Fayyad 2017 doi 10.1007/s12402-016-0208-3 · Song 2021 doi 10.7189/jogh.11.04009 · Conteúdo educativo", y=1560)]
SFX_D = [{"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": c2 + 0.05, "gain": 0.4, "pico": 0.45},
         {"src": "whoosh2", "t": D2, "gain": 0.35}, {"src": "boom", "t": D2 + 0.4, "gain": 0.5, "pico": 0.3, "d": 1.5}, {"src": "notif", "t": d_(5), "gain": 0.3}]

voz = [{"src": M + "uq_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "uq_viral.words.json", "gain": 0.16},
       {"src": M + "uq_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "uq_r1.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "uq_r1.words.json"},
       {"src": M + "uq_i_voz.wav", "t": tI, "ms": 0, "d": DI, "palavras": M + "uq_i_voz.words.json"},
       {"src": M + "uq_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "uq_b_voz.words.json"},
       {"src": M + "uq_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "uq_c_voz.words.json"},
       {"src": M + "uq_f_voz.wav", "t": tF, "ms": 0, "d": DF, "palavras": M + "uq_f_voz.words.json"},
       {"src": M + "uq_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "uq_e_voz.words.json"},
       {"src": M + "uq_cta.mp4", "t": c1, "ms": 0, "d": 3.01, "palavras": M + "uq_cta.words.json"},
       {"src": M + "uq_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "uq_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35}, {"src": "whoosh2", "t": 6.45, "gain": 0.25},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.45, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, *SFX_I,
       {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_B,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, *SFX_C,
       {"src": "glitch", "t": CF + 0.05, "gain": 0.4}, *SFX_F,
       {"src": "glitch", "t": FF + 0.05, "gain": 0.4}, *SFX_E,
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, *SFX_D]
for L in c:
    if vd <= L.get("t", 0) < c1 - 0.06: L["fixo"] = True
salvar(PID, dur, 414, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, dur, 1700]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": round(r1 - 0.3, 2), "d": round(tE - r1 + 0.6, 2), "gain": 0.16, "fade": 0.8},
                        {"src": "m_humor", "t": round(tE - 0.3, 2), "d": round(c1 - tE + 0.6, 2), "gain": 0.13, "fade": 0.6},
                        {"src": "m_emocao", "t": round(c2 - 0.2, 2), "d": round(dur - c2 + 0.2, 2), "gain": 0.15, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tI", tI, "tB", tB, "AF", AF, "tC", tC, "tF", tF, "tE", tE, "c1", c1, "c2", c2, "tD", tD)
if '--sem-pos' not in sys.argv:
    subprocess.run(["python3", "scripts/entrada.py", PID, M + "uq_ent.mp4", M + "uq_ent.mp4.words.json", "2.07",
                    "1 EM 4 ACHA QUE TEM TDAH?", "o que as pesquisas grandes dizem"], check=True)
    subprocess.run(["python3", "scripts/pele.py", PID, "noticia"], check=True)
    p = json.load(open(f'planos/{PID}.json'))
    p['legenda']['estilo'] = 'serif'          # Mapeamento: legenda serifada palavra a palavra
    json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
