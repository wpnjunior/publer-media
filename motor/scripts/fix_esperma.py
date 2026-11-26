import json, sys
sys.path.insert(0, 'scripts')
from mk import T, F
d = json.load(open('planos/react_esperma.v1.json'))
C = d['camadas']
tira = set(range(15, 34)) | {39, 40, 41, 43, 44, 45}
C = [c for i, c in enumerate(C) if i not in tira]
DUR = 44.6
d['dur'] = DUR
for c in C:
    if c.get('tipo') == 'fundo' and c.get('t') == 0: c['d'] = DUR
    if c.get('t') == 35.25 and c.get('tipo') in ('video', 'fundo'): c['d'] = round(DUR - 35.25, 2)
SH = "text-shadow:8px 8px 0 #000"
novas = [
 T(10.5, 2.75, "ELES ACERTAM:", y=380, f="160px Anton", cor="#3ddc84", anim=None, entra="zoom", css=SH),
 T(11.05, 2.2, "NÃO PRECISA", y=620, f="180px Anton", cor="#ffffff", anim=None, entra="zoom", css=SH),
 T(13.3, 3.45, "EM 1 MINUTO JÁ CHEGA LÁ", y=440, f="150px Anton", vel=0.12),
 F(13.3, 7.6, "Kunz et al., Hum Reprod 1996 (teste com partículas do tamanho do espermatozoide)"),
 T(16.8, 4.1, "O CAMINHO É RÁPIDO", y=520, f="170px Anton", cor="#f2c230", anim=None, entra="zoom", css=SH),
 T(20.95, 3.8, "SAEM MILHÕES", y=420, f="170px Anton", vel=0.12),
 T(22.65, 2.1, "CHEGAM POUCOS", y=760, f="170px Anton", cor="#f2c230", anim=None, entra="zoom", css=SH),
 T(24.8, 1.8, "ESCORRER É NORMAL", y=520, f="170px Anton", cor="#3ddc84", anim=None, entra="zoom", css=SH),
 T(26.6, 4.3, "PERNAS PARA CIMA?", y=380, f="160px Anton", vel=0.12),
 T(28.0, 2.9, "NÃO PROVOU AJUDAR", y=760, f="160px Anton", cor="#ff2d3d", anim=None, entra="zoom", css="text-shadow:8px 8px 0 #5a0d10"),
 F(28.0, 2.9, "Cordary et al. 2017: 4 estudos, 1.361 casais"),
 T(35.35, 3.85, "1 ANO TENTANDO?", y=380, f="170px Anton", vel=0.12),
 T(36.85, 2.35, "+35 ANOS: 6 MESES", y=760, f="150px Anton", cor="#f2c230", anim=None, entra="zoom", css=SH),
 T(39.2, 2.3, "CONSULTA PARA OS DOIS", y=520, f="160px Anton", cor="#3ddc84", anim=None, entra="zoom", css=SH),
 T(41.5, DUR - 41.5, "O QUE IMPORTA NÃO ESCORRE", y=420, f="140px Anton", vel=0.12),
 T(42.45, DUR - 42.45, "JÁ SUBIU.", y=900, f="210px Anton", cor="#f2c230", anim=None, entra="zoom", css=SH),
 F(41.5, DUR - 41.5, "Kunz et al., Hum Reprod 1996 · doi 10.1093/humrep/11.3.627 · Cordary et al. 2017 · ACOG 2019"),
]
# entra antes de progresso/vinheta/grao
fim = [c for c in C if c.get('tipo') in ('progresso', 'vinheta', 'grao')]
C = [c for c in C if c not in fim] + novas + fim
d['camadas'] = C
d['audio']['sfx'] = [s for s in d['audio']['sfx'] if s['t'] < 10.45 or s['src'] == 'glitch' or s['t'] in (10.45, 31.15)] + [
 {"src": "boing", "t": 11.05, "gain": 0.35}, {"src": "whoosh2", "t": 13.3, "gain": 0.4}, {"src": "boom", "t": 16.8, "gain": 0.5, "pico": 0.3, "d": 1.2},
 {"src": "whoosh2", "t": 20.95, "gain": 0.4}, {"src": "boing", "t": 22.65, "gain": 0.35}, {"src": "whoosh2", "t": 24.8, "gain": 0.4},
 {"src": "whoosh2", "t": 26.6, "gain": 0.4}, {"src": "boom", "t": 28.0, "gain": 0.6, "pico": 0.3, "d": 1.5}, {"src": "whoosh2", "t": 35.35, "gain": 0.4},
 {"src": "boing", "t": 36.85, "gain": 0.35}, {"src": "whoosh", "t": 39.2, "gain": 0.5, "pico": 0.45}, {"src": "whoosh2", "t": 41.5, "gain": 0.4},
 {"src": "boom", "t": 42.45, "gain": 0.6, "pico": 0.3, "d": 1.3}]
json.dump(d, open('planos/react_esperma.json', 'w'), ensure_ascii=False, indent=1)
print('ok')
