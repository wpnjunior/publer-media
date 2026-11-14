# plano_cafe_v5.py (14/11 manhã): EDIÇÃO CAIXINHA na aula (sem b-roll), pedido do Wagner 14/11 06h59:
# (1) voz sem "de tabela": frase nova "A cafeína tampa o aviso de cansaço e ainda mexe na dopamina."
#     emendada em assets/midia/cf_v5_voz.wav (+ .words.json); tudo depois anda 0,74 s para trás;
# (2) uma ideia por cena dentro do cartão creme com aba lima; (3) sem b-roll na aula.
# Estudos, CTA e fecho iguais ao plano_cafe.py (v4, agendado). Depois deste script:
#   python3 scripts/entrada.py react_cafe_v5 assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 '“QUEM TEM TDAH DORME COM CAFÉ”?' 'o vídeo passou de 800 mil views'
#   python3 scripts/pele.py react_cafe_v5 noticia
import sys; sys.path.insert(0, 'scripts')
from mk import *
P = 'cf'
VMS = 1.2                      # corta 1,2 s do começo mudo do viral (música tirada); teclado+riser cobrem o resto
vd = round(11.25 - VMS, 2)     # 10.05
r1 = round(vd + 4.6, 2)        # fim do rosto da reação (voz 0..4,55)
n = lambda v: round(v + (r1 - 4.55), 3)   # tempo da voz (aula+estudo) -> tempo do plano
S = 0.74                       # a frase nova é 0,74 s mais curta que a antiga
t_cta = round(51.0 - S, 2); d_cta = 4.12
N = lambda v: round(n(v) - S, 3)   # tempos ANTIGOS da voz (depois da emenda) -> plano novo
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

# ---------------- AULA RÁPIDA: EDIÇÃO CAIXINHA (sem b-roll) ----------------
# Tempos em segundos da voz NOVA (cf_v5_voz.wav); n() leva para o plano. Uma ideia por cena.
A1, A2, A3, A3b, A4, A4b, A5, AF = n(4.6), n(10.35), n(14.85), n(17.2), n(19.9), n(22.2), n(24.08), n(26.96)
TINTA = "#1c1a17"
ENT = 1.88   # entrada.py empurra "t" das camadas 1,88 s mas não os tempos internos de "abas": somo aqui
def FR(t, d, txt, tam=112, y=385, cor=TINTA):   # frase grande dentro da caixinha
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [95, y], "w": 890, "fonte": f"{tam}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 45, "anim": "palavras", "vel": 0.09, "fixo": True}
def NOTA(t, d, txt, x, y, w=420, tam=96, cor="#c0392b", rot=-4):   # anotação à mão (Caveat)
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg)", "fixo": True}
def FS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": 42, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def DS(t, d, formas, cor="#e0322b", lw=11):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": 44, "fixo": True}

c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": r1, "d": 0.2, "max": 0.5},
      {"tipo": "fundo", "t": A1, "d": AF - A1, "cor": "#0e1012", "textura": "gradiente", "cor2": "#22302a", "z": 11, "fixo": True},
      {"tipo": "cartao", "t": A1, "d": AF - A1, "box": [60, 330, 960, 1250], "aba": "1 · recompensa", "z": 30, "fixo": True,
       "abas": [[round(a + ENT, 3), x] for a, x in [[A2, "2 · no TDAH"], [A3, "3 · prazer"], [A4, "4 · cafeína"], [A4b, "5 · dopamina"], [A5, "6 · em alguns"]]]},
      SELO(A1 + 0.2, AF - A1 - 0.2, "● AULA RÁPIDA · CÉREBRO")]
c[-1]["fixo"] = True

