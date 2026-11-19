# plano_l4_magro.py (14/11, lote 4, Caneta com Músculo): "magro não é exame" (nem todo magro é saudável, nem todo gordo é doente).
# Viral: vídeo de opinião do NYT (via @nytopinion), em inglês, dublado pela Murilo (original a 0,16 por baixo). Nome dela fora da
# fala e da tela (crédito só o @ do canal; a arroba dela fica fora do recorte). Dois pedaços cortados no corte de cena:
#   A 13,50-17,30 "Love yourself at any size, but don't forget that your heart has to beat, babes." (fora 8,7-12,0 e a cantora)
#   B 401,41-407,24 "Let me be clear, not every fat person is unhealthy. Not every skinny person is healthy." (sem o clipe antigo de top)
#   -> VERDADE (o mito é "magro é sempre saudável"). Nenhum comentário sobre corpo; a caneta só no "com ou sem caneta".
# Rosto r1 novo (6cd9, "Nisso ela tem razão. E tem número.") com o áudio do bloco neutro. Entrada ent6 e CTA cta6 do banco.
# Voz em 4 blocos por clima, sem atempo e SEM <break> (pausas abertas na edição, tmp_mx/voz.py):
#   a indignado (abertura) | b manso (aula) + o manso (o que fazer) | e neutro (estudos) + d neutro (fecho) | j alegre (cobrança)
# Aula: edição DOSSIÊ (pasta de papel, ficha datilografada, foto com clipe, carimbo) com a mala fechada na balança e a mesma mala
# aberta em corte (fisio_extra/mala_balanca.svg, mala_aberta_corte.svg). Pele NOTÍCIA no resto (o dossiê fica só na aula).
# Depois deste script:
#   python3 scripts/entrada.py react_l4_magro assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     'MAGRO É SINAL DE SAÚDE?' 'a fala que viralizou num vídeo de opinião' && python3 scripts/pele.py react_l4_magro noticia
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l4_magro'; P = 'mx'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}mx_{k}_voz.words.json'))
WA, WB, WE, WO, WJ, WD = W('a'), W('b'), W('e'), W('o'), W('j'), W('d')
DA, DB, DE, DO, DJ, DD = [round(dur_de(f'{M}mx_{k}_voz.wav'), 3) for k in 'abeojd']
vd = round(dur_de(M + 'mx_viral.mp4'), 3)       # 9,667 (A 3,80 + B 5,83)
VA = 3.80                                       # emenda A -> B
R1D = 2.82                                      # r1: última palavra termina em 2,32 s; 0,5 s de folga (último quadro 0,06 s sob o glitch)
r1 = round(vd + R1D, 3)
tA = round(r1 + 0.15, 3)
tB = round(tA + DA + 0.6, 3)
tC = round(tB + DB + 0.7, 3)                    # respiro depois da aula (trilha por baixo)
tO = round(tC + DE + 0.65, 3)
tJ = round(tO + DO + 0.6, 3)
c1 = round(tJ + DJ + 0.1, 3)                    # CTA 6cd9 (banco cta6, 4,12 s; "hoje." termina em 3,44)
c2 = round(c1 + 4.12, 3)
tD = round(c2 + 0.15, 3)
dur = round(tD + DD + 1.8, 2)
mk_ = lambda T0, WW: (lambda i: round(T0 + WW[i]['s'], 3))
a, b, e, o, j, f = mk_(tA, WA), mk_(tB, WB), mk_(tC, WE), mk_(tO, WO), mk_(tJ, WJ), mk_(tD, WD)
AF = tC                                         # fim visual da aula
BR, AMAR, VERDE, VERM, TINTA, CREME = '#ffffff', '#ffd400', '#3ddc84', '#ff4d4d', '#1c1a17', '#f6efdc'
VERM_P, VERDE_P, MANILA, PAPEL = '#b3121f', '#2e7d32', '#d6b273', '#fbf7ec'
SH = "text-shadow:0 6px 0 rgba(0,0,0,.35),0 0 24px rgba(0,0,0,.35)"
SP = "text-shadow:4px 4px 0 rgba(0,0,0,.12)"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.4, "fixo": True}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25, "fixo": True}
def TT(t, d, txt, y=330, fz=130, cor=BR, css=SH, z=40, **k):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=css, vel=0.09, **k); L["z"] = z; L["fixo"] = True; return L
def BOX(t, d, x, y, w, h, css, entra="pop", z=20, rot=0, **k):
    """caixa sem texto (pasta, folha, moldura de foto): texto vazio com fundo; fonte Anton 100 só para o portão de leitura."""
    L = {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": "100px Anton", "cor": TINTA, "alinha": "center",
         "txt": " ", "z": z, "entra": entra, "fixo": True, "css": f"height:{h}px;box-sizing:border-box;{css};transform:rotate({rot}deg)", "rot": rot}
    L.update(k); return L
