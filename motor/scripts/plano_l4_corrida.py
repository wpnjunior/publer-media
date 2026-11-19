# plano_l4_corrida.py (14/11, lote 4, Fertilidade a Dois): "a contagem de espermatozoides está caindo?"
# Viral: notícia do Daily Mail no TikTok (campeonato de corrida de espermatozoides), em inglês, dublada pela Murilo
# (original a 0,16 por baixo). Trecho A 0,00-4,56 "The sperm race is back and this year there's $100,000 up for grabs."
# + trecho B 25,50-32,62 "The event began as a creative way to highlight declining global sperm counts and promote
# awareness of male reproductive health." -> VERDADE, COM PORÉM.
# No B o vídeo original mostra uma montagem de famosos em podcast: o cartão usa SÓ imagens do evento (print da matéria
# 25,50-26,85 + pista do evento 16,50-22,27) por baixo do áudio do B; nada de rosto de famoso (tmp_ce/, ce_viral.mp4).
# Entrada de notícia do banco (rk_ent "Olha só essa notícia", 6cd9) + manchete; CTA cta6 do banco.
# Rosto r1 novo (6cd9): "Parece piada. Mas a queda é de verdade." com o áudio do bloco neutro.
# Voz: 3 create_speech por clima, SEM atempo e SEM <break> (pausas abertas na edição, tmp_ce/voz.py):
#   neutro (r1 + estudo + fecho) | manso (aula + o que fazer) | alegre (abertura + cobrança).
# EDIÇÃO DA AULA: MAPEAMENTO em papel antigo (planta vista de cima, etiquetas com fita, legenda serifada palavra a
# palavra, troca a cada 2-4 s): testiculo_corte = fábrica (dn_fabrica), gota_espermatozoides com a contagem um a um,
# estádio visto de cima com a torcida saindo em ondas (estadio + estadio_torcida_1..6) e a arquibancada quase vazia.
# O estudo também é Mapeamento: mapa em papel com o pino de Copenhague (1992), pinos nos continentes (223 estudos) e
# gráfico desenhado (queda de 51,6% e a linha de referência de 16 milhões/ml).
# Pele: papel antigo (mapeamento) na narração, sem pele.py; legenda serifada (global) com faixa escura por baixo no papel.
# Depois deste script (ele mesmo roda): entrada.py com rk_ent.
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
from PIL import ImageFont
PID = 'react_l4_corrida'; P = 'ce'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
DA, DE, DB, DO, DC, DD = [round(dur_de(f'{M}ce_{k}_voz.wav'), 3) for k in 'aebocd']
vd = 11.68                                # ce_viral.mp4 (4,56 + 7,12)
r1 = round(vd + 3.027 + 0.5, 2)           # ce_r1: "verdade." termina em 3,03 s; 0,5 s de folga
tA = round(r1 + 0.15, 2)                  # abertura (alegre)
tB = round(tA + DA + 0.7, 2)              # aula (manso)
tC = round(tB + DB + 0.75, 2)             # estudo (neutro)
tO = round(tC + DC + 0.7, 2)              # o que fazer (manso)
tE = round(tO + DO + 0.6, 2)              # cobrança (alegre)
c1 = round(tE + DE + 0.15, 2)             # CTA 6cd9 (banco cta6, 4,12 s)
c2 = round(c1 + 4.12, 2)                  # fecho (neutro)
dur = round(c2 + DD + 0.6, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3)
o = lambda v: round(tO + v, 3); k_ = lambda v: round(tE + v, 3); f = lambda v: round(c2 + v, 3)
INK, VERM, AZUL, VERDE, OURO = '#1c1a17', '#b3121f', '#1f5fa8', '#2e7d32', '#9a6400'
SP = "text-shadow:5px 5px 0 rgba(0,0,0,.14)"
SH = "text-shadow:8px 8px 0 #000,0 0 18px rgba(0,0,0,.8)"
ANTON = ImageFont.truetype('assets/fonts/Anton-Regular.ttf', 100)

