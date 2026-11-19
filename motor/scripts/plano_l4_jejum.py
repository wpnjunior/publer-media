import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
# plano_l4_jejum.py (14/11, lote 4, Papo de Médico): "jejum só de água é o melhor tratamento para pressão alta?"
# Viral: The Diary Of A CEO (TikTok @steven), inglês, dublado pela Murilo (original a 0,16 por baixo). Não citar convidado nem apresentador.
# Trecho (2 pedaços, 8,29 s): 0,00-6,41 "Esse é o tratamento mais eficaz já mostrado contra a principal causa de morte e
#   incapacidade: a pressão alta." + 15,10-16,98 "Chama-se jejum. E tem mais." -> EXAGERO (caixinha: MITO).
#   Corte só da parte de cima (sem a caixa 'DOCTORS DONT WANT YOU TO KNOW THIS!' nem a legenda queimada); a caixa vira
#   cartela em português; o cartão de dicionário 'fasting' é coberto pela versão em português (jp_dic.png).
# Aula: CARTÕES (um por ideia, entram de lado sobre o baralho; a pergunta fica no alto), desenhos novos em fisio_extra:
#   vaso_mangueira, vaso_mangueira_fraco, rim, silhueta_levantando, jp_prato_vazio, jp_pessoa, jp_pessoa_alerta.
# Pele: notícia (a última do Papo, carnívora, foi dossiê). Voz: 4 blocos HeyGen por clima, sem atempo e sem <break>
#   (pausas abertas na edição, tmp_jp/prep.py): A indignado (r1 + abertura), B manso (aula + o que fazer),
#   C neutro (estudo + fecho), D alegre (cobrança). r1 = A[0:3,10] no avatar 6cd9 (jp_rosto.mp4).
# Depois deste script (ele mesmo roda):
#   python3 scripts/entrada.py react_l4_jejum assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 '“O MELHOR TRATAMENTO” PRA PRESSÃO?' 'a fala que viralizou num podcast gringo'
#   python3 scripts/pele.py react_l4_jejum noticia
PID = 'react_l4_jejum'; P = 'jp'
DU = json.load(open('tmp_jp/dur.json'))
WD = {k: json.load(open(f'assets/midia/{P}_{k}_voz.words.json')) for k in ('ab', 'au', 'es', 'oq', 'co', 'fe')}
vd = DU['vd']
R1D = 3.33                      # "saiba" acaba em 2,834 + 0,5 s de folga
r1 = round(vd + R1D, 2)
GAP = 0.55
tAB = r1
tAU = round(tAB + DU['ab'] + GAP, 3)
tES = round(tAU + DU['au'] + GAP, 3)
tOQ = round(tES + DU['es'] + GAP, 3)
tCO = round(tOQ + DU['oq'] + 0.5, 3)
c1 = round(tCO + DU['co'] + 0.35, 2)
c2 = round(c1 + 4.12, 2)
dur = round(c2 + DU['fe'] + 0.6, 2)
A = lambda v: round(tAB + v, 3); U = lambda v: round(tAU + v, 3); E = lambda v: round(tES + v, 3)
O = lambda v: round(tOQ + v, 3); K = lambda v: round(tCO + v, 3); F = lambda v: round(c2 + v, 3)
def w(blk, palavra, n=0):
    k = 0
    for x in WD[blk]:
        if x['w'].strip('.,?:!').lower() == palavra.lower():
            if k == n: return x['s']
            k += 1
    raise SystemExit(f'sem {palavra} em {blk}')

