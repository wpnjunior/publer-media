# plano_l3_doenca.py (14/11, lote 3, Caneta com Músculo): "pegar doença pra emagrecer" (perder 5 kg numa semana doente é emagrecer?)
# Viral TikTok @isabellalacerda_nutri (nutricionista), trecho 4,30-15,13 (10,83 s): "Não é de hoje que conteúdos exaltando a magreza
# estão em alta nas redes sociais. Comentário sobre querer contrair doenças, porque assim você consegue perder cinco quilos em uma
# semana." -> concordamos com ela (MITO: doente não perde 5 kg de GORDURA numa semana). Nome dela fora da fala e da tela (só o @).
# Print borrado da terceira pessoa (6,79-9,30 s no corte) recebeu borrão extra (tmp_de/prep_viral.py). Fim do vídeo dela (propaganda) fora.
# Tema vizinho de transtorno alimentar: tom acolhedor, sem humor; CTA sério ("Se te ajudou, segue e curte").
# Rosto 6cd9: UM clipe HeyGen com r1 ("Ela está certa. A balança desce, mas olha o que desce.") + CTA sério, cortado por ms.
# Voz: blocos HeyGen por clima SEM <break> e sem atempo; pausas de 0,8-1,0 s abertas na edição (tmp_de/voz.py):
#   A indignado (r1 + veredito), B manso (aula + CTA), E manso (frase "Corpo doente precisa..."), C neutro (estudo + fecho).
# AULA: uva e uva-passa (o Papo usa a esponja em 05/12), em CARTÕES que caem um por vez sobre a pele DOSSIÊ (papel),
#   uma ideia por cartão; desenhos novos fisio_extra/uva.svg e uva_passa.svg.
# Depois deste script:
#   python3 scripts/entrada.py react_l3_doenca assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     '“PEGAR DOENÇA PRA EMAGRECER”?' 'o alerta de uma nutricionista que viralizou' && python3 scripts/pele.py react_l3_doenca dossie
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l3_doenca'; P = 'de'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}de_{k}_voz.words.json'))
WA, WB, WC, WF, WD = W('a'), W('b'), W('c'), W('f'), W('d')
DA, DB, DC, DF, DD = [round(dur_de(f'{M}de_{k}_voz.wav'), 3) for k in 'abcfd']
vd = 10.83
R1D = 4.34                      # r1: última palavra termina em 3,844 s no clipe; 0,5 s de folga
CTA_MS, CTA_D = 4.67, 3.01      # CTA no mesmo clipe: "Se" em 4,824, "curte." termina em 7,09; 0,59 s de folga
r1 = round(vd + R1D, 2)
tA = round(r1 + 0.15, 3)
tB = round(tA + DA + 0.6, 3)
tC = round(tB + DB + 0.75, 3)
tF = round(tC + DC + 0.65, 3)
c1 = round(tF + DF + 0.1, 3)
c2 = round(c1 + CTA_D, 3)
tD = round(c2 + 0.15, 3)
dur = round(tD + DD + 1.5, 2)
a = lambda i: round(tA + WA[i]['s'], 3); ae = lambda i: round(tA + WA[i]['e'], 3)
b = lambda i: round(tB + WB[i]['s'], 3); be = lambda i: round(tB + WB[i]['e'], 3)
e = lambda i: round(tC + WC[i]['s'], 3); ee = lambda i: round(tC + WC[i]['e'], 3)
g = lambda i: round(tF + WF[i]['s'], 3); ge = lambda i: round(tF + WF[i]['e'], 3)
h = lambda i: round(tD + WD[i]['s'], 3)
TINTA, VERM, AZUL, OURO, VERDE = '#1c1a17', '#b3121f', '#1f5fa8', '#9a6400', '#2e7d32'
SP = "text-shadow:5px 5px 0 rgba(0,0,0,.14)"
def TT(t, d, txt, y=330, fz=120, cor=TINTA, z=40, **k):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SP, vel=0.09, **k); L["z"] = z; return L
def GIG(t, d, txt, y=1250, tam=460, cont=False, cor="rgba(28,26,23,.08)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "cor_rotulo": "#ffffff"}; L.update(k); return L
def SETA(t, d, de, para, cor=VERM, lw=18, curva=0, z=45): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "seta", "de": de, "para": para, "curva": curva}], "espessura": lw, "cor": cor, "z": z}
def XX(t, d, cx, cy, s=70, cor=VERM, z=45): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "x", "c": [cx, cy], "s": s}], "espessura": 18, "cor": cor, "z": z}
def CHECK(t, d, cx, cy, s=60, z=46): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 18, "cor": VERDE, "z": z}
def CIRC(t, d, cx, cy, rx, ry, cor=VERM, lw=12, z=44): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "circulo", "c": [cx, cy], "r": [rx, ry]}], "espessura": lw, "cor": cor, "z": z}
def CARIMBO(t, d, txt, xy, tam=130, rot=-8, cor=VERM, z=60): return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": z, "cor": cor, "blend": "normal", "css": "background:rgba(255,255,255,.9)"}
def FONTE(t, d, txt): return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 196], "w": 1000, "fonte": "600 28px Montserrat", "cor": TINTA, "alinha": "center", "txt": txt, "z": 70, "css": "background:rgba(255,255,255,.55);border-radius:12px;padding:6px 0"}
def NUM(t, d, valor, y=560, cor=VERM, sombra='#d9c49a', z=44, **k):
    L = {"tipo": "numero", "t": round(t, 3), "d": round(d, 3), "xy": [0, y], "valor": valor, "tam": 300, "cor": cor, "sombra": sombra, "cor_rotulo": TINTA, "sombra_rotulo": "none", "z": z}
    L.update(k); return L
