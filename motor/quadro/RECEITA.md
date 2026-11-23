# Edição "Quadro" (papel infinito desenhado a lápis)

Copiada da **estrutura de edição** de um Reels de referência que o Wagner mandou em 23/11/2026
(perfil de estrategista de conteúdo, série sobre "adultos de 30 que ainda são adolescentes", 2 min 54 s, 34 mil curtidas).
Não copiamos texto, desenho nem marca: só a gramática da edição.

## O que a referência faz (medido)
- Fundo único: papel bege claro com grão. Nenhum rosto na narração; só voz.
- **Um quadro gigante**: cada ideia é desenhada numa área do papel e a câmera desliza para a próxima. No fim a
  câmera **afasta e mostra o mapa inteiro** ("tudo isso é a parte 1"), o momento mais "salvável".
- **Lápis visível** desenhando cada traço e escrevendo cada palavra (é ele que dá o movimento constante).
- Poucas cores: tinta marrom, verde nos sublinhados e setas, mostarda de marca-texto, rosa de pele.
- Recursos que se repetem: número grande; palavra-chave com marca-texto; palavra riscada ("frescura", "preguiça");
  etiqueta com losango ("parte 1 de 3"); setas manuscritas; foto/livro como polaroide; gráfico simples desenhado.
- Algo novo a cada 1 a 2 s, câmera parada só enquanto o lápis desenha.
- Legenda pequena numa caixinha branca embaixo à esquerda, 3 a 6 palavras por vez (não compete com o desenho).
- Som: narração protagonista, trilha calma bem baixa, master perto de -14 LUFS.
- CTA desenhado: "Siga esse perfil" + botão "Seguindo ✓" + balão de comentário.

## Como usamos no motor
1. Roteiro de leigo (régua da vó), aula de fisiologia em desenho, estudo com nome e ano.
2. Voz só áudio (HeyGen `create_speech` com timestamps ou ElevenLabs) e depois
   `python3 voz_quadro.py voz_raw.wav words_raw.txt pasta` (atempo 1,15 e pausa de 0,75 s entre frases).
3. Plano JSON com cenas (`origem` no quadro, `t` de entrada, `deriva` para passear dentro da cena) e elementos:
   `texto`, `marca`, `riscar`, `etiqueta`, `linha`, `seta`, `circulo`, `caixa`, `onda`, `check`, `xis`, `foto`
   (com `video` do banco de rostos), `botao` e desenhos prontos `relogio`, `estomago`, `bateria`, `prato`,
   `copo`, `boneco`. `afastar` faz o zoom final do mapa inteiro. Modelo: `planos/quadro_grelina.json`.
4. `./fazer_quadro.sh plano.json pasta musica.wav` (gera, renderiza no HyperFrames 0.9.42, mixa com SFX Kit, junta).
5. CTA: clipe do banco de rostos (avatar padrão) numa polaroide, sem gastar crédito.

## Quando o Jev escolhe o Quadro
- Tema de explicação de mecanismo (hormônio, fisiologia, "por que acontece") ou série em partes.
- Não usar em react (react é tela dividida) nem duas vezes seguidas no mesmo perfil.
- Cuidado: é narração sem rosto. Por isso o rosto entra no CTA e, se o tema pedir, numa polaroide curta no meio.

## Portões
O `portoes.py` foi calibrado no Rosenhan (≤10% de tela quase parada). Traço fino em papel liso muda poucos pixels,
então o Quadro sempre "reprova" nessa régua: a própria referência mede 52,8%; a amostra da grelina mede 77,5%
(maior trecho sem mudança 4,5 s). Régua do Quadro = a referência. Próximo passo para chegar perto: mais elementos
por cena e passeio de câmera mais largo.
