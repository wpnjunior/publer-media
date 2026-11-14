import sys, json; sys.path.insert(0, 'scripts')
from mk import *
# plano_l2_estomago.py (14/11, lote 2, Caneta com Músculo): "estômago paralisado" (TikTok @france.tv, Envoyé Spécial, France 2),
# paciente em francês, dublada pela Murilo (original a 0,16 por baixo; a marca vira BIP no original e na dublagem e as
# legendas francesas queimadas foram borradas no ep_viral.mp4, ver tmp_ep/prep.py).
# Trecho 0-15,3 s: "Isso aqui é o meu estoque de bebidas hiperproteicas... a única coisa que eu consigo comer há meses.
# Eu tomo isso por causa do [bip], porque eu desenvolvi uma paralisia do estômago." -> MEIA VERDADE (devagar é o remédio;
# parado de verdade é raro, mas existe). Critica a frase, não a pessoa; o sofrimento dela é tratado com respeito.
# EDIÇÃO FULL (sem b-roll): Wagner RECORTADO sem fundo (webm com alfa do HeyGen) sobre a cena com palavra gigante atrás,
# gigantes Anton atrás de cada cena, um desenho por cena (fisio_extra/estomago.svg, caneta.svg, cerebro, intestino, prato),
# números 3D, artigo 3D com grifo, carimbo. Pele: notícia.
# Voz em blocos por clima, sem atempo: A neutro (r1 + abertura), B manso (aula), C neutro (problema + estudo), D manso (fecho).
# Depois deste script:
#   python3 scripts/entrada.py react_l2_estomago assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     '“ESTÔMAGO PARALISADO” PELA CANETA?' 'reportagem da TV francesa (France 2)' && python3 scripts/pele.py react_l2_estomago noticia
PID = 'react_l2_estomago'; P = 'ep'
vd = 15.3
r1 = round(vd + 3.42, 2)                 # recorte webm (3,42 s): "Estômago paralisado? Tem um pedaço de verdade aí."
DA, DB, DC, DD = 10.33, 22.27, 28.26, 9.78
tA = r1
tB = round(tA + DA + 0.6, 2)
tC = round(tB + DB + 0.6, 2)
c1 = round(tC + DC + 0.4, 2)             # CTA banco cta6
c2 = round(c1 + 4.12 + 0.05, 2)
dur = round(c2 + DD + 0.6, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3); f = lambda v: round(c2 + v, 3)
AMAR, VERM, VERDE, BRANCO = '#ffd400', '#ff4d4f', '#3ddc84', '#ffffff'
SOMBRA = "text-shadow:7px 7px 0 #000,0 0 18px rgba(0,0,0,.7)"
def TT(t, d, txt, y=330, fz=120, cor=BRANCO, **k):
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SOMBRA, vel=0.09, **k)
def GIG(t, d, txt, y=1300, tam=420, cont=False, cor="rgba(255,255,255,.10)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.5)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": 30, "orgaos": orgaos}; L.update(k); return L
def DS(t, d, formas, cor=VERM, lw=16, z=45):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z}
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.5}
def SELO(t, d, txt="● CHECAGEM · O QUE A CIÊNCIA DIZ"):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#ffffff",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ff2d3d;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"}
FONTE = "Sodhi e col., JAMA 2023 · 5.411 pacientes · doi 10.1001/jama.2023.19574"
# porteira (bolinha amarela do estomago.svg, local 150,-8) na tela
def port(xy, s): return [round(xy[0] + 150 * s), round(xy[1] - 8 * s)]

