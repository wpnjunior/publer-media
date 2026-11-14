# plano_l2_banho.py (14/11, lote 2, Papo de Médico): "água gelada = cocaína" (TikTok @talktwenties, podcast britânico
# giftofthegabshow), inglês, dublado pela Murilo (original a 0,16 por baixo; legendas inglesas queimadas borradas).
# Trecho 41,75-53,56 s: "A imersão em água gelada é o único comportamento que aumenta a dopamina em 2,5 vezes. O mesmo que a
# cocaína faz. Só que, em vez de dar o pico em nove minutos e despencar, ela sobe por duas horas e meia." -> MITO
# (o número existe, mas é dopamina do SANGUE, em 1 h de imersão a 14 °C; a comparação com a droga vem de rato, medida no cérebro).
# Fonte: Šrámek et al., Eur J Appl Physiol 2000;81(5):436-42, doi 10.1007/s004210050065 (PMID 10751106);
#        Di Chiara & Imperato, PNAS 1988;85(14):5274-8, doi 10.1073/pnas.85.14.5274 (ratos, diálise no cérebro).
# Aula na EDIÇÃO CAIXINHA (cartão creme, aba lima, desenhos que se desenham, Caveat; sem b-roll). Pele: dossiê.
# Voz em blocos por clima (sem atempo): A indignado (r1 + abertura), B manso (aula), C neutro (estudo + honesto + segurança).
# r1 = os 4,75 s iniciais do bloco A no avatar 6cd9 (bh_rosto.mp4). Áudio preparado em tmp_bh/prep.py.
# Depois deste script:
#   python3 scripts/entrada.py react_l2_banho assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 'ÁGUA GELADA = COCAÍNA?' 'podcast britânico no TikTok'
#   python3 scripts/pele.py react_l2_banho dossie
import sys; sys.path.insert(0, 'scripts')
from mk import *
P = 'bh'
vd = 11.81
r1 = round(vd + 4.80, 2)            # rosto "Mito. A dopamina sobe, sim. Só que no lugar errado."
DA, DB, DC = 7.032, 20.036, 37.345  # bh_a_voz, bh_b_voz, bh_c_voz
tA = r1
tB = round(tA + DA + 0.45, 3)
tC = round(tB + DB + 0.55, 3)
t_cta = round(tC + DC + 0.3, 2); d_cta = 4.12
F0 = round(t_cta + d_cta + 0.05, 2)
dur = round(F0 + 3.8, 2)
a = lambda v: round(tA + v, 3)
b = lambda v: round(tB + v, 3)
k_ = lambda v: round(tC + v, 3)
SOMBRA = "text-shadow:8px 8px 0 #000"

