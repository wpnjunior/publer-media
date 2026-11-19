# plano_l2_teste.py (14/11, lote 2, TDAH): teste de TDAH do TikTok (@opaiokia, Robson Fidelis Filho), viral em português.
# Trecho 0,0-14,4 s: "9 perguntas, abaixe o dedo para positivo. Primeiro, presta pouca atenção a detalhes, se erra por falta
# de atenção. Dois, dificuldade em se concentrar e ler um livro." (na tela do viral: "Considerado pré diagnóstico").
# Veredito: MITO (dedo abaixado não é laudo), com a parte verdadeira dita (as perguntas parecem as de verdade).
# Edição da aula: CELULAR (telas feitas em tmp_tt/telas.py: o teste rolando com o dedo, notificações, resultado,
# grade dos 50 vídeos e o consenso), desenhos fisio saltando da tela. Sem b-roll. Pele: dossie.
# Voz em blocos (HeyGen c4755690..., sem atempo): A indignado (r1 + resposta), B manso (aula), C neutro (estudo), D alegre (fecho).
# Rosto r1 = os 3,28 s iniciais do bloco A no avatar 6cd9 (tk_rosto.mp4). Pausas longas aparadas (tmp_dn/encurta.py).
import sys, json, subprocess; sys.path.insert(0, 'scripts')
from mk import *
P = 'tk'; PID = 'react_l2_teste'
vd = 14.4                         # viral 0-14,4 ("livro." termina 13,94)
r1 = round(vd + 3.28, 2)          # rosto "Calma. Dedo abaixado não é laudo, tá?"
n = lambda v: round(r1 + 0.1 + v, 3)   # tempo em tk_voz.wav -> plano
VEND = 56.39
t_cta = round(n(VEND) + 0.3, 2); d_cta = 4.12
F0 = round(t_cta + d_cta + 0.05, 2)
f = lambda v: round(F0 + v, 3)    # tempo em tk_fecho_voz.wav -> plano
FEND = 8.66
dur = round(f(FEND) + 0.6, 2)
TINTA = "#1c1a17"
PH = dict(xy=[240, 560], wh=[600, 1100])   # celular: tela 262..818 x 582..1638, centro (540,1110)

def TX(t, d, txt, y=250, tam=112, cor="#ffffff", **k):
    return T(t, d, txt, y=y, f=f"{tam}px Anton", cor=cor, vel=0.1, css="text-shadow:6px 6px 0 rgba(0,0,0,.35)", **k)
def NOTA(t, d, txt, x, y, w=420, tam=92, cor="#b3121f", rot=-4, fundo=True):
    css = f"transform:rotate({rot}deg)" + (";background:rgba(255,255,255,.92);border-radius:18px;padding:4px 10px" if fundo else "")
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 52, "entra": "pop", "css": css, "fixo": True}
def FS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": 50, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def DS(t, d, formas, cor="#b3121f", lw=12):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": 51, "fixo": True}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}
def CEL(t, d, src=None, img=None):
    L = {"tipo": "celular", "t": round(t, 3), "d": round(d, 3), "z": 30, **PH}
    if src: L["video"] = {"src": M + src, "ms": 0}
    if img: L["img"] = M + img
    return L
def ROD(t, d, txt):   # fonte do estudo, logo acima da legenda
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 132], "w": 1000, "fonte": "600 26px Montserrat", "cor": "#ffffff",
            "alinha": "center", "txt": txt, "z": 70, "css": "text-shadow:0 2px 6px #000;background:rgba(0,0,0,.55);border-radius:10px;padding:4px 0", "fixo": True}

