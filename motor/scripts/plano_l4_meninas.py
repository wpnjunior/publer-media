# plano_l4_meninas.py (14/11, lote 4, TDAH Adulto Real): "TDAH nas meninas só aparece aos 12?" (não começa tarde, é visto tarde).
# Viral TikTok @melrobbins (podcast), em inglês, dois pedaços conferidos pelo volume e pela transcrição (tmp_mq/prep_viral.py):
#   A 28,11-34,60 "boys tend to show the symptoms of ADHD around the age of seven." (sem o "And so")
#   B 44,40-49,80 "Girls, on the other hand, don't start displaying symptoms until about the age of 12."
#   -> MEIA VERDADE (o que chega tarde na menina é o diagnóstico, não o sintoma). Nome dela fora da fala e da tela (só o @);
#   logo com o nome borrado e legenda queimada fora do enquadramento. Não falamos do diagnóstico nem da vida dela.
# Dublagem Murilo (1 create_speech, tmp_mq/prep_dub.py), original a 0,16 por baixo.
# r1 SEM crédito novo: bb_r1 (6cd9, "Calma. Não é bem assim.") a partir de 0,95 s (perfil Caneta; nunca usado no TDAH).
# Voz: 4 blocos HeyGen por clima, sem <break> e sem atempo; pausas de 0,7-0,8 s abertas na edição (tmp_mq/voz.py):
#   a indignado (veredito), b manso (aula) + f manso (o que fazer), c neutro (estudos) + d neutro (fecho), e alegre (cobrança).
# AULA: duas panelas no mesmo fogo, em CARTÕES que caem um por vez (creme, LARANJA = menino, VERDE-ÁGUA = menina; nada de
#   azul/rosa) sobre a pele NOTÍCIA (vinho; o último TDAH, Cury, foi lab). Desenhos novos: fisio_extra/chama, panela_aberta,
#   panela_tampada_corte (+ cerebro_lado, cf_livro, cy_nuvem, cy_relogio, cx_exame, rm_oculos do banco).
# Depois deste script (tmp_mq/build.sh):
#   python3 scripts/entrada.py react_l4_meninas assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     'MENINAS SÓ AOS 12?' 'a fala que viralizou com 2 milhões de views' && python3 scripts/pele.py react_l4_meninas noticia
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l4_meninas'; P = 'mq'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}mq_{k}_voz.words.json'))
WA, WB, WC, WF, WE, WD = W('a'), W('b'), W('c'), W('f'), W('e'), W('d')
DA, DB, DC, DF, DE, DD = [round(dur_de(f'{M}mq_{k}_voz.wav'), 3) for k in 'abcfed']
vd = 11.89
VA = 6.49                        # emenda dos pedaços A|B no viral
R1_MS = 0.95                     # bb_r1: "Calma." em 1,261, "assim." termina em 3,073; olhos abertos em 0,95
R1D = round(3.073 + 0.5 - R1_MS, 2)
CTA_D = 4.12
r1 = round(vd + R1D, 2)
tA = round(r1 + 0.15, 3)
tB = round(tA + DA + 0.75, 3)
tC = round(tB + DB + 0.75, 3)
tF = round(tC + DC + 0.65, 3)
tE = round(tF + DF + 0.6, 3)
c1 = round(tE + DE + 0.1, 3)
c2 = round(c1 + CTA_D, 3)
tD = round(c2 + 0.15, 3)
dur = round(tD + DD + 1.5, 2)
a = lambda i: round(tA + WA[i]['s'], 3); ae = lambda i: round(tA + WA[i]['e'], 3)
b = lambda i: round(tB + WB[i]['s'], 3); be = lambda i: round(tB + WB[i]['e'], 3)
e = lambda i: round(tC + WC[i]['s'], 3); ee = lambda i: round(tC + WC[i]['e'], 3)
g = lambda i: round(tF + WF[i]['s'], 3); ge = lambda i: round(tF + WF[i]['e'], 3)
q = lambda i: round(tE + WE[i]['s'], 3); qe = lambda i: round(tE + WE[i]['e'], 3)
h = lambda i: round(tD + WD[i]['s'], 3); he = lambda i: round(tD + WD[i]['e'], 3)
TINTA, VERM, VERDE, AMAR, BRANCO = '#1c1a17', '#c0182a', '#2e7d32', '#ffd400', '#ffffff'
LARANJA, AGUA, CREME = '#f6a04d', '#7ccfc0', '#f6efdc'
SP = "text-shadow:5px 5px 0 rgba(0,0,0,.14)"          # texto sobre cartão
SB = "text-shadow:7px 7px 0 #000"                     # texto solto sobre o vinho
def TC(t, d, txt, y=410, fz=125, cor=TINTA, z=40, **k):   # texto em cartão
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SP, vel=0.09, **k); L["z"] = z; return L
def TV(t, d, txt, y=330, fz=125, cor=BRANCO, z=40, **k):  # texto solto no vinho
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SB, vel=0.09, **k); L["z"] = z; return L
def GIG(t, d, txt, y=1300, tam=440, cont=False, cor="rgba(255,212,0,.13)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "cor_rotulo": "#ffffff"}; L.update(k); return L
def CHECK(t, d, cx, cy, s=60, z=46, cor='#3ddc84'): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 20, "cor": cor, "z": z}
def CIRC(t, d, cx, cy, rx, ry, cor=VERDE, lw=12, z=44): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "circulo", "c": [cx, cy], "r": [rx, ry]}], "espessura": lw, "cor": cor, "z": z}
def CARIMBO(t, d, txt, xy, tam=130, rot=-8, cor=VERM, z=60): return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": z, "cor": cor, "blend": "normal", "css": "background:rgba(255,255,255,.92)"}
def FONTE(t, d, txt): return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 196], "w": 1000, "fonte": "600 28px Montserrat", "cor": "#ffffff", "alinha": "center", "txt": txt, "z": 70, "css": "background:rgba(0,0,0,.45);border-radius:12px;padding:6px 0"}
def CHECAGEM(t, d): return {"tipo": "texto", "t": round(t + 0.3, 3), "d": round(d - 0.3, 3), "xy": [40, 128], "w": 1000, "fonte": "900 34px Montserrat", "cor": "#ffffff", "alinha": "center",
                            "txt": "● CHECAGEM · O QUE A CIÊNCIA DIZ", "css": "letter-spacing:3px;background:#ff2d3d;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"}
