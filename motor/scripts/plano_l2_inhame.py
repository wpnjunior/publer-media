import sys, json; sys.path.insert(0, 'scripts')
from mk import *
# plano_l2_inhame.py (14/11, lote 2, Fertilidade a Dois): "inhame estimula a ovulação" (TikTok @maeaflordapele).
# Wagner: "sem nome e acolhendo" -> nunca dizer o nome dela, crédito só o @, tom acolhedor (muita tentante busca isso).
# Trecho 37,6-47,1 s: "Então o inhame é poderoso sim para estimular a ovulação, para ajudar a produzir muco cervical,
# para ajudar a produzir progesterona, mas ele não faz milagres." -> MITO (ovular/muco/progesterona); "não faz milagre" está certo.
# Aula na edição LOUSA (lousa verde, giz, um desenho por cena, sem b-roll): ovulação (cérebro -> ovário, 2 recados,
# progesterona, muco) e depois inhame -> frasco (vira no laboratório) x inhame -> corpo (não vira). Pele: notícia.
# Voz em blocos por clima, SEM atempo: A neutro (r1 + abertura), B manso (aula), C neutro (estudo), D alegre (fecho).
# Pausas longas aparadas por tmp_ih/prep.py (A/C/D ficam com 0,75 s; B com 0,6 s).
# Depois deste script:
#   python3 scripts/entrada.py react_l2_inhame assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 'INHAME FAZ OVULAR?' 'falaram isso no TikTok' \
#     && python3 scripts/pele.py react_l2_inhame noticia
PID = 'react_l2_inhame'; P = 'ih'
vd = 9.5                                  # viral 37,6-47,1 s
r1 = round(vd + 3.68, 2)                  # rosto 6cd9 "Eu entendo a esperança. Mas não é bem assim, tá?" (3,68 s)
DA, DB, DC, DD = 6.81, 35.92, 21.18, 10.69
tA = r1
tB = round(tA + DA + 0.6, 2)
tC = round(tB + DB + 0.6, 2)
c1 = round(tC + DC + 0.4, 2)              # CTA banco cta6
c2 = round(c1 + 4.12 + 0.05, 2)
dur = round(c2 + DD + 0.6, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3); f = lambda v: round(c2 + v, 3)
BRANCO, AMAR, ROSA, VERM, VERDE = '#ffffff', '#ffd400', '#ff9fb4', '#ff4d4f', '#3ddc84'
GIZ, GAMAR = '#f4f1e8', '#ffe27a'
SOMBRA = "text-shadow:7px 7px 0 #000,0 0 18px rgba(0,0,0,.7)"
GZ = "text-shadow:0 0 3px rgba(255,255,255,.45),5px 6px 0 rgba(0,0,0,.4)"
def TT(t, d, txt, y=330, fz=120, cor=BRANCO, css=SOMBRA, **k):
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=css, vel=0.09, **k)
def TG(t, d, txt, y=300, fz=120, cor=GIZ, **k):       # texto em giz (lousa)
    return TT(t, d, txt, y=y, fz=fz, cor=cor, css=GZ, **k)
