# Motor de edição dos Reels (caso 006 do Hospital)

Um motor só para todos os perfis. Lê um plano em JSON (camadas com tempo) e monta o vídeo vertical 1080x1920
em HTML + GSAP, renderizado pelo HyperFrames 0.9.42 (versão travada). O áudio é mixado à parte pelo ffmpeg.

```
./fazer.sh <id>            # planos/<id>.json -> saida/<id>.mp4
python3 portoes.py saida/<id>.mp4   # mede tela parada, maior trecho sem mudança e volume; REPROVADO barra a entrega
```

- `gerar.py`: plano -> `amostras/<id>/index.html`. Tipos de camada: fundo, foto, video, recorte (rosto com fundo
  transparente .webm), cartao, desenho (círculo, seta, sublinhado, x, check, caixa, linha à mão), texto, gigante,
  carimbo, numero (contador 3D), celular (com notificações), mapa (câmera, pinos, rotas com avião), regua (linha do
  tempo), artigo (página de estudo 3D com grifo), pergunta (caixinha do Instagram), comentario, manchete, checklist,
  barra, flash, glitch, progresso, vinheta, grao, cta. Legendas: lima, serif, pilula, manuscrita, maquina, gigante.
- `mix.py`: voz + viral num barramento, trilha com ducking (sidechain), efeitos; master -14 LUFS.
- `portoes.py`: limites calibrados no Reels Rosenhan (tela quase parada 8,4% com este instrumento).
- `planos/`: as 6 amostras do caso 006 (B história no mapa, C mito ou verdade 3D, D notícia de famoso, E caderno com
  humor, F dossiê secreto, react completo do glúten).

Fora do git (pôr em `assets/` antes de rodar): `assets/midia/` (vídeos do clone, prontos, virais e `.words.json`
do faster-whisper) e `assets/som/` (trilhas e efeitos: m_noticia, m_investiga, m_tensao, m_humor, m_emocao,
m_viagem, whoosh, whoosh2, boom, glitch, notif, boing, pagina, papel, teclado, scratch, riser). As trilhas vieram da
biblioteca de sons do HeyGen; confirmar licença antes de publicar. Fontes em `assets/fonts/` são OFL.

Recorte do rosto: `npx hyperframes remove-background in.mp4 -o out.webm --quality best` (CPU, ~0,6 a 0,9 s por
quadro). Fazer uma vez por clipe e guardar.