TINTA, AMAR, VERM, VERDE, AZUL, CREME = '#1c1a17', '#ffd400', '#ff4d4d', '#3ddc84', '#7fd3ff', '#f6efdc'
SOMBRA = "text-shadow:6px 6px 0 #000,0 0 18px rgba(0,0,0,.8)"
def TT(t, d, txt, y=300, fz=120, cor="#ffffff", **k):
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SOMBRA, vel=0.09, **k)
def TC(t, d, txt, y, fz=104):  # texto do cartão (tinta escura sobre o creme)
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=TINTA, css="text-shadow:4px 4px 0 rgba(0,0,0,.10)", vel=0.08, xy=[140, y], w=800, z=None)
def GIG(t, d, txt, y=1480, tam=300, cont=False, cor="rgba(255,212,0,.10)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos}; L.update(k); return L
def X(t, d, cx, cy, s=70, cor="#ff2d3d", z=45): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "x", "c": [cx, cy], "s": s}], "espessura": 20, "cor": cor, "z": z}
def CHECK(t, d, cx, cy, s=60, cor=VERDE, z=46): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 20, "cor": cor, "z": z}
def CIRC(t, d, cx, cy, rx, ry, cor="#ff2d3d", lw=12, z=44): return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": [{"k": "circulo", "c": [cx, cy], "r": [rx, ry]}], "espessura": lw, "cor": cor, "z": z}
def CARIMBO(t, d, txt, xy, tam=130, rot=-8, cor="#ff2d3d"): return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": 60, "cor": cor, "blend": "normal", "css": "background:rgba(255,255,255,.92)"}
def FONTE(t, d, txt): return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 210], "w": 1000, "fonte": "600 28px Montserrat", "cor": "#ffffff", "alinha": "center", "txt": txt, "z": 70, "css": "text-shadow:0 2px 6px #000;background:rgba(0,0,0,.35);border-radius:12px;padding:6px 0"}
def NUM(t, d, valor, y=1010, cor=AMAR, sombra='#7a5a00', **k):
    L = {"tipo": "numero", "t": round(t, 3), "d": round(d, 3), "xy": [0, y], "valor": valor, "tam": 280, "cor": cor, "sombra": sombra, "z": 44}
    L.update(k); return L
FL = lambda t, mx=0.45: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": mx}

# ================= viral em tela dividida + caixinha =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 933], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 853], "raio": 14, "pos": "center top",
      "arroba": "via @steven · The Diary Of A CEO", "arroba_pos": "topo", "respira": False, "zoom": [[0, 1.0, 0.01], [3.6, 1.05, 0.4], [vd - 2.6, 1.0, 0.4]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [110, 1120], "w": 860, "topo": "Mito ou verdade? 👇", "txt": "Jejum de água é o melhor tratamento pra pressão?",
      "botoes": ["MITO", "VERDADE"], "vel": 0.022},
     # a caixa queimada em inglês (0-4 s) vira cartela em português depois da caixinha
     {"tipo": "texto", "t": 4.25, "d": round(vd - 4.25, 2), "xy": [90, 1092], "w": 900, "fonte": "800 30px Montserrat", "cor": "#ffffff", "alinha": "center",
      "txt": "a legenda do vídeo diz:", "z": 50, "css": "text-shadow:0 2px 6px #000", "entra": "desliza", "dy": 40},
     {"tipo": "texto", "t": 4.3, "d": round(vd - 4.3, 2), "xy": [90, 1140], "w": 900, "fonte": "100px Anton", "cor": "#111111", "alinha": "center",
      "txt": "“OS MÉDICOS NÃO QUEREM QUE VOCÊ SAIBA!”", "z": 50, "css": "background:#ffffff;border-radius:16px;padding:14px 22px;box-shadow:0 14px 34px rgba(0,0,0,.45)", "entra": "pop"},
     # cartão de dicionário 'fasting' coberto pelo 'jejum' em português (6,79-7,55 do corte)
     {"tipo": "foto", "t": 6.79, "d": 0.77, "src": M + P + "_dic.png", "box": [432, 768, 578, 275], "raio": 14, "sombra": False, "entra": "nada", "z": 30},
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 853], "raio": 14, "sombra": False, "z": 29}]
# r1: "Sou médico. E quero muito que você saiba." (responde à caixa)
c += [{"tipo": "texto", "t": vd + 0.05, "d": round(R1D - 0.05, 2), "xy": [110, 800], "w": 860, "fonte": "100px Anton", "cor": "#111111", "alinha": "center",
       "txt": "“NÃO QUEREM QUE VOCÊ SAIBA”", "z": 50, "css": "background:#ffffff;border-radius:16px;padding:12px 20px;box-shadow:0 14px 34px rgba(0,0,0,.45)", "entra": "pop"},
      X(vd + 0.55, round(R1D - 0.55, 2), 540, 915, s=130, z=52),
      TT(vd + 1.45, round(R1D - 1.45, 2), "EU QUERO!", y=290, fz=150, cor=AMAR, anim=None, entra="zoom", xy=[590, 290], w=440, z=52),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + P + "_rosto.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= abertura (indignado) =================
a_nisso, a_agora, a_mostrado, a_frase, a_maior = w('ab', 'nisso'), w('ab', 'agora'), w('ab', 'mostrado'), w('ab', 'frase'), w('ab', 'maior')
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, FL(r1),
      GIG(A(0), a_agora, "SÉRIA", y=1380, tam=460, cont=True, cor="rgba(255,212,0,.22)"),
      TT(A(0.05), a_agora - 0.05, "PRESSÃO ALTA É COISA SÉRIA", y=330, fz=135),
      CHECK(A(a_nisso - 0.1), a_agora - a_nisso + 0.1, 540, 900, s=90),
      TT(A(a_nisso - 0.05), a_agora - a_nisso + 0.05, "NISSO, ACERTOU", y=1080, fz=130, cor=VERDE, anim=None, entra="zoom"),
      FL(A(a_agora)),
      GIG(A(a_agora), a_frase - a_agora - 0.1, "EFICAZ", y=1400, tam=440),
      {"tipo": "pergunta", "t": A(a_agora), "d": round(a_frase - a_agora - 0.1, 3), "xy": [110, 380], "w": 860, "topo": "Mito ou verdade? 👇",
       "txt": "Jejum de água é o melhor tratamento pra pressão?", "botoes": ["MITO", "VERDADE"], "vel": 0.012, "escolha": 0, "t_escolha": A(a_mostrado + 0.2)},
      TT(A(a_agora + 0.3), a_frase - a_agora - 0.4, "“O MAIS EFICAZ JÁ MOSTRADO”?", y=930, fz=120, cor=AMAR),
      CIRC(A(a_mostrado + 0.15), a_frase - a_mostrado - 0.25, 340, 712, 220, 85, cor=AMAR, z=75),
      FL(A(a_frase - 0.1)),
      GIG(A(a_frase - 0.1), round(tAU - A(a_frase - 0.1), 3), "FRASE", y=1420, tam=420, cont=True, cor="rgba(255,77,77,.25)", ida=False),
      TT(A(a_frase - 0.05), round(tAU - A(a_frase - 0.05), 3), "FRASE", y=300, fz=330, cor=VERM, anim=None, entra="zoom"),
      TT(A(a_maior - 0.05), round(tAU - A(a_maior - 0.05), 3), "prova", y=740, fz=100, anim=None, entra="pop"),
      CARIMBO(A(a_maior + 0.15), round(tAU - A(a_maior + 0.15), 3), "EXAGERO", [250, 960], tam=170, rot=-8)]