# (a) O cérebro presta atenção no que dá recompensa. Quem leva esse recado é a dopamina.
c += [FR(A1 + 0.25, A2 - A1 - 0.3, "RECOMPENSA = ATENÇÃO", tam=120),
      FS(A1 + 0.35, A2 - A1 - 0.4, [{"k": "cf_estrela", "xy": [240, 1330], "s": 0.8, "t": 0.0},
                                     {"k": "cerebro", "xy": [690, 970], "s": 1.0, "t": 0.5}],
         pulsos=[{"o": 1, "t": 2.4}, {"o": 1, "t": n(8.6) - A1 - 0.35}]),
      DS(A1 + 1.6, A2 - A1 - 1.65, [{"k": "seta", "de": [330, 1250], "para": [520, 1080], "curva": 30}]),
      FS(n(8.25), A2 - n(8.25) - 0.05, [], fluxos=[{"de": [320, 1270], "para": [540, 1070], "curva": -40, "cor": "#ffd400", "t": 0.1, "d": 1.9, "n": 7, "r": 15, "viagem": 0.8}]),
      {"tipo": "texto", "t": n(8.4), "d": A2 - n(8.4) - 0.05, "xy": [430, 1330], "w": 560, "fonte": "120px Anton", "cor": "#ffd400", "alinha": "center",
       "txt": "DOPAMINA", "z": 46, "entra": "zoom", "css": "-webkit-text-stroke:10px #1c1a17;paint-order:stroke fill", "fixo": True}]
# (b) No TDAH, esse sistema responde diferente, como se o sinal chegasse mais fraco.
c += [FR(A2 + 0.1, A3 - A2 - 0.15, "NO TDAH, O SINAL CHEGA MAIS FRACO", tam=110),
      FS(A2 + 0.2, A3 - A2 - 0.25, [{"k": "neuronio", "xy": [540, 1080], "s": 1.5, "t": 0.0}],
         fluxos=[{"de": [380, 1080], "para": [800, 1080], "curva": -150, "cor": "#8e8e8e", "t": 0.7, "d": 3.4, "n": 3, "r": 10, "viagem": 1.7, "fica": True}]),
      DS(n(13.2), A3 - n(13.2) - 0.05, [{"k": "circulo", "c": [830, 1080], "r": [125, 150]}]),
      NOTA(n(13.18), A3 - n(13.18) - 0.05, "fraquinho...", 230, 1330, w=620, tam=110)]
# (c1) Sem prazer, não tem atenção
c += [FR(A3 + 0.03, A3b - A3 - 0.06, "SEM PRAZER, SEM ATENÇÃO", tam=140),
      FS(A3 + 0.15, A3b - A3 - 0.2, [{"k": "cerebro", "xy": [540, 1130], "s": 1.05, "t": 0.0}],
         encolhe=[{"o": 0, "t": 0.6, "para": 0.82, "d": 1.0}])]
# (c2) aula chata não prende, videogame prende
c += [FR(A3b + 0.05, A4 - A3b - 0.1, "AULA CHATA x VIDEOGAME", tam=120),
      DS(A3b + 0.1, A4 - A3b - 0.15, [{"k": "linha", "pts": [[540, 740], [536, 1120], [542, 1500]], "j": 4}], cor="#9aa3ad", lw=8),
      FS(n(17.25), A4 - n(17.25) - 0.05, [{"k": "cf_livro", "xy": [300, 1090], "s": 0.95, "t": 0.0}]),
      NOTA(n(17.6), A4 - n(17.6) - 0.05, "zzz", 330, 780, w=260, tam=120, cor="#5b6670", rot=-8),
      DS(n(18.05), A4 - n(18.05) - 0.05, [{"k": "x", "c": [300, 1100], "s": 120}], lw=16),
      FS(n(18.9), A4 - n(18.9) - 0.05, [{"k": "cf_controle", "xy": [785, 1080], "s": 0.95, "t": 0.0}], pulsos=[{"o": 0, "t": 0.7}]),
      DS(n(19.4), A4 - n(19.4) - 0.05, [{"k": "check", "c": [760, 1330], "s": 75}], cor="#1f9e4f", lw=18)]
