# plano_l5_academia.py (15/11, lote 5, Caneta com Músculo): "larguei a academia e fiquei mais magra; quer um visual
# enxuto e definido? larga a academia" (personal trainer no TikTok, via @rileyjourdan, em inglês).
# Viral: dois pedaços (A 0,00-2,38 e B 37,00-41,05 do original; tmp_la/), 72 + 122 quadros, emenda limpa (quadro 72 = foto
#   de "antes", fora). Conferido de ouvido (faster-whisper medium no corte): "I quit the gym and got skinnier because of it."
#   + "If you want a leaner and more toned look, this might be your sign to ditch the gym." Dublagem Murilo (original a 0,16).
#   O texto na tela do pedaço A ("the gym made me bulky") fica visível com a tradução por cima ("a academia me deixou
#   grandona"), porque a cena 3 e 4 da aula respondem a ele. Nome dela fora da fala e da tela (crédito só o @).
# Veredito: MEIA VERDADE (caixinha: MITO para "definido"). Rosto r1 do banco de reações 6cd9 (cx_r1 "Calma. Tem verdade aí,
#   mas tem porém.", sem crédito). Entrada rk_ent ("Olha só essa notícia", banco) e CTA cta6_serio (banco, sem piada).
# Voz: 4 create_speech por clima SEM <break> e SEM atempo (pausas abertas na edição, tmp_la/voz.py):
#   indignado (abertura) | manso (aula + o que fazer) | neutro (estudo) | alegre (cobrança + fecho).
# EDIÇÃO da aula: CAIXINHA QUE SE DESENHA (cartão creme, aba lima, desenhos que se desenham, Caveat) na pele LAB:
#   o calo de quem capina (fisio_extra/la_mao_enxada, la_mao_calo), a LINHA DA CARGA pontilhada (fluxo) até o braço por
#   dentro (la_braco_fino -> la_braco_forte), "grandona?" (citação do texto dela) e jarra x copinho (la_jarra, la_copinho).
#   Estudo: la_bol101, la_bol49, la_bol52, la_coluna_forte, la_coluna_fraca.
# Depois deste script (ele mesmo roda): entrada.py com rk_ent.
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l5_academia'; P = 'la'
ENT = 2.07                                 # rk_ent.mp4 (entrada.py empurra "t" das camadas, mas não as "abas" do cartão)
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}la_{k}_voz.words.json'))
WA, WB, WC, WO, WE, WD = W('a'), W('b'), W('c'), W('o'), W('e'), W('d')
DA, DB, DC, DO, DE, DD = [round(dur_de(f'{M}la_{k}_voz.wav'), 3) for k in 'abcoed']
vd = 6.46                                  # la_viral.mp4 (6,467 s de vídeo, 6,45 de áudio)
R1D = 3.87                                 # la_r1.mp4: "porém." termina em 3,37 s; 0,5 s de folga
CTAD = 3.01                                # la_cta.mp4 (cta6_serio): "curte." termina em 2,42 s
r1 = round(vd + R1D, 2)
tA = round(r1 + 0.15, 2)
tB = round(tA + DA + 0.7, 2)
tC = round(tB + DB + 0.75, 2)
tO = round(tC + DC + 0.65, 2)
tE = round(tO + DO + 0.6, 2)
c1 = round(tE + DE + 0.15, 2)
c2 = round(c1 + CTAD, 2)
tD = round(c2 + 0.15, 2)
dur = round(tD + DD + 1.2, 2)
mk_ = lambda T0, WW: (lambda i: round(T0 + WW[i]['s'], 3))
a, b, e, o, q, f = mk_(tA, WA), mk_(tB, WB), mk_(tC, WC), mk_(tO, WO), mk_(tE, WE), mk_(tD, WD)
AF = tC                                    # fim visual da aula
BR, AMAR, VERDE, VERM, CINZA, TINTA = "#ffffff", "#ffd400", "#3ddc84", "#ff4d5a", "#c9ccd2", "#1c1a17"
SH = "text-shadow:6px 6px 0 rgba(0,0,0,.45)"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}
from PIL import ImageFont
_FA = {}
def nlin(txt, tam, w):
    fo = _FA.setdefault(tam, ImageFont.truetype('assets/fonts/Anton-Regular.ttf', tam))
    n, cur = 1, ''
    for wd in txt.split():
        tt = (cur + ' ' + wd).strip()
        if fo.getlength(tt) > w and cur: n += 1; cur = wd
        else: cur = tt
    return n
LINHAS = []
def TT(t, d, txt, y=300, fz=130, cor=BR, **k):
    LINHAS.append((txt, nlin(txt.replace('\\n', ' '), fz, 940)))
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SH, vel=0.09, **k); L["fixo"] = True; return L
def GIG(t, d, txt, y=700, tam=420, cont=False, cor="rgba(198,255,61,.10)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12, "fixo": True,
         "x": [1100, -int(len(txt) * tam * 0.5)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=40, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def DS(t, d, formas, cor=AMAR, lw=14, z=44, vel=0.45):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel, "fixo": True}
def PIL(t, d, txt, x, y, w=600, tam=90, cor=AMAR, fundo="rgba(6,16,12,.9)", z=47):
    LINHAS.append((txt, nlin(txt, tam, w - 30)))
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"{tam}px Anton", "cor": cor, "alinha": "center",
            "txt": txt, "z": z, "entra": "pop", "fixo": True, "css": f"border:7px solid {cor};border-radius:30px;padding:2px 0 8px;background:{fundo}"}
