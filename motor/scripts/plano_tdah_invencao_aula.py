import sys, json, copy; sys.path.insert(0, 'scripts')
from mk import B, T, F, M
# Remake com aula (14/11): react "TDAH é invenção / doença fictícia" (TDAH 18/11 21h06).
# Roteiro: /mnt/project-files/reacts/remakes/tdah-invencao.md
# Parte do plano atual (já com entrada td_entB e pele lab aplicadas), NÃO o sobrescreve:
#  - corta "Laboratório nenhum vende gene, né?" (16,62-18,58 de ti_voz) e a cartela dela;
#  - manchete e caixinha passam a "doença fictícia" (o corte não fala de indústria);
#  - aula nova do "porteiro" (ti_aula_voz) entre o bloco B (1775) e o bloco C (37 estudos de gêmeos).
src = json.load(open('planos/react_tdah_invencao.json'))
p = copy.deepcopy(src)
p['id'] = 'react_tdah_invencao_aula'

VA = 19.83                 # ti_aula_voz.wav (25,79 s brutos / 1,3)
Da = 20.05                 # aula = voz + respiro antes do "Olha só" do bloco C
t0 = 22.997                # fim do bloco B (ti_voz 3,55 -> 10,65 em 15,897)
tC = round(t0 + Da, 3)     # bloco C (ti_voz 10,68 -> 16,62)
tE = round(tC + 5.94, 3)   # bloco E (ti_voz 18,58 -> 24,60)
tF = round(tE + 6.02, 3)   # CTA com rosto (ti_voz 25,10)
sC = tC - 23.027           # deslocamentos em relação ao plano atual
sE = tE - 30.927
sF = tF - 36.817
dur = round(src['dur'] + sF, 3)
a = lambda v: round(t0 + v, 3)   # tempo relativo ao início da aula
SOMBRA = "text-shadow:6px 6px 0 #000,0 0 18px rgba(0,0,0,.8)"

def BR(arq, t, d, ms=0.3, veu=.6):
    z = [[round(t, 3), 1.04, 0.01], [round(t + d, 3), 1.14, round(d, 3)]]
    return [{"tipo": "video", "t": round(t, 3), "d": round(d, 3), "ms": ms, "src": M + arq, "box": [0, 0, 1080, 1920], "pos": "center", "respira": False, "z": 10, "zoom": z},
            {"tipo": "fundo", "t": round(t, 3), "d": round(d, 3), "cor": f"rgba(6,14,11,{veu})", "z": 11}]
def TT(t, d, txt, y=230, f="100px Anton", cor="#ffffff", **k):
    return T(t, d, txt, y=y, f=f, cor=cor, css=SOMBRA, vel=0.09, **k)
def desloca(t):
    if t < t0 - 0.001: return 0.0
    if t < 28.967: return sC
    if t < 30.9: return None          # trecho cortado
    if t < 36.76: return sE
    return sF

# ---------- camadas do plano atual ----------
novas = []
for c in p['camadas']:
    tp, t = c.get('tipo'), c.get('t', 0)
    if tp in ('progresso', 'vinheta', 'grao'): continue
    if tp == 'fundo' and c.get('textura') == 'grade':
        c['d'] = dur; novas.append(c); continue
    if '_viral_blur' in c.get('src', '') and abs(t - 15.897) < 0.01: continue        # refeito abaixo em 2 trechos
    if tp == 'fundo' and c.get('cor') == 'rgba(6,14,11,.5)' and abs(t - 15.897) < 0.01: continue
    if c.get('txt') == 'LABORATÓRIO NENHUM VENDE GENE': continue
    if tp == 'manchete':
        c['txt'] = '“TDAH É DOENÇA FICTÍCIA”?'
    if tp == 'desenho' and abs(t - 21.847) < 0.01:
        c['formas'] = [{"k": "sublinhado", "de": [220, 812], "ate": 850}]   # em 612 riscava a 1ª linha de "EM 1775 JÁ SE DESCREVIA"
    if tp == 'pergunta':
        c['txt'] = 'TDAH é doença fictícia?'
    s = desloca(t)
    if s is None:
        print('fora (trecho cortado):', tp, t, c.get('txt', '')); continue
    if s == 0 and t + c.get('d', 0) > t0 + 0.001 and c.get('d'):
        c['d'] = round(t0 - t, 3)      # nada do bloco B invade a aula
    if s:
        c['t'] = round(t + s, 3)
        if 'zoom' in c: c['zoom'] = [[round(z[0] + s, 3)] + z[1:] for z in c['zoom']]
    novas.append(c)

# fundo borrado do viral nos blocos B e E (como no plano atual)
novas += B('ti_viral_blur.mp4', 15.897, round(t0 - 15.897, 3), 0.5)
novas += B('ti_viral_blur.mp4', tE, round(tF - tE, 3), 15.5)

