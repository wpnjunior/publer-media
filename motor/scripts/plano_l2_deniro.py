# plano_l2_deniro.py (14/11, lote 2, Fertilidade a Dois): Robert De Niro no TODAY (@todayshow), dublado pela Murilo.
# Trecho (3 pedaços, 14,87 s): "Você tem um bebê novo. Como é ser pai nessa idade?" + "É ótimo." + "Quando a gente é mais velho,
# tem consciência de certas coisas da vida." -> VERDADE com um porém (o relógio do homem também anda).
# Edição: CELULAR + MANCHETE na abertura da narração; aula na CAIXINHA (cartão creme, desenhos fisio_extra dn_*, sem b-roll);
# estudo com número grande em 3D ("~2 ERROS NOVOS POR ANO"). Voz em blocos: A alegre (r1 + abertura), B manso (aula),
# C neutro (estudo), D alegre (fecho). Pausas longas aparadas (tmp_dn/encurta.py), sem atempo.
# Depois deste script:
#   python3 scripts/entrada.py react_l2_deniro assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 'PAI AOS 79 ANOS?' 'Robert De Niro no TODAY Show'
#   python3 scripts/pele.py react_l2_deniro dossie
import sys; sys.path.insert(0, 'scripts')
from mk import *
P = 'dn'
vd = 14.87                      # viral cortado (6,36-11,95 + 21,46-24,97 + 31,72-37,47)
r1 = round(vd + 3.24, 2)        # rosto "Dá, sim. Mas tem um porém, tá?" (dn_rosto.mp4, 3,24 s)
n = lambda v: round(r1 + v, 3)  # tempo em dn_voz.wav -> plano
VEND = 71.56                    # fim de dn_voz.wav
t_cta = round(n(VEND) + 0.35, 2); d_cta = 4.12
F0 = round(t_cta + d_cta + 0.05, 2)
f = lambda v: round(F0 + v, 3)  # tempo em dn_fecho_voz.wav -> plano
FEND = 12.37
dur = round(f(FEND) + 0.6, 2)
SOMBRA = "text-shadow:8px 8px 0 #000"

c = abertura(P, vd, "via @todayshow", "center 20%", "Mito ou verdade? 👇", "Homem é pai em qualquer idade?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 2.5, "dec": 1, "suf": " MI DE VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta": L["escolha"] = 1
c += [{"tipo": "glitch", "t": 5.59, "d": 0.18}, {"tipo": "glitch", "t": 9.10, "d": 0.18}]   # emendas dos pedaços
# R1: resposta grande + rosto embaixo
c += [{"tipo": "carimbo", "t": vd + 0.1, "d": r1 - vd - 0.15, "xy": [150, 470], "txt": "DÁ. MAS...", "tam": 150, "rot": -7, "z": 60,
       "cor": "#1f9e4f", "blend": "normal", "css": "background:rgba(255,255,255,.9)", "fixo": True},
      rosto_r1(P, vd, r1 - vd, 0)]

# ---------------- ABERTURA DA NARRAÇÃO (A alegre): CELULAR + MANCHETE ----------------
A1 = n(11.25)           # começo do bloco B (aula)
c += B(P + "_viral_blur.mp4", r1, A1 - r1, 40.0)
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": r1, "d": 0.2, "max": 0.5},
      {"tipo": "celular", "t": n(0.2), "d": n(7.85) - n(0.2), "xy": [250, 520], "wh": [580, 1060], "img": M + "dn_cel.jpg", "z": 30,
       "notif": [{"t": n(1.2), "app": "TODAY", "txt": "Ser pai agora? “É ótimo.”"},
                 {"t": n(5.0), "app": "Ciência", "txt": "E a idade do pai, pesa?"}]},
      T(n(0.3), n(3.8) - n(0.3), "ELE TEM RAZÃO ✓", y=250, f="150px Anton", cor="#3ddc84", css=SOMBRA),
      T(n(3.85), n(7.85) - n(3.85), "O ASSUNTO, NÃO A FAMÍLIA DELE", y=230, f="112px Anton", vel=0.1, css=SOMBRA),
      {"tipo": "flash", "t": n(7.9), "d": 0.2, "max": 0.5},
      {"tipo": "manchete", "t": n(7.92), "d": A1 - n(7.92) - 0.05, "xy": [50, 520], "w": 980, "jornal": "Ciência do dia a dia",
       "data": "14/11", "txt": "O relógio do homem também anda", "sub": "Fazer filho tarde dá. Mas a idade dele conta.", "z": 40},
      {"tipo": "gigante", "t": n(8.4), "d": 2.3, "txt": "TIC-TAC", "y": 1180, "tam": 280, "cor": "rgba(255,255,255,.16)", "x": [1000, -1900], "z": 20}]

