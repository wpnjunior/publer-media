# pele.py <plano_id> <lab|dossie|noticia>
# Troca a "pele" da narração para o mesmo perfil não ver dois reacts iguais seguidos (Wagner, 13/11 22h02).
# lab = escuro com grade (padrão). dossie = papel, tinta escura, legenda de máquina. noticia = vinho, legenda pílula, faixa de checagem.
import json, sys
pid, pele = sys.argv[1], sys.argv[2]
p = json.load(open(f'planos/{pid}.json'))
C = p['camadas']
# janelas em que o fundo é o viral borrado (narração)
jan = [(c['t'], c['t'] + c['d']) for c in C if c.get('tipo') == 'video' and '_viral_blur' in c.get('src', '')]
def na_narr(c): return any(a - 0.05 <= c.get('t', -1) < b for a, b in jan)
if pele == 'dossie':
    p['fundo'] = '#e9dcbc'
    TINTA, VERM = '#1c1a17', '#b3121f'
    for c in C:
        t = c.get('tipo')
        if t == 'fundo' and c.get('textura') == 'grade':
            c['textura'] = 'papel'; c['cor'] = '#efe4c9'
        elif t == 'fundo' and c.get('cor') == 'rgba(6,14,11,.5)':
            c['cor'] = 'rgba(239,228,201,.68)'
        elif t == 'texto' and na_narr(c):
            if c.get('cor', '#ffffff').lower() in ('#ffffff', '#fff'): c['cor'] = TINTA
            elif c.get('cor', '').lower() in ('#3ddc84', '#c6ff3d'): c['cor'] = VERM
            css = c.get('css', '')
            c['css'] = 'text-shadow:5px 5px 0 rgba(0,0,0,.14)' if 'text-shadow' in css else css
        elif t == 'numero':
            if c.get('cor') in (None, '#ffd400', '#f2c230'): c['cor'] = VERM; c['sombra'] = '#d9c49a'
            c['cor_rotulo'] = TINTA; c['sombra_rotulo'] = 'none'
        elif t == 'gigante':
            c['cor'] = '#c9b48a' if c.get('cor') in (None, '#c6ff3d') else c['cor']
        elif t == 'desenho' and na_narr(c):
            c['cor'] = VERM
        elif t == 'grao':
            c['op'] = 0.12
    p['legenda']['estilo'] = 'maquina'
elif pele == 'noticia':
    p['fundo'] = '#14070a'
    for c in C:
        t = c.get('tipo')
        if t == 'fundo' and c.get('textura') == 'grade':
            c['textura'] = 'gradiente'; c['cor'] = '#14070a'; c['cor2'] = '#5a0d10'
        elif t == 'fundo' and c.get('cor') == 'rgba(6,14,11,.5)':
            c['cor'] = 'rgba(24,5,9,.62)'
        elif t == 'texto' and c.get('cor', '').lower() in ('#3ddc84', '#c6ff3d'):
            c['cor'] = '#ffd400'
        elif t == 'gigante' and c.get('cor') in (None, '#c6ff3d'):
            c['cor'] = '#ffd400'
        elif t == 'desenho' and c.get('cor') in (None, '#c6ff3d'):
            c['cor'] = '#ffd400'
    p['legenda']['estilo'] = 'pilula'
    for a, b in jan:
        C.append({"tipo": "texto", "t": round(a + 0.3, 3), "d": round(b - a - 0.3, 3), "xy": [40, 128], "w": 1000,
                  "fonte": "900 34px Montserrat", "cor": "#ffffff", "alinha": "center", "txt": "● CHECAGEM · O QUE A CIÊNCIA DIZ",
                  "css": "letter-spacing:3px;background:#ff2d3d;border-radius:14px;padding:12px 0", "z": 69, "entra": "desliza"})
json.dump(p, open(f'planos/{pid}.json', 'w'), ensure_ascii=False, indent=1)
print('pele', pele, pid, 'janelas', [(round(a, 1), round(b, 1)) for a, b in jan])