def CARD(t, d, aba, k, rot):
    """cartão creme que CAI sobre o anterior (a pilha cresce: z sobe a cada cartão; o de baixo some depois que o novo pousa)"""
    return {"tipo": "cartao", "t": round(t, 3), "d": round(d, 3), "box": [60, 330, 960, 1250], "aba": aba, "entra": "cai", "rot": rot, "z": 20 + 8 * k}
def ZC(k, j=1): return 20 + 8 * k + j       # z do conteúdo do cartão k
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4}

# ================= abertura: viral em tela dividida + caixinha =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 1100], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 1027], "raio": 14, "pos": "center top",
      "arroba": "via @isabellalacerda_nutri", "respira": False, "zoom": [[0, 1.0, 0.01], [4.0, 1.05, 0.4], [vd - 2.5, 1.0, 0.4]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [110, 1190], "w": 790, "topo": "Mito ou verdade? 👇", "txt": "Doente perde 5 kg de gordura numa semana?",
      "botoes": ["MITO", "VERDADE"], "vel": 0.025, "escolha": 0, "t_escolha": 3.3},
     {"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1265], "valor": 874, "suf": " MIL VIEWS", "tam": 120},
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 1027], "raio": 14, "sombra": False, "z": 29}]

# ================= r1: "Ela está certa. A balança desce, mas olha o que desce." =================
PAINEL = "background:rgba(239,228,201,.97);border-radius:14px;height:1027px;box-sizing:border-box;line-height:1.1;" + SP
c += [{"tipo": "texto", "t": vd + 0.02, "d": 1.8, "xy": [70, 190], "w": 940, "fonte": "160px Anton", "cor": VERDE, "alinha": "center",
       "txt": "ELA ESTÁ\\nCERTA.", "z": 55, "entra": "pop", "css": PAINEL + ";padding:250px 40px 0"},
      CHECK(vd + 0.55, 1.25, 540, 840, s=80, z=56),
      {"tipo": "texto", "t": vd + 1.82, "d": round(R1D - 1.82, 2), "xy": [70, 190], "w": 940, "fonte": "140px Anton", "cor": TINTA, "alinha": "center",
       "txt": "OLHA O QUE\\nDESCE.", "z": 55, "entra": "nada", "css": PAINEL + ";padding:90px 40px 0"},
      FIS(vd + 1.82, round(R1D - 1.82, 2), [{"k": "balanca", "xy": [470, 800], "s": 0.75, "t": 0.15}], z=56, pulsos=[{"o": 0, "t": 1.3}]),
      SETA(vd + 2.3, round(R1D - 2.3, 2), [800, 690], [800, 960], z=57),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + P + "_rosto.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (indignado): veredito =================
A2 = round(a(7) - 0.1, 3)        # "O que despenca primeiro é água."
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1),
      GIG(tA, round(A2 - tA, 3), "5 QUILOS", y=1420, tam=420, cont=True, cor="rgba(179,18,31,.26)"),
      {"tipo": "pergunta", "t": tA, "d": round(A2 - tA, 3), "xy": [110, 380], "w": 860, "topo": "Mito ou verdade? 👇", "txt": "Doente perde 5 kg de gordura numa semana?",
       "botoes": ["MITO", "VERDADE"], "vel": 0.012, "escolha": 0, "t_escolha": a(6)},
      CARIMBO(a(6), round(A2 - a(6), 3), "MITO", [330, 1000], tam=200, rot=-7),
      FL(A2),
      GIG(A2, round(tB - A2, 3), "ÁGUA", y=1400, tam=520, cor="rgba(31,95,168,.16)", ida=False),
      TT(A2 + 0.03, round(tB - A2 - 0.03, 3), "PRIMEIRO SAI ÁGUA", y=330, fz=150, cor=AZUL),
      FIS(A2, round(tB - A2, 3), [{"k": "es_gota", "xy": [540, 1020], "s": 1.15, "t": 0.15}], pulsos=[{"o": 0, "t": 1.2}])]

