# plano_cafe.py v3 (14/11 madrugada): refeito pelo pedido do Wagner (00h36): responder só ao que o viral
# diz (meia verdade), aula rápida de fisiologia para leigo (recompensa, dopamina, aula chata x videogame,
# cafeína tampa o aviso de cansaço) com camada fisio em cima de b-roll Mixkit, depois 2 estudos e fecho.
# Rosto r1 novo do avatar 6cd9; entrada ent6 e CTA cta6 do banco. Depois deste script:
#   python3 scripts/entrada.py react_cafe assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 '...' '...'
#   python3 scripts/pele.py react_cafe noticia
# Versões antigas: scripts/plano_cafe.v1.py, plano_cafe.v2.py; planos/react_cafe.v2.json, v3.json.
import sys; sys.path.insert(0, 'scripts')
from mk import *
P = 'cf'
VMS = 1.2                      # corta 1,2 s do começo mudo do viral (música tirada); teclado+riser cobrem o resto
vd = round(11.25 - VMS, 2)     # 10.05
r1 = round(vd + 4.6, 2)        # fim do rosto da reação (voz 0..4,55)
n = lambda v: round(v + (r1 - 4.55), 3)   # tempo da voz (aula+estudo) -> tempo do plano
t_cta = 51.0; d_cta = 4.12
n2 = lambda v: round(v + (t_cta + d_cta + 0.03 - 40.95), 3)  # fecho
dur = round(n2(47.84) + 0.6, 2)
ESC = 'rgba(8,4,6,.46)'

def BR(src, t, d, ms=0.0):
    z = [[t, 1.04, 0.01]]; k = 0.05; alto = True
    while k < d - 0.2:
        z.append([round(t + k, 3), 1.14 if alto else 1.04, round(min(1.2, d - k), 3)]); k += 1.2; alto = not alto
    return [{"tipo": "video", "t": round(t, 3), "d": round(d, 3), "ms": ms, "src": M + src, "box": [0, 0, 1080, 1920], "pos": "center",
             "respira": False, "z": 10, "zoom": z},
            {"tipo": "fundo", "t": round(t, 3), "d": round(d, 3), "cor": ESC, "z": 11}]

def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"}