# (d) A cafeína tampa o aviso de cansaço
c += [FR(A4 + 0.03, A4b - A4 - 0.06, "CAFEÍNA TAMPA O CANSAÇO", tam=120),
      FS(A4 + 0.1, A4b - A4 - 0.15, [{"k": "xicara", "xy": [290, 1160], "s": 1.0, "t": 0.0},
                                     {"k": "cf_bateria", "xy": [770, 1110], "s": 0.95, "t": 0.15}]),
      NOTA(A4 + 0.35, A4b - A4 - 0.4, "cansaço!", 590, 1195, w=360, tam=80, rot=-3),
      {"tipo": "texto", "t": n(20.64), "d": A4b - n(20.64) - 0.03, "xy": [578, 905], "w": 384, "fonte": "104px Anton", "cor": "#f4f1e8",
       "alinha": "center", "txt": "CAFEÍNA", "z": 47, "entra": "desliza", "dx": -430, "dy": 0, "fixo": True,
       "css": "background:#5a3418;border:8px solid #2b1a0e;border-radius:26px;padding:126px 0;letter-spacing:2px;box-shadow:0 14px 0 rgba(0,0,0,.25)"}]
# (e) e ainda mexe na dopamina
c += [FR(A4b + 0.03, A5 - A4b - 0.06, "MEXE NA DOPAMINA", tam=128),
      FS(A4b + 0.1, A5 - A4b - 0.15, [{"k": "xicara", "xy": [270, 1310], "s": 0.85, "t": 0.0},
                                      {"k": "cerebro", "xy": [720, 960], "s": 0.92, "t": 0.1}],
         fluxos=[{"de": [370, 1210], "para": [570, 1050], "curva": -30, "cor": "#ffd400", "t": 0.5, "d": 1.2, "n": 5, "r": 14, "viagem": 0.6}],
         pulsos=[{"o": 1, "t": 1.1}]),
      DS(A4b + 0.25, A5 - A4b - 0.3, [{"k": "seta", "de": [380, 1190], "para": [560, 1060], "curva": 25}])]
# (f) Por isso, em alguns, acalma ou dá sono.
c += [FR(A5 + 0.05, AF - A5 - 0.1, "EM ALGUNS: CALMA OU SONO", tam=120),
      FS(A5 + 0.1, AF - A5 - 0.15, [{"k": "cf_lua", "xy": [500, 1120], "s": 1.15, "t": 0.0}]),
      NOTA(n(25.4), AF - n(25.4) - 0.05, "Zzz", 620, 820, w=300, tam=140, cor="#2d5aa0", rot=-10)]

