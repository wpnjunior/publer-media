# plano_l5_probio.py (15/11, lote 5, Papo de Médico): "melhor comer uma maçã do que tomar probiótico; as bactérias da cápsula
# vivem menos de uma hora" (gastroenterologista convidada do The Mel Robbins Podcast, TikTok @melrobbins), inglês, dublado pela Murilo.
# Trecho (2 pedaços, 11,08 s): A 0,00-4,585 (apresentadora pergunta; médica: "melhor comer uma maçã do que tomar probiótico";
#   o "My" seguinte começa em 4,62, conferido pela energia) + B 14,99-21,50 ("essas bactérias vivem talvez meia hora, quer dizer,
#   menos de uma hora"; "In order" começa em 21,60). Veredito MEIA VERDADE (caixinha DEPENDE).
# Recorte só da faixa do estúdio (y 186-1202 do original, tmp_pb/prep_viral.py): fora a caixa "Are Probiotics...", a legenda inglesa
#   e o RODAPÉ COM O NOME da médica. Nomes fora da fala e da tela; crédito só @melrobbins. Dois falantes: etiqueta na tela
#   (APRESENTADORA PERGUNTA / MÉDICA CONVIDADA RESPONDE) e a pergunta da Murilo 1,5 semitom acima.
# Rostos SEM crédito novo: entrada rk_ent ("Olha só essa notícia"), r1 cx_r1 ("Calma. Tem verdade aí, mas tem porém."),
#   CTA cta6_serio ("Se te ajudou, segue e curte.": o cta6 tem piada do dedão e a cobrança já tem piada).
# Voz: 3 create_speech por clima, sem atempo e sem <break> (pausas abertas na edição, tmp_pb/voz.py):
#   A alegre (abertura + cobrança) | M manso (aula + o que fazer) | N neutro (estudo + fecho). Dublagem Murilo 1 chamada.
# AULA na edição DOSSIÊ: quadro de cortiça "O CASO DA BACTÉRIA DA CÁPSULA", polaroides com tachinha e barbante vermelho
#   (intestino = prédio lotado; moradores = bactérias da casa; a da cápsula é visita: passa viva, não acha vaga, sai no cocô;
#   fibra da maçã = comida dos moradores). Desenhos novos fisio_extra/pb_*.svg (tmp_pb/svgs.py), cortiça assets/midia/pb_cortica.jpg.
# Pele LAB (Papo: jejum notícia, carnívora dossiê, protetor lousa, RFK notícia, banho dossiê).
# Depois deste script (o próprio script roda):
#   python3 scripts/entrada.py react_l5_probio assets/midia/pb_ent.mp4 assets/midia/pb_ent.mp4.words.json 2.18 \
#     'PROBIÓTICO É DINHEIRO JOGADO FORA?' 'a resposta que viralizou num podcast gringo' && python3 scripts/pele.py react_l5_probio lab
import sys, json, math, subprocess; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l5_probio'; P = 'pb'
def dur_de(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
def W(k): return json.load(open(f'{M}pb_{k}_voz.words.json'))
WAB, WAU, WES, WOQ, WCO, WFE = W('ab'), W('au'), W('es'), W('oq'), W('co'), W('fe')
DAB, DAU, DES, DOQ, DCO, DFE = [round(dur_de(f'{M}pb_{k}_voz.wav'), 3) for k in ('ab', 'au', 'es', 'oq', 'co', 'fe')]
vd = 11.08                               # pb_viral.mp4 (vídeo 11,078 s)
R1D = 3.87                               # pb_r1: "porém." termina em 3,37 + 0,5 s de folga
r1 = round(vd + R1D, 2)
tAB = round(r1 + 0.15, 3)
tAU = round(tAB + DAB + 0.5, 3)
tES = round(tAU + DAU + 0.7, 3)         # respiro depois da aula
tOQ = round(tES + DES + 0.6, 3)
tCO = round(tOQ + DOQ + 0.5, 3)
c1 = round(tCO + DCO + 0.1, 3)          # CTA 6cd9 (banco cta6_serio, 3,01 s; "curte." acaba em 2,42)
c2 = round(c1 + 3.01, 3)
tFE = round(c2 + 0.15, 3)
dur = round(tFE + DFE + 0.85, 2)
a_ = lambda k: round(tAB + WAB[k]['s'], 3); u_ = lambda k: round(tAU + WAU[k]['s'], 3); e_ = lambda k: round(tES + WES[k]['s'], 3)
o_ = lambda k: round(tOQ + WOQ[k]['s'], 3); q_ = lambda k: round(tCO + WCO[k]['s'], 3); f_ = lambda k: round(tFE + WFE[k]['s'], 3)
ABF, AF, ESF, OQF = round(tAU - 0.05, 3), round(tES - 0.05, 3), round(tOQ - 0.05, 3), round(tCO - 0.05, 3)
VERDE, AMAR, VERM, TINTA = "#3ddc84", "#ffd400", "#ff2d3d", "#1c1a17"
SOMBRA = "text-shadow:7px 7px 0 #000"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.45}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}
def TT(t0, t1, txt, y=250, fz=120, cor="#ffffff", **k):
    if 0.47 * fz * len(txt) > 940:
        um = int(940 / (0.47 * len(txt)))
        if um >= 108: fz = um
        else: fz = min(fz, 116); y = min(y, 230)
    return T(t0, round(t1 - t0, 3), txt, y=y, f=f"{fz}px Anton", cor=cor, css=SOMBRA, vel=0.09, **k)