def TT(t, d, txt, y=250, fz=120, cor=INK, vel=0.09, **kw):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SP, vel=vel, **kw); L['fixo'] = True; return L
def TD(t, d, txt, y=470, fz=120, cor='#ffffff', **kw):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SH, vel=0.09, **kw); L['fixo'] = True; return L
def ETQ(t, d, txt, cx, y, rot=-4, cor=INK, fz=100):
    """etiqueta de papel presa com fita (Mapeamento)."""
    w = int(ANTON.getlength(txt) * fz / 100) + 80
    x = int(cx - w / 2)
    card = {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"{fz}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 56, "entra": "cai", "rot": rot, "fixo": True,
            "css": "background:#fffaf0;border:5px solid #1c1a17;border-radius:6px;padding:6px 0 0;box-shadow:9px 11px 0 rgba(0,0,0,.18);letter-spacing:2px"}
    fita = {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [int(cx - 75), y - 26], "w": 150, "fonte": "100px Anton", "cor": INK,
            "alinha": "center", "txt": " ", "z": 57, "entra": "cai", "rot": rot - 5, "fixo": True,
            "css": "height:46px;overflow:hidden;background:rgba(226,203,120,.82);box-shadow:0 2px 4px rgba(0,0,0,.15)"}
    return [card, fita]
def F2(t, d, txt, y=1462):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, y], "w": 1000, "fonte": "700 28px Montserrat", "cor": INK,
            "alinha": "center", "txt": txt, "z": 70, "fixo": True, "css": "background:rgba(255,250,235,.88);border-radius:12px;padding:6px 10px"}
def FS(t, d, orgaos, z=30, **kw):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": True, "cor_rotulo": INK}; L.update(kw); return L
def DW(t, d, formas, cor=VERM, esp=12, vel=0.45, z=45):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "espessura": esp, "cor": cor, "vel": vel, "z": z, "fixo": True}
def CAR(t, d, txt, xy, tam=130, rot=-8, cor=VERM):
    return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": 60, "cor": cor,
            "blend": "normal", "css": "background:rgba(255,250,235,.92)", "fixo": True}
def GIG(t, d, txt, y=1180, tam=420):
    return {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": "rgba(28,26,23,.07)",
            "x": [700, -int(len(txt) * tam * 0.5)], "z": 12, "fixo": True}
def PAPEL(t, d):
    return {"tipo": "fundo", "t": round(t, 3), "d": round(d, 3), "cor": "#efe4c9", "textura": "papel", "z": 2, "fixo": True}
def VEU(t, d, op=0.5, z=4):
    return {"tipo": "fundo", "t": round(t, 3), "d": round(d, 3), "cor": f"rgba(239,228,201,{op})", "z": z, "fixo": True}
def FAIXA(t, d):
    # faixa escura suave por baixo da legenda serifada branca (a legenda não some no papel claro)
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [0, 1590], "w": 1080, "fonte": "100px Anton", "cor": "#fff",
            "alinha": "center", "txt": " ", "z": 86, "entra": "nada", "fixo": True,
            "css": "height:250px;overflow:hidden;background:linear-gradient(180deg,rgba(28,20,12,0) 0%,rgba(28,20,12,.66) 28%,rgba(28,20,12,.66) 72%,rgba(28,20,12,0) 100%)"}
FL = lambda t, mx=0.35: {"tipo": "flash", "t": round(t, 2), "d": 0.22, "max": mx}
PIN = dict(fs=36, stroke="#fff", sw=8, cor_txt=INK)
MUNDO = [[40, -100], [45, -75], [-15, -50], [-34, -60], [52, 10], [45, 2], [60, 15], [5, 20], [-25, 25], [30, 31],
         [35, 105], [21, 78], [36, 138], [55, 80], [-25, 135], [32, 50]]

