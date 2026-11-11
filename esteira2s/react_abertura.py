#!/usr/bin/env python3
"""Abertura de React em 2 formatos (Wagner, 11/11): o trecho do viral com o rosto dele reagindo.

- dividida: viral em cima, rosto embaixo (ouvindo), crédito do autor no meio.
- canto: viral em tela cheia, rosto pequeno no canto de baixo à esquerda; no fim a imagem pausa (II)
  e o rosto cresce até a tela cheia, emendando com a resposta.

Uso: python esteira2s/react_abertura.py viral.mp4 rosto_ouvindo.mp4 dividida|canto saida.mp4 --ini 0 --dur 9.5 --credito "@autor"
Depois: junte com o corpo editado (filtro concat, nunca -c copy):
  python esteira2s/react_abertura.py --juntar abertura.mp4 corpo.mp4 final.mp4
Saída 1080x1920, 25 fps, AAC 48 kHz. O rosto é clipe do Banco de Rostos (sem som na abertura), em vai e volta.
"""
import argparse
import subprocess
import sys

FONTE = "/home/user/publer-media/reel_kit/diario/fonts/Montserrat.ttf"


def roda(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-1500:])


def juntar(a: str, b: str, saida: str) -> None:
    roda(["ffmpeg", "-y", "-v", "error", "-i", a, "-i", b, "-filter_complex",
          "[0:v]fps=25,scale=1080:1920,setsar=1[v0];[1:v]fps=25,scale=1080:1920,setsar=1[v1];"
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
          "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
          "-movflags", "+faststart", saida])


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--juntar":
        juntar(*sys.argv[2:5])
        print("react pronto:", sys.argv[4])
        return
    p = argparse.ArgumentParser()
    p.add_argument("viral"); p.add_argument("rosto"); p.add_argument("formato", choices=["dividida", "canto"]); p.add_argument("saida")
    p.add_argument("--ini", type=float, default=0.0); p.add_argument("--dur", type=float, default=9.5)
    p.add_argument("--credito", default="")
    p.add_argument("--recorte", default="", help="clipe do rosto SEM fundo (npx hyperframes remove-background rosto.mp4 -o rosto_alpha.mov); no formato canto vira só a cabeça, recortada, em 1/6 da tela")
    a = p.parse_args()
    d = a.dur
    cred = ("Vídeo original: " + a.credito).replace(":", r"\:").replace("'", "")
    # rosto em vai e volta, pelo tempo todo da abertura
    # rosto: começo do clipe em câmera lenta, vai e volta (ouvindo); nos últimos segundos o clipe inteiro, com a fala dele
    dr = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.rosto],
                              capture_output=True, text=True).stdout.strip())
    esp = max(d - dr, 0.5)
    laco = ("[1:v]fps=25,split[rA][rB];[rA]trim=duration=0.4,setpts=3*(PTS-STARTPTS),split[r1][r2];[r2]reverse[r3];"
            "[r1][r3]concat=n=2:v=1[rr];[rr]loop=loop=-1:size=32767,trim=duration={e},setpts=PTS-STARTPTS[ri];"
            "[rB]setpts=PTS-STARTPTS[rf];[ri][rf]concat=n=2:v=1,trim=duration={d},setpts=PTS-STARTPTS").format(e=esp, d=d)
    if a.formato == "dividida":
        fc = (f"[0:v]trim=start={a.ini}:duration={d},setpts=PTS-STARTPTS,fps=25,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1150:0:400[cima];"
              f"{laco},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:770:0:250[baixo];"
              f"[cima][baixo]vstack[v0];"
              f"[v0]drawbox=x=0:y=1142:w=1080:h=16:color=white:t=fill,"
              f"drawbox=x=0:y=0:w=1080:h=72:color=black@0.55:t=fill,"
              f"drawtext=fontfile={FONTE}:text='{cred}':fontsize=34:fontcolor=white:x=(w-text_w)/2:y=18[v]")
    elif a.recorte:
        # Wagner, 11/11: no canto só a CABEÇA, recortada sem o fundo, ocupando cerca de 1/6 da tela, embaixo à esquerda
        pausa = 0.5
        t0 = d - pausa
        laco_a = laco.replace("[1:v]", "[2:v]format=yuva444p,")
        fc = (f"[0:v]trim=start={a.ini}:duration={t0},setpts=PTS-STARTPTS,fps=25,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"tpad=stop_mode=clone:stop_duration={pausa},eq=brightness='if(gte(t,{t0}),-0.18,0)':eval=frame[fundo];"
              f"{laco_a},scale=1080:1920,crop=640:800:220:230,scale=540:-2[rp];"
              f"[fundo][rp]overlay=x=10:y=H-h-170:format=auto[v1];"
              f"[v1]drawbox=x=0:y=60:w=1080:h=72:color=black@0.55:t=fill,"
              f"drawtext=fontfile={FONTE}:text='{cred}':fontsize=34:fontcolor=white:x=(w-text_w)/2:y=78,"
              f"drawtext=fontfile={FONTE}:text='II':fontsize=220:fontcolor=white@0.9:x=(w-text_w)/2:y=520:enable='gte(t,{t0})'[v]")
    else:
        pausa = 0.7  # fim: viral pausa e o rosto cresce
        t0 = d - pausa
        fc = (f"[0:v]trim=start={a.ini}:duration={t0},setpts=PTS-STARTPTS,fps=25,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"tpad=stop_mode=clone:stop_duration={pausa},eq=brightness='if(gte(t,{t0}),-0.18,0)':eval=frame[fundo];"
              f"{laco},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,drawbox=x=0:y=0:w=1080:h=1920:color=white:t=22,"
              f"scale=w='2*trunc((380+700*pow(max(t-{t0},0)/{pausa},2))/2)':h=-2:eval=frame[rp];"
              f"[fundo][rp]overlay=x='40*(1-pow(max(t-{t0},0)/{pausa},2))':y='H-h-150*(1-pow(max(t-{t0},0)/{pausa},2))':eval=frame[v1];"
              f"[v1]drawbox=x=0:y=60:w=1080:h=72:color=black@0.55:t=fill:enable='lt(t,{t0})',"
              f"drawtext=fontfile={FONTE}:text='{cred}':fontsize=34:fontcolor=white:x=(w-text_w)/2:y=78:enable='lt(t,{t0})',"
              f"drawtext=fontfile={FONTE}:text='II':fontsize=220:fontcolor=white@0.9:x=(w-text_w)/2:y=520:enable='between(t,{t0},{t0 + 0.35})'[v]")
    entradas = ["-i", a.viral, "-i", a.rosto] + (["-i", a.recorte] if a.recorte else [])
    roda(["ffmpeg", "-y", "-v", "error", *entradas, "-filter_complex",
          fc + f";[0:a]atrim=start={a.ini}:duration={d},asetpts=PTS-STARTPTS,aresample=48000,volume='if(gte(t,{esp}),0.25,1)':eval=frame[va];"
               f"[1:a]aresample=48000,adelay={int(esp * 1000)}:all=1,volume=1.6[ra];[va][ra]amix=inputs=2:duration=first:normalize=0[a]",
          "-map", "[v]", "-map", "[a]", "-t", str(d), "-r", "25", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-b:a", "160k", a.saida])
    print("abertura pronta:", a.saida)


if __name__ == "__main__":
    main()