# ---------- AULA: o porteiro do cérebro ----------
aula = []
aula += [{"tipo": "glitch", "t": round(t0 - 0.05, 3), "d": 0.25}, {"tipo": "flash", "t": t0, "d": 0.2, "max": 0.6}]
aula += BR('ti_br_hotel.mp4', t0, 5.95, 0.3)                      # cenas 1-2: portaria de hotel
aula += BR('ti_br_porta.mp4', a(5.95), 4.8, 0.2)                   # cenas 3-4: porta com chave
aula += BR('ti_br_multidao.mp4', a(10.75), 2.9, 0.3)              # cena 5: multidão no cruzamento
aula += BR('ti_br_rua.mp4', a(13.65), 4.8, 0.4)                   # cena 6: gente andando
aula += BR('ti_br_dna.mp4', a(18.45), round(tE - a(18.45), 3), 0.3, .76)  # cena 7 + bloco C: médico, tela com DNA
CER, POR = [540, 640], [540, 1100]
O = {"TAREFA": (200, 1340), "BARULHO": (820, 1340), "CELULAR": (430, 1460), "IDEIA NOVA": (640, 1460)}   # de onde saem os fluxos
aula += [{"tipo": "fisio", "t": t0, "d": round(Da, 3), "z": 30,
          "orgaos": [{"k": "cerebro_lado", "xy": CER, "s": .85, "t": 2.75, "rotulo": "CÉREBRO", "rot_y": 200},
                     {"k": "porteiro", "xy": POR, "s": .8, "t": 4.6, "rotulo": "PORTEIRO", "rot_y": -185}],
          "fluxos": [
              # cena 3: a tarefa passa pelo porteiro e chega na frente do cérebro; o resto espera
              {"de": list(O["TAREFA"]), "para": [490, 1235], "curva": -40, "cor": "#3ddc84", "t": 6.4, "d": 3.4, "n": 6, "viagem": 0.9},
              {"de": [560, 965], "para": [445, 680], "curva": -20, "cor": "#3ddc84", "t": 7.2, "d": 2.8, "n": 6, "viagem": 0.8},
              {"de": list(O["BARULHO"]), "para": [600, 1235], "curva": -40, "cor": "#ffffff", "t": 6.8, "d": 3.2, "n": 3, "viagem": 1.0},
              {"de": list(O["CELULAR"]), "para": [520, 1240], "curva": -20, "cor": "#4dd8ff", "t": 7.0, "d": 3.0, "n": 3, "viagem": 1.0},
              {"de": list(O["IDEIA NOVA"]), "para": [570, 1240], "curva": -20, "cor": "#ffd400", "t": 7.2, "d": 2.8, "n": 3, "viagem": 1.0},
              # cena 4: mensageiro (dopamina) do porteiro para a frente do cérebro
              {"de": [560, 965], "para": [450, 690], "curva": -20, "cor": "#ffd400", "t": 8.7, "d": 2.1, "n": 5, "viagem": 0.8, "r": 15},
              # cenas 5-6: no TDAH o porteiro libera tudo de uma vez
              {"de": list(O["TAREFA"]), "para": [440, 680], "curva": -60, "cor": "#3ddc84", "t": 13.2, "d": 5.0, "n": 7, "viagem": 0.8},
              {"de": list(O["BARULHO"]), "para": [480, 600], "curva": -60, "cor": "#ffffff", "t": 13.25, "d": 5.0, "n": 7, "viagem": 0.8},
              {"de": list(O["CELULAR"]), "para": [455, 630], "curva": -40, "cor": "#4dd8ff", "t": 13.3, "d": 5.0, "n": 7, "viagem": 0.8},
              {"de": list(O["IDEIA NOVA"]), "para": [470, 700], "curva": -40, "cor": "#ffd400", "t": 13.35, "d": 5.0, "n": 7, "viagem": 0.8}],
          "pulsos": [{"o": 0, "t": 3.6}, {"o": 1, "t": 7.4}, {"o": 0, "t": 9.9}, {"o": 1, "t": 12.4}, {"o": 1, "t": 13.8},
                     {"o": 0, "t": 14.6}, {"o": 0, "t": 15.9}, {"o": 0, "t": 16.9}, {"o": 0, "t": 17.9}, {"o": 0, "t": 19.2}]}]
# as quatro coisas que chegam no porteiro (2 fileiras desencontradas; os fluxos de baixo sobem pelo vão)
for txt, cx, y, cor, te in [("TAREFA", 200, 1345, "#3ddc84", 6.0), ("BARULHO", 820, 1345, "#ffffff", 6.3),
                            ("CELULAR", 300, 1465, "#4dd8ff", 6.6), ("IDEIA NOVA", 790, 1465, "#ffd400", 6.9)]:
    aula.append({"tipo": "texto", "t": a(te), "d": round(18.45 - te, 3), "xy": [cx - 230, y], "w": 460, "fonte": "100px Anton", "cor": cor,
                 "alinha": "center", "txt": txt, "z": 41, "entra": "zoom", "css": SOMBRA})
