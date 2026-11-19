# plano_l2_remedio.py (14/11, lote 2, TDAH): relato de uma paciente no TikTok @tdahdescomplicado.
# Trecho (6,5-19,9 s do original, 13,4 s): "Eu tinha passado uma semana com livros de constitucional abertos... não entendi
# nada... Aí ela passou a [bip]. Fiz tudo que eu fazia, igual. Só que com a diferença que eu tomei a [bip]." -> MEIA VERDADE
# (o tratamento ajuda a atenção a ficar; quem põe a matéria na cabeça é o método). Ela TEM diagnóstico (a médica receitou):
# tom acolhedor, nenhum nome de remédio (bip no áudio, legenda queimada do viral borrada), sem dose.
# Edição da aula: CAIXINHA QUE SE DESENHA (cartão creme, aba lima; cérebro, neurônio, óculos e lousa; uma ideia por cartão).
# Pele: LOUSA (TDAH já teve lab, dossiê e notícia). Voz em blocos por clima, sem atempo:
#   r1 + A neutro (rm_rosto / rm_a_voz), B manso (aula), C neutro (estudo), D alegre (fecho). Pausas longas aparadas para ~0,6-0,75 s.
# Depois deste script:
#   python3 scripts/entrada.py react_l2_remedio assets/midia/ent6.mp4 assets/midia/ent6.mp4.words.json 1.88 \
#     'REMÉDIO DE TDAH FAZ APRENDER?' 'relato que viralizou no TikTok' && python3 scripts/pele.py react_l2_remedio lousa
import sys, json; sys.path.insert(0, 'scripts')
from mk import *
PID = 'react_l2_remedio'; P = 'rm'
vd = 13.4                        # viral cortado (6,5-19,9), bips em 9,25-9,9 e 12,95-13,4
r1 = round(vd + 3.24, 2)         # rosto 6cd9 "Que bom que ela teve ajuda. Mas tem um detalhe." (rm_rosto.mp4, 3,24 s)
DA, DB, DC, DD = 10.18, 21.9, 18.2, 11.9
tA = round(r1 + 0.2, 2)
tB = round(tA + DA + 0.6, 2)
tC = round(tB + DB + 0.6, 2)
c1 = round(tC + DC + 0.4, 2)     # CTA 6cd9 (banco cta6)
c2 = round(c1 + 4.12, 2)
dur = round(c2 + DD + 0.6, 2)
a = lambda v: round(tA + v, 3); b = lambda v: round(tB + v, 3); e = lambda v: round(tC + v, 3); f = lambda v: round(c2 + v, 3)
ENT = 1.88                       # entrada.py empurra "t" mas não os tempos internos de "abas"
TINTA, VERM, AZUL_T, VERDE_T, CINZA = "#1c1a17", "#e0322b", "#1f5fb2", "#1f9e4f", "#5b6670"
SOMBRA = "text-shadow:8px 8px 0 #000"
FL = lambda t: {"tipo": "flash", "t": round(t, 3), "d": 0.2, "max": 0.5}
GL = lambda t: {"tipo": "glitch", "t": round(t - 0.05, 3), "d": 0.25}

def FR(t, d, txt, tam=112, y=385, cor=TINTA):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [95, y], "w": 890, "fonte": f"{tam}px Anton", "cor": cor,
            "alinha": "center", "txt": txt, "z": 45, "anim": "palavras", "vel": 0.09, "fixo": True}
def NOTA(t, d, txt, x, y, w=420, tam=96, cor=VERM, rot=-4):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [x, y], "w": w, "fonte": f"700 {tam}px Caveat", "cor": cor,
            "alinha": "center", "txt": txt, "z": 46, "entra": "pop", "css": f"transform:rotate({rot}deg)", "fixo": True}
def FS(t, d, orgaos, z=42, fixo=True, **k):
    L = {"tipo": "fisio", "t": round(t, 3), "d": round(d, 3), "z": z, "orgaos": orgaos, "fixo": fixo}; L.update(k); return L
def DS(t, d, formas, cor=VERM, lw=11, vel=0.45, z=44):
    return {"tipo": "desenho", "t": round(t, 3), "d": round(d, 3), "formas": formas, "cor": cor, "espessura": lw, "z": z, "fixo": True, "vel": vel}
def SELO(t, d, txt):
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [40, 128], "w": 1000, "fonte": "900 32px Montserrat", "cor": "#111",
            "alinha": "center", "txt": txt, "css": "letter-spacing:3px;background:#ffd400;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza", "fixo": True}
