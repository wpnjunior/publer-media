# plano_esperma_aula.py (14/11, remake com aula, Fertilidade 26/11 19h12): react "esperma escorre / pernas para cima".
# Viral @casal_fertilidade (só texto + música cortada; a voz Murilo lê o texto): "Tentante: pernas para cima ajudam?
# E por travesseiro ajuda??? / Não / Os espermatozoides levam 2 minutos para chegarem nas trompas" -> VERDADE (eles acertam).
# NÃO sobrescreve o plano agendado (planos/react_esperma.json): lê de lá a parte de 0 a 13,017 s (entrada fe_entB,
# viral A + dublagem, rosto r1, viral B + dublagem + 5,5 MI) e refaz tudo depois.
# Roteiro: /mnt/project-files/reacts/remakes/esperma.md
# Voz em blocos por clima, sem atempo (voz c4755690, create_speech, 14/11):
#   A alegre (veredito) es_a_voz · B manso (AULA) es_b_voz · C neutro (estudo) es_c_voz · D alegre (fecho) es_d_voz.
#   Pausas longas entre frases aparadas para 0,7 s (B, C) e duas curtas de D esticadas para 0,7 s.
# Rostos: os mesmos arquivos do vídeo atual (fe_entB entrada, sp_rosto r1 e CTA). Nenhum rosto novo.
# Aula: CAIXINHA QUE SE DESENHA (cartão creme, aba lima, um desenho por cena). Pele: lab (a mesma do vídeo atual).
# Depois deste script: python3 scripts/pele.py react_esperma_aula lab
import sys, json; sys.path.insert(0, 'scripts')
from mk import M, B, T, F
PID = 'react_esperma_aula'
V = json.load(open('planos/react_esperma.json'))
V0 = 13.017                      # fim do viral B no plano atual (corte para a narração)

def wl(n): return json.load(open(M + n))
WA, WB, WC, WD = (wl(f'es_{k}_voz.words.json') for k in 'abcd')
tA = 13.04                       # voz A
tB = round(tA + WA[-1]['e'] + 0.75 - WB[0]['s'], 3)       # aula (0,75 s depois de "travesseiro")
tC = round(tB + WB[-1]['e'] + 0.75 - WC[0]['s'], 3)       # estudo
c1 = round(tC + WC[-1]['e'] + 0.6, 3)                     # CTA (rosto sp_rosto, banco do vídeo atual)
FACE_D = 4.395                   # sp_rosto ms 3,6 até o fim (7,88) + 0,115 s segurando o quadro sob o glitch
c2 = round(c1 + FACE_D, 3)       # "domingo" some em ~7,40 s do arquivo -> 0,5 s de folga antes do corte
tD = round(c2 + 0.05, 3)         # fecho
dur = round(tD + WD[-1]['e'] + 0.9, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3); f = lambda v: round(tD + v, 3)
TINTA, VERM, AZUL_T, VERDE_T = "#1c1a17", "#e0322b", "#1f5fb2", "#1f9e4f"
SOMBRA = "text-shadow:8px 8px 0 #000"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.5}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}

def FR(t, d, txt, tam=112, y=385, cor=TINTA):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [95, y], "w": 890, "fonte": f"{tam}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 45, "anim": "palavras", "vel": 0.09, "fixo": True}
def NOTA(t, d, txt, x, y, w=420, tam=96, cor=VERM, rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg)", "fixo": True}
def FS(t, d, orgaos, z=42, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def DS(t, d, formas, cor=VERM, lw=11, vel=0.45, z=44):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "fixo": True, "vel": vel}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 215], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}

# ================= 0 a 13,017 s: igual ao vídeo agendado =================
FIM_T = ('progresso', 'vinheta', 'grao')
velhas = V['camadas']
c = []
for L in velhas[1:]:
    if L['tipo'] in FIM_T: continue
    if L.get('t', 0) < V0 - 0.001 or (L['tipo'] == 'flash' and abs(L['t'] - V0) < 0.01):
        c.append(L)
