import sys; sys.path.insert(0, 'scripts')
from mk import *
# plano_l3_carnivora.py (14/11, lote 3, Papo de Médico): "dieta só de carne derrete a barriga?" (Joe Rogan, repost do TikTok
# @carnivorenutrition), inglês, dublado pela Murilo (original a 0,16 por baixo).
# Trecho (2 pedaços, 11,21 s): 0,00-6,55 "Fiz a dieta carnívora janeiro inteiro. Perdi uns cinco quilos e meio, ganhei muita energia."
#   + 16,95-21,61 "Perdi toda a minha gordura. Perdi a barriga inteira." -> MEIA VERDADE.
#   Fora: 26-34 s (doença de pele dele, CFM) e 47-51 s (cartão de venda de e-book). Marca da camiseta borrada (tmp_cv/prep.py).
# Aula: EDIÇÃO FULL sem b-roll (gigantes Anton cheias e contorno, número 3D, artigo em perspectiva, carimbo), um desenho por cena:
#   fisio_extra/esponja_cheia, esponja_seca, balanca, cv_prato (novos) + figado, musculo, bh_gota, calendario, gordura.
# Voz: 4 blocos HeyGen por clima, SEM atempo: A indignado (r1 + veredito), B manso (aula, pausas 0,5 s), C neutro (estudo), D alegre (fecho).
# r1 = os 5,1 s iniciais do bloco A no avatar 6cd9 (cv_rosto.mp4). Áudio preparado em tmp_cv/prep.py.
# Depois deste script:
#   python3 scripts/entrada.py react_l3_carnivora assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 'SÓ CARNE DERRETE A BARRIGA?' 'Joe Rogan, num vídeo que viralizou no TikTok'
#   python3 scripts/pele.py react_l3_carnivora dossie
P = 'cv'; vd = 11.21
R1D = 5.12
r1 = round(vd + R1D, 2)
DA, DB, DC, DD = 18.435, 22.554, 38.690, 14.854
tA = r1
tB = round(tA + DA + 0.55, 3)
tC = round(tB + DB + 0.55, 3)
c1 = round(tC + DC + 0.35, 2)
c2 = round(c1 + 4.12, 2)
dur = round(c2 + DD + 0.6, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3); f = lambda v: round(c2 + v, 3)
TINTA, VERM, AZUL, OURO, VERDE = '#1c1a17', '#b3121f', '#1f5fa8', '#9a6400', '#2e7d32'
SP = "text-shadow:5px 5px 0 rgba(0,0,0,.14)"
def TT(t, d, txt, y=330, fz=120, cor=TINTA, **k):
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SP, vel=0.09, **k)
def GIG(t, d, txt, y=1250, tam=460, cont=False, cor="rgba(28,26,23,.08)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": 30, "orgaos": orgaos}; L.update(k); return L
def X(t, d, cx, cy, s=70, cor=VERM): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "x", "c": [cx, cy], "s": s}], "espessura": 18, "cor": cor, "z": 45}
def SETA(t, d, de, para, cor=VERM, lw=18, curva=0): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "seta", "de": de, "para": para, "curva": curva}], "espessura": lw, "cor": cor, "z": 45}
def CHECK(t, d, cx, cy, s=60): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 18, "cor": VERDE, "z": 46}
def CIRC(t, d, cx, cy, rx, ry, cor=VERM, lw=12): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "circulo", "c": [cx, cy], "r": [rx, ry]}], "espessura": lw, "cor": cor, "z": 44}
def CARIMBO(t, d, txt, xy, tam=130, rot=-8, cor=VERM): return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": 60, "cor": cor, "blend": "normal", "css": "background:rgba(255,255,255,.9)"}
def FONTE(t, d, txt): return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 196], "w": 1000, "fonte": "600 28px Montserrat", "cor": TINTA, "alinha": "center", "txt": txt, "z": 70, "css": "background:rgba(255,255,255,.55);border-radius:12px;padding:6px 0"}
def NUM(t, d, valor, y=560, cor=VERM, sombra='#d9c49a', **k):
    L = {"tipo": "numero", "t": round(t, 3), "d": round(d, 3), "xy": [0, y], "valor": valor, "tam": 330, "cor": cor, "sombra": sombra, "cor_rotulo": TINTA, "sombra_rotulo": "none", "z": 44}
    L.update(k); return L
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.45}