# ---------------- VIRAL + R1 ----------------
c = abertura(P, vd, "@opaiokia", "center 55%", "Vale como laudo? 👇", "Teste do TikTok dá diagnóstico de TDAH?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 2.5, "dec": 1, "suf": " MI DE VIEWS", "tam": 120}])
c += [{"tipo": "carimbo", "t": vd + 0.1, "d": r1 - vd - 0.15, "xy": [140, 480], "txt": "NÃO É LAUDO", "tam": 150, "rot": -7, "z": 60,
       "cor": "#b3121f", "blend": "normal", "css": "background:rgba(255,255,255,.9)", "fixo": True},
      rosto_r1(P, vd, r1 - vd, 0)]

# ---------------- RESPOSTA (A indignado): o teste rolando no celular ----------------
A1 = n(10.75)
c += B(P + "_viral_blur.mp4", r1, t_cta - r1, 2.0)
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": r1, "d": 0.2, "max": 0.5},
      CEL(r1, A1 - r1, src="tk_cel_teste.mp4"),
      TX(n(0.0), n(3.15) - n(0.0), "AS PERGUNTAS PARECEM REAIS", tam=118, cor="#3ddc84"),
      {"tipo": "flash", "t": n(3.2), "d": 0.2, "max": 0.4},
      TX(n(3.2), n(7.35) - n(3.2), "CONTAR DEDO NÃO É DIAGNÓSTICO", tam=112),
      {"tipo": "flash", "t": n(7.4), "d": 0.2, "max": 0.4},
      TX(n(7.4), A1 - n(7.4) - 0.05, "DIA RUIM? TODO MUNDO ABAIXA", tam=112)]

