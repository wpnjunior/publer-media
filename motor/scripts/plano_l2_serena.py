# plano_l2_serena.py (14/11, lote 2, Caneta com Músculo): Serena Williams no TODAY (via @etalkctv), dublada pela Murilo.
# Trecho: "É um jeito preguiçoso? É um atalho?" + "nunca consegui ficar num peso saudável... muita mulher passa por isso" -> VERDADE
# (o corpo defende o peso). Aula na EDIÇÃO CAIXINHA (cartão creme, aba lima, desenhos que se desenham, Caveat; sem b-roll).
# Voz em blocos por clima (sem atempo): A indignado (r1 + abertura), B manso (aula), C neutro (estudo), D alegre (fecho).
# Depois deste script:
#   python3 scripts/entrada.py react_l2_serena assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 '“É PREGUIÇA? É ATALHO?”' 'Serena Williams no TODAY'
#   python3 scripts/pele.py react_l2_serena noticia
import sys; sys.path.insert(0, 'scripts')
from mk import *
P = 'sw'
vd = 13.03                      # viral cortado (18,00-20,37 + 27,32-37,95)
r1 = round(vd + 3.84, 2)        # rosto "Preguiça? Não. É biologia, tá?" (sw_rosto.mp4, 3,84 s)
n = lambda v: round(r1 + v - 4.0, 3)    # tempo em sw_voz.wav -> plano (sw_voz toca a partir de 4,0 s)
VEND = 53.365                   # fim de sw_voz.wav
t_cta = round(n(VEND) + 0.35, 2); d_cta = 4.12
F0 = round(t_cta + d_cta + 0.05, 2)
f = lambda v: round(F0 + v, 3)  # tempo em sw_fecho_voz.wav -> plano
dur = round(f(13.74) + 0.6, 2)
SOMBRA = "text-shadow:8px 8px 0 #000"

c = abertura(P, vd, "via @etalkctv (TODAY)", "center 26%", "Mito ou verdade? 👇", "Peso que não desce é preguiça?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 446.5, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta": L["escolha"] = 0
c += [{"tipo": "glitch", "t": 2.33, "d": 0.18}]          # emenda dos dois pedaços do viral
# R1: resposta grande + rosto embaixo
c += [{"tipo": "carimbo", "t": vd + 0.1, "d": r1 - vd - 0.15, "xy": [80, 470], "txt": "NÃO É PREGUIÇA", "tam": 120, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)"},
      rosto_r1(P, vd, r1 - vd, 0)]

# ---------------- ABERTURA DA NARRAÇÃO (A indignado, 4,26-11,08) ----------------
A1 = n(11.936)          # começo do bloco B (aula)
c += B(P + "_viral_blur.mp4", r1, A1 - r1, 40.0)
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": r1, "d": 0.2, "max": 0.5},
      T(n(4.26), n(8.7) - n(4.26), "PREGUIÇA? ATALHO?", y=470, f="150px Anton", css=SOMBRA),
      {"tipo": "gigante", "t": n(7.0), "d": 1.6, "txt": "ATALHO?", "y": 980, "tam": 280, "cor": "rgba(255,255,255,.16)", "x": [1000, -1700], "z": 20},
      {"tipo": "flash", "t": n(8.72), "d": 0.2, "max": 0.5},
      T(n(8.75), A1 - n(8.75) - 0.05, "NÃO É SÓ FORÇA DE VONTADE", y=440, f="140px Anton", cor="#f2c230", vel=0.1, css=SOMBRA),
      {"tipo": "gigante", "t": n(9.6), "d": 2.0, "txt": "BIOLOGIA", "y": 1150, "tam": 260, "cor": "#c6ff3d", "x": [1000, -2100], "z": 42}]