def NUM(t, d, valor, y=560, cor=AMAR, sombra='#5a0d10', z=44, **k):
    L = {"tipo": "numero", "t": round(t, 3), "d": round(d, 3), "xy": [0, y], "valor": valor, "tam": 300, "cor": cor, "sombra": sombra, "z": z}
    L.update(k); return L
def EMO(t, d, x, y, tam=120, z=47, txt="👀"):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": 240, "fonte": f"{tam}px Montserrat", "cor": "#fff", "alinha": "center", "txt": txt, "z": z, "entra": "pop"}
def CARD(t, d, aba, k, rot, cor=CREME, box=(60, 330, 960, 1250)):
    """cartão que CAI sobre o anterior (a pilha cresce: z sobe a cada cartão; o de baixo some depois que o novo pousa)"""
    return {"tipo": "cartao", "t": round(t, 3), "d": round(d, 3), "box": list(box), "aba": aba, "entra": "cai", "rot": rot, "z": 20 + 8 * k, "cor": cor}
def ZC(k, j=1): return 20 + 8 * k + j       # z do conteúdo do cartão k
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4}
FONTE1 = "Dalsgaard e col., JAMA Psychiatry 2020 · doi 10.1001/jamapsychiatry.2019.3523"
FONTE2 = "Mowlem e col., Psychiatry Res 2019 · doi 10.1016/j.psychres.2018.12.128"

# ================= abertura: viral em tela dividida + caixinha (dublagem Murilo por cima) =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 990], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 909], "raio": 14, "pos": "center 30%",
      "arroba": "via @melrobbins", "respira": False, "zoom": [[0, 1.0, 0.01], [3.0, 1.05, 0.4], [VA, 1.0, 0.3], [VA + 2.0, 1.06, 0.4]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [110, 1150], "w": 790, "topo": "Mito ou verdade? 👇", "txt": "Na menina, o TDAH só dá sinal aos 12?",
      "botoes": ["MITO", "VERDADE"], "vel": 0.025, "escolha": 0, "t_escolha": 3.3},
     {"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 2, "suf": " MI DE VIEWS", "tam": 120},
     {"tipo": "glitch", "t": VA - 0.08, "d": 0.18},
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 909], "raio": 14, "sombra": False, "pos": "center 30%", "z": 29}]