def GIG(t, d, txt, y=1250, tam=460, cont=False, cor="rgba(255,255,255,.10)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 2), "d": round(d, 2), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 2), "d": round(d, 2), "z": 30, "orgaos": orgaos}; L.update(k); return L
def X(t, d, cx, cy, s=90, cor=VERM): return {"tipo": "desenho", "t": round(t, 2), "d": round(d, 2), "formas": [{"k": "x", "c": [cx, cy], "s": s}], "espessura": 18, "cor": cor, "z": 45}
def OK(t, d, cx, cy, s=70, cor=VERDE): return {"tipo": "desenho", "t": round(t, 2), "d": round(d, 2), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 18, "cor": cor, "z": 45}
def SETA(t, d, de, para, curva=0, cor=GAMAR, lw=14): return {"tipo": "desenho", "t": round(t, 2), "d": round(d, 2), "formas": [{"k": "seta", "de": de, "para": para, "curva": curva}], "espessura": lw, "cor": cor, "z": 44}
def CIRC(t, d, cx, cy, r, cor=GAMAR, lw=12): return {"tipo": "desenho", "t": round(t, 2), "d": round(d, 2), "formas": [{"k": "circulo", "c": [cx, cy], "r": [r, r], "t": 0}], "espessura": lw, "cor": cor, "z": 44}
FL = lambda t: {"tipo": "flash", "t": round(t, 2), "d": 0.2, "max": 0.5}

# ================= abertura: viral em tela dividida + caixinha =================
c = abertura(P, vd, "via @maeaflordapele", "center 30%", "Mito ou verdade? 👇", "Inhame estimula a ovulação?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 93.6, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta": L["escolha"] = 0
c += [{"tipo": "carimbo", "t": vd + 0.1, "d": r1 - vd - 0.15, "xy": [90, 470], "txt": "NÃO É BEM ASSIM", "tam": 120, "rot": -6, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92)"},
      rosto_r1(P, vd, r1 - vd, 0)]

# ================= A (neutro): o que ela acertou e o que não =================
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1),
      GIG(a(0), 3.6, "MILAGRE", y=1500, tam=400, cont=True, cor="rgba(255,212,0,.35)"),
      FIS(a(0), 3.6, [{"k": "ih_inhame", "xy": [540, 1130], "s": 1.5, "t": 0.1, "rotulo": "INHAME", "rot_y": 175}], pulsos=[{"o": 0, "t": 2.4}]),
      TT(a(0.05), 3.55, "ELA ACERTOU: NÃO FAZ MILAGRE", y=300, fz=118),
      OK(a(2.45), 1.15, 900, 860, s=70),
      FL(a(3.6)),
      GIG(a(3.6), DA + 0.6 - 3.6, "OVULAR?", y=1560, tam=400, ida=False),
      FIS(a(3.6), DA + 0.6 - 3.6, [{"k": "ih_inhame", "xy": [270, 1120], "s": .72, "t": 0.05},
                                    {"k": "ovario_cheio", "xy": [800, 1120], "s": .7, "t": 0.2, "rotulo": "OVÁRIO", "rot_y": 190}]),
      SETA(a(4.25), DA + 0.6 - 4.25, [420, 1120], [640, 1120], curva=-60),
      TT(a(3.62), 1.88, "FAZER OVULAR?", y=330, fz=170, cor=AMAR),
      X(a(5.5), DA + 0.6 - 5.5, 530, 1080, s=110),
      TT(a(5.5), DA + 0.6 - 5.5, "NINGUÉM MOSTROU ISSO", y=330, fz=150, anim=None, entra="zoom")]

# ================= B (manso): AULA NA LOUSA, uma ideia por cena =================
EB = DB + 0.6
c += [{"tipo": "fundo", "t": b(-0.05), "d": round(EB + 0.1, 2), "cor": "#22392f", "textura": "lousa", "z": 9}, FL(tB)]
# S1 como funciona
c += [GIG(b(0), 2.3, "OVULAÇÃO", y=1500, tam=330, cont=True, cor="rgba(244,241,232,.22)"),
      FIS(b(0), 2.3, [{"k": "utero", "xy": [540, 1080], "s": 1.5, "t": 0.1}]),
      TG(b(0.05), 2.25, "COMO A OVULAÇÃO FUNCIONA", y=300, fz=125),
      FL(b(2.3))]
# S2 cérebro manda recado pelo sangue até o ovário
c += [FIS(b(2.3), 3.85, [{"k": "cerebro", "xy": [540, 700], "s": .75, "t": 0.05, "rotulo": "CÉREBRO", "rot_y": 200},
                         {"k": "ovario_cheio", "xy": [540, 1380], "s": .75, "t": 2.6, "rotulo": "OVÁRIO", "rot_y": 190}],
          fluxos=[{"de": [540, 840], "para": [540, 1270], "curva": 0, "cor": GAMAR, "t": 1.2, "d": 2.5, "n": 6, "rotulo": "RECADO", "viagem": 0.9, "fica": True}],
          pulsos=[{"o": 0, "t": 0.9}, {"o": 1, "t": 3.1}]),
      GIG(b(2.3), 3.85, "RECADO", y=1450, tam=420, ida=False),
      TG(b(2.32), 3.83, "O CÉREBRO MANDA UM RECADO", y=250, fz=110),
      FL(b(6.15))]