# ---------------- AULA RÁPIDA: EDIÇÃO CAIXINHA (sem b-roll) ----------------
TINTA = "#1c1a17"
ENT = 1.88   # entrada.py empurra "t" das camadas mas não os tempos internos de "abas"
S1, S2, S2b, S3, S4, S5, S6, S7 = n(11.25), n(16.45), n(19.15), n(23.25), n(26.55), n(31.65), n(34.7), n(37.6)
AF = n(42.0)
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
      {"tipo": "cartao", "t": A1, "d": AF - A1, "box": [60, 330, 960, 1250], "aba": "1 · ela", "z": 30, "fixo": True,
       "abas": [[round(a + ENT, 3), x] for a, x in [[S2, "2 · ele"], [S2b, "3 · a fábrica"], [S3, "4 · divide"], [S4, "5 · copia"],
                                                     [S5, "6 · xerox"], [S6, "7 · os anos"], [S7, "8 · o errinho"]]]},
      SELO(A1 + 0.2, AF - A1 - 0.2, "● AULA RÁPIDA · IDADE DO PAI")]

# (1) A mulher já nasce com os óvulos prontos, guardados.
c += [FR(S1 + 0.15, S2 - S1 - 0.2, "ELA: ESTOQUE PRONTO", tam=130),
      FS(S1 + 0.3, S2 - S1 - 0.35, [{"k": "ovario_cheio", "xy": [540, 1090], "s": 1.5, "t": 0.0}], pulsos=[{"o": 0, "t": 2.4}]),
      NOTA(n(13.7), S2 - n(13.7) - 0.05, "já nasce com eles", 300, 1360, w=480, tam=92, cor="#c0392b", rot=-4)]
# (2) O homem, não.
c += [FR(S2 + 0.05, S2b - S2 - 0.1, "O HOMEM, NÃO.", tam=190, y=720),
      DS(S2 + 0.5, S2b - S2 - 0.55, [{"k": "sublinhado", "de": [200, 1000], "ate": 880}], cor="#e0322b", lw=14)]
# (3) Ele tem uma fábrica que faz espermatozoide a vida inteira.
c += [FR(S2b + 0.05, S3 - S2b - 0.1, "ELE: FÁBRICA A VIDA TODA", tam=118),
      FS(S2b + 0.1, S3 - S2b - 0.15, [{"k": "dn_fabrica", "xy": [470, 1060], "s": 1.6, "t": 0.0}],
         fluxos=[{"de": [800, 1200], "para": [980, 820], "curva": -60, "cor": "#1f6fb2", "t": 1.0, "d": 2.9, "n": 9, "r": 12, "viagem": 1.0}]),
      NOTA(n(21.3), S3 - n(21.3) - 0.05, "não fecha nunca", 360, 1380, w=460, tam=92, cor="#1f6fb2", rot=-3)]
# (4) Lá dentro, as células se dividem sem parar.
c += [FR(S3 + 0.05, S4 - S3 - 0.1, "AS CÉLULAS SE DIVIDEM", tam=118),
      FS(S3 + 0.1, S4 - S3 - 0.15, [{"k": "celula", "xy": [540, 900], "s": 0.75, "t": 0.0},
                                    {"k": "celula", "xy": [310, 1260], "s": 0.62, "t": 1.4},
                                    {"k": "celula", "xy": [770, 1260], "s": 0.62, "t": 1.6}],
         pulsos=[{"o": 0, "t": 1.0}, {"o": 1, "t": 2.4}, {"o": 2, "t": 2.6}]),
      DS(S3 + 1.1, S4 - S3 - 1.15, [{"k": "seta", "de": [460, 1000], "para": [350, 1150], "curva": 20},
                                    {"k": "seta", "de": [620, 1000], "para": [730, 1150], "curva": -20}], cor="#1f6fb2", lw=12)]