# ================= AULA (manso): cartões, um por ideia =================
u = {k: w('au', k) for k in ('pensa', 'sem', 'rim', 'por')}
u['menos'] = w('au', 'menos', 1)   # "Menos água no cano" (o 1º 'menos' é "menos insulina")
u_por2 = w('au', 'por', 1)
DECK0, DECK1 = round(U(u['pensa'] - 0.15), 3), round(tES - 0.2, 3)
cards = [  # (início, texto, aba, gigante)
    (u['pensa'] - 0.15, "PENSA NUMA MANGUEIRA", "1 / 5", "MANGUEIRA"),
    (u['sem'] - 0.1, "SEM COMIDA, MENOS INSULINA", "2 / 5", "INSULINA"),
    (u['rim'] - 0.35, "RIM SOLTA SAL E ÁGUA", "3 / 5", "XIXI"),
    (u['menos'] - 0.1, "MENOS ÁGUA, MENOS PRESSÃO", "4 / 5", "PRESSÃO"),
    (u_por2 - 0.15, "TONTURA AO LEVANTAR", "5 / 5", "TONTURA")]
c += [FL(tAU),
      TT(U(0.05), round(tES - 0.2 - U(0.05), 3), "POR QUE A PRESSÃO CAI NO JEJUM?", y=160, fz=104, cor=AMAR, z=48),
      GIG(U(0), u['pensa'] - 0.15, "JEJUM", y=1250, tam=560, cont=True, cor="rgba(255,212,0,.25)"),
      {"tipo": "cartao", "t": DECK0, "d": round(DECK1 - DECK0, 3), "box": [126, 462, 900, 1060], "cor": "#d2c39d", "entra": "pop", "z": 14},
      {"tipo": "cartao", "t": DECK0, "d": round(DECK1 - DECK0, 3), "box": [108, 446, 900, 1060], "cor": "#e4d7b6", "entra": "pop", "z": 15}]
for i, (t0, txt, aba, gig) in enumerate(cards):
    ini = U(t0)
    fim = U(cards[i + 1][0] + 0.35) if i + 1 < len(cards) else DECK1
    d = round(fim - ini, 3)
    zc = 20 + 3 * i
    c += [{"tipo": "cartao", "t": ini, "d": d, "box": [90, 430, 900, 1060], "aba": aba, "entra": "whip", "z": zc},
          TC(ini + 0.15, d - 0.15, txt, 490) | {"z": zc + 1},
          GIG(ini, d, gig, y=1495, tam=240, cor="rgba(255,212,0,.16)", ida=(i % 2 == 0))]