# ================= abertura: viral em tela dividida + caixinha =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 1100], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 1027], "raio": 14, "pos": "center top",
      "arroba": "via @carnivorenutrition · vídeo do Joe Rogan", "respira": False, "zoom": [[0, 1.0, 0.01], [4.0, 1.05, 0.4], [vd - 2.5, 1.0, 0.4]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [110, 1190], "w": 790, "topo": "Mito ou verdade? 👇", "txt": "Só carne derrete a barriga em um mês?",
      "botoes": ["MITO", "VERDADE"], "vel": 0.025},
     {"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1265], "valor": 3, "suf": " MI VIEWS", "tam": 120},
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 1027], "raio": 14, "sombra": False, "z": 29}]
# r1: resposta grande em cima da foto + rosto embaixo
c += [CARIMBO(vd + 0.1, R1D - 0.12, "MEIA VERDADE", [150, 470], tam=130, rot=-7),
      T(vd + 2.6, round(R1D - 2.62, 2), "O QUE SAI PRIMEIRO?", y=790, f="110px Anton", cor="#f2c230", css="text-shadow:8px 8px 0 #000"),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + P + "_rosto.mp4", "box": [0, 1140, 1080, 780], "pos": "center 32%", "entra": "desliza", "z": 45}]

# ================= A (indignado): veredito =================
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1),
      # A1 meia verdade (a caixinha volta com os dois botões e o carimbo)
      GIG(a(0), 3.2, "MEIA", y=1350, tam=520, cont=True, cor="rgba(179,18,31,.28)"),
      {"tipo": "pergunta", "t": a(0), "d": 3.2, "xy": [110, 360], "w": 860, "topo": "Mito ou verdade? 👇", "txt": "Só carne derrete a barriga em um mês?",
       "botoes": ["MITO", "VERDADE"], "vel": 0.012},
      CARIMBO(a(0.85), 2.35, "MEIA VERDADE", [120, 980], tam=150, rot=-6),
      FL(a(3.2)),
      # A2 eu não examinei ninguém, falo da frase
      GIG(a(3.2), 4.0, "FRASE", y=1380, tam=480),
      TT(a(3.25), 3.5, "EU NÃO EXAMINEI NINGUÉM.", y=330, fz=118),
      TT(a(4.6), 2.6, "“PERDI TODA A MINHA GORDURA”", y=860, fz=118, cor=VERM, anim=None, entra="zoom"),
      CIRC(a(5.0), 2.2, 540, 990, 470, 190),
      FL(a(7.2)),
      # A3 uns 5 kg no primeiro mês acontece
      GIG(a(7.2), 5.75, "5 QUILOS", y=1380, tam=400, cont=True, cor="rgba(28,26,23,.22)", ida=False),
      NUM(a(7.2), 5.75, 5, y=330, pre="-", suf=" KG", rotulo="no primeiro mês"),
      TT(a(9.2), 2.2, "CORTANDO PÃO E ARROZ", y=920, fz=118),
      TT(a(11.4), 1.55, "ACONTECE.", y=920, fz=150, cor=VERDE, anim=None, entra="zoom"),
      CHECK(a(11.5), 1.45, 540, 1250, 70),
      FL(a(12.95)),
      # A4 toda a gordura em um mês?
      GIG(a(12.95), 3.6, "GORDURA", y=1380, tam=440),
      TT(a(13.0), 3.55, "TODA A GORDURA EM UM MÊS?", y=330, fz=125),
      FIS(a(12.95), 3.6, [{"k": "calendario", "xy": [540, 1000], "s": 1.25, "t": 0.15}], pulsos=[{"o": 0, "t": 1.6}, {"o": 0, "t": 2.6}]),
      FL(a(16.55)),
      # A5 aí não
      GIG(a(16.55), round(tB - a(16.55), 3), "NÃO", y=1300, tam=560, cont=True, cor="rgba(179,18,31,.30)", ida=False),
      TT(a(16.6), round(tB - a(16.6), 3), "AÍ, NÃO.", y=700, fz=280, cor=VERM, anim=None, entra="zoom")]

