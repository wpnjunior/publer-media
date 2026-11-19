"""Fotografa os slides do molde Papo News (pipeline/template_news.py) em JPEG 1080x1350.
Uso: NEWS_OUT=pasta python pipeline/template_news.py news.json && python esteira2s/fotografar_news.py pasta
Saída: 01.jpg, 02.jpg... Avisa VAZA se o texto passar da tela."""
import sys,glob,os
from playwright.sync_api import sync_playwright
d=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium");pg=b.new_page(viewport={"width":1080,"height":1350})
    for h in sorted(glob.glob(d+"/slide_*.html")):
        pg.goto("file://"+os.path.abspath(h));pg.wait_for_timeout(200)
        over=pg.evaluate("()=>{const w=document.querySelector('.wrap');return w.scrollHeight>w.clientHeight+2}")
        pg.screenshot(path=h.replace("slide_","").replace(".html",".jpg"),type="jpeg",quality=92)
        print(os.path.basename(h),"VAZA" if over else "ok")
    b.close()