# ================= abertura: viral em tela dividida + caixinha =================
c = abertura(P, vd, "via @france.tv (Envoyé Spécial)", "center 30%", "Mito ou verdade? 👇", "A caneta paralisa o estômago?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 872.7, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
c = [L for L in c if L.get("tipo") != "foto"]
for L in c:
    if L.get("tipo") == "cartao": L["d"] = vd
    if L.get("tipo") == "pergunta": L["botoes"] = ["MITO", "VERDADE", "DEPENDE"]; L["escolha"] = 2; L["xy"] = [70, 1150]; L["w"] = 940

# ================= R1: Wagner RECORTADO sobre a cena, palavra gigante atrás =================
c += [{"tipo": "glitch", "t": vd - 0.05, "d": 0.25}, FL(vd),
      GIG(vd, r1 - vd, "PARALISADO?", y=760, tam=360, cor="rgba(255,212,0,.85)"),
      {"tipo": "recorte", "t": vd, "d": round(r1 - vd, 2), "ms": 0, "src": M + P + "_r1.webm", "box": [0, 250, 1080, 1670], "pos": "center top",
       "zoom": [[vd, 1.0, 0.01], [vd + 1.6, 1.07, 0.4]], "z": 45, "entra": "desliza"},
      {"tipo": "texto", "t": round(vd + 1.6, 2), "d": round(r1 - vd - 1.6, 2), "xy": [40, 210], "w": 1000, "fonte": "170px Anton", "cor": "#f39c12",
       "alinha": "center", "txt": "MEIA VERDADE", "z": 50, "entra": "zoom", "css": "text-shadow:10px 10px 0 #000"}]

# ================= A (neutro): respeito + "falo só da frase" =================
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1), SELO(a(0.1), c1 - a(0.1)),
      GIG(a(0), 3.9, "RESPEITO", y=1380, tam=400, cont=True, cor="rgba(255,212,0,.45)"),
      {"tipo": "foto", "t": a(0.05), "d": 3.85, "src": M + P + "_rosto_viral.jpg", "box": [250, 640, 580, 604], "rot": -3, "raio": 20, "entra": "pop", "z": 30},
      TT(a(0.1), 3.85, "O QUE ELA SENTE É SÉRIO", y=300, fz=118),
      TT(a(2.1), 1.85, "E MERECE RESPEITO", y=1320, fz=120, cor=AMAR, anim=None, entra="zoom"),
      FL(a(3.95)),
      GIG(a(3.95), 4.1, "A FRASE", y=1350, tam=420, ida=False),
      TT(a(4.0), 4.05, "NÃO EXAMINEI ELA: FALO DA FRASE", y=300, fz=124, cor=AMAR),
      {"tipo": "texto", "t": a(4.6), "d": 3.45, "xy": [110, 760], "w": 860, "fonte": "700 92px Caveat", "cor": "#111", "alinha": "center",
       "txt": "“desenvolvi uma paralisia do estômago”", "entra": "pop", "z": 44,
       "css": "background:#fff;border-radius:26px;padding:40px 30px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(0,0,0,.5)"},
      FL(a(8.05)),
      GIG(a(8.05), DA + 0.6 - 8.05, "PARADO?", y=1380, tam=440, cont=True, cor="rgba(255,77,79,.55)"),
      TT(a(8.1), DA + 0.6 - 8.1, "A CANETA PARA O ESTÔMAGO?", y=300, fz=130),
      FIS(a(8.4), DA + 0.6 - 8.4, [{"k": "caneta", "xy": [540, 1080], "s": 1.25, "t": 0.0}], pulsos=[{"o": 0, "t": 1.2}])]

# ================= B (manso): AULA, uma ideia por cena =================
E1 = [540, 1060]; S1 = 1.7
c += [FL(tB),
      FIS(b(0), 4.75, [{"k": "estomago", "xy": E1, "s": S1, "t": 0.05}], pulsos=[{"o": 0, "t": 1.4}]),
      GIG(b(0), 4.75, "LIQUIDIFICADOR", y=1420, tam=330),
      TT(b(0.07), 2.85, "ESTÔMAGO = LIQUIDIFICADOR", y=300, fz=120),
      TT(b(2.95), 1.8, "COM UMA PORTEIRA", y=300, fz=120, cor=AMAR),
      DS(b(3.0), 1.75, [{"k": "circulo", "c": port(E1, S1), "r": [62, 62]}], cor=AMAR, lw=14),
      {"tipo": "texto", "t": b(3.2), "d": 1.55, "xy": [640, 1150], "w": 360, "fonte": "700 84px Caveat", "cor": AMAR, "alinha": "center",
       "txt": "porteira", "entra": "pop", "z": 46, "css": "text-shadow:3px 3px 0 #000;transform:rotate(-6deg)"},
      FL(b(4.75))]
E2 = [430, 900]; S2 = 1.3; p2 = port(E2, S2)
c += [FIS(b(4.75), 4.2, [{"k": "estomago", "xy": E2, "s": S2, "t": 0.05}, {"k": "intestino", "xy": [640, 1440], "s": 0.62, "t": 0.3, "rotulo": "INTESTINO", "rot_y": 215}],
          fluxos=[{"de": p2, "para": [600, 1330], "curva": 70, "cor": AMAR, "t": 1.0, "d": 3.0, "n": 6, "r": 15, "rotulo": "COMIDA", "viagem": 1.0}]),
      GIG(b(4.75), 4.2, "AOS POUQUINHOS", y=1560, tam=300, cont=True, cor="rgba(255,212,0,.40)", ida=False),
      TT(b(4.86), 4.05, "BATE E SOLTA AOS POUQUINHOS", y=300, fz=118),
      FL(b(8.95))]