SFX_AULA = [{"src": "whoosh", "t": A1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": A1 + 0.15, "gain": 0.4},
            {"src": "boing", "t": A1 + 1.6, "gain": 0.3}, {"src": "pagina", "t": A2, "gain": 0.4}, {"src": "pagina", "t": A3, "gain": 0.4},
            {"src": "pagina", "t": A3b, "gain": 0.4}, {"src": "boing", "t": n(18.05), "gain": 0.35}, {"src": "notif", "t": n(19.4), "gain": 0.35},
            {"src": "pagina", "t": A4, "gain": 0.4}, {"src": "whoosh2", "t": n(20.64), "gain": 0.45}, {"src": "pagina", "t": A4b, "gain": 0.4},
            {"src": "pagina", "t": A5, "gain": 0.4}, {"src": "boing", "t": n(25.4), "gain": 0.3}]

# ---------------- ESTUDOS ----------------
E2 = N(33.4)
c += B(P + "_viral_blur.mp4", AF, t_cta - AF, 0.5)
c += [{"tipo": "glitch", "t": AF - 0.05, "d": 0.25},
      {"tipo": "numero", "t": AF + 0.05, "d": N(30.75) - AF - 0.05, "xy": [0, 420], "valor": 7, "rotulo": "estudos com crianças", "tam": 300, "z": 44},
      {"tipo": "flash", "t": N(30.75), "d": 0.2, "max": 0.5},
      T(N(30.75), E2 - N(30.75), "CAFÉ NÃO MELHOROU OS SINTOMAS", y=440, f="140px Anton", cor="#f2c230", vel=0.12, css=SOMBRA),
      F(AF + 0.05, E2 - AF - 0.05, "Perrotte et al., Brain Sci 2023 · 7 estudos, 104 crianças de 5 a 15 anos"),
      {"tipo": "flash", "t": E2, "d": 0.2, "max": 0.5},
      T(E2 + 0.02, N(36.1) - E2 - 0.02, "300 ADOLESCENTES COM TDAH", y=440, f="150px Anton", vel=0.12),
      {"tipo": "flash", "t": N(36.1), "d": 0.2, "max": 0.5},
      {"tipo": "numero", "t": N(36.12), "d": N(39.3) - N(36.12), "xy": [0, 380], "valor": 2.5, "dec": 1, "suf": "x", "rotulo": "mais chance", "tam": 280, "cor": "#f2c230", "z": 44},
      T(N(36.3), N(39.3) - N(36.3), "CAFEÍNA À TARDE E À NOITE", y=900, f="110px Anton", anim=None, entra="zoom", css=SOMBRA),
      T(N(39.3), t_cta - N(39.3) - 0.02, "DORMIA PIOR", y=440, f="180px Anton", cor="#f2c230", css=SOMBRA),
      {"tipo": "gigante", "t": N(39.3), "d": t_cta - N(39.3), "txt": "SONO", "y": 760, "tam": 320, "cor": "#c6ff3d", "x": [1000, -1300], "z": 42},
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
       {"src": M + "cf_v5_voz.wav", "t": vd, "ms": 0, "d": 4.55, "palavras": M + "cf_v5_voz.words.json"},
       {"src": M + "cf_v5_voz.wav", "t": n(4.55), "ms": 4.55, "d": round(40.6 - S - 4.55, 2), "palavras": M + "cf_v5_voz.words.json"},
       {"src": M + "cta6.mp4", "t": t_cta, "ms": 0, "d": d_cta, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "cf_v5_voz.wav", "t": n2(40.95), "ms": round(40.95 - S, 2), "d": round(48.04 - 40.95, 2), "palavras": M + "cf_v5_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "teclado", "t": 0.1, "d": 1.85, "gain": 0.55}, {"src": "riser", "t": 0.9, "d": 1.1, "gain": 0.35},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.5},
       {"src": "boom", "t": AF + 0.05, "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "whoosh2", "t": N(30.75), "gain": 0.4},
       {"src": "whoosh2", "t": E2, "gain": 0.4}, {"src": "boom", "t": N(36.12), "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "boing", "t": N(36.3), "gain": 0.35},
       {"src": "whoosh", "t": N(39.3), "gain": 0.5, "pico": 0.45}, {"src": "glitch", "t": t_cta - 0.05, "gain": 0.5}, {"src": "notif", "t": t_cta + 0.2, "gain": 0.4},
       {"src": "glitch", "t": F0 - 0.05, "gain": 0.5}, {"src": "papel", "t": F0 + 0.03, "gain": 0.5}, {"src": "whoosh2", "t": n2(43.75), "gain": 0.4},
       {"src": "boom", "t": n2(45.95), "gain": 0.7, "pico": 0.3, "d": 1.5}]
salvar("react_cafe_v5", dur, 93, c, voz, sfx, {"r1_fim": r1, "esconde": [[0, 4.0]], "ys": [[4.0, vd, 1440], [vd, r1, 1000], [A1, AF, 1730]]})
import json
p = json.load(open('planos/react_cafe_v5.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": r1, "d": round(t_cta - r1, 2), "gain": 0.14, "fade": 0.8}]
json.dump(p, open('planos/react_cafe_v5.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "aula", A1, AF, "cta", t_cta, "fecho", F0)
