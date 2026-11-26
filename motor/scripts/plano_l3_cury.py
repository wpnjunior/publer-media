# plano_l3_cury.py (14/11, lote 3, TDAH Adulto Real): "é TDAH ou síndrome do pensamento acelerado?"
# Viral TikTok @augustocuryoficial (palestra), trecho 40,14-49,71 (9,57 s): "médico no mundo todo dando diagnósticos
# errados, como se fosse transtorno de déficit de atenção e hiperatividade, quando na verdade é síndrome do pensamento
# acelerado." -> MEIA VERDADE. Quem fala é médico e autor famoso: respeito total, nome dele fora da fala e da tela
# (só o @ no crédito do viral). Responde só às 2 afirmações do corte (erro de diagnóstico existe / a síndrome não é oficial).
# Legenda queimada dele (errada em 47-49,7 s) borrada no arquivo e fora do enquadramento da tela dividida.
# r1 SEM crédito novo: rosto 6cd9 do banco de reações (cx_r1 "Calma. Tem verdade aí, mas tem porém.", copiado para cy_r1).
# Voz: 3 blocos HeyGen por clima, sem atempo: A indignado (resposta), B manso (aula), C neutro (estudo + cobrança + fecho,
# partido em cy_c / cy_e / cy_d); pausas abertas sem crédito em tmp_cury/voz.py.
# Aula: EDIÇÃO FULL sem b-roll (gigantes Anton, número 3D, artigo 3D com grifo, uma ideia por cena) com a casa:
# TDAH = fiação de dentro; correria, ansiedade e sono ruim = barulho da rua que passa quando fecha a janela
# (fisio_extra/casa.svg + casa_fios, casa_janela_aberta, casa_janela, cy_relogio, cy_nuvem). Pele: LAB (TDAH: invenção lab,
# superpoder dossiê, café notícia, remédio lousa -> volta ao lab).
# Depois deste script:
#   python3 scripts/entrada.py react_l3_cury assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     'É TDAH OU “PENSAMENTO ACELERADO”?' 'a fala que viralizou com 284 mil views' && python3 scripts/pele.py react_l3_cury lab
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l3_cury'; P = 'cy'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}cy_{k}_voz.words.json'))
WA, WB, WC, WE, WD = W('a'), W('b'), W('c'), W('e'), W('d')
DA, DB, DC, DE, DD = [round(dur_de(f'{M}cy_{k}_voz.wav'), 3) for k in 'abced']
vd = 9.57
r1 = round(vd + 3.37 + 0.5, 2)          # cy_r1: última palavra termina em 3,37 s; 0,5 s de folga
tA = round(r1 + 0.15, 2)
tB = round(tA + DA + 0.45, 2)
tC = round(tB + DB + 0.8, 2)            # respiro depois da lição da aula (~1,0 s com trilha)
tE = round(tC + DC + 0.6, 2)
c1 = round(tE + DE + 0.1, 2)            # CTA 6cd9 (banco cta6, 4,12 s)
c2 = round(c1 + 4.12, 2)
tD = round(c2 + 0.15, 2)
dur = round(tD + DD + 0.85, 2)
a = lambda i: round(tA + WA[i]['s'], 3); b = lambda i: round(tB + WB[i]['s'], 3); e = lambda i: round(tC + WC[i]['s'], 3)
q = lambda i: round(tE + WE[i]['s'], 3); f = lambda i: round(tD + WD[i]['s'], 3)
ae = lambda i: round(tA + WA[i]['e'] + 0.2, 3)   # troca de cena na pausa depois da frase
AF = round(tC, 3)                       # fim visual da aula
CF = round(tE - 0.12, 3)
VERDE, AMAR, VERM, ROSA, CINZA = "#3ddc84", "#ffd400", "#ff2d3d", "#ff9fb4", "#9aa3ad"
SOMBRA = "text-shadow:7px 7px 0 #000"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.5}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}
def TT(t, d, txt, y=360, fz=120, cor="#ffffff", **k):
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SOMBRA, vel=0.09, **k)
def GIG(t, d, txt, y=1250, tam=430, cont=False, cor="rgba(198,255,61,.13)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos}; L.update(k); return L
def DS(t, d, formas, cor=VERM, lw=14, z=45, vel=0.45):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel}
def NOTA(t, d, txt, x, y, w=460, tam=92, cor=AMAR, rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg);text-shadow:4px 4px 0 #000"}
def BUSCA(t, d, txt, y=860):
    """barra de busca branca que digita (lista oficial de doenças)"""
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [90, y], "w": 900, "fonte": "700 80px Montserrat", "cor": "#111",
            "alinha": "left", "txt": "🔍 " + txt, "anim": "digita", "vel": 0.03, "z": 44,
            "css": "background:#ffffff;border-radius:60px;padding:30px 44px;box-shadow:0 20px 50px rgba(0,0,0,.5)"}
