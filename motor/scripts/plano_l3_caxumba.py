import sys, json; sys.path.insert(0, 'scripts')
from mk import *
# plano_l3_caxumba.py (14/11, lote 3, Fertilidade a Dois): "caxumba desce e deixa o homem estéril?"
# Viral: @banheiradeconhecimento (TikTok, canal de curiosidades). Trecho (2 pedaços, 9,73 s de fala + 0,5 s de folga congelada):
#   18,22-20,50 "Caxumba pode descer para os testículos." + 61,70-69,15 "E, em casos considerados mais graves, pode levar à
#   infertilidade, ou seja, pode deixar o homem estéril." (conferido com whisper medium + energia: o "e" do começo vem colado
#   no "em"; o "estéril" sai "estériu" e o "ou seja" seguinte começa 0,03 s depois, por isso o corte em 69,15 com fade de 40 ms).
# Veredito: VERDADE COM PORÉM (caixinha DEPENDE). Não dá porcentagem de esterilidade (revisões divergem).
# EDIÇÃO FULL sem b-roll, pele LAB: gigantes Anton (cheias e contorno), número 3D, artigo em perspectiva com grifo, carimbo,
# um desenho grande por cena (fisio_extra/cx_virus, cx_corpo, cx_rosto_inchado, cx_testiculo, cx_testiculo_inflamado,
# cx_capa, cx_bota, cx_exame; dn_fabrica reusado). Imagem do dia a dia: pé inchado em bota apertada.
# Voz: 3 create_speech por clima, SEM atempo: neutro (r1 + A + C, separados depois; 2 artefatos do TTS cortados),
# manso (B, aula), alegre (D). Pausas acertadas em tmp_cx/prep.py.
# Depois: python3 scripts/entrada.py react_l3_caxumba assets/midia/cx_ent6.mp4 assets/midia/cx_ent6.words.json 1.88 \
#   'CAXUMBA DESCE E DEIXA ESTÉRIL?' 'falaram isso num vídeo de curiosidades' && python3 scripts/pele.py react_l3_caxumba lab
P = 'cx'; vd = 10.23
J = 2.28                          # emenda entre os 2 pedaços do viral
r1 = round(vd + 3.90, 2)          # rosto 6cd9 "Calma. Tem verdade aí, mas tem porém." (última palavra 3,37 s + 0,5)
DA, DB, DC, DD = 16.32, 17.17, 26.15, 15.78
tA = r1
tB = round(tA + DA + 0.6, 2)
tC = round(tB + DB + 0.6, 2)
c1 = round(tC + DC + 0.4, 2)      # CTA 6cd9 (banco cta6)
c2 = round(c1 + 4.12, 2)
dur = round(c2 + DD + 0.6, 2)
a = lambda v: round(tA + v, 2); b = lambda v: round(tB + v, 2); e = lambda v: round(tC + v, 2); f = lambda v: round(c2 + v, 2)
BR, LIMA, AMAR, ROSA, VERM = '#ffffff', '#c6ff3d', '#ffd400', '#ff9fb4', '#ff2d3d'
SH = "text-shadow:6px 6px 0 #000"
def TT(t, d, txt, y=300, fz=120, cor=BR, **k):
    return T(t, d, txt, y=y, f=f"{fz}px Anton", cor=cor, css=SH, vel=0.09, **k)
def GIG(t, d, txt, y=1250, tam=460, cont=False, cor="rgba(198,255,61,.12)", ida=True):
    L = {"tipo": "gigante", "t": round(t, 2), "d": round(d, 2), "txt": txt, "y": y, "tam": tam, "cor": cor, "z": 12,
         "x": [1100, -int(len(txt) * tam * 0.52)] if ida else [-int(len(txt) * tam * 0.45), 900]}
    if cont: L["contorno"] = True
    return L
def FIS(t, d, orgaos, **k):
    L = {"tipo": "fisio", "t": round(t, 2), "d": round(d, 2), "z": 30, "orgaos": orgaos}; L.update(k); return L