# ================= B (manso): AULA em cartões, uma ideia por cartão =================
K1, K2, K3, K4, K5 = tB, round(be(5) + 0.4, 3), round(be(20) + 0.4, 3), round(be(33) + 0.4, 3), round(be(41) + 0.4, 3)
KF = tC
POUSA = 0.55                     # o cartão de baixo some quando o de cima já pousou
c += [FL(tB)]
# K1 "Pensa no músculo como uma uva."
c += [CARD(K1, K2 + POUSA - K1, "1 · a imagem", 0, -1.5),
      TT(K1 + 0.35, round(K2 + POUSA - K1 - 0.35, 3), "MÚSCULO = UVA", y=420, fz=150, z=ZC(0)),
      FIS(K1, round(K2 + POUSA - K1, 3), [{"k": "musculo", "xy": [300, 1000], "s": 0.62, "t": 0.45, "rotulo": "MÚSCULO", "rot_y": 200},
                                          {"k": "uva", "xy": [770, 990], "s": 0.75, "t": round(b(5) - K1, 3), "rotulo": "UVA", "rot_y": 250}],
          z=ZC(0, 2), pulsos=[{"o": 0, "t": round(b(2) - K1, 3)}, {"o": 1, "t": round(b(5) - K1 + 0.5, 3)}])]
# K2 "Ele guarda açúcar, e cada colher de açúcar segura três a quatro colheres de água."
c += [CARD(K2, K3 + POUSA - K2, "2 · dentro da uva", 1, 1.2),
      TT(K2 + 0.35, round(K3 + POUSA - K2 - 0.35, 3), "1 COLHER DE AÇÚCAR SEGURA", y=400, fz=105, z=ZC(1)),
      FIS(K2, round(K3 + POUSA - K2, 3), [{"k": "uva", "xy": [540, 850], "s": 0.72, "t": 0.4}], z=ZC(1, 2),
          fluxos=[{"de": [150, 760], "para": [470, 850], "curva": -90, "cor": "#f2c230", "t": round(b(8) - K2, 3), "d": 2.0, "n": 5, "rotulo": "AÇÚCAR", "viagem": 0.8},
                  {"de": [930, 760], "para": [610, 850], "curva": -90, "cor": "#4aa8ff", "t": round(b(15) - K2, 3), "d": 2.0, "n": 8, "rotulo": "ÁGUA", "viagem": 0.8}]),
      NUM(b(15) - 0.05, round(K3 + POUSA - b(15) + 0.05, 3), 4, y=1090, cor=AZUL, sombra='#9fb7d6', pre="3 A ", de=4, conta=0.01, rotulo="colheres de água", tam=230, z=ZC(1, 3)),
      FONTE(K2, round(KF - K2, 3), "Kreitzman e col., Am J Clin Nutr 1992 · doi 10.1093/ajcn/56.1.292S")]