# ================= r1: "Calma. Não é bem assim." (resposta grande logo depois do viral) =================
PAINEL = "background:rgba(32,6,10,.96);border-radius:14px;height:909px;box-sizing:border-box;line-height:1.1;" + SB
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(R1D - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "118px Anton", "cor": BRANCO, "alinha": "center",
       "txt": "COMEÇA ANTES.\\nÉ VISTO TARDE.", "z": 55, "entra": "pop", "css": PAINEL + ";padding:110px 30px 0"},
      CARIMBO(vd + 0.5, round(R1D - 0.5, 2), "MEIA VERDADE", [160, 720], tam=110, rot=-7, z=60),
      {"tipo": "video", "t": vd, "d": R1D, "ms": R1_MS, "src": M + "bb_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= a (indignado): veredito =================
A2, A3, A4 = round(a(4) - 0.1, 3), round(a(11) - 0.2, 3), round(a(17) - 0.2, 3)
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1), CHECAGEM(tA, round(tB - tA, 3)),
      GIG(tA, round(A2 - tA, 3), "VERDADE", y=1350, tam=400, cont=True, cor="rgba(61,220,132,.35)"),
      TV(tA, round(A2 - tA, 3), "TEM VERDADE", y=420, fz=170, cor='#3ddc84'),
      CHECK(a(2), round(A2 - a(2), 3), 540, 860, s=110),
      FL(A2),
      GIG(A2, round(A3 - A2, 3), "DEMORA", y=1420, tam=440, cor="rgba(255,212,0,.12)", ida=False),
      TV(A2 + 0.03, round(A3 - A2 - 0.03, 3), "NA MENINA, DEMORA MAIS PRA PERCEBER", y=310, fz=120),
      FIS(A2, round(A3 - A2, 3), [{"k": "cy_relogio", "xy": [540, 1080], "s": 1.35, "t": 0.2}], pulsos=[{"o": 0, "t": round(a(6) - A2 + 0.1, 3)}]),
      FL(A3),
      {"tipo": "pergunta", "t": A3, "d": round(A4 - A3, 3), "xy": [110, 400], "w": 860, "topo": "Mito ou verdade? 👇", "txt": "Na menina, o TDAH só dá sinal aos 12?",
       "botoes": ["MITO", "VERDADE"], "vel": 0.012, "escolha": 0, "t_escolha": a(16)},
      CARIMBO(a(16), round(A4 - a(16), 3), "MITO", [340, 1010], tam=200, rot=-7),
      FL(A4),
      GIG(A4, round(tB - A4, 3), "TARDE", y=1450, tam=480, cont=True, cor="rgba(255,255,255,.22)"),
      TV(A4 + 0.03, round(tB - A4 - 0.03, 3), "O QUE CHEGA TARDE", y=330, fz=118),
      TV(a(21) - 0.05, round(tB - a(21) + 0.05, 3), "É O DIAGNÓSTICO", y=520, fz=135, cor=AMAR, anim=None, entra="zoom"),
      FIS(A4, round(tB - A4, 3), [{"k": "cx_exame", "xy": [540, 1130], "s": 0.95, "t": round(a(22) - A4, 3)}])]

# ================= b (manso): AULA em cartões, uma ideia por cartão =================
K1, K2, K3, K4, K5, K6 = tB, round(b(7) - 0.3, 3), round(b(19) - 0.3, 3), round(b(29) - 0.2, 3), round(b(36) - 0.3, 3), round(b(44) - 0.3, 3)
KF = tC
POUSA = 0.55
c += [FL(tB)]
# K1 "Pensa em duas panelas no mesmo fogo."
c += [CARD(K1, K2 + POUSA - K1, "a imagem", 0, -1.5),
      TC(K1 + 0.35, round(K2 + POUSA - K1 - 0.35, 3), "DUAS PANELAS, UM FOGO SÓ", y=420, fz=130, z=ZC(0)),
      FIS(K1, round(K2 + POUSA - K1, 3), [{"k": "panela_aberta", "xy": [330, 960], "s": 0.6, "t": round(b(3) - K1, 3)},
                                          {"k": "panela_tampada_corte", "xy": [750, 960], "s": 0.6, "t": round(b(3) - K1 + 0.2, 3)},
                                          {"k": "chama", "xy": [540, 1250], "s": 0.95, "t": round(b(5) - K1, 3)}],
          z=ZC(0, 2), pulsos=[{"o": 2, "t": round(b(6) - K1 + 0.2, 3)}])]
