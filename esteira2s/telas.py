#!/usr/bin/env python3
"""Gera telas de carrossel (1080x1350) e stories (1080x1920) das duas marcas.

Uso: python esteira2s/telas.py spec.json pasta_saida
spec.json = {
  "marca": "fertilidade" | "papo",
  "formato": "carrossel" | "story",
  "telas": [ {"rotulo": "O QUE VOCÊ JÁ OUVIU", "titulo": "Relaxa que vem.",
              "texto": "...", "lista": ["...", "..."], "fonte": "Autor, Revista, 2024 (doi ...)"} ]
}
Saída: 01.jpg, 02.jpg ... (JPEG qualidade 92). Precisa de `pip install playwright`; usa o Chromium pré-instalado (/opt/pw-browsers/chromium) se o do pip faltar.
"""
import html, json, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FONTES = AQUI / "fonts"

TEMAS = {
    "fertilidade": {"fundo": "#F4EEE8", "barra": "#2F5D72", "tinta": "#1F2A33", "texto": "#3A4651",
                    "acento": "#B5452E", "ponto": "#D8CCC0", "arroba": "@fertilidadeadois"},
    "papo": {"fundo": "#0F2233", "barra": "#F2B705", "tinta": "#FFFFFF", "texto": "#C9D6E2",
             "acento": "#F2B705", "ponto": "#36506A", "arroba": "@dr.wagnernovaesjr"},
}
TAMANHOS = {"carrossel": (1080, 1350), "story": (1080, 1920)}


def _css(t, w, h):
    f = FONTES.as_uri()
    return f"""
@font-face {{ font-family: Titulo; src: url('{f}/InterDisplay-ExtraBold.otf'); }}
@font-face {{ font-family: Corpo; src: url('{f}/Inter-Regular.otf'); }}
@font-face {{ font-family: Rotulo; src: url('{f}/Inter-SemiBold.otf'); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {w}px; height: {h}px; background: {t['fundo']}; overflow: hidden; }}
.tela {{ position: relative; width: {w}px; height: {h}px; padding: 0 92px;
         display: flex; flex-direction: column; justify-content: center; }}
.barra {{ position: absolute; top: 0; left: 0; right: 0; height: 18px; background: {t['barra']}; }}
.rotulo {{ font: 30px Rotulo; letter-spacing: 6px; color: {t['acento']}; text-transform: uppercase;
           margin-bottom: 36px; }}
.titulo {{ font-family: Titulo; color: {t['tinta']}; letter-spacing: -3px; line-height: 1.02;
           margin-bottom: 44px; }}
.texto {{ font: 42px/1.42 Corpo; color: {t['texto']}; }}
.lista {{ list-style: none; margin-top: 8px; }}
.lista li {{ font: 40px/1.35 Corpo; color: {t['texto']}; padding: 18px 0 18px 64px; position: relative;
             border-bottom: 2px solid {t['ponto']}; }}
.lista li::before {{ content: counter(item); counter-increment: item; position: absolute; left: 0; top: 16px;
                     font: 40px Titulo; color: {t['acento']}; }}
.lista {{ counter-reset: item; }}
.fonte {{ font: 24px/1.35 Corpo; color: {t['texto']}; opacity: .8; margin-top: 40px; }}
.rodape {{ position: absolute; bottom: 60px; left: 92px; right: 92px; display: flex;
           justify-content: space-between; align-items: center; font: 30px Rotulo; color: {t['texto']}; }}
.story .rodape {{ bottom: 320px; }}
.pontos span {{ display: inline-block; width: 16px; height: 16px; border-radius: 50%;
                background: {t['ponto']}; margin-left: 10px; }}
.pontos span.on {{ background: {t['acento']}; }}
"""


def _tamanho_titulo(titulo, formato):
    n = len(titulo)
    base = 150 if formato == "story" else 136
    if n > 60:
        return int(base * 0.55)
    if n > 40:
        return int(base * 0.68)
    if n > 22:
        return int(base * 0.82)
    return base


def _html(tela, i, total, t, formato, w, h):
    e = html.escape
    partes = [f'<div class="tela {formato}"><div class="barra"></div>']
    if tela.get("rotulo"):
        partes.append(f'<div class="rotulo">{e(tela["rotulo"])}</div>')
    if tela.get("titulo"):
        px = _tamanho_titulo(tela["titulo"], formato)
        partes.append(f'<div class="titulo" style="font-size:{px}px">{e(tela["titulo"])}</div>')
    if tela.get("texto"):
        partes.append(f'<div class="texto">{e(tela["texto"])}</div>')
    if tela.get("lista"):
        itens = "".join(f"<li>{e(x)}</li>" for x in tela["lista"])
        partes.append(f'<ul class="lista">{itens}</ul>')
    if tela.get("fonte"):
        partes.append(f'<div class="fonte">Fonte: {e(tela["fonte"])}</div>')
    pontos = ""
    if formato == "carrossel" and total > 1:
        pontos = '<div class="pontos">' + "".join(
            f'<span class="{"on" if k == i else ""}"></span>' for k in range(total)) + "</div>"
    partes.append(f'<div class="rodape"><span>{e(t["arroba"])}</span>{pontos}</div></div>')
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{_css(t, w, h)}</style></head>" \
           f"<body>{''.join(partes)}</body></html>"


def gerar(spec, saida):
    from playwright.sync_api import sync_playwright
    t = TEMAS[spec["marca"]]
    formato = spec.get("formato", "carrossel")
    w, h = TAMANHOS[formato]
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    telas = spec["telas"]
    arquivos = []
    with sync_playwright() as p:
        try:
            nav = p.chromium.launch()
        except Exception:
            nav = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = nav.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        for i, tela in enumerate(telas):
            tmp = saida / f".tela{i + 1:02d}.html"
            tmp.write_text(_html(tela, i, len(telas), t, formato, w, h), encoding="utf-8")
            pg.goto(tmp.resolve().as_uri())
            pg.evaluate("document.fonts.ready")
            if not pg.evaluate("document.fonts.check('40px Titulo') && document.fonts.check('40px Corpo')"):
                raise SystemExit("fontes não carregaram")
            pg.wait_for_timeout(150)
            # trava: texto não pode vazar da tela
            vaza = pg.evaluate("() => document.querySelector('.tela').scrollHeight > window.innerHeight + 2")
            if vaza:
                raise SystemExit(f"tela {i + 1}: texto passa da altura; encurte")
            arq = saida / f"{i + 1:02d}.jpg"
            pg.screenshot(path=str(arq), type="jpeg", quality=92)
            arquivos.append(str(arq))
            tmp.unlink()
        nav.close()
    return arquivos


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for a in gerar(spec, sys.argv[2]):
        print(a)