# ================= viral em tela dividida + caixinha =================
c = abertura(P, vd, "via @dailymail", "center", "Mito ou verdade? 👇", "A contagem de espermatozoides está caindo?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 3.4, "dec": 1, "suf": " MI DE VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta": L["escolha"] = 1
# r1: rosto embaixo, foto do viral em cima com a resposta grande
c += [{"tipo": "video", "t": vd, "d": round(r1 - vd, 2), "ms": 0, "src": M + "ce_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45},
      TD(vd + 0.05, round(r1 - vd - 0.05, 2), "VERDADE", y=400, fz=160, cor="#f2c230", anim=None, entra="zoom"),
      TD(vd + 1.1, round(r1 - vd - 1.1, 2), "A QUEDA É REAL", y=640, fz=115, cor="#3ddc84")]
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1, 0.6), PAPEL(r1, c1 - r1), FAIXA(r1, c1 - r1)]

# ================= ABERTURA (alegre): caiu no mundo todo, mas caiu = infértil? Não. =================
c += [{"tipo": "mapa", "t": r1, "d": round(tB - r1, 2), "tema": "papel", "area": [0, 560, 1080, 900],
       "camera": [[r1, 30, 15, 0.95, 0], [a(1.6), 15, 10, 0.58, 1.4]],
       "pinos": [dict(ll=ll, t=a(1.75 + 0.06 * i), txt="", **PIN) for i, ll in enumerate(MUNDO)], "z": 3, "fixo": True},
      VEU(r1, tB - r1, 0.38),
      TT(a(0.05), 3.0, "A CONTAGEM CAIU NO MUNDO TODO", y=250, fz=125, vel=0.37),
      DW(a(2.2), 0.9, [{"k": "seta", "de": [150, 640], "para": [930, 1180], "curva": -40}], esp=16, vel=0.6),
      FL(a(3.05)), TT(a(3.07), 2.4, "CAIU = INFÉRTIL?", y=330, fz=150),
      FS(a(3.07), 2.4, [{"k": "gota_espermatozoides", "xy": [540, 1050], "s": 1.25, "t": 0.1}]),
      CAR(a(5.48), round(tB - a(5.48) - 0.05, 2), "NÃO", [300, 900], tam=300, rot=-9)]

# ================= AULA (manso), MAPEAMENTO em papel antigo =================
c += [{"tipo": "glitch", "t": tB - 0.05, "d": 0.2}, FL(tB)]
# S1 0-2,85: o testículo é uma fábrica que não para
c += [TT(b(0.1), 2.75, "TESTÍCULO = FÁBRICA", y=240, fz=125),
      FS(b(0.05), 2.8, [{"k": "testiculo_corte", "xy": [300, 1010], "s": 1.05, "t": 0.05},
                        {"k": "dn_fabrica", "xy": [810, 1030], "s": 0.85, "t": 1.0}],
         fluxos=[{"de": [345, 1015], "para": [490, 780], "curva": -40, "cor": "#ffffff", "t": 0.4, "d": 2.35, "n": 12, "r": 15, "viagem": 0.9, "fica": True}],
         pulsos=[{"o": 1, "t": 1.5}]),
      {"tipo": "texto", "t": b(1.0), "d": 1.85, "xy": [500, 900], "w": 110, "fonte": "160px Anton", "cor": VERM, "alinha": "center", "txt": "=", "z": 40, "fixo": True, "css": SP},
      *ETQ(b(1.3), 1.55, "NÃO PARA", 540, 1330, rot=-4, cor=VERM),
      GIG(b(0.05), 2.8, "FÁBRICA", y=1480, tam=360)]
