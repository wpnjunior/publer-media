# Brief do lote 2: react NOVO completo (14/11/2026, prazo: pronto até 11h30 BRT = 14h30 UTC)

Você produz UM react novo do começo ao fim no motor `/tmp/claude-0/motor`. Eu (thread principal) faço sabor, upload, Metricool, ficha e envio ao Wagner. Você NÃO publica, NÃO mexe no Metricool, NÃO faz commit.

## Leia antes (rápido, só o necessário)
1. `BRIEF-AJUDANTE.md` (regras, render em fila, portões) e os dois adendos de 14/11 no fim de `BRIEF-REMAKE-AULA.md` ("VARIAR A EDIÇÃO DA AULA" e "VOZ COM EMOÇÃO E RITMO CALMO").
2. Memória: `/tmp/claude/memory/team/silo/regra-ritmo-voz-e-regua-da-vo.md`, `regra-variar-edicao-aula.md`, `regra-react-fisiologia-leigo.md`, `regra-entrada-olha-noticia.md`, `regra-dublagem-viral-estrangeiro.md`, `regra-leitura-cartelas.md`, `feedback-audio-sem-buraco.md`.
3. A pasta do seu tema em `/mnt/project-files/reacts/lote2/<perfil>/<slug>/` (dossie.md, roteiro.json com narração, aula, estudos, manchete, caixinha, legenda, stories, títulos; viral.mp4; words.json; traducao_pt.json quando estrangeiro). /mnt/project-files é rede: barra no fim, nunca buscar na pasta inteira; copie o viral para `assets/midia/` (mídia viral nunca vai para o git).
4. Modelos de script: `scripts/plano_cariani2.py` (estrutura completa: entrada, viral em tela dividida, r1, narração, aula, estudo, CTA, fecho), `scripts/plano_ivete_aula.py`, `scripts/plano_tdah_invencao_aula.py`.

## Estrutura do vídeo (todas obrigatórias)
1. Entrada: banco `ent6.mp4` ("Olha só o que falaram aqui", 1,88 s, avatar 6cd9, em /mnt/project-files/esteira2s/banco-rostos/ com words.json) ou, se o viral for notícia, gere "Olha só essa notícia." no rosto do mesmo avatar só se não houver no banco (`python3 banco.py procurar`). Manchete animada por cima.
2. Viral em TELA DIVIDIDA com a caixinha de pergunta do Instagram (Mito ou verdade). Estrangeiro = dublagem Murilo (`d703f08d1ef34302a36945aa3efc7b3f`, viral a gain ~0.16), texto em traducao_pt.json / roteiro.dublagem_murilo.
3. Rosto r1 (reação curta, 2-4 s): create_video_from_avatar com o avatar 6cd9 (`6cd9ee3df3544397ad8d38fa091e14cc`, look "Wagner Podcast -- 55"), audioAssetId do bloco de voz da reação (upload do wav LOCAL de /tmp), 9:16, 1080p, motionPrompt calmo, sem sorrisão. Corte logo depois da última palavra (+0,5 s de folga antes da próxima cena).
4. Narração SÓ voz, em blocos por clima (adendo da voz: indignado/alegre/manso/neutro com speed, pitchVariance, pitchShift e `<break time="0.7s"/>`; SEM atempo). Responder só ao que o viral disse no trecho.
5. Aula para leigo (régua da vó), 12-20 s, na EDIÇÃO indicada no seu pedido (não use b-roll se o pedido disser outra). Uma ideia por cena; desenhos novos em `fisio_extra/<nome>.svg` (só o `<g>`, centro 0,0, cabe em ±200, traço grosso como fisio.py).
6. Estudo com número e fonte (DOI do roteiro; conferir no PubMed se tiver dúvida).
7. CTA do banco `cta6.mp4` (4,12 s) e fecho curto.
CFM: criticar a afirmação, não a pessoa; sem marca/remédio (bip, nunca silêncio); sem dose; sem promessa de cura; nunca sugerir que o famoso usa ou tem algo; Fertilidade nunca brinca com não engravidar; TDAH nunca diagnostica nem diz "falta de dopamina"; Caneta nunca indica nem contraindica.

## Créditos HeyGen (saldo alto, mas sem desperdício)
Voz: 3-4 blocos, teto ~14 créditos. Rosto r1: 1 vídeo curto (~5-8 créditos). Dublagem Murilo se precisar (~2-4). Teto total 26 por vídeo. Confira o saldo (get_current_user) antes e depois.

## Render
Plano em `planos/react_l2_<slug_curto>.json` via `scripts/plano_l2_<slug_curto>.py`. Pele: escolha uma diferente de lab se o perfil já tem muitos lab (lab|dossie|noticia|lousa). Rode audio_plano e leitura, olhe snapshots da aula e das emendas. Render: um por vez na máquina toda; se nenhum hyperframes estiver rodando (`pgrep -af "hyperframes render"`), rode `./fila.sh <id>`; senão espere (cheque a cada ~60 s) e então rode. Portões: parado ≤10%, maior_parado ≤3 s, LUFS -16..-12, buraco <1,2 s.

## Entregue (curto)
Caminho do mp4, portões, duração, palavras/min da narração, transcrição do trecho do viral, texto da narração, fontes (DOI), legenda final, 2 stories (rótulo/título/texto), títulos YouTube/TikTok, créditos gastos, e qualquer ponto CFM que o Wagner possa querer vetar.