def GIG(t0, t1, txt, y=1250, tam=430, cont=False, cor="rgba(255,212,0,.16)", ida=True, z=12):
    L = {"tipo": "gigante", "t": round(t0, 3), "d": round(t1 - t0, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": z,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t0, t1, orgaos, z=30, **k):
    L = {"tipo": "fisio", "t": round(t0, 3), "d": round(t1 - t0, 3), "z": z, "orgaos": orgaos}; L.update(k); return L
def DS(t0, t1, formas, cor=VERM, lw=14, z=45, vel=0.45):
    return {"tipo": "desenho", "t": round(t0, 3), "d": round(t1 - t0, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "vel": vel}
def EMO(t0, t1, ch, x, y, tam=170, z=38):
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": tam + 60, "fonte": f"{tam}px Montserrat", "cor": "#000",
            "alinha": "center", "txt": ch, "z": z, "entra": "pop", "css": "filter:drop-shadow(0 10px 12px rgba(0,0,0,.35))"}
def PILULA(t0, t1, txt, y, cor=AMAR, cor_txt="#111", x=140, w=800, tam=100, z=45):
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": w, "fonte": f"{tam}px Anton", "cor": cor_txt,
            "alinha": "center", "txt": txt, "z": z, "entra": "pop", "css": f"background:{cor};border-radius:26px;padding:14px 0;box-shadow:0 14px 30px rgba(0,0,0,.4)"}
def SELO(t0, t1, txt, cor="#ff2d3d"):
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [60, 128], "w": 960, "fonte": "900 32px Montserrat", "cor": "#ffffff",
            "alinha": "center", "txt": txt, "css": f"letter-spacing:3px;background:{cor};border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"}
def ROT(txt, x, y, cor="#ffffff", t=0.0):
    return {"k": "uq_vazio", "xy": [x, y], "s": 1.0, "t": t, "rotulo": txt, "rot_y": 20, "cor_rotulo": cor}
def RODAPE(t0, t1, txt, y=1592):
    L = F(t0, round(t1 - t0, 3), txt); L["xy"] = [40, y]; L["z"] = 86; return L
def CARIMBO(t0, t1, txt, x, y, tam=120, cor="#14964a", rot=-7, z=60):
    return {"tipo": "carimbo", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "txt": txt, "tam": tam, "rot": rot, "z": z,
            "cor": cor, "blend": "normal", "css": "background:rgba(255,255,255,.92)"}

# ---------- DOSSIÊ: cortiça, ficha, polaroide, tachinha, barbante ----------
def CORTICA(t0, t1):
    return {"tipo": "foto", "t": round(t0, 3), "d": round(t1 - t0, 3), "src": M + "pb_cortica.jpg", "box": [0, 0, 1080, 1920], "raio": 0,
            "sombra": False, "entra": "mascara", "kb": {"s": [1.02, 1.08], "x": [20, -30], "y": [0, -40]}, "z": 14}
def ETIQUETA(t0, t1, txt="ARQUIVO · O CASO DA BACTÉRIA DA CÁPSULA"):
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [110, 122], "w": 860, "fonte": "700 32px 'Courier Prime'", "cor": "#3a2414",
            "alinha": "center", "txt": txt, "z": 69, "entra": "desliza", "dy": -200,
            "css": "letter-spacing:2px;background:#e8d29a;border:3px solid #a8894a;border-radius:10px 10px 4px 4px;padding:12px 0;"
                   "box-shadow:0 8px 16px rgba(0,0,0,.35);transform:rotate(-1deg)"}
def CARTELA(t0, t1, txt, fz=104, y=212, cor=TINTA):
    """ficha datilografada do quadro: a informação principal da cena (Anton grande, tinta escura em papel)"""
    return {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [70, y], "w": 940, "fonte": f"{fz}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 44, "anim": "palavras", "vel": 0.09,
            "css": "background:#fffdf3;padding:18px 22px 12px;border-radius:6px;box-shadow:0 16px 30px rgba(0,0,0,.45);transform:rotate(-1.2deg);"
                   "background-image:repeating-linear-gradient(0deg,transparent 0 62px,rgba(40,90,160,.13) 62px 64px);line-height:1.08"}