def TIPO(t, d, txt, x, y, w, tam=80, cor=TINTA, z=30, entra="pop", css="", al="center"):
    """letra de máquina de escrever (dossiê)."""
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px 'Courier Prime',monospace", "cor": cor,
            "alinha": al, "txt": txt, "z": z, "entra": entra, "fixo": True, "css": f"letter-spacing:1px;{css}"}
def PIL(t, d, txt, x, y, w=900, tam=100, cor=AMAR, fundo="rgba(20,7,10,.9)", z=47):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"{tam}px Anton", "cor": cor, "alinha": "center",
            "txt": txt, "z": z, "entra": "pop", "fixo": True, "css": f"border:7px solid {cor};border-radius:34px;padding:4px 0 10px;background:{fundo};{SH}"}
def GIG(t, d, txt, y=1450, tam=420, cont=False, cor="rgba(255,212,0,.16)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12, "fixo": True,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, z=33, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": True, "cor_rotulo": "#ffffff"}; L.update(k); return L
def DS(t, d, formas, cor=AMAR, lw=16, z=45, vel=0.45):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel, "fixo": True}
def CARIMBO(t, d, txt, xy, tam=130, rot=-8, cor=VERM_P, z=60):
    return {"tipo": "carimbo", "t": round(t, 3), "d": round(d, 3), "xy": xy, "txt": txt, "tam": tam, "rot": rot, "z": z, "cor": cor,
            "blend": "normal", "css": "background:rgba(255,255,255,.92)", "fixo": True}
def NUM(t, d, valor, y=400, cor=AMAR, sombra='#5a0d10', z=44, **k):
    L = {"tipo": "numero", "t": round(t, 3), "d": round(d, 3), "xy": [0, y], "valor": valor, "tam": 300, "cor": cor, "sombra": sombra,
         "cor_rotulo": BR, "z": z, "fixo": True}
    L.update(k); return L
def FN(t, d, txt):
    L = F(t, d, txt); L["fixo"] = True; return L
def SELO(t, d, txt, cor="#ff2d3d", cor_txt=BR):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": cor_txt,
            "alinha": "center", "txt": txt, "css": f"letter-spacing:3px;background:{cor};border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}

# ================= abertura: viral em tela dividida + caixinha =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 1100], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 1027], "raio": 14, "pos": "center top",
      "arroba": "via @nytopinion", "respira": False, "zoom": [[0, 1.0, 0.01], [2.0, 1.04, 1.2], [VA, 1.0, 0.01], [VA + 1.5, 1.05, 1.5], [vd - 2.0, 1.0, 0.6]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [110, 1190], "w": 790, "topo": "Mito ou verdade? 👇", "txt": "Magro é sempre saudável?",
      "botoes": ["MITO", "VERDADE"], "vel": 0.025, "escolha": 0, "t_escolha": 3.3},
     {"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1255], "valor": 3.9, "dec": 1, "suf": " MILHÕES", "tam": 120, "rotulo": "de visualizações"},
     {"tipo": "glitch", "t": VA - 0.04, "d": 0.16},             # emenda dos dois pedaços
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 1027], "raio": 14, "sombra": False, "z": 29}]

