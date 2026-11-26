# leitura.py planos/X.json - portão de leitura (Wagner, 13/11 22h08: "daria para ler o que está escrito?")
# Reprova cartela curta demais para ler, informação em letra pequena e artigo relâmpago.
import json, re, sys
p = json.load(open(sys.argv[1]))
ruins = []
def px(f):
    m = re.search(r'(\d+)px', f or '')
    return int(m.group(1)) if m else 70
def precisa(txt): return max(1.5, 0.4 * len(str(txt).split()) + 0.6)
for c in p['camadas']:
    t = c.get('tipo'); d = c.get('d') or 0; ini = c.get('t', 0)
    if t == 'texto':
        f = c.get('fonte', '')
        fonte_rodape = px(f) <= 32 or 'doi' in c['txt'].lower() or ' et al' in c['txt']
        if fonte_rodape or 'CHECAGEM' in c['txt']: continue
        # cartelas empilhadas: a duração que conta é até a cartela sumir
        if d + 0.01 < precisa(c['txt']):
            ruins.append(f"{ini:6.2f} texto {d:.2f}s < {precisa(c['txt']):.2f}s: {c['txt'][:50]}")
        lim = 100 if 'Anton' in f else 80
        if px(f) < lim:
            ruins.append(f"{ini:6.2f} texto pequeno {px(f)}px: {c['txt'][:50]}")
    elif t == 'numero':
        if d < 1.8: ruins.append(f"{ini:6.2f} numero {d:.2f}s < 1.8s: {c.get('valor')} {c.get('rotulo','')[:40]}")
        if c.get('rotulo') and d < precisa(c['rotulo']) + 0.6:
            ruins.append(f"{ini:6.2f} rotulo sem tempo ({d:.2f}s): {c['rotulo'][:50]}")
        if c.get('rotulo') and len(c['rotulo'].split()) > 4:
            ruins.append(f"{ini:6.2f} rotulo longo (informação principal em letra pequena?): {c['rotulo'][:50]}")
    elif t == 'artigo':
        if d < 3.0: ruins.append(f"{ini:6.2f} artigo {d:.2f}s < 3s: {c.get('titulo','')[:40]}")
    elif t == 'checklist':
        n = len(c.get('itens', []))
        if d + 0.05 < 1.0 + 0.9 * n: ruins.append(f"{ini:6.2f} checklist {d:.2f}s curto para {n} itens")
print(f"leitura: {len(ruins)} problema(s)")
for r in ruins: print('  ' + r)
sys.exit(1 if ruins else 0)
