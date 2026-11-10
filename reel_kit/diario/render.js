// Renderiza a composição quadro a quadro (comp.html) e grava MP4 sem áudio.
// Uso: node render.js <pasta_trabalho> <saida.mp4> [processos=3]
//      node render.js <pasta_trabalho> test <pasta_jpgs> t1,t2,...   (quadros avulsos para conferir)
// A pasta de trabalho precisa ter timeline.json e frames/00001.jpg... (extraídos do bruto a 25 fps).
// Ela é servida por http (módulos e fontes não carregam via file://).
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const AQUI = __dirname;
const [, , WORK, SAIDA, A3, A4] = process.argv;
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.jpg': 'image/jpeg', '.png': 'image/png', '.ttf': 'font/ttf' };

function servidor() {
  return new Promise((ok) => {
    const srv = http.createServer((req, res) => {
      const u = decodeURIComponent(req.url.split('?')[0]);
      let f = path.join(AQUI, u);
      if (u.startsWith('/frames/') || u === '/timeline.json') f = path.join(WORK, u);
      fs.readFile(f, (err, data) => {
        if (err) { res.writeHead(404); return res.end(); }
        res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' });
        res.end(data);
      });
    });
    srv.listen(0, '127.0.0.1', () => ok(srv));
  });
}

async function abrir(browser, porta, tl) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:${porta}/comp.html`);
  await page.evaluate((tl) => window.init(tl), tl);
  return page;
}

async function faixa(browser, porta, tl, f0, f1, out) {
  const page = await abrir(browser, porta, tl);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(tl.fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = f0; f < f1; f++) {
    await page.evaluate((f) => window.renderFrame(f), f);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise((r, j) => ff.on('close', (c) => (c === 0 ? r() : j(new Error('ffmpeg ' + c)))));
  await page.close();
}

(async () => {
  const tl = JSON.parse(fs.readFileSync(path.join(WORK, 'timeline.json'), 'utf8'));
  const srv = await servidor();
  const porta = srv.address().port;
  const browser = await chromium.launch({ args: ['--font-render-hinting=none'] });
  const N = Math.round(tl.total * tl.fps);
  if (SAIDA === 'test') {
    fs.mkdirSync(A3, { recursive: true });
    const page = await abrir(browser, porta, tl);
    for (const ts of A4.split(',')) {
      const f = Math.round(parseFloat(ts) * tl.fps);
      await page.evaluate((f) => window.renderFrame(f), f);
      await page.screenshot({ path: path.join(A3, `t${String(ts).padStart(6, '0')}.jpg`), type: 'jpeg', quality: 80 });
    }
  } else {
    const procs = parseInt(A3 || '3', 10);
    const passo = Math.ceil(N / procs);
    const partes = [];
    const jobs = [];
    for (let i = 0; i < procs; i++) {
      const f0 = i * passo, f1 = Math.min(N, f0 + passo);
      if (f0 >= f1) break;
      const out = path.join(WORK, `parte${i}.mp4`);
      partes.push(out);
      jobs.push(faixa(browser, porta, tl, f0, f1, out));
    }
    const t0 = Date.now();
    await Promise.all(jobs);
    fs.writeFileSync(path.join(WORK, 'partes.txt'), partes.map((p) => `file '${p}'`).join('\n'));
    await new Promise((r, j) => spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(WORK, 'partes.txt'), '-c', 'copy', SAIDA], { stdio: 'inherit' })
      .on('close', (c) => (c === 0 ? r() : j(new Error('concat ' + c)))));
    console.log(`${N} quadros em ${((Date.now() - t0) / 1000).toFixed(0)} s -> ${SAIDA}`);
  }
  await browser.close();
  srv.close();
})().catch((e) => { console.error(e); process.exit(1); });
