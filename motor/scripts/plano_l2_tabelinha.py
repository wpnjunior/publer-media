# plano_l2_tabelinha.py (14/11, lote 2, Fertilidade a Dois): "como engravidar de menina" (TikTok @maviemeubrasil).
# Trecho (34,5-43,45 s, 8,95 s): "O que poderia ajudar em engravidar de menina? Primeiro, relação sexual alguns dias antes
# da ovulação. Os espermatozoides X são mais lentos, mas vivem mais." -> MITO.
# Decisão do Wagner: "sem nome e acolhendo" (nunca nomear o colega nem a apresentadora; crédito só o @; tom acolhedor).
# Edição da aula: CAIXINHA QUE SE DESENHA (cartão creme, aba lima, desenhos e calendário que se desenham, uma ideia por
# cartão), sem b-roll. Estudo com barras desenhadas no calendário do ciclo. Pele: LOUSA.
# Voz em blocos por clima (sem atempo): r1+A neutro, B manso (aula), C neutro (estudo), D alegre (fecho).
# Depois deste script:
#   python3 scripts/entrada.py react_l2_tabelinha assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     'TABELINHA PARA FAZER MENINA?' 'dica que viralizou nas redes' && python3 scripts/pele.py react_l2_tabelinha lousa
import sys, json; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l2_tabelinha'; P = 'tb'
vd = 8.95                        # viral cortado (fim congelado 8,45-8,95 para a legenda queimada não adiantar a frase)
r1 = round(vd + 2.88, 2)         # rosto 6cd9 "Calma. Isso aí é mito, tá?" (tb_rosto.mp4, 2,88 s)
DA, DB, DC, DD = 6.23, 22.97, 21.48, 14.39
tA = round(r1 + 0.2, 2)
tB = round(tA + DA + 0.6, 2)
tC = round(tB + DB + 0.6, 2)
c1 = round(tC + DC + 0.4, 2)     # CTA 6cd9 (banco cta6)
c2 = round(c1 + 4.12, 2)
dur = round(c2 + DD + 0.6, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3); f = lambda v: round(c2 + v, 3)
ENT = 1.88                       # entrada.py empurra "t" mas não os tempos internos de "abas"
TINTA, VERM, ROSA_T, AZUL_T, VERDE_T = "#1c1a17", "#e0322b", "#c0396b", "#1f5fb2", "#1f9e4f"
SOMBRA = "text-shadow:8px 8px 0 #000"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.5}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}

def FR(t, d, txt, tam=112, y=385, cor=TINTA):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [95, y], "w": 890, "fonte": f"{tam}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 45, "anim": "palavras", "vel": 0.09, "fixo": True}
def NOTA(t, d, txt, x, y, w=420, tam=96, cor=VERM, rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg)", "fixo": True}
def FS(t, d, orgaos, z=42, fixo=True, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": fixo}; L.update(k); return L
def DS(t, d, formas, cor=VERM, lw=11, vel=0.45, z=44):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "fixo": True, "vel": vel}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}
def DIAS(t0, d, n, x0, y, w, h, gap, passo=0.12, cor=TINTA, lw=9):
    """fileira de quadradinhos de calendário que se desenham um a um"""
    return DS(t0, d, [{"k": "caixa", "b": [x0 + k * (w + gap), y, w, h], "t": round(k * passo, 3)} for k in range(n)], cor=cor, lw=lw, vel=0.3)
def ROT(t, d, txt, x, y, w, tam=44, cor=TINTA, fonte="800 Montserrat"):
    fo = f"{tam}px Anton" if fonte == "Anton" else f"800 {tam}px Montserrat"
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": fo, "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "fixo": True}