# S2a 2,85-5,3: o exame conta quantos espermatozoides
gp = json.load(open('tmp_ce/gota_pos.json')); GS, GX, GY = 1.75, 540, 1010
circ = [{"k": "circulo", "c": [round(GX + x * GS), round(GY + y * GS)], "r": [34, 28], "t": round(0.75 + 0.27 * j, 2)} for j, (x, y, _) in enumerate(sorted(gp, key=lambda q: (q[1], q[0])))]
c += [FL(b(2.85)),
      TT(b(2.9), 2.4, "O EXAME CONTA", y=240, fz=135),
      FS(b(2.85), 2.45, [{"k": "gota_espermatozoides", "xy": [GX, GY], "s": GS, "t": 0.05}]),
      DW(b(2.85), 2.45, circ, cor=VERM, esp=8, vel=0.22),
      *ETQ(b(3.6), 1.7, "ESPERMOGRAMA", 540, 1395, rot=3, cor=AZUL)]
# S2b 5,3-7,45: em cada mililitro
c += [FL(b(5.3)),
      TT(b(5.35), 2.1, "EM CADA MILILITRO", y=240, fz=125),
      FS(b(5.3), 2.15, [{"k": "gota_espermatozoides", "xy": [540, 1060], "s": 2.15, "t": 0.0}]),
      CAR(b(5.95), 1.5, "1 ML", [610, 1290], tam=150, rot=-10, cor=AZUL)]
# S3a 7,45-10,1: pensa num estádio: o público caiu (a torcida sai em 3 ondas)
ES, EX, EY = 2.05, 540, 1030
base = lambda g: {"k": g, "xy": [EX, EY], "s": ES, "t": 0.05}
c += [FL(b(7.45)),
      TT(b(7.5), 2.6, "O PÚBLICO CAIU", y=240, fz=140),
      FS(b(7.45), 4.45, [base("estadio"), base("estadio_torcida_4"), base("estadio_torcida_5"), base("estadio_torcida_6")], z=30),
      FS(b(7.45), 1.65, [base("estadio_torcida_1")], z=31),
      FS(b(7.45), 1.95, [base("estadio_torcida_2")], z=32),
      FS(b(7.45), 2.25, [base("estadio_torcida_3")], z=33),
      GIG(b(7.5), 4.35, "ESTÁDIO", y=1500, tam=360)]
# S3b 10,1-11,9: mas ainda tem jogo
c += [TT(b(10.05), 1.85, "AINDA TEM JOGO", y=240, fz=140, cor=VERDE),
      DW(b(10.6), 1.3, [{"k": "check", "c": [880, 560], "s": 60}], cor=VERDE, esp=16)]
# S4 11,9-15,8: o problema é a arquibancada quase vazia (zoom na arquibancada; sai o resto da torcida)
ZS, ZX, ZY = 3.3, 760, 1260
zb = lambda g: {"k": g, "xy": [ZX, ZY], "s": ZS, "t": 0.0}
s4 = round(tC - b(11.9) - 0.05, 2)
c += [FL(b(11.9)),
      TT(b(11.95), round(s4 - 0.05, 2), "O PROBLEMA: QUASE VAZIA", y=240, fz=125, vel=0.6),
      FS(b(11.9), s4, [zb("estadio"), zb("estadio_torcida_6")], z=30),
      FS(b(11.9), 1.2, [zb("estadio_torcida_4")], z=31),
      FS(b(11.9), 1.6, [zb("estadio_torcida_5")], z=32),
      CAR(b(14.3), round(s4 - 2.4, 2), "INVESTIGAR", [160, 1290], tam=125, rot=-7)]