def X(t, d, cx, cy, s=70, cor=VERM): return {"tipo": "desenho", "t": round(t, 2), "d": round(d, 2), "formas": [{"k": "x", "c": [cx, cy], "s": s}], "espessura": 16, "cor": cor, "z": 45}
def CHK(t, d, cx, cy, s=60): return {"tipo": "desenho", "t": round(t, 2), "d": round(d, 2), "formas": [{"k": "check", "c": [cx, cy], "s": s}], "espessura": 18, "cor": "#3ddc84", "z": 46}
def SETAS(t, d, pares, cor=VERM, lw=16):
    return {"tipo": "desenho", "t": round(t, 2), "d": round(d, 2), "formas": [dict(k="seta", de=de, para=pa, curva=0, t=tt) for de, pa, tt in pares], "espessura": lw, "cor": cor, "z": 45}
FL = lambda t: {"tipo": "flash", "t": round(t, 2), "d": 0.2, "max": 0.5}

# ================= abertura: viral em tela dividida + caixinha =================
c = [{"tipo": "cartao", "t": 0, "d": None, "box": [40, 150, 1000, 990], "aba": "o viral", "entra": "whip"},
     {"tipo": "video", "t": 0, "d": vd, "ms": 0, "src": M + P + "_viral.mp4", "box": [70, 190, 940, 909], "raio": 14, "pos": "center 22%", "arroba": "via @banheiradeconhecimento", "respira": False,
      "zoom": [[0, 1.0, 0.01], [J - 0.02, 1.07, 2.2], [J, 1.0, 0.01], [J + 3.0, 1.08, 3.0], [vd - 0.6, 1.12, 1.5]], "z": 30},
     {"tipo": "pergunta", "t": 0.1, "d": 3.95, "xy": [90, 1150], "w": 900, "topo": "Mito ou verdade? 👇", "txt": "Caxumba desce e deixa o homem estéril?", "botoes": ["MITO", "VERDADE", "DEPENDE"], "vel": 0.025, "escolha": 2, "t_escolha": 3.3},
     {"tipo": "glitch", "t": J - 0.05, "d": 0.2},
     T(4.1, vd - 4.1, "O QUE ELE DISSE", y=1170, f="105px Anton", cor="#ffffff", css=SH),
     GIG(4.1, vd - 4.1, "CAXUMBA", y=1500, tam=400, cont=True, cor="rgba(198,255,61,.35)"),
     {"tipo": "glitch", "t": vd - 0.05, "d": 0.25},
     {"tipo": "foto", "t": vd, "d": None, "src": M + P + "_still.jpg", "box": [70, 190, 940, 909], "raio": 14, "sombra": False, "z": 29},
     {"tipo": "texto", "t": vd + 0.05, "d": r1 - vd - 0.05, "xy": [40, 380], "w": 1000, "fonte": "150px Anton", "cor": AMAR, "alinha": "center", "txt": "TEM VERDADE,\\nMAS TEM PORÉM", "z": 50, "entra": "zoom", "css": "text-shadow:10px 10px 0 #000"},
     {"tipo": "video", "t": vd, "d": r1 - vd, "ms": 0, "src": M + P + "_r1.mp4", "box": [0, 1140, 1080, 780], "pos": "center 30%", "entra": "desliza", "z": 45}]