def LOUSA(t, d, borrada):
    """lousinha verde com conta de giz; borrada = sem óculos"""
    css = ("background:#23443a;border:14px solid #8a5a2b;border-radius:10px;padding:34px 0;line-height:1.1;"
           + ("filter:blur(9px);" if borrada else ""))
    return {"tipo": "texto", "t": round(t, 3), "d": round(d, 3), "xy": [190, 760], "w": 700, "fonte": "700 120px Caveat", "cor": "#f4f1e8",
            "alinha": "center", "txt": "ABC", "z": 43, "entra": "pop" if not borrada else None, "css": css, "fixo": True}

# ================= abertura: viral em tela dividida + caixinha de pergunta =================
c = abertura(P, vd, "@tdahdescomplicado", "center 30%", "Mito ou verdade? 👇", "O remédio de TDAH faz aprender?",
             [{"tipo": "numero", "t": 4.3, "d": vd - 4.35, "xy": [0, 1150], "valor": 83.1, "dec": 1, "suf": " MIL VIEWS", "tam": 120}])
for L in c:
    if L.get("tipo") == "pergunta":
        L["botoes"] = ["MITO", "VERDADE", "MEIO A MEIO"]; L["escolha"] = 2
c += [{"tipo": "texto", "t": vd + 0.02, "d": r1 - vd - 0.02, "xy": [70, 190], "w": 940, "fonte": "112px Anton", "cor": "#ffffff", "alinha": "center",
       "txt": "“FIZ TUDO IGUAL,\\nSÓ QUE TOMEI\\nO REMÉDIO”", "z": 55, "entra": "pop", "fixo": True,
       "css": "background:rgba(11,21,18,.9);border-radius:14px;height:909px;box-sizing:border-box;padding:150px 40px 0;line-height:1.15;text-shadow:6px 6px 0 #000"},
      {"tipo": "carimbo", "t": vd + 0.45, "d": r1 - vd - 0.45, "xy": [170, 700], "txt": "MEIA VERDADE", "tam": 130, "rot": -7, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)", "fixo": True},
      rosto_r1(P, vd, r1 - vd, 0)]

# ================= A (neutro, acolhendo): a história é real; o tratamento ajuda a atenção; não põe matéria na cabeça =================
c += B(P + "_viral_blur.mp4", r1, tB - r1, 30.0)
c += [GL(r1), FL(r1),
      T(a(0.0), a(2.6) - a(0.0), "A HISTÓRIA DELA É REAL", y=430, f="150px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": a(0.2), "d": a(2.6) - a(0.2), "z": 30, "orgaos": [{"k": "coracao_afeto", "xy": [540, 1080], "s": 1.3, "t": 0.0}],
       "pulsos": [{"o": 0, "t": 0.9}, {"o": 0, "t": 1.8}]},
      FL(a(2.6)),
      T(a(2.62), a(5.0) - a(2.62), "DIAGNÓSTICO + ACOMPANHAMENTO", y=400, f="124px Anton", cor="#3ddc84", css=SOMBRA),
      {"tipo": "desenho", "t": a(3.3), "d": a(5.0) - a(3.3), "formas": [{"k": "check", "c": [540, 1080], "s": 80}], "cor": "#3ddc84", "espessura": 20, "z": 46},
      T(a(5.05), a(7.6) - a(5.05), "A ATENÇÃO FICA", y=420, f="170px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": a(5.1), "d": a(7.6) - a(5.1), "z": 30, "orgaos": [{"k": "cerebro_lado", "xy": [540, 1100], "s": 1.25, "t": 0.0}],
       "pulsos": [{"o": 0, "t": 0.8}]},
      FL(a(7.65)),
      T(a(7.7), tB - a(7.7) - 0.05, "NÃO PÕE MATÉRIA NA CABEÇA", y=380, f="140px Anton", cor="#f2c230", css=SOMBRA),
      {"tipo": "gigante", "t": a(8.4), "d": tB - a(8.4) - 0.05, "txt": "MATÉRIA?", "y": 1150, "tam": 280, "cor": "rgba(255,255,255,.16)", "x": [1000, -1900], "z": 20}]