# K2 "O fogo é um cérebro que segura a atenção de outro jeito."
c += [CARD(K2, K3 + POUSA - K2, "o fogo", 1, 1.2),
      TC(K2 + 0.35, round(K3 + POUSA - K2 - 0.35, 3), "O FOGO: ATENÇÃO DE OUTRO JEITO", y=420, fz=112, z=ZC(1)),
      FIS(K2, round(K3 + POUSA - K2, 3), [{"k": "chama", "xy": [540, 1110], "s": 1.35, "t": 0.35},
                                          {"k": "cerebro_lado", "xy": [540, 1160], "s": 0.5, "t": round(b(11) - K2, 3)}],
          z=ZC(1, 2), pulsos=[{"o": 1, "t": round(b(15) - K2, 3)}, {"o": 1, "t": round(b(17) - K2 + 0.2, 3)}])]
# K3 MENINO (laranja) "A do menino, sem tampa: ferve, derrama, todo mundo vê."
c += [CARD(K3, K4 + POUSA - K3, "menino", 2, -1.0, cor=LARANJA),
      TC(K3 + 0.35, round(b(24) - K3 - 0.37, 3), "SEM TAMPA", y=420, fz=160, z=ZC(2)),
      TC(b(24) - 0.02, round(b(26) - b(24), 3), "FERVE, DERRAMA", y=420, fz=150, z=ZC(2), anim=None, entra="zoom"),
      TC(b(26) - 0.02, round(K4 + POUSA - b(26) + 0.02, 3), "TODO MUNDO VÊ", y=420, fz=150, z=ZC(2), anim=None, entra="zoom"),
      FIS(K3, round(K4 + POUSA - K3, 3), [{"k": "panela_aberta", "xy": [540, 1080], "s": 1.15, "t": 0.4}], z=ZC(2, 2),
          pulsos=[{"o": 0, "t": round(b(24) - K3, 3)}, {"o": 0, "t": round(b(25) - K3, 3)}],
          fluxos=[{"de": [470, 920], "para": [200, 700], "curva": -90, "cor": "#fbfaf5", "t": round(b(24) - K3, 3), "d": 2.2, "n": 6, "r": 16, "viagem": 0.8},
                  {"de": [610, 920], "para": [880, 700], "curva": -90, "cor": "#fbfaf5", "t": round(b(24) - K3 + 0.15, 3), "d": 2.2, "n": 6, "r": 16, "viagem": 0.8},
                  {"de": [380, 1030], "para": [330, 1400], "curva": 30, "cor": "#fbfaf5", "t": round(b(25) - K3, 3), "d": 1.8, "n": 5, "r": 14, "viagem": 0.9},
                  {"de": [700, 1030], "para": [760, 1400], "curva": 30, "cor": "#fbfaf5", "t": round(b(25) - K3 + 0.1, 3), "d": 1.8, "n": 5, "r": 14, "viagem": 0.9}]),
      EMO(b(26), round(K4 + POUSA - b(26), 3), 40, 640, z=ZC(2, 4)),
      EMO(b(26) + 0.1, round(K4 + POUSA - b(26) - 0.1, 3), 800, 760, z=ZC(2, 4)),
      EMO(b(26) + 0.2, round(K4 + POUSA - b(26) - 0.2, 3), 70, 1300, z=ZC(2, 4)),
      EMO(b(26) + 0.3, round(K4 + POUSA - b(26) - 0.3, 3), 780, 1330, z=ZC(2, 4))]