# desenhos de cada cartão (z acima do cartão e do texto)
t1, t2, t3, t4, t5 = [U(x[0]) for x in cards]
f1 = U(cards[1][0] + 0.35); f2 = U(cards[2][0] + 0.35); f3 = U(cards[3][0] + 0.35); f4 = U(cards[4][0] + 0.35)
c += [FIS(t1 + 0.2, f1 - t1 - 0.2, [{"k": "vaso_mangueira", "xy": [540, 1110], "s": 1.5, "t": 0.0, "rotulo": "JATO FORTE", "rot_y": 200, "cor_rotulo": AZUL}],
          z=22, fluxos=[{"de": [378, 1155], "para": [642, 1155], "curva": 0, "cor": AZUL, "t": 0.3, "d": 1.9, "n": 7, "r": 11, "viagem": 0.6}],
          pulsos=[{"o": 0, "t": 0.9}]),
      FIS(t2 + 0.2, f2 - t2 - 0.2, [{"k": "jp_prato_vazio", "xy": [540, 1110], "s": 1.5, "t": 0.0}], z=25,
          pulsos=[{"o": 0, "t": 1.2}]),
      FIS(t3 + 0.2, f3 - t3 - 0.2, [{"k": "rim", "xy": [570, 1060], "s": 1.35, "t": 0.0, "rotulo": "XIXI", "rot_y": 218, "cor_rotulo": AZUL}], z=28,
          fluxos=[{"de": [462, 1075], "para": [462, 1318], "curva": 0, "cor": AZUL, "t": 0.5, "d": 2.2, "n": 6, "r": 13, "viagem": 0.8},
                  {"de": [462, 1075], "para": [462, 1318], "curva": 0, "cor": "#ffffff", "t": 0.75, "d": 2.0, "n": 5, "r": 8, "viagem": 0.8}],
          pulsos=[{"o": 0, "t": 0.6}]),
      FIS(t4 + 0.2, f4 - t4 - 0.2, [{"k": "vaso_mangueira_fraco", "xy": [540, 1110], "s": 1.5, "t": 0.0, "rotulo": "JATO FRACO", "rot_y": 200, "cor_rotulo": AZUL}],
          z=31, fluxos=[{"de": [378, 1155], "para": [642, 1155], "curva": 0, "cor": AZUL, "t": 0.4, "d": 2.4, "n": 3, "r": 9, "viagem": 1.3}]),
      FIS(t5 + 0.2, DECK1 - t5 - 0.2, [{"k": "silhueta_levantando", "xy": [520, 1100], "s": 1.45, "t": 0.0}], z=34,
          fluxos=[{"de": [636, 945], "para": [621, 1318], "curva": 0, "cor": VERM, "t": 0.5, "d": 2.0, "n": 6, "r": 12, "viagem": 0.8}],
          pulsos=[{"o": 0, "t": 1.0}, {"o": 0, "t": 2.0}])]