# S3 o óvulo cresce
c += [FIS(b(6.15), 2.5, [{"k": "ovulo", "xy": [540, 1100], "s": .45, "t": 0.05},
                        {"k": "ovulo", "xy": [540, 1100], "s": 1.0, "t": 1.05, "rotulo": "ÓVULO", "rot_y": 200}]),
      GIG(b(6.15), 2.5, "CRESCE", y=1560, tam=420),
      TG(b(6.17), 2.48, "O ÓVULO CRESCE", y=300, fz=160, cor=GAMAR),
      FL(b(8.65))]
# S4 segundo recado: ele sai
c += [FIS(b(8.65), 3.2, [{"k": "ovario_cheio", "xy": [420, 1250], "s": .8, "t": 0.05, "rotulo": "OVÁRIO", "rot_y": 190},
                        {"k": "ovulo", "xy": [860, 860], "s": .38, "t": 2.0}],
          fluxos=[{"de": [420, 560], "para": [420, 1130], "curva": 0, "cor": ROSA, "t": 0.15, "d": 1.6, "n": 5, "rotulo": "2º RECADO", "viagem": 0.8}],
          pulsos=[{"o": 0, "t": 1.0}, {"o": 0, "t": 1.9}]),
      SETA(b(10.6), 1.25, [560, 1160], [780, 940], curva=-40, cor=GAMAR),
      TG(b(8.67), 3.18, "2º RECADO: O ÓVULO SAI", y=300, fz=125, cor=ROSA),
      FL(b(11.85))]
# S5 o ovário faz a progesterona
c += [FIS(b(11.85), 3.9, [{"k": "ovario_cheio", "xy": [540, 800], "s": .8, "t": 0.05, "rotulo": "OVÁRIO", "rot_y": 185}],
          fluxos=[{"de": [540, 930], "para": [540, 1480], "curva": 0, "cor": GAMAR, "t": 2.3, "d": 1.5, "n": 8, "rotulo": "PROGESTERONA", "viagem": 0.8, "fica": True}],
          pulsos=[{"o": 0, "t": 1.7}, {"o": 0, "t": 2.6}]),
      GIG(b(11.85), 3.9, "PROGESTERONA", y=1560, tam=300, cont=True, cor="rgba(255,226,122,.30)", ida=False),
      TG(b(11.87), 3.88, "O OVÁRIO FAZ A PROGESTERONA", y=280, fz=110),
      FL(b(15.75))]
# S6 o muco muda sozinho, seguindo os recados
c += [FIS(b(15.75), 3.65, [{"k": "utero", "xy": [540, 1020], "s": 1.6, "t": 0.05}], pulsos=[{"o": 0, "t": 1.5}]),
      CIRC(b(16.5), 2.9, 540, 1290, 80, cor=GAMAR, lw=12),
      TG(b(15.77), 3.63, "O MUCO SEGUE OS RECADOS", y=280, fz=120),
      GIG(b(15.75), 3.65, "MUCO", y=1560, tam=440),
      FL(b(19.4))]
# S7 e o inhame? tem uma substância
c += [FIS(b(19.4), 2.7, [{"k": "ih_inhame", "xy": [540, 1120], "s": 1.6, "t": 0.6}], pulsos=[{"o": 0, "t": 1.9}]),
      GIG(b(19.4), 2.7, "INHAME", y=1560, tam=420, cont=True, cor="rgba(244,241,232,.25)"),
      TG(b(19.42), 2.68, "E O INHAME?", y=330, fz=180, cor=GAMAR, anim=None, entra="zoom"),
      FL(b(22.1)),
      FIS(b(22.1), 3.55, [{"k": "ih_inhame", "xy": [540, 1150], "s": 1.3, "t": 0.05, "rotulo": "DIOSGENINA", "rot_y": 180, "cor_rotulo": ROSA}],
          pulsos=[{"o": 0, "t": 2.1}]),
      CIRC(b(23.9), 1.75, 540, 1150, 230, cor=ROSA, lw=12),
      TG(b(22.12), 3.53, "TEM UMA SUBSTÂNCIA", y=330, fz=135),
      FL(b(25.65))]
