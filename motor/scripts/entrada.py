# entrada.py <plano_id> <rosto_entrada.mp4> <palavras.json> <dur> <manchete> <sub> [jornal]
# Molde aprovado pelo Wagner (13/11 22h03): o clone do perfil diz "Olha só essa notícia" com a
# manchete por cima (gancho do 1º segundo) e logo entra o viral com a voz original.
# Empurra todo o plano para frente em <dur> segundos e prepende a entrada.
import json, sys
pid, src, pal, E, txt, sub = sys.argv[1:7]
jornal = sys.argv[7] if len(sys.argv) > 7 else "Plantão das Redes"
E = float(E)
p = json.load(open(f'planos/{pid}.json'))
def sh(v): return round(v + E, 3)
for c in p['camadas']:
    if c.get('tipo') == 'fundo' and c.get('t', 0) == 0 and c.get('textura') and c.get('z') is None:
        c['d'] = sh(c['d']); continue
    if 't' in c: c['t'] = sh(c['t'])
    for k in ('t_escolha',):
        if k in c: c[k] = sh(c[k])
    for it in c.get('itens', []):
        if 't' in it: it['t'] = sh(it['t'])
        if 'marca' in it: it['marca'] = sh(it['marca'])
    for ln in c.get('linhas', []):
        if isinstance(ln.get('grifo'), (int, float)) and not isinstance(ln.get('grifo'), bool): ln['grifo'] = sh(ln['grifo'])
    if 'zoom' in c: c['zoom'] = [[sh(z[0])] + z[1:] for z in c['zoom']]
    for pn in c.get('pinos', []):
        if 't' in pn: pn['t'] = sh(pn['t'])
    for nt in c.get('notif', []):
        if 't' in nt: nt['t'] = sh(nt['t'])
    for f in c.get('formas', []):
        if 't' in f and c.get('tipo') != 'desenho': f['t'] = sh(f['t'])
    if 'camera' in c and c.get('tipo') == 'mapa': c['camera'] = [[sh(k[0])] + k[1:] for k in c['camera']]
for k in ('voz', 'sfx', 'viral', 'musica'):
    for a in p['audio'].get(k, []) or []:
        if 't' in a: a['t'] = sh(a['t'])
lg = p.get('legenda', {})
lg['esconde'] = [[0, round(E, 3)]] + [[sh(a), sh(b)] for a, b in lg.get('esconde', [])]
lg['ys'] = [[sh(a), sh(b), y] for a, b, y in lg.get('ys', [])]
p['dur'] = sh(p['dur'])
for c in p['camadas']:
    if c.get('tipo') in ('progresso', 'vinheta', 'grao'): continue
nova = [
    {"tipo": "video", "t": 0, "d": E, "ms": 0, "src": src, "box": [0, 0, 1080, 1920], "pos": "center 30%", "zoom": [[0, 1.12, E]], "z": 30},
    {"tipo": "manchete", "t": 0.12, "d": round(E - 0.12, 3), "xy": [50, 235], "w": 980, "jornal": jornal, "data": "nov 2026", "txt": txt, "sub": sub, "rot": -3, "z": 40},
    {"tipo": "flash", "t": round(E, 3), "d": 0.25},
]
p['camadas'] = p['camadas'][:1] + nova + p['camadas'][1:]
p['audio']['voz'] = [{"src": src, "t": 0, "ms": 0, "d": E, "palavras": pal}] + p['audio']['voz']
p['audio']['sfx'] = [{"src": "notif", "t": 0.15, "gain": 0.7}, {"src": "pagina", "t": 0.2, "gain": 0.45}] + \
    [s for s in p['audio']['sfx'] if not (s['src'] == 'notif' and abs(s['t'] - (E + 0.15)) < 0.01)]
json.dump(p, open(f'planos/{pid}.json', 'w'), ensure_ascii=False, indent=1)
print('entrada ok', pid, 'dur', p['dur'])