# ================= ESTUDO (neutro): mapa + gráfico =================
c += [{"tipo": "glitch", "t": tC - 0.05, "d": 0.2}, FL(tC)]
cph = [55.68, 12.57]
c += [{"tipo": "mapa", "t": tC, "d": 15.5, "tema": "papel", "area": [0, 480, 1080, 1000],
       "camera": [[tC, 30, 10, 0.62, 0], [e(1.4), 55.0, 19.5, 3.6, 1.8], [e(4.85), 37.0, 19.5, 3.6, 0.7], [e(10.9), 15, 10, 0.58, 1.4]],
       "pinos": [dict(ll=cph, t=e(4.25), txt="COPENHAGUE", cor=VERM, fs=17, stroke="#fff", sw=4, cor_txt=INK)] +
                [dict(ll=ll, t=e(13.2 + 0.07 * i), txt="", **PIN) for i, ll in enumerate(MUNDO)],
       "z": 3, "fixo": True},
      TT(e(0.05), 4.8, "1992", y=230, fz=210, cor=VERM, anim=None, entra="zoom")]
# E2 4,9-10,9: a média caiu de 113 para 66 milhões por ml (manchete de jornal antigo)
c += [FL(e(4.9)), VEU(e(4.9), 6.0, 0.82),
      {"tipo": "manchete", "t": e(4.9), "d": 6.0, "xy": [60, 230], "w": 960, "jornal": "BMJ · Copenhague", "data": "1992",
       "txt": "A média de espermatozoides caiu", "sub": "61 estudos, quase 15 mil homens, de 1940 a 1990", "rot": -2, "z": 40, "fixo": True},
      {"tipo": "numero", "t": e(6.1), "d": 4.8, "xy": [0, 700], "valor": 66, "de": 113, "conta": 1.9, "tam": 330, "cor": VERM, "sombra": "#d9c49a",
       "rotulo": "milhões por ml", "cor_rotulo": INK, "sombra_rotulo": "none", "z": 44, "fixo": True},
      TT(e(9.0), 1.9, "EM 50 ANOS", y=1295, fz=120),
      F2(e(4.9), 6.0, "Carlsen e col., BMJ 1992 · média de 113 para 66 milhões/ml (1940-1990)")]
# E3 10,9-15,5: 2023, 223 estudos, no mundo todo
c += [FL(e(10.9)),
      TT(e(10.95), 4.55, "2023", y=230, fz=210, cor=VERM, anim=None, entra="zoom"),
      {"tipo": "numero", "t": e(13.1), "d": 2.4, "xy": [0, 960], "valor": 223, "tam": 260, "cor": VERM, "sombra": "#d9c49a",
       "rotulo": "estudos", "cor_rotulo": INK, "sombra_rotulo": "none", "z": 44, "fixo": True},
      F2(e(10.95), 4.55, "Levine e col., Hum Reprod Update 2023 · 223 estudos, amostras de 1973 a 2018")]
# E4 15,5-19,25: em 45 anos, caiu mais da metade (gráfico desenhado)
X0, X1, YB = 175, 935, 1130
yv = lambda v: round(YB - v / 110 * 470)
vals = [101, 100, 97, 94, 91, 88, 84, 80, 74, 66, 58, 52, 49]
curva = [[round(X0 + (X1 - X0) * i / (len(vals) - 1)), yv(v)] for i, v in enumerate(vals)]
gtab = round(tO - e(15.5) - 0.05, 2)
c += [FL(e(15.5)),
      {"tipo": "cartao", "t": e(15.5), "d": gtab, "box": [80, 560, 920, 640], "aba": "contagem média no mundo", "entra": "pop", "z": 30, "fixo": True},
      DW(e(15.6), round(gtab - 0.1, 2), [{"k": "linha", "pts": [[150, 615], [150, YB], [960, YB]], "j": 2}], cor=INK, esp=7, vel=0.4, z=35),
      DW(e(16.0), round(gtab - 0.5, 2), [{"k": "linha", "pts": curva, "j": 2}], cor=VERM, esp=14, vel=2.2, z=36),
      {"tipo": "texto", "t": e(15.7), "d": round(gtab - 0.2, 2), "xy": [95, YB + 12], "w": 160, "fonte": "800 32px Montserrat", "cor": INK, "alinha": "center", "txt": "1973", "z": 37, "fixo": True},
      {"tipo": "texto", "t": e(15.7), "d": round(gtab - 0.2, 2), "xy": [855, YB + 12], "w": 160, "fonte": "800 32px Montserrat", "cor": INK, "alinha": "center", "txt": "2018", "z": 37, "fixo": True},
      TT(e(15.55), 3.7, "EM 45 ANOS, CAIU MAIS DA METADE", y=230, fz=115, vel=0.42),
      {"tipo": "numero", "t": e(17.4), "d": 1.85, "xy": [0, 1190], "valor": 51.6, "dec": 1, "pre": "-", "suf": "%", "tam": 190, "cor": VERM, "sombra": "#d9c49a", "z": 44, "fixo": True},
      F2(e(15.55), 3.7, "Levine e col., Hum Reprod Update 2023 · queda de 51,6% na concentração média")]