# S8 no laboratório vira progesterona
c += [FIS(b(25.65), 4.85, [{"k": "ih_inhame", "xy": [260, 1120], "s": .7, "t": 0.05},
                          {"k": "ih_frasco", "xy": [810, 1120], "s": .8, "t": 0.5, "rotulo": "LABORATÓRIO", "rot_y": 245}],
          fluxos=[{"de": [400, 1050], "para": [680, 1050], "curva": -150, "cor": GAMAR, "t": 1.3, "d": 1.6, "n": 5, "rotulo": "QUÍMICA", "viagem": 0.8}],
          pulsos=[{"o": 1, "t": 3.1}]),
      OK(b(28.75), 1.75, 810, 1450, s=70),
      TG(b(25.67), 2.75, "NO LABORATÓRIO...", y=330, fz=150),
      TG(b(28.42), 2.08, "VIRA PROGESTERONA ✓", y=330, fz=140, cor=GAMAR, anim=None, entra="zoom"),
      FL(b(30.5))]
# S9 dentro do corpo, não
c += [FIS(b(30.5), 2.6, [{"k": "ih_inhame", "xy": [260, 1120], "s": .7, "t": 0.05},
                        {"k": "ih_corpo", "xy": [810, 1120], "s": .85, "t": 0.3, "rotulo": "CORPO", "rot_y": 225}],
          fluxos=[{"de": [400, 1050], "para": [680, 1050], "curva": -150, "cor": ROSA, "t": 0.4, "d": 1.2, "n": 4, "viagem": 0.8}]),
      X(b(31.7), 1.4, 810, 1100, s=150),
      TG(b(30.52), 2.58, "NO CORPO: NÃO VIRA", y=330, fz=150, cor=ROSA),
      FL(b(33.1)),
      FIS(b(33.1), EB - 33.1, [{"k": "ih_ferramenta", "xy": [540, 1130], "s": 1.3, "t": 0.05}]),
      X(b(34.3), EB - 34.3, 540, 1130, s=170),
      GIG(b(33.1), EB - 33.1, "FERRAMENTA", y=1580, tam=320, ida=False),
      TG(b(33.12), EB - 33.12, "O CORPO NÃO TEM A FERRAMENTA", y=280, fz=115),
      FL(tC)]

