#!/usr/bin/env python3
"""checar_fundos.py: barra foto de fundo repetida nos carrosséis (Papo News e Papo de Carcinicultor).

Rodar ANTES de agendar/subir e, depois de aprovado e agendado, de novo com --registrar:

  python pipeline/checar_fundos.py <pasta do carrossel | news.json | conteudo.json> \
      --marca <papo|fertilidade|caneta|tdah|camarao> --data <AAAA-MM-DD do post> [--registrar]

REPROVA (saída 1) quando uma foto do carrossel:
  - já saiu na mesma marca nos últimos N carrosséis (N = "janela" da marca no registro, padrão 30),
    contando também os carrosséis já registrados com data DEPOIS desta (agendados);
  - é da mesma sessão provável de uma que saiu (id do Pexels a até 1500 de distância:
    mesma pessoa ou mesmo cenário, com outro nome de arquivo);
  - é quase igual a uma que saiu (dHash da foto recortada 4:5 ou da faixa de cima do slide pronto);
  - aparece duas vezes (ou com outra foto da mesma sessão) dentro do próprio carrossel.

Opções:
  --registrar        grava o carrossel no registro (só se passou; repetir com o mesmo --id substitui).
  --liberar FOTO     depois de OLHAR as duas imagens e ver que são outra pessoa/outro cenário,
                     aceita "mesma sessão provável" ou "quase igual" dessa foto (nunca a mesma foto).
  --so-registrar     grava sem reprovar: só para completar o histórico com carrossel que JÁ saiu.
  --livres           lista as fotos do banco que ainda podem entrar nessa marca (e sai).
  --slides PASTA     slides prontos em outra pasta que não a do JSON (ex.: JSON em pipeline/, PNG em queue/).
  --janela N         sobrepõe a janela da marca.  --id / --origem / --metricool: dados do registro.

O registro (esteira2s/fotos-usadas.json) guarda só nome, id do Pexels, sessão aproximada, dHash e
data: nada de imagem no git. A foto é escolhida pelo ASSUNTO do slide, nunca pela posição.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RAIZ, 'esteira2s', 'fotos-usadas.json')
MARCAS = ('papo', 'fertilidade', 'caneta', 'tdah', 'camarao')
BANCO = {'camarao': 'camarao/fotos'}           # demais marcas: bg_bank
LIMITES = {'janela': 30, 'sessao_pexels': 1500, 'dhash_foto': 40, 'dhash_faixa': 36, 'mesma_imagem': 12}


# ---------- imagem ----------
def dhash(im, n=16):
    g = im.convert('L').resize((n + 1, n), Image.LANCZOS)
    px = g.load()
    bits = 0
    for y in range(n):
        for x in range(n):
            bits = (bits << 1) | (1 if px[x, y] > px[x + 1, y] else 0)
    return f'{bits:0{n * n // 4}x}'


def distancia(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count('1')


def corte_45(im):
    """O molde usa object-fit:cover centralizado num quadro 1080x1350 (4:5)."""
    w, h = im.size
    if w / h > 0.8:
        nw = round(h * 0.8)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w / 0.8)
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def faixa(im):
    """Faixa de cima do slide pronto (0-25%), onde a foto aparece com pouco véu."""
    w, h = im.size
    return im.crop((0, 0, w, round(h * 0.25)))


def pexels_id(nome):
    m = re.findall(r'(?<!\d)(\d{5,})(?!\d)', os.path.splitext(os.path.basename(nome))[0])
    return int(m[-1]) if m else None


# ---------- leitura do carrossel ----------
def tem_slides(p):
    try:
        return isinstance(json.load(open(p, encoding='utf-8')).get('slides'), list)
    except Exception:
        return False


def imagens_dos_slides(pasta):
    achadas = {}
    for padrao in ('[0-9][0-9].jpg', 'slide_[0-9][0-9].png', 'slide_[0-9][0-9].jpg',
                   'jpg/slide_[0-9][0-9].jpg', 'jpg/[0-9][0-9].jpg'):
        for f in sorted(glob.glob(os.path.join(pasta, padrao))):
            n = int(re.findall(r'(\d\d)\.(?:jpg|png)$', f)[0])
            achadas.setdefault(n, f)
    return achadas


def achar_foto(foto, lugares):
    if os.path.isabs(foto) and os.path.exists(foto):
        return foto
    for d in lugares:
        for c in (os.path.join(d, foto), os.path.join(d, os.path.basename(foto))):
            if os.path.exists(c):
                return c
    return None


def ler_carrossel(entrada, bancos, pasta_slides=None):
    if os.path.isdir(entrada):
        pasta = entrada
        cands = [os.path.join(pasta, n) for n in ('news.json', 'conteudo.json')]
        cands = [c for c in cands if os.path.exists(c)] or \
            [c for c in sorted(glob.glob(os.path.join(pasta, '*.json'))) if tem_slides(c)]
        jpath = cands[0] if cands else None
    else:
        jpath, pasta = entrada, os.path.dirname(os.path.abspath(entrada))
    slides = json.load(open(jpath, encoding='utf-8'))['slides'] if jpath else []
    imgs = imagens_dos_slides(pasta_slides or pasta)
    total = max([len(slides)] + list(imgs))
    fotos, avisos = [], []
    for i in range(1, total + 1):
        sl = slides[i - 1] if i <= len(slides) else {}
        foto = sl.get('foto')
        if jpath and not foto:
            continue                          # slide sem foto de fundo (ex.: print do artigo)
        e = {'slide': i}
        if foto:
            e['foto'] = os.path.basename(foto)
            pid = pexels_id(foto)
            if pid:
                e['pexels'] = pid
                e['sessao'] = f'pexels {str(pid)[:-3]}xxx'
            arq = achar_foto(foto, [pasta] + bancos)
            if arq:
                e['dhash_foto'] = dhash(corte_45(Image.open(arq)))
            else:
                avisos.append(f'slide {i:02d}: não achei {foto} em {", ".join([pasta] + bancos)} (sem dHash da foto)')
        if i in imgs:
            e['dhash_faixa'] = dhash(faixa(Image.open(imgs[i])))
        fotos.append(e)
    if not fotos:
        sys.exit(f'ERRO: nenhum slide com foto em {entrada} (esperava news.json/conteudo.json ou 01.jpg/slide_01.png)')
    return fotos, avisos, jpath


# ---------- registro ----------
def ler_registro(p):
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8'))
    return {'sobre': 'Fotos de fundo já usadas nos carrosséis, por marca. Gerado por pipeline/checar_fundos.py.',
            'limites': dict(LIMITES), 'marcas': {}}


def gravar_registro(reg, p):
    """JSON legível com uma foto por linha (o arquivo cresce pouco e o diff fica limpo)."""
    linhas = ['{']
    cab = [(k, v) for k, v in reg.items() if k != 'marcas']
    for k, v in cab:
        linhas.append(f' {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},')
    linhas.append(' "marcas": {')
    marcas = list(reg['marcas'].items())
    for mi, (m, dados) in enumerate(marcas):
        linhas.append(f'  {json.dumps(m)}: {{')
        extra = [(k, v) for k, v in dados.items() if k != 'carrosseis']
        for k, v in extra:
            linhas.append(f'   {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)},')
        linhas.append('   "carrosseis": [')
        cs = sorted(dados.get('carrosseis', []), key=lambda c: (c['data'], c['id']))
        for ci, c in enumerate(cs):
            linhas.append('    {' + ', '.join(f'{json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}'
                                            for k, v in c.items() if k != 'fotos') + ', "fotos": [')
            for fi, f in enumerate(c['fotos']):
                linhas.append('     ' + json.dumps(f, ensure_ascii=False) + (',' if fi < len(c['fotos']) - 1 else ''))
            linhas.append('    ]}' + (',' if ci < len(cs) - 1 else ''))
        linhas.append('   ]')
        linhas.append('  }' + (',' if mi < len(marcas) - 1 else ''))
    linhas.append(' }')
    linhas.append('}')
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(linhas) + '\n')


def janela_da_marca(reg, marca, data, cid, n):
    cs = [c for c in reg['marcas'].get(marca, {}).get('carrosseis', []) if c['id'] != cid]
    antes = sorted([c for c in cs if c['data'] <= data], key=lambda c: (c['data'], c['id']))
    depois = sorted([c for c in cs if c['data'] > data], key=lambda c: (c['data'], c['id']))
    return (antes[-n:] if n > 0 else []) + depois


# ---------- comparação ----------
def comparar(a, b, lim):
    """Devolve (motivo, liberavel) ou None."""
    if a.get('foto') and a.get('foto') == b.get('foto'):
        return 'mesma foto', False
    if a.get('pexels') and a.get('pexels') == b.get('pexels'):
        return 'mesma foto (mesmo id do Pexels)', False
    for chave, nome in (('dhash_foto', 'foto'), ('dhash_faixa', 'topo do slide')):
        if a.get(chave) and b.get(chave):
            d = distancia(a[chave], b[chave])
            if d <= lim['mesma_imagem']:
                return f'mesma imagem com outro nome ({nome}: dHash {d})', False
    if a.get('pexels') and b.get('pexels'):
        d = abs(a['pexels'] - b['pexels'])
        if d <= lim['sessao_pexels']:
            return f'mesma sessão de fotos provável (Pexels {a["pexels"]} x {b["pexels"]}, distância {d})', True
    for chave, nome in (('dhash_foto', 'foto'), ('dhash_faixa', 'topo do slide')):
        if a.get(chave) and b.get(chave):
            d = distancia(a[chave], b[chave])
            if d <= lim[chave]:
                return f'{nome} quase igual (dHash {d} de 256)', True
    return None


def rotulo(f):
    return f'slide {f["slide"]:02d} {f.get("foto", "(sem nome)")}'


def checar(fotos, historico, marca, lim, liberar):
    falhas, liberadas = [], []
    for i, a in enumerate(fotos):
        for b in fotos[i + 1:]:
            r = comparar(a, b, lim)
            if r:
                (liberadas if r[1] and (a.get('foto') in liberar or b.get('foto') in liberar) else falhas).append(
                    f'{rotulo(b)}: {r[0]} que o {rotulo(a)} do MESMO carrossel')
        for c in reversed(historico):
            for b in c['fotos']:
                r = comparar(a, b, lim)
                if r:
                    (liberadas if r[1] and a.get('foto') in liberar else falhas).append(
                        f'{rotulo(a)}: {r[0]} que {marca} {c["data"]} ({c["id"]}) {rotulo(b)}')
    return falhas, liberadas


def fotos_livres(reg, marca, data, n, lim, bancos):
    hist = janela_da_marca(reg, marca, data, None, n)
    usadas = [b for c in hist for b in c['fotos']]
    livres = []
    for d in bancos:
        for arq in sorted(glob.glob(os.path.join(d, '*.jp*g')) + glob.glob(os.path.join(d, '*.png'))):
            nome = os.path.basename(arq)
            e = {'slide': 0, 'foto': nome}
            pid = pexels_id(nome)
            if pid:
                e['pexels'] = pid
            if any(comparar(e, b, lim) for b in usadas):
                continue
            e['dhash_foto'] = dhash(corte_45(Image.open(arq)))
            if any(comparar(e, b, lim) for b in usadas):
                continue
            livres.append(nome)
    return livres


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('entrada', nargs='?', help='pasta do carrossel, news.json ou conteudo.json')
    ap.add_argument('--marca', required=True, choices=MARCAS)
    ap.add_argument('--data', help='dia do post (AAAA-MM-DD); padrão: data no caminho ou hoje')
    ap.add_argument('--id', help='identificador no registro; padrão: <data>-<pasta>')
    ap.add_argument('--origem', help='de onde veio (caminho/commit), só para o registro')
    ap.add_argument('--metricool', type=int, help='id do post no Metricool, só para o registro')
    ap.add_argument('--slides', help='pasta dos slides prontos, quando não é a mesma do JSON (ex.: queue/<pasta>)')
    ap.add_argument('--registro', default=REGISTRO)
    ap.add_argument('--banco', action='append', help='pasta das fotos (repetível); padrão bg_bank ou camarao/fotos')
    ap.add_argument('--janela', type=int)
    ap.add_argument('--liberar', action='append', default=[], metavar='FOTO')
    ap.add_argument('--registrar', action='store_true')
    ap.add_argument('--so-registrar', action='store_true')
    ap.add_argument('--livres', action='store_true')
    a = ap.parse_args()

    reg = ler_registro(a.registro)
    lim = dict(LIMITES, **reg.get('limites', {}))
    dados_marca = reg['marcas'].get(a.marca, {})
    n = a.janela if a.janela is not None else dados_marca.get('janela', lim['janela'])
    bancos = a.banco or [os.path.join(RAIZ, BANCO.get(a.marca, 'bg_bank'))]
    data = a.data
    if not data:
        m = re.findall(r'\d{4}-\d{2}-\d{2}', os.path.abspath(a.entrada or ''))
        data = m[-1] if m else dt.date.today().isoformat()
    dt.date.fromisoformat(data)

    if a.livres:
        livres = fotos_livres(reg, a.marca, data, n, lim, bancos)
        print(f'{len(livres)} foto(s) do banco livres para {a.marca} (janela de {n} carrosséis):')
        for nome in livres:
            print('  ' + nome)
        if not livres:
            print('  nenhuma: busque foto nova pelo assunto do slide (ver o passo das fotos no doc da esteira).')
        return 0
    if not a.entrada:
        ap.error('informe a pasta ou o JSON do carrossel')

    fotos, avisos, jpath = ler_carrossel(a.entrada, bancos, a.slides)
    if os.path.isdir(a.entrada):
        base = os.path.basename(os.path.abspath(a.entrada))
    else:
        base = os.path.splitext(os.path.basename(a.entrada))[0]
        if base in ('news', 'conteudo'):
            base = os.path.basename(os.path.dirname(os.path.abspath(a.entrada)))
    cid = a.id or (base if re.match(r'\d{4}-\d{2}-\d{2}', base) else f'{data}-{base}')
    hist = janela_da_marca(reg, a.marca, data, cid, n)
    for av in avisos:
        print('AVISO ' + av)
    falhas, liberadas = checar(fotos, hist, a.marca, lim, set(a.liberar))
    for l in liberadas:
        print('LIBERADA (conferida a olho) ' + l)
    print(f'{a.marca} {data} ({cid}): {len(fotos)} slide(s) com foto, comparados com {len(hist)} carrossel(is) da marca '
          f'(janela {n}).')
    if falhas:
        for f in falhas:
            print('REPROVADO ' + f)
        if not a.so_registrar:
            print('\nTroque a foto por outra que combine com o ASSUNTO daquele slide e rode de novo.\n'
                  f'Fotos ainda livres no banco: python pipeline/checar_fundos.py --marca {a.marca} --data {data} --livres\n'
                  'Sem foto livre que combine: busque foto nova (Pexels/Openverse CC0) em vez de repetir.')
            return 1
    else:
        print('OK: nenhuma foto, sessão ou imagem quase igual repetida.')

    if a.registrar or a.so_registrar:
        if a.liberar:
            for f in fotos:
                if f.get('foto') in a.liberar:
                    f['liberada'] = True
        c = {'id': cid, 'data': data}
        if a.origem:
            c['origem'] = a.origem
        elif jpath:
            c['origem'] = os.path.relpath(os.path.abspath(jpath), RAIZ) if os.path.abspath(jpath).startswith(RAIZ) else jpath
        if a.metricool:
            c['metricool_id'] = a.metricool
        c['fotos'] = fotos
        dm = reg['marcas'].setdefault(a.marca, {})
        dm['carrosseis'] = [x for x in dm.get('carrosseis', []) if x['id'] != cid] + [c]
        gravar_registro(reg, a.registro)
        print(f'registrado em {a.registro} como {a.marca}/{cid}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
