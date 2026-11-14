# plano_claudia_aula.py (14/11, remake com aula): react "Grávida depois dos 50" (Claudia, @canalgnt · Fertilidade 29/11 18h41).
# Roteiro: /mnt/project-files/reacts/remakes/claudia.md. Viral (5,17 s): "Eu engravidei naturalmente. Eu ovulei já na menopausa.
# Isso é raro? É." -> VERDADE ("ELA ACERTA: É RARO"). Não rebate nada que não foi dito.
# Edição da aula: EDIÇÃO FULL sem b-roll e sem caixinha (palavras gigantes Anton atrás, cheias e só contorno; um desenho grande
# por cena; cartela grande), troca visual a cada 2-4 s. No estudo: artigo em perspectiva com grifo + números 3D.
# Pele: NOTÍCIA (a mesma do vídeo atual). Rostos: os MESMOS arquivos (cr_rosto.mp4 r1 e CTA, fe_entA.mp4 na entrada), com a voz antiga.
# Voz nova em 3 gravações HeyGen por clima, SEM atempo (aparadas em /tmp/claude-0/cr_aula/bin/cortar.py, pausas ~0,7 s):
#   alegre  (A_raw, 13,5 s): "Ela acerta: é raro." -> cr_aula_a_voz  +  fecho "Dúvida? ... caminho." -> cr_aula_d_voz
#   manso   (B_raw, 27,8 s): aula -> cr_aula_b_voz
#   neutro  (C_raw, 24,2 s): estudo -> cr_aula_c_voz
# Depois deste script (igual ao original):
#   python3 scripts/entrada.py react_claudia_aula assets/midia/fe_entA.mp4 assets/midia/fe_entA.mp4.words.json 2.1 \
#     'GRÁVIDA DEPOIS DOS 50?' 'entrevista na TV reacendeu o assunto' && python3 scripts/pele.py react_claudia_aula noticia
import sys, json; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_claudia_aula'; P = 'cr'
vd = 5.17; r1 = 8.17                      # viral e rosto r1 iguais ao atual
def W(k): return json.load(open(M + f'cr_aula_{k}_voz.words.json'))
def dur_wav(k):
    import subprocess
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", M + f'cr_aula_{k}_voz.wav'],
                                capture_output=True, text=True).stdout)
WA, WB, WC, WD = W('a'), W('b'), W('c'), W('d')
DA, DB, DC, DD = dur_wav('a'), dur_wav('b'), dur_wav('c'), dur_wav('d')
GAP = 0.7                                  # pausa entre blocos
tA = r1                                    # "Ela acerta: é raro."
tB = round(tA + WA[-1]['e'] + GAP - WB[0]['s'], 2)      # aula
tC = round(tB + WB[-1]['e'] + GAP - WC[0]['s'], 2)      # estudo
c1 = round(tC + WC[-1]['e'] + 0.5, 2)                   # CTA: rosto antigo (cr_rosto ms 3,15 <-> cr_voz 24,6)
CTA_MS, CTA_D = 24.6, 5.06                              # "Revista não traz esse número. Aqui traz: curte e segue, casal." (24,86-29,36)
g = round(c1 + 3.4, 2)                                  # corta o rosto antes do sorrisão; entra a tela CURTE E SEGUE
c2 = round(c1 + (29.36 - CTA_MS) + GAP - WD[0]['s'], 2)  # fecho
dur = round(c2 + WD[-1]['e'] + 1.0, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3); f = lambda v: round(c2 + v, 3)
AMAR, VERM, BRANCO = "#ffd400", "#ff2d3d", "#ffffff"
SOMBRA = "text-shadow:8px 8px 0 #000"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.5}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}

def TT(t, d, txt, y=330, fz=130, cor=BRANCO, **k):
    L = T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SOMBRA, vel=0.09, **k); L["fixo"] = True; L["z"] = 45; return L
