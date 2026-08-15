# -*- coding: utf-8 -*-
"""CARROSSEL COMENTADO: slides do carrossel em 9:16, o clone recortado falando no
canto esquerdo, e b-roll entrando por alguns segundos no lugar do slide para dar ritmo.

Uso:
  python montar_comentado.py <pasta_carrossel> <clone> <saida.mp4> <t1,t2,...> [broll.json]

<t1,t2,...> = segundo em que cada slide entra (o tempos.py calcula).
broll.json  = [{"arquivo":"broll/gestante_1.mp4","entra":1.5,"dura":2.6}, ...]
              Cada clipe cobre a área do slide pelo tempo indicado, e o slide volta depois.
O clone continua visível o tempo todo — quem fala nunca some.
"""
import sys, os, glob, json, subprocess

PASTA, CLONE, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
TEMPOS = [float(x) for x in sys.argv[4].split(",")]
BROLL = json.load(open(sys.argv[5], encoding="utf-8")) if len(sys.argv) > 5 else []

W, H = 1080, 1920
FUNDO = "#080B11"
# Busto, em FRAÇÃO do quadro. O webm do HeyGen já vem enquadrado: a cabeça começa
# a ~12% do topo e o corpo preenche a largura. Então corta-se só a folga do topo e
# um pouco das laterais — cropar como se fosse plano aberto decepava a cabeça.
CLONE_CROP = "iw*0.70:ih*0.52:iw*0.15:ih*0.10"
CLONE_W = 340
CLONE_X, CLONE_Y_BASE = 25, 566  # acima da faixa de legenda do Instagram
SLIDE_W, SLIDE_Y = 900, 262
CORTE_RODAPE = 150               # tira a faixa de marca do card (o clone cobriria)
MARCA = "Dr. Wagner Novaes  ·  CRM-RJ 0127554-2"
FONTE = "C\\:/Windows/Fonts/segoeui.ttf"


def dur_de(caminho):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", caminho],
                                capture_output=True, text=True).stdout.strip())


def main():
    slides = sorted(glob.glob(os.path.join(PASTA, "slide_*.png")))[:len(TEMPOS)]
    tempos = TEMPOS[:len(slides)]
    dur = dur_de(CLONE)

    entradas, filtros = [], []
    for s in slides:
        entradas += ["-loop", "1", "-t", str(dur), "-i", s]
    idx_clone = len(slides)
    entradas += ["-c:v", "libvpx-vp9", "-i", CLONE] if CLONE.endswith(".webm") else ["-i", CLONE]
    idx_broll0 = idx_clone + 1
    for b in BROLL:
        entradas += ["-i", b["arquivo"]]

    marca = MARCA.replace(":", r"\:")
    filtros.append(f"color=c={FUNDO}:s={W}x{H}:r=30:d={dur},"
                   f"drawtext=fontfile='{FONTE}':text='{marca}':fontcolor=#8A97A5:fontsize=25"
                   f":x=W-tw-40:y=H-566-40[bg]")
    for i in range(len(slides)):
        filtros.append(f"[{i}:v]crop=iw:ih-{CORTE_RODAPE}:0:0,scale={SLIDE_W}:-1,setsar=1[s{i}]")
    # format=yuva420p PRESERVA o alfa do webm — sem isso o clone entra como retângulo opaco
    filtros.append(f"[{idx_clone}:v]crop={CLONE_CROP},scale={CLONE_W}:-2,"
                   f"format=yuva420p,setsar=1[cl]")

    # altura que o slide ocupa: o b-roll usa a mesma caixa, para o quadro não "pular"
    alt_slide = int(SLIDE_W * 1200 / 1080)
    for j, b in enumerate(BROLL):
        ini, d = b["entra"], b["dura"]
        filtros.append(
            f"[{idx_broll0 + j}:v]trim=0:{d},setpts=PTS-STARTPTS+{ini}/TB,"
            f"scale={SLIDE_W}:{alt_slide}:force_original_aspect_ratio=increase,"
            f"crop={SLIDE_W}:{alt_slide},setsar=1,format=yuva420p,"
            f"fade=t=in:st={ini}:d=0.25:alpha=1,fade=t=out:st={ini + d - 0.25}:d=0.25:alpha=1[b{j}]")

    atual = "bg"
    for i in range(len(slides)):
        cond = f"gte(t,{tempos[i]})" if i > 0 else "1"
        filtros.append(f"[{atual}][s{i}]overlay=x=(W-w)/2:y={SLIDE_Y}:enable='{cond}'[v{i}]")
        atual = f"v{i}"
    for j, b in enumerate(BROLL):
        ini, d = b["entra"], b["dura"]
        filtros.append(f"[{atual}][b{j}]overlay=x=(W-w)/2:y={SLIDE_Y}"
                       f":enable='between(t,{ini},{ini + d})'[bv{j}]")
        atual = f"bv{j}"
    filtros.append(f"[{atual}][cl]overlay=x={CLONE_X}:y=H-h-{CLONE_Y_BASE}[v]")

    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + entradas + [
        "-filter_complex", ";".join(filtros),
        "-map", "[v]", "-map", f"{idx_clone}:a",
        "-t", str(dur), "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", SAIDA]
    subprocess.run(cmd, check=True)
    print(f"montado: {SAIDA} | {len(slides)} slides | {len(BROLL)} b-rolls | {dur:.1f}s")


if __name__ == "__main__":
    main()
