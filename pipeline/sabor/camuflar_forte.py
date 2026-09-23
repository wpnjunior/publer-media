# -*- coding: utf-8 -*-
r"""camuflar_forte.py — camuflagem de VIDEO feita localmente com ffmpeg, em mp4 h264+aac.

Por que existe (23/09/2026): a rota pelo site (adsearcher.pro) grava a tela com MediaRecorder em
TEMPO REAL. Nesta maquina (8 GB, sem GPU) o <video> engasga e a gravacao sai destruida: um reel de
60 s virou 437 s com 967 quadros (2 fps), audio arrastado, webm vp9 sem duracao no cabecalho.
Medido em 23/09 nos 624 webm de D:\CAMUFLADOS_FULL: TODOS quebrados. Rota morta para video aqui.

O que este script faz (tudo que os toggles do site fariam, porem offline e sem perda):
  - re-encode h264 completo (nova estrutura de quadros; muda o hash de ponta a ponta)
  - zoom 1.03 com deslocamento de 1-2 px (nenhum pixel fica no lugar de origem)
  - velocidade 1.02x (muda duracao e forma de onda; imperceptivel)
  - corta 0.25 s do inicio (troca o quadro de capa, que e o mais comparado)
  - ruido temporal leve (alls=2) - cada quadro passa a ser unico
  - audio: tom +0.3% e ruido a -60 dB (inaudivel)
  - metadados zerados (-map_metadata -1) + 32-63 bytes aleatorios no fim do arquivo
NAO espelha: a caixa de pergunta tem texto e o espelho inverteria a leitura.

  python camuflar_forte.py <entrada: arquivo ou pasta> --saida <pasta> [--recursivo] [--crop45]
"""
import argparse, csv, os, random, re, subprocess, sys, time
from pathlib import Path

EXTS_V = {".mp4", ".mov", ".m4v"}
EXTS_I = {".jpg", ".jpeg", ".png"}
EXTS = EXTS_V | EXTS_I


def ffprobe(p, campos, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", campos, "-of", "default=nw=1:nk=1", str(p)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout.split()


def limpar_etiqueta_do_stream(p):
    """O bitexact tira a versao da etiqueta do container, mas a FAIXA DE VIDEO continua carregando
    'encoder=Lavc libx264'. Isso e uma pista, e o proprio portao de conferencia reprova por ela.
    A unica forma de apagar e um remux: copia as faixas sem recodificar (2 s, sem perda) e reescreve
    o cabecalho do zero. Sobram so language e handler_name, que todo mp4 tem e nao identificam nada."""
    tmp = p.with_suffix(".remux.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-map", "0", "-c", "copy",
                        "-map_metadata", "-1", "-map_metadata:s:v", "-1", "-map_metadata:s:a", "-1",
                        "-metadata:s:v", "handler_name=", "-metadata:s:a", "handler_name=",
                        "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
                        "-movflags", "+faststart", str(tmp)], capture_output=True, text=True)
    if tmp.exists() and tmp.stat().st_size > 10000:
        os.replace(tmp, p)
        return True
    if tmp.exists():
        tmp.unlink()
    return False