# ---------------- AULA (B manso): edição CELULAR, uma ideia por cena ----------------
AF = n(39.45)
S2, S3, S4, S5 = n(15.25), n(22.3), n(28.4), n(33.9)
c += [{"tipo": "glitch", "t": A1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": A1, "d": 0.2, "max": 0.5},
      CEL(A1, AF - A1, src="tk_cel_aula.mp4"),
      SELO(A1 + 0.2, AF - A1 - 0.2, "● AULA RÁPIDA · DE ONDE VEM A DISTRAÇÃO")]
# (1) A atenção tem um gerente, aqui na frente do cérebro.
c += [TX(A1 + 0.1, S2 - A1 - 0.15, "O GERENTE DA ATENÇÃO", tam=120),
      FS(A1 + 0.3, S2 - A1 - 0.35, [{"k": "cerebro_lado", "xy": [560, 1060], "s": 1.25, "t": 0.0}], pulsos=[{"o": 0, "t": 2.6}, {"o": 0, "t": 3.6}]),
      DS(n(12.9), S2 - n(12.9) - 0.05, [{"k": "seta", "de": [330, 1420], "para": [380, 1180], "curva": 30}], lw=13),
      NOTA(n(12.9), S2 - n(12.9) - 0.05, "a frente do cérebro", 300, 1440, w=500, tam=84)]
# (2) Muita coisa atrapalha esse gerente: sono ruim, ansiedade, tristeza, celular.
c += [{"tipo": "flash", "t": S2, "d": 0.2, "max": 0.4},
      TX(S2 + 0.05, S3 - S2 - 0.1, "MUITA COISA ATRAPALHA O GERENTE", tam=110)]
# (3) No TDAH, esse caminho, que usa dopamina, funciona diferente desde criança.
c += [{"tipo": "flash", "t": S3, "d": 0.2, "max": 0.4},
      TX(S3 + 0.05, S4 - S3 - 0.1, "NO TDAH, O CAMINHO FUNCIONA DIFERENTE", tam=104),
      FS(S3 + 0.1, S4 - S3 - 0.15, [{"k": "neuronio", "xy": [545, 1060], "s": 1.1, "t": 0.0}],
         fluxos=[{"de": [420, 1060], "para": [738, 1050], "curva": -50, "cor": "#ffd400", "t": 1.6, "d": 1.4, "n": 3, "r": 13, "viagem": 1.1, "rotulo": "DOPAMINA"},
                 {"de": [420, 1060], "para": [738, 1050], "curva": -50, "cor": "#ffd400", "t": 3.4, "d": 2.2, "n": 4, "r": 11, "viagem": 0.8}]),
      NOTA(n(26.5), S4 - n(26.5) - 0.05, "desde criança", 320, 1400, w=440, tam=96, cor="#1f6fb2", rot=-3)]
# (4) Pensa num termômetro: mostra a febre, mas não diz se é gripe ou dengue.
c += [{"tipo": "flash", "t": S4, "d": 0.2, "max": 0.4},
      TX(S4 + 0.05, S5 - S4 - 0.1, "O TERMÔMETRO MOSTRA A FEBRE", tam=112),
      FS(S4 + 0.1, S5 - S4 - 0.15, [{"k": "termometro", "xy": [540, 1040], "s": 1.25, "t": 0.0}], pulsos=[{"o": 0, "t": 2.1}]),
      NOTA(n(30.5), S5 - n(30.5) - 0.05, "38,5°", 600, 900, w=200, tam=96, cor="#b3121f", rot=6),
      NOTA(n(31.9), S5 - n(31.9) - 0.05, "gripe?", 290, 1400, w=240, tam=96, cor="#1c1a17", rot=-5),
      NOTA(n(32.2), S5 - n(32.2) - 0.05, "dengue?", 560, 1400, w=260, tam=96, cor="#1c1a17", rot=4)]
# (5) O teste do dedo é igual: mostra a distração, não diz de onde ela vem.
c += [{"tipo": "flash", "t": S5, "d": 0.2, "max": 0.4},
      TX(S5 + 0.05, n(37.2) - S5 - 0.1, "O TESTE DO DEDO É IGUAL", tam=120),
      {"tipo": "flash", "t": n(37.2), "d": 0.2, "max": 0.4},
      TX(n(37.2), AF - n(37.2), "NÃO ACHA A CAUSA", tam=130, cor="#ff5a5f")]

SFX_AULA = [{"src": "whoosh", "t": A1 + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": n(13.3), "gain": 0.3},
            {"src": "pagina", "t": S2, "gain": 0.35}, {"src": "notif", "t": n(17.62), "gain": 0.4}, {"src": "notif", "t": n(18.92), "gain": 0.4},
            {"src": "notif", "t": n(20.08), "gain": 0.4}, {"src": "notif", "t": n(21.28), "gain": 0.4},
            {"src": "pagina", "t": S3, "gain": 0.35}, {"src": "boing", "t": n(27.1), "gain": 0.3},
            {"src": "pagina", "t": S4, "gain": 0.35}, {"src": "boing", "t": n(30.5), "gain": 0.3}, {"src": "boing", "t": n(32.4), "gain": 0.25},
            {"src": "pagina", "t": S5, "gain": 0.35}, {"src": "whoosh2", "t": n(37.2), "gain": 0.35}]

# ---------------- ESTUDO (C neutro): grade dos 50 vídeos e o consenso no celular ----------------
E2, E3 = n(46.2), n(49.3)
c += [{"tipo": "glitch", "t": AF - 0.05, "d": 0.25}, {"tipo": "flash", "t": AF, "d": 0.2, "max": 0.5},
      CEL(AF, t_cta - AF, src="tk_cel_estudo.mp4"),
      TX(AF + 0.1, E2 - AF - 0.15, "50 VÍDEOS DE TESTE DE TDAH", y=262, tam=112),
      {"tipo": "numero", "t": E2, "d": E3 - E2, "xy": [0, 165], "valor": 92, "suf": "%", "tam": 220, "cor": "#ff5a5f", "sombra": "#5c0f14", "z": 44, "fixo": True},
      TX(E2 + 0.4, E3 - E2 - 0.45, "ENGANOSOS", y=432, tam=110, cor="#ff5a5f"),
      {"tipo": "flash", "t": E3, "d": 0.2, "max": 0.4},
      TX(E3, t_cta - E3 - 0.05, "NEM QUESTIONÁRIO OFICIAL BASTA", y=262, tam=112),
      ROD(AF + 0.3, E3 - AF - 0.3, "Verma e Sinha, 2024 · doi 10.1177/10398562241291956"),
      ROD(E3, t_cta - E3 - 0.02, "Faraone e col., 2021 · doi 10.1016/j.neubiorev.2021.01.022")]

# ---------------- CTA (banco cta6) ----------------
c += [{"tipo": "glitch", "t": t_cta - 0.05, "d": 0.25},
      {"tipo": "video", "t": t_cta, "d": d_cta, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[t_cta, 1.0, 0.01], [t_cta + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": t_cta + 0.2, "d": d_cta - 0.25, "y": 215, "txt": "SEGUE + CURTE = TREINO DO DEDÃO", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ---------------- FECHO (D alegre) ----------------
c += B(P + "_viral_blur.mp4", F0, dur - F0, 40.0)
c += [{"tipo": "glitch", "t": F0 - 0.05, "d": 0.25}, {"tipo": "flash", "t": F0, "d": 0.2, "max": 0.5},
      CEL(F0, dur - F0, img="tk_cel_fim.jpg"),
      TX(f(0.0), f(3.3) - f(0.0), "DEU POSITIVO? LEVA AO MÉDICO", tam=118),
      {"tipo": "flash", "t": f(3.3), "d": 0.2, "max": 0.4},
      TX(f(3.3), f(6.05) - f(3.3), "TESTE LEVANTA A DÚVIDA", tam=120),
      TX(f(6.05), dur - f(6.05), "AVALIAÇÃO RESPONDE", tam=130, cor="#3ddc84"),
      {"tipo": "carimbo", "t": f(6.3), "d": dur - f(6.3), "xy": [150, 1180], "txt": "SÓ COM AVALIAÇÃO", "tam": 92, "rot": -6, "z": 60,
       "cor": "#1f9e4f", "blend": "normal", "css": "background:rgba(255,255,255,.92)", "fixo": True}]

voz = [{"src": M + "tk_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "tk_viral.words.json"},
       {"src": M + "tk_rosto.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "tk_rosto.words.json"},
       {"src": M + "tk_voz.wav", "t": n(0), "ms": 0, "d": VEND, "palavras": M + "tk_voz.words.json"},
       {"src": M + "cta6.mp4", "t": t_cta, "ms": 0, "d": d_cta, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "tk_fecho_voz.wav", "t": F0, "ms": 0, "d": FEND, "palavras": M + "tk_fecho_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.1, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1 + 0.05, "gain": 0.45, "pico": 0.45},
       {"src": "notif", "t": n(3.5), "gain": 0.35}, {"src": "notif", "t": n(4.7), "gain": 0.3}, {"src": "notif", "t": n(5.9), "gain": 0.3},
       {"src": "whoosh2", "t": n(7.4), "gain": 0.35}, {"src": "boing", "t": n(7.6), "gain": 0.3},
       {"src": "glitch", "t": A1 - 0.05, "gain": 0.5}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.5}, {"src": "pagina", "t": AF + 0.3, "gain": 0.35},
       {"src": "boom", "t": E2, "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "papel", "t": E3, "gain": 0.4},
       {"src": "glitch", "t": t_cta - 0.05, "gain": 0.5}, {"src": "notif", "t": t_cta + 0.2, "gain": 0.4},
       {"src": "glitch", "t": F0 - 0.05, "gain": 0.5}, {"src": "whoosh2", "t": f(1.4), "gain": 0.35},
       {"src": "whoosh2", "t": f(3.3), "gain": 0.35}, {"src": "boom", "t": f(6.3), "gain": 0.55, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 92, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, dur, 1745]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": r1, "d": round(t_cta - r1, 2), "gain": 0.14, "fade": 0.8},
                        {"src": "m_investiga", "t": F0, "d": round(dur - F0, 2), "gain": 0.12, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
subprocess.run(["python3", "scripts/entrada.py", PID, M + "ent6.mp4", M + "ent6.mp4.words.json", "1.88",
                "TESTE DO TIKTOK “DÁ” TDAH?", "9 perguntas: abaixe o dedo para positivo"], check=True)
subprocess.run(["python3", "scripts/pele.py", PID, "dossie"], check=True)
print("ok dur", dur + 1.88, "r1", r1, "aula", A1, AF, round(AF - A1, 2), "cta", t_cta, "fecho", F0)