# ================= B (manso): AULA na CAIXINHA que se desenha =================
S1, S2, S3, S4, S5 = b(0.0), b(5.95), b(10.8), b(15.6), b(19.15)
AF = b(DB + 0.3)
c += [GL(tB), FL(tB),
      {"tipo": "fundo", "t": tB, "d": AF - tB, "cor": "#0e1012", "textura": "gradiente", "cor2": "#22302a", "z": 11, "fixo": True},
      {"tipo": "cartao", "t": tB, "d": AF - tB, "box": [60, 330, 960, 1250], "aba": "1 · o foco", "z": 30, "fixo": True,
       "abas": [[round(x + ENT, 3), s] for x, s in [[S2, "2 · no TDAH"], [S3, "3 · o remédio"], [S4, "4 · o óculos"], [S5, "5 · a matéria"]]]},
      SELO(tB + 0.2, AF - tB - 0.2, "● AULA RÁPIDA · ATENÇÃO X MATÉRIA")]
# (1) Olha só. Na frente do cérebro, um sistema que usa dopamina segura a atenção.
c += [FR(S1 + 0.15, S2 - S1 - 0.2, "A FRENTE DO CÉREBRO SEGURA A ATENÇÃO", tam=104),
      FS(S1 + 0.3, S2 - S1 - 0.35, [{"k": "cerebro_lado", "xy": [560, 1080], "s": 1.45, "t": 0.0}], pulsos=[{"o": 0, "t": 2.0}, {"o": 0, "t": 4.3}]),
      DS(b(2.0), S2 - b(2.0) - 0.05, [{"k": "seta", "de": [230, 1420], "para": [330, 1180], "curva": -40}], cor=VERM, lw=13),
      NOTA(b(2.1), S2 - b(2.1) - 0.05, "aqui: atenção", 110, 1400, w=480, tam=96, cor=VERM, rot=-4),
      NOTA(b(3.9), S2 - b(3.9) - 0.05, "usa dopamina", 560, 1400, w=420, tam=84, cor=AZUL_T, rot=3)]
# (2) No TDAH, ele responde diferente, e a atenção escapa.
c += [FR(S2 + 0.05, S3 - S2 - 0.1, "NO TDAH, A ATENÇÃO ESCAPA", tam=118),
      FS(S2 + 0.1, S3 - S2 - 0.15, [{"k": "cerebro_lado", "xy": [600, 1060], "s": 1.15, "t": 0.0}],
         fluxos=[{"de": [440, 1000], "para": [150, 760], "curva": -60, "cor": "#9aa3ad", "t": 3.0, "d": 1.8, "n": 4, "r": 13, "viagem": 0.9},
                 {"de": [440, 1080], "para": [130, 1060], "curva": 40, "cor": "#9aa3ad", "t": 3.2, "d": 1.6, "n": 4, "r": 13, "viagem": 0.9},
                 {"de": [460, 1150], "para": [180, 1380], "curva": 60, "cor": "#9aa3ad", "t": 3.4, "d": 1.4, "n": 4, "r": 13, "viagem": 0.9}]),
      NOTA(b(7.3), S3 - b(7.3) - 0.05, "responde diferente", 420, 1340, w=560, tam=88, cor=AZUL_T, rot=-3),
      NOTA(b(9.1), S3 - b(9.1) - 0.05, "escapa!", 90, 1250, w=320, tam=110, cor=VERM, rot=-8)]
# (3) O remédio faz o recado da dopamina durar mais, e a atenção fica.
c += [FR(S3 + 0.05, S4 - S3 - 0.1, "O RECADO DURA MAIS", tam=140),
      FS(S3 + 0.1, S4 - S3 - 0.15, [{"k": "neuronio", "xy": [520, 1030], "s": 1.5, "t": 0.0}],
         fluxos=[{"de": [670, 1030], "para": [740, 1030], "curva": -30, "cor": "#ffd400", "t": 1.3, "d": 3.3, "n": 8, "r": 13, "viagem": 0.9}],
         pulsos=[{"o": 0, "t": 3.4}]),
      NOTA(b(11.9), S4 - b(11.9) - 0.05, "recado da dopamina", 300, 1190, w=600, tam=88, cor="#b8860b", rot=-3),
      DS(b(13.6), S4 - b(13.6) - 0.05, [{"k": "check", "c": [540, 1400], "s": 60}], cor=VERDE_T, lw=18),
      NOTA(b(13.4), S4 - b(13.4) - 0.05, "a atenção fica", 600, 1380, w=380, tam=88, cor=VERDE_T, rot=-3)]