def PILULA(t, d, txt, y, cor=AMAR, cor_txt="#111", x=240, w=600, tam=84):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"900 {tam}px Montserrat", "cor": cor_txt,
            "alinha": "center", "txt": txt, "z": 45, "entra": "pop", "css": f"background:{cor};border-radius:26px;padding:18px 0"}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#c6ff3d;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"}

# ================= abertura: viral em tela dividida + caixinha de pergunta =================
c = abertura(P, vd, "@augustocuryoficial", "center 15%", "Mito ou verdade? 🧠", "Médicos confundem TDAH com outra síndrome?",
             [{"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 284.7, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta":
        L["botoes"] = ["MITO", "VERDADE", "MEIO A MEIO"]; L["escolha"] = 2
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(r1 - vd - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "104px Anton", "cor": "#ffffff", "alinha": "center",
       "txt": "ERRO DE DIAGNÓSTICO\\nEXISTE.\\nA SÍNDROME\\nNÃO É OFICIAL.", "z": 55, "entra": "pop",
       "css": "background:rgba(11,21,18,.92);border-radius:14px;height:909px;box-sizing:border-box;padding:70px 40px 0;line-height:1.12;text-shadow:6px 6px 0 #000"},
      {"tipo": "carimbo", "t": vd + 0.45, "d": round(r1 - vd - 0.45, 2), "xy": [170, 760], "txt": "MEIA VERDADE", "tam": 130, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)"},
      {"tipo": "video", "t": vd, "d": round(r1 - vd, 2), "ms": 0, "src": M + "cy_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (indignado): a parte certa e o porém =================
A2, A3, A4 = ae(7), ae(18), ae(25)
c += [GL(r1), FL(r1),
      # A1 erro de diagnóstico existe
      GIG(r1, A2 - r1, "ERRO", y=1150, tam=560, cont=True, cor="rgba(198,255,61,.35)"),
      TT(a(0), A2 - a(0) - 0.05, "A PARTE CERTA:", y=330, fz=110, cor=VERDE),
      TT(a(3), A2 - a(3) - 0.05, "ERRO DE DIAGNÓSTICO EXISTE", y=520, fz=140),
      DS(a(6), A2 - a(6) - 0.05, [{"k": "check", "c": [540, 1180], "s": 95}], cor=VERDE, lw=24),
      FL(A2),
      # A2 a síndrome não está na lista oficial de doenças
      GIG(A2, A3 - A2, "LISTA OFICIAL", y=1380, tam=360, ida=False),
      TT(A2 + 0.02, A3 - A2 - 0.05, "O PORÉM: NÃO ESTÁ NA LISTA OFICIAL DE DOENÇAS", y=300, fz=108, cor=AMAR),
      BUSCA(a(10), A3 - a(10) - 0.05, "síndrome do pensamento acelerado", y=820),
      PILULA(a(12), A3 - a(12) - 0.05, "como doença: nenhuma", y=1200, cor="#ffffff", cor_txt=VERM, x=140, w=800),
      F(A2, A4 - A2, "CID-11, a lista oficial de doenças da OMS (versão 2026): “racing thoughts” só como sintoma (MB21.B)"),
      FL(A3),
      # A3 pensamento acelerado aparece lá só como sintoma
      GIG(A3, A4 - A3, "SINTOMA", y=1380, tam=420, cont=True, cor="rgba(255,212,0,.35)"),
      TT(A3 + 0.02, A4 - A3 - 0.05, "SÓ COMO SINTOMA", y=330, fz=160, cor=AMAR),
      BUSCA(A3 + 0.1, A4 - A3 - 0.15, "pensamento acelerado", y=760),
      PILULA(a(21), A4 - a(21) - 0.05, "SINTOMA ✓", y=1000, cor=AMAR),
      FL(A4),
      # A4 não tem estudo com esse nome
      GIG(A4, tB - A4, "ZERO", y=1350, tam=520, ida=False),
      {"tipo": "numero", "t": A4 + 0.05, "d": round(tB - A4 - 0.1, 2), "xy": [0, 420], "valor": 0, "conta": 0.3, "tam": 420,
       "rotulo": "estudos com esse nome", "z": 44},
      F(A4, tB - A4, "PubMed, busca em 14/11/2026: “síndrome do pensamento acelerado” e “accelerated thinking syndrome” = 0 artigos")]

# ================= B (manso): AULA, edição full, a casa =================
S2, S3, S4, S5 = [round(b(i) - 0.15, 3) for i in (7, 15, 25, 34)]
HX, HY, HS = 430, 1110, 1.8                       # casa
hp = lambda x, y: [round(HX + x * HS), round(HY + y * HS)]
JX, JY = hp(156, 78)                              # centro da janela
c += [GL(tB), FL(tB), SELO(tB + 0.2, AF - tB - 0.2, "● AULA RÁPIDA")]
# S1 a atenção mora na frente do cérebro
c += [GIG(tB, S2 - tB, "ATENÇÃO", y=1420, tam=430),
      FIS(tB + 0.1, S2 - tB - 0.15, [{"k": "cerebro_lado", "xy": [560, 1080], "s": 1.9, "t": 0.0}],
          pulsos=[{"o": 0, "t": round(WB[1]['s'] + 0.1, 2)}, {"o": 0, "t": round(WB[4]['s'] + 0.1, 2)}]),
      TT(tB + 0.02, S2 - tB - 0.05, "ATENÇÃO: FRENTE DO CÉREBRO", y=300, fz=130),
      DS(b(1), S2 - b(1) - 0.05, [{"k": "seta", "de": [140, 1560], "para": [300, 1150], "curva": -50}], cor=AMAR, lw=15),
      NOTA(b(1), S2 - b(1) - 0.05, "aqui!", 60, 1560, w=300, tam=110, cor=AMAR, rot=-6),
      FL(S2)]
# S2 no TDAH amadurece mais devagar, desde criança (Shaw 2007: +3 anos)
c += [GIG(S2, S3 - S2, "DESDE CRIANÇA", y=1430, tam=330, cont=True, cor="rgba(198,255,61,.35)", ida=False),
      TT(S2 + 0.02, S3 - S2 - 0.05, "NO TDAH, ELA AMADURECE DEPOIS", y=290, fz=120),
      {"tipo": "numero", "t": b(10), "d": round(S3 - b(10) - 0.05, 2), "xy": [0, 640], "valor": 3, "pre": "+", "suf": " ANOS", "tam": 320,
       "rotulo": "de atraso", "z": 44},
      F(S2, S3 - S2, "Shaw e col., PNAS 2007 · 446 crianças com ressonância repetida · doi 10.1073/pnas.0707741104"),
      FL(S3)]
# S3-S5 a casa (camadas contínuas para não pular)
c += [FIS(S3 + 0.05, AF - S3 - 0.05, [{"k": "casa", "xy": [HX, HY], "s": HS, "t": 0.0}], z=30,
          pulsos=[{"o": 0, "t": round(WB[17]['s'] - WB[15]['s'] + 0.05, 2)}]),
      FIS(S3 + 0.25, S5 - S3 - 0.2, [{"k": "casa_janela_aberta", "xy": [JX, JY], "s": HS, "t": 0.0}], z=31),
      FIS(b(21), AF - b(21), [{"k": "casa_fios", "xy": [HX, HY], "s": HS, "t": 0.0}], z=32,
          pulsos=[{"o": 0, "t": 0.6}, {"o": 0, "t": round(WB[22]['s'] - WB[21]['s'] + 0.1, 2)}, {"o": 0, "t": round(S5 - b(21) + 1.6, 2)}],
          fluxos=[{"de": hp(-156, 150), "para": hp(-156, -14), "curva": 0, "cor": "#ffe94d", "t": 0.15, "d": 1.6, "n": 4, "r": 12, "viagem": 0.7},
                  {"de": hp(-156, -14), "para": hp(156, -14), "curva": 0, "cor": "#ffe94d", "t": 0.8, "d": 1.8, "n": 4, "r": 12, "viagem": 0.9}]),
      GIG(S3, S4 - S3, "FIAÇÃO", y=1430, tam=430),
      TT(b(17) - 0.1, S4 - b(17) + 0.05, "TDAH = FIAÇÃO\\nVEM DE DENTRO", y=270, fz=160, cor=AMAR, anim=None, entra="zoom"),
      NOTA(b(21) + 0.3, S4 - b(21) - 0.35, "fios", 820, 820, w=240, tam=100, cor=AMAR, rot=6),
      DS(b(21) + 0.3, S4 - b(21) - 0.35, [{"k": "seta", "de": [880, 930], "para": hp(120, -14), "curva": 30}], cor=AMAR, lw=12),
      FL(S4)]
# S4 correria, ansiedade e sono ruim = barulho da rua (entra pela janela)
ONDA = lambda dy, t0, dd: {"de": [1075, JY + dy], "para": [JX - 60, JY + dy - 10], "curva": -25, "cor": CINZA, "t": t0, "d": dd, "n": 6, "r": 12, "viagem": 0.85}
c += [GIG(S4, S5 - S4, "BARULHO", y=1450, tam=400, cont=True, cor="rgba(154,163,173,.45)", ida=False),
      TT(S4 + 0.02, S5 - S4 - 0.05, "CORRERIA, ANSIEDADE, SONO RUIM", y=240, fz=112, cor="#e6eaee"),
      TT(b(28) - 0.1, S5 - b(28) + 0.05, "= BARULHO DA RUA", y=500, fz=120, cor=AMAR, anim=None, entra="zoom"),
      FIS(S4 + 0.05, S5 - S4 + 0.25, [{"k": "cy_relogio", "xy": [955, 790], "s": 0.5, "t": 0.0},
                                      {"k": "cy_nuvem", "xy": [955, 990], "s": 0.5, "t": round(WB[26]['s'] - WB[25]['s'], 2)},
                                      {"k": "cf_lua", "xy": [960, 1460], "s": 0.5, "t": round(WB[28]['s'] - WB[25]['s'], 2)}], z=33,
          fluxos=[ONDA(40, 0.3, round(S5 - S4 - 0.3, 2)), ONDA(70, 0.6, round(S5 - S4 - 0.6, 2)), ONDA(100, 0.9, round(S5 - S4 - 0.9, 2))]),
      FL(S5)]
# S5 fecha a janela, o barulho passa (a fiação fica)
c += [FIS(S5 + 0.05, AF - S5 - 0.05, [{"k": "casa_janela", "xy": [JX, JY], "s": HS, "t": 0.0}], z=34, pulsos=[{"o": 0, "t": 0.5}]),
      GIG(S5, AF - S5, "PASSA", y=1450, tam=460),
      TT(S5 + 0.02, AF - S5 - 0.05, "O BARULHO PASSA.\\nA FIAÇÃO FICA.", y=270, fz=130, cor="#ffffff", anim=None, entra="zoom"),
      DS(b(37), AF - b(37), [{"k": "check", "c": [955, 1000], "s": 70}], cor=VERDE, lw=22)]
SFX_AULA = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.45, "pico": 0.45}, {"src": "boing", "t": b(1), "gain": 0.3},
            {"src": "scratch", "t": b(4), "gain": 0.3}, {"src": "boing", "t": b(4) + 0.1, "gain": 0.25},
            {"src": "whoosh2", "t": S2, "gain": 0.35}, {"src": "riser", "t": b(9), "gain": 0.2, "d": 1.4}, {"src": "boom", "t": b(10), "gain": 0.5, "pico": 0.3, "d": 1.2},
            {"src": "whoosh", "t": S3, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": S3 + 0.1, "gain": 0.3},
            {"src": "whoosh2", "t": b(18), "gain": 0.3}, {"src": "notif", "t": b(21) + 0.1, "gain": 0.3}, {"src": "whoosh2", "t": b(22), "gain": 0.3},
            {"src": "whoosh2", "t": S4, "gain": 0.35}, {"src": "boing", "t": S4 + 0.1, "gain": 0.22}, {"src": "boing", "t": b(26), "gain": 0.22},
            {"src": "boing", "t": b(28), "gain": 0.22}, {"src": "whoosh2", "t": b(30), "gain": 0.3},
            {"src": "papel", "t": S5 + 0.05, "gain": 0.45}, {"src": "notif", "t": b(37), "gain": 0.35}]

# ================= C (neutro): o estudo (Sibley 2018) =================
E3, E4 = round(e(17) - 0.15, 3), round(e(21) - 0.15, 3)
c += [GL(AF), FL(AF),
      {"tipo": "artigo", "t": tC, "d": round(E3 - tC - 0.05, 2), "box": [100, 300, 880, 640], "z": 34,
       "revista": "The American Journal of Psychiatry · 2018", "titulo": "Jovens acompanhados dos 10 aos 25 anos",
       "autores": "Sibley e col. · estudo MTA · 239 jovens sem TDAH na infância", "rola": 0,
       "linhas": [{"txt": "8 avaliações completas, com pais e professores.", "grifo": e(2)},
                  {"txt": "Quem parecia ter TDAH só depois de grande...", "grifo": e(9)},
                  {"txt": "...quase sempre tinha outra explicação.", "grifo": e(17) - 0.6}],
       "rodape": "doi 10.1176/appi.ajp.2017.17030298"},
      GIG(tC, E3 - tC, "ESTUDO", y=1420, tam=430, cont=True, cor="rgba(198,255,61,.3)"),
      TT(e(9), E3 - e(9) - 0.05, "PARECIA TDAH SÓ DEPOIS DE GRANDE?", y=1060, fz=104, cor=AMAR),
      FL(E3),
      GIG(E3, E4 - E3, "95%", y=1380, tam=520, ida=False),
      {"tipo": "numero", "t": E3 + 0.05, "d": round(E4 - E3 - 0.1, 2), "xy": [0, 420], "valor": 95, "suf": "%", "tam": 380,
       "rotulo": "não tinham TDAH", "z": 44},
      FL(E4),
      GIG(E4, CF - E4, "MOTIVO", y=1420, tam=420, cont=True, cor="rgba(255,159,180,.35)"),
      TT(E4 + 0.02, CF - E4 - 0.05, "O MOTIVO MAIS COMUM:", y=360, fz=120),
      TT(e(24) + 0.1, CF - e(24) - 0.15, "MUITO ÁLCOOL OU DROGA", y=700, fz=150, cor=ROSA, anim=None, entra="zoom"),
      F(tC, CF - tC, "Sibley e col., Am J Psychiatry 2018 · 239 jovens, 10 a 25 anos · doi 10.1176/appi.ajp.2017.17030298")]
# cobrança (fim do bloco C)
c += [FL(tE - 0.1),
      GIG(tE - 0.1, c1 - tE + 0.1, "AULA", y=1350, tam=520),
      TT(tE - 0.08, c1 - tE + 0.06, "NINGUÉM SAI COM DIAGNÓSTICO.\\nSAI COM AULA.", y=400, fz=130, anim=None, entra="zoom")]

# ================= CTA (banco cta6) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (neutro): fecho =================
D2, D3 = round(f(3) + 0.3, 3), round(f(13) - 0.15, 3)
c += [GL(c2), FL(c2),
      GIG(c2, D2 - c2, "CABEÇA A MIL", y=1430, tam=330),
      TT(c2 + 0.05, D2 - c2 - 0.05, "CABEÇA A MIL?", y=300, fz=180, cor=AMAR, anim=None, entra="zoom"),
      FIS(f(0) + 0.1, D2 - f(0) - 0.15, [{"k": "cerebro_lado", "xy": [540, 1080], "s": 1.3, "t": 0.0}],
          pulsos=[{"o": 0, "t": 0.4}, {"o": 0, "t": 0.9}, {"o": 0, "t": 1.4}]),
      {"tipo": "checklist", "t": D2 + 0.05, "d": round(D3 - D2 - 0.1, 2), "box": [120, 640, 840, 620], "titulo": "Na consulta:", "entra": "cai",
       "itens": [{"txt": "conversa com o seu médico", "t": D2 + 0.35, "marca": f(7)}, {"txt": "conta da sua infância", "t": f(8), "marca": f(12)}], "z": 40},
      GIG(D2, D3 - D2, "INFÂNCIA", y=1420, tam=400, cont=True, cor="rgba(198,255,61,.3)", ida=False),
      FL(D3),
      GIG(D3, dur - D3, "AVALIAÇÃO", y=1420, tam=380),
      TT(D3 + 0.05, dur - D3 - 0.05, "ERRO SE CORRIGE COM AVALIAÇÃO.", y=360, fz=130),
      TT(f(20) - 0.2, dur - f(20) + 0.2, "NÃO COM NOME NOVO.", y=820, fz=150, cor=AMAR, anim=None, entra="zoom"),
      F(c2, dur - c2, "Sibley e col., Am J Psychiatry 2018 · Shaw e col., PNAS 2007 · Conteúdo educativo")]

voz = [{"src": M + "cy_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "cy_viral.words.json"},
       {"src": M + "cy_r1.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "cy_r1.words.json"},
       {"src": M + "cy_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "cy_a_voz.words.json"},
       {"src": M + "cy_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "cy_b_voz.words.json"},
       {"src": M + "cy_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "cy_c_voz.words.json"},
       {"src": M + "cy_e_voz.wav", "t": tE, "ms": 0, "d": DE, "palavras": M + "cy_e_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "cy_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "cy_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.45, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45},
       {"src": "notif", "t": a(6), "gain": 0.35}, {"src": "whoosh2", "t": A2, "gain": 0.35}, {"src": "teclado", "t": a(10), "gain": 0.3, "d": 1.6},
       {"src": "whoosh2", "t": A3, "gain": 0.35}, {"src": "boing", "t": a(23), "gain": 0.3},
       {"src": "whoosh", "t": A4, "gain": 0.4, "pico": 0.45}, {"src": "boom", "t": A4 + 0.3, "gain": 0.5, "pico": 0.3, "d": 1.4},
       {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, {"src": "pagina", "t": tC + 0.1, "gain": 0.5},
       {"src": "whoosh2", "t": e(9), "gain": 0.3}, {"src": "riser", "t": E3 - 1.2, "gain": 0.22, "d": 1.3}, {"src": "boom", "t": E3 + 0.05, "gain": 0.55, "pico": 0.3, "d": 1.5},
       {"src": "whoosh2", "t": E4, "gain": 0.35}, {"src": "boing", "t": e(25), "gain": 0.3},
       {"src": "whoosh", "t": tE - 0.1, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": q(5), "gain": 0.3},
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
       {"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "boing", "t": f(0) + 0.1, "gain": 0.3}, {"src": "papel", "t": D2 + 0.05, "gain": 0.45},
       {"src": "notif", "t": f(7), "gain": 0.3}, {"src": "notif", "t": f(12), "gain": 0.3},
       {"src": "whoosh2", "t": D3, "gain": 0.35}, {"src": "boom", "t": f(20), "gain": 0.5, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 317, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": round(r1 - 0.3, 2), "d": round(c1 - r1 + 0.6, 2), "gain": 0.16, "fade": 0.8},
                        {"src": "m_emocao", "t": round(c2 - 0.2, 2), "d": round(dur - c2 + 0.2, 2), "gain": 0.15, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "AF", AF, "tC", tC, "tE", tE, "c1", c1, "c2", c2, "tD", tD)