# ================= estudo (neutro), pele notícia =================
e_cento, e_uns, e_a, e_so, e_e, e_E = w('es', 'cento'), w('es', 'uns'), w('es', 'a'), w('es', 'só', 1), w('es', 'e', 3), w('es', 'e', 4)
# 'só' (1) = "Só que"; 'e' (3) = "e quem fez", (4) = "E lá"  -> conferido na saída do prep
ES_FIM = round(tOQ - tES, 3)
c += [FL(tES),
      {"tipo": "texto", "t": E(0.1), "d": round(ES_FIM - 0.1, 3), "xy": [40, 128], "w": 1000, "fonte": "900 34px Montserrat", "cor": "#ffffff", "alinha": "center",
       "txt": "● CHECAGEM · O QUE A CIÊNCIA DIZ", "css": "letter-spacing:3px;background:#ff2d3d;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"},
      {"tipo": "artigo", "t": E(0.2), "d": round(e_so - 0.25, 3), "box": [100, 290, 880, 640], "z": 34,
       "revista": "Journal of Manipulative and Physiological Therapeutics · 2001", "titulo": "Jejum só de água, com supervisão médica, no tratamento da pressão alta",
       "autores": "Goldhamer e col. · série de casos, sem grupo controle", "rola": 0,
       "linhas": [{"txt": "174 pessoas com pressão alta, internadas.", "grifo": E(e_cento + 0.1)},
                  {"txt": "Uns 10 a 11 dias só de água.", "grifo": E(e_uns + 0.1)},
                  {"txt": "A pressão caiu 37/13 mmHg, em média.", "grifo": E(e_a + 0.3)}],
       "rodape": "doi 10.1067/mmt.2001.115263"},
      GIG(E(0), e_cento - 0.1, "2001", y=1450, tam=420, cor="rgba(255,212,0,.12)"),
      TT(E(0.15), e_cento - 0.25, "O ESTUDO MAIS CITADO: 2001", y=1010, fz=120),
      FL(E(e_cento - 0.1)),
      GIG(E(e_cento - 0.1), e_uns - e_cento - 0.25, "174", y=1450, tam=440, cont=True, cor="rgba(255,212,0,.25)", ida=False),
      NUM(E(e_cento - 0.1), e_uns - e_cento - 0.25, 174, rotulo="pessoas internadas", conta=0.9),
      FL(E(e_uns - 0.35)),
      GIG(E(e_uns - 0.35), e_a - e_uns + 0.35, "10 DIAS", y=1450, tam=380, cor="rgba(127,211,255,.14)"),
      NUM(E(e_uns - 0.35), round(e_a - e_uns + 0.35, 3), 10, suf=" DIAS", cor=AZUL, sombra="#0d4f78", rotulo="só de água", conta=0.6, tam=240),
      FL(E(e_a)),
      GIG(E(e_a), e_so - e_a - 0.1, "-37", y=1450, tam=440, cont=True, cor="rgba(255,77,77,.28)", ida=False),
      NUM(E(e_a), round(e_so - e_a - 0.1, 3), 37, pre="-", suf=" mmHg", cor=VERM, sombra="#6b0f1a", rotulo="na máxima, em média", conta=1.0, tam=250),
      TT(E(w('es', 'quase') - 0.15), round(e_so - w('es', 'quase') + 0.05, 3), "QUASE 4 PONTOS", y=1420, fz=110, cor=AMAR, anim=None, entra="zoom"),
      FONTE(E(0.2), e_so - 0.25, "Goldhamer e col., J Manipulative Physiol Ther 2001 · doi 10.1067/mmt.2001.115263"),
      FL(E(e_so - 0.1)),
      GIG(E(e_so - 0.1), e_e - e_so + 0.3, "COMPARAR", y=1450, tam=330, cor="rgba(255,212,0,.12)"),
      TT(E(e_so - 0.1), e_e - e_so + 0.3, "SEM GRUPO PRA COMPARAR", y=420, fz=150, cor=AMAR),
      FIS(E(e_so + 0.2), e_e - e_so, [{"k": "jp_pessoa", "xy": [330, 1110], "s": 0.75, "t": 0.0, "rotulo": "JEJUM", "rot_y": 270},
                                          {"k": "jp_pessoa", "xy": [750, 1110], "s": 0.75, "t": 0.6, "rotulo": "SEM JEJUM", "rot_y": 270}], z=40),
      X(E(e_so + 1.2), e_e - e_so - 1.0, 750, 1120, s=120, z=46),
      FL(E(e_e + 0.2)),
      GIG(E(e_e + 0.2), e_E - e_e - 0.3, "CLÍNICA", y=1450, tam=380, cont=True, cor="rgba(255,212,0,.22)", ida=False),
      TT(E(e_e + 0.2), e_E - e_e - 0.3, "QUEM FEZ? A PRÓPRIA CLÍNICA", y=520, fz=150),
      {"tipo": "desenho", "t": E(w('es', 'própria') - 0.05), "d": round(e_E - w('es', 'própria') - 0.1, 3), "formas": [{"k": "sublinhado", "de": [120, 870], "ate": 960}], "espessura": 18, "cor": AMAR, "z": 44},
      FONTE(E(e_so - 0.1), e_E - e_so + 0.05, "Goldhamer e col., J Manipulative Physiol Ther 2001 · série de casos, sem grupo controle"),
      FL(E(e_E - 0.1)),
      GIG(E(e_E - 0.1), round(ES_FIM - e_E + 0.1, 3), "1 EM 4", y=1460, tam=400, cor="rgba(255,77,77,.16)"),
      TT(E(e_E - 0.05), round(ES_FIM - e_E + 0.05, 3), "OUTRO ESTUDO, MESMA CLÍNICA", y=300, fz=118),
      NUM(E(w('es', 'mais', 1) - 0.1), round(ES_FIM - w('es', 'mais', 1) + 0.1, 3), 4, pre="1 EM ", cor=VERM, sombra="#6b0f1a", de=4, conta=0.01,
          rotulo="com efeito colateral importante", y=610, tam=260),
      FIS(E(w('es', 'internação') - 0.1), round(ES_FIM - w('es', 'internação') + 0.1, 3),
          [{"k": "jp_pessoa_alerta", "xy": [270, 1180], "s": 0.55, "t": 0.0}, {"k": "jp_pessoa", "xy": [450, 1180], "s": 0.55, "t": 0.15},
           {"k": "jp_pessoa", "xy": [630, 1180], "s": 0.55, "t": 0.3}, {"k": "jp_pessoa", "xy": [810, 1180], "s": 0.55, "t": 0.45}],
          z=40, pulsos=[{"o": 0, "t": 1.6}, {"o": 0, "t": 2.6}]),
      FONTE(E(e_E - 0.1), round(ES_FIM - e_E + 0.1, 3), "Finnell e col., BMC Complement Altern Med 2018 · doi 10.1186/s12906-018-2136-6")]