# (4) É como um óculos: a lousa fica nítida.
c += [FR(S4 + 0.05, S5 - S4 - 0.1, "É COMO UM ÓCULOS", tam=150),
      LOUSA(S4 + 0.2, b(17.55) - S4 - 0.2, True),
      LOUSA(b(17.55), S5 - b(17.55) - 0.05, False),
      FS(S4 + 0.6, S5 - S4 - 0.65, [{"k": "rm_oculos", "xy": [540, 1300], "s": 1.1, "t": 0.0}], pulsos=[{"o": 0, "t": 1.9}]),
      NOTA(b(17.5), S5 - b(17.5) - 0.05, "nítida!", 640, 1400, w=320, tam=110, cor=VERDE_T, rot=-5)]
# (5) Mas o óculos não sabe a matéria.
c += [FR(S5 + 0.05, AF - S5 - 0.1, "ÓCULOS NÃO SABE A MATÉRIA", tam=118),
      FS(S5 + 0.1, AF - S5 - 0.15, [{"k": "rm_oculos", "xy": [280, 1050], "s": 0.75, "t": 0.0},
                                    {"k": "cf_livro", "xy": [790, 1050], "s": 0.8, "t": 0.3, "rotulo": "MATÉRIA", "rot_y": 150}]),
      DS(b(20.1), AF - b(20.1), [{"k": "seta", "de": [440, 1050], "para": [620, 1050], "curva": -40}], cor=TINTA, lw=12),
      DS(b(20.7), AF - b(20.7), [{"k": "x", "c": [530, 1030], "s": 60}], cor=VERM, lw=16),
      NOTA(b(20.5), AF - b(20.5) - 0.02, "não ensina", 300, 1360, w=480, tam=104, cor=VERM, rot=-3)]
SFX_AULA = [{"src": "whoosh", "t": tB + 0.05, "gain": 0.4, "pico": 0.45}, {"src": "papel", "t": tB + 0.15, "gain": 0.4},
            {"src": "scratch", "t": b(2.0), "gain": 0.25}, {"src": "boing", "t": b(2.1), "gain": 0.3}, {"src": "boing", "t": b(3.9), "gain": 0.25},
            {"src": "pagina", "t": S2, "gain": 0.4}, {"src": "whoosh2", "t": b(9.0), "gain": 0.3}, {"src": "boing", "t": b(9.4), "gain": 0.3},
            {"src": "pagina", "t": S3, "gain": 0.4}, {"src": "boing", "t": b(11.9), "gain": 0.25}, {"src": "notif", "t": b(13.6), "gain": 0.3},
            {"src": "pagina", "t": S4, "gain": 0.4}, {"src": "whoosh2", "t": b(17.5), "gain": 0.3}, {"src": "boing", "t": b(17.7), "gain": 0.3},
            {"src": "pagina", "t": S5, "gain": 0.4}, {"src": "scratch", "t": b(20.1), "gain": 0.25}, {"src": "scratch", "t": b(20.7), "gain": 0.3}]