# K3 "Doente, sem comer, o corpo gasta esse açúcar, e a água vai junto."
c += [CARD(K3, K4 + POUSA - K3, "3 · doente", 2, -1.0),
      TT(K3 + 0.35, round(b(24) - K3 - 0.37, 3), "DOENTE, SEM COMER", y=410, fz=130, z=ZC(2)),
      TT(b(24) - 0.02, round(K4 + POUSA - b(24) + 0.02, 3), "A ÁGUA VAI JUNTO", y=410, fz=130, cor=AZUL, z=ZC(2)),
      FIS(K3, round(K4 + POUSA - K3, 3), [{"k": "uva", "xy": [450, 1000], "s": 0.85, "t": 0.4}, {"k": "termometro", "xy": [850, 980], "s": 0.5, "t": 0.6}],
          z=ZC(2, 2), encolhe=[{"o": 0, "t": round(b(30) - K3, 3), "para": 0.74, "d": 1.2}],
          fluxos=[{"de": [450, 1000], "para": [190, 1440], "curva": 40, "cor": "#f2c230", "t": round(b(26) - K3, 3), "d": 1.6, "n": 5, "viagem": 0.9},
                  {"de": [450, 1000], "para": [800, 1460], "curva": 60, "cor": "#4aa8ff", "t": round(b(30) - K3, 3), "d": 1.8, "n": 8, "rotulo": "ÁGUA", "viagem": 0.9}],
          pulsos=[{"o": 1, "t": 1.0}])]
# K4 "A uva vira passa, e a balança despenca."
c += [CARD(K4, K5 + POUSA - K4, "4 · a passa", 3, 1.4),
      TT(K4 + 0.35, round(K5 + POUSA - K4 - 0.35, 3), "A UVA VIRA PASSA", y=410, fz=130, z=ZC(3)),
      FIS(K4, round(b(37) - K4 + 0.05, 3), [{"k": "uva", "xy": [330, 1000], "s": 0.85, "t": 0.35}], z=ZC(3, 2),
          encolhe=[{"o": 0, "t": round(b(36) - K4, 3), "para": 0.5, "d": 0.4}]),
      FIS(b(37), round(K5 + POUSA - b(37), 3), [{"k": "uva_passa", "xy": [330, 1000], "s": 1.05, "t": 0.0, "rotulo": "PASSA", "rot_y": 190}], z=ZC(3, 2)),
      FIS(b(40) - 0.1, round(K5 + POUSA - b(40) + 0.1, 3), [{"k": "balanca", "xy": [760, 1010], "s": 0.62, "t": 0.0}], z=ZC(3, 3)),
      SETA(b(41), round(K5 + POUSA - b(41), 3), [950, 860], [950, 1200], z=ZC(3, 4)),
      TT(b(40) - 0.1, round(K5 + POUSA - b(40) + 0.1, 3), "A BALANÇA DESPENCA", y=1300, fz=105, cor=VERM, z=ZC(3, 4), anim=None, entra="zoom")]
# K5 "Voltou a comer, a passa vira uva de novo."
c += [CARD(K5, KF - K5, "5 · voltou a comer", 4, -1.2),
      TT(K5 + 0.35, round(KF - K5 - 0.35, 3), "VOLTOU A COMER", y=410, fz=140, z=ZC(4)),
      FIS(K5, round(b(47) - K5 + 0.05, 3), [{"k": "uva_passa", "xy": [540, 960], "s": 1.0, "t": 0.35}], z=ZC(4, 2)),
      FIS(b(47), round(KF - b(47), 3), [{"k": "uva", "xy": [540, 950], "s": 0.85, "t": 0.0}], z=ZC(4, 2),
          fluxos=[{"de": [960, 1180], "para": [640, 990], "curva": -40, "cor": "#4aa8ff", "t": 0.1, "d": 1.3, "n": 7, "viagem": 0.7}]),
      TT(b(47), round(KF - b(47), 3), "A ÁGUA VOLTA", y=1290, fz=120, cor=AZUL, z=ZC(4, 3), anim=None, entra="zoom")]