fundo0 = dict(velhas[0], d=dur)
fim = [L for L in velhas if L['tipo'] in FIM_T]

# ================= A (alegre): veredito =================
c += B('sp_viral_blur.mp4', V0, tB - V0, 1.0)
c += [T(a(0.1), tB - a(0.1) - 0.05, "ELES ACERTAM:", y=380, f="160px Anton", cor="#3ddc84", anim=None, entra="zoom", css=SOMBRA),
      T(a(1.40), tB - a(1.40) - 0.05, "NÃO PRECISA", y=620, f="180px Anton", anim=None, entra="zoom", css=SOMBRA),
      FS(a(3.70), tB - a(3.70) - 0.05, [{"k": "almofada", "xy": [540, 1060], "s": 0.85, "t": 0.0}], z=41),
      DS(a(4.05), tB - a(4.05) - 0.05, [{"k": "x", "c": [540, 1060], "s": 115}], cor="#ff2d3d", lw=20)]

# ================= B (manso): AULA na CAIXINHA que se desenha =================
S1, S2, S3, S4 = b(2.62), b(8.55), b(14.15), b(18.55)
AF = tC
c += [GL(tB), FL(tB),
      {"tipo": "cartao", "t": tB, "d": round(AF - tB, 3), "box": [60, 330, 960, 1250], "aba": "1 · depois", "z": 30, "fixo": True,
       "abas": [[S1, "2 · sobe"], [S2, "3 · o ônibus"], [S3, "4 · o resto"], [S4, "5 · escorre"]]},
      SELO(tB + 0.2, AF - tB - 0.2, "● AULA RÁPIDA · DEPOIS DA RELAÇÃO")]
# (0) Depois da relação, é assim.
c += [FR(tB + 0.15, S1 - tB - 0.2, "DEPOIS DA RELAÇÃO", tam=140),
      FS(tB + 0.3, S1 - tB - 0.35, [{"k": "coracao_afeto", "xy": [540, 1030], "s": 1.15, "t": 0.0}], pulsos=[{"o": 0, "t": 0.9}, {"o": 0, "t": 1.7}])]
# (1) Os espermatozoides que nadam bem entram pelo colo do útero em poucos minutos.
c += [FR(S1 + 0.05, S2 - S1 - 0.1, "EM MINUTOS, ELES JÁ ENTRAM", tam=112),
      FS(S1 + 0.1, S2 - S1 - 0.15, [{"k": "utero", "xy": [540, 1010], "s": 1.25, "t": 0.0}],
         fluxos=[{"de": [540, 1440], "para": [540, 1236], "curva": 0, "cor": "#ffd400", "t": 0.9, "d": 2.4, "n": 6, "r": 12, "viagem": 0.7},
                 {"de": [540, 1222], "para": [540, 935], "curva": 0, "cor": "#ffd400", "t": 1.5, "d": 2.6, "n": 5, "r": 12, "viagem": 0.8},
                 {"de": [540, 925], "para": [345, 862], "curva": -40, "cor": "#ffd400", "t": 2.7, "d": 2.0, "n": 3, "r": 12, "viagem": 0.8},
                 {"de": [540, 925], "para": [735, 862], "curva": -40, "cor": "#ffd400", "t": 2.9, "d": 2.0, "n": 3, "r": 12, "viagem": 0.8}],
         pulsos=[{"o": 0, "t": 4.6}]),
      NOTA(b(4.45), S2 - b(4.45) - 0.05, "nadam bem", 575, 1300, w=350, tam=80, cor=AZUL_T, rot=3),
      DS(b(5.9), S2 - b(5.9) - 0.05, [{"k": "seta", "de": [250, 1335], "para": [470, 1225], "curva": -30}], cor=VERM, lw=12),
      NOTA(b(5.9), S2 - b(5.9) - 0.05, "colo do útero", 70, 1345, w=430, tam=88, cor=VERM, rot=-4)]