# ================= C (neutro): o estudo =================
E1, E2, E3, E4 = e(0.0), e(4.5), e(10.0), e(15.65)
c += B(P + "_viral_blur.mp4", AF, c1 - AF, 40.0)
QB = 1400   # base das barras
c += [GL(AF), FL(AF),
      {"tipo": "numero", "t": E1 + 0.05, "d": E2 - E1 - 0.1, "xy": [0, 430], "valor": 173, "tam": 330, "z": 44},
      T(E1 + 0.9, E2 - E1 - 0.95, "CRIANÇAS COM TDAH", y=900, f="130px Anton", css=SOMBRA),
      FL(E2),
      {"tipo": "checklist", "t": E2 + 0.05, "d": E3 - E2 - 0.1, "box": [120, 330, 840, 620], "titulo": "Com o remédio:", "entra": "cai",
       "itens": [{"txt": "mais tarefa feita", "t": e(5.6), "marca": e(6.6)}, {"txt": "melhor comportamento", "t": e(7.2), "marca": e(8.2)}], "z": 40},
      T(e(8.4), E3 - e(8.4) - 0.05, "TODO DIA", y=1120, f="150px Anton", cor="#3ddc84", css=SOMBRA, anim=None, entra="zoom"),
      FL(E3),
      T(E3 + 0.05, E4 - E3 - 0.1, "MATÉRIA APRENDIDA", y=330, f="140px Anton", css=SOMBRA),
      {"tipo": "desenho", "t": e(11.2), "d": E4 - e(11.2) - 0.05, "formas": [{"k": "linha", "pts": [[340, QB], [340, QB - 520]], "j": 0}], "cor": "#ffd400", "espessura": 150, "z": 44, "vel": 0.8, "fixo": True},
      {"tipo": "desenho", "t": e(13.4), "d": E4 - e(13.4) - 0.05, "formas": [{"k": "linha", "pts": [[740, QB], [740, QB - 520]], "j": 0}], "cor": "#9aa3ad", "espessura": 150, "z": 44, "vel": 0.8, "fixo": True},
      {"tipo": "texto", "t": e(11.2), "d": E4 - e(11.2) - 0.05, "xy": [140, QB + 90], "w": 400, "fonte": "700 80px Caveat", "cor": "#ffd400", "alinha": "center", "txt": "com remédio", "z": 46, "entra": "pop", "css": "text-shadow:4px 4px 0 #000"},
      {"tipo": "texto", "t": e(13.4), "d": E4 - e(13.4) - 0.05, "xy": [540, QB + 90], "w": 400, "fonte": "700 80px Caveat", "cor": "#e6eaee", "alinha": "center", "txt": "cápsula sem remédio", "z": 46, "entra": "pop", "css": "text-shadow:4px 4px 0 #000;line-height:1.0"},
      T(e(14.0), E4 - e(14.0) - 0.05, "=", y=800, f="260px Anton", cor="#ffffff", css=SOMBRA, anim=None, entra="zoom"),
      FL(E4),
      T(E4 + 0.05, c1 - E4 - 0.05, "QUEM ENSINOU FOI A AULA", y=420, f="150px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": E4 + 0.15, "d": c1 - E4 - 0.15, "z": 30, "orgaos": [{"k": "cf_livro", "xy": [540, 1150], "s": 1.3, "t": 0.0}], "pulsos": [{"o": 0, "t": 1.2}]},
      F(E1, c1 - E1, "Pelham e col., J Consult Clin Psychol 2022 · 173 crianças com TDAH, remédio x cápsula sem remédio, 3 semanas de aula")]
c[-1]["fixo"] = True

# ================= CTA (banco cta6) =================
c += [GL(c1),
      {"tipo": "video", "t": c1, "d": 4.12, "ms": 0, "src": M + "cta6.mp4", "box": [0, 0, 1080, 1920], "pos": "center 30%",
       "zoom": [[c1, 1.0, 0.01], [c1 + 2.0, 1.1, 0.3]], "z": 40},
      {"tipo": "barra", "t": c1 + 0.2, "d": 3.87, "y": 215, "txt": "AULA VALEU? SEGUE + CURTE", "cor": "#c6ff3d", "cor_txt": "#0b1512"}]

# ================= D (alegre): fecho =================
c += B(P + "_viral_blur.mp4", c2, dur - c2, 20.0)
c += [GL(c2), FL(c2),
      T(f(0.05), f(3.8) - f(0.05), "REMÉDIO: A ATENÇÃO FICA", y=420, f="150px Anton", css=SOMBRA),
      {"tipo": "fisio", "t": f(0.3), "d": f(3.8) - f(0.3), "z": 30, "orgaos": [{"k": "rm_oculos", "xy": [540, 1120], "s": 1.2, "t": 0.0}], "pulsos": [{"o": 0, "t": 1.5}]},
      FL(f(3.85)),
      {"tipo": "checklist", "t": f(3.9), "d": f(9.1) - f(3.9), "box": [120, 330, 840, 620], "titulo": "Matéria entra pelo método:", "entra": "cai",
       "itens": [{"txt": "explicar com suas palavras", "t": f(5.8), "marca": f(7.1)}, {"txt": "se testar", "t": f(7.8), "marca": f(8.3)}], "z": 40},
      FL(f(9.15)),
      {"tipo": "gigante", "t": f(9.2), "d": dur - f(9.2), "txt": "COM O SEU MÉDICO", "y": 1180, "tam": 300, "cor": "rgba(255,255,255,.14)", "x": [1000, -2700], "z": 20},
      {"tipo": "carimbo", "t": f(9.25), "d": dur - f(9.25), "xy": [110, 700], "txt": "TRATAMENTO: COM O MÉDICO", "tam": 80, "rot": -6, "z": 60,
       "cor": "#ff2d3d", "blend": "normal", "css": "background:rgba(255,255,255,.9)"},
      F(c2, dur - c2, "Pelham e col., J Consult Clin Psychol 2022 · doi 10.1037/ccp0000725")]