# ================= r1: "Nisso ela tem razão. E tem número." =================
PAINEL = f"background:rgba(239,228,201,.97);border-radius:14px;height:1027px;box-sizing:border-box;line-height:1.1;{SP}"
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(R1D - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "170px Anton", "cor": VERDE_P, "alinha": "center",
       "txt": "NISSO ELA\\nTEM RAZÃO.", "z": 55, "entra": "pop", "fixo": True, "css": PAINEL + ";padding:200px 40px 0"},
      DS(vd + 0.5, round(R1D - 0.5, 2), [{"k": "check", "c": [520, 860], "s": 95}], cor=VERDE_P, lw=26, z=56),
      {"tipo": "video", "t": vd, "d": R1D, "ms": 0, "src": M + P + "_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (indignado): tamanho não é exame =================
A4 = round(a(19) - 0.2, 3)                      # "Achar que magro é sempre saudável? Não é."
CARD = f"background:{CREME};border-radius:24px;box-shadow:0 26px 50px rgba(0,0,0,.45)"
c += [GL(r1), FL(r1), SELO(tA + 0.2, round(tB - tA - 0.25, 3), "● CHECAGEM · O QUE A CIÊNCIA DIZ"),
      GIG(tA, round(A4 - tA, 3), "TAMANHO", y=1480, tam=420, cont=True, cor="rgba(255,212,0,.30)"),
      TT(tA + 0.02, round(A4 - tA - 0.05, 3), "TAMANHO NÃO É EXAME", y=270, fz=150),
      # cartão 1: mais peso, exame bom
      BOX(a(4) - 0.1, round(A4 - a(4) + 0.05, 3), 40, 690, 485, 730, CARD, z=30),
      {"tipo": "texto", "t": round(a(4), 3), "d": round(A4 - a(4), 3), "xy": [40, 712], "w": 485, "fonte": "100px Anton", "cor": TINTA, "alinha": "center",
       "txt": "MAIS\\nPESO", "z": 32, "entra": "pop", "fixo": True, "css": "line-height:1"},
      FIS(a(4), round(A4 - a(4), 3), [{"k": "cx_exame", "xy": [282, 1045], "s": 0.58, "t": 0.15}], z=33),
      DS(a(8), round(A4 - a(8), 3), [{"k": "check", "c": [262, 1062], "s": 66}], cor=VERDE_P, lw=24, z=36),
      {"tipo": "texto", "t": round(a(8), 3), "d": round(A4 - a(8), 3), "xy": [40, 1185], "w": 485, "fonte": "100px Anton", "cor": VERDE_P, "alinha": "center",
       "txt": "EXAME\\nBOM", "z": 32, "entra": "zoom", "fixo": True, "css": "line-height:1"},
      # cartão 2: menos peso, açúcar e pressão bagunçados
      BOX(a(10) - 0.1, round(A4 - a(10) + 0.05, 3), 555, 690, 485, 730, CARD, z=30),
      {"tipo": "texto", "t": round(a(10), 3), "d": round(A4 - a(10), 3), "xy": [555, 712], "w": 485, "fonte": "100px Anton", "cor": TINTA, "alinha": "center",
       "txt": "MENOS\\nPESO", "z": 32, "entra": "pop", "fixo": True, "css": "line-height:1"},
      FIS(a(10), round(A4 - a(10), 3), [{"k": "cx_exame", "xy": [797, 1045], "s": 0.58, "t": 0.15}], z=33),
      DS(a(15), round(A4 - a(15), 3), [{"k": "x", "c": [797, 1062], "s": 70}], cor=VERM_P, lw=24, z=36),
      {"tipo": "texto", "t": round(a(15), 3), "d": round(A4 - a(15), 3), "xy": [555, 1185], "w": 485, "fonte": "100px Anton", "cor": VERM_P, "alinha": "center",
       "txt": "EXAME\\nRUIM", "z": 32, "entra": "zoom", "fixo": True, "css": "line-height:1"},
      FL(A4),
      # o mito: a caixinha volta e o MITO é carimbado no "Não é."
      GIG(A4, round(tB - A4, 3), "MITO", y=1420, tam=520, cor="rgba(255,212,0,.14)", ida=False),
      {"tipo": "pergunta", "t": A4, "d": round(tB - A4, 3), "xy": [110, 420], "w": 860, "topo": "Mito ou verdade? 👇", "txt": "Magro é sempre saudável?",
       "botoes": ["MITO", "VERDADE"], "vel": 0.012, "escolha": 0, "t_escolha": a(25), "fixo": True},
      CARIMBO(a(25), round(tB - a(25), 3), "MITO", [330, 1000], tam=210, rot=-7)]
SFX_A = [{"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": r1, "gain": 0.45, "pico": 0.45}, {"src": "notif", "t": tA + 0.2, "gain": 0.35},
         {"src": "papel", "t": a(4) - 0.1, "gain": 0.4}, {"src": "boing", "t": a(8), "gain": 0.25}, {"src": "papel", "t": a(10) - 0.1, "gain": 0.4},
         {"src": "scratch", "t": a(15), "gain": 0.22}, {"src": "whoosh2", "t": A4, "gain": 0.35}, {"src": "notif", "t": A4 + 0.1, "gain": 0.3},
         {"src": "boom", "t": a(25), "gain": 0.45, "pico": 0.3, "d": 1.2}]

# ================= B (manso): AULA em DOSSIÊ (pasta de papel, só aqui) =================
K2 = round(b(8) - 0.15, 3)        # "diz o peso, não o que tem dentro."
K3 = round(b(16) - 0.25, 3)       # FICHA A: "Pode ser mais músculo, que gasta o açúcar do sangue."
K4 = round(b(26) - 0.25, 3)       # FICHA B: "Ou mais gordura dentro da barriga, que bagunça o açúcar e a pressão."
K3b = round(b(32) - 0.15, 3)
K5 = round(b(39) - 0.25, 3)       # "Mesmo peso, recheio diferente."
PASTA = f"background:{MANILA};border-radius:22px;box-shadow:0 34px 70px rgba(0,0,0,.6);background-image:linear-gradient(180deg,rgba(255,255,255,.12),rgba(0,0,0,.06))"
ABA = f"background:{MANILA};border-radius:20px 20px 0 0;padding:14px 0 0"
FOLHA = (f"background:{PAPEL};box-shadow:0 8px 18px rgba(0,0,0,.25);"
         "background-image:repeating-linear-gradient(0deg,transparent 0 76px,rgba(40,90,160,.08) 76px 78px)")
FOTO = "background:#ffffff;box-shadow:0 18px 34px rgba(0,0,0,.35);border:2px solid #ddd"
CLIPE = [(300, 668), (300, 586), (312, 572), (336, 572), (348, 586), (348, 690), (336, 704), (320, 704), (316, 690), (316, 600)]
MX, MY = 540, 935                  # centro do desenho dentro da foto
c += [GL(tB), FL(tB),
      {"tipo": "fundo", "t": round(tB - 0.05, 3), "d": round(AF - tB + 0.15, 3), "cor": "#1d140e", "cor2": "#5a3b24", "textura": "gradiente", "z": 14, "fixo": True},
      BOX(tB, round(K5 - tB + 0.1, 3), 50, 250, 980, 1340, PASTA, entra="cai", z=16, rot=-1),
      BOX(tB, round(K5 - tB + 0.1, 3), 90, 295, 900, 1250, FOLHA, entra="cai", z=17, rot=-1),
      TIPO(tB, round(K5 - tB + 0.1, 3), "CONFIDENCIAL · O QUE A BALANÇA NÃO VÊ", 120, 318, 840, tam=26, cor="#6b5a3a", z=18, entra="cai")]
# aba da pasta (troca a cada ficha)
for t0, t1, txt in ((tB, K3, "DOSSIÊ"), (K3, K4, "FICHA A"), (K4, K5, "FICHA B")):
    c += [{"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0 + 0.1, 3), "xy": [90, 160], "w": 420, "fonte": "700 80px 'Courier Prime',monospace",
           "cor": TINTA, "alinha": "center", "txt": txt, "z": 15, "entra": "cai" if t0 == tB else "desliza", "fixo": True, "css": ABA + ";height:120px;box-sizing:border-box"}]
# foto presa por clipe (fica nas 3 fichas)
c += [BOX(tB + 0.35, round(K5 - tB - 0.2, 3), 190, 600, 700, 640, FOTO, entra="pop", z=20, rot=-2),
      DS(tB + 0.55, round(K5 - tB - 0.4, 3), [{"k": "linha", "pts": CLIPE, "j": 1.5}], cor="#7d848c", lw=11, z=24, vel=0.35)]
# S1a "Subir na balança é pesar uma mala fechada:"
c += [TT(tB + 0.35, round(K2 - tB - 0.35, 3), "BALANÇA = MALA FECHADA", y=360, fz=120, cor=TINTA, css=SP, z=30),
      FIS(b(2) - 0.05, round(K3 - b(2) + 0.05, 3), [{"k": "mala_balanca", "xy": [MX, MY - 24], "s": 1.25, "t": 0.0}], z=22, pulsos=[{"o": 0, "t": round(b(6) - b(2) + 0.05, 3)}]),
      GIG(tB, round(K3 - tB, 3), "MALA FECHADA", y=1610, tam=300, cor="rgba(246,239,220,.10)")]
# S1b "diz o peso, não o que tem dentro."
c += [TT(K2, round(K3 - K2, 3), "A BALANÇA NÃO VÊ DENTRO", y=360, fz=115, cor=TINTA, css=SP, z=30, anim=None, entra="zoom"),
      TIPO(b(10) - 0.05, round(K3 - b(10) + 0.05, 3), "PESO: 70 KG", 190, 1290, 600, tam=80, z=30),
      DS(b(10) + 0.3, round(K3 - b(10) - 0.3, 3), [{"k": "check", "c": [850, 1335], "s": 45}], cor=VERDE_P, lw=18, z=31),
      {"tipo": "texto", "t": round(b(11) - 0.1, 3), "d": round(K3 - b(11) + 0.1, 3), "xy": [40, 700], "w": 1000, "fonte": "330px Anton", "cor": VERM_P,
       "alinha": "center", "txt": "?", "z": 34, "entra": "zoom", "fixo": True, "css": "text-shadow:0 0 0 #fff,8px 8px 0 rgba(255,255,255,.9)"}]
# S2 FICHA A: mais músculo, que gasta o açúcar do sangue
c += [FL(K3),
      TT(K3 + 0.05, round(K4 - K3 - 0.05, 3), "MÚSCULO GASTA O AÇÚCAR", y=360, fz=120, cor=TINTA, css=SP, z=30),
      FIS(K3, round(K4 - K3, 3), [{"k": "mala_aberta_corte", "xy": [MX, MY - 10], "s": 1.2, "t": 0.1},
                                  {"k": "musculo", "xy": [MX + 10, MY + 14], "s": 0.58, "t": round(b(19) - K3, 3), "rotulo": "MÚSCULO", "rot_y": 200},
                                  {"k": "gordura", "xy": [MX - 120, MY + 50], "s": 0.18, "t": round(b(19) - K3 + 0.2, 3)}],
          z=22, pulsos=[{"o": 1, "t": round(b(21) - K3 + 0.9, 3)}],
          fluxos=[{"de": [1000, 640], "para": [MX + 10, MY + 10], "curva": -150, "cor": "#ffffff", "t": round(b(21) - K3, 3), "d": 2.2, "n": 7,
                   "rotulo": "AÇÚCAR", "viagem": 0.9, "r": 10}]),
      TIPO(K3 + 0.2, round(K4 - K3 - 0.2, 3), "FICHA A · 70 KG", 140, 1290, 800, tam=80, z=30),
      GIG(K3, round(K4 - K3, 3), "MÚSCULO" if False else "FICHA A", y=1610, tam=300, cor="rgba(246,239,220,.10)", ida=False)]
# S3 FICHA B: mais gordura dentro da barriga, que bagunça o açúcar e a pressão
c += [FL(K4),
      TT(K4 + 0.05, round(K3b - K4 - 0.05, 3), "GORDURA DENTRO DA BARRIGA", y=360, fz=115, cor=TINTA, css=SP, z=30),
      TT(K3b, round(K5 - K3b, 3), "BAGUNÇA AÇÚCAR E PRESSÃO", y=360, fz=115, cor=VERM_P, css=SP, z=30, anim=None, entra="zoom"),
      FIS(K4, round(K5 - K4, 3), [{"k": "mala_aberta_corte", "xy": [MX, MY - 10], "s": 1.2, "t": 0.1},
                                  {"k": "gordura", "xy": [MX, MY + 18], "s": 0.66, "t": round(b(28) - K4, 3), "rotulo": "GORDURA", "rot_y": 205}],
          z=22, pulsos=[{"o": 1, "t": round(b(33) - K4, 3)}],
          fluxos=[{"de": [MX - 40, MY - 30], "para": [1000, 640], "curva": -150, "cor": "#ffffff", "t": round(b(33) - K4, 3), "d": 1.8, "n": 6,
                   "rotulo": "AÇÚCAR SOBRA", "viagem": 0.9, "r": 10}]),
      DS(b(36), round(K5 - b(36), 3), [{"k": "seta", "de": [945, 1180], "para": [945, 860], "curva": 0}], cor=VERM_P, lw=20, z=36),
      TIPO(K4 + 0.2, round(K5 - K4 - 0.2, 3), "FICHA B · 70 KG", 140, 1290, 800, tam=80, z=30),
      GIG(K4, round(K5 - K4, 3), "FICHA B", y=1610, tam=300, cor="rgba(246,239,220,.10)")]
# S4 as duas fichas lado a lado: mesmo peso, recheio diferente
MINI = f"background:{PAPEL};box-shadow:0 22px 44px rgba(0,0,0,.5)"
c += [FL(K5),
      BOX(K5, round(AF - K5, 3), 55, 560, 470, 760, MINI, entra="cai", z=20, rot=-3),
      BOX(K5 + 0.12, round(AF - K5 - 0.12, 3), 555, 560, 470, 760, MINI, entra="cai", z=20, rot=3),
      TIPO(K5 + 0.3, round(AF - K5 - 0.3, 3), "FICHA A", 55, 600, 470, tam=80, z=26),
      TIPO(K5 + 0.4, round(AF - K5 - 0.4, 3), "FICHA B", 555, 600, 470, tam=80, z=26),
      FIS(K5 + 0.3, round(AF - K5 - 0.3, 3), [{"k": "mala_aberta_corte", "xy": [290, 930], "s": 0.95}, {"k": "musculo", "xy": [298, 950], "s": 0.46},
                                             {"k": "mala_aberta_corte", "xy": [790, 930], "s": 0.95, "t": 0.1}, {"k": "gordura", "xy": [790, 952], "s": 0.52, "t": 0.1}], z=24),
      TIPO(K5 + 0.5, round(AF - K5 - 0.5, 3), "70 KG", 55, 1170, 470, tam=90, z=26),
      TIPO(K5 + 0.6, round(AF - K5 - 0.6, 3), "70 KG", 555, 1170, 470, tam=90, z=26),
      CARIMBO(b(40), round(AF - b(40), 3), "MESMO PESO", [215, 1320], tam=130, rot=-6),
      TT(b(41) - 0.1, round(AF - b(41) + 0.1, 3), "RECHEIO DIFERENTE", y=300, fz=135, cor=AMAR, z=40, anim=None, entra="zoom"),
      GIG(K5, round(AF - K5, 3), "RECHEIO", y=1560, tam=360, cont=True, cor="rgba(255,212,0,.35)")]
SFX_B = [{"src": "whoosh", "t": tB, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": tB + 0.3, "gain": 0.5},
         {"src": "papel", "t": tB + 0.35, "gain": 0.4}, {"src": "boing", "t": b(2) - 0.05, "gain": 0.22},
         {"src": "teclado", "t": b(10) - 0.05, "gain": 0.25, "d": 0.9}, {"src": "boing", "t": b(11) - 0.05, "gain": 0.25},
         {"src": "papel", "t": K3 + 0.05, "gain": 0.45}, {"src": "teclado", "t": K3 + 0.2, "gain": 0.2, "d": 0.8}, {"src": "whoosh2", "t": b(21), "gain": 0.3},
         {"src": "papel", "t": K4 + 0.05, "gain": 0.45}, {"src": "teclado", "t": K4 + 0.2, "gain": 0.2, "d": 0.8}, {"src": "scratch", "t": b(33), "gain": 0.22},
         {"src": "papel", "t": K5 + 0.05, "gain": 0.45}, {"src": "papel", "t": K5 + 0.2, "gain": 0.35},
         {"src": "boom", "t": b(40), "gain": 0.4, "pico": 0.3, "d": 1.2}, {"src": "whoosh2", "t": b(41) - 0.1, "gain": 0.3}]

# ================= E (neutro): os dois estudos =================
E2, E3, E4, E5, E6 = round(e(8) - 0.1, 3), round(e(14) - 0.25, 3), round(e(21) - 0.15, 3), round(e(35) - 0.25, 3), round(e(46) - 0.2, 3)
c += [GL(AF), FL(AF), SELO(AF + 0.2, round(tO - AF - 0.25, 3), "● O QUE A CIÊNCIA DIZ", cor=AMAR, cor_txt="#1c1012"),
      # E1 Clínica Mayo, peso normal
      {"tipo": "artigo", "t": round(AF + 0.05, 3), "d": round(E2 - AF - 0.05, 3), "box": [100, 330, 880, 700], "z": 34, "fixo": True,
       "revista": "European Heart Journal · 2010", "titulo": "Peso normal na balança, gordura alta no corpo",
       "autores": "Romero-Corral e col. · Clínica Mayo (EUA)", "rola": 0,
       "linhas": [{"txt": "Adultos com peso normal.", "grifo": round(e(5), 3)}, {"txt": "Gordura do corpo medida à parte.", "grifo": round(e(7), 3)}],
       "rodape": "doi 10.1093/eurheartj/ehp487"},
      GIG(AF, round(E2 - AF, 3), "ESTUDO", y=1300, tam=420, cont=True, cor="rgba(255,212,0,.30)"),
      FL(E2),
      # E2 seis mil adultos com peso normal
      NUM(E2, round(E3 - E2, 3), 6, y=330, suf=" MIL", rotulo="com peso normal", conta=0.6),
      FIS(E2, round(E3 - E2, 3), [{"k": "mala_balanca", "xy": [540, 1120], "s": 0.95, "t": 0.2}]),
      FL(E3),
      # E3 mais gordura no corpo
      GIG(E3, round(E4 - E3, 3), "GORDURA", y=1450, tam=420, ida=False),
      TT(E3 + 0.05, round(E4 - E3 - 0.05, 3), "MAIS GORDURA NO CORPO", y=330, fz=140),
      FIS(E3, round(E4 - E3, 3), [{"k": "gordura", "xy": [540, 1030], "s": 1.15, "t": 0.15}], pulsos=[{"o": 0, "t": round(e(17) - E3 + 0.3, 3)}]),
      FL(E4),
      # E4 quatro vezes mais chance de açúcar, pressão e gordura do sangue alterados juntos
      NUM(E4, round(E5 - E4, 3), 4, y=300, suf="X", tam=330, rotulo="mais chance", conta=0.5),
      TT(e(27) - 0.1, round(E5 - e(27) + 0.1, 3), "AÇÚCAR, PRESSÃO E GORDURA DO SANGUE", y=900, fz=115),
      PIL(e(33) - 0.05, round(E5 - e(33) + 0.05, 3), "ALTERADOS JUNTOS", 140, 1250, w=800, tam=100, cor=AMAR),
      GIG(E4, round(E5 - E4, 3), "4X", y=1450, tam=520, cor="rgba(255,212,0,.12)"),
      FN(AF, round(E5 - AF, 3), "Romero-Corral e col., Eur Heart J 2010 · 6.171 adultos · doi 10.1093/eurheartj/ehp487"),
      FL(E5),
      # E5 outro estudo, 3.600 adultos mais velhos
      {"tipo": "artigo", "t": round(E5 + 0.05, 3), "d": round(E6 - E5 - 0.05, 3), "box": [100, 330, 880, 700], "z": 34, "fixo": True,
       "revista": "The American Journal of Medicine · 2014", "titulo": "Mais músculo, menos risco de morrer",
       "autores": "Srikanthan e Karlamangla · 3.659 adultos mais velhos", "rola": 0,
       "linhas": [{"txt": "Homens de 55+ e mulheres de 65+.", "grifo": round(e(43), 3)}, {"txt": "Músculo medido, vida seguida por anos.", "grifo": round(e(45), 3)}],
       "rodape": "doi 10.1016/j.amjmed.2014.02.007"},
      GIG(E5, round(E6 - E5, 3), "ESTUDO", y=1300, tam=420, cont=True, cor="rgba(255,212,0,.30)", ida=False),
      FL(E6),
      # E6 mais músculo, uns 20% menos risco de morrer
      NUM(E6, round(tO - E6, 3), 20, y=330, pre="-", suf="%", rotulo="risco de morrer", conta=0.6),
      FIS(E6, round(tO - E6, 3), [{"k": "musculo", "xy": [540, 1110], "s": 1.05, "t": 0.2, "rotulo": "MAIS MÚSCULO", "rot_y": 190}],
          pulsos=[{"o": 0, "t": round(e(47) - E6 + 0.2, 3)}]),
      FN(E5, round(tO - E5, 3), "Srikanthan e Karlamangla, Am J Med 2014 · estudo de observação · doi 10.1016/j.amjmed.2014.02.007")]
SFX_E = [{"src": "whoosh", "t": AF, "gain": 0.4, "pico": 0.45}, {"src": "pagina", "t": AF + 0.1, "gain": 0.45},
         {"src": "whoosh2", "t": E2, "gain": 0.3}, {"src": "boom", "t": E2 + 0.1, "gain": 0.35, "pico": 0.3, "d": 1.0},
         {"src": "whoosh2", "t": E3, "gain": 0.3}, {"src": "boing", "t": E3 + 0.2, "gain": 0.22},
         {"src": "riser", "t": E4 - 1.0, "gain": 0.16, "d": 1.0}, {"src": "boom", "t": E4, "gain": 0.45, "pico": 0.3, "d": 1.3},
         {"src": "notif", "t": e(33) - 0.05, "gain": 0.3},
         {"src": "pagina", "t": E5 + 0.1, "gain": 0.45}, {"src": "whoosh2", "t": E6, "gain": 0.3}, {"src": "boom", "t": E6 + 0.1, "gain": 0.4, "pico": 0.3, "d": 1.2}]

# ================= O (manso): o que fazer (sem indicar nem contraindicar) =================
O2 = round(o(9) - 0.2, 3)
c += [GL(tO), FL(tO),
      GIG(tO, round(O2 - tO, 3), "EXAME", y=1460, tam=440, cont=True, cor="rgba(255,212,0,.30)"),
      TT(tO + 0.05, round(O2 - tO - 0.05, 3), "SAÚDE SE VÊ NO EXAME", y=300, fz=140),
      FIS(tO, round(O2 - tO, 3), [{"k": "cx_exame", "xy": [540, 960], "s": 1.0, "t": 0.2}]),
      PIL(o(3) - 0.1, round(O2 - o(3) + 0.1, 3), "COM O SEU MÉDICO", 90, 1240, w=900, tam=105, cor=AMAR),
      FL(O2),
      GIG(O2, round(tJ - O2, 3), "MÚSCULO" if False else "PERGUNTA", y=1460, tam=400, ida=False),
      TT(O2 + 0.05, round(tJ - O2 - 0.05, 3), "EMAGRECENDO?", y=300, fz=160),
      PIL(o(11) - 0.15, round(tJ - o(11) + 0.15, 3), "COM OU SEM CANETA", 90, 560, w=900, tam=105, cor=BR),
      TT(o(15) - 0.15, round(tJ - o(15) + 0.15, 3), "PERGUNTE: QUANTO DO PESO É MÚSCULO?", y=880, fz=120, cor=AMAR),
      FIS(o(22) - 0.1, round(tJ - o(22) + 0.1, 3), [{"k": "musculo", "xy": [540, 1330], "s": 0.75}], pulsos=[{"o": 0, "t": 0.5}])]
SFX_O = [{"src": "whoosh", "t": tO, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": tO + 0.2, "gain": 0.35}, {"src": "notif", "t": o(3), "gain": 0.3},
         {"src": "whoosh2", "t": O2, "gain": 0.3}, {"src": "boing", "t": o(11), "gain": 0.22}, {"src": "notif", "t": o(15), "gain": 0.28},
         {"src": "boing", "t": o(22), "gain": 0.22}]

# ================= J (alegre): cobrança =================
J2 = round(j(9) - 0.2, 3)
c += [GL(tJ), FL(tJ),
      TT(tJ + 0.05, round(J2 - tJ - 0.05, 3), "A BALANÇA NÃO TE CONTA O RECHEIO", y=300, fz=125),
      FIS(tJ, round(c1 - tJ, 3), [{"k": "mala_balanca", "xy": [540, 980], "s": 1.0, "t": 0.15}], pulsos=[{"o": 0, "t": round(j(6) - tJ, 3)}]),
      PIL(j(7) - 0.05, round(c1 - j(7) + 0.05, 3), "EU CONTO.", 240, 1320, w=600, tam=130, cor=AMAR),
      TT(J2, round(c1 - J2, 3), "O MÍNIMO: SEGUIR", y=300, fz=150, cor=AMAR, anim=None, entra="zoom"),
      GIG(tJ, round(c1 - tJ, 3), "RECHEIO", y=1500, tam=400, cont=True, cor="rgba(255,212,0,.30)")]
SFX_J = [{"src": "whoosh", "t": tJ, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": j(7), "gain": 0.28}, {"src": "whoosh2", "t": J2, "gain": 0.3},
         {"src": "notif", "t": J2 + 0.1, "gain": 0.3}]

# ================= CTA (rosto 6cd9, banco cta6) + fecho (neutro) =================
c += [{"tipo": "glitch", "t": round(c1 - 0.05, 3), "d": 0.25, "fixo": True},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.4, 1.08, 0.3]], "z": 40},
      {"tipo": "barra", "t": round(c1 + 0.2, 3), "d": 3.87, "y": 215, "txt": "COMBINADO: SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512", "fixo": True},
      GL(c2), FL(c2),
      GIG(c2, round(dur - c2, 3), "SAÚDE", y=1500, tam=460, cont=True, cor="rgba(255,212,0,.30)"),
      TT(tD + 0.05, round(dur - tD - 0.05, 3), "PESO, A BALANÇA MEDE.", y=300, fz=140),
      FIS(tD, round(dur - tD, 3), [{"k": "mala_balanca", "xy": [540, 830], "s": 0.85, "t": 0.15}]),
      TT(f(4) - 0.05, round(dur - f(4) + 0.05, 3), "SAÚDE, NÃO.", y=1060, fz=180, cor=AMAR, anim=None, entra="zoom"),
      CARIMBO(f(5) + 0.3, round(dur - f(5) - 0.3, 3), "TAMANHO NÃO É EXAME", [110, 1330], tam=78, rot=-5),
      FN(tD, round(dur - tD, 3), "Romero-Corral e col., Eur Heart J 2010 · Srikanthan e Karlamangla, Am J Med 2014")]
SFX_F = [{"src": "glitch", "t": c1 - 0.05, "gain": 0.4}, {"src": "notif", "t": c1 + 0.2, "gain": 0.35}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.4},
         {"src": "whoosh2", "t": f(4) - 0.05, "gain": 0.3}, {"src": "boom", "t": f(5) + 0.3, "gain": 0.45, "pico": 0.3, "d": 1.4}]