# ================= A (neutro): o que ele acertou e os poréns =================
c += [{"tipo": "glitch", "t": r1 - 0.05, "d": 0.25}, {"tipo": "flash", "t": r1, "d": 0.2, "max": 0.6},
      GIG(a(0), 4.75, "ACERTOU", y=1420, tam=420),
      TT(a(0.05), 1.6, "ELE ACERTOU", y=300, fz=160, cor=LIMA, anim=None, entra="zoom"),
      CHK(a(0.4), 1.3, 540, 580, s=55),
      FIS(a(1.5), 3.25, [{"k": "cx_testiculo", "xy": [540, 1060], "s": 1.6, "t": 0.1, "rotulo": "TESTÍCULO", "rot_y": 215}], pulsos=[{"o": 0, "t": 1.7}]),
      TT(a(1.65), 3.1, "PODE ATINGIR O TESTÍCULO", y=300, fz=125),
      FL(a(4.75)),
      GIG(a(4.75), 4.15, "GRAVE", y=1460, tam=440, cont=True, cor="rgba(255,45,61,.35)", ida=False),
      FIS(a(4.75), 4.15, [{"k": "cx_testiculo_inflamado", "xy": [540, 1080], "s": 1.5, "t": 0.1}], pulsos=[{"o": 0, "t": 1.4}, {"o": 0, "t": 2.6}]),
      TT(a(4.8), 1.9, "NOS CASOS GRAVES", y=300, fz=135, cor=ROSA),
      TT(a(6.7), 2.2, "PODE ATRAPALHAR A FERTILIDADE", y=300, fz=118),
      FL(a(8.9)),
      GIG(a(8.9), 2.1, "PORÉM", y=1250, tam=520, cont=True, cor="rgba(255,212,0,.35)"),
      TT(a(8.95), 2.05, "OS PORÉNS?", y=640, fz=220, cor=AMAR, anim=None, entra="zoom"),
      FL(a(11.0)),
      FIS(a(11.0), 2.6, [{"k": "cx_corpo", "xy": [540, 1110], "s": 2.0, "t": 0.05}]),
      SETAS(a(11.6), 2.1, [([540, 860], [540, 1240], 0)], cor=VERM, lw=18),
      X(a(12.2), 1.4, 540, 1050, s=110),
      TT(a(11.05), 2.55, "NÃO DESCE DO PESCOÇO", y=300, fz=130, cor=BR),
      FL(a(13.6)),
      GIG(a(13.6), DA + 0.6 - 13.6, "RARO", y=1350, tam=560, ida=False),
      TT(a(13.6), 1.8, "ESTÉRIL DE VEZ?", y=330, fz=150),
      TT(a(15.4), round(DA + 0.6 - 15.4, 2), "É RARO", y=760, fz=260, cor=AMAR, anim=None, entra="zoom")]

# ================= B (manso): AULA, uma ideia por cena (edição full) =================
c += [FL(tB)]
# S1 caxumba = vírus
c += [FIS(b(0), 1.95, [{"k": "cx_virus", "xy": [540, 1020], "s": 1.9, "t": 0.05}], pulsos=[{"o": 0, "t": 0.9}]),
      GIG(b(0), 1.95, "VÍRUS", y=1350, tam=520, cont=True, cor="rgba(155,107,214,.55)"),
      TT(b(0.05), 1.9, "CAXUMBA = VÍRUS", y=300, fz=150, cor=LIMA, anim=None, entra="zoom"),
      FL(b(1.95))]
# S2 viaja pelo sangue (bolinhas roxas correndo pelos vasos)
CX, CY, S = 540, 1110, 2.2
pt = lambda x, y: [round(CX + x * S), round(CY + y * S)]
c += [FIS(b(1.95), 2.05, [{"k": "cx_corpo", "xy": [CX, CY], "s": S, "t": 0.0}],
          fluxos=[{"de": pt(0, -84), "para": pt(0, -140), "curva": 0, "cor": "#b98cff", "t": 0.3, "d": 1.5, "n": 4, "viagem": 0.6, "r": 14},
                  {"de": pt(0, -84), "para": pt(-104, 40), "curva": -40, "cor": "#b98cff", "t": 0.35, "d": 1.5, "n": 4, "viagem": 0.7, "r": 14},
                  {"de": pt(0, -84), "para": pt(104, 40), "curva": -40, "cor": "#b98cff", "t": 0.4, "d": 1.5, "n": 4, "viagem": 0.7, "r": 14},
                  {"de": pt(0, -84), "para": pt(-46, 182), "curva": 0, "cor": "#b98cff", "t": 0.45, "d": 1.5, "n": 4, "viagem": 0.8, "r": 14},
                  {"de": pt(0, -84), "para": pt(46, 182), "curva": 0, "cor": "#b98cff", "t": 0.5, "d": 1.5, "n": 4, "viagem": 0.8, "r": 14}]),
      GIG(b(1.95), 2.05, "SANGUE", y=1400, tam=440, cor="rgba(255,45,61,.18)", ida=False),
      TT(b(2.0), 2.0, "VAI PELO SANGUE", y=300, fz=150),
      FL(b(4.0))]