c = abertura(P, vd, "via @talktwenties (TikTok)", "center 30%", "Mito ou verdade? 👇", "Água gelada dá a mesma onda da cocaína?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 5.2, "dec": 1, "suf": " MI VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta": L["escolha"] = 0
# R1: resposta grande + rosto embaixo
c += [{"tipo": "carimbo", "t": vd + 0.1, "d": 1.9, "xy": [250, 470], "txt": "MITO", "tam": 170, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)", "fixo": True},
      T(vd + 2.05, r1 - vd - 2.08, "SOBE, SIM. NO LUGAR ERRADO", y=440, f="130px Anton", cor="#f2c230", css=SOMBRA, fixo=True),
      rosto_r1(P, vd, r1 - vd, 0)]

# ---------------- ABERTURA DA NARRAÇÃO (A indignado) ----------------
c += B(P + "_viral_blur.mp4", tA, tB - tA, 20.0)
c += [{"tipo": "glitch", "t": tA - 0.05, "d": 0.25}, {"tipo": "flash", "t": tA, "d": 0.2, "max": 0.5},
      T(a(0.3), a(3.98) - a(0.3), "SOBE NO SANGUE, NÃO NO CÉREBRO", y=420, f="136px Anton", css=SOMBRA),
      {"tipo": "gigante", "t": a(0.9), "d": 2.4, "txt": "SANGUE", "y": 1050, "tam": 280, "cor": "#ff5a5f", "x": [1000, -1900], "z": 42},
      {"tipo": "flash", "t": a(4.0), "d": 0.2, "max": 0.5},
      T(a(4.02), tB - a(4.02) - 0.05, "IGUAL COCAÍNA? NÃO FAZ SENTIDO", y=420, f="136px Anton", cor="#f2c230", vel=0.1, css=SOMBRA),
      {"tipo": "gigante", "t": a(5.1), "d": 1.9, "txt": "NÃO", "y": 1050, "tam": 340, "cor": "rgba(255,255,255,.16)", "x": [1000, -1200], "z": 20}]

# ---------------- AULA RÁPIDA: EDIÇÃO CAIXINHA (sem b-roll) ----------------
TINTA = "#1c1a17"
ENT = 1.88   # entrada.py empurra "t" das camadas mas não os tempos internos de "abas"
S1, S2, S3, S4, S5, S6 = b(0.0), b(3.72), b(7.70), b(10.66), b(13.76), b(17.18)
A1 = tB; AF = round(tB + DB, 3)
def FR(t, d, txt, tam=112, y=385, cor=TINTA):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [95, y], "w": 890, "fonte": f"{tam}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 45, "anim": "palavras", "vel": 0.09, "fixo": True}
def NOTA(t, d, txt, x, y, w=420, tam=96, cor="#c0392b", rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg)", "fixo": True}
def FS(t, d, orgaos, **kw):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": 42, "orgaos": orgaos, "fixo": True}; L.update(kw); return L
def DS(t, d, formas, cor="#e0322b", lw=11):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": 44, "fixo": True}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}

c += [{"tipo": "glitch", "t": A1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": A1, "d": 0.2, "max": 0.5},
      {"tipo": "fundo", "t": A1, "d": AF - A1, "cor": "#0e1012", "textura": "gradiente", "cor2": "#1d2a33", "z": 11, "fixo": True},
      {"tipo": "cartao", "t": A1, "d": AF - A1, "box": [60, 330, 960, 1250], "aba": "1 · susto", "z": 30, "fixo": True,
       "abas": [[round(x + ENT, 3), y] for x, y in [[S2, "2 · sangue"], [S3, "3 · dopamina"], [S4, "4 · o muro"], [S5, "5 · não passa"], [S6, "6 · lá dentro"]]]},
      SELO(A1 + 0.2, AF - A1 - 0.2, "● AULA RÁPIDA · FRIO E DOPAMINA")]

# (1) A água gelada é um susto para o corpo.
c += [FR(S1 + 0.15, S2 - S1 - 0.2, "ÁGUA GELADA = SUSTO", tam=140),
      FS(S1 + 0.25, S2 - S1 - 0.3, [{"k": "bh_gota", "xy": [330, 1090], "s": 1.1, "t": 0.0},
                                    {"k": "raio", "xy": [770, 1060], "s": 0.85, "t": 1.45}], pulsos=[{"o": 1, "t": 1.9}, {"o": 1, "t": 2.6}]),
      NOTA(b(1.75), S2 - b(1.75) - 0.05, "susto!", 560, 1330, w=420, tam=120, cor="#c0392b", rot=-6)]
# (2) E o susto joga no sangue os hormônios do alerta.
c += [FR(S2 + 0.05, S3 - S2 - 0.1, "HORMÔNIOS DO ALERTA NO SANGUE", tam=108),
      FS(S2 + 0.1, S3 - S2 - 0.15, [{"k": "bh_vaso", "xy": [540, 1080], "s": 2.0, "t": 0.0, "rotulo": "SANGUE", "rot_y": 190}],
         fluxos=[{"de": [190, 1080], "para": [900, 1080], "curva": 0, "cor": "#ffd400", "t": b(4.8) - S2 - 0.1, "d": 2.8, "n": 9, "r": 16, "viagem": 1.2},
                 {"de": [190, 1060], "para": [900, 1100], "curva": 0, "cor": "#4dd8ff", "t": b(5.2) - S2 - 0.1, "d": 2.4, "n": 6, "r": 14, "viagem": 1.3}])]
# (3) A dopamina é um deles.
c += [FR(S3 + 0.05, S4 - S3 - 0.1, "A DOPAMINA É UM DELES", tam=124),
      FS(S3 + 0.1, S4 - S3 - 0.15, [{"k": "bh_vaso", "xy": [540, 1080], "s": 2.0, "t": 0.0}],
         fluxos=[{"de": [190, 1080], "para": [900, 1080], "curva": 0, "cor": "#ffd400", "t": 0.1, "d": 2.7, "n": 6, "r": 20, "viagem": 1.4}]),
      DS(b(8.0), S4 - b(8.0) - 0.05, [{"k": "seta", "de": [800, 800], "para": [640, 1010], "curva": -60}], cor="#1f6fb2", lw=13),
      NOTA(b(8.1), S4 - b(8.1) - 0.05, "dopamina", 560, 680, w=440, tam=110, cor="#b8860b", rot=-4)]
# (4) Só que o cérebro tem um muro em volta.
c += [FR(S4 + 0.05, S5 - S4 - 0.1, "O CÉREBRO TEM UM MURO", tam=124),
      FS(S4 + 0.1, S5 - S4 - 0.15, [{"k": "cerebro", "xy": [540, 1110], "s": 0.78, "t": 0.0},
                                    {"k": "bh_muro", "xy": [540, 1110], "s": 0.95, "t": b(11.9) - S4 - 0.1}],
         pulsos=[{"o": 1, "t": b(12.3) - S4 - 0.1}]),
      NOTA(b(12.2), S5 - b(12.2) - 0.05, "muro", 690, 1360, w=330, tam=120, cor="#8a4a1c", rot=-5)]
# (5) A dopamina do sangue não passa por ele.
c += [FR(S5 + 0.05, S6 - S5 - 0.1, "A DO SANGUE NÃO PASSA", tam=130),
      FS(S5 + 0.1, S6 - S5 - 0.15, [{"k": "cerebro", "xy": [540, 1110], "s": 0.78, "t": 0.0},
                                    {"k": "bh_muro", "xy": [540, 1110], "s": 0.95, "t": 0.0}],
         fluxos=[{"de": [540, 1560], "para": [540, 1335], "curva": 0, "cor": "#ffd400", "t": 0.3, "d": 2.8, "n": 7, "r": 16, "viagem": 0.8}]),
      DS(b(15.35), S6 - b(15.35) - 0.05, [{"k": "x", "c": [540, 1440], "s": 70}], cor="#e0322b", lw=18)]
# (6) A do prazer é feita lá dentro.
c += [FR(S6 + 0.05, AF - S6 - 0.1, "A DO PRAZER: LÁ DENTRO", tam=130),
      FS(S6 + 0.1, AF - S6 - 0.15, [{"k": "cerebro", "xy": [540, 1110], "s": 0.78, "t": 0.0},
                                    {"k": "bh_muro", "xy": [540, 1110], "s": 0.95, "t": 0.0}],
         fluxos=[{"de": [450, 1110], "para": [640, 1080], "curva": -50, "cor": "#ffd400", "t": 0.4, "d": 2.2, "n": 6, "r": 12, "viagem": 0.7}],
         pulsos=[{"o": 0, "t": 0.6}, {"o": 0, "t": 1.6}]),
      DS(b(18.9), AF - b(18.9) - 0.02, [{"k": "check", "c": [840, 860], "s": 60}], cor="#1f9e4f", lw=18)]

SFX_AULA = [{"src": "whoosh", "t": A1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": A1 + 0.15, "gain": 0.4},
            {"src": "boing", "t": b(1.7), "gain": 0.3}, {"src": "pagina", "t": S2, "gain": 0.4}, {"src": "pagina", "t": S3, "gain": 0.4},
            {"src": "boing", "t": b(8.1), "gain": 0.3}, {"src": "pagina", "t": S4, "gain": 0.4}, {"src": "boing", "t": b(12.0), "gain": 0.3},
            {"src": "pagina", "t": S5, "gain": 0.4}, {"src": "scratch", "t": b(15.35), "gain": 0.3}, {"src": "pagina", "t": S6, "gain": 0.4},
            {"src": "notif", "t": b(18.9), "gain": 0.35}]

# ---------------- ESTUDO + HONESTO + SEGURANÇA (C neutro) ----------------
C1, C2, C2b, C3, C4, C5, C5b, C6, C6b, C7, C7b, C8 = (k_(0.0), k_(2.85), k_(4.6), k_(7.95), k_(12.2), k_(16.55), k_(19.6),
                                                       k_(21.85), k_(24.3), k_(27.45), k_(30.6), k_(33.45))
CF = t_cta
c += B(P + "_viral_blur.mp4", tC, t_cta - tC, 5.0)
c += [{"tipo": "glitch", "t": tC - 0.05, "d": 0.25}, {"tipo": "flash", "t": tC, "d": 0.2, "max": 0.5},
      T(C1 + 0.02, C2 - C1 - 0.05, "DE ONDE VEIO ESSE NÚMERO?", y=420, f="150px Anton", css=SOMBRA),
      {"tipo": "flash", "t": C2, "d": 0.2, "max": 0.5},
      T(C2 + 0.02, C3 - C2 - 0.06, "ESTUDO DE 2000: POUCOS RAPAZES JOVENS", y=420, f="140px Anton", cor="#f2c230", vel=0.1, css=SOMBRA),
      {"tipo": "gigante", "t": C2b, "d": 2.6, "txt": "2000", "y": 1050, "tam": 320, "cor": "rgba(255,255,255,.18)", "x": [1000, -1500], "z": 20},
      {"tipo": "flash", "t": C3, "d": 0.2, "max": 0.5},
      {"tipo": "numero", "t": C3 + 0.02, "d": C4 - C3 - 0.04, "xy": [0, 420], "valor": 14, "suf": " °C", "rotulo": "1 hora na água", "tam": 300, "cor": "#4dd8ff", "z": 44},
      {"tipo": "flash", "t": C4, "d": 0.2, "max": 0.5},
      {"tipo": "numero", "t": C4 + 0.02, "d": C5 - C4 - 0.04, "xy": [0, 420], "valor": 250, "pre": "+", "suf": "%", "rotulo": "dopamina NO SANGUE", "tam": 300, "cor": "#3ddc84", "z": 44},
      {"tipo": "gigante", "t": C4 + 0.3, "d": 2.6, "txt": "SANGUE", "y": 1050, "tam": 280, "cor": "rgba(255,90,95,.35)", "x": [1000, -1900], "z": 20},
      F(C2, C5 - C2 - 0.02, "Šrámek et al., Eur J Appl Physiol 2000 · 1 h na água a 14 °C · no sangue: dopamina +250%, noradrenalina +530%"),
      {"tipo": "flash", "t": C5, "d": 0.2, "max": 0.5},
      T(C5 + 0.02, C5b - C5 - 0.04, "OS NÚMEROS DA COCAÍNA: EM RATO", y=420, f="136px Anton", css=SOMBRA),
      T(C5b, C6 - C5b - 0.04, "MEDIDOS DENTRO DO CÉREBRO", y=420, f="146px Anton", cor="#ff5a5f", css=SOMBRA),
      {"tipo": "gigante", "t": C5b + 0.2, "d": 1.9, "txt": "≠", "y": 1000, "tam": 420, "cor": "#c6ff3d", "x": [1000, -700], "z": 42},
      F(C5, C6 - C5 - 0.02, "Di Chiara & Imperato, PNAS 1988 · ratos, medida dentro do cérebro"),
      {"tipo": "flash", "t": C6, "d": 0.2, "max": 0.5},
      T(C6 + 0.02, C6b - C6 - 0.04, "ACORDA, SIM ✓", y=440, f="170px Anton", cor="#3ddc84", css=SOMBRA, fixo=True),
      T(C6b, C7 - C6b - 0.04, "É O CORPO REAGINDO AO SUSTO", y=420, f="146px Anton", css=SOMBRA),
      {"tipo": "flash", "t": C7, "d": 0.2, "max": 0.5},
      T(C7 + 0.02, C7b - C7 - 0.04, "CORAÇÃO OU PRESSÃO ALTA?", y=380, f="146px Anton", cor="#f2c230", css=SOMBRA),
      {"tipo": "fisio", "t": C7 + 0.1, "d": C8 - C7 - 0.15, "z": 30, "orgaos": [{"k": "coracao_afeto", "xy": [540, 1020], "s": 0.95, "t": 0.0}],
       "pulsos": [{"o": 0, "t": 0.7}, {"o": 0, "t": 1.5}, {"o": 0, "t": 2.3}, {"o": 0, "t": 3.1}, {"o": 0, "t": 3.9}]},
      T(C7b, C8 - C7b - 0.04, "FALE COM SEU MÉDICO ANTES", y=380, f="146px Anton", cor="#3ddc84", css=SOMBRA, fixo=True),
      {"tipo": "flash", "t": C8, "d": 0.2, "max": 0.5},
      T(C8 + 0.02, CF - C8 - 0.06, "ÁGUA GELADA DE RIO OU MAR?", y=380, f="140px Anton", css=SOMBRA),
      {"tipo": "carimbo", "t": k_(34.0), "d": CF - k_(34.0) - 0.06, "xy": [90, 860], "txt": "NUNCA SOZINHO", "tam": 130, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)"}]

# ---------------- CTA (banco cta6) ----------------
c += [{"tipo": "glitch", "t": t_cta - 0.05, "d": 0.25},
      {"tipo": "video", "t": t_cta, "d": d_cta, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[t_cta, 1.0, 0.01], [t_cta + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": t_cta + 0.2, "d": d_cta - 0.25, "y": 215, "txt": "SEGUE + CURTE = TREINO DO DEDÃO", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ---------------- FECHO (visual, trilha por baixo) ----------------
c += B(P + "_viral_blur.mp4", F0, dur - F0, 30.0)
c += [{"tipo": "glitch", "t": F0 - 0.05, "d": 0.25}, {"tipo": "flash", "t": F0, "d": 0.2, "max": 0.5},
      T(F0 + 0.05, 1.5, "ACORDA, SIM", y=420, f="170px Anton", cor="#3ddc84", css=SOMBRA, fixo=True),
      {"tipo": "carimbo", "t": F0 + 1.5, "d": dur - F0 - 1.5, "xy": [70, 860], "txt": "SUSTO, NÃO DROGA", "tam": 120, "rot": -7, "z": 60},
      T(F0 + 1.55, dur - F0 - 1.55, "MAS NÃO É DROGA", y=420, f="150px Anton", cor="#f2c230", css=SOMBRA),
      F(F0, dur - F0, "Šrámek et al., Eur J Appl Physiol 2000 · doi 10.1007/s004210050065")]

voz = [{"src": M + "bh_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "bh_viral.words.json", "gain": 0.16},
       {"src": M + "bh_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "bh_rosto.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "bh_rosto.words.json"},
       {"src": M + "bh_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "bh_a_voz.words.json"},
       {"src": M + "bh_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "bh_b_voz.words.json"},
       {"src": M + "bh_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "bh_c_voz.words.json"},
       {"src": M + "cta6.mp4", "t": t_cta, "ms": 0, "d": d_cta, "palavras": M + "cta6.mp4.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": vd + 2.05, "gain": 0.35},
       {"src": "glitch", "t": tA - 0.05, "gain": 0.5}, {"src": "whoosh", "t": tA, "gain": 0.5, "pico": 0.45},
       {"src": "whoosh2", "t": a(0.9), "gain": 0.35}, {"src": "whoosh2", "t": a(4.0), "gain": 0.4}, {"src": "whoosh", "t": a(5.1), "gain": 0.4, "pico": 0.45},
       {"src": "glitch", "t": A1 - 0.05, "gain": 0.5}, *SFX_AULA,
       {"src": "glitch", "t": tC - 0.05, "gain": 0.5}, {"src": "whoosh2", "t": C2, "gain": 0.4}, {"src": "papel", "t": C2b, "gain": 0.4},
       {"src": "whoosh2", "t": C3, "gain": 0.4}, {"src": "boom", "t": C4, "gain": 0.55, "pico": 0.3, "d": 1.5},
       {"src": "pagina", "t": C5, "gain": 0.4}, {"src": "whoosh", "t": C5b + 0.2, "gain": 0.4, "pico": 0.45},
       {"src": "boing", "t": C6, "gain": 0.35}, {"src": "whoosh2", "t": C6b, "gain": 0.35}, {"src": "whoosh2", "t": C7, "gain": 0.4},
       {"src": "notif", "t": C7b, "gain": 0.35}, {"src": "whoosh2", "t": C8, "gain": 0.4}, {"src": "boom", "t": k_(34.0), "gain": 0.55, "pico": 0.3, "d": 1.5},
       {"src": "glitch", "t": t_cta - 0.05, "gain": 0.5}, {"src": "notif", "t": t_cta + 0.2, "gain": 0.4},
       {"src": "glitch", "t": F0 - 0.05, "gain": 0.5}, {"src": "boom", "t": F0 + 1.5, "gain": 0.6, "pico": 0.3, "d": 1.5}]
salvar("react_l2_banho", dur, 131, c, voz, sfx, {"r1_fim": r1, "esconde": [[0, 4.0]], "ys": [[4.0, vd, 1440], [vd, r1, 1000], [A1, AF, 1730]]})
import json
p = json.load(open('planos/react_l2_banho.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": vd, "d": round(t_cta - vd + 0.3, 2), "gain": 0.15, "fade": 0.8},
                        {"src": "m_investiga", "t": round(F0 - 0.2, 2), "d": round(dur - F0 + 0.2, 2), "gain": 0.3, "fade": 0.8}]
json.dump(p, open('planos/react_l2_banho.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "A", tA, "aula", A1, AF, round(AF - A1, 2), "C", tC, "cta", t_cta, "fecho", F0)