# ================= B (manso): AULA, uma ideia por cena =================
c += [FL(tB)]
# S1 o corpo guarda açúcar no fígado e nos músculos
c += [GIG(b(0), 7.05, "RESERVA", y=1420, tam=420, cont=True, cor="rgba(154,100,0,.30)"),
      TT(b(0.05), 2.8, "FUNCIONA ASSIM", y=330, fz=135),
      TT(b(2.85), 4.2, "O CORPO GUARDA AÇÚCAR", y=330, fz=125),
      FIS(b(0), 7.05, [{"k": "figado", "xy": [330, 1000], "s": 1.0, "t": 2.95, "rotulo": "FÍGADO", "rot_y": 175},
                      {"k": "musculo", "xy": [770, 1230], "s": 0.95, "t": 3.15, "rotulo": "MÚSCULO", "rot_y": 175}],
          fluxos=[{"de": [540, 620], "para": [330, 900], "curva": -60, "cor": "#f2c230", "t": 4.4, "d": 2.4, "n": 6, "rotulo": "AÇÚCAR", "viagem": 0.9},
                  {"de": [560, 620], "para": [770, 1120], "curva": 60, "cor": "#f2c230", "t": 4.7, "d": 2.2, "n": 6, "viagem": 1.0}],
          pulsos=[{"o": 0, "t": 5.2}, {"o": 1, "t": 5.9}]),
      FL(b(7.05))]
# S2 como uma esponja: 1 g segura 3 a 4 g de água
c += [GIG(b(7.05), 5.9, "ESPONJA", y=1480, tam=400, cor="rgba(31,95,168,.16)", ida=False),
      TT(b(7.1), 1.8, "COMO UMA ESPONJA", y=290, fz=130),
      TT(b(8.9), 4.05, "CADA 1 g DE AÇÚCAR SEGURA", y=290, fz=110),
      FIS(b(7.05), 5.9, [{"k": "esponja_cheia", "xy": [540, 820], "s": 1.25, "t": 0.15}], pulsos=[{"o": 0, "t": 1.0}, {"o": 0, "t": 4.6}]),
      NUM(b(10.3), 2.65, 4, y=1110, cor=AZUL, sombra='#9fb7d6', pre="3 A ", suf=" g", de=4, conta=0.01, rotulo="de água", tam=300),
      FONTE(b(7.05), 5.9, "Kreitzman e col., Am J Clin Nutr 1992 · doi 10.1093/ajcn/56.1.292S"),
      FL(b(12.95))]
# S3 cortou pão e arroz?
c += [GIG(b(12.95), 2.65, "PÃO E ARROZ", y=1450, tam=360, cont=True, cor="rgba(28,26,23,.22)"),
      TT(b(13.0), 2.6, "CORTOU PÃO E ARROZ?", y=330, fz=130),
      FIS(b(12.95), 2.65, [{"k": "cv_prato", "xy": [540, 1000], "s": 1.6, "t": 0.05}]),
      X(b(14.0), 1.6, 540, 1010, s=170),
      FL(b(15.6))]
# S4 em poucos dias a esponja seca
c += [GIG(b(15.6), 3.25, "POUCOS DIAS", y=1450, tam=340, ida=False),
      TT(b(15.65), 3.2, "EM POUCOS DIAS, A ESPONJA SECA", y=300, fz=112),
      FIS(b(15.6), 2.2, [{"k": "esponja_cheia", "xy": [540, 980], "s": 1.25, "t": 0.0},
                         {"k": "calendario", "xy": [860, 690], "s": 0.55, "t": 0.3}],
          encolhe=[{"o": 0, "t": 0.7, "para": 0.85, "d": 1.3}], pulsos=[{"o": 1, "t": 0.9}, {"o": 1, "t": 1.5}]),
      FIS(b(17.8), 1.05, [{"k": "esponja_seca", "xy": [540, 990], "s": 1.15, "t": 0.0},
                          {"k": "calendario", "xy": [860, 690], "s": 0.55, "t": 0.0}]),
      FL(b(18.85))]
# S5 a água sai no xixi e a balança despenca
S5d = round(tC - b(18.85), 3)
c += [GIG(b(18.85), S5d, "ÁGUA", y=1440, tam=480, cor="rgba(31,95,168,.18)"),
      TT(b(18.9), S5d - 0.05, "SAI NO XIXI, A BALANÇA CAI", y=300, fz=112),
      FIS(b(18.85), S5d, [{"k": "bh_gota", "xy": [270, 880], "s": 0.75, "t": 0.1, "rotulo": "XIXI", "rot_y": 250},
                          {"k": "balanca", "xy": [690, 1080], "s": 1.05, "t": 2.0}],
          fluxos=[{"de": [270, 1060], "para": [270, 1420], "curva": 0, "cor": "#7fd3ff", "t": 0.8, "d": 2.2, "n": 6, "viagem": 0.8}],
          pulsos=[{"o": 1, "t": 2.9}, {"o": 1, "t": 3.4}]),
      SETA(b(21.6), round(tC - b(21.6), 3), [960, 860], [960, 1330], cor=VERM, lw=20),
      FL(tC)]