# ================= abertura: viral em tela dividida + caixinha de pergunta =================
c = abertura(P, vd, "via @maviemeubrasil", "center 30%", "Mito ou verdade? 👇", "A data da relação escolhe se vem menina?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 751, "suf": " MIL VIEWS", "tam": 120}])
c += [{"tipo": "texto", "t": vd + 0.02, "d": r1 - vd - 0.02, "xy": [70, 190], "w": 940, "fonte": "125px Anton", "cor": "#ffffff", "alinha": "center",
       "txt": "“X: MAIS LENTO,\\nVIVE MAIS”", "z": 55, "entra": "pop", "fixo": True,
       "css": "background:rgba(11,21,18,.9);border-radius:14px;height:909px;box-sizing:border-box;padding:190px 40px 0;line-height:1.15;text-shadow:6px 6px 0 #000"},
      {"tipo": "carimbo", "t": vd + 0.45, "d": r1 - vd - 0.45, "xy": [300, 680], "txt": "MITO", "tam": 150, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)", "fixo": True},
      rosto_r1(P, vd, r1 - vd, 0)]

# ================= A (neutro, acolhendo): o sonho é lindo, mas a data não escolhe =================
c += B(P + "_viral_blur.mp4", r1, tB - r1, 20.0)
c += [GL(r1), FL(r1),
      FS(a(0.1), 3.05, [{"k": "coracao_afeto", "xy": [540, 1060], "s": 1.5, "t": 0.0}], pulsos=[{"o": 0, "t": 1.0}, {"o": 0, "t": 2.2}], fixo=False, z=30),
      T(a(0.0), 3.15, "SONHAR COM UMA MENINA É LINDO", y=330, f="124px Anton", cor="#ff9fb4", css=SOMBRA),
      FL(a(3.15)),
      FS(a(3.15), tB - a(3.15), [{"k": "calendario", "xy": [540, 1010], "s": 1.5, "t": 0.0}], fixo=False, z=30),
      T(a(3.2), tB - a(3.2), "O DIA DA RELAÇÃO", y=330, f="140px Anton", css=SOMBRA),
      {"tipo": "desenho", "t": a(4.25), "d": tB - a(4.25), "formas": [{"k": "x", "c": [540, 1010], "s": 150}], "cor": "#ff2d3d", "espessura": 22, "z": 45},
      T(a(4.24), tB - a(4.24), "NÃO ESCOLHE O SEXO", y=1340, f="112px Anton", cor="#ffe27a", css=SOMBRA, anim=None, entra="zoom")]

# ================= B (manso): AULA na CAIXINHA que se desenha =================
S1, S2, S3, S4, S5, S6 = b(0.0), b(6.8), b(9.72), b(12.92), b(16.27), b(19.37)
AF = b(DB + 0.3)
c += [GL(tB), FL(tB),
      {"tipo": "fundo", "t": tB, "d": AF - tB, "cor": "#0e1012", "textura": "gradiente", "cor2": "#22302a", "z": 11, "fixo": True},
      {"tipo": "cartao", "t": tB, "d": AF - tB, "box": [60, 330, 960, 1250], "aba": "1 · quem decide", "z": 30, "fixo": True,
       "abas": [[round(x + ENT, 3), s] for x, s in [[S2, "2 · o X"], [S3, "3 · o Y"], [S4, "4 · a corrida"], [S5, "5 · a moeda"], [S6, "6 · o calendário"]]]},
      SELO(tB + 0.2, AF - tB - 0.2, "● AULA RÁPIDA · MENINA OU MENINO?")]
# (1) Quem decide se vem menina ou menino é o espermatozoide.
c += [FR(S1 + 0.15, S2 - S1 - 0.2, "QUEM DECIDE?", tam=190, y=420),
      FS(S1 + 0.3, S2 - S1 - 0.35, [{"k": "ovulo", "xy": [740, 1060], "s": 1.0, "t": 0.0, "rotulo": "ÓVULO", "rot_y": 205}],
         fluxos=[{"de": [150, 1160], "para": [570, 1080], "curva": -40, "cor": "#7a2b3e", "t": 4.3, "d": 2.3, "n": 6, "r": 12, "viagem": 1.0}],
         pulsos=[{"o": 0, "t": 5.6}]),
      NOTA(b(4.5), S2 - b(4.5) - 0.05, "o espermatozoide!", 120, 1380, w=600, tam=100, cor=VERM, rot=-3)]
# (2) Metade leva o X, de menina.
c += [FR(S2 + 0.05, S3 - S2 - 0.1, "METADE LEVA O X", tam=124),
      FS(S2 + 0.1, S3 - S2 - 0.15, [{"k": "tb_esp_x", "xy": [560, 1000], "s": 1.6, "t": 0.0}], pulsos=[{"o": 0, "t": 1.6}]),
      NOTA(b(7.7), S3 - b(7.7) - 0.05, "X = menina", 260, 1300, w=560, tam=120, cor=ROSA_T, rot=-4)]
# (3) Metade leva o Y, de menino.
c += [FR(S3 + 0.05, S4 - S3 - 0.1, "METADE LEVA O Y", tam=124),
      FS(S3 + 0.1, S4 - S3 - 0.15, [{"k": "tb_esp_y", "xy": [560, 1000], "s": 1.6, "t": 0.0}], pulsos=[{"o": 0, "t": 1.9}]),
      NOTA(b(10.8), S4 - b(10.8) - 0.05, "Y = menino", 260, 1300, w=560, tam=120, cor=AZUL_T, rot=-3)]
# (4) E ninguém é mais lento, nem vive mais.
c += [FR(S4 + 0.05, S5 - S4 - 0.1, "NINGUÉM É MAIS LENTO", tam=124),
      FS(S4 + 0.1, S5 - S4 - 0.15, [{"k": "tb_esp_x", "xy": [270, 760], "s": 0.75, "t": 0.0},
                                    {"k": "tb_esp_y", "xy": [270, 1010], "s": 0.75, "t": 0.15}]),
      DS(S4 + 0.5, S5 - S4 - 0.55, [{"k": "seta", "de": [400, 760], "para": [880, 760], "curva": 0},
                                    {"k": "seta", "de": [400, 1010], "para": [880, 1010], "curva": 0}], cor=TINTA, lw=12),
      DS(S4 + 0.9, S5 - S4 - 0.95, [{"k": "linha", "pts": [[930, 660], [930, 1110]]}], cor=VERDE_T, lw=10),
      DS(b(14.0), S5 - b(14.0) - 0.05, [{"k": "check", "c": [930, 1220], "s": 45}], cor=VERDE_T, lw=16),
      NOTA(b(14.3), S5 - b(14.3) - 0.05, "nem vive mais", 140, 1260, w=620, tam=104, cor=VERM, rot=-3)]
# (5) É igual cara ou coroa.
c += [FR(S5 + 0.05, S6 - S5 - 0.1, "IGUAL CARA OU COROA", tam=132),
      FS(S5 + 0.1, S6 - S5 - 0.15, [{"k": "tb_moeda", "xy": [540, 1000], "s": 1.45, "t": 0.0}], pulsos=[{"o": 0, "t": 1.2}, {"o": 0, "t": 2.2}]),
      NOTA(b(17.3), S6 - b(17.3) - 0.05, "50%", 90, 1330, w=300, tam=120, cor=ROSA_T, rot=-5),
      NOTA(b(17.6), S6 - b(17.6) - 0.05, "50%", 690, 1330, w=300, tam=120, cor=AZUL_T, rot=4)]
# (6) Jogar a moeda na segunda ou na sexta não muda a chance, né?  (calendário que se desenha)
DX, DW, DG, DY, DH = 95, 120, 10, 700, 130
cx = lambda k: DX + k * (DW + DG) + DW / 2
c += [FR(S6 + 0.05, AF - S6 - 0.1, "O DIA NÃO MUDA A CHANCE", tam=118),
      DIAS(S6 + 0.15, AF - S6 - 0.2, 7, DX, DY, DW, DH, DG, passo=0.1)]
c += [DS(b(20.3), AF - b(20.3), [{"k": "circulo", "c": [cx(0), DY + DH / 2], "r": [78, 88]}], cor=ROSA_T, lw=11),
      DS(b(21.15), AF - b(21.15), [{"k": "circulo", "c": [cx(4), DY + DH / 2], "r": [78, 88]}], cor=AZUL_T, lw=11),
      NOTA(b(20.3), AF - b(20.3), "segunda", 62, DY + DH + 20, w=280, tam=84, cor=ROSA_T, rot=-4),
      NOTA(b(21.15), AF - b(21.15), "sexta", cx(4) - 150, DY + DH + 20, w=300, tam=84, cor=AZUL_T, rot=3),
      DS(b(21.5), AF - b(21.5), [{"k": "seta", "de": [cx(0) + 40, DY + DH + 140], "para": [440, 1150], "curva": -30},
                                 {"k": "seta", "de": [cx(4) - 40, DY + DH + 140], "para": [640, 1150], "curva": 30}], cor=TINTA, lw=11),
      NOTA(b(21.6), AF - b(21.6), "50%", 390, 1160, w=300, tam=150, cor=VERDE_T, rot=-3),
      NOTA(b(21.75), AF - b(21.75) - 0.01, "mesma chance", 240, 1390, w=600, tam=96, cor=VERM, rot=-2)]
SFX_AULA = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": tB + 0.15, "gain": 0.4},
            {"src": "boing", "t": b(4.5), "gain": 0.3}, {"src": "pagina", "t": S2, "gain": 0.4}, {"src": "boing", "t": b(8.5), "gain": 0.3},
            {"src": "pagina", "t": S3, "gain": 0.4}, {"src": "boing", "t": b(11.7), "gain": 0.3},
            {"src": "pagina", "t": S4, "gain": 0.4}, {"src": "whoosh2", "t": S4 + 0.5, "gain": 0.3}, {"src": "boing", "t": b(14.0), "gain": 0.3},
            {"src": "pagina", "t": S5, "gain": 0.4}, {"src": "boing", "t": b(17.6), "gain": 0.3}, {"src": "boing", "t": b(17.9), "gain": 0.25},
            {"src": "pagina", "t": S6, "gain": 0.4}, {"src": "teclado", "t": S6 + 0.15, "gain": 0.25, "d": 0.9},
            {"src": "scratch", "t": b(20.3), "gain": 0.25}, {"src": "scratch", "t": b(21.15), "gain": 0.25}, {"src": "boing", "t": b(21.75), "gain": 0.3}]