# E5 19,25-fim: a linha de referência do exame: 16 milhões/ml (valor de referência, não linha de corte)
y16 = yv(16)
traco = [{"k": "linha", "pts": [[x, y16], [x + 34, y16]], "j": 1, "t": round(0.04 * i, 2)} for i, x in enumerate(range(X0, X1, 56))]
c += [FL(e(19.25), 0.25),
      TT(e(19.3), round(tO - e(19.3) - 0.05, 2), "VALOR DE REFERÊNCIA DO EXAME", y=230, fz=115, vel=0.25),
      DW(e(20.5), round(tO - e(20.5) - 0.05, 2), traco, cor=AZUL, esp=10, vel=0.25, z=38),
      {"tipo": "texto", "t": e(21.6), "d": round(tO - e(21.6) - 0.05, 2), "xy": [175, y16 - 120], "w": 700, "fonte": "100px Anton", "cor": AZUL,
       "alinha": "left", "txt": "16 MILHÕES/ML", "z": 40, "entra": "desliza", "dy": 40, "fixo": True, "css": "text-shadow:4px 4px 0 rgba(255,250,235,.9)"},
      F2(e(19.3), round(tO - e(19.3) - 0.05, 2), "Campbell e col., Andrology 2021 (OMS) · 16 milhões/ml é referência, não linha de corte")]

# ================= O QUE FAZER (manso): vocês dois, espermograma dele, consulta a dois =================
c += [{"tipo": "glitch", "t": tO - 0.05, "d": 0.2}, FL(tO)]
c += [FS(o(0.05), 4.9, [{"k": "coracao_afeto", "xy": [420, 1030], "s": 0.95, "t": 0.1}, {"k": "coracao_afeto", "xy": [660, 1060], "s": 0.95, "t": 0.45}],
         pulsos=[{"o": 0, "t": 1.1}, {"o": 1, "t": 1.55}]),
      TT(o(1.0), 3.95, "VOCÊS DOIS: A MÉDIA NÃO DECIDE", y=240, fz=125, vel=0.5),
      FL(o(4.95)),
      FS(o(4.95), 4.6, [{"k": "gota_espermatozoides", "xy": [540, 1020], "s": 1.45, "t": 0.1}]),
      TT(o(5.5), 2.1, "ESPERMOGRAMA DELE", y=240, fz=130, cor=AZUL),
      TT(o(7.6), 1.95, "EXAME SIMPLES", y=240, fz=140, cor=VERDE),
      DW(o(8.6), 0.95, [{"k": "check", "c": [800, 1250], "s": 70}], cor=VERDE, esp=18),
      FL(o(9.6)),
      FS(o(9.6), round(tE - o(9.6) - 0.05, 2), [{"k": "calendario", "xy": [540, 1000], "s": 1.35, "t": 0.1},
                                                {"k": "coracao_afeto", "xy": [250, 1250], "s": 0.55, "t": 0.6}, {"k": "coracao_afeto", "xy": [830, 1250], "s": 0.55, "t": 0.8}]),
      TT(o(9.9), round(tE - o(9.9) - 0.05, 2), "CONSULTA COM OS DOIS JUNTOS", y=240, fz=125, vel=0.3)]