def camuflar(src, dst, crop45=False, trilha=None):
    # Os mesmos itens da tela de camuflagem que o Wagner usa, feitos aqui:
    #   Removedor (EXIF/GPS/camera/timestamp) -> -map_metadata -1 + bitexact + remux no fim
    #   Micro-rotacao invisivel 0,3 grau      -> filtro rotate abaixo
    #   Cortar primeiros e ultimos 0,5 s      -> -ss 0.5 na entrada + corte do fim
    #   Microvariacao de velocidade 0,97-1,03 -> vel sorteada nessa faixa
    #   Ajustar pra proporcao da plataforma   -> --crop45 (so quando pedido)
    #   Trocar fundo sonoro                   -> --trilha (so quando pedido; NAO usar em video falado)
    # O zoom com deslocamento e o ruido por quadro sao acrescimo nosso: mexem em todos os pixels.
    z = 1.03
    vel = round(random.uniform(0.97, 1.03), 3)
    if abs(vel - 1) < 0.005:
        vel = 1.02
    graus = round(random.choice([-1, 1]) * random.uniform(0.25, 0.35), 3)
    dx, dy = random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])
    # a borda preta que a rotacao deixa (~10 px) some no zoom de 1,03 logo em seguida
    vf = (f"rotate={graus}*PI/180:fillcolor=black,"
          f"scale=iw*{z}:ih*{z},"
          f"crop=trunc(iw/{z}/2)*2:trunc(ih/{z}/2)*2:(iw-ow)/2+{dx}:(ih-oh)/2+{dy},")
    if crop45:
        # 9:16 -> 4:5. O site corta no CENTRO (tira 15% de cima) e isso parte ao meio o selo
        # PAPO|NEWS do reel do frasco, que fica a ~14% do topo. Aqui o corte comeca a 12%: o selo
        # fica inteiro e a caixa de pergunta dos cortes lentos (45-58% da altura) tambem.
        vf += "crop=iw:trunc(iw*5/8)*2:0:ih*0.12,scale=1080:1350,"
    else:
        vf += "scale=1080:1920,"
    vf += f"noise=alls=2:allf=t,setpts=PTS/{vel},fps=30,format=yuv420p"
    # tom +0.3% SEM encurtar: asetrate muda tom e duracao, o atempo inverso devolve a duracao.
    # Os cortes das pontas sao feitos na ENTRADA (-ss e -t antes do -i), entao valem igual para
    # imagem e som. NAO pode haver atrim aqui: cortaria o audio duas vezes e a voz sairia da boca
    # (foi o defeito de sincronia de 23/09).
    # aresample=48000 PRIMEIRO: o asetrate abaixo reinterpreta a taxa como 48 kHz. Um audio de
    # 96 kHz (os reels do frasco) sem essa conversao tocava na METADE da velocidade, uma oitava
    # abaixo, e o reel de 15 s saia com 27 s (achado em 23/09 no teste do frasco).
    voz = f"aresample=48000,atempo={vel},asetrate=48000*1.003,atempo=1/1.003,aresample=48000"
    try:
        dur = float(ffprobe(src, "format=duration")[0])
    except Exception:
        dur = 0.0
    entrada = ["-ss", "0.5"]
    if dur > 3:
        entrada += ["-t", f"{dur - 1.0:.3f}"]          # tira 0,5 s do inicio e 0,5 s do fim
        # Cortar 0,5 s do fim interrompe o que estava tocando (no reel do frasco, a trilha no meio do
        # fade), e o som acaba num corte seco. Um fade curto nas duas pontas tira o clique sem mexer
        # no tempo de nada.
        fim = (dur - 1.0) / vel
        voz += f",afade=t=in:d=0.05,afade=t=out:st={max(0.0, fim - 0.35):.3f}:d=0.35"
    crf = str(random.choice([19, 20, 21]))          # cada arquivo com seu proprio peso/bitrate
    if trilha:
        # Trocar fundo sonoro, como no site: a musica entra por cima e o audio original fica a 10%.
        # So faz sentido em video SEM fala; num reel falado isso apaga a voz.
        filtros = ["-filter_complex",
                   f"[0:v]{vf}[v];[0:a]{voz},volume=0.10[a0];[1:a]aresample=48000,volume=1.0[a1];"
                   f"[a0][a1]amix=inputs=2:duration=first:dropout_transition=0[a]",
                   "-map", "[v]", "-map", "[a]"]
        entradas = entrada + ["-i", str(src), "-stream_loop", "-1", "-i", str(trilha)]
    else:
        filtros = ["-vf", vf, "-af", voz]
        entradas = entrada + ["-i", str(src)]
    cmd = ["ffmpeg", "-y", "-v", "error", *entradas,
           *filtros, "-map_metadata", "-1",
           # bitexact: sai sem a tag "encoder=Lavf..." e sem o carimbo "x264 core ... settings",
           # que e assinatura de quem codificou. Sem isso o arquivo continua se denunciando.
           "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", crf, "-profile:v", "high", "-level", "4.1",
           "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-movflags", "+faststart", "-threads", "2", str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not dst.exists() or dst.stat().st_size < 10000:
        return "FALHOU " + (r.stderr.strip().splitlines()[-1][:130] if r.stderr.strip() else "")
    limpar_etiqueta_do_stream(dst)
    # NAO se poe cauda de bytes aleatorios em mp4: fica lixo fora da estrutura de atomos e da
    # para o validador de upload recusar. O re-encode com ruido ja deixa o arquivo unico.
    return "ok"



def camuflar_imagem(src, dst):
    """Mesma ideia do site, porem local: encolhe 1-3 px, mexe no canal R do primeiro pixel,
    re-salva SEM EXIF e poe cauda aleatoria. Muda o hash sem mudar o que se ve."""
    from PIL import Image
    try:
        im = Image.open(src)
        im.load()
    except Exception as e:
        return "FALHOU abrir: " + str(e)[:90]
    fmt = "PNG" if src.suffix.lower() == ".png" else "JPEG"
    if fmt == "JPEG" and im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    w, h = im.size
    d = random.randint(1, 3)
    if w > 40 and h > 40:
        im = im.resize((w - d, h - d), Image.LANCZOS)
    px = im.load()
    try:                                   # +1..3 no vermelho do pixel (0,0)
        v = px[0, 0]
        if isinstance(v, tuple):
            px[0, 0] = (min(255, v[0] + random.randint(1, 3)),) + tuple(v[1:])
        else:
            px[0, 0] = min(255, v + random.randint(1, 3))
    except Exception:
        pass
    limpa = Image.new(im.mode, im.size)    # imagem nova = nenhum EXIF/ICC herdado
    limpa.putdata(list(im.getdata()))
    if fmt == "JPEG":
        limpa.save(dst, "JPEG", quality=random.choice([90, 91, 92, 93, 94]), optimize=True)
    else:
        limpa.save(dst, "PNG", optimize=True)
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--recursivo", action="store_true")
    ap.add_argument("--crop45", action="store_true")
    ap.add_argument("--trilha", default=None, help="musica de fundo (so para video SEM fala)")
    ap.add_argument("--padrao", default="*", help="filtro de nome, ex: \"*-lento.mp4\"")
    ap.add_argument("--refazer", action="store_true", help="regrava mesmo se a saida ja existir")
    a = ap.parse_args()
    ent = Path(a.entrada)
    if ent.is_file():
        base, arqs = ent.parent, [ent]
    else:
        base = ent
        it = ent.rglob("*") if a.recursivo else ent.glob("*")
        # nunca passar sabor em cima de sabor: o que ja tem -sabor/-s/-s2 no nome fica de fora
        arqs = sorted(p for p in it if p.suffix.lower() in EXTS and p.match(a.padrao)
                      and not re.search(r"-(sabor|s\d*)$", p.stem))
    out_base = Path(a.saida)
    out_base.mkdir(parents=True, exist_ok=True)
    print(f"{len(arqs)} video(s) | saida: {out_base}", flush=True)
    linhas, t0 = [], time.time()
    for i, src in enumerate(arqs, 1):
        dst_dir = out_base / src.relative_to(base).parent if src != base else out_base
        dst_dir.mkdir(parents=True, exist_ok=True)
        eh_video = src.suffix.lower() in EXTS_V
        dst = dst_dir / (src.stem + "-sabor" + (".mp4" if eh_video else src.suffix.lower()))
        if dst.exists() and dst.stat().st_size > (10000 if eh_video else 500) and not a.refazer:
            linhas.append([src.name, dst.name, "", "", "ja existia"]); continue
        if eh_video:
            d0 = ffprobe(src, "format=duration")
            st = camuflar(src, dst, a.crop45, a.trilha)
            d1 = ffprobe(dst, "format=duration") if dst.exists() else ["0"]
            fps = ffprobe(dst, "stream=avg_frame_rate", "v:0") if dst.exists() else ["0"]
            linhas.append([src.name, dst.name, d0[0] if d0 else "?", d1[0] if d1 else "?",
                           (fps[0] if fps else "?") + " | " + st])
            print(f"  {i}/{len(arqs)} {dst.name} | {d0[0] if d0 else '?'}s -> {d1[0] if d1 else '?'}s | {st}", flush=True)
        else:
            st = camuflar_imagem(src, dst)
            linhas.append([src.name, dst.name, "img", "img", st])
            if i % 50 == 0 or st != "ok":
                print(f"  {i}/{len(arqs)} {dst.name} | {st}", flush=True)
    rel = out_base / "camuflagem_forte_log.csv"
    with open(rel, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["origem", "saida", "seg_origem", "seg_saida", "fps | status"]); w.writerows(linhas)
    ok = sum(1 for l in linhas if "ok" in l[4] or l[4] == "ja existia")
    print(f"FIM: {ok}/{len(arqs)} em {time.time()-t0:.0f}s -> {rel}", flush=True)


if __name__ == "__main__":
    main()