# S3 gosta da glândula da saliva e do testículo
c += [FIS(b(4.0), 3.1, [{"k": "cx_rosto_inchado", "xy": [320, 1060], "s": 1.15, "t": 0.45, "rotulo": "SALIVA", "rot_y": 240},
                         {"k": "cx_testiculo", "xy": [790, 1080], "s": 1.05, "t": 1.95, "rotulo": "TESTÍCULO", "rot_y": 215}],
          pulsos=[{"o": 0, "t": 1.1}, {"o": 1, "t": 2.4}]),
      GIG(b(4.0), 3.1, "SALIVA", y=1450, tam=420, cont=True, cor="rgba(255,154,92,.40)"),
      TT(b(4.05), 3.05, "SALIVA E TESTÍCULO", y=300, fz=140),
      FL(b(7.1))]
# S4 capa dura que não estica
c += [FIS(b(7.1), 3.75, [{"k": "cx_capa", "xy": [540, 1060], "s": 2.0, "t": 0.05, "rotulo": "CAPA DURA", "rot_y": 240},
                          {"k": "cx_testiculo", "xy": [540, 1060], "s": 1.85, "t": 0.25}],
          pulsos=[{"o": 0, "t": 2.9}]),
      SETAS(b(9.55), 1.3, [([540, 1060], [540, 760], 0), ([540, 1060], [300, 1060], 0.08), ([540, 1060], [780, 1060], 0.16), ([540, 1060], [540, 1360], 0.24)], cor=AMAR, lw=16),
      GIG(b(7.1), 3.75, "DURA", y=1480, tam=480),
      TT(b(7.15), 2.2, "CAPA DURA", y=300, fz=170, cor=BR),
      TT(b(9.35), 1.5, "NÃO ESTICA", y=300, fz=170, cor=AMAR, anim=None, entra="zoom"),
      FL(b(10.85))]
# S5 inchou: aperta a fábrica
c += [{"tipo": "fundo", "t": b(10.85), "d": 3.75, "cor": "rgba(255,60,60,.16)", "z": 13, "fixo": True},
      FIS(b(10.85), 3.75, [{"k": "cx_capa", "xy": [540, 1060], "s": 2.0, "t": 0.0},
                            {"k": "cx_testiculo_inflamado", "xy": [540, 1060], "s": 2.0, "t": 0.15},
                            {"k": "dn_fabrica", "xy": [540, 1075], "s": 0.95, "t": 1.15}],
          pulsos=[{"o": 1, "t": 0.6}, {"o": 1, "t": 1.0}], encolhe=[{"o": 2, "t": 1.9, "para": 0.72, "d": 1.2}]),
      SETAS(b(12.0), 2.6, [([60, 1075], [250, 1075], 0), ([1020, 1075], [830, 1075], 0)], cor=VERM, lw=20),
      GIG(b(10.85), 3.75, "APERTA", y=1480, tam=420, cont=True, cor="rgba(255,45,61,.45)", ida=False),
      TT(b(10.9), 1.5, "INCHOU", y=300, fz=190, cor=ROSA, anim=None, entra="zoom"),
      TT(b(12.4), 2.2, "APERTA A FÁBRICA", y=300, fz=150),
      FL(b(14.6))]
# S6 pé inchado em bota apertada
c += [FIS(b(14.6), round(DB + 0.6 - 14.6, 2), [{"k": "cx_bota", "xy": [540, 1080], "s": 2.0, "t": 0.05}],
          pulsos=[{"o": 0, "t": 1.0}, {"o": 0, "t": 1.8}, {"o": 0, "t": 2.6}]),
      GIG(b(14.6), round(DB + 0.6 - 14.6, 2), "BOTA", y=1450, tam=520),
      TT(b(14.65), round(DB + 0.6 - 14.65, 2), "PÉ INCHADO\\nNA BOTA APERTADA", y=260, fz=125, cor=AMAR, anim=None, entra="zoom"),
      FL(tC)]