# (2) É como ônibus no ponto: quem tinha que entrar, entra rápido.
c += [FR(S2 + 0.05, S3 - S2 - 0.1, "É COMO ÔNIBUS NO PONTO", tam=112),
      FS(S2 + 0.1, S3 - S2 - 0.15, [{"k": "es_onibus", "xy": [480, 1010], "s": 1.3, "t": 0.0}],
         fluxos=[{"de": [578, 1345], "para": [578, 1085], "curva": 0, "cor": "#ffd400", "t": 2.8, "d": 2.3, "n": 7, "r": 18, "viagem": 0.8}],
         pulsos=[{"o": 0, "t": 4.5}]),
      NOTA(b(12.0), S3 - b(12.0) - 0.05, "entra rápido!", 80, 1250, w=450, tam=96, cor=VERDE_T, rot=-3)]
# (3) O resto do sêmen é quase todo líquido, e fica para trás.
c += [FR(S3 + 0.05, S4 - S3 - 0.1, "O RESTO É LÍQUIDO", tam=130),
      FS(S3 + 0.1, S4 - S3 - 0.15, [{"k": "es_gota", "xy": [540, 1010], "s": 1.15, "t": 0.0}], pulsos=[{"o": 0, "t": 2.1}]),
      NOTA(b(16.3), S4 - b(16.3) - 0.05, "fica para trás", 200, 1270, w=680, tam=96, cor=AZUL_T, rot=-3)]
# (4) É isso que escorre. E é normal.
c += [FR(S4 + 0.05, AF - S4 - 0.1, "ESCORRER É NORMAL", tam=130),
      FS(S4 + 0.1, AF - S4 - 0.15, [{"k": "utero", "xy": [540, 880], "s": 0.85, "t": 0.0}],
         fluxos=[{"de": [540, 1046], "para": [540, 1330], "curva": 0, "cor": "#a9bccb", "t": 0.35, "d": 2.5, "n": 6, "r": 16, "viagem": 1.0}]),
      NOTA(b(19.8), AF - b(19.8) - 0.05, "normal!", 600, 1250, w=320, tam=110, cor=VERDE_T, rot=-5),
      DS(b(20.6), AF - b(20.6) - 0.05, [{"k": "check", "c": [790, 1170], "s": 50}], cor=VERDE_T, lw=18)]
SFX_AULA = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": tB + 0.15, "gain": 0.4},
            {"src": "boing", "t": tB + 0.35, "gain": 0.25},
            {"src": "pagina", "t": S1, "gain": 0.4}, {"src": "boing", "t": b(4.45), "gain": 0.25},
            {"src": "scratch", "t": b(5.9), "gain": 0.25}, {"src": "boing", "t": b(6.0), "gain": 0.25},
            {"src": "pagina", "t": S2, "gain": 0.4}, {"src": "whoosh2", "t": b(11.35), "gain": 0.3}, {"src": "boing", "t": b(12.0), "gain": 0.3},
            {"src": "pagina", "t": S3, "gain": 0.4}, {"src": "boing", "t": b(16.3), "gain": 0.25},
            {"src": "pagina", "t": S4, "gain": 0.4}, {"src": "boing", "t": b(19.8), "gain": 0.3}, {"src": "notif", "t": b(20.6), "gain": 0.3}]