# ================= C (neutro): o estudo, com o calendário do ciclo =================
E1, E2, E3, E4, E5 = e(0.0), e(5.12), e(8.3), e(10.15), e(17.75)
c += B(P + "_viral_blur.mp4", AF, E4 - AF, 40.0)
c += [GL(AF), FL(AF),
      {"tipo": "numero", "t": E1 + 0.05, "d": E2 - E1 - 0.1, "xy": [0, 430], "valor": 221, "tam": 330, "z": 44},
      T(E1 + 0.7, E2 - E1 - 0.75, "MULHERES, DIA A DIA", y=900, f="124px Anton", css=SOMBRA),
      FL(E2),
      T(E2 + 0.02, E3 - E2 - 0.04, "MENINO E MENINA:", y=380, f="130px Anton", css=SOMBRA),
      T(E2 + 0.9, E3 - E2 - 0.95, "MESMAS DATAS", y=620, f="190px Anton", cor="#3ddc84", css=SOMBRA, anim=None, entra="zoom"),
      {"tipo": "desenho", "t": E2 + 1.6, "d": E3 - E2 - 1.65, "formas": [{"k": "check", "c": [540, 1080], "s": 80}], "cor": "#3ddc84", "espessura": 20, "z": 46},
      FL(E3),
      T(E3 + 0.02, E4 - E3 - 0.04, "E TEM MAIS...", y=560, f="170px Anton", cor="#ffe27a", css=SOMBRA, anim=None, entra="zoom")]