# ================= C (neutro): o que se perde de verdade = músculo (Dirks 2016) =================
C2, C3, C4, C5 = round(e(13) - 0.3, 3), round(e(23) - 0.3, 3), round(e(33) - 0.3, 3), round(e(41) - 0.3, 3)
c += [FL(tC),
      GIG(tC, round(C2 - tC, 3), "PERDA", y=1430, tam=500, cont=True, cor="rgba(179,18,31,.24)"),
      TT(tC + 0.05, round(C2 - tC - 0.05, 3), "O QUE SE PERDE DE VERDADE?", y=330, fz=125),
      FIS(tC, round(C2 - tC, 3), [{"k": "musculo", "xy": [540, 1020], "s": 1.25, "t": round(e(12) - tC, 3), "rotulo": "MÚSCULO", "rot_y": 190}],
          pulsos=[{"o": 0, "t": round(e(12) - tC + 0.6, 3)}]),
      FL(C2),
      {"tipo": "artigo", "t": C2, "d": round(C3 - C2, 3), "box": [100, 300, 880, 640], "z": 34,
       "revista": "Diabetes · 2016", "titulo": "Uma semana de cama já tira músculo", "autores": "Dirks e col. · 10 rapazes jovens e saudáveis", "rola": 0,
       "linhas": [{"txt": "10 rapazes saudáveis.", "grifo": e(15)}, {"txt": "Uma semana deitados na cama.", "grifo": e(18)}],
       "rodape": "doi 10.2337/db15-1661"},
      GIG(C2, round(C3 - C2, 3), "7 DIAS", y=1470, tam=420, cor="rgba(28,26,23,.10)", ida=False),
      TT(e(15) - 0.05, round(C3 - e(15) + 0.05, 3), "10 RAPAZES, 7 DIAS DE CAMA", y=1040, fz=120),
      FL(C3),
      GIG(C3, round(C4 - C3, 3), "MASSA MAGRA", y=1470, tam=360, cont=True, cor="rgba(28,26,23,.2)"),
      TT(C3 + 0.05, round(C4 - C3 - 0.05, 3), "PERDERAM, EM MÉDIA", y=300, fz=125),
      NUM(e(26) - 0.05, round(C4 - e(26) + 0.05, 3), 1.4, y=520, dec=1, suf=" KG", de=0, rotulo="de massa magra", tam=300),
      FIS(C3, round(C4 - C3, 3), [{"k": "musculo", "xy": [540, 1230], "s": 0.95, "t": 0.2}], encolhe=[{"o": 0, "t": round(e(29) - C3, 3), "para": 0.82, "d": 1.4}]),
      FL(C4),
      GIG(C4, round(C5 - C4, 3), "COXA", y=1460, tam=480, cor="rgba(179,18,31,.12)", ida=False),
      TT(C4 + 0.05, round(C5 - C4 - 0.05, 3), "O MÚSCULO DA COXA", y=300, fz=125),
      NUM(e(34) - 0.05, round(C5 - e(34) + 0.05, 3), 3, y=520, pre="-", suf="%", rotulo="em 7 dias", tam=300),
      FIS(C4, round(C5 - C4, 3), [{"k": "musculo", "xy": [540, 1230], "s": 0.95, "t": 0.2}], encolhe=[{"o": 0, "t": round(e(37) - C4, 3), "para": 0.86, "d": 1.0}]),
      FL(C5),
      GIG(C5, round(tF - C5, 3), "SAUDÁVEIS", y=1470, tam=360, cor="rgba(46,125,50,.14)"),
      TT(C5 + 0.05, round(tF - C5 - 0.05, 3), "E ELES NEM ESTAVAM DOENTES.", y=330, fz=125),
      FIS(C5, round(tF - C5, 3), [{"k": "termometro", "xy": [460, 1050], "s": 0.95, "t": 0.2}]),
      CHECK(e(47), round(tF - e(47), 3), 760, 1000, s=80),
      FONTE(C2, round(tF - C2, 3), "Dirks e col., Diabetes 2016 · doi 10.2337/db15-1661")]