def POLA(t0, t1, x, y, w, cap, rot=-3, entra="desliza", z=32):
    """polaroide: moldura branca com a área da foto (o desenho fisio entra por cima) e a legenda à mão embaixo.
    Devolve (camadas, centro da foto, ponto da tachinha)."""
    s = w - 40
    L = {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [x, y], "w": w, "fonte": "700 80px Caveat", "cor": "#2a2320",
         "alinha": "center", "txt": cap, "z": z, "entra": entra, "dx": 1150, "dy": 0, "rot": rot,
         "css": (f"background:radial-gradient(circle at 50% 38%,#fffaf0 0%,#dfe7ea 100%) 20px 20px/{s}px {s}px no-repeat,#fbf9f2;"
                 f"padding:{s + 26}px 10px 6px;box-shadow:0 24px 44px rgba(0,0,0,.5);transform:rotate({rot}deg);line-height:1;white-space:nowrap")}
    if entra == "cai": L.pop("dx"); L.pop("dy")
    pino = {"tipo": "texto", "t": round(t0 + 0.4, 3), "d": round(t1 - t0 - 0.4, 3), "xy": [x + w // 2 - 19, y - 14], "w": 38, "fonte": "10px Montserrat",
            "cor": "#000", "alinha": "center", "txt": " ", "z": z + 6, "entra": "pop",
            "css": "height:38px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ff9a9a 0%,#d11d1d 55%,#6a0808 100%);box-shadow:0 6px 7px rgba(0,0,0,.55)"}
    return [L, pino], (x + w // 2, y + 20 + s // 2), (x + w // 2, y + 5)
def BARBANTE(t0, t1, a, b, desce=60, z=37):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + desce
    return DS(t0, t1, [{"k": "linha", "pts": [list(a), [round(mx, 1), round(my, 1)], list(b)], "j": 1.5}], cor="#c81e1e", lw=7, z=z, vel=0.55)

c = []
# ================= abertura: viral em tela dividida + caixinha de pergunta =================
LAB = lambda t0, t1, txt, e="desliza": {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [96, 212], "w": 640, "fonte": "900 32px Montserrat",
                           "cor": "#ffffff", "alinha": "left", "txt": txt, "z": 36, "entra": e, "dx": -300, "dy": 0,
                           "css": "display:inline-block;width:auto;background:rgba(0,0,0,.72);border-radius:30px;padding:10px 22px;letter-spacing:1px"}
# cortes do viral (detecção de cena): 0-2,00 apresentadora pergunta | 2,00-4,54 médica | 4,54-6,84 apresentadora OUVE (a voz é da médica)
# | 6,84-fim médica. A etiqueta acompanha quem FALA e avisa quando a câmera está em quem ouve.
meio = [LAB(0.05, 2.0, "🎤 APRESENTADORA PERGUNTA"), LAB(2.0, 4.54, "🩺 MÉDICA CONVIDADA RESPONDE", "pop"),
        LAB(4.54, 6.84, "🩺 FALA A MÉDICA · APRESENTADORA OUVE", "pop"), LAB(6.84, vd - 0.02, "🩺 MÉDICA CONVIDADA RESPONDE", "pop"),
        # crédito: pílula própria em cima da marca d'água do TikTok (canto inferior esquerdo, só nos planos da apresentadora),
        # para não ficar arroba sobre arroba
        # a marca d'água muda de altura entre os planos (medida no quadro: plano 1 y 1032-1090, plano 3 y 907-967)
        *[{"tipo": "texto", "t": t0, "d": round(t1 - t0, 2), "xy": [x0, y0], "w": 300, "fonte": "800 30px Montserrat", "cor": "#ffffff", "alinha": "center",
           "txt": "@melrobbins", "z": 36, "entra": "nada", "css": f"background:rgba(8,8,8,.97);border-radius:16px;padding:{15 if y0 > 950 else 18}px 0"}
          for t0, t1, x0, y0 in ((0.0, 4.54, 140, 1002), (4.54, 6.84, 130, 897), (6.84, vd, 140, 1002))],
        {"tipo": "numero", "t": 4.3, "d": round(vd - 4.35, 2), "xy": [0, 1150], "valor": 488.5, "dec": 1, "suf": " MIL VIEWS", "tam": 120}]
c += abertura(P, vd, "", "center 50%", "Mito ou verdade? 🍎", "Probiótico em cápsula é dinheiro jogado fora?", meio)
for L in c:
    if L.get("tipo") == "pergunta":   # 3 botões: cartão mais largo para "VERDADE"/"DEPENDE" não encostarem na borda do botão
        L["botoes"] = ["MITO", "VERDADE", "DEPENDE"]; L["escolha"] = 2; L["xy"] = [90, 1150]; L["w"] = 900
c += [{"tipo": "texto", "t": vd + 0.02, "d": round(r1 - vd - 0.02, 2), "xy": [70, 190], "w": 940, "fonte": "112px Anton", "cor": "#ffffff", "alinha": "center",
       "txt": "ACERTOU O\\nPRINCIPAL.\\nERROU NA\\nMEIA HORA.", "z": 55, "entra": "pop",
       "css": "background:rgba(6,14,11,.93);border-radius:14px;height:909px;box-sizing:border-box;padding:56px 30px 0;line-height:1.12;text-shadow:6px 6px 0 #000"},
      CARIMBO(vd + 0.45, r1, "MEIA VERDADE", 165, 765, tam=110, cor="#d97a00", rot=-6),
      {"tipo": "video", "t": vd, "d": round(r1 - vd, 2), "ms": 0, "src": M + "pb_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= AB (alegre): saudável? ela acertou / a cápsula muda pouco / vive só meia hora? / aí não =================
A3, A4, A5 = round(tAB + 2.75, 3), round(a_(13) - 0.15, 3), round(a_(20) - 0.2, 3)
c += [GL(r1), FL(r1),
      TT(tAB + 0.02, A3, "SAUDÁVEL? ELA ACERTOU O PRINCIPAL", y=260, fz=120),
      FIS(tAB + 0.05, A3, [{"k": "jp_pessoa", "xy": [540, 1080], "s": 1.35, "t": 0.0}], pulsos=[{"o": 0, "t": round(WAB[3]['s'], 2)}]),
      DS(a_(6) - 0.05, A3, [{"k": "check", "c": [800, 860], "s": 95}], cor=VERDE, lw=26),
      FL(A3),
      GIG(A3, A4, "POUCO", y=1250, tam=430, cont=True, cor="rgba(255,212,0,.45)"),
      TT(A3 + 0.02, A4, "A CÁPSULA MUDA POUCO", y=280, fz=130, cor=AMAR),
      FIS(A3 + 0.05, A4, [{"k": "pb_capsula", "xy": [540, 1010], "s": 1.55, "t": 0.0}], pulsos=[{"o": 0, "t": round(WAB[11]['s'] - 2.75 + 0.1, 2)}]),
      FL(A4),
      TT(A4 + 0.02, A5, "VIVE SÓ MEIA HORA?", y=290, fz=150),
      FIS(A4 + 0.05, ABF, [{"k": "pb_relogio", "xy": [540, 1010], "s": 1.55, "t": 0.0}], pulsos=[{"o": 0, "t": round(WAB[18]['s'] - WAB[13]['s'] + 0.3, 2)}]),
      FIS(a_(14) - 0.05, A5, [{"k": "pb_bact_solo", "xy": [890, 1300], "s": 0.55, "t": 0.0}], z=31),
      TT(A5 + 0.02, ABF + 0.05, "AÍ NÃO.", y=300, fz=230, cor=VERM, anim=None, entra="zoom"),
      DS(a_(21) - 0.05, ABF, [{"k": "x", "c": [540, 1010], "s": 230}], cor=VERM, lw=34, vel=0.3)]
SFX_A = [{"src": "whoosh", "t": r1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": tAB + 0.15, "gain": 0.3}, {"src": "notif", "t": a_(6), "gain": 0.3},
         {"src": "whoosh2", "t": A3, "gain": 0.35}, {"src": "boing", "t": A3 + 0.1, "gain": 0.3},
         {"src": "whoosh2", "t": A4, "gain": 0.35}, {"src": "teclado", "t": A4 + 0.3, "gain": 0.22, "d": 1.2}, {"src": "boing", "t": a_(14), "gain": 0.25},
         {"src": "whoosh", "t": A5, "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": a_(21) - 0.05, "gain": 0.32},
         {"src": "boom", "t": a_(21) + 0.05, "gain": 0.5, "pico": 0.3, "d": 1.3}]

# ================= AU (manso): AULA no DOSSIÊ (quadro de cortiça, polaroides, barbante) =================
B2, B3, B4, B5 = [round(u_(k) - 0.15, 3) for k in (7, 14, 23, 35)]
c += [GL(tAU), FL(tAU), CORTICA(tAU, AF), ETIQUETA(tAU + 0.2, AF)]
# cena 1: intestino = prédio lotado
pa, ca, ka = POLA(tAU + 0.1, B2, 80, 560, 400, "INTESTINO", rot=-5)
pb, cb, kb = POLA(u_(5) - 0.25, B2, 495, 830, 540, "PRÉDIO LOTADO", rot=4)
c += [CARTELA(tAU + 0.05, B2, "INTESTINO = PRÉDIO LOTADO"), *pa, *pb,
      FIS(tAU + 0.45, B2, [{"k": "intestino", "xy": list(ca), "s": 0.78, "t": 0.0}], z=38),
      FIS(u_(5) + 0.1, B2, [{"k": "pb_predio", "xy": list(cb), "s": 1.15, "t": 0.0}], z=38, pulsos=[{"o": 0, "t": round(WAU[6]['s'] - WAU[5]['s'] + 0.1, 2)}]),
      BARBANTE(u_(5) + 0.3, B2, ka, kb, desce=50),
      FL(B2)]
# cena 2: moradores = bactérias da casa
pc, cc, kc = POLA(B2, B3, 210, 560, 660, "OS MORADORES", rot=-2)
c += [CARTELA(B2 + 0.03, B3, "MORADORES = BACTÉRIAS DA CASA"), *pc,
      FIS(B2 + 0.4, B3, [{"k": "pb_moradores", "xy": list(cc), "s": 1.45, "t": 0.0}], z=38,
          pulsos=[{"o": 0, "t": round(WAU[11]['s'] - WAU[7]['s'] + 0.15 + 0.1, 2)}, {"o": 0, "t": round(WAU[13]['s'] - WAU[7]['s'] + 0.15 + 0.1, 2)}]),
      FL(B3)]
# cena 3: a da cápsula chega de visita e passa viva
pd0, cd0, kd0 = POLA(B3, B4, 690, 540, 320, "CÁPSULA", rot=6)
pd, cd, kd = POLA(u_(18) - 0.25, B4, 90, 640, 580, "A VISITA", rot=-3)
c += [CARTELA(B3 + 0.03, B4, "VISITA: PASSA VIVA"), *pd0, *pd,
      FIS(B3 + 0.4, B4, [{"k": "pb_capsula", "xy": list(cd0), "s": 0.62, "t": 0.0}], z=38),
      FIS(u_(18) + 0.1, B4, [{"k": "pb_visita", "xy": list(cd), "s": 1.25, "t": 0.0}], z=38),
      BARBANTE(u_(18) + 0.25, B4, kd0, kd, desce=40),
      CARIMBO(u_(22) - 0.05, B4, "VIVA", 700, 1010, tam=110, cor="#14964a", rot=-10, z=46),
      FL(B4)]
# cena 4: em muita gente não acha vaga e sai no cocô
pe, ce, ke = POLA(B4, B5, 70, 560, 560, "SEM VAGA", rot=-4)
pf, cf, kf = POLA(u_(31) - 0.3, B5, 560, 960, 460, "SAÍDA", rot=5)
c += [GIG(B4, B5, "SEM VAGA", y=1420, tam=330, cor="rgba(70,35,10,.22)", z=15),
      CARTELA(B4 + 0.03, B5, "SEM VAGA: SAI NO COCÔ"), *pe, *pf,
      FIS(B4 + 0.4, B5, [{"k": "pb_semvaga", "xy": list(ce), "s": 1.24, "t": 0.0}], z=38, pulsos=[{"o": 0, "t": round(WAU[29]['s'] - WAU[23]['s'] + 0.15 + 0.1, 2)}]),
      FIS(u_(31) + 0.05, B5, [{"k": "pb_vaso", "xy": list(cf), "s": 0.98, "t": 0.0}], z=38,
          fluxos=[{"de": [ce[0] + 150, ce[1] + 120], "para": [cf[0] - 60, cf[1] + 40], "curva": -120, "cor": AMAR, "t": 0.35, "d": 1.4, "n": 4, "r": 17}]),
      BARBANTE(u_(31) + 0.2, B5, ke, kf, desce=70),
      FL(B5)]
# cena 5: a fibra da maçã é a comida dos moradores
pg, cg, kg = POLA(B5, AF, 55, 600, 480, "FIBRA", rot=-4)
ph, ch, kh = POLA(u_(41) - 0.3, AF, 560, 930, 480, "MORADORES", rot=4)
c += [CARTELA(B5 + 0.03, AF, "FIBRA = COMIDA DOS MORADORES"), *pg, *ph,
      FIS(B5 + 0.4, AF, [{"k": "pb_maca", "xy": list(cg), "s": 1.02, "t": 0.0}], z=38),
      FIS(u_(41) + 0.05, AF, [{"k": "pb_comendo", "xy": list(ch), "s": 1.0, "t": 0.0}], z=38, pulsos=[{"o": 0, "t": 0.8}, {"o": 0, "t": 1.6}],
          fluxos=[{"de": [cg[0] + 120, cg[1] + 140], "para": [ch[0] - 120, ch[1] + 10], "curva": -110, "cor": VERDE, "t": 0.3, "d": 1.4, "n": 5, "r": 15}]),
      BARBANTE(u_(41) + 0.15, AF, kg, kh, desce=60)]
SFX_U = [{"src": "whoosh", "t": tAU + 0.05, "gain": 0.45, "pico": 0.45}, {"src": "papel", "t": tAU + 0.25, "gain": 0.45}, {"src": "boing", "t": tAU + 0.5, "gain": 0.25},
         {"src": "papel", "t": u_(5), "gain": 0.45}, {"src": "boing", "t": u_(5) + 0.2, "gain": 0.25}, {"src": "scratch", "t": u_(5) + 0.3, "gain": 0.2},
         {"src": "whoosh2", "t": B2, "gain": 0.4}, {"src": "papel", "t": B2 + 0.2, "gain": 0.45}, {"src": "boing", "t": B2 + 0.45, "gain": 0.25},
         {"src": "whoosh2", "t": B3, "gain": 0.4}, {"src": "papel", "t": B3 + 0.2, "gain": 0.4}, {"src": "papel", "t": u_(18), "gain": 0.45},
         {"src": "scratch", "t": u_(18) + 0.25, "gain": 0.2}, {"src": "boom", "t": u_(22), "gain": 0.4, "pico": 0.3, "d": 1.2},
         {"src": "whoosh2", "t": B4, "gain": 0.4}, {"src": "papel", "t": B4 + 0.2, "gain": 0.45}, {"src": "papel", "t": u_(31) - 0.1, "gain": 0.4},
         {"src": "scratch", "t": u_(31) + 0.2, "gain": 0.2}, {"src": "whoosh", "t": u_(32), "gain": 0.25},
         {"src": "whoosh2", "t": B5, "gain": 0.4}, {"src": "papel", "t": B5 + 0.2, "gain": 0.45}, {"src": "papel", "t": u_(41) - 0.1, "gain": 0.4},
         {"src": "scratch", "t": u_(41) + 0.15, "gain": 0.2}, {"src": "boing", "t": u_(41) + 0.6, "gain": 0.25}, {"src": "boing", "t": u_(43) + 0.2, "gain": 0.25}]

# ================= ES (neutro): estudos =================
E3, E4, E5, E6, E7, E8, E9 = (round(e_(11) - 0.15, 3), round(e_(20) - 0.15, 3), round(e_(26) - 0.15, 3), round(e_(29) - 0.15, 3),
                              round(tES + 14.95, 3), round(e_(42) - 0.15, 3), round(e_(51) - 0.15, 3))
FONTE1 = "Zmora e col., Cell 2018 · Instituto Weizmann, Israel · doi 10.1016/j.cell.2018.08.041"
FONTE2 = "Kristensen e col., Genome Med 2016 · 7 ensaios com placebo, adultos saudáveis · doi 10.1186/s13073-016-0300-5"
HC = 980
MOLD = lambda t0, t1: {"tipo": "texto", "t": round(t0, 3), "d": round(t1 - t0, 3), "xy": [50, 490], "w": 980, "fonte": "120px Anton", "cor": TINTA,
                       "alinha": "center", "txt": " ", "z": 25, "entra": "nada",
                       "css": f"height:{HC}px;border-radius:12px;border:6px solid #3d6b5c;box-shadow:0 0 0 2400px rgba(6,14,11,.88)"}
DOCS7 = [(195, 760), (425, 760), (655, 760), (885, 760), (310, 1010), (540, 1010), (770, 1010)]
c += [GL(AF), FL(AF), SELO(tES + 0.2, ESF, "● O QUE OS ESTUDOS ACHARAM"),
      # E1-E2: Israel, 2018 (mapa escuro com alfinete)
      {"tipo": "mapa", "t": tES, "d": round(E3 - tES + 0.05, 3), "tema": "escuro", "area": [50, 490, 980, HC],
       "camera": [[tES, 25, 20, 0.9, 0], [tES + 0.5, 31.6, 37.2, 3.0, 2.2]],
       "pinos": [{"ll": [31.9, 34.8], "t": round(tES + 1.0, 3), "txt": "ISRAEL", "fs": 24, "stroke": "#000", "sw": 8, "cor_txt": "#ffffff", "cor": VERM}], "z": 20},
      MOLD(tES, E3 + 0.05),
      TT(tES + 0.02, E3, "CIENTISTAS DE ISRAEL, 2018", y=240, fz=118),
      RODAPE(tES + 0.2, E5, FONTE1),
      FL(E3),
      # E3: olharam o intestino por dentro
      TT(E3 + 0.02, E4, "OLHARAM O INTESTINO POR DENTRO", y=240, fz=118),
      FIS(E3 + 0.05, E4, [{"k": "intestino", "xy": [540, 1020], "s": 1.6, "t": 0.0}], z=30),
      FIS(E3 + 0.45, E4, [{"k": "pb_lupa", "xy": [650, 930], "s": 1.0, "t": 0.0}], z=32, pulsos=[{"o": 0, "t": 0.9}]),
      FL(E4),
      # E4: onze tipos de bactéria em cápsula
      {"tipo": "numero", "t": E4, "d": round(E5 - E4, 3), "xy": [0, 330], "valor": 11, "tam": 330, "rotulo": "TIPOS NA CÁPSULA", "z": 44},
      FIS(E4 + 0.3, E5, [{"k": "pb_capsula", "xy": [540, 1260], "s": 1.25, "t": 0.0}], z=30, pulsos=[{"o": 0, "t": 1.2}]),
      FL(E5),
      # E5: elas chegavam vivas
      TT(E5 + 0.02, E6, "CHEGAVAM VIVAS", y=280, fz=160, cor=VERDE),
      FIS(E5 + 0.05, E6, [{"k": "pb_bact", "xy": [520, 1050], "s": 1.5, "t": 0.0}], z=30),
      DS(e_(28), E6, [{"k": "check", "c": [850, 760], "s": 80}], cor=VERDE, lw=24),
      RODAPE(E5, E8, FONTE1),
      FL(E6),
      # E6: grudar na parede: cada pessoa, um jeito
      TT(E6 + 0.02, E7, "CADA PESSOA, UM JEITO", y=270, fz=140, cor=AMAR),
      FIS(E6 + 0.05, E8, [{"k": "jp_pessoa", "xy": [200, 700], "s": 0.5, "t": 0.0}, {"k": "jp_pessoa", "xy": [540, 700], "s": 0.5, "t": 0.12},
                          {"k": "jp_pessoa", "xy": [880, 700], "s": 0.5, "t": 0.24},
                          {"k": "pb_parede", "xy": [200, 1000], "s": 0.62, "t": 0.3}, {"k": "pb_parede", "xy": [540, 1000], "s": 0.62, "t": 0.4},
                          {"k": "pb_parede", "xy": [880, 1000], "s": 0.62, "t": 0.5}], z=30),
      FIS(e_(30) - 0.05, E7, [{"k": "pb_bact_solo", "xy": [130, 912], "s": 0.28, "t": 0.0}, {"k": "pb_bact_solo", "xy": [200, 912], "s": 0.28, "t": 0.1},
                              {"k": "pb_bact_solo", "xy": [270, 912], "s": 0.28, "t": 0.2}, {"k": "pb_bact_solo", "xy": [540, 912], "s": 0.28, "t": 0.3}], z=31),
      FIS(e_(33) - 0.05, E7, [ROT("MUITO", 200, 1110, cor=VERDE), ROT("POUCO", 540, 1110, cor=AMAR, t=0.15), ROT("NADA", 880, 1110, cor=VERM, t=0.3)], z=32),
      FL(E7),
      # E7: e o efeito passou
      TT(E7 + 0.02, E8, "O EFEITO PASSOU", y=270, fz=150),
      FIS(E7 + 0.05, E8, [], z=31,
          fluxos=[{"de": [200, 925], "para": [1160, 820], "curva": -160, "cor": AMAR, "t": 0.1, "d": 1.3, "n": 3, "r": 15},
                  {"de": [540, 925], "para": [1160, 860], "curva": -120, "cor": AMAR, "t": 0.3, "d": 1.1, "n": 1, "r": 15}]),
      FL(E8),
      # E8: revisão de 7 estudos com adultos saudáveis
      TT(E8 + 0.02, E9, "7 ESTUDOS COM ADULTOS SAUDÁVEIS", y=240, fz=118),
      FIS(e_(46) - 0.1, E9 + 0.05, [{"k": "pb_estudo", "xy": [x, y], "s": 0.62, "t": round(0.1 * k, 2)} for k, (x, y) in enumerate(DOCS7)], z=30),
      RODAPE(E8, ESF, FONTE2),
      FL(E9),
      # E9: em nenhum a variedade da flora mudou (0 de 7), comparando com cápsula de mentira
      # Kristensen 2016: nenhum dos 7 mudou a VARIEDADE (alfa-diversidade); 1 mudou a estrutura (beta). O rótulo diz só o que vale para os 7,
      # em Anton grande (rótulo pequeno de 5 palavras reprova na leitura)
      {"tipo": "numero", "t": E9, "d": round(ESF - E9, 3), "xy": [0, 300], "valor": 0, "suf": " DE 7", "tam": 260, "z": 44},
      {"tipo": "texto", "t": round(E9 + 0.25, 3), "d": round(ESF - E9 - 0.25, 3), "xy": [70, 668], "w": 940, "fonte": "100px Anton", "cor": "#ffffff",
       "alinha": "center", "txt": "MUDARAM A VARIEDADE DA FLORA", "z": 44, "anim": "palavras", "vel": 0.09, "css": SOMBRA},
      FIS(E9 + 0.05, ESF, [{"k": "pb_estudo", "xy": [130 + 137 * k, 1060], "s": 0.48, "t": round(0.05 * k, 2)} for k in range(7)], z=30,
          pulsos=[{"o": k, "t": round(e_(52) - E9 + 0.1 + 0.12 * k, 2)} for k in range(7)]),
      PILULA(e_(58) - 0.1, ESF, "VS. CÁPSULA DE MENTIRA", y=1250, cor="#ffffff", cor_txt="#111", x=110, w=860, tam=100)]
SFX_E = [{"src": "pagina", "t": tES + 0.05, "gain": 0.5}, {"src": "whoosh2", "t": tES + 0.5, "gain": 0.3}, {"src": "boing", "t": e_(10), "gain": 0.35},
         {"src": "whoosh2", "t": E3, "gain": 0.35}, {"src": "boing", "t": E3 + 0.5, "gain": 0.25},
         {"src": "riser", "t": E4 - 0.9, "gain": 0.16, "d": 1.0}, {"src": "boom", "t": E4, "gain": 0.45, "pico": 0.3, "d": 1.3},
         {"src": "whoosh2", "t": E5, "gain": 0.35}, {"src": "notif", "t": e_(28), "gain": 0.3},
         {"src": "whoosh2", "t": E6, "gain": 0.35}, *[{"src": "boing", "t": round(E6 + 0.1 + 0.12 * k, 3), "gain": 0.14} for k in range(3)],
         *[{"src": "boing", "t": round(e_(30) + 0.1 * k, 3), "gain": 0.12} for k in range(0, 5, 2)],
         {"src": "whoosh", "t": E7 + 0.1, "gain": 0.35}, {"src": "whoosh2", "t": E8, "gain": 0.35},
         *[{"src": "papel", "t": round(e_(46) - 0.1 + 0.1 * k, 3), "gain": 0.18} for k in range(0, 7, 2)],
         {"src": "boom", "t": E9, "gain": 0.45, "pico": 0.3, "d": 1.3}, {"src": "scratch", "t": e_(52) + 0.1, "gain": 0.25}, {"src": "boing", "t": e_(58) - 0.1, "gain": 0.3}]

# ================= OQ (manso): casos específicos / quem indica é o médico / fruta, verdura e feijão =================
O2, O3, O4 = round(o_(6) - 0.1, 3), round(o_(12) - 0.1, 3), round(o_(20) - 0.15, 3)
c += [GL(ESF + 0.05), FL(ESF + 0.05),
      TT(tOQ + 0.02, O2, "TEM USO EM CASOS ESPECÍFICOS", y=260, fz=118),
      FIS(tOQ + 0.05, O2, [{"k": "pb_capsula", "xy": [540, 1030], "s": 1.4, "t": 0.0}], z=30),
      FL(O2),
      TT(O2 + 0.02, O3, "QUEM INDICA? SEU MÉDICO", y=270, fz=130, cor=AMAR),
      EMO(O2 + 0.1, O3, "🩺", 360, 760, tam=300),
      FL(O3),
      TT(O3 + 0.02, O4, "FRUTA, VERDURA E FEIJÃO", y=270, fz=130),
      FIS(o_(16) - 0.1, OQF, [{"k": "pb_maca", "xy": [210, 820], "s": 0.62, "t": 0.0}], z=30),
      FIS(o_(17) - 0.1, OQF, [{"k": "alface", "xy": [540, 820], "s": 0.62, "t": 0.0}], z=30),
      FIS(o_(19) - 0.1, OQF, [{"k": "pb_feijao", "xy": [870, 830], "s": 0.62, "t": 0.0}], z=30),
      TT(O4 + 0.02, OQF + 0.05, "ALIMENTAM OS MORADORES", y=270, fz=130, cor=VERDE),
      FIS(O4 + 0.05, OQF, [{"k": "pb_comendo", "xy": [540, 1230], "s": 1.25, "t": 0.0}], z=31, pulsos=[{"o": 0, "t": 0.8}])]
SFX_O = [{"src": "whoosh", "t": tOQ, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": tOQ + 0.15, "gain": 0.28}, {"src": "whoosh2", "t": O2, "gain": 0.35},
         {"src": "notif", "t": O2 + 0.15, "gain": 0.3}, {"src": "whoosh2", "t": O3, "gain": 0.35},
         {"src": "boing", "t": o_(16), "gain": 0.28}, {"src": "boing", "t": o_(17), "gain": 0.28}, {"src": "boing", "t": o_(19), "gain": 0.28},
         {"src": "whoosh2", "t": O4, "gain": 0.3}, {"src": "boing", "t": O4 + 0.2, "gain": 0.3}]

# ================= CO (alegre): cobrança leve =================
C2 = round(q_(6) - 0.15, 3)
c += [GL(OQF + 0.05), FL(OQF + 0.05),
      TT(tCO + 0.02, C2, "DINHEIRO ECONOMIZADO 😉", y=290, fz=130, cor=AMAR),
      FIS(tCO + 0.05, C2, [{"k": "cr_cofrinho", "xy": [540, 1030], "s": 1.5, "t": 0.0}], z=30, pulsos=[{"o": 0, "t": 0.9}]),
      FL(C2),
      TT(C2 + 0.02, c1, "MAIS BARATO 😉", y=300, fz=170, cor=AMAR),
      {"tipo": "texto", "t": round(C2 + 0.1, 3), "d": round(c1 - C2 - 0.1, 3), "xy": [240, 900], "w": 600, "fonte": "900 120px Montserrat", "cor": "#ffffff",
       "alinha": "center", "txt": "Seguir", "z": 44, "entra": "pop", "css": "background:#0095f6;border-radius:34px;padding:26px 0;box-shadow:0 20px 50px rgba(0,0,0,.5)"},
      DS(q_(10) - 0.05, c1, [{"k": "circulo", "c": [540, 985], "r": [370, 150]}], cor=AMAR, lw=14, vel=0.5),
      EMO(C2 + 0.3, c1, "👆", 425, 1180, tam=170)]
SFX_C = [{"src": "whoosh2", "t": tCO, "gain": 0.35}, {"src": "boing", "t": tCO + 0.15, "gain": 0.3}, {"src": "notif", "t": tCO + 0.9, "gain": 0.3},
         {"src": "whoosh", "t": C2, "gain": 0.4, "pico": 0.45}, {"src": "notif", "t": C2 + 0.1, "gain": 0.35},
         {"src": "scratch", "t": q_(10) - 0.05, "gain": 0.25}, {"src": "boing", "t": q_(11) - 0.1, "gain": 0.3}]

# ================= CTA (banco cta6_serio) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": 3.01, "ms": 0, "src": M + "pb_cta.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 1.8, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 2.76, "y": 215, "txt": "TE AJUDOU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= FE (neutro): fecho + carimbo MEIA VERDADE =================
F2 = round(f_(6) - 0.15, 3)
c += [GL(c2), FL(c2),
      GIG(c2, F2, "VISITA", y=1300, tam=420),
      TT(c2 + 0.03, F2, "CÁPSULA É VISITA", y=300, fz=160),
      FIS(c2 + 0.08, F2, [{"k": "pb_visita", "xy": [540, 1000], "s": 1.35, "t": 0.0}], z=30),
      FL(F2),
      TT(F2 + 0.02, dur, "FIBRA ALIMENTA QUEM MORA", y=270, fz=140, cor=VERDE),
      FIS(F2 + 0.05, dur, [{"k": "pb_comendo", "xy": [540, 820], "s": 1.05, "t": 0.0}], z=30, pulsos=[{"o": 0, "t": 0.8}]),
      CARIMBO(F2 + 0.45, dur, "MEIA VERDADE", 140, 1110, tam=130, cor="#d97a00", rot=-6),
      RODAPE(c2, dur, "Zmora 2018 doi 10.1016/j.cell.2018.08.041 · Kristensen 2016 doi 10.1186/s13073-016-0300-5 · Conteúdo educativo", y=1560)]
SFX_F = [{"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": c2 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": c2 + 0.15, "gain": 0.25},
         {"src": "whoosh2", "t": F2, "gain": 0.35}, {"src": "boing", "t": F2 + 0.1, "gain": 0.25}, {"src": "boom", "t": F2 + 0.45, "gain": 0.5, "pico": 0.3, "d": 1.5}]

voz = [{"src": M + "pb_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "pb_viral.words.json", "gain": 0.16},
       {"src": M + "pb_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "pb_r1.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "pb_r1.words.json"},
       {"src": M + "pb_ab_voz.wav", "t": tAB, "ms": 0, "d": DAB, "palavras": M + "pb_ab_voz.words.json"},
       {"src": M + "pb_au_voz.wav", "t": tAU, "ms": 0, "d": DAU, "palavras": M + "pb_au_voz.words.json"},
       {"src": M + "pb_es_voz.wav", "t": tES, "ms": 0, "d": DES, "palavras": M + "pb_es_voz.words.json"},
       {"src": M + "pb_oq_voz.wav", "t": tOQ, "ms": 0, "d": DOQ, "palavras": M + "pb_oq_voz.words.json"},
       {"src": M + "pb_co_voz.wav", "t": tCO, "ms": 0, "d": DCO, "palavras": M + "pb_co_voz.words.json"},
       {"src": M + "pb_cta.mp4", "t": c1, "ms": 0, "d": 3.01, "palavras": M + "pb_cta.words.json"},
       {"src": M + "pb_fe_voz.wav", "t": tFE, "ms": 0, "d": DFE, "palavras": M + "pb_fe_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35}, {"src": "whoosh2", "t": 2.18, "gain": 0.22},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.45, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, *SFX_A,
       {"src": "glitch", "t": tAU - 0.05, "gain": 0.45}, *SFX_U,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, *SFX_E,
       {"src": "glitch", "t": ESF + 0.05, "gain": 0.4}, *SFX_O,
       {"src": "glitch", "t": OQF + 0.05, "gain": 0.4}, *SFX_C,
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, *SFX_F]
for L in c:
    if vd <= L.get("t", 0) < c1 - 0.06: L["fixo"] = True
salvar(PID, dur, 515, c, voz, sfx, {"r1_fim": r1, "esconde": [],
                                    "ys": [[0, 4.05, 1720], [4.05, vd, 1440], [vd, r1, 1060], [r1, tAU, 1700], [tAU, AF, 1735], [AF, dur, 1700]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": round(r1 - 0.3, 2), "d": round(tCO - r1 + 0.6, 2), "gain": 0.16, "fade": 0.8},
                        {"src": "m_humor", "t": round(tCO - 0.3, 2), "d": round(c1 - tCO + 0.6, 2), "gain": 0.13, "fade": 0.6},
                        {"src": "m_emocao", "t": round(c2 - 0.2, 2), "d": round(dur - c2 + 0.2, 2), "gain": 0.15, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tAB", tAB, "tAU", tAU, "AF", AF, "tES", tES, "tOQ", tOQ, "tCO", tCO, "c1", c1, "c2", c2, "tFE", tFE)
if '--sem-pos' not in sys.argv:
    subprocess.run(["python3", "scripts/entrada.py", PID, M + "pb_ent.mp4", M + "pb_ent.mp4.words.json", "2.18",
                    "PROBIÓTICO É DINHEIRO JOGADO FORA?", "a resposta que viralizou num podcast gringo"], check=True)
    subprocess.run(["python3", "scripts/pele.py", PID, "lab"], check=True)
