# audio_plano.py planos/X.json - portão de áudio do PLANO, antes do render (Wagner, 13/11 23h30: "no vídeo da Ivete ele falha a voz").
# Causa do erro: o nome do remédio foi apagado do viral com silêncio digital (0,8 s) e a voz pareceu falhar.
# Mesmo erro escondido em outros dois: música do viral cortada deixou 2 s mudos no começo (café, esperma).
# Reprova: (1) trecho de voz/viral com silêncio digital >= 0,25 s no meio (palavra apagada: usar bip);
#          (2) buraco >= 0,9 s sem nenhuma voz nem efeito cobrindo (viral só de texto: pôr teclado/riser).
import json, struct, subprocess, sys
p = json.load(open(sys.argv[1]))
A = p['audio']; ruins = []
def pcm(src, ms, d):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ms), "-t", str(d), "-i", src, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    n = len(out) // 2
    return struct.unpack(f"<{n}h", out[:2 * n]) if n else ()
zeros = []
for v in (A.get('voz') or []) + (A.get('viral') or []):
    if v['src'].endswith('.wav') and '_voz' in v['src']:
        continue  # narração do clone: pausa entre frases é natural
    a = pcm(v['src'], v.get('ms', 0), v['d']); z = 0; ini = None
    for i, x in enumerate(list(a) + [1]):
        if x == 0:
            z += 1; ini = i if z == 1 else ini
        else:
            if z >= 8000 * 0.25 and ini + z < len(a) - 80:  # cauda do clipe (fim natural antes do corte) não conta
                zeros.append((v['t'] + ini / 8000, v['t'] + (ini + z) / 8000, v['src'].split('/')[-1]))
            z = 0
cob = [(v['t'], v['t'] + v['d']) for v in (A.get('voz') or []) + (A.get('viral') or []) + (A.get('musica') or [])]
for s in A.get('sfx') or []:
    dur = s.get('d') or float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                               s['src'] if '/' in s['src'] else f"assets/som/{s['src']}.m4a"], capture_output=True, text=True).stdout or 0.3)
    cob.append((s['t'], s['t'] + dur))
sfx_cob = cob[len((A.get('voz') or []) + (A.get('viral') or []) + (A.get('musica') or [])):]
for a, b, nome in zeros:
    livre = b - a - sum(max(0, min(b, y) - max(a, x)) for x, y in sfx_cob)
    if livre >= 0.25:
        ruins.append(f"{a:6.2f} silêncio digital {b - a:.2f}s dentro de {nome}, {livre:.2f}s sem efeito por cima (palavra apagada? usar bip)")
cob.sort(); fim = 0.0
for a, b in cob:
    if a - fim >= 0.9 and fim < p['dur'] - 0.6:
        ruins.append(f"{fim:6.2f} {a - fim:.2f}s sem voz nem efeito (viral só texto? pôr teclado/riser)")
    fim = max(fim, b)
if p['dur'] - fim >= 0.9: ruins.append(f"{fim:6.2f} fim mudo {p['dur'] - fim:.2f}s")
print(f"audio_plano: {len(ruins)} problema(s)")
for r in ruins: print('  ' + r)
sys.exit(1 if ruins else 0)