# ================= C (neutro): os estudos =================
c += [GIG(e(0), 1.95, "NÚMEROS", y=1300, tam=420, cont=True, cor="rgba(255,212,0,.35)"),
      TT(e(0.05), 1.9, "E OS NÚMEROS?", y=700, fz=190, cor=AMAR, anim=None, entra="zoom"),
      FL(e(1.95)),
      TT(e(2.0), 6.0, "DEPOIS DA PUBERDADE", y=300, fz=120),
      {"tipo": "numero", "t": e(3.7), "d": 4.3, "xy": [0, 560], "valor": 4, "pre": "ATÉ ", "suf": " EM 10", "rotulo": "homens com caxumba", "tam": 300, "cor": AMAR, "sombra": "#5a4600", "z": 44},
      GIG(e(2.0), 6.0, "4 EM 10", y=1450, tam=420),
      TT(e(5.9), 2.1, "TESTÍCULO INFLAMADO", y=1130, fz=120, cor=ROSA, anim=None, entra="zoom"),
      F(e(2.0), 6.0, "Philip e col., BJU Int 2006 · doi 10.1111/j.1464-410X.2006.05902.x"),
      FL(e(8.0)),
      GIG(e(8.0), 2.7, "ESTUDO", y=1350, tam=440, cont=True, cor="rgba(198,255,61,.35)", ida=False),
      TT(e(8.05), 2.65, "ESTUDO COM 67 HOMENS", y=600, fz=150),
      FL(e(10.7)),
      {"tipo": "numero", "t": e(10.7), "d": 3.35, "xy": [0, 300], "valor": 9, "pre": "QUASE ", "suf": " EM 10", "tam": 280, "cor": AMAR, "sombra": "#5a4600", "z": 44},
      FIS(e(10.7), 3.35, [{"k": "cx_testiculo_inflamado", "xy": [360, 1150], "s": 0.95, "t": 1.4},
                           {"k": "cx_testiculo", "xy": [720, 1160], "s": 0.9, "t": 1.55}],
          pulsos=[{"o": 0, "t": 2.0}, {"o": 0, "t": 2.8}]),
      TT(e(12.25), 1.8, "UM LADO SÓ", y=1440, fz=150, cor=LIMA, anim=None, entra="zoom"),
      F(e(8.0), 6.05, "Ternavasio-de la Vega e col., Medicine 2010 · 67 homens · doi 10.1097/MD.0b013e3181d63191"),
      FL(e(14.05)),
      TT(e(14.1), 2.3, "ESTÉRIL DE VEZ?", y=300, fz=160),
      {"tipo": "artigo", "t": e(16.4), "d": 3.2, "box": [100, 560, 880, 520], "z": 34,
       "revista": "Progrès en Urologie · 2002 · revisão", "titulo": "Ficar infértil depois da caxumba: exceção",
       "autores": "Mouchel e col. · revisão sobre caxumba no testículo", "rola": 0,
       "linhas": [{"txt": "“A infertilidade depois da caxumba é excepcional.”", "grifo": e(17.7)}],
       "rodape": "PMID 11980005"},
      GIG(e(14.05), 5.45, "EXCEÇÃO", y=1450, tam=400, cont=True, cor="rgba(255,255,255,.22)"),
      {"tipo": "carimbo", "t": e(18.15), "d": 1.35, "xy": [190, 1260], "txt": "EXCEÇÃO", "tam": 130, "rot": -8, "z": 60, "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)"},
      F(e(14.05), 5.45, "Mouchel e col., Prog Urol 2002 · PMID 11980005"),
      FL(e(19.5)),
      FIS(e(19.5), 4.2, [{"k": "cx_exame", "xy": [540, 1130], "s": 1.75, "t": 0.1}], pulsos=[{"o": 0, "t": 2.4}]),
      GIG(e(19.5), 4.2, "TEMPO", y=1480, tam=480, ida=False),
      TT(e(19.55), 4.15, "ESPERMOGRAMA PODE ALTERAR POR UM TEMPO", y=260, fz=110),
      FL(e(23.7)),
      GIG(e(23.7), round(c1 - e(23.7), 2), "VACINA", y=1350, tam=480, cont=True, cor="rgba(198,255,61,.40)"),
      TT(e(23.75), round(c1 - e(23.75), 2), "VACINA PREVINE", y=700, fz=190, cor=LIMA, anim=None, entra="zoom"),
      CHK(e(24.6), round(c1 - e(24.6), 2), 540, 1150, s=80)]