def SELO(t, d, txt, cor="#ff2d3d", cor_txt="#ffffff"):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": cor_txt,
            "alinha": "center", "txt": txt, "css": f"letter-spacing:3px;background:{cor};border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}
def FN(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 214], "w": 1000, "fonte": "600 26px Montserrat", "cor": "#ffffff",
            "alinha": "center", "txt": txt, "z": 70, "fixo": True, "css": "text-shadow:0 2px 6px #000;background:rgba(0,0,0,.45);border-radius:10px;padding:4px 10px"}
# caixinha: título Anton em tinta escura e nota Caveat dentro do cartão creme
def FR(t, d, txt, tam=112, y=385, cor=TINTA):
    LINHAS.append((txt, nlin(txt, tam, 890)))
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [95, y], "w": 890, "fonte": f"{tam}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 45, "anim": "palavras", "vel": 0.09, "fixo": True}
def NOTA(t, d, txt, x, y, w=420, tam=96, cor="#c0392b", rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg)", "fixo": True}

# ================= abertura: viral em tela dividida + caixinha =================
c = abertura(P, vd, "via @rileyjourdan", "center 38%", "Mito ou verdade?", "Largar a academia deixa o corpo definido?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 780, "suf": " MIL VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta":
        L["escolha"] = 0; L["t_escolha"] = 3.3
# texto que estava na tela dela (pedaço A, y ~1278 do original = ~1013 na caixa): tradução por cima, fica até o fim da caixinha
c += [{"tipo": "texto", "t": 0.12, "d": 4.1, "xy": [110, 880], "w": 860, "fonte": "800 80px Montserrat", "cor": "#111111", "alinha": "center",
       "txt": "“a academia me deixou grandona”", "z": 34, "entra": "pop", "fixo": True,
       "css": "background:rgba(255,255,255,.95);border-radius:16px;padding:6px 10px 8px;box-shadow:0 6px 18px rgba(0,0,0,.35)"},
      {"tipo": "glitch", "t": 2.36, "d": 0.16}]          # emenda dos dois pedaços do viral
# r1: "Calma. Tem verdade aí, mas tem porém." (painel cobre o quadro parado dela; a resposta grande logo depois do viral)
PAINEL = "background:#0b1512;border-radius:14px;height:909px;box-sizing:border-box;line-height:1.02;" + SH
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(R1D - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "150px Anton", "cor": BR, "alinha": "center",
       "txt": "MAIS MAGRA?\\nPODE.", "z": 55, "entra": "pop", "fixo": True, "css": PAINEL + ";padding:70px 30px 0"},
      {"tipo": "texto", "t": round(vd + 2.3, 2), "d": round(R1D - 2.3, 2), "xy": [70, 600], "w": 940, "fonte": "150px Anton", "cor": AMAR, "alinha": "center",
       "txt": "DEFINIDA?\\nAÍ NÃO.", "z": 56, "entra": "zoom", "fixo": True, "css": SH},
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + "la_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (indignado): cada uma escolhe; emagrecer sem academia dá; definido é músculo =================
A2, A3, A4, A5 = [round(a(i) - 0.25, 3) for i in (8, 13, 25, 29)]
QUOTE = "background:#ffffff;border-radius:22px;padding:26px 30px 30px;box-shadow:0 20px 50px rgba(0,0,0,.5);transform:rotate(-2deg)"
c += [GL(r1), FL(r1), SELO(tA + 0.2, tB - tA - 0.25, "● CHECAGEM · O QUE A CIÊNCIA DIZ"),
      # A1 "Cada uma escolhe o visual que quer, tá?"
      GIG(tA, A2 - tA, "VISUAL", y=1150, tam=460, cont=True, cor="rgba(198,255,61,.30)"),
      TT(tA + 0.02, A2 - tA - 0.07, "CADA UMA ESCOLHE O VISUAL", y=330, fz=120),
      DS(a(6), A2 - a(6) - 0.05, [{"k": "check", "c": [540, 1180], "s": 110}], cor=VERDE, lw=26),
      # A2 "E eu não examinei ninguém." -> fala só da frase
      FL(A2),
      TT(A2 + 0.02, A3 - A2 - 0.04, "NÃO EXAMINEI NINGUÉM", y=600, fz=170),
      GIG(A2, A3 - A2, "NINGUÉM", y=1250, tam=420, cont=True, cor="rgba(255,212,0,.30)", ida=False),
      # A3 "Emagrecer sem academia, dá: quem manda na balança é mais o prato."
      FL(A3),
      GIG(A3, A4 - A3, "PRATO", y=1300, tam=480, ida=False),
      TT(A3 + 0.02, a(17) - A3 - 0.1, "EMAGRECER SEM ACADEMIA? DÁ.", y=330, fz=130),
      TT(a(17) - 0.05, A4 - a(17) + 0.0, "QUEM MANDA: O PRATO", y=330, fz=140, cor=AMAR, xy=[140, 330], w=800),
      FIS(a(17), A4 - a(17) - 0.05, [{"k": "balanca", "xy": [330, 1050], "s": 0.9, "t": 0.0},
                                     {"k": "prato", "xy": [760, 1060], "s": 0.95, "t": round(a(24) - a(17), 3)}],
          pulsos=[{"o": 1, "t": round(a(24) - a(17) + 0.3, 3)}]),
      # A4 "Agora, definido sem peso?"
      FL(A4),
      TT(A4 + 0.02, A5 - A4 - 0.07, "DEFINIDO SEM PESO?", y=330, fz=150, cor=AMAR),
      {"tipo": "texto", "t": round(A4 + 0.1, 3), "d": round(A5 - A4 - 0.15, 3), "xy": [40, 640], "w": 1000, "fonte": "640px Anton", "cor": BR,
       "alinha": "center", "txt": "?", "z": 42, "entra": "zoom", "fixo": True, "css": "text-shadow:14px 14px 0 rgba(0,0,0,.35)"},
      # A5 "Definido é músculo."
      FL(A5),
      GIG(A5, tB - A5, "DEFINIDO", y=1380, tam=400, cont=True, cor="rgba(61,220,132,.35)"),
      TT(A5 + 0.02, tB - A5 - 0.05, "DEFINIDO = MÚSCULO", y=330, fz=150, cor=VERDE),
      FIS(A5 + 0.05, tB - A5 - 0.05, [{"k": "musculo", "xy": [540, 960], "s": 1.25, "t": 0.1}],
          pulsos=[{"o": 0, "t": round(a(31) - A5, 3)}])]
SFX_A = [{"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45},
         {"src": "boing", "t": a(6), "gain": 0.25},
         {"src": "whoosh2", "t": A2, "gain": 0.3}, {"src": "papel", "t": a(10), "gain": 0.4}, {"src": "boing", "t": a(11), "gain": 0.22},
         {"src": "whoosh2", "t": A3, "gain": 0.3}, {"src": "boing", "t": a(17), "gain": 0.25}, {"src": "boing", "t": a(24), "gain": 0.22},
         {"src": "whoosh2", "t": A4, "gain": 0.3}, {"src": "scratch", "t": a(27), "gain": 0.22},
         {"src": "whoosh", "t": A5, "gain": 0.35, "pico": 0.45}, {"src": "boom", "t": a(31), "gain": 0.4, "pico": 0.3, "d": 1.2}]

# ================= B (manso): AULA na CAIXINHA QUE SE DESENHA =================
S1b, S2, S2b, S3, S4 = round(b(6) - 0.25, 3), round(b(12) - 0.25, 3), round(b(16) - 0.2, 3), round(b(21) - 0.25, 3), round(b(27) - 0.25, 3)
CART = [60, 330, 960, 1250]                 # cartão creme: x 60..1020, y 330..1580
c += [GL(tB), FL(tB), SELO(tB + 0.2, AF - tB - 0.25, "● AULA RÁPIDA", cor=AMAR, cor_txt="#10210f"),
      {"tipo": "cartao", "t": tB, "d": round(AF - tB, 3), "box": CART, "aba": "1 · o calo", "z": 30, "fixo": True, "entra": "pop",
       "abas": [[round(x + ENT, 3), txt] for x, txt in [[S2, "2 · a carga"], [S3, "3 · grandona?"], [S4, "4 · o hormônio"]]]}]
# (1a) "Sabe o calo de quem capina?"
SW = round(b(9) - 0.1, 3)                   # "o corpo": a mão abre e mostra o calo
c += [FR(tB + 0.15, S1b - tB - 0.17, "O CALO", tam=200, y=400),
      FIS(tB + 0.2, round(SW - tB - 0.15, 3), [{"k": "la_mao_enxada", "xy": [540, 1130], "s": 1.25}], pulsos=[{"o": 0, "t": round(b(5) - tB, 3)}]),
      NOTA(b(4), SW - b(4) - 0.03, "esfrega, esfrega...", 380, 1430, w=620, tam=80, cor="#c0392b", rot=-3)]
# (1b) "Onde tem esforço, o corpo engrossa." (a mão abre: o calo aparece onde o cabo esfregava)
c += [FR(S1b, S2 - S1b - 0.02, "ONDE TEM ESFORÇO, ENGROSSA", tam=120),
      FIS(SW, round(S2 - SW + 0.02, 3), [{"k": "la_mao_calo", "xy": [400, 1140], "s": 1.25}], z=41,
          pulsos=[{"o": 0, "t": round(b(11) - SW + 0.5, 3)}]),
      DS(b(11), S2 - b(11) - 0.03, [{"k": "circulo", "c": [400, 1150], "r": [140, 52]}], cor="#e0322b", lw=12),
      NOTA(SW - 0.1, S2 - SW + 0.07, "mais grossa!", 600, 900, w=380, tam=104, cor="#1f6fb2", rot=-4),
      DS(SW + 0.2, S2 - SW - 0.23, [{"k": "seta", "de": [760, 1060], "para": [560, 1140], "curva": 30}], cor="#1f6fb2", lw=11)]
# (2a) "Músculo e osso também:" (a LINHA DA CARGA pontilhada sai do calo e chega no braço por dentro)
BX, BY = 590, 1190
c += [FR(S2, S2b - S2 - 0.02, "MÚSCULO E OSSO", tam=150, y=400),
      FIS(S2 + 0.02, S2b - S2 - 0.02, [{"k": "la_mao_calo", "xy": [215, 800], "s": 0.5}], z=41,
          fluxos=[{"de": [300, 900], "para": [470, 1110], "curva": -30, "cor": "#e0322b", "t": 0.25, "d": 1.6, "n": 5, "r": 12, "viagem": 0.7, "fica": True}]),
      FIS(S2 + 0.1, round(b(18) - S2 - 0.05, 3), [{"k": "la_braco_fino", "xy": [BX, BY], "s": 1.1}], z=42),
      NOTA(b(12) + 0.1, S2b - b(12) - 0.12, "músculo", 690, 900, w=300, tam=92, cor="#c0392b", rot=-4),
      DS(b(12) + 0.25, S2b - b(12) - 0.27, [{"k": "seta", "de": [820, 1000], "para": [740, 1090], "curva": 10}], cor="#c0392b", lw=10),
      NOTA(b(12) + 0.1, S2b - b(12) - 0.12, "osso", 300, 1330, w=240, tam=92, cor="#7a5a20", rot=3),
      DS(b(12) + 0.3, S2b - b(12) - 0.32, [{"k": "seta", "de": [430, 1340], "para": [480, 1215], "curva": -10}], cor="#7a5a20", lw=10)]
# (2b) "com carga, ficam mais firmes." (o haltere entra; a linha da carga desce até o braço; músculo e osso engrossam)
c += [FR(S2b, S3 - S2b - 0.02, "COM CARGA: MAIS FIRMES", tam=120),
      FIS(S2b + 0.02, S3 - S2b - 0.02, [{"k": "haltere", "xy": [BX, 760], "s": 0.5}], z=43, pulsos=[{"o": 0, "t": 0.5}],
          fluxos=[{"de": [BX, 830], "para": [BX, 1000], "curva": 0, "cor": "#e0322b", "t": 0.2, "d": 1.8, "n": 5, "r": 12, "viagem": 0.6,
                   "rotulo": "CARGA", "fica": True}]),
      FIS(S2b + 0.02, round(b(18) - S2b - 0.05, 3), [{"k": "la_braco_fino", "xy": [BX, BY], "s": 1.1}], z=42),
      FIS(round(b(18) - 0.08, 3), round(S3 - b(18) + 0.06, 3), [{"k": "la_braco_forte", "xy": [BX, BY], "s": 1.1}], z=42,
          pulsos=[{"o": 0, "t": 0.5}]),
      DS(b(19), S3 - b(19) - 0.03, [{"k": "seta", "de": [330, 1200], "para": [190, 1200], "curva": 0},
                                    {"k": "seta", "de": [850, 1200], "para": [990, 1200], "curva": 0}], cor="#1f9e4f", lw=14),
      NOTA(b(18) - 0.2, S3 - b(18) + 0.17, "mais firme!", 330, 1400, w=520, tam=104, cor="#1f9e4f", rot=-3)]
# (3) "E ficar grandona não é fácil." (responde ao texto que estava na tela dela)
c += [{"tipo": "texto", "t": round(S3 + 0.05, 3), "d": round(S4 - S3 - 0.07, 3), "xy": [130, 440], "w": 820, "fonte": "700 32px Montserrat",
       "cor": "#5b6670", "alinha": "center", "txt": "estava escrito no vídeo: “a academia...”", "z": 45, "entra": "pop", "fixo": True},
      {"tipo": "texto", "t": round(S3 + 0.05, 3), "d": round(S4 - S3 - 0.07, 3), "xy": [150, 510], "w": 780, "fonte": "italic 700 100px 'Source Serif 4'",
       "cor": TINTA, "alinha": "center", "txt": "“...me deixou grandona”", "z": 46, "entra": "cai", "fixo": True,
       "css": "box-sizing:border-box;background:#ffffff;border-radius:20px;padding:22px 26px 26px;box-shadow:0 14px 30px rgba(0,0,0,.25);transform:rotate(-2deg)"},
      NOTA(S3 + 0.55, S4 - S3 - 0.57, "não é fácil!", 150, 1020, w=780, tam=170, cor="#c0392b", rot=-4),
      DS(b(26), S4 - b(26) - 0.03, [{"k": "sublinhado", "de": [250, 1250], "ate": 830}], cor="#c0392b", lw=14)]
# (4) "No homem, o hormônio que ajuda o músculo a crescer é mais de 15 vezes mais alto." (jarra x copinho)
N15 = round(b(39) - 0.05, 3)
c += [FR(S4, AF - S4 - 0.05, "O HORMÔNIO QUE AJUDA O MÚSCULO A CRESCER", tam=100),
      FIS(S4 + 0.1, AF - S4 - 0.15, [{"k": "la_jarra", "xy": [330, 1215], "s": 0.95, "rotulo": "HOMEM", "rot_y": 220, "t": round(b(28) - S4 - 0.1, 3)},
                                     {"k": "la_copinho", "xy": [760, 1215], "s": 0.95, "rotulo": "MULHER", "rot_y": 238, "t": round(b(30) - S4, 3)}],
          z=42, pulsos=[{"o": 0, "t": round(N15 - S4 + 0.3, 3)}]),
      {"tipo": "numero", "t": N15, "d": round(AF - N15 - 0.05, 3), "xy": [60, 625], "w": 960, "valor": 15, "pre": "MAIS DE ", "suf": "x",
       "tam": 170, "cor": "#c8102e", "sombra": "#6b0a18", "z": 46, "fixo": True, "conta": 0.7, "de": 1},
      DS(round(N15 + 1.1, 3), round(AF - N15 - 1.15, 3), [{"k": "circulo", "c": [330, 1150], "r": [200, 190]}], cor="#1f6fb2", lw=11),
      FN(S4, AF - S4, "Handelsman e col., Endocr Rev 2018: no homem, o hormônio passa de 15 vezes o da mulher · doi 10.1210/er.2018-00020")]
SFX_AULA = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": tB + 0.15, "gain": 0.4},
            {"src": "boing", "t": b(4), "gain": 0.25},
            {"src": "pagina", "t": S1b, "gain": 0.35}, {"src": "boing", "t": b(10), "gain": 0.25}, {"src": "papel", "t": b(11), "gain": 0.3},
            {"src": "pagina", "t": S2, "gain": 0.35}, {"src": "riser", "t": S2 + 0.1, "gain": 0.14, "d": 1.4},
            {"src": "pagina", "t": S2b, "gain": 0.35}, {"src": "boom", "t": S2b + 0.1, "gain": 0.38, "pico": 0.3, "d": 1.0}, {"src": "boing", "t": b(18), "gain": 0.25},
            {"src": "pagina", "t": S3, "gain": 0.35}, {"src": "papel", "t": S3 + 0.2, "gain": 0.35}, {"src": "scratch", "t": b(24), "gain": 0.22},
            {"src": "pagina", "t": S4, "gain": 0.35}, {"src": "boing", "t": b(28), "gain": 0.22}, {"src": "boing", "t": b(30), "gain": 0.22},
            {"src": "riser", "t": N15 - 0.9, "gain": 0.16, "d": 1.0}, {"src": "boom", "t": N15, "gain": 0.45, "pico": 0.3, "d": 1.2}]

# ================= C (neutro): o estudo da Austrália =================
C2, C2b, C3, C4, C5, C6 = round(e(3) - 0.2, 3), round(e(13) - 0.2, 3), round(e(22) - 0.2, 3), round(e(30) - 0.2, 3), round(e(37) - 0.2, 3), round(e(50) - 0.15, 3)
FONTE1 = "Watson e col. (equipe de Belinda Beck), J Bone Miner Res 2018 · 101 mulheres de ~65 anos com osso fraco · doi 10.1002/jbmr.3284"
c += [GL(AF), FL(AF), SELO(AF + 0.2, tO - AF - 0.25, "● CHECAGEM · O QUE A CIÊNCIA DIZ"),
      FN(C2, tO - C2, FONTE1),
      # C1 "Olha que coisa." / C2 "Na Austrália, em 2018, a equipe da pesquisadora Belinda Beck..."
      TT(AF + 0.05, C2 - AF + 0.4, "OLHA QUE COISA", y=330, fz=150),
      {"tipo": "artigo", "t": round(AF + 0.1, 3), "d": round(C2b - AF - 0.12, 3), "box": [150, 560, 780, 720], "z": 36, "fixo": True,
       "revista": "J Bone Miner Res · Austrália · 2018", "titulo": "Peso pesado em quem tem osso fraco", "autores": "equipe de Belinda Beck · Griffith University",
       "rola": 0, "linhas": [{"txt": "Austrália, 2018.", "grifo": e(4)}, {"txt": "Mulheres depois da menopausa.", "grifo": e(10)},
                             {"txt": "8 meses de treino.", "grifo": None}],
       "rodape": "doi 10.1002/jbmr.3284"},
      TT(C2 + 0.47, C2b - C2 - 0.5, "AUSTRÁLIA, 2018", y=330, fz=150, cor=AMAR),
      # C2b "...juntou 101 mulheres depois da menopausa, com osso fraco."
      FL(C2b),
      {"tipo": "numero", "t": round(e(14) - 0.1, 3), "d": round(C3 - e(14) + 0.08, 3), "xy": [0, 300], "valor": 101, "tam": 230, "cor": AMAR,
       "sombra": "#5a4a00", "rotulo": "MULHERES", "z": 46, "fixo": True, "conta": 0.6, "de": 1},
      FIS(C2b + 0.05, C3 - C2b - 0.05, [{"k": "la_bol101", "xy": [540, 1000], "s": 1.0}], z=40),
      PIL(e(16), C3 - e(16) - 0.03, "DEPOIS DA MENOPAUSA", 80, 1230, w=920, tam=100, cor=BR),
      PIL(e(19) - 0.3, C3 - e(19) + 0.27, "OSSO FRACO", 270, 1390, w=540, tam=100, cor=AMAR),
      # C3 "Metade pegou peso pesado, com professor do lado."
      FL(C3),
      TT(C3 + 0.02, C4 - C3 - 0.04, "METADE: PESO PESADO", y=330, fz=140, cor=VERDE),
      FIS(C3 + 0.05, C5 - C3 - 0.07, [{"k": "haltere", "xy": [300, 780], "s": 0.45, "t": round(e(24) - C3, 3)},
                                      {"k": "la_bol49", "xy": [300, 1050], "s": 0.95}], z=40, pulsos=[{"o": 0, "t": round(e(24) - C3 + 0.4, 3)}]),
      PIL(e(26), C5 - e(26) - 0.05, "COM PROFESSOR", 50, 1240, w=470, tam=100, cor=VERDE),
      # C4 "A outra metade, exercício leve em casa."
      FL(C4),
      TT(C4 + 0.02, C5 - C4 - 0.04, "OUTRA METADE: LEVE, EM CASA", y=330, fz=120, cor=BR),
      FIS(C4 + 0.05, C5 - C4 - 0.07, [{"k": "la_bol52", "xy": [780, 1050], "s": 0.85}], z=40),
      PIL(e(33) - 0.1, C5 - e(33) + 0.05, "LEVE, EM CASA", 560, 1240, w=470, tam=100, cor=CINZA),
      # C5 "Em 8 meses, o osso da coluna do peso pesado ganhou quase 3%."
      FL(C5),
      TT(C5 + 0.02, C6 - C5 - 0.04, "8 MESES DEPOIS:", y=330, fz=120, cor=BR),
      TT(C5 + 0.3, C6 - C5 - 0.32, "O OSSO DA COLUNA", y=465, fz=120, cor=BR),
      FIS(C5 + 0.05, tO - C5 - 0.07, [{"k": "la_coluna_forte", "xy": [300, 1010], "s": 0.8, "rotulo": "PESO PESADO", "rot_y": 245, "t": round(e(41) - C5 - 0.1, 3)}],
          z=40, pulsos=[{"o": 0, "t": round(e(49) - C5 + 0.2, 3)}]),
      DS(e(47), tO - e(47) - 0.05, [{"k": "seta", "de": [480, 1180], "para": [480, 900], "curva": 0}], cor=VERDE, lw=16),
      {"tipo": "numero", "t": round(e(48) - 0.05, 3), "d": round(tO - e(48), 3), "xy": [40, 1290], "w": 520, "valor": 2.9, "dec": 1, "pre": "+", "suf": "%",
       "tam": 150, "cor": VERDE, "sombra": "#0b3d22", "z": 46, "fixo": True, "conta": 0.6, "de": 0},
      # C6 "O do leve perdeu um pouco."
      FL(C6),
      TT(C6 + 0.02, tO - C6 - 0.04, "O DO LEVE PERDEU", y=330, fz=124, cor=CINZA),
      FIS(C6 + 0.05, tO - C6 - 0.07, [{"k": "la_coluna_fraca", "xy": [780, 1010], "s": 0.8, "rotulo": "LEVE", "rot_y": 245}], z=40),
      DS(e(53), tO - e(53) - 0.05, [{"k": "seta", "de": [960, 900], "para": [960, 1180], "curva": 0}], cor=CINZA, lw=16),
      {"tipo": "numero", "t": round(C6 + 0.1, 3), "d": round(tO - C6 - 0.1, 3), "xy": [520, 1290], "w": 520, "valor": 1.2, "dec": 1, "pre": "-", "suf": "%",
       "tam": 150, "cor": CINZA, "sombra": "#3a3d42", "z": 46, "fixo": True, "conta": 0.5, "de": 0}]
SFX_EST = [{"src": "whoosh", "t": AF + 0.05, "gain": 0.35, "pico": 0.45}, {"src": "pagina", "t": AF + 0.15, "gain": 0.45},
           {"src": "whoosh2", "t": C2, "gain": 0.3},
           {"src": "riser", "t": e(14) - 1.0, "gain": 0.14, "d": 1.0}, {"src": "boom", "t": e(14), "gain": 0.45, "pico": 0.3, "d": 1.2},
           {"src": "boing", "t": e(16), "gain": 0.22}, {"src": "boing", "t": e(19), "gain": 0.22},
           {"src": "whoosh2", "t": C3, "gain": 0.3}, {"src": "boing", "t": e(24), "gain": 0.25}, {"src": "notif", "t": e(26), "gain": 0.25},
           {"src": "whoosh2", "t": C4, "gain": 0.3}, {"src": "boing", "t": e(33), "gain": 0.22},
           {"src": "whoosh2", "t": C5, "gain": 0.3}, {"src": "riser", "t": e(48) - 1.0, "gain": 0.14, "d": 1.0}, {"src": "boom", "t": e(48), "gain": 0.42, "pico": 0.3, "d": 1.2},
           {"src": "whoosh2", "t": C6, "gain": 0.3}, {"src": "scratch", "t": e(53), "gain": 0.2}]

# ================= O (manso): o que fazer (com ou sem caneta, sem indicar nem contraindicar) =================
O2, O3 = round(o(6) - 0.55, 3), round(o(11) - 0.1, 3)
c += [GL(tO), FL(tO), SELO(tO + 0.2, tE - tO - 0.25, "● O QUE FAZER", cor=VERDE, cor_txt="#06220f"),
      TT(tO + 0.03, O2 - tO - 0.05, "TÁ EMAGRECENDO?", y=330, fz=150),
      PIL(o(2) - 0.05, O3 - o(2) - 0.05, "COM OU SEM CANETA", 140, 720, w=800, tam=100, cor=AMAR),
      FL(O2),
      TT(O2 + 0.02, round(o(12) - O2, 3), "NÃO LARGA O PESO", y=330, fz=150, cor=VERDE, xy=[210, 330], w=660),
      FIS(O2 + 0.05, O3 - O2 - 0.07, [{"k": "haltere", "xy": [540, 1000], "s": 0.95}], z=40, pulsos=[{"o": 0, "t": round(o(9) - O2, 3)}]),
      FL(O3),
      {"tipo": "checklist", "t": O3, "d": round(tE - O3 - 0.02, 3), "box": [150, 620, 780, 500], "z": 36, "fixo": True, "entra": "desliza",
       "titulo": "Com orientação:", "itens": [{"t": round(o(11) - 0.05, 3), "txt": "conversa com o médico", "marca": o(14)},
                                              {"t": o(16), "txt": "treino de força", "marca": o(17)},
                                              {"t": o(18), "txt": "com professor", "marca": o(19)}]},
      FIS(o(16), tE - o(16), [{"k": "musculo", "xy": [540, 1270], "s": 0.7}], z=40, pulsos=[{"o": 0, "t": round(o(19) - o(16) + 0.2, 3)}])]
SFX_O = [{"src": "whoosh", "t": tO + 0.05, "gain": 0.35, "pico": 0.45}, {"src": "boing", "t": o(2), "gain": 0.22},
         {"src": "whoosh2", "t": O2, "gain": 0.3}, {"src": "boom", "t": O2 + 0.1, "gain": 0.35, "pico": 0.3, "d": 1.0},
         {"src": "papel", "t": O3 + 0.05, "gain": 0.4}, {"src": "notif", "t": o(14), "gain": 0.25},
         {"src": "notif", "t": o(17), "gain": 0.25}, {"src": "notif", "t": o(19), "gain": 0.25}]

# ================= E (alegre): cobrança com o botão SEGUIR =================
E_2, E_3 = round(q(6) - 0.15, 3), round(q(11) - 0.1, 3)
BOT = "border-radius:30px;padding:16px 0 24px;box-shadow:0 12px 26px rgba(0,0,0,.3)"
c += [GL(tE), FL(tE),
      TT(tE + 0.03, E_2 - tE - 0.05, "DIETA DA MODA? PODE.", y=330, fz=150),
      DS(q(5), E_2 - q(5) - 0.05, [{"k": "check", "c": [540, 1000], "s": 100}], cor=VERDE, lw=24),
      FL(E_2),
      TT(E_2 + 0.02, c1 - E_2 - 0.02, "LARGAR ESTE VÍDEO SEM SEGUIR?", y=330, fz=130, cor=AMAR),
      {"tipo": "texto", "t": E_2 + 0.2, "d": round(E_3 - E_2 - 0.2, 3), "xy": [270, 900], "w": 540, "fonte": "900 84px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": "SEGUIR", "z": 40, "entra": "pop", "fixo": True, "css": "background:#1f6fe5;" + BOT},
      {"tipo": "texto", "t": E_3, "d": round(c1 - E_3 + 0.02, 3), "xy": [210, 900], "w": 660, "fonte": "900 84px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": "SEGUINDO", "z": 40, "entra": "pop", "fixo": True, "css": "background:#16a34a;" + BOT},
      DS(q(10), round(E_3 - q(10) + 0.4, 3), [{"k": "circulo", "c": [540, 966], "r": [330, 100]}], cor=AMAR, lw=12, z=45),
      {"tipo": "texto", "t": round(q(11), 3), "d": round(c1 - q(11), 3), "xy": [140, 1150], "w": 800, "fonte": "700 120px Caveat", "cor": AMAR,
       "alinha": "center", "txt": "exagero, né?", "z": 46, "entra": "pop", "fixo": True, "css": "transform:rotate(-4deg);" + SH}]
SFX_E = [{"src": "whoosh", "t": tE + 0.05, "gain": 0.35, "pico": 0.45}, {"src": "boing", "t": q(5), "gain": 0.25},
         {"src": "whoosh2", "t": E_2, "gain": 0.3}, {"src": "boing", "t": E_2 + 0.2, "gain": 0.28}, {"src": "notif", "t": E_3, "gain": 0.45}]

# ================= CTA (banco cta6_serio) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": CTAD, "ms": 0, "src": M + "la_cta.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 1.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": round(CTAD - 0.25, 2), "y": 215, "txt": "SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (alegre): fecho + carimbo =================
D2 = round(f(5) - 0.2, 3)
FONTE2 = "Watson e col., J Bone Miner Res 2018 · Handelsman e col., Endocr Rev 2018 · Conteúdo educativo. Converse com o seu médico."
c += [GL(c2), FL(c2),
      GIG(c2, D2 - c2, "PRATO", y=1300, tam=520, ida=False),
      TT(c2 + 0.03, D2 - c2 - 0.04, "AFINA? O PRATO.", y=330, fz=140),
      FIS(tD + 0.05, D2 - tD - 0.05, [{"k": "prato", "xy": [540, 960], "s": 1.15, "t": 0.1}]),
      FL(D2),
      GIG(D2, dur - D2, "PESO", y=1320, tam=520, cont=True, cor="rgba(61,220,132,.35)"),
      TT(D2 + 0.02, dur - D2 - 0.02, "FIRMA? O PESO.", y=330, fz=140, cor=VERDE),
      FIS(D2 + 0.05, dur - D2 - 0.05, [{"k": "musculo", "xy": [540, 830], "s": 0.95, "t": 0.1}, {"k": "haltere", "xy": [540, 1080], "s": 0.55, "t": round(f(6) - D2, 3)}],
          pulsos=[{"o": 0, "t": round(f(6) - D2 + 0.3, 3)}]),
      PIL(f(8), dur - f(8), "DEFINIDO = MÚSCULO", 130, 1210, w=820, tam=100, cor=VERDE),
      {"tipo": "carimbo", "t": round(f(9) + 0.1, 3), "d": round(dur - f(9) - 0.1, 3), "xy": [190, 1440], "txt": "MEIA VERDADE", "tam": 110, "rot": -6,
       "z": 60, "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92)", "fixo": True},
      FN(c2, dur - c2, FONTE2)]

voz = [{"src": M + "la_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "la_viral.words.json", "gain": 0.16},
       {"src": M + "la_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "la_r1.mp4", "t": vd, "ms": 0, "d": R1D, "palavras": M + "la_r1.words.json"},
       {"src": M + "la_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "la_a_voz.words.json"},
       {"src": M + "la_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "la_b_voz.words.json"},
       {"src": M + "la_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "la_c_voz.words.json"},
       {"src": M + "la_o_voz.wav", "t": tO, "ms": 0, "d": DO, "palavras": M + "la_o_voz.words.json"},
       {"src": M + "la_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "la_e_voz.words.json"},
       {"src": M + "la_cta.mp4", "t": c1, "ms": 0, "d": CTAD, "palavras": M + "la_cta.mp4.words.json"},
       {"src": M + "la_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "la_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35}, {"src": "glitch", "t": 2.36, "gain": 0.3},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "whoosh2", "t": vd + 0.05, "gain": 0.35}, {"src": "boing", "t": vd + 2.5, "gain": 0.25},
       *SFX_A, {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, *SFX_EST,
       {"src": "glitch", "t": tO - 0.05, "gain": 0.45}, *SFX_O,
       {"src": "glitch", "t": tE - 0.05, "gain": 0.45}, *SFX_E,
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
       {"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": D2, "gain": 0.3},
       {"src": "boom", "t": f(9) + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.5}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar(PID, dur, 1515, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, c1, 1730], [c1, c2, 1640], [c2, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json'))
# trilha contínua por baixo de toda a narração (nenhuma pausa muda); emendas cruzadas
p['audio']['musica'] = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.2, "fade": 0.6},
                        {"src": "m_investiga", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tO - tB + 0.8, 2), "gain": 0.16, "fade": 0.6},
                        {"src": "m_emocao", "t": round(tO - 0.4, 2), "ms": 0, "d": round(dur - tO + 0.4, 2), "gain": 0.15, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "AF", AF, "tO", tO, "tE", tE, "c1", c1, "c2", c2, "tD", tD, "| aula", round(AF - tB, 2), "s")
for txt, n in LINHAS:
    if n >= 3: print("  3+ linhas:", n, txt)
# entrada de notícia do banco (rk_ent, 6cd9) com a manchete
subprocess.run(["python3", "scripts/entrada.py", PID, M + "rk_ent.mp4", M + "rk_ent.mp4.words.json", str(ENT),
                "LARGAR A ACADEMIA PRA AFINAR?", "a dica que viralizou com 780 mil views no TikTok", "Plantão das Redes"], check=True)