# ================= o que fazer (manso) =================
o_pressao, o_diab, o_rem, o_grav, o_amam, o_so, o_E = (w('oq', 'pressão'), w('oq', 'diabetes'), w('oq', 'remédio'), w('oq', 'gravidez'),
                                                     w('oq', 'amamentação'), w('oq', 'só'), w('oq', 'e'))
OQ_FIM = round(tCO - tOQ, 3)
c += [FL(tOQ),
      GIG(O(0), o_pressao - 0.1, "CASA", y=1420, tam=480, cont=True, cor="rgba(255,212,0,.22)"),
      TT(O(0.05), o_pressao - 0.15, "NÃO FAÇA EM CASA", y=330, fz=140),
      FIS(O(0.1), o_pressao - 0.2, [{"k": "casa", "xy": [540, 980], "s": 1.25, "t": 0.0}], z=40),
      X(O(1.1), o_pressao - 1.2, 540, 960, s=200, z=46),
      FL(O(o_pressao - 0.1)),
      {"tipo": "checklist", "t": O(o_pressao - 0.1), "d": round(o_E - o_pressao, 3), "box": [140, 300, 800, 760], "titulo": "Tem algum desses?",
       "itens": [{"txt": "Pressão alta", "t": O(o_pressao), "marca": O(o_pressao + 0.4)}, {"txt": "Diabetes", "t": O(o_diab), "marca": O(o_diab + 0.4)},
                 {"txt": "Usa remédio", "t": O(o_rem), "marca": O(o_rem + 0.4)}, {"txt": "Gravidez", "t": O(o_grav), "marca": O(o_grav + 0.4)},
                 {"txt": "Amamentação", "t": O(o_amam), "marca": O(o_amam + 0.4)}], "z": 40},
      TT(O(o_so - 0.1), o_E - o_so + 0.0, "SÓ COM MÉDICO", y=1120, fz=150, cor=AMAR, anim=None, entra="zoom"),
      FL(O(o_E - 0.1)),
      GIG(O(o_E - 0.1), round(OQ_FIM - o_E + 0.1, 3), "SOZINHO", y=1420, tam=400, cor="rgba(255,77,77,.18)", ida=False),
      TT(O(o_E - 0.05), round(OQ_FIM - o_E + 0.05, 3), "REMÉDIO DE PRESSÃO", y=360, fz=140),
      CARIMBO(O(w('oq', 'para') - 0.1), round(OQ_FIM - w('oq', 'para') + 0.1, 3), "NÃO PARE SOZINHO", [120, 820], tam=104, rot=-6)]