voz = [{"src": M + "rm_viral_bip.wav", "t": 0, "ms": 0, "d": vd, "palavras": M + "rm_viral.words.json"},
       {"src": M + "rm_rosto.mp4", "t": vd, "ms": 0, "d": round(r1 - vd, 2), "palavras": M + "rm_rosto.words.json"},
       {"src": M + "rm_a_voz.wav", "t": tA, "ms": 0, "d": DA, "palavras": M + "rm_a_voz.words.json"},
       {"src": M + "rm_b_voz.wav", "t": tB, "ms": 0, "d": DB, "palavras": M + "rm_b_voz.words.json"},
       {"src": M + "rm_c_voz.wav", "t": tC, "ms": 0, "d": DC, "palavras": M + "rm_c_voz.words.json"},
       {"src": M + "cta6.mp4", "t": c1, "ms": 0, "d": 4.12, "palavras": M + "cta6.mp4.words.json"},
       {"src": M + "rm_d_voz.wav", "t": c2, "ms": 0, "d": DD, "palavras": M + "rm_d_voz.words.json"}]
sfx = [{"src": "whoosh", "t": 0, "gain": 0.6, "pico": 0.45}, {"src": "notif", "t": 0.15, "gain": 0.5},
       {"src": "boing", "t": 3.3, "gain": 0.4}, {"src": "pagina", "t": 4.3, "gain": 0.35},
       {"src": "glitch", "t": vd - 0.05, "gain": 0.5}, {"src": "boom", "t": vd + 0.45, "gain": 0.45, "pico": 0.3, "d": 1.2},
       {"src": "glitch", "t": r1 - 0.05, "gain": 0.45}, {"src": "whoosh", "t": a(0.1), "gain": 0.4, "pico": 0.45},
       {"src": "whoosh2", "t": a(2.6), "gain": 0.35}, {"src": "notif", "t": a(3.3), "gain": 0.3}, {"src": "whoosh2", "t": a(5.05), "gain": 0.35},
       {"src": "whoosh", "t": a(7.65), "gain": 0.4, "pico": 0.45},
       {"src": "glitch", "t": tB - 0.05, "gain": 0.45}, *SFX_AULA,
       {"src": "glitch", "t": AF - 0.05, "gain": 0.45}, {"src": "boom", "t": E1 + 0.05, "gain": 0.5, "pico": 0.3, "d": 1.5},
       {"src": "papel", "t": E2 + 0.05, "gain": 0.45}, {"src": "notif", "t": e(6.6), "gain": 0.3}, {"src": "notif", "t": e(8.2), "gain": 0.3},
       {"src": "whoosh2", "t": E3, "gain": 0.35}, {"src": "riser", "t": e(11.2), "gain": 0.2, "d": 1.5}, {"src": "boing", "t": e(14.0), "gain": 0.35},
       {"src": "whoosh", "t": E4, "gain": 0.4, "pico": 0.45},
       {"src": "glitch", "t": c1 - 0.05, "gain": 0.45}, {"src": "notif", "t": c1 + 0.2, "gain": 0.4},
       {"src": "glitch", "t": c2 - 0.05, "gain": 0.45}, {"src": "papel", "t": f(3.9), "gain": 0.45},
       {"src": "notif", "t": f(7.1), "gain": 0.3}, {"src": "notif", "t": f(8.3), "gain": 0.3}, {"src": "boom", "t": f(9.25), "gain": 0.5, "pico": 0.3, "d": 1.5}]
salvar(PID, dur, 151, c, voz, sfx, {"r1_fim": r1, "esconde": [], "ys": [[0, 4.0, 1720], [4.0, vd, 1440], [vd, r1, 1000], [r1, dur, 1730]]})
p = json.load(open(f'planos/{PID}.json'))
p['audio']['musica'] = [{"src": "m_investiga", "t": r1 - 0.3, "d": round(c1 - r1 + 0.5, 2), "gain": 0.14, "fade": 0.8},
                        {"src": "m_emocao", "t": c2 - 0.2, "d": round(dur - c2 + 0.2, 2), "gain": 0.14, "fade": 0.8}]
json.dump(p, open(f'planos/{PID}.json', 'w'), ensure_ascii=False, indent=1)
print("ok dur", dur, "r1", r1, "tA", tA, "tB", tB, "AF", AF, "tC", tC, "c1", c1, "c2", c2)