# (5) E cada divisão copia o DNA, que é a receita do bebê.
c += [FR(S4 + 0.05, S5 - S4 - 0.1, "CADA DIVISÃO COPIA O DNA", tam=112),
      FS(S4 + 0.1, S5 - S4 - 0.15, [{"k": "pv_dna", "xy": [540, 1020], "s": 1.6, "t": 0.0}], pulsos=[{"o": 0, "t": 1.8}]),
      NOTA(n(28.9), S5 - n(28.9) - 0.05, "= a receita do bebê", 210, 1300, w=660, tam=100, cor="#c0392b", rot=-3)]
# (6) É como xerox da xerox.
c += [FR(S5 + 0.05, S6 - S5 - 0.1, "XEROX DA XEROX", tam=160),
      FS(S5 + 0.1, S6 - S5 - 0.15, [{"k": "dn_xerox", "xy": [540, 1120], "s": 1.45, "t": 0.0}], pulsos=[{"o": 0, "t": 1.6}]),
      NOTA(n(32.2), S6 - n(32.2) - 0.05, "cada cópia, mais borrada", 160, 1430, w=760, tam=88, cor="#5b6670", rot=-2)]
# (7) Cada ano, mais cópias.
c += [FR(S6 + 0.05, S7 - S6 - 0.1, "CADA ANO, MAIS CÓPIAS", tam=124),
      NOTA(S6 + 0.2, S7 - S6 - 0.25, "20", 90, 950, w=200, tam=140, cor="#1f6fb2", rot=-5),
      NOTA(S6 + 0.5, S7 - S6 - 0.55, "40", 310, 950, w=200, tam=140, cor="#1f6fb2", rot=3),
      NOTA(S6 + 0.8, S7 - S6 - 0.85, "60", 530, 950, w=200, tam=140, cor="#c0392b", rot=-4),
      NOTA(S6 + 1.1, S7 - S6 - 1.15, "80", 750, 950, w=200, tam=150, cor="#c0392b", rot=4),
      DS(S6 + 0.4, S7 - S6 - 0.45, [{"k": "seta", "de": [140, 1200], "para": [940, 1200], "curva": 0}], cor=TINTA, lw=12),
      NOTA(S6 + 1.0, S7 - S6 - 1.05, "anos do pai", 300, 1260, w=480, tam=92, cor=TINTA, rot=-2)]
# (8) E quanto mais cópia, mais chance de um errinho de digitação.
c += [FR(S7 + 0.05, AF - S7 - 0.1, "MAIS CHANCE DE UM ERRINHO", tam=112),
      FS(S7 + 0.1, AF - S7 - 0.15, [{"k": "dn_letras", "xy": [540, 1090], "s": 1.4, "t": 0.0}]),
      DS(n(39.7), AF - n(39.7) - 0.05, [{"k": "circulo", "c": [597, 1094], "r": [70, 80]}], cor="#e0322b", lw=12),
      NOTA(n(39.8), AF - n(39.8) - 0.05, "errinho de digitação", 190, 1380, w=700, tam=96, cor="#c0392b", rot=-3)]