# ================= C (neutro): o estudo =================
E2, E3, E4, E5 = e(3.6), e(8.65), e(10.65), e(13.2)
c += B('sp_viral_blur.mp4', AF, c1 - AF, 7.0)
c += [GL(AF), FL(AF),
      T(e(0.05), E2 - e(0.05) - 0.05, "AINDA MAIS RÁPIDO", y=430, f="170px Anton", cor="#f2c230", anim=None, entra="zoom", css=SOMBRA),
      T(e(1.5), E2 - e(1.5) - 0.05, "QUE 2 MINUTOS", y=800, f="130px Anton", css=SOMBRA),
      FL(E2),
      {"tipo": "numero", "t": E2 + 0.05, "d": round(E3 - E2 - 0.1, 3), "xy": [0, 400], "valor": 1, "suf": " MINUTO", "tam": 300,
       "rotulo": "bolinhas até a trompa", "z": 44},
      FS(e(6.3), E3 - e(6.3) - 0.05, [{"k": "utero", "xy": [540, 1090], "s": 0.7, "t": 0.0}],
         fluxos=[{"de": [540, 1230], "para": [400, 1010], "curva": -60, "cor": "#ffd400", "t": 0.5, "d": 1.3, "n": 4, "r": 11, "viagem": 0.6}], z=41),
      F(E2, E3 - E2, "Kunz e col., Hum Reprod 1996 · bolinhas do tamanho do espermatozoide postas no colo do útero"),
      FL(E3),
      T(E3 + 0.05, E4 - E3 - 0.05, "E FICAR DEITADA?", y=430, f="160px Anton", css=SOMBRA),
      FS(E3 + 0.3, e(13.1) - E3 - 0.3, [{"k": "almofada", "xy": [540, 1030], "s": 0.85, "t": 0.0}], z=41),
      T(E4 + 0.05, c1 - E4 - 0.05, "NÃO PROVOU AJUDAR", y=400, f="160px Anton", cor="#ff2d3d", anim=None, entra="zoom", css="text-shadow:8px 8px 0 #5a0d10"),
      DS(e(11.95), e(13.1) - e(11.95), [{"k": "x", "c": [540, 1030], "s": 120}], cor="#ff2d3d", lw=20),
      T(E5, c1 - E5 - 0.05, "4 ESTUDOS", y=830, f="150px Anton", css=SOMBRA, anim=None, entra="zoom"),
      T(E5 + 0.6, c1 - E5 - 0.65, "1.361 CASAIS", y=1000, f="150px Anton", cor="#f2c230", css=SOMBRA, anim=None, entra="zoom"),
      F(E4, c1 - E4, "Cordary e col., J Gynecol Obstet Hum Reprod 2017 · ficar deitada depois da inseminação: 4 estudos, 1.361 casais")]

# ================= CTA: o mesmo rosto do vídeo atual (sp_rosto, 3,6 s até o fim) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": FACE_D, "ms": 3.6, "src": M + "sp_rosto.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [round(c1 + 2.6, 3), 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": round(c1 + 0.2, 3), "d": round(FACE_D - 0.25, 3), "y": 215, "txt": "COMBINADO: SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (alegre): fecho =================
c += B('sp_viral_blur.mp4', c2, dur - c2, 15.0)
c += [GL(c2), FL(c2),
      T(f(0.05), f(4.2) - f(0.05), "1 ANO TENTANDO?", y=380, f="170px Anton", vel=0.12),
      T(f(1.6), f(4.2) - f(1.6), "+35 ANOS:\\n6 MESES", y=760, f="150px Anton", cor="#f2c230", anim=None, entra="zoom", css=SOMBRA),
      FL(f(4.25)),
      T(f(4.3), f(8.2) - f(4.3), "CONSULTA PARA OS DOIS", y=400, f="160px Anton", cor="#3ddc84", anim=None, entra="zoom", css=SOMBRA),
      T(f(5.85), f(8.2) - f(5.85), "JUNTOS E SEM CULPA", y=790, f="110px Anton", css=SOMBRA, anim=None, entra="zoom"),
      FS(f(6.0), f(8.2) - f(6.0), [{"k": "coracao_afeto", "xy": [540, 1170], "s": 0.55, "t": 0.0}], pulsos=[{"o": 0, "t": 0.7}, {"o": 0, "t": 1.5}], z=41),
      FL(f(8.25)),
      T(f(8.3), dur - f(8.3), "O QUE IMPORTA NÃO ESCORRE", y=400, f="140px Anton", vel=0.12),
      T(f(10.35), dur - f(10.35), "JÁ SUBIU.", y=900, f="210px Anton", cor="#f2c230", anim=None, entra="zoom", css=SOMBRA),
      F(f(8.3), dur - f(8.3), "Kunz e col., Hum Reprod 1996 · doi 10.1093/humrep/11.3.627 · Cordary e col. 2017 · doi 10.1016/j.jogoh.2017.09.005 · Suarez e Pacey 2006 · ACOG 2019")]