# K4 MENINA (verde-água) "A da menina, tampada: ferve por dentro."
c += [CARD(K4, K5 + POUSA - K4, "menina", 3, 1.4, cor=AGUA),
      TC(K4 + 0.35, round(b(33) - K4 - 0.37, 3), "TAMPADA", y=420, fz=170, z=ZC(3)),
      TC(b(33) - 0.02, round(K5 + POUSA - b(33) + 0.02, 3), "FERVE POR DENTRO", y=420, fz=150, z=ZC(3), anim=None, entra="zoom"),
      FIS(K4, round(K5 + POUSA - K4, 3), [{"k": "panela_tampada_corte", "xy": [540, 1080], "s": 1.15, "t": 0.4}], z=ZC(3, 2),
          pulsos=[{"o": 0, "t": round(b(33) - K4, 3)}, {"o": 0, "t": round(b(35) - K4, 3)}],
          fluxos=[{"de": [480, 1240], "para": [485, 1065], "curva": -8, "cor": "#fff6c8", "t": round(b(33) - K4 - 0.1, 3), "d": 2.4, "n": 6, "r": 11, "viagem": 0.75},
                  {"de": [610, 1250], "para": [600, 1060], "curva": 8, "cor": "#fff6c8", "t": round(b(33) - K4 + 0.2, 3), "d": 2.4, "n": 6, "r": 11, "viagem": 0.75}])]
# K5 MENINA na aula "Ela se perde na aula e se culpa."
c += [CARD(K5, K6 + POUSA - K5, "menina, na aula", 4, -1.2, cor=AGUA),
      TC(K5 + 0.35, round(K6 + POUSA - K5 - 0.35, 3), "SE PERDE NA AULA", y=420, fz=150, z=ZC(4)),
      TC(b(41) - 0.02, round(K6 + POUSA - b(41) + 0.02, 3), "E SE CULPA", y=1360, fz=160, cor=VERM, z=ZC(4, 3), anim=None, entra="zoom"),
      FIS(K5, round(K6 + POUSA - K5, 3), [{"k": "cf_livro", "xy": [430, 1170], "s": 0.95, "t": 0.4},
                                          {"k": "cy_nuvem", "xy": [740, 880], "s": 0.75, "t": round(b(42) - K5, 3)}], z=ZC(4, 2),
          pulsos=[{"o": 0, "t": round(b(39) - K5, 3)}])]
# K6 "Ninguém percebe." dois cartões lado a lado + selos
c += [CARD(K6, round(KF - K6, 3), "menino", 5, -2.0, cor=LARANJA, box=(50, 600, 470, 760)),
      CARD(K6 + 0.2, round(KF - K6 - 0.2, 3), "menina", 6, 2.0, cor=AGUA, box=(560, 600, 470, 760)),
      FIS(K6, round(KF - K6, 3), [{"k": "panela_aberta", "xy": [285, 980], "s": 0.72, "t": 0.35},
                                  {"k": "panela_tampada_corte", "xy": [795, 980], "s": 0.72, "t": 0.55}], z=ZC(6, 2)),
      TV(b(44) - 0.05, round(KF - b(44) + 0.05, 3), "NINGUÉM PERCEBE", y=380, fz=125, z=ZC(6, 3)),
      CARIMBO(b(44) + 0.15, round(KF - b(44) - 0.15, 3), "VISTO", [140, 1180], tam=100, rot=-8, cor=VERDE, z=ZC(6, 4)),
      CARIMBO(b(45) + 0.1, round(KF - b(45) - 0.1, 3), "NÃO VISTO", [585, 1180], tam=82, rot=6, cor=VERM, z=ZC(6, 4))]

