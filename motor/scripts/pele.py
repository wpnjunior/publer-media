# pele.py <plano_id> <lab|dossie|noticia|lousa> [PALAVRA]
# Troca a "pele" da narração para o mesmo perfil não ver dois reacts iguais seguidos (Wagner, 13/11 22h02).
# lab = escuro com grade (padrão). dossie = papel, tinta escura, legenda de máquina. noticia = vinho, legenda pílula, faixa de checagem.
import json, sys
pid, pele = sys.argv[1], sys.argv[2]
palavra = sys.argv[3] if len(sys.argv) > 3 else None  # palavra gigante para viral de pouco movimento
p = json.load(open(f'planos/{pid}.json'))
C = p['camadas']
# janelas em que o fundo é o viral borrado (narração)
jan = [(c['t'], c['t'] + c['d']) for c in C if c.get('tipo') == 'video' and '_viral_blur' in c.get('src', '')]
def na_narr(c): return any(a - 0.05 <= c.get('t', -1) < b for a, b in jan)
if pele == 'dossie':
    p['fundo'] = '#e9dcbc'
    TINTA, VERM = '#1c1a17', '#b3121f'
    for c in C:
        if c.get('fixo'): continue
        t = c.get('tipo')
        if t == 'fundo' and c.get('textura') == 'grade':
            c['textura'] = 'papel'; c['cor'] = '#efe4c9'
        elif t == 'fundo' and c.get('cor') == 'rgba(6,14,11,.5)':
            c['cor'] = 'rgba(239,228,201,.5)'
        elif t == 'texto' and na_narr(c):
            if c.get('cor', '#ffffff').lower() in ('#ffffff', '#fff'): c['cor'] = TINTA
            elif c.get('cor', '').lower() in ('#3ddc84', '#c6ff3d'): c['cor'] = VERM
            css = c.get('css', '')
            c['css'] = 'text-shadow:5px 5px 0 rgba(0,0,0,.14)' if 'text-shadow' in css else css
        elif t == 'texto' and c.get('cor', '').lower() in ('#3ddc84', '#c6ff3d'):
            # fora da narração também: verde-limão some no papel creme (Mel 14/11: "podcast, jan/2025" ilegível)
            c['cor'] = VERM
        elif t == 'numero':
            if c.get('cor') in (None, '#ffd400', '#f2c230'): c['cor'] = VERM; c['sombra'] = '#d9c49a'
            c['cor_rotulo'] = TINTA; c['sombra_rotulo'] = 'none'
        elif t == 'gigante':
            c['cor'] = '#c9b48a' if c.get('cor') in (None, '#c6ff3d') else c['cor']
        elif t == 'desenho' and na_narr(c):
            c['cor'] = VERM
        elif t == 'grao':
            c['op'] = 0.2
    p['legenda']['estilo'] = 'maquina'
elif pele == 'noticia':
    p['fundo'] = '#14070a'
    for c in C:
        if c.get('fixo'): continue
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
elif pele == 'lousa':
    # quarta edição (Wagner pediu 4 edições de react, 14/11): lousa verde, tudo em giz, legenda manuscrita.
    p['fundo'] = '#16261f'
    GIZ, AMAR, ROSA = '#f4f1e8', '#ffe27a', '#ff9fb4'
    for c in C:
        if c.get('fixo'): continue
        t = c.get('tipo')
        if t == 'fundo' and c.get('textura') == 'grade':
            c['textura'] = 'lousa'; c['cor'] = '#22392f'
        elif t == 'fundo' and c.get('cor') == 'rgba(6,14,11,.5)':
            c['cor'] = 'rgba(28,50,40,.7)'
        elif t == 'texto' and na_narr(c):
            cor = c.get('cor', '#ffffff').lower()
            if cor in ('#ffffff', '#fff'): c['cor'] = GIZ
            elif cor in ('#3ddc84', '#c6ff3d'): c['cor'] = AMAR
            elif cor in ('#ff2d3d', '#ff3b3b'): c['cor'] = ROSA
            css = c.get('css', '')
            if 'background' not in css:
                c['css'] = 'text-shadow:0 0 3px rgba(255,255,255,.45),3px 4px 0 rgba(0,0,0,.28)'
        elif t == 'numero':
            c['cor'] = AMAR; c['sombra'] = '#0e1a14'
            c['cor_rotulo'] = GIZ; c['sombra_rotulo'] = 'none'
        elif t == 'gigante':
            c['cor'] = 'rgba(244,241,232,.10)' if c.get('cor') in (None, '#c6ff3d') else c['cor']
        elif t == 'desenho' and c.get('cor') in (None, '#c6ff3d', '#ffd400'):
            c['cor'] = GIZ
    p['legenda']['estilo'] = 'manuscrita'
# viral de pouco movimento (rosto parado, câmera fixa): o borrado vira quadro parado (superpoder reprovou 15-16%).
# Troca o pulso com pausa por uma respiração contínua, sem trecho parado.
import subprocess
def pouco_movimento(src):
    try:
        out = subprocess.run(["ffmpeg", "-nostats", "-i", src, "-t", "20", "-vf", "scale=180:-2,fps=10,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
        ys = [float(l.split("=")[1]) for l in out.splitlines() if "YAVG=" in l]
        return ys and sum(1 for y in ys if y < 1.0) / len(ys) > 0.4
    except Exception:
        return False
for c in C:
    if c.get('tipo') == 'video' and '_viral_blur' in c.get('src', '') and pouco_movimento(c['src']):
        t0, d = c['t'], c['d']
        ks, k, alto = [[t0, 1.04, 0.01]], 0.05, True
        while k < d - 0.2:
            ks.append([round(t0 + k, 3), 1.16 if alto else 1.04, round(min(0.9, d - k), 3)]); k += 0.9; alto = not alto
        c['zoom'] = ks
        print('respiração contínua no borrado', c['src'], t0)
        # e uma palavra gigante cruzando a tela atrás das cartelas (movimento contínuo que o borrado não dá)
        if palavra:
            cor = {'dossie': '#c9a86a', 'noticia': '#4a1016', 'lab': '#16352a', 'lousa': 'rgba(244,241,232,.12)'}.get(pele, '#c9a86a')
            C.append({"tipo": "gigante", "t": round(t0, 3), "d": round(d, 3), "txt": palavra, "y": 980, "tam": 430,
                      "cor": cor, "x": [700, -int(len(palavra) * 215)], "z": 12})
json.dump(p, open(f'planos/{pid}.json', 'w'), ensure_ascii=False, indent=1)
print('pele', pele, pid, 'janelas', [(round(a, 1), round(b, 1)) for a, b in jan])