# ================= áudio =================
voz = [v for v in V['audio']['voz'] if v['t'] < V0 - 0.001]
voz += [{"src": M + "es_a_voz.wav", "t": tA, "ms": 0, "d": 4.81, "palavras": M + "es_a_voz.words.json"},
        {"src": M + "es_b_voz.wav", "t": tB, "ms": 0, "d": 21.67, "palavras": M + "es_b_voz.words.json"},
        {"src": M + "es_c_voz.wav", "t": tC, "ms": 0, "d": 16.54, "palavras": M + "es_c_voz.words.json"},
        {"src": M + "sp_voz.wav", "t": c1, "ms": 24.5, "d": FACE_D, "palavras": M + "sp_voz.words.json"},
        {"src": M + "es_d_voz.wav", "t": tD, "ms": 0, "d": 12.29, "palavras": M + "es_d_voz.words.json"}]
sfx = [s for s in V['audio']['sfx'] if s['t'] < V0 + 0.01]
sfx += [{"src": "boing", "t": a(1.40), "gain": 0.35}, {"src": "boing", "t": a(3.70), "gain": 0.3}, {"src": "scratch", "t": a(4.05), "gain": 0.3},
        {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
        {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, {"src": "whoosh", "t": AF, "gain": 0.4, "pico": 0.45},
        {"src": "boing", "t": e(1.5), "gain": 0.3},
        {"src": "whoosh2", "t": E2, "gain": 0.35}, {"src": "boom", "t": E2 + 0.05, "gain": 0.45, "pico": 0.3, "d": 1.2},
        {"src": "whoosh2", "t": e(6.8), "gain": 0.3},
        {"src": "whoosh2", "t": E3, "gain": 0.35}, {"src": "boing", "t": E3 + 0.3, "gain": 0.3},
        {"src": "boom", "t": E4 + 0.05, "gain": 0.5, "pico": 0.3, "d": 1.5}, {"src": "scratch", "t": e(11.95), "gain": 0.3},
        {"src": "whoosh2", "t": E5, "gain": 0.35}, {"src": "boing", "t": E5 + 0.6, "gain": 0.3},
        {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
        {"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": c2, "gain": 0.4, "pico": 0.45},
        {"src": "boing", "t": f(1.6), "gain": 0.35}, {"src": "whoosh2", "t": f(4.25), "gain": 0.35}, {"src": "boing", "t": f(5.85), "gain": 0.3},
        {"src": "whoosh2", "t": f(8.25), "gain": 0.35}, {"src": "boom", "t": f(10.35), "gain": 0.55, "pico": 0.3, "d": 1.3}]
for s in sfx: s['t'] = round(s['t'], 3)
# trilha por baixo de toda a narração: m_investiga (23 s) até o meio da aula, m_emocao (41 s) até o fim
musica = [{"src": "m_investiga", "t": 12.9, "d": 23.0, "gain": 0.14, "fade": 0.8},
          {"src": "m_emocao", "t": round(S3 + 2.8, 3), "d": round(dur - S3 - 2.8, 3), "gain": 0.14, "fade": 0.8}]
assert musica[1]['d'] <= 41.0 and musica[1]['t'] < 12.9 + 23.0 - 0.3, musica
p = {"id": PID, "dur": dur, "seed": V.get('seed', 52), "fundo": V.get('fundo', '#0b1512'),
     "legenda": {"estilo": "lima", "y": 1340, "esconde": V['legenda']['esconde'],
                 "ys": V['legenda']['ys'] + [[tB, round(AF, 3), 1730]]},
     "camera": V.get('camera', {"amp": 1.0}),
     "audio": {"voz": voz, "musica": musica, "sfx": sfx},
     "camadas": [fundo0] + c + fim}
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok", PID, "dur", dur, "tA", tA, "tB", tB, "S1..S4", S1, S2, S3, S4, "tC", tC, "c1", c1, "c2", c2, "tD", tD)