SOMBRA = "text-shadow:8px 8px 0 #000"
c = abertura(P, vd, "via @psi.walace", "center 34%", "Mito ou verdade? ☕", "Quem tem TDAH dorme com café?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 821.8, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
for L in c:   # viral começa 1,2 s depois
    if L.get("tipo") == "video" and L.get("src", "").endswith("cf_viral.mp4"): L["ms"] = VMS
    if L.get("tipo") == "pergunta":
        L["botoes"] = ["MITO", "VERDADE", "MEIO A MEIO"]; L["escolha"] = 2
# R1: resposta grande logo depois do viral + rosto embaixo
c += [{"tipo": "carimbo", "t": vd + 0.1, "d": r1 - vd - 0.15, "xy": [95, 470], "txt": "MEIA VERDADE", "tam": 130, "rot": -7, "z": 60, "cor": "#ffd400", "blend": "normal"},
      rosto_r1(P, vd, r1 - vd, 0)]

# ---------------- AULA RÁPIDA (fisiologia para leigo) ----------------
A1, A2, A3, A4, A5, AF = n(4.6), n(10.35), n(15.0), n(20.05), n(24.6), n(27.7)
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": r1, "d": 0.2, "max": 0.5}]
c += BR("cf_br_cerebro.mp4", A1, A2 - A1) + BR("cf_br_scan.mp4", A2, A3 - A2) + BR("cf_br_aula.mp4", A3, n(18.85) - A3) \
     + BR("cf_br_game.mp4", n(18.85), A4 + 0.3 - n(18.85)) + BR("cf_br_cafe.mp4", A4 + 0.3, A5 - A4 - 0.3) + BR("cf_br_sono.mp4", A5, AF - A5)
c += [SELO(A1 + 0.2, AF - A1 - 0.2, "● AULA RÁPIDA · CÉREBRO")]
# A1: atenção segue a recompensa; o recado é a dopamina
c += [T(A1 + 0.05, A2 - A1 - 0.1, "ATENÇÃO SEGUE A RECOMPENSA", y=250, f="118px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": A1 + 0.3, "d": A2 - A1 - 0.35, "z": 42,
       "orgaos": [{"k": "cerebro", "xy": [540, 760], "s": 0.95, "t": 0.0},
                  {"k": "neuronio", "xy": [540, 1130], "s": 1.3, "t": 0.5}],
       "fluxos": [{"de": [384, 1110], "para": [790, 1110], "curva": -150, "cor": "#ffd400", "t": 1.8, "d": 3.6, "n": 10, "r": 15, "rotulo": "DOPAMINA", "viagem": 1.1}],
       "pulsos": [{"o": 0, "t": 0.9}, {"o": 0, "t": 3.2}]}]
# A2: no TDAH o sistema responde diferente, como se o sinal chegasse mais fraco
c += [{"tipo": "flash", "t": A2, "d": 0.2, "max": 0.4},
      T(A2 + 0.05, A3 - A2 - 0.1, "NO TDAH, O SINAL CHEGA MAIS FRACO", y=250, f="112px Anton", cor="#ffd400", css=SOMBRA),
      {"tipo": "fisio", "t": A2 + 0.25, "d": A3 - A2 - 0.3, "z": 42,
       "orgaos": [{"k": "cerebro", "xy": [540, 780], "s": 0.9, "t": 0.0},
                  {"k": "neuronio", "xy": [540, 1130], "s": 1.3, "t": 0.2}],
       "fluxos": [{"de": [384, 1110], "para": [790, 1110], "curva": -150, "cor": "#9a9a9a", "t": 0.9, "d": 3.2, "n": 3, "r": 9, "rotulo": "SINAL FRACO", "viagem": 1.6}],
       "encolhe": [{"o": 0, "t": 1.2, "para": 0.78, "d": 1.2}]}]
# A3: sem prazer, sem atenção: aula chata x videogame
c += [{"tipo": "flash", "t": A3, "d": 0.2, "max": 0.4},
      T(A3 - 0.02, n(17.2) - A3 + 0.02, "SEM PRAZER, SEM ATENÇÃO", y=300, f="140px Anton", css=SOMBRA),
      T(n(17.2), n(18.85) - n(17.2), "AULA CHATA", y=380, f="190px Anton", cor="#ff5a5a", anim=None, entra="zoom", css=SOMBRA),
      {"tipo": "gigante", "t": n(17.2), "d": n(18.85) - n(17.2), "txt": "ZZZ", "y": 900, "tam": 300, "cor": "rgba(255,255,255,.18)", "x": [900, -700], "z": 41},
      {"tipo": "flash", "t": n(18.85), "d": 0.2, "max": 0.45},
      T(n(18.85), A4 + 0.3 - n(18.85), "VIDEOGAME PRENDE", y=380, f="170px Anton", cor="#3ddc84", anim=None, entra="zoom", css=SOMBRA),
      {"tipo": "fisio", "t": n(18.95), "d": A4 + 0.25 - n(18.95), "z": 42,
       "orgaos": [{"k": "cerebro", "xy": [540, 960], "s": 0.75, "t": 0.0}],
       "fluxos": [{"de": [140, 1180], "para": [470, 930], "curva": -60, "cor": "#ffd400", "t": 0.15, "d": 1.4, "n": 6, "r": 13, "viagem": 0.7}],
       "pulsos": [{"o": 0, "t": 0.5}, {"o": 0, "t": 1.1}]}]
# A4: a cafeína tampa o aviso de cansaço e, de tabela, mexe nesse sistema
c += [{"tipo": "flash", "t": A4 + 0.3, "d": 0.2, "max": 0.4},
      T(A4 + 0.35, A5 - A4 - 0.4, "CAFEÍNA TAMPA O AVISO DE CANSAÇO", y=250, f="112px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": A4 + 0.4, "d": A5 - A4 - 0.45, "z": 42,
       "orgaos": [{"k": "xicara", "xy": [250, 1110], "s": 0.75, "t": 0.0, "rotulo": "CAFEÍNA", "rot_y": 200},
                  {"k": "cerebro", "xy": [760, 760], "s": 0.75, "t": 0.15}],
       "fluxos": [{"de": [80, 600], "para": [600, 700], "curva": -90, "cor": "#b9b9b9", "t": 0.35, "d": 1.5, "n": 4, "r": 12, "rotulo": "AVISO DE CANSAÇO", "viagem": 1.1},
                  {"de": [330, 1010], "para": [700, 860], "curva": -40, "cor": "#c8873a", "t": 1.3, "d": 2.4, "n": 7, "r": 13, "viagem": 0.9}],
       "pulsos": [{"o": 1, "t": 2.6}]},
      {"tipo": "texto", "t": A4 + 2.0, "d": A5 - A4 - 2.05, "xy": [250, 520], "w": 300, "fonte": "230px Anton", "cor": "#ff2d3d", "alinha": "center",
       "txt": "✕", "z": 46, "entra": "zoom", "css": "text-shadow:6px 6px 0 #000"}]
# A5: por isso, em alguns, acalma ou dá sono
c += [{"tipo": "flash", "t": A5, "d": 0.2, "max": 0.4},
      T(A5 + 0.05, AF - A5 - 0.05, "EM ALGUNS: ACALMA OU DÁ SONO", y=300, f="140px Anton", cor="#ffd400", css=SOMBRA),
      {"tipo": "gigante", "t": A5, "d": AF - A5, "txt": "SONO", "y": 860, "tam": 330, "cor": "rgba(255,255,255,.16)", "x": [1000, -1500], "z": 41}]

# ---------------- ESTUDOS ----------------
E2 = n(33.4)
c += B(P + "_viral_blur.mp4", AF, t_cta - AF, 0.5)
c += [{"tipo": "glitch", "t": AF - 0.05, "d": 0.25},
      {"tipo": "numero", "t": AF + 0.05, "d": n(30.75) - AF - 0.05, "xy": [0, 420], "valor": 7, "rotulo": "estudos com crianças", "tam": 300, "z": 44},
      {"tipo": "flash", "t": n(30.75), "d": 0.2, "max": 0.5},
      T(n(30.75), E2 - n(30.75), "CAFÉ NÃO MELHOROU OS SINTOMAS", y=440, f="140px Anton", cor="#f2c230", vel=0.12, css=SOMBRA),
      F(AF + 0.05, E2 - AF - 0.05, "Perrotte et al., Brain Sci 2023 · 7 estudos, 104 crianças de 5 a 15 anos"),
      {"tipo": "flash", "t": E2, "d": 0.2, "max": 0.5},
      T(E2 + 0.02, n(36.1) - E2 - 0.02, "300 ADOLESCENTES COM TDAH", y=440, f="150px Anton", vel=0.12),
      {"tipo": "flash", "t": n(36.1), "d": 0.2, "max": 0.5},
      {"tipo": "numero", "t": n(36.12), "d": n(39.3) - n(36.12), "xy": [0, 380], "valor": 2.5, "dec": 1, "suf": "x", "rotulo": "mais chance", "tam": 280, "cor": "#f2c230", "z": 44},
      T(n(36.3), n(39.3) - n(36.3), "CAFEÍNA À TARDE E À NOITE", y=900, f="110px Anton", anim=None, entra="zoom", css=SOMBRA),
      T(n(39.3), t_cta - n(39.3) - 0.02, "DORMIA PIOR", y=440, f="180px Anton", cor="#f2c230", css=SOMBRA),
      {"tipo": "gigante", "t": n(39.3), "d": t_cta - n(39.3), "txt": "SONO", "y": 760, "tam": 320, "cor": "#c6ff3d", "x": [1000, -1300], "z": 42},
      F(E2 + 0.02, t_cta - E2 - 0.02, "Cusick et al., J Pediatr Psychol 2020 · 302 adolescentes de 12 a 14 anos")]

# ---------------- CTA (banco cta6) ----------------
c += [{"tipo": "glitch", "t": t_cta - 0.05, "d": 0.25},
      {"tipo": "video", "t": t_cta, "d": d_cta, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[t_cta, 1.0, 0.01], [t_cta + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": t_cta + 0.2, "d": d_cta - 0.25, "y": 215, "txt": "SEGUE + CURTE = TREINO DO DEDÃO", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ---------------- FECHO ----------------
F0 = t_cta + d_cta
c += B(P + "_viral_blur.mp4", F0, dur - F0, 20.0)
c += [{"tipo": "flash", "t": F0, "d": 0.2, "max": 0.5},
      {"tipo": "checklist", "t": F0 + 0.03, "d": n2(43.75) - F0 - 0.03, "box": [120, 260, 840, 900], "titulo": "Vale consulta?", "entra": "cai",
       "itens": [{"txt": "sono demais", "t": n2(41.05)}, {"txt": "foco que não vem", "t": n2(42.25)}], "z": 40},
      T(n2(43.75), n2(45.95) - n2(43.75), "CONVERSA COM SEU MÉDICO", y=420, f="140px Anton", cor="#3ddc84", vel=0.1, css=SOMBRA),
      {"tipo": "carimbo", "t": n2(45.95), "d": dur - n2(45.95), "xy": [60, 760], "txt": "CAFÉ NÃO É EXAME", "tam": 118, "rot": -8, "z": 60},
      F(n2(45.95), dur - n2(45.95), "Perrotte, Brain Sci 2023 · doi 10.3390/brainsci13091304 · Cusick, J Pediatr Psychol 2020 · doi 10.1093/jpepsy/jsaa033")]

voz = [{"src": M + "cf_viral.mp4", "t": 0, "ms": VMS, "d": vd, "palavras": M + "cf_viral.words.json"},
       {"src": M + "cf_voz.wav", "t": vd, "ms": 0, "d": 4.55, "palavras": M + "cf_voz.words.json"},
       {"src": M + "cf_voz.wav", "t": n(4.55), "ms": 4.55, "d": round(40.6 - 4.55, 2), "palavras": M + "cf_voz.words.json"},
       {"src": M + "cta6.mp4", "t": t_cta, "ms": 0, "d": d_cta, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "cf_voz.wav", "t": n2(40.95), "ms": 40.95, "d": round(48.04 - 40.95, 2), "palavras": M + "cf_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "teclado", "t": 0.1, "d": 1.85, "gain": 0.55}, {"src": "riser", "t": 0.9, "d": 1.1, "gain": 0.35},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": A1 + 0.3, "gain": 0.4, "pico": 0.45},
       {"src": "boing", "t": A1 + 0.8, "gain": 0.3}, {"src": "whoosh2", "t": A2, "gain": 0.4}, {"src": "whoosh2", "t": A3, "gain": 0.4},
       {"src": "boing", "t": n(17.2), "gain": 0.35}, {"src": "whoosh", "t": n(18.85), "gain": 0.45, "pico": 0.45},
       {"src": "whoosh2", "t": A4 + 0.3, "gain": 0.4}, {"src": "boom", "t": A4 + 2.0, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": A5, "gain": 0.4}, {"src": "glitch", "t": AF - 0.05, "gain": 0.5},
       {"src": "boom", "t": AF + 0.05, "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "whoosh2", "t": n(30.75), "gain": 0.4},
       {"src": "whoosh2", "t": E2, "gain": 0.4}, {"src": "boom", "t": n(36.12), "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "boing", "t": n(36.3), "gain": 0.35},
       {"src": "whoosh", "t": n(39.3), "gain": 0.5, "pico": 0.45}, {"src": "glitch", "t": t_cta - 0.05, "gain": 0.5}, {"src": "notif", "t": t_cta + 0.2, "gain": 0.4},
       {"src": "glitch", "t": F0 - 0.05, "gain": 0.5}, {"src": "papel", "t": F0 + 0.03, "gain": 0.5}, {"src": "whoosh2", "t": n2(43.75), "gain": 0.4},
       {"src": "boom", "t": n2(45.95), "gain": 0.7, "pico": 0.3, "d": 1.5}]
salvar("react_cafe", dur, 93, c, voz, sfx, {"r1_fim": r1, "esconde": [[0, 4.0]], "ys": [[4.0, vd, 1440], [vd, r1, 1000]]})
import json
p = json.load(open('planos/react_cafe.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": r1, "d": round(t_cta - r1, 2), "gain": 0.14, "fade": 0.8}]
json.dump(p, open('planos/react_cafe.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "aula", A1, AF, "cta", t_cta, "fecho", F0)