# ================= c (neutro): estudos =================
C2, C3, C4, C5, C6, C7 = round(e(8) - 0.2, 3), round(e(14) - 0.25, 3), round(e(26) - 0.25, 3), round(e(30) - 0.25, 3), round(e(38) - 0.25, 3), round(e(48) - 0.1, 3)
c += [FL(tC), CHECAGEM(tC, round(tF - tC, 3)),
      GIG(tC, round(C2 - tC, 3), "DINAMARCA", y=1420, tam=400, cont=True, cor="rgba(255,255,255,.2)"),
      TV(tC + 0.05, round(C2 - tC - 0.05, 3), "UM ESTUDO NA DINAMARCA", y=1050, fz=120, anim=None, entra="zoom"),
      {"tipo": "artigo", "t": tC, "d": round(C2 - tC + 0.3, 3), "box": [100, 300, 880, 640], "z": 34,
       "revista": "JAMA Psychiatry · 2020", "titulo": "Em que idade sai cada diagnóstico", "autores": "Dalsgaard e col. · todos os nascidos na Dinamarca de 1995 a 2016", "rola": 0,
       "linhas": [{"txt": "Crianças acompanhadas desde o nascimento.", "grifo": e(6)}], "rodape": "doi 10.1001/jamapsychiatry.2019.3523"},
      FL(C2),
      NUM(C2, round(C3 - C2, 3), 1.3, y=700, dec=1, suf=" MILHÃO", rotulo="de crianças acompanhadas", tam=260, de=0),
      GIG(C2, round(C3 - C2, 3), "CRIANÇAS", y=1420, tam=380, cor="rgba(255,212,0,.12)", ida=False),
      FL(C3),
      TV(C3 + 0.05, round(C5 - C3 - 0.05, 3), "PICO DE DIAGNÓSTICOS", y=300, fz=120),
      GIG(C3, round(C6 - C3, 3), "8 x 17", y=1450, tam=420, cont=True, cor="rgba(255,255,255,.18)"),
      CARD(C3, round(C6 - C3, 3), "menino", 7, -1.5, cor=LARANJA, box=(60, 620, 460, 700)),
      NUM(e(24) - 0.1, round(C6 - e(24) + 0.1, 3), 8, y=720, cor=TINTA, sombra='#b86a1f', w=460, xy=[60, 720], tam=330, rotulo="ANOS", cor_rotulo=TINTA, sombra_rotulo="none", z=ZC(7, 2), de=8, conta=0.01),
      FIS(C3, round(e(24) - 0.1 - C3, 3), [{"k": "panela_aberta", "xy": [290, 960], "s": 0.75, "t": 0.4}], z=ZC(7, 2)),
      CARD(C4, round(C6 - C4, 3), "menina", 8, 1.5, cor=AGUA, box=(560, 620, 460, 700)),
      NUM(e(29) - 0.1, round(C6 - e(29) + 0.1, 3), 17, y=720, cor=TINTA, sombra='#3f8f82', w=460, xy=[560, 720], tam=330, rotulo="ANOS", cor_rotulo=TINTA, sombra_rotulo="none", z=ZC(8, 2), de=17, conta=0.01),
      FIS(C4, round(e(29) - 0.1 - C4, 3), [{"k": "panela_tampada_corte", "xy": [790, 960], "s": 0.75, "t": 0.4}], z=ZC(8, 2)),
      FL(C5),
      TV(C5 + 0.05, round(C6 - C5 - 0.05, 3), "POSSÍVEL ATRASO PRA PERCEBER", y=300, fz=120, cor=AMAR),
      FIS(C5, round(C6 - C5, 3), [{"k": "cy_relogio", "xy": [540, 1460], "s": 0.75, "t": 0.15}], z=ZC(8, 4), pulsos=[{"o": 0, "t": round(e(35) - C5, 3)}]),
      FONTE(tC, round(C6 - tC, 3), FONTE1),
      FL(C6),
      {"tipo": "artigo", "t": C6, "d": round(C7 - C6 + 0.3, 3), "box": [100, 300, 880, 640], "z": 34,
       "revista": "Psychiatry Research · 2019", "titulo": "Meninas e meninos com muitos sinais de TDAH", "autores": "Mowlem e col. · estudo de base populacional", "rola": 0,
       "linhas": [{"txt": "283 crianças de 7 a 12 anos.", "grifo": e(42)}], "rodape": "doi 10.1016/j.psychres.2018.12.128"},
      TV(e(41) - 0.1, round(C7 - e(41) + 0.1, 3), "7 A 12 ANOS", y=1080, fz=170, cor=AMAR, anim=None, entra="zoom"),
      FL(C7),
      TV(C7 + 0.05, round(tF - C7 - 0.05, 3), "OS PAIS VIAM MENOS A AGITAÇÃO DELAS", y=310, fz=120),
      FIS(C7, round(tF - C7, 3), [{"k": "rm_oculos", "xy": [540, 1080], "s": 1.25, "t": 0.2}], encolhe=[{"o": 0, "t": round(e(53) - C7, 3), "para": 0.9, "d": 0.9}]),
      FONTE(C6, round(tF - C6, 3), FONTE2)]