# ================= C (neutro): o estudo =================
c += [GIG(e(0), 3.5, "ÁGUA", y=1440, tam=480, cont=True, cor="rgba(31,95,168,.30)"),
      TT(e(0.05), 3.45, "BOA PARTE É ÁGUA, NÃO GORDURA", y=330, fz=118),
      CARIMBO(e(1.4), 2.1, "É ÁGUA", [250, 860], tam=190, rot=-8, cor=AZUL),
      FL(e(3.5)),
      # C2 o estudo de 1976
      {"tipo": "artigo", "t": e(3.5), "d": 9.8, "box": [100, 300, 880, 640], "z": 34,
       "revista": "Journal of Clinical Investigation · 1976", "titulo": "Do que é feito o peso que some nos primeiros dias de dieta",
       "autores": "Yang e Van Itallie · 6 pessoas, 10 dias em cada dieta", "rola": 0,
       "linhas": [{"txt": "As mesmas calorias, duas dietas.", "grifo": e(7.5)},
                  {"txt": "Uma quase sem carboidrato.", "grifo": e(9.5)},
                  {"txt": "Outra com comida comum.", "grifo": e(11.0)}],
       "rodape": "doi 10.1172/JCI108519"},
      GIG(e(3.5), 9.8, "1976", y=1480, tam=420, cor="rgba(28,26,23,.10)", ida=False),
      TT(e(3.9), 3.8, "1976: SEIS PESSOAS", y=1040, fz=130),
      TT(e(7.7), 1.8, "MESMAS CALORIAS", y=1040, fz=130, cor=VERM, anim=None, entra="zoom"),
      TT(e(9.5), 3.8, "QUASE SEM CARBOIDRATO OU COMIDA COMUM", y=1040, fz=110),
      FL(e(13.3)),
      # C3a a balança caiu mais rápido
      GIG(e(13.3), 4.3, "MAIS RÁPIDO", y=1450, tam=360, cont=True, cor="rgba(28,26,23,.22)"),
      TT(e(13.35), 4.25, "QUASE SEM CARBOIDRATO, A BALANÇA CAIU MAIS RÁPIDO", y=270, fz=105),
      FIS(e(13.3), 4.3, [{"k": "balanca", "xy": [540, 1080], "s": 1.15, "t": 0.1}], pulsos=[{"o": 0, "t": 2.6}]),
      SETA(e(15.4), 2.2, [880, 880], [880, 1330], cor=VERM, lw=20),
      FL(e(17.6)),
      # C3b 61% era água
      GIG(e(17.6), 4.6, "ÁGUA", y=1440, tam=480, cor="rgba(31,95,168,.18)", ida=False),
      TT(e(17.65), 4.55, "DO PESO QUE SAIU", y=300, fz=125),
      NUM(e(18.4), 3.8, 61, y=520, cor=AZUL, sombra='#9fb7d6', suf="%", rotulo="era água", tam=360),
      FIS(e(17.6), 4.6, [{"k": "bh_gota", "xy": [540, 1310], "s": 0.8, "t": 0.6}], pulsos=[{"o": 0, "t": 2.2}, {"o": 0, "t": 3.4}]),
      FL(e(22.2)),
      # C4 com comida comum, quase 60% era gordura
      GIG(e(22.2), 4.7, "GORDURA", y=1440, tam=440, cor="rgba(154,100,0,.18)"),
      TT(e(22.25), 4.65, "COM COMIDA COMUM", y=300, fz=116),
      NUM(e(23.85), 3.05, 60, y=580, cor=OURO, sombra='#e0c98f', pre="QUASE ", suf="%", de=50, rotulo="era gordura", tam=300),
      FIS(e(22.2), 4.7, [{"k": "gordura", "xy": [540, 1230], "s": 0.9, "t": 1.6}], pulsos=[{"o": 0, "t": 3.5}]),
      FL(e(26.9)),
      # C5 estudo pequeno, 10 dias
      GIG(e(26.9), 3.7, "PEQUENO", y=1440, tam=420, cont=True, cor="rgba(179,18,31,.26)", ida=False),
      TT(e(26.95), 3.65, "ESTUDO PEQUENO: 6 PESSOAS, 10 DIAS", y=300, fz=112),
      FIS(e(26.9), 3.7, [{"k": "calendario", "xy": [540, 1050], "s": 1.15, "t": 0.2}], pulsos=[{"o": 0, "t": 1.9}]),
      FONTE(e(3.5), 27.1, "Yang e Van Itallie, J Clin Invest 1976 · doi 10.1172/JCI108519"),
      FL(e(30.6)),
      # C6 revisão de 32 estudos
      GIG(e(30.6), round(c1 - e(30.6), 3), "32 ESTUDOS", y=1460, tam=360, cor="rgba(28,26,23,.10)"),
      TT(e(30.65), 3.25, "UMA REVISÃO GRANDE", y=300, fz=130),
      NUM(e(31.1), 4.45, 32, y=650, suf=" ESTUDOS", tam=280),
      TT(e(33.9), 1.7, "MESMAS CALORIAS", y=300, fz=130, cor=VERM, anim=None, entra="zoom"),
      TT(e(35.6), round(c1 - e(35.6), 3), "CORTAR CARBOIDRATO NÃO QUEIMA MAIS GORDURA", y=300, fz=118),
      FIS(e(35.6), round(c1 - e(35.6), 3), [{"k": "gordura", "xy": [540, 1020], "s": 1.1, "t": 0.1}], pulsos=[{"o": 0, "t": 1.8}]),
      FONTE(e(30.6), round(c1 - e(30.6), 3), "Hall e Guo, Gastroenterology 2017 · doi 10.1053/j.gastro.2017.01.052")]