SFX_AULA = [{"src": "whoosh", "t": A1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": A1 + 0.15, "gain": 0.4},
            {"src": "boing", "t": n(13.7), "gain": 0.3}, {"src": "pagina", "t": S2, "gain": 0.4}, {"src": "pagina", "t": S2b, "gain": 0.4},
            {"src": "boing", "t": n(21.3), "gain": 0.3}, {"src": "pagina", "t": S3, "gain": 0.4}, {"src": "boing", "t": S3 + 1.4, "gain": 0.3},
            {"src": "pagina", "t": S4, "gain": 0.4}, {"src": "boing", "t": n(28.9), "gain": 0.3}, {"src": "pagina", "t": S5, "gain": 0.4},
            {"src": "pagina", "t": S6, "gain": 0.4}, {"src": "boing", "t": S6 + 1.1, "gain": 0.3}, {"src": "pagina", "t": S7, "gain": 0.4},
            {"src": "scratch", "t": n(39.7), "gain": 0.3}]

# ---------------- ESTUDO (C neutro) ----------------
E1, E2, E3, E4, E5, E6, E7 = n(42.1), n(46.05), n(50.7), n(53.5), n(57.6), n(65.1), n(67.95)
c += B(P + "_viral_blur.mp4", AF, t_cta - AF, 5.0)
c += [{"tipo": "glitch", "t": AF - 0.05, "d": 0.25},
      {"tipo": "numero", "t": E1, "d": E2 - E1, "xy": [0, 420], "valor": 78, "tam": 320, "z": 44},
      T(E1 + 0.6, E2 - E1 - 0.65, "FAMÍLIAS COM O DNA LIDO", y=900, f="112px Anton", vel=0.1, css=SOMBRA),
      {"tipo": "flash", "t": E2, "d": 0.2, "max": 0.5},
      {"tipo": "numero", "t": E2 + 0.02, "d": E3 - E2 - 0.02, "xy": [0, 380], "valor": 2, "pre": "~", "tam": 380, "cor": "#ff5a5f", "z": 44, "sombra": "#5c0f14"},
      T(E2 + 0.5, E3 - E2 - 0.55, "ERROS NOVOS POR ANO", y=900, f="112px Anton", css=SOMBRA),
      T(n(47.6), E3 - n(47.6) - 0.05, "por ano do pai", y=1180, f="700 80px Caveat", anim=None, entra="pop", css=SOMBRA),
      {"tipo": "flash", "t": E3, "d": 0.2, "max": 0.5},
      T(E3 + 0.02, E4 - E3 - 0.04, "A MAIORIA NÃO FAZ NADA", y=470, f="140px Anton", cor="#3ddc84", css=SOMBRA),
      {"tipo": "flash", "t": E4, "d": 0.2, "max": 0.5},
      {"tipo": "numero", "t": E4 + 0.02, "d": E5 - E4 - 0.02, "xy": [0, 420], "valor": 40, "suf": " MI", "tam": 300, "z": 44},
      T(E4 + 0.6, E5 - E4 - 0.65, "DE NASCIMENTOS", y=880, f="130px Anton", css=SOMBRA),
      {"tipo": "flash", "t": E5, "d": 0.2, "max": 0.5},
      T(E5 + 0.02, n(60.9) - E5 - 0.04, "PAI COM 45 ANOS OU MAIS", y=360, f="120px Anton", vel=0.1, css=SOMBRA),
      {"tipo": "numero", "t": n(60.9), "d": E6 - n(60.9), "xy": [0, 360], "valor": 14, "pre": "+", "suf": "%", "tam": 320, "cor": "#ff5a5f", "z": 44, "sombra": "#5c0f14"},
      T(n(61.6), E6 - n(61.6) - 0.05, "CHANCE DE BEBÊ PREMATURO", y=860, f="112px Anton", vel=0.1, css=SOMBRA),
      {"tipo": "flash", "t": E6, "d": 0.2, "max": 0.5},
      T(E6 + 0.02, E7 - E6 - 0.04, "PEQUENO, MAS EXISTE", y=470, f="150px Anton", cor="#f2c230", css=SOMBRA),
      {"tipo": "flash", "t": E7, "d": 0.2, "max": 0.5},
      T(E7 + 0.02, t_cta - E7 - 0.04, "A MAIORIA NASCE BEM", y=470, f="150px Anton", cor="#3ddc84", css=SOMBRA),
      {"tipo": "desenho", "t": n(69.6), "d": t_cta - n(69.6) - 0.04, "formas": [{"k": "check", "c": [800, 860], "s": 70}], "cor": "#3ddc84", "espessura": 18, "z": 46},
      F(E1, E4 - E1, "Kong et al., Nature 2012 · 78 famílias (Islândia) · doi 10.1038/nature11396"),
      F(E4, t_cta - E4 - 0.02, "Khandwala et al., BMJ 2018 · 40,5 milhões de nascimentos (EUA) · doi 10.1136/bmj.k4372")]

# ---------------- CTA (banco cta6) ----------------
c += [{"tipo": "glitch", "t": t_cta - 0.05, "d": 0.25},
      {"tipo": "video", "t": t_cta, "d": d_cta, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[t_cta, 1.0, 0.01], [t_cta + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": t_cta + 0.2, "d": d_cta - 0.25, "y": 215, "txt": "SEGUE + CURTE = TREINO DO DEDÃO", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ---------------- FECHO (D alegre) ----------------
c += B(P + "_viral_blur.mp4", F0, dur - F0, 24.0)
c += [{"tipo": "glitch", "t": F0 - 0.05, "d": 0.25}, {"tipo": "flash", "t": F0, "d": 0.2, "max": 0.5},
      T(f(0.1), f(1.9) - f(0.1), "PLANEJANDO UM FILHO?", y=420, f="140px Anton", css=SOMBRA),
      {"tipo": "checklist", "t": f(1.9), "d": f(7.25) - f(1.9), "box": [120, 300, 840, 560], "titulo": "Na consulta:", "entra": "cai",
       "itens": [{"txt": "os dois juntos", "t": f(2.4), "marca": f(3.4)}, {"txt": "a idade dele", "t": f(4.8), "marca": f(5.4)}], "z": 40},
      {"tipo": "flash", "t": f(7.25), "d": 0.2, "max": 0.5},
      T(f(7.3), f(9.95) - f(7.3), "A FÁBRICA NÃO FECHA", y=380, f="140px Anton", cor="#3ddc84", css=SOMBRA),
      {"tipo": "fisio", "t": f(7.3), "d": dur - f(7.3), "z": 30, "orgaos": [{"k": "dn_fabrica", "xy": [540, 1060], "s": 1.15, "t": 0.0}],
       "fluxos": [{"de": [790, 1180], "para": [990, 880], "curva": -50, "cor": "#1f6fb2", "t": 0.6, "d": 2.2, "n": 6, "r": 11, "viagem": 1.0}]},
      T(f(9.95), dur - f(9.95), "MAS A MÁQUINA ENVELHECE", y=380, f="130px Anton", cor="#f2c230", vel=0.1, css=SOMBRA),
      {"tipo": "carimbo", "t": f(10.7), "d": dur - f(10.7), "xy": [110, 1330], "txt": "O RELÓGIO DELE ANDA", "tam": 84, "rot": -6, "z": 60},
      F(F0, dur - F0, "Kong et al., Nature 2012 · Khandwala et al., BMJ 2018")]

voz = [{"src": M + "dn_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "dn_viral.words.json", "gain": 0.16},
       {"src": M + "dn_dub_voz.wav", "t": 0, "ms": 0, "d": vd, "gain": 1.0},
       {"src": M + "dn_rosto.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "dn_rosto.words.json"},
       {"src": M + "dn_voz.wav", "t": r1, "ms": 0, "d": VEND, "palavras": M + "dn_voz.words.json"},
       {"src": M + "cta6.mp4", "t": t_cta, "ms": 0, "d": d_cta, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "dn_fecho_voz.wav", "t": F0, "ms": 0, "d": FEND, "palavras": M + "dn_fecho_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": 5.59, "gain": 0.3}, {"src": "glitch", "t": 9.10, "gain": 0.3},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": n(0.2), "gain": 0.5, "pico": 0.45},
       {"src": "notif", "t": n(1.2), "gain": 0.45}, {"src": "whoosh2", "t": n(3.85), "gain": 0.35}, {"src": "notif", "t": n(5.0), "gain": 0.45},
       {"src": "papel", "t": n(7.92), "gain": 0.45}, {"src": "whoosh", "t": n(8.4), "gain": 0.35, "pico": 0.45},
       {"src": "glitch", "t": A1 - 0.05, "gain": 0.5}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.5}, {"src": "boom", "t": E1, "gain": 0.55, "pico": 0.3, "d": 1.5},
       {"src": "boom", "t": E2, "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "whoosh2", "t": E3, "gain": 0.4},
       {"src": "whoosh2", "t": E4, "gain": 0.4}, {"src": "pagina", "t": E5, "gain": 0.4}, {"src": "boom", "t": n(60.9), "gain": 0.6, "pico": 0.3, "d": 1.5},
       {"src": "whoosh", "t": E6, "gain": 0.45, "pico": 0.45}, {"src": "whoosh2", "t": E7, "gain": 0.4}, {"src": "notif", "t": n(69.6), "gain": 0.35},
       {"src": "glitch", "t": t_cta - 0.05, "gain": 0.5}, {"src": "notif", "t": t_cta + 0.2, "gain": 0.4},
       {"src": "glitch", "t": F0 - 0.05, "gain": 0.5}, {"src": "papel", "t": f(1.9), "gain": 0.5}, {"src": "whoosh2", "t": f(7.3), "gain": 0.4},
       {"src": "whoosh2", "t": f(9.95), "gain": 0.4}, {"src": "boom", "t": f(10.7), "gain": 0.6, "pico": 0.3, "d": 1.5}]
salvar("react_l2_deniro", dur, 79, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, dur, 1730]]})
import json
p = json.load(open('planos/react_l2_deniro.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": r1, "d": round(t_cta - r1, 2), "gain": 0.14, "fade": 0.8},
                        {"src": "m_investiga", "t": F0, "d": round(dur - F0, 2), "gain": 0.12, "fade": 0.8}]
json.dump(p, open('planos/react_l2_deniro.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "aula", A1, AF, round(AF - A1, 2), "cta", t_cta, "fecho", F0)