c += [FIS(b(8.95), 4.5, [{"k": "caneta", "xy": [300, 1180], "s": 0.95, "t": 0.1}, {"k": "cerebro", "xy": [770, 900], "s": 0.8, "t": 2.8, "rotulo": "CÉREBRO", "rot_y": 190}],
          fluxos=[{"de": [380, 1080], "para": [700, 1010], "curva": -60, "cor": VERDE, "t": 2.95, "d": 1.4, "n": 5, "r": 15, "viagem": 0.7}],
          pulsos=[{"o": 1, "t": 3.7}]),
      GIG(b(8.95), 4.5, "AVISO", y=1500, tam=460),
      TT(b(9.04), 2.8, "A CANETA IMITA UM AVISO", y=300, fz=112),
      TT(b(11.88), 1.57, "“CHEGOU COMIDA”", y=300, fz=150, cor=AMAR, anim=None, entra="zoom"),
      FL(b(13.45))]
E4 = [540, 1020]; S4 = 1.7; p4 = port(E4, S4)
c += [FIS(b(13.45), 3.05, [{"k": "estomago", "xy": E4, "s": S4, "t": 0.05}],
          fluxos=[{"de": p4, "para": [880, 1500], "curva": 40, "cor": AMAR, "t": 0.6, "d": 2.4, "n": 2, "r": 16, "rotulo": "DEVAGAR", "viagem": 2.2}],
          pulsos=[{"o": 0, "t": 1.0}]),
      GIG(b(13.45), 3.05, "DEVAGAR", y=1560, tam=420, cont=True, cor="rgba(255,255,255,.35)"),
      TT(b(13.55), 2.95, "A PORTEIRA ABRE MAIS DEVAGAR", y=300, fz=118, cor=AMAR),
      FL(b(16.5))]
c += [FIS(b(16.5), 3.4, [{"k": "prato", "xy": [540, 1080], "s": 1.6, "t": 0.05}], encolhe=[{"o": 0, "t": 1.5, "para": 0.85, "d": 1.4}]),
      GIG(b(16.5), 3.4, "MENOS", y=1440, tam=480, ida=False),
      TT(b(16.5), 1.5, "ENCHE RÁPIDO", y=300, fz=150),
      TT(b(18.0), 1.9, "E COME MENOS", y=300, fz=150, cor=AMAR, anim=None, entra="zoom"),
      FL(b(19.9))]
c += [GIG(b(19.9), DB + 0.6 - 19.9, "FUNCIONANDO", y=1460, tam=340, cont=True, cor="rgba(61,220,132,.5)"),
      TT(b(19.96), DB + 0.6 - 19.96, "É O REMÉDIO FUNCIONANDO", y=330, fz=140, cor=VERDE),
      DS(b(20.4), DB + 0.6 - 20.4, [{"k": "check", "c": [500, 1000], "s": 150}], cor=VERDE, lw=30)]