# ================= CTA (banco cta6) + fecho (D, alegre) =================
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(f(0), 1.85, "EMAGRECER", y=1400, tam=380, cont=True, cor="rgba(28,26,23,.22)"),
      TT(f(0.05), 1.8, "QUER EMAGRECER?", y=620, fz=170, anim=None, entra="zoom"),
      FL(f(1.85)),
      GIG(f(1.85), 4.7, "ANOS", y=1380, tam=520, cor="rgba(46,125,50,.16)", ida=False),
      TT(f(1.9), 4.65, "UM JEITO DE COMER QUE VOCÊ AGUENTA POR ANOS", y=420, fz=125),
      FIS(f(1.85), 4.7, [{"k": "calendario", "xy": [540, 1180], "s": 0.95, "t": 1.0}], pulsos=[{"o": 0, "t": 2.6}, {"o": 0, "t": 3.6}]),
      FL(f(6.55)),
      GIG(f(6.55), 2.6, "MÉDICO", y=1380, tam=460, cont=True, cor="rgba(28,26,23,.22)"),
      TT(f(6.55), 2.6, "E ACOMPANHA COM SEU MÉDICO", y=560, fz=140),
      FL(f(9.15)),
      GIG(f(9.15), round(dur - f(9.15), 3), "DIAS × MESES", y=1500, tam=300, cor="rgba(28,26,23,.10)"),
      TT(f(9.2), round(dur - f(9.2), 3), "ÁGUA SAI EM DIAS.", y=300, fz=125, cor=AZUL, anim=None, entra="zoom"),
      FIS(f(9.15), round(dur - f(9.15), 3), [{"k": "bh_gota", "xy": [540, 700], "s": 0.55, "t": 0.2},
                                             {"k": "gordura", "xy": [540, 1320], "s": 0.7, "t": 3.2}]),
      TT(f(12.25), round(dur - f(12.25), 3), "GORDURA SAI EM MESES.", y=900, fz=125, cor=OURO, anim=None, entra="zoom"),
      FONTE(f(0), round(dur - f(0), 3), "Yang e Van Itallie, J Clin Invest 1976 · Hall e Guo, Gastroenterology 2017")]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json", "gain": 0.16},
       {"src": M + P + "_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + P + "_rosto.mp4", "t": vd, "ms": 0, "d": R1D, "palavras": M + P + "_r1.words.json"},
       {"src": M + P + "_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + P + "_a_voz.words.json"},
       {"src": M + P + "_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + P + "_b_voz.words.json"},
       {"src": M + P + "_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + P + "_c_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + P + "_d_voz.wav", "t": c2, "ms": 0, "d": DD, "palavras": M + P + "_d_voz.words.json"}]
# trilha por baixo de tudo depois do viral (inclusive CTA), para nenhuma pausa ficar muda
musica = [{"src": "m_investiga", "t": vd, "ms": 0, "d": round(c1 - vd + 0.3, 2), "gain": 0.22, "fade": 0.8},
          {"src": "m_emocao", "t": round(c1 - 0.2, 2), "ms": 0, "d": round(dur - c1 + 0.2, 2), "gain": 0.24, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": 6.55, "gain": 0.3},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": vd + 2.6, "gain": 0.35},
       # A
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1, "gain": 0.5, "pico": 0.45}, {"src": "notif", "t": a(0.1), "gain": 0.4},
       {"src": "boom", "t": a(0.85), "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": a(3.2), "gain": 0.35}, {"src": "scratch", "t": a(5.0), "gain": 0.3},
       {"src": "whoosh", "t": a(7.2), "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": a(11.5), "gain": 0.35},
       {"src": "whoosh2", "t": a(12.95), "gain": 0.35}, {"src": "boing", "t": a(13.15), "gain": 0.25},
       {"src": "boom", "t": a(16.6), "gain": 0.55, "pico": 0.3, "d": 1.5},
       # aula
       {"src": "whoosh", "t": tB, "gain": 0.45, "pico": 0.45}, {"src": "boing", "t": b(3.0), "gain": 0.3}, {"src": "boing", "t": b(3.2), "gain": 0.25},
       {"src": "riser", "t": b(4.4), "gain": 0.2, "d": 1.5},
       {"src": "whoosh2", "t": b(7.05), "gain": 0.35}, {"src": "boing", "t": b(7.2), "gain": 0.3}, {"src": "boom", "t": b(10.3), "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": b(12.95), "gain": 0.35}, {"src": "scratch", "t": b(14.0), "gain": 0.35},
       {"src": "whoosh2", "t": b(15.6), "gain": 0.35}, {"src": "pagina", "t": b(15.9), "gain": 0.3}, {"src": "boing", "t": b(17.8), "gain": 0.3},
       {"src": "whoosh", "t": b(18.85), "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": b(20.85), "gain": 0.3}, {"src": "scratch", "t": b(21.6), "gain": 0.3},
       # estudo
       {"src": "whoosh", "t": tC, "gain": 0.45, "pico": 0.45}, {"src": "boom", "t": e(1.4), "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "pagina", "t": e(3.6), "gain": 0.5}, {"src": "whoosh2", "t": e(7.7), "gain": 0.3}, {"src": "whoosh2", "t": e(9.5), "gain": 0.3},
       {"src": "whoosh2", "t": e(13.3), "gain": 0.35}, {"src": "scratch", "t": e(15.4), "gain": 0.3},
       {"src": "riser", "t": e(16.9), "gain": 0.22, "d": 1.5}, {"src": "boom", "t": e(18.4), "gain": 0.55, "pico": 0.3, "d": 1.5},
       {"src": "whoosh2", "t": e(22.2), "gain": 0.35}, {"src": "boom", "t": e(23.85), "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": e(26.9), "gain": 0.35}, {"src": "pagina", "t": e(27.1), "gain": 0.3},
       {"src": "whoosh", "t": e(30.6), "gain": 0.4, "pico": 0.45}, {"src": "boom", "t": e(31.1), "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": e(33.9), "gain": 0.3}, {"src": "whoosh2", "t": e(35.6), "gain": 0.35},
       # CTA e fecho
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.5},
       {"src": "whoosh2", "t": f(1.85), "gain": 0.35}, {"src": "whoosh2", "t": f(6.55), "gain": 0.35},
       {"src": "whoosh", "t": f(9.15), "gain": 0.4, "pico": 0.45}, {"src": "boom", "t": f(12.25), "gain": 0.55, "pico": 0.3, "d": 1.5}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar("react_l3_carnivora", dur, 317, c, voz, sfx,
       {"r1_fim": r1, "esconde": [[0, 4.1]], "ys": [[4.1, vd, 1480], [vd, r1, 1010], [r1, c1, 1720], [c1, c2, 1560], [c2, dur, 1720]]})
import json
p = json.load(open('planos/react_l3_carnivora.json')); p['audio']['musica'] = musica
json.dump(p, open('planos/react_l3_carnivora.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "tC", tC, "c1", c1, "c2", c2)