# ================= C (neutro): o estudo =================
c += [GIG(e(0), 1.85, "ESTUDO", y=1350, tam=440, cont=True, cor="rgba(255,212,0,.35)"),
      TT(e(0.03), 1.82, "E QUANDO MEDIRAM?", y=620, fz=150),
      FL(e(1.85)),
      {"tipo": "numero", "t": e(1.85), "d": 5.05, "xy": [0, 360], "valor": 22, "suf": " MULHERES", "tam": 210, "cor": AMAR, "z": 44},
      TT(e(3.35), 3.55, "INHAME 2 VEZES POR DIA, 1 MÊS", y=860, fz=105),
      FIS(e(1.85), 5.05, [{"k": "ih_inhame", "xy": [540, 1330], "s": .95, "t": 1.7}]),
      F(e(1.85), 9.45, "Wu e col., J Am Coll Nutr 2005 · 22 mulheres na menopausa · doi 10.1080/07315724.2005.10719470"),
      FL(e(6.9)),
      FIS(e(6.9), 4.4, [{"k": "cerebro", "xy": [540, 720], "s": .6, "t": 0.05},
                       {"k": "ovario_cheio", "xy": [540, 1260], "s": .6, "t": 0.3}],
          fluxos=[{"de": [540, 830], "para": [540, 1170], "curva": 0, "cor": AMAR, "t": 0.5, "d": 2.4, "n": 5, "viagem": 0.8}]),
      TT(e(6.92), 4.38, "OS RECADOS DA OVULAÇÃO", y=280, fz=115),
      {"tipo": "carimbo", "t": e(9.9), "d": 1.4, "xy": [170, 1400], "txt": "NÃO MUDARAM", "tam": 130, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92)"},
      FL(e(11.3)),
      GIG(e(11.3), 3.9, "PROGESTERONA", y=1450, tam=300, cont=True, cor="rgba(255,159,180,.35)"),
      TT(e(11.32), 3.88, "CREME DE INHAME:\\nPROGESTERONA NÃO SUBIU", y=380, fz=130, cor=AMAR, anim=None, entra="zoom"),
      F(e(11.3), 3.9, "Komesaroff e col., Climacteric 2001 · 23 mulheres na menopausa, creme x placebo, 3 meses · PMID 11428178"),
      FL(e(15.2)),
      GIG(e(15.2), 2.75, "MENOPAUSA", y=1400, tam=380, ida=False),
      TT(e(15.22), 2.73, "ERAM MULHERES NA MENOPAUSA", y=520, fz=135),
      F(e(15.2), 2.75, "Os dois estudos foram com mulheres que já não ovulam"),
      FL(e(17.95)),
      TT(e(17.97), round(c1 - e(17.97), 2), "EM QUEM TENTA ENGRAVIDAR?", y=380, fz=130),
      GIG(e(17.95), round(c1 - e(17.95), 2), "TENTANTE", y=1450, tam=380, cont=True, cor="rgba(255,212,0,.30)"),
      {"tipo": "carimbo", "t": e(20.0), "d": round(c1 - e(20.0), 2), "xy": [100, 900], "txt": "NENHUM ESTUDO", "tam": 112, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.92)"}]

# ================= CTA (banco cta6) + fecho (D, alegre) =================
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      FIS(f(0), 3.4, [{"k": "ih_inhame", "xy": [540, 1130], "s": 1.3, "t": 0.1}]),
      OK(f(1.0), 2.4, 880, 880, s=70),
      TT(f(0.05), 3.35, "INHAME É COMIDA ✓", y=330, fz=150),
      FL(f(3.4)),
      GIG(f(3.4), 2.95, "INVESTIGAÇÃO", y=1250, tam=300, cont=True, cor="rgba(255,212,0,.35)", ida=False),
      TT(f(3.42), 2.93, "NÃO TROCA A INVESTIGAÇÃO", y=420, fz=135, cor=AMAR),
      FL(f(6.35)),
      FIS(f(6.35), 1.6, [{"k": "calendario", "xy": [540, 1130], "s": 1.2, "t": 0.05}]),
      TT(f(6.37), 1.58, "OVULAÇÃO IRREGULAR?", y=330, fz=130, cor=ROSA),
      FL(f(7.95)),
      FIS(f(7.95), round(dur - f(7.95), 2), [{"k": "coracao_afeto", "xy": [540, 1120], "s": 1.2, "t": 0.05}]),
      TT(f(7.97), round(dur - f(7.97), 2), "VOCÊS DOIS NO MÉDICO", y=330, fz=140, cor=AMAR, anim=None, entra="zoom"),
      F(f(0), round(dur - f(0), 2), "Wu e col., J Am Coll Nutr 2005 · Komesaroff e col., Climacteric 2001 · conteúdo educativo")]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json"},
       {"src": M + P + "_rosto.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + P + "_rosto.words.json"},
       {"src": M + P + "_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + P + "_a_voz.words.json"},
       {"src": M + P + "_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + P + "_b_voz.words.json"},
       {"src": M + P + "_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + P + "_c_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + P + "_d_voz.wav", "t": c2, "ms": 0, "d": DD, "palavras": M + P + "_d_voz.words.json"}]
# trilha contínua por baixo de TODA a narração (m_investiga só tem 23 s: um trecho por bloco, com emenda cruzada)
musica = [{"src": "m_noticia", "t": round(r1 - 0.3, 2), "ms": 0, "d": round(tB - r1 + 0.8, 2), "gain": 0.30, "fade": 0.5},
          {"src": "m_emocao", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tC - tB + 0.9, 2), "gain": 0.30, "fade": 0.6},
          {"src": "m_investiga", "t": round(tC - 0.4, 2), "ms": 0, "d": round(c1 - tC + 0.6, 2), "gain": 0.30, "fade": 0.6},
          {"src": "m_emocao", "t": round(c2 - 0.3, 2), "ms": 2.0, "d": round(dur - c2 + 0.3, 2), "gain": 0.28, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1, "gain": 0.5, "pico": 0.45},
       {"src": "boing", "t": a(0.15), "gain": 0.3}, {"src": "boing", "t": a(2.45), "gain": 0.35},
       {"src": "whoosh2", "t": a(3.6), "gain": 0.4}, {"src": "scratch", "t": a(5.5), "gain": 0.35},
       # aula
       {"src": "whoosh", "t": tB, "gain": 0.45, "pico": 0.45}, {"src": "papel", "t": b(0.1), "gain": 0.3},
       {"src": "whoosh2", "t": b(2.3), "gain": 0.35}, {"src": "boing", "t": b(2.35), "gain": 0.28}, {"src": "boing", "t": b(4.9), "gain": 0.28},
       {"src": "whoosh2", "t": b(6.15), "gain": 0.35}, {"src": "boing", "t": b(7.2), "gain": 0.3},
       {"src": "whoosh2", "t": b(8.65), "gain": 0.35}, {"src": "riser", "t": b(9.2), "gain": 0.2, "d": 1.4}, {"src": "boing", "t": b(10.65), "gain": 0.3},
       {"src": "whoosh2", "t": b(11.85), "gain": 0.35}, {"src": "boing", "t": b(14.2), "gain": 0.28},
       {"src": "whoosh2", "t": b(15.75), "gain": 0.35}, {"src": "scratch", "t": b(16.5), "gain": 0.25},
       {"src": "whoosh", "t": b(19.4), "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": b(20.0), "gain": 0.3},
       {"src": "whoosh2", "t": b(22.1), "gain": 0.35}, {"src": "scratch", "t": b(23.9), "gain": 0.25},
       {"src": "whoosh2", "t": b(25.65), "gain": 0.35}, {"src": "riser", "t": b(26.9), "gain": 0.2, "d": 1.5}, {"src": "boing", "t": b(28.75), "gain": 0.35},
       {"src": "whoosh2", "t": b(30.5), "gain": 0.35}, {"src": "scratch", "t": b(31.7), "gain": 0.35},
       {"src": "whoosh2", "t": b(33.1), "gain": 0.35}, {"src": "scratch", "t": b(34.3), "gain": 0.3},
       # estudo
       {"src": "whoosh", "t": tC, "gain": 0.45, "pico": 0.45}, {"src": "pagina", "t": e(0.1), "gain": 0.4},
       {"src": "boom", "t": e(1.9), "gain": 0.5, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": e(6.9), "gain": 0.35},
       {"src": "boom", "t": e(9.9), "gain": 0.5, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": e(11.3), "gain": 0.35}, {"src": "whoosh2", "t": e(12.92), "gain": 0.3},
       {"src": "whoosh2", "t": e(15.2), "gain": 0.35}, {"src": "whoosh2", "t": e(17.95), "gain": 0.35}, {"src": "boom", "t": e(20.0), "gain": 0.55, "pico": 0.3, "d": 1.3},
       # CTA e fecho
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.5},
       {"src": "boing", "t": f(1.0), "gain": 0.35}, {"src": "whoosh2", "t": f(3.4), "gain": 0.35}, {"src": "whoosh2", "t": f(6.35), "gain": 0.35}, {"src": "whoosh2", "t": f(7.95), "gain": 0.35}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar(PID, dur, 237, c, voz, sfx, {"r1_fim": r1, "esconde": [[0, 4.1]], "ys": [[4.1, vd, 1440], [vd, r1, 1000], [r1, c1, 1730], [c2, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json')); p['audio']['musica'] = musica
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tB", tB, "tC", tC, "c1", c1, "c2", c2)