# ================= F (manso): acolher, em cartões =================
F2, F3 = round(ge(9) + 0.45, 3), round(ge(26) + 0.45, 3)
c += [FL(tF),
      CARD(tF, F2 + POUSA - tF, "cuidado", 5, -1.2),
      TT(tF + 0.35, round(g(7) - tF - 0.35, 3), "COMIDA E DESCANSO", y=420, fz=140, cor=VERDE, z=ZC(5)),
      FIS(tF, round(g(7) - tF, 3), [{"k": "cv_prato", "xy": [320, 1020], "s": 0.75, "t": round(g(4) - tF, 3)},
                                    {"k": "almofada", "xy": [770, 1020], "s": 0.7, "t": round(g(6) - tF, 3)}], z=ZC(5, 2)),
      TT(g(7), round(F2 + POUSA - g(7), 3), "NÃO DE BALANÇA", y=420, fz=140, cor=VERM, z=ZC(5), anim=None, entra="zoom"),
      FIS(g(7), round(F2 + POUSA - g(7), 3), [{"k": "balanca", "xy": [540, 1030], "s": 0.95, "t": 0.0}], z=ZC(5, 2)),
      XX(g(9), round(F2 + POUSA - g(9), 3), 540, 1030, s=190, z=ZC(5, 3)),
      CARD(F2, F3 + POUSA - F2, "se for com você", 6, 1.0),
      TT(F2 + 0.35, round(F3 + POUSA - F2 - 0.35, 3), "SE ESSA VONTADE JÁ PASSOU PELA SUA CABEÇA", y=420, fz=110, z=ZC(6)),
      TT(g(21) + 0.3, round(F3 + POUSA - g(21) - 0.3, 3), "CONVERSA COM O SEU MÉDICO", y=1050, fz=125, cor=VERDE, z=ZC(6, 2), anim=None, entra="zoom"),
      CIRC(g(26) - 0.2, round(F3 + POUSA - g(26) + 0.2, 3), 540, 1130, 460, 175, cor=VERDE, z=ZC(6, 3)),
      CARD(F3, round(c1 - F3 + 0.05, 3), "importante", 7, -0.8),
      TT(F3 + 0.3, round(c1 - F3 - 0.25, 3), "ISSO MERECE CUIDADO, NÃO VERGONHA.", y=440, fz=135, z=ZC(7)),
      FIS(F3, round(c1 - F3 + 0.05, 3), [{"k": "coracao_afeto", "xy": [540, 1170], "s": 0.95, "t": 0.5}], z=ZC(7, 2), pulsos=[{"o": 0, "t": 1.6}])]