# ================= cobrança (alegre) =================
k_nao = w('co', 'não')
CO_FIM = round(c1 - tCO, 3)
c += [FL(tCO),
      GIG(K(0), k_nao - 0.1, "MIÚDA", y=1420, tam=440, cont=True, cor="rgba(255,212,0,.22)"),
      TT(K(0.05), k_nao - 0.15, "LETRINHA MIÚDA", y=360, fz=150, cor=AMAR),
      {"tipo": "texto", "t": K(0.3), "d": k_nao - 0.4, "xy": [385, 905], "w": 310, "fonte": "600 28px Montserrat", "cor": "#ffffff", "alinha": "center",
       "txt": "sem grupo pra comparar · feito pela própria clínica · 1 em 4 com efeito colateral", "z": 40, "css": "text-shadow:0 2px 6px #000"},
      {"tipo": "desenho", "t": K(0.4), "d": k_nao - 0.5, "formas": [{"k": "circulo", "c": [540, 985], "r": [225, 225]}, {"k": "linha", "pts": [[705, 1150], [870, 1320]], "t": 0.3}],
       "espessura": 22, "cor": "#ffffff", "z": 44},
      FL(K(k_nao - 0.1)),
      GIG(K(k_nao - 0.1), round(CO_FIM - k_nao + 0.1, 3), "SEGUE", y=1420, tam=480, cor="rgba(255,212,0,.14)", ida=False),
      TT(K(k_nao - 0.05), round(CO_FIM - k_nao + 0.05, 3), "NÃO SEGUIR É DESFEITA", y=360, fz=150),
      {"tipo": "texto", "t": K(k_nao + 0.3), "d": round(CO_FIM - k_nao - 0.3, 3), "xy": [340, 1000], "w": 400, "fonte": "800 80px Montserrat", "cor": "#ffffff", "alinha": "center",
       "txt": "Seguir", "z": 45, "css": "background:#0095f6;border-radius:24px;padding:18px 0;box-shadow:0 12px 30px rgba(0,0,0,.45)", "entra": "pop"}]