aula += [{"tipo": "texto", "t": a(8.75), "d": 2.1, "xy": [600, 820], "w": 450, "fonte": "100px Anton", "cor": "#ffd400", "alinha": "right",
          "txt": "DOPAMINA", "z": 41, "entra": "zoom", "css": SOMBRA}]
aula += [TT(a(0.05), 2.6, "DOENÇA FICTÍCIA?", f="120px Anton", cor="#f2c230"),
         TT(a(2.7), 3.2, "O PORTEIRO DO CÉREBRO"),
         TT(a(5.95), 2.25, "DECIDE O QUE ENTRA", cor="#3ddc84"),
         TT(a(8.2), 2.55, "MENSAGEIRO: DOPAMINA", cor="#ffd400"),
         TT(a(10.75), 2.9, "NO TDAH, RESPONDE DIFERENTE", cor="#4dd8ff"),
         TT(a(13.65), 4.8, "ENTRA TUDO DE UMA VEZ", cor="#ff5a5f"),
         TT(a(18.45), round(tC + 0.84 - a(18.45), 3), "DE ONDE VEM?", f="120px Anton", cor="#f2c230"),
         {"tipo": "texto", "t": a(10.8), "d": 7.6, "xy": [40, 1262], "w": 1000, "fonte": "600 28px Montserrat", "cor": "#ffffff", "alinha": "center",
          "txt": "Cortese et al., Am J Psychiatry 2012 · 55 estudos de imagem", "z": 70, "css": "text-shadow:0 2px 6px #000"},
         {"tipo": "flash", "t": a(5.95), "d": 0.2, "max": 0.4}, {"tipo": "flash", "t": a(10.75), "d": 0.2, "max": 0.4},
         {"tipo": "flash", "t": tC, "d": 0.2, "max": 0.4}]
for L in aula:
    L['fixo'] = True
novas += aula
p['camadas'] = novas + [{"tipo": "progresso"}, {"tipo": "vinheta"}, {"tipo": "grao", "op": 0.07}]
p['dur'] = dur

# ---------- áudio ----------
V = M + 'ti_voz.wav'; W = M + 'ti_voz.words.json'
voz = [v for v in src['audio']['voz'] if 'ti_voz' not in v['src']]   # entrada + viral
voz += [{"src": V, "t": 12.897, "ms": 0, "d": 3.0, "palavras": W},                       # A (rosto)
        {"src": V, "t": 15.897, "ms": 3.55, "d": 7.1, "palavras": W},                    # B
        {"src": M + 'ti_aula_voz.wav', "t": t0, "ms": 0, "d": VA, "palavras": M + 'ti_aula_voz.words.json'},  # AULA
        {"src": V, "t": tC, "ms": 10.68, "d": 5.94, "palavras": W},                      # C
        {"src": V, "t": tE, "ms": 18.58, "d": 6.02, "palavras": W},                      # E
        {"src": V, "t": tF, "ms": 25.10, "d": 5.45, "palavras": W},                      # F (CTA)
        {"src": V, "t": round(tF + 5.45, 3), "ms": 31.15, "d": 6.9, "palavras": W}]  # G
sfx = []
for s in src['audio']['sfx']:
    if abs(s['t'] - 28.517) < 0.01: continue          # whoosh da cartela cortada
    d = desloca(s['t'] + 0.05)
    if d is None: continue
    s = dict(s); s['t'] = round(s['t'] + d, 3); sfx.append(s)
sfx += [{"src": "whoosh", "t": t0, "gain": 0.5, "pico": 0.45}, {"src": "boing", "t": a(2.75), "gain": 0.3}, {"src": "boing", "t": a(4.6), "gain": 0.3},
        {"src": "whoosh2", "t": a(5.95), "gain": 0.35}, {"src": "pagina", "t": a(6.0), "gain": 0.25},
        {"src": "whoosh2", "t": a(8.2), "gain": 0.3}, {"src": "whoosh2", "t": a(10.75), "gain": 0.35},
        {"src": "riser", "t": a(13.3), "gain": 0.22, "d": 4.8}, {"src": "whoosh", "t": a(18.45), "gain": 0.4, "pico": 0.45},
        {"src": "whoosh2", "t": tC, "gain": 0.3}]
p['audio'] = {"voz": voz, "musica": [{"src": "m_investiga", "t": t0, "ms": 0, "d": round(Da + 0.3, 3), "gain": 0.32, "fade": 0.8}], "sfx": sfx}

# ---------- legenda ----------
LG = p['legenda']
LG['ys'] = [[6.667, 12.897, 1430], [12.897, 15.897, 1000], [t0, tC, 1730]]
json.dump(p, open(f"planos/{p['id']}.json", 'w'), ensure_ascii=False, indent=1)
print('ok', p['id'], 'dur', dur, 't0', t0, 'tC', tC, 'tE', tE, 'tF', tF)