# ---------------- AULA RÁPIDA: EDIÇÃO CAIXINHA (sem b-roll) ----------------
TINTA = "#1c1a17"
ENT = 1.88   # entrada.py empurra "t" das camadas mas não os tempos internos de "abas"
S1, S2, S3, S4, S5, S6, S7 = n(11.94), n(15.3), n(19.7), n(22.15), n(27.05), n(30.4), n(33.6)
AF = n(35.55)
def FR(t, d, txt, tam=112, y=385, cor=TINTA):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [95, y], "w": 890, "fonte": f"{tam}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 45, "anim": "palavras", "vel": 0.09, "fixo": True}
def NOTA(t, d, txt, x, y, w=420, tam=96, cor="#c0392b", rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg)", "fixo": True}
def FS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": 42, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def DS(t, d, formas, cor="#e0322b", lw=11):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": 44, "fixo": True}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}

c += [{"tipo": "glitch", "t": A1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": A1, "d": 0.2, "max": 0.5},
      {"tipo": "fundo", "t": A1, "d": AF - A1, "cor": "#0e1012", "textura": "gradiente", "cor2": "#22302a", "z": 11, "fixo": True},
      {"tipo": "cartao", "t": A1, "d": AF - A1, "box": [60, 330, 960, 1250], "aba": "1 · termostato", "z": 30, "fixo": True,
       "abas": [[round(a + ENT, 3), x] for a, x in [[S2, "2 · volta"], [S3, "3 · no peso"], [S4, "4 · gordura"], [S5, "5 · estômago"], [S6, "6 · a caneta"], [S7, "7 · cérebro"]]]},
      SELO(A1 + 0.2, AF - A1 - 0.2, "● AULA RÁPIDA · FOME")]

# (1) Pensa no termostato do ar-condicionado.
c += [FR(S1 + 0.15, S2 - S1 - 0.2, "O CORPO TEM UM TERMOSTATO", tam=120),
      FS(S1 + 0.3, S2 - S1 - 0.35, [{"k": "termometro", "xy": [540, 1080], "s": 1.25, "t": 0.0}], pulsos=[{"o": 0, "t": 1.4}]),
      NOTA(S1 + 0.9, S2 - S1 - 0.95, "24°", 640, 900, w=300, tam=150, cor="#1f6fb2", rot=-6)]
# (2) Abriu a janela, ele liga mais forte pra voltar pro número de antes.
c += [FR(S2 + 0.05, S3 - S2 - 0.1, "ELE VOLTA PRO NÚMERO DE ANTES", tam=112),
      FS(S2 + 0.1, S3 - S2 - 0.15, [{"k": "termometro", "xy": [330, 1090], "s": 1.15, "t": 0.0}], pulsos=[{"o": 0, "t": 1.6}, {"o": 0, "t": 2.6}]),
      NOTA(S2 + 0.3, S3 - S2 - 0.35, "janela aberta: 28°", 520, 830, w=480, tam=84, cor="#c0392b", rot=-4),
      DS(n(16.9), S3 - n(16.9) - 0.05, [{"k": "seta", "de": [760, 980], "para": [760, 1330], "curva": -120}], cor="#1f6fb2", lw=14),
      NOTA(n(17.9), S3 - n(17.9) - 0.05, "volta: 24°", 560, 1380, w=440, tam=96, cor="#1f9e4f", rot=-3)]
# (3) No peso é igual.
c += [FR(S3 + 0.05, S4 - S3 - 0.1, "NO PESO É IGUAL", tam=170, y=700),
      DS(S3 + 0.4, S4 - S3 - 0.45, [{"k": "sublinhado", "de": [200, 1020], "ate": 880}], cor="#e0322b", lw=14)]
# (4) Você emagrece, e a gordura manda menos o aviso de tô cheio.
c += [FR(S4 + 0.05, S5 - S4 - 0.1, "MENOS AVISO DE “TÔ CHEIO”", tam=112),
      FS(S4 + 0.1, S5 - S4 - 0.15, [{"k": "gordura", "xy": [300, 1300], "s": 0.85, "t": 0.0, "rotulo": "GORDURA", "rot_y": 175},
                                    {"k": "cerebro", "xy": [760, 870], "s": 0.8, "t": 0.3, "rotulo": "CÉREBRO", "rot_y": 190}],
         encolhe=[{"o": 0, "t": n(22.6) - S4 - 0.1, "para": 0.72, "d": 1.2}],
         fluxos=[{"de": [360, 1170], "para": [680, 960], "curva": -60, "cor": "#9aa3ad", "t": n(24.0) - S4 - 0.1, "d": 2.6, "n": 2, "r": 12, "viagem": 1.4}]),
      NOTA(n(24.4), S5 - n(24.4) - 0.05, "fraquinho...", 560, 1260, w=440, tam=96, cor="#5b6670", rot=-4)]
# (5) O estômago manda mais o aviso de fome.
c += [FR(S5 + 0.05, S6 - S5 - 0.1, "MAIS AVISO DE FOME", tam=130),
      FS(S5 + 0.1, S6 - S5 - 0.15, [{"k": "estomago_serena", "xy": [300, 1260], "s": 0.95, "t": 0.0, "rotulo": "ESTÔMAGO", "rot_y": 215},
                                    {"k": "cerebro", "xy": [770, 860], "s": 0.8, "t": 0.2}],
         fluxos=[{"de": [380, 1130], "para": [690, 950], "curva": -60, "cor": "#ff3b30", "t": 0.7, "d": 2.4, "n": 9, "r": 16, "viagem": 0.8}],
         pulsos=[{"o": 1, "t": 1.6}, {"o": 1, "t": 2.4}]),
      NOTA(n(28.8), S6 - n(28.8) - 0.05, "FOME!", 590, 1230, w=380, tam=130, cor="#c0392b", rot=-7)]
# (6) A caneta imita um aviso do intestino
c += [FR(S6 + 0.05, S7 - S6 - 0.1, "CANETA IMITA AVISO DO INTESTINO", tam=108),
      FS(S6 + 0.1, S7 - S6 - 0.15, [{"k": "intestino", "xy": [330, 1150], "s": 0.95, "t": 0.0, "rotulo": "INTESTINO", "rot_y": 200},
                                    {"k": "caneta", "xy": [770, 1120], "s": 0.85, "t": n(30.7) - S6 - 0.1}]),
      DS(n(31.5), S7 - n(31.5) - 0.05, [{"k": "seta", "de": [690, 980], "para": [480, 1010], "curva": -60}], cor="#1f9e4f", lw=13),
      NOTA(n(31.6), S7 - n(31.6) - 0.05, "imita", 560, 860, w=300, tam=96, cor="#1f9e4f", rot=-5)]
# (7) que diz pro cérebro: chegou comida.
c += [FR(S7 + 0.05, AF - S7 - 0.1, "“CHEGOU COMIDA”", tam=150),
      FS(S7 + 0.1, AF - S7 - 0.15, [{"k": "cerebro", "xy": [540, 1080], "s": 1.05, "t": 0.0}],
         fluxos=[{"de": [540, 1500], "para": [540, 1220], "curva": 0, "cor": "#3ddc84", "t": 0.1, "d": 1.2, "n": 5, "r": 14, "viagem": 0.6}],
         pulsos=[{"o": 0, "t": 0.6}]),
      DS(n(34.5), AF - n(34.5) - 0.02, [{"k": "check", "c": [820, 860], "s": 70}], cor="#1f9e4f", lw=18)]

SFX_AULA = [{"src": "whoosh", "t": A1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": A1 + 0.15, "gain": 0.4},
            {"src": "boing", "t": S1 + 0.9, "gain": 0.3}, {"src": "pagina", "t": S2, "gain": 0.4}, {"src": "boing", "t": n(17.9), "gain": 0.3},
            {"src": "pagina", "t": S3, "gain": 0.4}, {"src": "pagina", "t": S4, "gain": 0.4}, {"src": "pagina", "t": S5, "gain": 0.4},
            {"src": "boing", "t": n(28.8), "gain": 0.35}, {"src": "pagina", "t": S6, "gain": 0.4}, {"src": "pagina", "t": S7, "gain": 0.4},
            {"src": "notif", "t": n(34.5), "gain": 0.35}]

# ---------------- ESTUDO (C neutro) ----------------
E1, E2, E3, E4, E5 = n(35.6), n(38.9), n(41.05), n(46.35), n(49.1)
c += B(P + "_viral_blur.mp4", AF, t_cta - AF, 5.0)
c += [{"tipo": "glitch", "t": AF - 0.05, "d": 0.25},
      {"tipo": "numero", "t": E1, "d": E2 - E1, "xy": [0, 420], "valor": 50, "rotulo": "pessoas no estudo", "tam": 300, "z": 44},
      {"tipo": "flash", "t": E2, "d": 0.2, "max": 0.5},
      {"tipo": "numero", "t": E2 + 0.02, "d": E3 - E2 - 0.02, "xy": [0, 420], "valor": 13.5, "dec": 1, "pre": "-", "suf": " kg", "rotulo": "em média", "tam": 260, "cor": "#3ddc84", "z": 44},
      {"tipo": "flash", "t": E3, "d": 0.2, "max": 0.5},
      T(E3 + 0.02, n(42.9) - E3 - 0.02, "1 ANO DEPOIS", y=440, f="170px Anton", css=SOMBRA),
      T(n(42.9), E4 - n(42.9) - 0.02, "HORMÔNIOS DA FOME AINDA FORA DO NORMAL", y=420, f="124px Anton", cor="#f2c230", vel=0.1, css=SOMBRA),
      {"tipo": "flash", "t": E4, "d": 0.2, "max": 0.5},
      T(E4 + 0.02, E5 - E4 - 0.04, "A FOME CONTINUAVA MAIOR", y=440, f="150px Anton", cor="#ff5a5f", css=SOMBRA),
      {"tipo": "gigante", "t": E4 + 0.6, "d": 1.8, "txt": "FOME", "y": 1050, "tam": 320, "cor": "#c6ff3d", "x": [1000, -1300], "z": 42},
      {"tipo": "flash", "t": E5, "d": 0.2, "max": 0.5},
      T(E5 + 0.02, t_cta - E5 - 0.04, "UMA DAS MAIORES REVISTAS DE MEDICINA · 2011", y=420, f="120px Anton", vel=0.1, css=SOMBRA),
      F(E1, t_cta - E1 - 0.02, "Sumithran et al., N Engl J Med 2011 · 50 pessoas, acompanhadas por 1 ano")]

# ---------------- CTA (banco cta6) ----------------
c += [{"tipo": "glitch", "t": t_cta - 0.05, "d": 0.25},
      {"tipo": "video", "t": t_cta, "d": d_cta, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[t_cta, 1.0, 0.01], [t_cta + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": t_cta + 0.2, "d": d_cta - 0.25, "y": 215, "txt": "SEGUE + CURTE = TREINO DO DEDÃO", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ---------------- FECHO (D alegre) ----------------
c += B(P + "_viral_blur.mp4", F0, dur - F0, 24.0)
c += [{"tipo": "glitch", "t": F0 - 0.05, "d": 0.25}, {"tipo": "flash", "t": F0, "d": 0.2, "max": 0.5},
      T(f(0.1), f(3.5) - f(0.1), "NÃO É FALTA DE CARÁTER", y=420, f="150px Anton", css=SOMBRA),
      T(f(3.55), f(6.25) - f(3.55), "TAMBÉM NÃO É MÁGICA", y=420, f="150px Anton", cor="#f2c230", css=SOMBRA),
      {"tipo": "gigante", "t": f(4.3), "d": 1.7, "txt": "MÁGICA?", "y": 1000, "tam": 280, "cor": "rgba(255,255,255,.16)", "x": [1000, -1900], "z": 20},
      T(f(6.3), f(10.3) - f(6.3), "TRATAMENTO: DECISÃO SUA COM SEU MÉDICO", y=420, f="124px Anton", cor="#3ddc84", vel=0.1, css=SOMBRA),
      {"tipo": "checklist", "t": f(10.3), "d": dur - f(10.3), "box": [120, 260, 840, 560], "titulo": "Trabalho seu:", "entra": "cai",
       "itens": [{"txt": "proteína", "t": f(10.5), "marca": f(11.0)}, {"txt": "treino", "t": f(11.7), "marca": f(12.1)}], "z": 40},
      {"tipo": "carimbo", "t": f(12.6), "d": dur - f(12.6), "xy": [70, 880], "txt": "NEM PREGUIÇA, NEM MÁGICA", "tam": 96, "rot": -7, "z": 60},
      F(F0, dur - F0, "Sumithran et al., N Engl J Med 2011 · doi 10.1056/NEJMoa1105816")]

voz = [{"src": M + "sw_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "sw_viral.words.json", "gain": 0.16},
       {"src": M + "sw_dub_voz.wav", "t": 0, "ms": 0.2, "d": 11.5, "gain": 1.0},
       {"src": M + "sw_rosto.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "sw_rosto.words.json"},
       {"src": M + "sw_voz.wav", "t": r1, "ms": 4.0, "d": round(VEND - 4.0, 3), "palavras": M + "sw_voz.words.json"},
       {"src": M + "cta6.mp4", "t": t_cta, "ms": 0, "d": d_cta, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "sw_fecho_voz.wav", "t": F0, "ms": 0, "d": 13.74, "palavras": M + "sw_fecho_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35}, {"src": "glitch", "t": 2.33, "gain": 0.3},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1, "gain": 0.5, "pico": 0.45},
       {"src": "whoosh2", "t": n(7.0), "gain": 0.35}, {"src": "whoosh2", "t": n(8.75), "gain": 0.4}, {"src": "whoosh", "t": n(9.6), "gain": 0.4, "pico": 0.45},
       {"src": "glitch", "t": A1 - 0.05, "gain": 0.5}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.5}, {"src": "boom", "t": E1, "gain": 0.6, "pico": 0.3, "d": 1.5},
       {"src": "whoosh2", "t": E2, "gain": 0.4}, {"src": "whoosh2", "t": E3, "gain": 0.4}, {"src": "papel", "t": n(42.9), "gain": 0.4},
       {"src": "whoosh", "t": E4, "gain": 0.45, "pico": 0.45}, {"src": "pagina", "t": E5, "gain": 0.4},
       {"src": "glitch", "t": t_cta - 0.05, "gain": 0.5}, {"src": "notif", "t": t_cta + 0.2, "gain": 0.4},
       {"src": "glitch", "t": F0 - 0.05, "gain": 0.5}, {"src": "whoosh2", "t": f(3.55), "gain": 0.4}, {"src": "whoosh2", "t": f(6.3), "gain": 0.4},
       {"src": "papel", "t": f(10.3), "gain": 0.5}, {"src": "boom", "t": f(12.6), "gain": 0.6, "pico": 0.3, "d": 1.5}]
for L in c:
    if vd <= L.get("t", 0) < r1 - 0.06 and L.get("tipo") == "carimbo": L["fixo"] = True
salvar("react_l2_serena", dur, 117, c, voz, sfx, {"r1_fim": r1, "esconde": [[0, 4.0]], "ys": [[4.0, vd, 1440], [vd, r1, 1000], [A1, AF, 1730]]})
import json
p = json.load(open('planos/react_l2_serena.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": r1, "d": round(t_cta - r1, 2), "gain": 0.14, "fade": 0.8},
                        {"src": "m_investiga", "t": F0, "d": round(dur - F0, 2), "gain": 0.12, "fade": 0.8}]
json.dump(p, open('planos/react_l2_serena.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "aula", A1, AF, round(AF - A1, 2), "cta", t_cta, "fecho", F0)