# ================= C (neutro): o problema + o estudo =================
E5 = [540, 1080]; S5 = 1.7
c += [FL(tC),
      FIS(e(0), 3.6, [{"k": "estomago", "xy": E5, "s": S5, "t": 0.05}]),
      DS(e(1.6), 2.0, [{"k": "x", "c": port(E5, S5), "s": 70}], cor=VERM, lw=20),
      GIG(e(0), 3.6, "PROBLEMA", y=1480, tam=400, cont=True, cor="rgba(255,77,79,.55)"),
      TT(e(0.14), 3.4, "O PROBLEMA: A PORTEIRA QUASE NÃO ABRE", y=290, fz=112),
      FL(e(3.6)),
      {"tipo": "fundo", "t": e(3.6), "d": 3.75, "cor": "rgba(255,40,40,.20)", "z": 13},
      FIS(e(3.6), 3.75, [{"k": "estomago", "xy": [540, 1120], "s": 1.5, "t": 0.05}], pulsos=[{"o": 0, "t": 0.7}, {"o": 0, "t": 1.5}, {"o": 0, "t": 2.3}]),
      GIG(e(3.6), 3.75, "DOR", y=1450, tam=520, ida=False, cor="rgba(255,77,79,.35)"),
      TT(e(3.7), 3.65, "VÔMITO QUE NÃO PARA", y=300, fz=140),
      TT(e(5.85), 1.5, "E DOR", y=640, fz=220, cor=VERM, anim=None, entra="zoom"),
      FL(e(7.35)),
      GIG(e(7.35), 3.85, "ESTUDO", y=1400, tam=440, cont=True, cor="rgba(255,255,255,.30)"),
      TT(e(7.45), 3.75, "UM ESTUDO GRANDE", y=300, fz=140),
      {"tipo": "numero", "t": e(7.9), "d": 3.3, "xy": [0, 620], "valor": 5, "pre": "+", "suf": " MIL", "rotulo": "pessoas acompanhadas", "tam": 300, "cor": AMAR, "z": 44},
      FL(e(11.2)),
      GIG(e(11.2), 6.1, "POR ANO", y=1450, tam=400),
      TT(e(11.3), 6.0, "ESTÔMAGO PARADO DE VERDADE", y=300, fz=120),
      {"tipo": "numero", "t": e(12.95), "d": 4.35, "xy": [0, 620], "valor": 9, "pre": "7 A ", "rotulo": "por mil pessoas/ano", "tam": 280, "cor": VERM, "sombra": "#5a0d10", "z": 44},
      FL(e(17.3)),
      TT(e(17.4), 3.55, "COM OUTRO REMÉDIO DE EMAGRECER", y=300, fz=118),
      {"tipo": "numero", "t": e(18.5), "d": 2.45, "xy": [0, 660], "valor": 3, "rotulo": "em cada mil", "tam": 300, "cor": BRANCO, "sombra": "#555", "z": 44},
      GIG(e(17.3), 3.65, "3", y=1400, tam=520, ida=False),
      FL(e(20.95)),
      {"tipo": "artigo", "t": e(20.95), "d": 5.3, "box": [100, 330, 880, 760], "z": 34, "revista": "JAMA · 2023",
       "titulo": "Remédios da caneta e problemas no estômago e no intestino", "autores": "Sodhi e col. · 5.411 pacientes · planos de saúde dos EUA", "rola": 0,
       "linhas": [{"txt": "Estômago parado: raro.", "grifo": e(21.6)},
                  {"txt": "Mais que com outro remédio de emagrecer.", "grifo": e(22.6)},
                  {"txt": "Mostra ligação, não prova a causa em cada pessoa.", "grifo": e(23.9)}],
       "rodape": "doi 10.1001/jama.2023.19574"},
      TT(e(21.1), 5.1, "UMA DAS MAIORES REVISTAS DE MEDICINA", y=1210, fz=100, anim=None, entra="zoom"),
      GIG(e(20.95), 5.3, "2023", y=1450, tam=420, cont=True, cor="rgba(255,212,0,.35)"),
      FL(e(26.25)),
      GIG(e(26.25), c1 - e(26.25), "RARO", y=1300, tam=560, cor="rgba(255,212,0,.25)"),
      {"tipo": "carimbo", "t": e(26.35), "d": round(c1 - e(26.35), 2), "xy": [115, 720], "txt": "RARO, MAS EXISTE", "tam": 105, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92);white-space:nowrap"},
      {"tipo": "texto", "t": e(7.35), "d": round(c1 - e(7.35), 2), "xy": [40, 215], "w": 1000, "fonte": "600 28px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": FONTE, "z": 70, "css": "text-shadow:0 2px 6px #000"}]