# ================= CTA sério (rosto 6cd9, mesmo clipe do r1) + fecho (C, neutro) =================
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": CTA_D, "ms": CTA_MS, "src": M + P + "_rosto.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.0, 1.08, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": round(CTA_D - 0.25, 2), "y": 215, "txt": "SE TE AJUDOU, SEGUE E CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(c2, round(dur - c2, 3), "TEMPO", y=1480, tam=480, cont=True, cor="rgba(28,26,23,.2)"),
      TT(tD + 0.05, round(dur - tD - 0.05, 3), "DOENÇA TIRA ÁGUA E MÚSCULO.", y=300, fz=125),
      FIS(tD, round(dur - tD, 3), [{"k": "es_gota", "xy": [330, 760], "s": 0.5, "t": round(h(2) - tD, 3)},
                                   {"k": "musculo", "xy": [760, 760], "s": 0.55, "t": round(h(4) - tD, 3)}]),
      # carimbo logo abaixo da gota e do músculo (no "músculo"), antes da frase da gordura: lido como "água e músculo NÃO É GORDURA",
      # nunca como "gordura sai com tempo / não é gordura" (1ª versão punha o carimbo colado embaixo da frase do ouro e confundia)
      CARIMBO(h(4) + 0.45, round(dur - h(4) - 0.45, 3), "NÃO É GORDURA", [190, 880], tam=105, rot=-6),
      TT(h(5) - 0.05, round(dur - h(5) + 0.05, 3), "GORDURA SAI COM TEMPO.", y=1200, fz=125, cor=OURO, anim=None, entra="zoom"),
      FONTE(tD, round(dur - tD, 3), "Kreitzman e col., Am J Clin Nutr 1992 · Dirks e col., Diabetes 2016")]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json"},
       {"src": M + P + "_rosto.mp4", "t": vd, "ms": 0, "d": R1D, "palavras": M + P + "_rosto.words.json"},
       {"src": M + P + "_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + P + "_a_voz.words.json"},
       {"src": M + P + "_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + P + "_b_voz.words.json"},
       {"src": M + P + "_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + P + "_c_voz.words.json"},
       {"src": M + P + "_f_voz.wav", "t": tF, "ms": 0, "d": DF, "palavras": M + P + "_f_voz.words.json"},
       {"src": M + P + "_rosto.mp4", "t": c1, "ms": CTA_MS, "d": CTA_D, "palavras": M + P + "_rosto.words.json"},
       {"src": M + P + "_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + P + "_d_voz.words.json"}]
# trilha contínua por baixo de TUDO depois do viral (nenhuma pausa muda); uma faixa por bloco, emenda cruzada
musica = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.24, "fade": 0.6},
          {"src": "m_viagem", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tC - tB + 0.8, 2), "gain": 0.15, "fade": 0.6},
          {"src": "m_investiga", "t": round(tC - 0.4, 2), "ms": 0, "d": round(tF - tC + 0.8, 2), "gain": 0.24, "fade": 0.6},
          {"src": "m_emocao", "t": round(tF - 0.4, 2), "ms": 0, "d": round(dur - tF + 0.4, 2), "gain": 0.2, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": vd + 0.05, "gain": 0.35}, {"src": "papel", "t": vd + 1.82, "gain": 0.35},
       # A
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1, "gain": 0.45, "pico": 0.45}, {"src": "notif", "t": tA + 0.1, "gain": 0.35},
       {"src": "boom", "t": a(6), "gain": 0.45, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": A2, "gain": 0.35},
       # aula (cartões caindo)
       {"src": "papel", "t": K1 + 0.25, "gain": 0.45}, {"src": "boing", "t": b(5) + 0.05, "gain": 0.2},
       {"src": "papel", "t": K2 + 0.25, "gain": 0.45}, {"src": "whoosh2", "t": b(15) - 0.05, "gain": 0.3},
       {"src": "papel", "t": K3 + 0.25, "gain": 0.45}, {"src": "whoosh2", "t": b(30), "gain": 0.25},
       {"src": "papel", "t": K4 + 0.25, "gain": 0.45}, {"src": "scratch", "t": b(41), "gain": 0.25},
       {"src": "papel", "t": K5 + 0.25, "gain": 0.45}, {"src": "boing", "t": b(47) + 0.05, "gain": 0.2},
       # estudo
       {"src": "whoosh", "t": tC, "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": C2 + 0.1, "gain": 0.45},
       {"src": "whoosh2", "t": C3, "gain": 0.3}, {"src": "boom", "t": e(26), "gain": 0.4, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": C4, "gain": 0.3}, {"src": "whoosh2", "t": C5, "gain": 0.3},
       # acolher (sem impacto, só papel)
       {"src": "papel", "t": tF + 0.25, "gain": 0.4}, {"src": "papel", "t": F2 + 0.25, "gain": 0.4}, {"src": "papel", "t": F3 + 0.25, "gain": 0.4},
       # CTA e fecho
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.4}, {"src": "notif", "t": c1 + 0.2, "gain": 0.35}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.4},
       {"src": "whoosh2", "t": h(5) - 0.05, "gain": 0.3}, {"src": "boom", "t": h(4) + 0.45, "gain": 0.45, "pico": 0.3, "d": 1.4}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar(PID, dur, 1114, c, voz, sfx,
       {"r1_fim": r1, "esconde": [[0, vd]], "ys": [[vd, r1, 1000], [r1, c1, 1720], [c1, c2, 1560], [c2, dur, 1720]]})
p = json.load(open(f'planos/{PID}.json')); p['audio']['musica'] = musica
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "tC", tC, "tF", tF, "c1", c1, "c2", c2, "tD", tD, "| aula", round(tC - tB, 2), "s")