# barras no calendário do ciclo (cartão)
QX, QW, QG, QY, QH = 115, 130, 14, 1310, 120
qx = lambda k: QX + k * (QW + QG) + QW / 2
BASE = QY - 18
c += [GL(E4), FL(E4),
      {"tipo": "fundo", "t": E4, "d": E5 - E4, "cor": "#0e1012", "textura": "gradiente", "cor2": "#22302a", "z": 11, "fixo": True},
      {"tipo": "cartao", "t": E4, "d": E5 - E4, "box": [60, 330, 960, 1250], "aba": "chance de engravidar", "z": 30, "fixo": True},
      FR(E4 + 0.1, E5 - E4 - 0.15, "CHANCE DE ENGRAVIDAR", tam=112),
      DIAS(E4 + 0.3, E5 - E4 - 0.35, 6, QX, QY, QW, QH, QG, passo=0.12),
      ]
c += [ROT(E4 + 0.4 + k * 0.12, E5 - E4 - 0.45 - k * 0.12, d, QX + k * (QW + QG), QY - 8, QW, tam=100, fonte="Anton") for k, d in enumerate(["5", "4", "3", "2", "1", "♥"])]
c += [DS(e(11.55), E5 - e(11.55), [{"k": "linha", "pts": [[qx(0), BASE], [qx(0), BASE - 170]], "j": 0}], cor="#ff7a9c", lw=96, vel=0.6),
      NOTA(e(11.75), E5 - e(11.75), "10%", qx(0) - 120, BASE - 330, w=300, tam=130, cor=ROSA_T, rot=-4),
      NOTA(e(13.1), E5 - e(13.1), "5 dias antes", 50, QY + QH + 8, w=440, tam=84, cor="#5b6670", rot=-3),
      DS(e(14.55), E5 - e(14.55), [{"k": "linha", "pts": [[qx(5), BASE], [qx(5), BASE - 560]], "j": 0}], cor="#3dbb6e", lw=96, vel=0.8),
      NOTA(e(15.3), E5 - e(15.3), "33%", qx(5) - 360, BASE - 600, w=300, tam=150, cor=VERDE_T, rot=3),
      NOTA(e(15.5), E5 - e(15.5), "ovulação", 600, QY + QH + 8, w=420, tam=84, cor="#5b6670", rot=-2),
      DS(e(16.2), E5 - e(16.2), [{"k": "seta", "de": [qx(1) - 20, BASE - 230], "para": [qx(3) + 20, BASE - 400], "curva": 30}], cor=VERM, lw=12)]