# ================= CTA (banco cta6) + fecho (D manso) =================
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(f(0), 3.3, "COMUM", y=1400, tam=480, cont=True, cor="rgba(61,220,132,.45)"),
      TT(f(0.1), 3.2, "ENJOO LEVE NO COMEÇO", y=300, fz=130),
      TT(f(1.8), 1.5, "É COMUM", y=720, fz=200, cor=VERDE, anim=None, entra="zoom"),
      DS(f(2.0), 1.3, [{"k": "check", "c": [500, 1180], "s": 110}], cor=VERDE, lw=26),
      FL(f(3.3)),
      GIG(f(3.3), 4.15, "ALERTA", y=1420, tam=440, cor="rgba(255,77,79,.35)", ida=False),
      TT(f(3.4), 4.05, "VÔMITO QUE NÃO PASSA OU DOR FORTE", y=300, fz=130),
      TT(f(5.65), 1.8, "NÃO É NORMAL", y=760, fz=190, cor=VERM, anim=None, entra="zoom"),
      FL(f(7.45)),
      TT(f(7.5), round(dur - f(7.5), 2), "PROCURA O SEU MÉDICO", y=300, fz=140, cor=AMAR),
      {"tipo": "carimbo", "t": f(8.3), "d": round(dur - f(8.3), 2), "xy": [95, 860], "txt": "DEVAGAR NÃO É PARADO", "tam": 88, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92);white-space:nowrap"},
      {"tipo": "texto", "t": f(0), "d": round(dur - f(0), 2), "xy": [40, 215], "w": 1000, "fonte": "600 28px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": FONTE, "z": 70, "css": "text-shadow:0 2px 6px #000"}]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json", "gain": 0.16},
       {"src": M + P + "_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + P + "_r1.webm", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + P + "_r1.words.json"},
       {"src": M + P + "_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + P + "_a_voz.words.json"},
       {"src": M + P + "_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + P + "_b_voz.words.json"},
       {"src": M + P + "_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + P + "_c_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + P + "_d_voz.wav", "t": c2, "ms": 0, "d": DD, "palavras": M + P + "_d_voz.words.json"}]
musica = [{"src": "m_investiga", "t": vd, "ms": 0, "d": round(c1 - vd, 2), "gain": 0.24, "fade": 0.8},
          {"src": "m_emocao", "t": c2, "ms": 0, "d": round(dur - c2, 2), "gain": 0.22, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "whoosh", "t": vd, "gain": 0.5, "pico": 0.45}, {"src": "boom", "t": vd + 1.6, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1, "gain": 0.45, "pico": 0.45}, {"src": "pagina", "t": a(0.1), "gain": 0.35},
       {"src": "whoosh2", "t": a(3.95), "gain": 0.35}, {"src": "papel", "t": a(4.6), "gain": 0.45}, {"src": "whoosh", "t": a(8.05), "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": a(8.45), "gain": 0.3},
       # aula
       {"src": "whoosh", "t": tB, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": b(0.1), "gain": 0.3}, {"src": "scratch", "t": b(3.0), "gain": 0.3},
       {"src": "whoosh2", "t": b(4.75), "gain": 0.35}, {"src": "boing", "t": b(5.05), "gain": 0.25},
       {"src": "whoosh2", "t": b(8.95), "gain": 0.35}, {"src": "boing", "t": b(11.75), "gain": 0.3}, {"src": "notif", "t": b(11.9), "gain": 0.3},
       {"src": "whoosh2", "t": b(13.45), "gain": 0.35}, {"src": "whoosh2", "t": b(16.5), "gain": 0.35}, {"src": "boom", "t": b(18.0), "gain": 0.4, "pico": 0.3, "d": 1.2},
       {"src": "whoosh", "t": b(19.9), "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": b(20.4), "gain": 0.3},
       # problema + estudo
       {"src": "whoosh", "t": tC, "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": e(1.6), "gain": 0.35},
       {"src": "whoosh2", "t": e(3.6), "gain": 0.35}, {"src": "boom", "t": e(5.85), "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": e(7.35), "gain": 0.35}, {"src": "boom", "t": e(7.9), "gain": 0.5, "pico": 0.3, "d": 1.5},
       {"src": "whoosh2", "t": e(11.2), "gain": 0.35}, {"src": "riser", "t": e(11.4), "gain": 0.22, "d": 1.5}, {"src": "boom", "t": e(12.95), "gain": 0.55, "pico": 0.3, "d": 1.5},
       {"src": "whoosh2", "t": e(17.3), "gain": 0.35}, {"src": "boing", "t": e(18.5), "gain": 0.35},
       {"src": "whoosh", "t": e(20.95), "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": e(21.0), "gain": 0.5},
       {"src": "whoosh2", "t": e(26.25), "gain": 0.35}, {"src": "boom", "t": e(26.35), "gain": 0.6, "pico": 0.3, "d": 1.5},
       # CTA e fecho
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.5},
       {"src": "boing", "t": f(2.0), "gain": 0.3}, {"src": "whoosh2", "t": f(3.3), "gain": 0.35}, {"src": "whoosh2", "t": f(4.87), "gain": 0.3},
       {"src": "boom", "t": f(5.65), "gain": 0.45, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": f(7.45), "gain": 0.35}, {"src": "boom", "t": f(8.3), "gain": 0.55, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 331, c, voz, sfx, {"r1_fim": vd, "esconde": [[0, 4.0]], "ys": [[4.0, vd, 1440], [vd, r1, 1600], [r1, c1, 1730], [c2, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json')); p['audio']['musica'] = musica
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "tC", tC, "c1", c1, "c2", c2)