# ================= f (manso): o que fazer (sem diagnosticar) =================
F2 = round(g(13) - 0.2, 3)
c += [FL(tF),
      CARD(tF, round(F2 + POUSA - tF, 3), "importante", 9, -1.2),
      TC(tF + 0.35, round(F2 + POUSA - tF - 0.35, 3), "SE VOCÊ SE VIU NISSO", y=420, fz=135, z=ZC(9)),
      TC(g(5) - 0.15, round(F2 + POUSA - g(5) + 0.15, 3), "CONVERSA COM\\nO SEU MÉDICO", y=950, fz=125, cor=VERDE, z=ZC(9, 2), anim=None, entra="zoom"),
      CIRC(g(9) - 0.1, round(F2 + POUSA - g(9) + 0.1, 3), 540, 1075, 455, 205, z=ZC(9, 3)),
      CARD(F2, round(tE - F2 + 0.05, 3), "e leve", 10, 1.0),
      TC(F2 + 0.35, round(tE - F2 - 0.3, 3), "O BOLETIM DA ESCOLA", y=420, fz=135, z=ZC(10)),
      FIS(F2, round(tE - F2 + 0.05, 3), [{"k": "cx_exame", "xy": [540, 1110], "s": 1.15, "t": 0.3, "rotulo": "BOLETIM", "rot_y": 250}], z=ZC(10, 2))]

# ================= e (alegre): cobrança =================
E2 = round(q(6) - 0.2, 3)
c += [FL(tE),
      TV(tE + 0.05, round(E2 - tE - 0.05, 3), "MENINA QUIETA PASSAVA", y=330, fz=150),
      FIS(tE, round(E2 - tE, 3), [{"k": "panela_tampada_corte", "xy": [540, 1130], "s": 1.0, "t": 0.3}]),
      FL(E2),
      TV(E2 + 0.05, round(c1 - E2 - 0.05, 3), "AQUI NÃO PASSA", y=360, fz=170, cor=AMAR),
      EMO(q(10) - 0.05, round(c1 - q(10) + 0.05, 3), 300, 720, tam=330, z=46),
      TV(q(9) - 0.05, round(c1 - q(9) + 0.05, 3), "SAIR SEM SEGUIR?", y=1260, fz=120, anim=None, entra="zoom")]