def GIG(t, d, txt, y=1300, tam=440, cont=False, cor="rgba(140,24,34,.55)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 3), "d": round(d, 3), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12, "fixo": True,
         "x": [1100, -int(len(txt) * tam * 0.5)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": 30, "orgaos": orgaos, "fixo": True}; L.update(k); return L
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69,
            "entra": "desliza", "fixo": True}

# ================= abertura (igual ao atual): viral em tela dividida + caixinha + rosto r1 =================
c = abertura(P, vd, "via @canalgnt", "center 17%", "Responde aí 👇", "Engravidar depois dos 50 é...", [])
for x in c:
    if x.get("tipo") == "pergunta": x["botoes"] = ["RARO", "COMUM"]
c += [rosto_r1(P, vd, r1 - vd, 0)]

# ================= veredito (alegre): "Ela acerta: é raro." =================
c += B(P + "_viral_blur.mp4", r1, tB - r1, 0.5)
c += [GL(r1), {"tipo": "flash", "t": r1, "d": 0.2, "max": 0.6},
      T(a(0.03), tB + 0.02 - a(0.03), "ELA ACERTA: É RARO", f="150px Anton"),
      {"tipo": "gigante", "t": a(1.45), "d": 0.6, "txt": "RARO", "y": 1180, "tam": 300, "cor": "#c6ff3d", "x": [1000, -1500], "z": 42}]

# ================= AULA (manso): EDIÇÃO FULL, uma ideia por cena =================
def wb(i): return WB[i]['s']
# índices das frases no WB: 0 E | 3 A (nasce) | 11 É (poupança) | 18 Perto | 25 Só | 33 Não | 39 Já | 45 Por
S1, S2, S3, S4, S5, S6, S7 = [round(wb(i) - 0.15, 2) for i in (3, 11, 18, 25, 33, 39, 45)]
AF = round(tC - tB, 2)       # fim da aula (relativo)
c += [GL(tB), FL(tB), SELO(tB + 0.1, AF - 0.1, "● AULA RÁPIDA · POR QUE É RARO?")]
# S0 "E por quê?"
c += [TT(b(0.05), S1 + 0.25 - 0.05, "POR QUÊ?", y=640, fz=230, cor=AMAR, anim=None, entra="zoom"),
      GIG(b(0.0), S1, "POR QUÊ?", y=1250, tam=460, cont=True, cor="rgba(255,212,0,.30)")]
# S1 "A mulher já nasce com todos os óvulos."
c += [FIS(b(S1), S2 - S1, [{"k": "ovario_cheio", "xy": [540, 1030], "s": 1.6, "t": 0.0, "rotulo": "OVÁRIO"}],
          pulsos=[{"o": 0, "t": wb(8) - S1}, {"o": 0, "t": wb(10) - S1}]),
      TT(b(S1 + 0.25), S2 - S1 - 0.25, "JÁ NASCE COM TODOS", fz=140),
      GIG(b(S1), S2 - S1, "ÓVULOS", y=1380, tam=420, ida=False),
      FL(b(S2))]
# S2 "É poupança sem depósito: só tem saque."  (cofrinho; os "óvulos" só saem)
c += [FIS(b(S2), S3 - S2, [{"k": "cr_cofrinho", "xy": [480, 1100], "s": 1.5, "t": 0.0, "rotulo": "POUPANÇA", "rot_y": 225}],
          fluxos=[{"de": [470, 900], "para": [930, 760], "curva": -100, "cor": "#ffe08a", "t": wb(15) - S2, "d": 1.4, "n": 6, "r": 18,
                   "viagem": 0.9, "rotulo": "SÓ SAI"}],
          encolhe=[{"o": 0, "t": wb(15) - S2 + 0.2, "para": 1.25, "d": 1.2}],
          pulsos=[{"o": 0, "t": 0.6}]),
      TT(b(S2 + 0.05), S3 - S2 - 0.05, "POUPANÇA SEM DEPÓSITO", fz=130),
      GIG(b(S2), S3 - S2, "SAQUE", y=1420, tam=440, cont=True, cor="rgba(255,212,0,.30)"),
      FL(b(S3))]
# S3 "Perto da menopausa, ainda escapa uma ovulação."
c += [FIS(b(S3), S4 - S3, [{"k": "ovario_pouco", "xy": [330, 1110], "s": 1.15, "t": 0.0, "rotulo": "SOBRA POUCO"},
                          {"k": "ovulo", "xy": [790, 860], "s": 0.8, "t": wb(22) - S3 + 0.5, "rotulo": "1 ÓVULO", "rot_y": 235}],
          fluxos=[{"de": [420, 1040], "para": [780, 870], "curva": -170, "cor": "#ffe08a", "t": wb(22) - S3 - 0.1, "d": 1.1, "n": 1, "r": 22, "viagem": 1.0}],
          pulsos=[{"o": 1, "t": wb(24) - S3}]),
      TT(b(S3 + 0.05), S4 - S3 - 0.05, "AINDA ESCAPA UMA OVULAÇÃO", fz=125),
      GIG(b(S3), S4 - S3, "MENOPAUSA", y=1440, tam=380),
      FL(b(S4))]
# S4 "Só que o óvulo envelhece com a mulher."
c += [FIS(b(S4), S5 - S4, [{"k": "ovulo", "xy": [320, 1060], "s": 0.95, "t": 0.0, "rotulo": "ÓVULO", "rot_y": 235},
                          {"k": "calendario", "xy": [790, 1060], "s": 0.95, "t": 0.2, "rotulo": "OS ANOS", "rot_y": 210}],
          pulsos=[{"o": 1, "t": wb(29) - S4}, {"o": 1, "t": wb(29) - S4 + 0.6}, {"o": 1, "t": wb(32) - S4}],
          encolhe=[{"o": 0, "t": wb(29) - S4, "para": 0.72, "d": 1.6}]),
      TT(b(S4 + 0.05), S5 - S4 - 0.05, "O ÓVULO ENVELHECE JUNTO", fz=125),
      GIG(b(S4), S5 - S4, "ENVELHECE", y=1440, tam=380, cont=True, cor="rgba(255,255,255,.22)", ida=False),
      FL(b(S5))]
# S5 "Não é culpa de ninguém, tá?"  (acolher)
c += [{"tipo": "fundo", "t": b(S5), "d": round(S6 - S5, 3), "cor": "rgba(255,79,130,.10)", "z": 13, "fixo": True},
      FIS(b(S5), S6 - S5, [{"k": "coracao_afeto", "xy": [540, 1060], "s": 1.35, "t": 0.05}],
          pulsos=[{"o": 0, "t": wb(35) - S5}, {"o": 0, "t": wb(37) - S5}, {"o": 0, "t": wb(38) - S5}]),
      TT(b(S5 + 0.05), S6 - S5 - 0.05, "NINGUÉM TEM CULPA", fz=150, cor=AMAR),
      GIG(b(S5), S6 - S5, "NINGUÉM", y=1440, tam=380),
      FL(b(S6))]
# S6 "Já o útero envelhece bem menos."
c += [FIS(b(S6), S7 - S6, [{"k": "utero", "xy": [540, 1050], "s": 1.5, "t": 0.05, "rotulo": "ÚTERO", "rot_y": 235}],
          pulsos=[{"o": 0, "t": wb(41) - S6}, {"o": 0, "t": wb(44) - S6}]),
      TT(b(S6 + 0.05), S7 - S6 - 0.05, "ÚTERO ENVELHECE BEM MENOS", fz=125),
      GIG(b(S6), S7 - S6, "ÚTERO", y=1440, tam=440, cont=True, cor="rgba(255,212,0,.30)", ida=False),
      FL(b(S7))]
# S7 "Por isso gravidez tão tarde costuma vir de óvulo mais jovem."
OV = round(wb(53) - 0.3 - S7, 2)          # óvulo aparece pouco antes de "óvulo mais jovem"
TJ = round(wb(50) - 0.1, 2)               # troca de cartela em "costuma"
c += [FIS(b(S7), AF - S7, [{"k": "utero", "xy": [730, 1180], "s": 1.2, "t": 0.0, "rotulo": "ÚTERO", "rot_y": 235},
                          {"k": "ovulo", "xy": [280, 880], "s": 0.72, "t": OV}],
          fluxos=[{"de": [340, 940], "para": [715, 1150], "curva": -60, "cor": "#ffe08a", "t": OV + 0.6, "d": 1.4, "n": 3, "r": 16, "viagem": 1.0}],
          pulsos=[{"o": 1, "t": OV + 0.45}, {"o": 0, "t": OV + 1.6}]),
      TT(b(S7 + 0.05), TJ - S7 - 0.05, "GRAVIDEZ TÃO TARDE", fz=140),
      TT(b(TJ), AF - TJ, "ÓVULO MAIS JOVEM", fz=150, cor=AMAR, anim=None, entra="zoom"),
      GIG(b(S7), AF - S7, "JOVEM", y=1440, tam=460)]
SFX_AULA = [{"src": "whoosh", "t": b(0.0), "gain": 0.45, "pico": 0.45}, {"src": "boing", "t": b(0.1), "gain": 0.3},
            {"src": "whoosh2", "t": b(S1), "gain": 0.35}, {"src": "boing", "t": b(S1 + 0.05), "gain": 0.3},
            {"src": "whoosh2", "t": b(S2), "gain": 0.35}, {"src": "boing", "t": b(S2 + 0.05), "gain": 0.3}, {"src": "notif", "t": b(wb(15)), "gain": 0.25},
            {"src": "whoosh2", "t": b(S3), "gain": 0.35}, {"src": "boing", "t": b(S3 + 0.05), "gain": 0.25}, {"src": "boing", "t": b(wb(22) + 0.5), "gain": 0.3},
            {"src": "whoosh2", "t": b(S4), "gain": 0.35}, {"src": "pagina", "t": b(S4 + 0.2), "gain": 0.3},
            {"src": "whoosh", "t": b(S5), "gain": 0.35, "pico": 0.45},
            {"src": "whoosh2", "t": b(S6), "gain": 0.35}, {"src": "boing", "t": b(S6 + 0.05), "gain": 0.3},
            {"src": "riser", "t": b(S7 - 1.2), "gain": 0.18, "d": 1.4}, {"src": "whoosh2", "t": b(S7), "gain": 0.35},
            {"src": "boing", "t": b(OV), "gain": 0.3}, {"src": "whoosh", "t": b(TJ), "gain": 0.35, "pico": 0.45}]

# ================= ESTUDO (neutro): ponte + números (tempos do cr_aula_c_voz) =================
def wc(i): return WC[i]['s']
# 0 Eu | 7 Em | 13 quase(90%) 14 | 15 não tiveram | 22 Depois(50) | 28 Com | 35 5 em cada | 41 É média
E1, E2, E3, E4, E5, E6 = [round(wc(i) - 0.15, 2) for i in (7, 13, 22, 28, 35, 41)]
EF = round(c1 - tC, 2)
c += B(P + "_viral_blur.mp4", tC, c1 - tC, 3.5)
c += [GL(tC), FL(tC),
      T(e(0.03), E1 - 0.03, "NÃO EXAMINEI NINGUÉM", f="140px Anton"),
      {"tipo": "gigante", "t": e(0.0), "d": E1, "txt": "NÚMERO", "y": 1180, "tam": 380, "cor": "#4a1016", "x": [1100, -2300], "z": 12},
      FL(e(E1)),
      {"tipo": "artigo", "t": e(E1), "d": E2 - E1, "box": [110, 320, 860, 500], "z": 34,
       "revista": "Human Reproduction · 2014", "titulo": "Quando a fertilidade da mulher termina",
       "autores": "Eijkemans e col. · seis populações sem anticoncepção", "rola": 0,
       "linhas": [{"txt": "58.051 mulheres acompanhadas", "grifo": e(wc(8))},
                  {"txt": "sem nenhum anticoncepcional", "grifo": e(wc(11))}],
       "rodape": "doi 10.1093/humrep/deu056"},
      T(e(E1 + 0.05), E2 - E1 - 0.05, "58 MIL MULHERES", y=880, f="150px Anton", vel=0.12, css=SOMBRA),
      FL(e(E2)),
      {"tipo": "numero", "t": e(E2 + 0.02), "d": E3 - E2 - 0.02, "xy": [0, 420], "valor": 90, "suf": "%", "tam": 300, "cor": "#f2c230", "z": 44},
      T(e(wc(15) - 0.1), E3 - wc(15) + 0.1, "SEM FILHO DEPOIS DOS 45", y=860, f="130px Anton", anim=None, entra="zoom", css=SOMBRA),
      FL(e(E3)),
      {"tipo": "numero", "t": e(E3 + 0.02), "d": E4 - E3 - 0.02, "xy": [0, 420], "valor": 100, "pre": "QUASE ", "suf": "%", "tam": 190, "cor": VERM, "sombra": "#5a0d10", "z": 44},
      T(e(E3 + 0.02), E4 - E3 - 0.02, "DEPOIS DOS 50", y=860, f="150px Anton", anim=None, entra="zoom", css=SOMBRA),
      F(e(E1), E4 - E1, "Eijkemans et al., Hum Reprod 2014"),
      FL(e(E4)),
      T(e(E4 + 0.02), E5 - E4 - 0.02, "COM TRATAMENTO, AOS 45", y=440, f="150px Anton", vel=0.12),
      {"tipo": "gigante", "t": e(E4), "d": E5 - E4, "txt": "TRATAMENTO", "y": 1180, "tam": 340, "cor": "#4a1016", "x": [1100, -2600], "z": 12},
      FL(e(E5)),
      {"tipo": "numero", "t": e(E5 + 0.02), "d": E6 - E5 - 0.02, "xy": [0, 420], "valor": 5, "suf": " EM 100", "tam": 240, "cor": "#f2c230", "z": 44},
      T(e(E5 + 0.02), E6 - E5 - 0.02, "TIVERAM BEBÊ", y=860, f="150px Anton", anim=None, entra="zoom", css=SOMBRA),
      F(e(E4), E6 - E4, "Seifer et al., Reprod Biol Endocrinol 2023"),
      T(e(E6 + 0.02), EF - E6 - 0.02, "É MÉDIA, NÃO SENTENÇA", f="140px Anton", cor="#3ddc84", css=SOMBRA),
      {"tipo": "gigante", "t": e(E6), "d": EF - E6, "txt": "MÉDIA", "y": 1180, "tam": 420, "cor": "#4a1016", "x": [-1300, 900], "z": 12}]
SFX_EST = [{"src": "whoosh", "t": e(0.0), "gain": 0.45, "pico": 0.45}, {"src": "whoosh2", "t": e(E1), "gain": 0.4}, {"src": "pagina", "t": e(E1 + 0.1), "gain": 0.45},
           {"src": "boom", "t": e(E2), "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "boom", "t": e(E3), "gain": 0.5, "pico": 0.3, "d": 1.2},
           {"src": "whoosh2", "t": e(E4), "gain": 0.4}, {"src": "boom", "t": e(E5), "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "whoosh2", "t": e(E6), "gain": 0.4}]

# ================= CTA (rosto antigo, voz antiga) + tela CURTE E SEGUE =================
c += rosto_r2(P, c1, g - c1, 3.15)
c[-1]["txt"] = "COMBINADO: CURTE + SEGUE"; c[-1]["d"] = round(g - c1 - 0.25, 2)
c += B(P + "_viral_blur.mp4", g, dur - g, 24.5)
c += [GL(g), FL(g),
      T(g + 0.02, c2 - g - 0.02, "CURTE E SEGUE", y=600, f="160px Anton", cor="#c6ff3d", anim=None, entra="zoom", css="text-shadow:10px 10px 0 #000"),
      FL(c2)]

# ================= FECHO (alegre) =================
def wd(i): return WD[i]['s']
# 0 Dúvida | 1 Vocês | 3 juntos | 6 Manchete | 10 consulta
c += [T(f(0.1), f(wd(6) - 0.1) - f(0.1), "DÚVIDA?", y=380, f="200px Anton", anim=None, entra="zoom"),
      T(f(wd(1) - 0.1), f(wd(6) - 0.1) - f(wd(1) - 0.1), "VOCÊS DOIS, JUNTOS, NO MÉDICO", y=700, f="118px Anton", cor="#3ddc84", vel=0.1, css=SOMBRA),
      {"tipo": "gigante", "t": f(wd(3)), "d": 0.6, "txt": "JUNTOS", "y": 1180, "tam": 300, "cor": "#c6ff3d", "x": [1000, -1900], "z": 42},
      FL(f(wd(6) - 0.1)),
      T(f(wd(6) - 0.08), dur - f(wd(6) - 0.08), "MANCHETE MOSTRA A EXCEÇÃO", y=380, f="122px Anton"),
      {"tipo": "carimbo", "t": f(wd(10) - 0.05), "d": round(dur - f(wd(10) - 0.05), 3), "xy": [40, 760], "txt": "EXCEÇÃO, NÃO REGRA", "tam": 100, "rot": -8, "z": 60},
      F(f(wd(10) - 0.05), dur - f(wd(10) - 0.05), "Eijkemans, Hum Reprod 2014 · doi 10.1093/humrep/deu056 · Seifer, Reprod Biol Endocrinol 2023 · doi 10.1186/s12958-023-01144-z")]

GA, GB, GC, GD = 0.871, 1.084, 1.072, 0.944   # iguala as gravações novas à voz antiga (-16,7 LUFS)
voz = [{"src": M + "cr_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + "cr_viral.words.json"},
       {"src": M + "cr_voz.wav", "t": vd, "ms": 0, "d": 2.72, "palavras": M + "cr_voz.words.json"},
       {"src": M + "cr_aula_a_voz.wav", "t": tA, "ms": 0, "d": round(DA, 3), "gain": GA, "palavras": M + "cr_aula_a_voz.words.json"},
       {"src": M + "cr_aula_b_voz.wav", "t": tB, "ms": 0, "d": round(DB, 3), "gain": GB, "palavras": M + "cr_aula_b_voz.words.json"},
       {"src": M + "cr_aula_c_voz.wav", "t": tC, "ms": 0, "d": round(DC, 3), "gain": GC, "palavras": M + "cr_aula_c_voz.words.json"},
       {"src": M + "cr_voz.wav", "t": c1, "ms": CTA_MS, "d": CTA_D, "palavras": M + "cr_voz.words.json"},
       {"src": M + "cr_aula_d_voz.wav", "t": c2, "ms": 0, "d": round(DD, 3), "gain": GD, "palavras": M + "cr_aula_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "boing", "t": 3.3, "gain": 0.4},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "whoosh", "t": vd, "gain": 0.4, "pico": 0.45},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": a(1.45), "gain": 0.5, "pico": 0.45},
       {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
       {"src": "glitch", "t": tC - 0.05, "gain": 0.45}, *SFX_EST,
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
       {"src": "glitch", "t": g - 0.05, "gain": 0.5}, {"src": "boing", "t": g + 0.1, "gain": 0.4},
       {"src": "glitch", "t": c2 - 0.05, "gain": 0.4}, {"src": "whoosh2", "t": f(wd(1) - 0.1), "gain": 0.4},
       {"src": "whoosh", "t": f(wd(3)), "gain": 0.4, "pico": 0.45}, {"src": "whoosh2", "t": f(wd(6) - 0.1), "gain": 0.35},
       {"src": "boom", "t": f(wd(10) - 0.05), "gain": 0.7, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 97, c, voz, sfx, {"r1_fim": r1, "esconde": [[0, 4.1]], "ys": [[4.1, vd, 1440], [vd, r1, 1000], [tB, tC, 1730]]})
p = json.load(open(f'planos/{PID}.json'))
# trilha por baixo de toda pausa: emoção sob veredito+aula, investigação sob o estudo (arquivo de 23 s), notícia sob CTA+fecho
p['audio']['musica'] = [{"src": "m_emocao", "t": round(r1 - 0.3, 2), "ms": 0, "d": round(tC + 0.4 - (r1 - 0.3), 2), "gain": 0.26, "fade": 0.8},
                        {"src": "m_investiga", "t": round(tC - 0.3, 2), "ms": 0, "d": 22.9, "gain": 0.26, "fade": 0.8},
                        {"src": "m_noticia", "t": round(tC + 21.9, 2), "ms": 0, "d": round(dur - (tC + 21.9), 2), "gain": 0.22, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "(+2,1 entrada)", "tA", tA, "tB", tB, "tC", tC, "c1", c1, "g", g, "c2", c2)
print("cenas aula", [S1, S2, S3, S4, S5, S6, S7, AF], "estudo", [E1, E2, E3, E4, E5, E6, EF])