# fugir do dia fértil só tira chance
c += B(P + "_viral_blur.mp4", E5, c1 - E5, 55.0)
c += [GL(E5), FL(E5),
      T(E5 + 0.05, c1 - E5 - 0.05, "FUGIR DO DIA FÉRTIL", y=360, f="140px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": E5 + 0.1, "d": c1 - E5 - 0.1, "z": 30, "orgaos": [{"k": "calendario", "xy": [540, 1020], "s": 1.3, "t": 0.0}]},
      {"tipo": "desenho", "t": e(19.6), "d": c1 - e(19.6), "formas": [{"k": "seta", "de": [860, 820], "para": [860, 1220], "curva": 0}], "cor": "#ff9fb4", "espessura": 18, "z": 46},
      T(e(19.1), c1 - e(19.1), "SÓ TIRA CHANCE DE VOCÊS", y=1320, f="112px Anton", cor="#ffe27a", css=SOMBRA, anim=None, entra="zoom"),
      F(E1, c1 - E1, "Wilcox e col., N Engl J Med 1995 · 221 mulheres, 625 ciclos · doi 10.1056/NEJM199512073332301")]
c[-1]["fixo"] = True

# ================= CTA (banco cta6) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (alegre): fecho =================
c += B(P + "_viral_blur.mp4", c2, dur - c2, 48.0)
FX, FW, FG, FY, FH = 115, 130, 14, 860, 120
fxc = lambda k: FX + k * (FW + FG) + FW / 2
c += [GL(c2), FL(c2),
      T(f(0.05), 1.65, "QUEREM ENGRAVIDAR?", y=480, f="150px Anton", css=SOMBRA),
      FL(f(1.72)),
      T(f(1.75), 3.5, "OS 6 DIAS ATÉ A OVULAÇÃO", y=380, f="118px Anton", cor="#3ddc84", css=SOMBRA),
      {"tipo": "desenho", "t": f(1.9), "d": 3.35, "formas": [{"k": "caixa", "b": [FX + k * (FW + FG), FY, FW, FH], "t": round(k * 0.18, 2)} for k in range(6)],
       "cor": "#3ddc84", "espessura": 12, "z": 44, "vel": 0.3},
      {"tipo": "desenho", "t": f(3.9), "d": 1.35, "formas": [{"k": "circulo", "c": [fxc(5), FY + FH / 2], "r": [85, 95]}], "cor": "#ff9fb4", "espessura": 12, "z": 45},
      T(f(3.7), 1.55, "ovulação", y=1080, f="700 96px Caveat", cor="#ff9fb4", css=SOMBRA, anim=None, entra="pop"),
      FL(f(5.28)),
      T(f(5.3), 3.4, "BATEU A DÚVIDA?", y=420, f="150px Anton", cor="#ff9fb4", css=SOMBRA),
      T(f(6.6), 2.1, "OS DOIS AO MÉDICO", y=830, f="150px Anton", cor="#ffe27a", css=SOMBRA, anim=None, entra="zoom"),
      {"tipo": "desenho", "t": f(7.4), "d": 1.3, "formas": [{"k": "check", "c": [540, 1260], "s": 70}], "cor": "#3ddc84", "espessura": 20, "z": 46},
      FL(f(8.7)),
      T(f(8.72), 3.45, "A TABELINHA MARCA O DIA FÉRTIL", y=330, f="118px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": f(8.75), "d": 3.4, "z": 30, "orgaos": [{"k": "calendario", "xy": [540, 1030], "s": 1.35, "t": 0.0}], "pulsos": [{"o": 0, "t": 1.6}]},
      {"tipo": "desenho", "t": f(10.3), "d": 1.85, "formas": [{"k": "check", "c": [800, 1250], "s": 60}], "cor": "#3ddc84", "espessura": 20, "z": 46},
      FL(f(12.2)),
      {"tipo": "gigante", "t": f(12.2), "d": dur - f(12.2), "txt": "MENINA OU MENINO", "y": 1180, "tam": 300, "cor": "rgba(255,255,255,.14)", "x": [1000, -2600], "z": 20},
      {"tipo": "carimbo", "t": f(12.25), "d": dur - f(12.25), "xy": [100, 760], "txt": "O SEXO DO BEBÊ, NÃO.", "tam": 96, "rot": -6, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)"},
      F(c2, dur - c2, "Wilcox e col., N Engl J Med 1995 · doi 10.1056/NEJM199512073332301")]