# ================= COBRANÇA (alegre) =================
c += [FL(tE),
      {"tipo": "foto", "t": k_(0.0), "d": round(c1 - tE, 2), "src": M + "ce_still.jpg", "box": [150, 700, 780, 760], "raio": 6, "rot": -2,
       "borda": "border:18px solid #fffaf0;", "credito": "via @dailymail", "entra": "cai", "z": 30, "fixo": True, "kb": {"s": [1.0, 1.1]}},
      TT(k_(0.05), round(c1 - tE - 0.05, 2), "QUEM NÃO SEGUIR VAI EXPLICAR PRO SOGRO", y=230, fz=115, vel=0.33)]

# ================= CTA (6cd9) + fecho =================
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]
c += [{"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2, 0.5), PAPEL(c2, dur - c2), FAIXA(c2, dur - c2),
      {"tipo": "mapa", "t": c2, "d": round(dur - c2, 2), "tema": "papel", "area": [0, 560, 1080, 900],
       "camera": [[c2, 20, 10, 0.6, 0], [f(2.0), 20, 10, 0.66, 3.0]],
       "pinos": [dict(ll=ll, t=f(0.1 + 0.04 * i), txt="", **PIN) for i, ll in enumerate(MUNDO)], "z": 3, "fixo": True},
      VEU(c2, dur - c2, 0.45),
      TT(f(0.05), round(dur - c2 - 0.05, 2), "A MÉDIA CAIU. A RESPOSTA ESTÁ NO EXAME", y=230, fz=115, vel=0.45),
      CAR(f(1.0), round(dur - c2 - 1.0, 2), "VERDADE, COM PORÉM", [80, 990], tam=84, rot=-6),
      F2(f(0.05), round(dur - c2 - 0.05, 2), "Levine e col., Hum Reprod Update 2023 · doi 10.1093/humupd/dmac035")]

voz = [{"src": M + "ce_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "ce_viral.words.json", "gain": 0.16},
       {"src": M + "ce_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "ce_r1.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "ce_r1.words.json"},
       {"src": M + "ce_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "ce_a_voz.words.json"},
       {"src": M + "ce_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "ce_b_voz.words.json"},
       {"src": M + "ce_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "ce_c_voz.words.json"},
       {"src": M + "ce_o_voz.wav", "t": tO, "ms": 0, "d": DO, "palavras": M + "ce_o_voz.words.json"},
       {"src": M + "ce_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "ce_e_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "ce_d_voz.wav", "t": c2, "ms": 0, "d": DD, "palavras": M + "ce_d_voz.words.json"}]
musica = [{"src": "m_investiga", "t": round(r1 - 0.1, 2), "ms": 0, "d": round(min(22.9, tC + 0.4 - r1), 2), "gain": 0.17, "fade": 0.8},
          {"src": "m_viagem", "t": round(tC - 0.45, 2), "ms": 0, "d": round(tO + 0.4 - tC + 0.45, 2), "gain": 0.16, "fade": 0.8},
          {"src": "m_emocao", "t": round(tO - 0.4, 2), "ms": 0, "d": round(tE + 0.3 - tO + 0.4, 2), "gain": 0.16, "fade": 0.8},
          {"src": "m_humor", "t": round(tE - 0.3, 2), "ms": 0, "d": round(c1 + 0.3 - tE + 0.3, 2), "gain": 0.17, "fade": 0.5},
          {"src": "m_noticia", "t": round(c2 - 0.1, 2), "ms": 0, "d": round(dur - c2 + 0.1, 2), "gain": 0.15, "fade": 0.6}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "boing", "t": 3.3, "gain": 0.4},
       {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.05, "gain": 0.5, "pico": 0.3, "d": 1.2}, {"src": "boing", "t": vd + 1.1, "gain": 0.3},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "papel", "t": r1, "gain": 0.45}, {"src": "boing", "t": a(1.8), "gain": 0.25},
       {"src": "whoosh2", "t": a(2.2), "gain": 0.3}, {"src": "whoosh2", "t": a(3.05), "gain": 0.35}, {"src": "boing", "t": a(3.2), "gain": 0.3},
       {"src": "boom", "t": a(5.48), "gain": 0.55, "pico": 0.3, "d": 1.3},
       {"src": "glitch", "t": tB - 0.05, "gain": 0.4}, {"src": "papel", "t": tB, "gain": 0.45}, {"src": "boing", "t": b(1.05), "gain": 0.3}, {"src": "papel", "t": b(1.3), "gain": 0.4},
       {"src": "whoosh2", "t": b(2.85), "gain": 0.35}, {"src": "teclado", "t": b(3.55), "gain": 0.3, "d": 1.7}, {"src": "papel", "t": b(3.6), "gain": 0.35},
       {"src": "whoosh2", "t": b(5.3), "gain": 0.35}, {"src": "boom", "t": b(5.95), "gain": 0.45, "pico": 0.3, "d": 1.0},
       {"src": "whoosh2", "t": b(7.45), "gain": 0.35}, {"src": "scratch", "t": b(9.05), "gain": 0.22}, {"src": "boing", "t": b(10.6), "gain": 0.3},
       {"src": "whoosh2", "t": b(11.9), "gain": 0.35}, {"src": "scratch", "t": b(12.95), "gain": 0.2}, {"src": "boom", "t": b(14.3), "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": tC - 0.05, "gain": 0.4}, {"src": "papel", "t": tC, "gain": 0.4}, {"src": "whoosh2", "t": e(1.4), "gain": 0.3}, {"src": "boing", "t": e(4.25), "gain": 0.35},
       {"src": "pagina", "t": e(4.9), "gain": 0.45}, {"src": "riser", "t": e(6.1), "gain": 0.18, "d": 1.9},
       {"src": "whoosh2", "t": e(10.9), "gain": 0.35}, {"src": "boing", "t": e(13.2), "gain": 0.25}, {"src": "boing", "t": e(13.8), "gain": 0.25},
       {"src": "papel", "t": e(15.5), "gain": 0.4}, {"src": "riser", "t": e(16.0), "gain": 0.16, "d": 2.2}, {"src": "boom", "t": e(17.4), "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": e(19.25), "gain": 0.3}, {"src": "boing", "t": e(21.6), "gain": 0.3},
       {"src": "glitch", "t": tO - 0.05, "gain": 0.4}, {"src": "boing", "t": o(0.15), "gain": 0.25}, {"src": "boing", "t": o(0.5), "gain": 0.25},
       {"src": "whoosh2", "t": o(4.95), "gain": 0.3}, {"src": "boing", "t": o(8.6), "gain": 0.3}, {"src": "whoosh2", "t": o(9.6), "gain": 0.3},
       {"src": "papel", "t": tE, "gain": 0.45},
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.5},
       {"src": "boom", "t": f(1.0), "gain": 0.55, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 214, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.1, 1720], [4.1, vd, 1440], [vd, r1, 1000], [r1, c1, 1700], [c1, c2, 1500], [c2, dur + 1, 1700]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = musica
p['legenda']['estilo'] = 'serif'
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "tC", tC, "tO", tO, "tE", tE, "c1", c1, "c2", c2)
if '--sem-pos' not in sys.argv:
    subprocess.run(["python3", "scripts/entrada.py", PID, M + "rk_ent.mp4", M + "rk_ent.mp4.words.json", "2.07",
                    "CORRIDA DE ESPERMATOZOIDE VALENDO 100 MIL DÓLARES?", "notícia que viralizou com 3,4 milhões de views"], check=True)