voz = [{"src": M + "mx_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "mx_viral.words.json", "gain": 0.16},
       {"src": M + "mx_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "mx_r1.mp4", "t": vd, "ms": 0, "d": round(R1D - 0.06, 3), "palavras": M + "mx_r1.words.json"},
       {"src": M + "mx_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "mx_a_voz.words.json"},
       {"src": M + "mx_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "mx_b_voz.words.json"},
       {"src": M + "mx_e_voz.wav", "t": tC, "ms": 0, "d": DE, "palavras": M + "mx_e_voz.words.json"},
       {"src": M + "mx_o_voz.wav", "t": tO, "ms": 0, "d": DO, "palavras": M + "mx_o_voz.words.json"},
       {"src": M + "mx_j_voz.wav", "t": tJ, "ms": 0, "d": DJ, "palavras": M + "mx_j_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "mx_d_voz.wav", "t": tD, "ms": 0, "d": DD, "palavras": M + "mx_d_voz.words.json"}]
sfx = ([{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "pagina", "t": 4.3, "gain": 0.35},
        {"src": "glitch", "t": VA - 0.04, "gain": 0.3}, {"src": "glitch", "t": vd - 0.05, "gain": 0.45}, {"src": "whoosh2", "t": vd + 0.05, "gain": 0.35},
        {"src": "boing", "t": vd + 0.5, "gain": 0.25}]
       + SFX_A + SFX_B + SFX_E + SFX_O + SFX_J + SFX_F)
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar(PID, dur, 1414, c, voz, sfx,
       {"r1_fim": r1, "esconde": [[vd, r1]], "ys": [[0, 4.05, 1700], [4.05, vd, 1660], [r1, c1, 1700], [c1, c2, 1560], [c2, dur, 1700]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_noticia", "t": round(vd - 0.2, 2), "ms": 0, "d": round(tB - vd + 0.6, 2), "gain": 0.22, "fade": 0.6},
                        {"src": "m_viagem", "t": round(tB - 0.4, 2), "ms": 0, "d": round(tC - tB + 0.8, 2), "gain": 0.15, "fade": 0.6},
                        {"src": "m_investiga", "t": round(tC - 0.4, 2), "ms": 0, "d": 22.8, "gain": 0.22, "fade": 0.8},
                        {"src": "m_emocao", "t": round(tC + 21.6, 2), "ms": 0, "d": round(dur - tC - 21.6, 2), "gain": 0.2, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
narr = sum(len(x) for x in (WA, WB, WE, WO, WJ, WD)); tnarr = DA + DB + DE + DO + DJ + DD
print("ok dur", dur, "| vd", vd, "r1", r1, "tA", tA, "tB", tB, "tC", tC, "tO", tO, "tJ", tJ, "c1", c1, "c2", c2, "tD", tD,
      "| aula", round(tC - tB, 2), "s | narração", narr, "palavras em", round(tnarr, 1), "s =", round(narr / tnarr * 60), "ppm")