# ================= CTA (banco cta6) + fecho (D, alegre) =================
c += [{"tipo": "glitch", "t": c1 - 0.05, "d": 0.25},
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + P + "_cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[c1, 1.0, 0.01], [c1 + 2.6, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"},
      {"tipo": "glitch", "t": c2 - 0.05, "d": 0.25}, FL(c2),
      GIG(f(0), 2.95, "CHURRASCO", y=1400, tam=380),
      TT(f(0.05), 2.9, "CORRIGIR O TIO NO CHURRASCO", y=500, fz=135, cor=AMAR),
      FL(f(2.95)),
      GIG(f(2.95), 3.95, "TENTANTES", y=1400, tam=380, cont=True, cor="rgba(255,159,180,.40)", ida=False),
      TT(f(3.0), 3.9, "TEVE CAXUMBA NO TESTÍCULO E VOCÊS ESTÃO TENTANDO?", y=420, fz=118),
      FL(f(6.9)),
      TT(f(6.95), 1.6, "SEM PÂNICO", y=700, fz=210, cor=LIMA, anim=None, entra="zoom"),
      FL(f(8.55)),
      TT(f(8.6), 3.3, "OS DOIS NA CONSULTA\\n+ ESPERMOGRAMA", y=300, fz=125, anim=None, entra="zoom"),
      FIS(f(9.6), 2.3, [{"k": "cx_exame", "xy": [540, 1150], "s": 1.5, "t": 0.1}]),
      FL(f(11.9)),
      GIG(f(11.9), round(dur - f(11.9), 2), "MEDE", y=1450, tam=520),
      TT(f(11.95), round(dur - f(11.95), 2), "MEDO NÃO MEDE FERTILIDADE.", y=330, fz=125),
      {"tipo": "carimbo", "t": f(14.4), "d": round(dur - f(14.4), 2), "xy": [95, 930], "txt": "ESPERMOGRAMA MEDE", "tam": 84, "rot": -7, "z": 60, "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9);white-space:nowrap"},
      F(f(0), round(dur - f(0), 2), "Philip 2006 · Ternavasio-de la Vega 2010 · Mouchel 2002 · conteúdo educativo")]

