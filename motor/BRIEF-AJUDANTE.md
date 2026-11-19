# Brief comum dos ajudantes de edição (14/11/2026)

Você refaz UM react do Dr. Wagner (perfis de saúde) no motor `/tmp/claude-0/motor`. Eu (thread principal) faço o Cariani ao mesmo tempo, e depois cuido de sabor, upload, Metricool, fichas e envio ao Wagner. Você NÃO publica nada, NÃO mexe no Metricool, NÃO faz commit.

## Leia antes (nesta ordem)
1. Memória: `/tmp/claude/memory/team/silo/regra-react-fisiologia-leigo.md`, `regra-dublagem-viral-estrangeiro.md`, `regra-leitura-cartelas.md`, `regra-entrada-olha-noticia.md`, `feedback-audio-sem-buraco.md`, `regra-banco-rostos-reuso.md`.
2. `/mnt/project-files/reacts/BRIEF-ROTEIRO-REACT.md` (inteiro, sobretudo a seção "REGRAS NOVAS 14/11").
3. `/mnt/project-files/reacts/ESTADO-LOTE.md` (a parte do seu vídeo).
4. O script de plano atual do seu vídeo e `scripts/mk.py` (helpers abertura, rosto_r1, rosto_r2, B, T, F, salvar), `fisio.py` (camada nova "fisio" com órgãos animados, setas e partículas; veja o docstring/ART), `broll.py` (b-roll grátis Mixkit), `scripts/pele.py`, `scripts/entrada.py`.

/mnt/project-files é montagem de rede: use barra no fim do caminho, nunca busque na pasta inteira, releia um arquivo uns 10 s depois de gravar.

## O que o Wagner pediu (regras novas, obrigatórias)
1. Transcreva a fala inteira do viral (já existe em `assets/midia/<P>_viral.words.json`) e responda SÓ ao que aparece no trecho: concorda, discorda ou meia verdade. Nunca rebater algo que não foi dito.
2. "Aula rápida" de 10 a 20 s em linguagem de leigo, com um exemplo do dia a dia, usando a camada `fisio` (desenho do órgão atuando) EM CIMA DE B-ROLL que encaixe com a explicação (camada `video` em tela cheia + fundo escuro semitransparente + fisio por cima). "Hora de fazer algo incrível." Corpo normal = fisiologia; doença = fisiopatologia; remédio = mecanismo de ação (sem marca, sem dose).
3. Viral mudo, em outra língua ou difícil de entender: voz Murilo (`d703f08d1ef34302a36945aa3efc7b3f`) dá o contexto/dubla; viral fica com gain ~0.16 por baixo. Salvar como `assets/midia/<P>_ctx_voz.wav` (sufixo `_voz`). Entradas de dublagem/contexto no plano sem "palavras".
4. Depois da aula, o estudo com número e fonte verificados (PubMed MCP se precisar conferir). Sem número inventado.

## Regras de sempre
- React em tela dividida; 0,5 s de folga depois que a fala termina antes do próximo corte; sem rosto parado em narração; cartela ≥1,5 s e sem termo técnico; nunca silêncio (bip/efeito); efeitos somem devagar.
- CFM: criticar a afirmação, não a pessoa; nenhum nome de remédio ou marca (vira bip); sem dose; sem promessa de cura; nunca sugerir que o famoso usa ou tem algo. TDAH: nunca diagnosticar; dizer "o sistema de recompensa que usa dopamina responde diferente", não "falta de dopamina" como fato.
- Rostos: avatar novo 6cd9 (`6cd9ee3df3544397ad8d38fa091e14cc`, digital twin, look "Wagner Podcast -- 55"). REUSE do banco primeiro (`python3 banco.py procurar ...`): já existem `ent6.mp4` (entrada_fala "Olha só o que falaram aqui", 1,88 s) e `cta6.mp4` (cta "Se essa aula valeu, segue e curte. É o treino do dedão de hoje.", 4,12 s) do 6cd9 em `/mnt/project-files/esteira2s/banco-rostos/`. Gere no HeyGen só o rosto da reação r1 (1 vídeo curto, create_video_from_avatar com audioAssetId do trecho de voz, 9:16, 1080p, motionPrompt calmo, sem sorrisão). Upload para HeyGen sempre de arquivo local em /tmp, não de /mnt.
- Voz da narração: HeyGen create_speech com voz `c4755690737746ffa3bcc01c32d84751` (clone do Wagner), language pt, withTimestamps; depois `ffmpeg -filter:a atempo=1.3`; tempos das palavras ÷ 1,3. ElevenLabs NÃO está liberado. Créditos HeyGen liberados com moderação (só o necessário).
- Não leia .env nem chaves. Não rode `npx hyperframes events` nem envie feedback.

## Renderizar
- NÃO renderize em paralelo. Grave o plano em `planos/<id>.json` (via seu script em `scripts/`), depois coloque o id numa linha nova de `saida/fila.txt` (o `fila_viva.sh` já roda e pega). Se o id já estiver em `saida/feitos.txt`, remova a linha de lá para reenfileirar. O vídeo sai em `saida/<id>.mp4` e o resultado dos portões em `saida/<id>.gate` (FIM no final).
- Antes de enfileirar, teste quadros: `npx hyperframes snapshot --at t1,t2 --no-end -o dir` dentro da pasta do HTML gerado (veja como fazer.sh gera) ou use o que o fazer.sh faz; olhe os quadros da aula.
- Portões: parado ≤10%, maior_parado ≤3 s, LUFS -16..-12, buraco <1,2 s. Se reprovar, corrija e reenfileire.
- Só áudio mudou: `./remix.sh <id>`.

## Entregue (mensagem final, curta)
Caminho do mp4 final, resultado dos portões, duração, a transcrição do viral, o roteiro novo (texto da narração), as fontes do estudo (DOI) e quantos créditos HeyGen gastou. Faça backup do plano antigo (`.v<n>.json`) antes de sobrescrever.

## Adendo 14/11 02h (vale para todos)
- Vários ajudantes trabalham ao mesmo tempo. NÃO edite arquivos compartilhados do motor (gerar.py, fisio.py, mk.py, pele.py, mix.py, entrada.py, portoes.py, fazer.sh, fila*.sh). Órgão novo para a aula = criar `fisio_extra/<nome>.svg` só com o `<g>...</g>` (centro 0,0; cabe em ±200; traço grosso como os de fisio.py) e usar `"k":"<nome>"`.
- Modelos prontos do padrão novo: `scripts/plano_cariani2.py` (BR() = b-roll em tela cheia + véu rgba(6,14,11,.6); TT() = texto sobre b-roll; cenas fisio; `fixo:True` nas camadas que a pele não deve recolorir; trilha m_investiga baixinha sob a aula), `scripts/plano_cafe.py`, `scripts/plano_figado.py`.
- Banco de rostos 6cd9: `ent6.mp4` e `cta6.mp4` em /mnt/project-files/esteira2s/banco-rostos/ já têm `.words.json`.
- Mixkit: a página de categoria às vezes bloqueia (429); o CDN assets.mixkit.co baixa direto; quando o 1080 der acesso negado, use o -720.mp4 (broll.py já faz isso). Corte o b-roll em vertical 1080x1920 antes (ffmpeg crop=ih*9/16:ih,scale=1080:1920).
- Carimbo sobre fundo escuro: `"blend":"normal"` e `"css":"background:rgba(255,255,255,.9)"` (o padrão multiply some no escuro).
- Créditos HeyGen estão curtos (~60 para todos, renova 29/11): gaste só o que a sua tarefa disser.