# ================= CTA (banco cta6) + fecho (neutro) =================
f_sem = w('fe', 'sem')
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(F(0), f_sem - 0.1, "PRESSÃO", y=1420, tam=420, cont=True, cor="rgba(255,212,0,.22)"),
      TT(F(0.05), f_sem - 0.15, "PODE BAIXAR A PRESSÃO", y=360, fz=150),
      CHECK(F(0.6), f_sem - 0.7, 860, 760, s=70),
      FIS(F(0.15), f_sem - 0.25, [{"k": "vaso_mangueira_fraco", "xy": [540, 1110], "s": 1.3, "t": 0.0}], z=40),
      FL(F(f_sem - 0.1)),
      GIG(F(f_sem - 0.1), round(dur - F(f_sem - 0.1), 3), "MÉDICO", y=1460, tam=440, cor="rgba(255,77,77,.16)", ida=False),
      TT(F(f_sem - 0.05), round(dur - F(f_sem - 0.05), 3), "SEM MÉDICO, PODE DERRUBAR VOCÊ", y=300, fz=135),
      FIS(F(f_sem + 0.1), round(dur - F(f_sem + 0.1), 3), [{"k": "silhueta_levantando", "xy": [540, 1030], "s": 1.1, "t": 0.0}], z=40, pulsos=[{"o": 0, "t": 0.8}]),
      CARIMBO(F(w('fe', 'derrubar') - 0.2), round(dur - F(w('fe', 'derrubar') - 0.2), 3), "EXAGERO", [260, 1290], tam=170, rot=-8),
      FONTE(F(0), round(dur - F(0), 3), "Goldhamer e col., 2001 · Finnell e col., 2018 · conteúdo educativo")]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json", "gain": 0.16},
       {"src": M + P + "_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + P + "_rosto.mp4", "t": vd, "ms": 0, "d": R1D, "palavras": M + P + "_r1.words.json"},
       {"src": M + P + "_ab_voz.wav", "t": tAB, "ms": 0, "d": DU['ab'], "palavras": M + P + "_ab_voz.words.json"},
       {"src": M + P + "_au_voz.wav", "t": tAU, "ms": 0, "d": DU['au'], "palavras": M + P + "_au_voz.words.json"},
       {"src": M + P + "_es_voz.wav", "t": tES, "ms": 0, "d": DU['es'], "palavras": M + P + "_es_voz.words.json"},
       {"src": M + P + "_oq_voz.wav", "t": tOQ, "ms": 0, "d": DU['oq'], "palavras": M + P + "_oq_voz.words.json"},
       {"src": M + P + "_co_voz.wav", "t": tCO, "ms": 0, "d": DU['co'], "palavras": M + P + "_co_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + P + "_fe_voz.wav", "t": c2, "ms": 0, "d": DU['fe'], "palavras": M + P + "_fe_voz.words.json"}]
# trilha por baixo de tudo depois do viral (inclusive CTA): nenhuma pausa fica muda
musica = [{"src": "m_investiga", "t": vd, "ms": 0, "d": round(c1 - vd + 0.3, 2), "gain": 0.22, "fade": 0.8},
          {"src": "m_emocao", "t": round(c1 - 0.2, 2), "ms": 0, "d": round(dur - c1 + 0.2, 2), "gain": 0.24, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "scratch", "t": vd + 0.55, "gain": 0.35}, {"src": "whoosh2", "t": vd + 1.45, "gain": 0.35},
       # abertura
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1, "gain": 0.5, "pico": 0.45},
       {"src": "boing", "t": A(a_nisso), "gain": 0.35}, {"src": "notif", "t": A(a_agora + 0.1), "gain": 0.4}, {"src": "whoosh2", "t": A(a_mostrado + 0.2), "gain": 0.3},
       {"src": "whoosh", "t": A(a_frase - 0.1), "gain": 0.4, "pico": 0.45}, {"src": "boom", "t": A(a_maior + 0.15), "gain": 0.5, "pico": 0.3, "d": 1.3},
       # aula: um whoosh por cartão
       {"src": "whoosh", "t": tAU, "gain": 0.4, "pico": 0.45}]
for (t0, _, _, _) in cards:
    sfx.append({"src": "whoosh2", "t": U(t0), "gain": 0.4})
    sfx.append({"src": "papel", "t": U(t0 + 0.12), "gain": 0.3})
sfx += [{"src": "boing", "t": U(cards[4][0] + 1.2), "gain": 0.3},
        # estudo
        {"src": "whoosh", "t": tES, "gain": 0.45, "pico": 0.45}, {"src": "pagina", "t": E(0.3), "gain": 0.5},
        {"src": "boom", "t": E(e_cento - 0.1), "gain": 0.5, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": E(e_uns - 0.35), "gain": 0.35},
        {"src": "boom", "t": E(e_a), "gain": 0.5, "pico": 0.3, "d": 1.2},
        {"src": "whoosh", "t": E(e_so - 0.1), "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": E(e_so + 1.2), "gain": 0.3},
        {"src": "whoosh2", "t": E(e_e + 0.2), "gain": 0.35}, {"src": "riser", "t": E(e_E - 1.4), "gain": 0.2, "d": 1.3},
        {"src": "boom", "t": E(w('es', 'mais', 1) - 0.1), "gain": 0.5, "pico": 0.3, "d": 1.3},
        # o que fazer
        {"src": "whoosh", "t": tOQ, "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": O(1.1), "gain": 0.3},
        {"src": "pagina", "t": O(o_pressao - 0.1), "gain": 0.4}] + [{"src": "boing", "t": O(x + 0.4), "gain": 0.2} for x in (o_pressao, o_diab, o_rem, o_grav, o_amam)] + [
        {"src": "whoosh2", "t": O(o_so - 0.1), "gain": 0.35}, {"src": "whoosh", "t": O(o_E - 0.1), "gain": 0.4, "pico": 0.45},
        {"src": "boom", "t": O(w('oq', 'para') - 0.1), "gain": 0.5, "pico": 0.3, "d": 1.2},
        # cobrança
        {"src": "whoosh2", "t": tCO, "gain": 0.35}, {"src": "scratch", "t": K(0.4), "gain": 0.25}, {"src": "whoosh", "t": K(k_nao - 0.1), "gain": 0.4, "pico": 0.45},
        {"src": "notif", "t": K(k_nao + 0.3), "gain": 0.4},
        # CTA e fecho
        {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.5},
        {"src": "boing", "t": F(0.6), "gain": 0.3}, {"src": "whoosh", "t": F(f_sem - 0.1), "gain": 0.4, "pico": 0.45},
        {"src": "boom", "t": F(w('fe', 'derrubar') - 0.2), "gain": 0.55, "pico": 0.3, "d": 1.5}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
    if L.get("z", 0) is None: L.pop("z")
salvar(PID, dur, 414, c, voz, sfx,
       {"r1_fim": r1, "esconde": [[0, 4.1]], "ys": [[4.1, vd, 1590], [vd, r1, 1060], [r1, tAU, 1720], [tAU, tES, 1735], [tES, c1, 1720], [c1, c2, 1560], [c2, dur, 1720]]})
p = json.load(open(f'planos/{PID}.json')); p['audio']['musica'] = musica
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tAB", tAB, "tAU", tAU, "tES", tES, "tOQ", tOQ, "tCO", tCO, "c1", c1, "c2", c2)
subprocess.run(["python3", "scripts/entrada.py", PID, "assets/midia/ent6.mp4", "assets/midia/ent6.mp4.words.json", "1.88",
                "“O MELHOR TRATAMENTO” PRA PRESSÃO?", "a fala que viralizou num podcast gringo"], check=True)
subprocess.run(["python3", "scripts/pele.py", PID, "noticia"], check=True)