voz = [{"src": M + P + "_viral.mp4", "t": 0, "ms": 0, "d": vd, "palavras": M + P + "_viral.words.json"},
       {"src": M + P + "_r1.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + P + "_r1.words.json"},
       {"src": M + P + "_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + P + "_a_voz.words.json"},
       {"src": M + P + "_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + P + "_b_voz.words.json"},
       {"src": M + P + "_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + P + "_c_voz.words.json"},
       {"src": M + P + "_cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + P + "_cta6.words.json"},
       {"src": M + P + "_d_voz.wav", "t": c2, "ms": 0, "d": DD, "palavras": M + P + "_d_voz.words.json"}]
musica = [{"src": "m_investiga", "t": r1, "ms": 0, "d": round(c1 - r1, 2), "gain": 0.30, "fade": 0.8},
          {"src": "m_emocao", "t": c2, "ms": 0, "d": round(dur - c2, 2), "gain": 0.26, "fade": 0.8}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5}, {"src": "boing", "t": 3.3, "gain": 0.4},
       {"src": "glitch", "t": J - 0.05, "gain": 0.35}, {"src": "pagina", "t": 4.1, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.05, "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.5}, {"src": "whoosh", "t": r1, "gain": 0.5, "pico": 0.45},
       # A
       {"src": "boing", "t": a(0.4), "gain": 0.35}, {"src": "whoosh2", "t": a(1.5), "gain": 0.3},
       {"src": "whoosh2", "t": a(4.75), "gain": 0.4}, {"src": "boom", "t": a(8.95), "gain": 0.5, "pico": 0.3, "d": 1.2},
       {"src": "whoosh2", "t": a(11.0), "gain": 0.35}, {"src": "scratch", "t": a(12.2), "gain": 0.35},
       {"src": "whoosh2", "t": a(13.6), "gain": 0.35}, {"src": "boom", "t": a(15.4), "gain": 0.5, "pico": 0.3, "d": 1.2},
       # aula
       {"src": "whoosh", "t": tB, "gain": 0.45, "pico": 0.45}, {"src": "boing", "t": b(0.1), "gain": 0.3},
       {"src": "whoosh2", "t": b(1.95), "gain": 0.35}, {"src": "riser", "t": b(2.2), "gain": 0.18, "d": 1.5},
       {"src": "whoosh2", "t": b(4.0), "gain": 0.35}, {"src": "boing", "t": b(4.45), "gain": 0.3}, {"src": "boing", "t": b(5.95), "gain": 0.3},
       {"src": "whoosh2", "t": b(7.1), "gain": 0.35}, {"src": "boing", "t": b(9.55), "gain": 0.3},
       {"src": "whoosh", "t": b(10.85), "gain": 0.4, "pico": 0.45}, {"src": "scratch", "t": b(12.0), "gain": 0.3},
       {"src": "whoosh2", "t": b(14.6), "gain": 0.35}, {"src": "boing", "t": b(15.6), "gain": 0.25}, {"src": "boing", "t": b(16.4), "gain": 0.22},
       # estudo
       {"src": "whoosh", "t": tC, "gain": 0.45, "pico": 0.45}, {"src": "whoosh2", "t": e(2.0), "gain": 0.35}, {"src": "riser", "t": e(2.4), "gain": 0.22, "d": 1.3},
       {"src": "boom", "t": e(3.7), "gain": 0.6, "pico": 0.3, "d": 1.5},
       {"src": "whoosh2", "t": e(8.0), "gain": 0.35}, {"src": "boom", "t": e(10.7), "gain": 0.55, "pico": 0.3, "d": 1.5}, {"src": "boing", "t": e(12.35), "gain": 0.3},
       {"src": "whoosh2", "t": e(14.05), "gain": 0.35}, {"src": "pagina", "t": e(16.45), "gain": 0.5}, {"src": "boom", "t": e(18.15), "gain": 0.55, "pico": 0.3, "d": 1.3},
       {"src": "whoosh2", "t": e(19.5), "gain": 0.35}, {"src": "whoosh", "t": e(23.7), "gain": 0.4, "pico": 0.45}, {"src": "boing", "t": e(24.6), "gain": 0.3},
       # CTA e fecho
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.5}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4}, {"src": "glitch", "t": c2 - 0.05, "gain": 0.5},
       {"src": "whoosh2", "t": f(2.95), "gain": 0.35}, {"src": "whoosh", "t": f(6.9), "gain": 0.4, "pico": 0.45},
       {"src": "whoosh2", "t": f(8.55), "gain": 0.35}, {"src": "whoosh2", "t": f(11.9), "gain": 0.35},
       {"src": "boom", "t": f(14.4), "gain": 0.6, "pico": 0.3, "d": 1.5}]
for L in c:
    if L.get("t", 0) >= vd - 0.06: L["fixo"] = True
salvar("react_l3_caxumba", dur, 317, c, voz, sfx, {"r1_fim": r1, "esconde": [[0, 4.1]], "ys": [[4.1, vd, 1360], [vd, r1, 1010], [r1, c1, 1720], [c2, dur, 1720]]})
p = json.load(open('planos/react_l3_caxumba.json')); p['audio']['musica'] = musica
json.dump(p, open('planos/react_l3_caxumba.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tB", tB, "tC", tC, "c1", c1, "c2", c2)