# ================= CTA (banco cta6) + fecho (d, neutro) =================
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": CTA_D, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": round(CTA_D - 0.25, 2), "y": 215, "txt": "COMBINADO: SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(c2, round(dur - c2, 3), "VISTO TARDE", y=1460, tam=420, cont=True, cor="rgba(255,255,255,.22)"),
      TV(tD + 0.05, round(dur - tD - 0.05, 3), "NÃO COMEÇA TARDE.", y=330, fz=128),
      TV(h(3) - 0.05, round(dur - h(3) + 0.05, 3), "É VISTO TARDE.", y=650, fz=165, cor=AMAR, anim=None, entra="zoom"),
      FIS(tD, round(dur - tD, 3), [{"k": "panela_tampada_corte", "xy": [540, 1080], "s": 0.95, "t": 0.2}]),
      CARIMBO(he(5) + 0.1, round(dur - he(5) - 0.1, 3), "MEIA VERDADE", [150, 1310], tam=120, rot=-6),
      FONTE(tD, round(dur - tD, 3), "Dalsgaard e col., JAMA Psychiatry 2020 · Mowlem e col., Psychiatry Res 2019")]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json", "gain": 0.16},
       {"src": M + P + "_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "bb_r1.mp4", "t": vd, "ms": R1_MS, "d": R1D, "palavras": M + "bb_r1.words.json"},
       {"src": M + P + "_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + P + "_a_voz.words.json"},
       {"src": M + P + "_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + P + "_b_voz.words.json"},
       {"src": M + P + "_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + P + "_c_voz.words.json"},
       {"src": M + P + "_f_voz.wav", "t": tF, "ms": 0, "d": DF, "palavras": M + P + "_f_voz.words.json"},
       {"src": M + P + "_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + P + "_e_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": CTA_D, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + P + "_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + P + "_d_voz.words.json"}]
# trilha contínua por baixo de TUDO depois do viral (nenhuma pausa muda); uma faixa por bloco, emenda cruzada
musica = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.24, "fade": 0.6},
          {"src": "m_viagem", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tC - tB + 0.8, 2), "gain": 0.16, "fade": 0.6},
          {"src": "m_investiga", "t": round(tC - 0.4, 2), "ms": 0, "d": round(tF - tC + 0.8, 2), "gain": 0.24, "fade": 0.6},
          {"src": "m_emocao", "t": round(tF - 0.4, 2), "ms": 0, "d": round(tE - tF + 0.8, 2), "gain": 0.2, "fade": 0.6},
          {"src": "m_humor", "t": round(tE - 0.4, 2), "ms": 0, "d": round(dur - tE + 0.4, 2), "gain": 0.18, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": VA - 0.08, "gain": 0.3},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": vd + 0.05, "gain": 0.35}, {"src": "boom", "t": vd + 0.5, "gain": 0.4, "pico": 0.3, "d": 1.2},
       # a
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1, "gain": 0.45, "pico": 0.45}, {"src": "notif", "t": tA + 0.3, "gain": 0.3},
       {"src": "whoosh2", "t": A2, "gain": 0.3}, {"src": "pagina", "t": A3 + 0.05, "gain": 0.35},
       {"src": "boom", "t": a(16), "gain": 0.45, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": A4, "gain": 0.35}, {"src": "papel", "t": a(22), "gain": 0.35},
       # aula (cartões caindo)
       {"src": "papel", "t": K1 + 0.25, "gain": 0.45}, {"src": "papel", "t": K2 + 0.25, "gain": 0.45}, {"src": "boing", "t": b(11) + 0.05, "gain": 0.2},
       {"src": "papel", "t": K3 + 0.25, "gain": 0.45}, {"src": "whoosh2", "t": b(24), "gain": 0.25}, {"src": "boing", "t": b(26) + 0.05, "gain": 0.25},
       {"src": "papel", "t": K4 + 0.25, "gain": 0.45}, {"src": "papel", "t": K5 + 0.25, "gain": 0.45}, {"src": "scratch", "t": b(42), "gain": 0.2},
       {"src": "papel", "t": K6 + 0.25, "gain": 0.45}, {"src": "papel", "t": K6 + 0.45, "gain": 0.35}, {"src": "boom", "t": b(45) + 0.1, "gain": 0.35, "pico": 0.3, "d": 1.2},
       # estudos
       {"src": "whoosh", "t": tC, "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": tC + 0.1, "gain": 0.45},
       {"src": "whoosh2", "t": C2, "gain": 0.3}, {"src": "papel", "t": C3 + 0.25, "gain": 0.45}, {"src": "papel", "t": C4 + 0.25, "gain": 0.45},
       {"src": "whoosh2", "t": C5, "gain": 0.3}, {"src": "pagina", "t": C6 + 0.1, "gain": 0.45}, {"src": "whoosh2", "t": C7, "gain": 0.3},
       # o que fazer (sem impacto, só papel)
       {"src": "papel", "t": tF + 0.25, "gain": 0.4}, {"src": "papel", "t": F2 + 0.25, "gain": 0.4},
       # cobrança
       {"src": "whoosh2", "t": tE, "gain": 0.3}, {"src": "boing", "t": q(10), "gain": 0.3},
       # CTA e fecho
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.4}, {"src": "notif", "t": c1 + 0.2, "gain": 0.35}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.4},
       {"src": "whoosh2", "t": h(3) - 0.05, "gain": 0.3}, {"src": "boom", "t": he(5) + 0.1, "gain": 0.45, "pico": 0.3, "d": 1.4}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar(PID, dur, 1412, c, voz, sfx,
       {"r1_fim": r1, "esconde": [], "ys": [[0, 4.05, 1720], [4.05, vd, 1440], [vd, r1, 1000], [r1, c1, 1720], [c1, c2, 1560], [c2, dur, 1720]]})
p = json.load(open(f'planos/{PID}.json')); p['audio']['musica'] = musica
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "tC", tC, "tF", tF, "tE", tE, "c1", c1, "c2", c2, "tD", tD, "| aula", round(tC - tB, 2), "s")