voz = [{"src": M + "tb_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "tb_viral.words.json"},
       {"src": M + "tb_rosto.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "tb_rosto.words.json"},
       {"src": M + "tb_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "tb_a_voz.words.json"},
       {"src": M + "tb_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "tb_b_voz.words.json"},
       {"src": M + "tb_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "tb_c_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "tb_d_voz.wav", "t": c2, "ms": 0, "d": DD, "palavras": M + "tb_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": a(0.1), "gain": 0.4, "pico": 0.45},
       {"src": "whoosh2", "t": a(3.15), "gain": 0.35}, {"src": "scratch", "t": a(4.25), "gain": 0.3},
       {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, {"src": "boom", "t": E1 + 0.05, "gain": 0.5, "pico": 0.3, "d": 1.5},
       {"src": "whoosh2", "t": E2, "gain": 0.35}, {"src": "notif", "t": E2 + 1.6, "gain": 0.35}, {"src": "whoosh2", "t": E3, "gain": 0.35},
       {"src": "papel", "t": E4 + 0.05, "gain": 0.45}, {"src": "riser", "t": e(13.4), "gain": 0.2, "d": 1.5}, {"src": "boing", "t": e(15.3), "gain": 0.35},
       {"src": "whoosh", "t": E5, "gain": 0.4, "pico": 0.45},
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
       {"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": f(1.72), "gain": 0.35}, {"src": "whoosh2", "t": f(5.28), "gain": 0.35},
       {"src": "notif", "t": f(7.4), "gain": 0.35}, {"src": "whoosh2", "t": f(8.7), "gain": 0.35}, {"src": "boom", "t": f(12.25), "gain": 0.5, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 143, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": r1, "d": round(c1 - r1, 2), "gain": 0.14, "fade": 0.8},
                        {"src": "m_emocao", "t": c2, "d": round(dur - c2, 2), "gain": 0.14, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "AF", AF, "tC", tC, "c1", c1, "c2", c2)
