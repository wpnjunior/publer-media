# ESTEIRA DE 30 DIAS — Papo de Médico e Fertilidade a Dois (12/11 a 11/12/2026, sem folga)

Hospital caso 004 (doc: https://claude.ai/artifact/ABfNmo7rfJ4pxEvKXoRr6G). Cada marca tem a SUA rodada diária,
que produz os posts de AMANHÃ, já agenda no Metricool e manda a prévia. O Wagner só veta se quiser
(silêncio = sai). Você roda para UMA marca, dada no pedido: `papo` ou `fertilidade`.

Regra de ouro: o que vai ao ar é byte a byte o que foi para a prévia. Se algo falhar, a vaga fica vazia e você
avisa. Nunca troque mídia, nunca caia para plano B que gaste crédito, nunca gere vídeo de clone para usar a voz.

## 0. Travas (antes de gastar qualquer coisa)
- Datas no fuso America/Bahia. ALVO = amanhã. Leia `esteira2s/grade.json`: `marcas.<marca>.dias[ALVO]`.
  Se não existe (fora do ciclo): encerre. Não há folga (pedido do Wagner em 11/11): toda data do ciclo tem post.
  `tipo` = `ja_agendado`: o post do dia já está no Metricool; faça só os 2 stories (passo 7) e a prévia.
  Entrada com `midia_final`: o vídeo já está editado. Pule os passos 1 a 5 (rode só o Porteiro e o sabor), o tema é
  o campo `tema`. Entrada com `pronto`: o bruto já foi gravado (crédito já gasto). Pule os passos 1, 3, 4 e 4b: o
  tema é o campo `tema`, o roteiro é o `.txt` ao lado do bruto, e o bruto entra direto no editor (passo 5) com a
  edição da grade. Nunca gere voz nem clone para um `pronto`. As fontes (PubMed/DOI) você busca para a legenda e
  para a tela de fonte; se um número falado não tiver fonte, status `falha_fonte`, vaga vazia e aviso.
  Carrossel também vale para o Papo (estilo Papo News, passo 5).
- Pausa: se existe `/mnt/project-files/esteira2s/PAUSADO` ou `/mnt/project-files/esteira2s/PAUSADO-<marca>`, encerre.
- Exemplo já pronto: se `esteira2s/<ALVO>/<marca>/meta.json` (no repositório) tem status `pronto_para_agendar`, a mídia
  já está na mesma pasta (`reels.mp4` ou `01.jpg`...). Não produza de novo: rode o Porteiro e o sabor (só vídeo),
  escreva a legenda (passo 6), faça os stories (7), agende (8) e mande a prévia (9).
- Já feito: se existe `/mnt/project-files/esteira2s/<ALVO>/<marca>/meta.json` com status diferente de `falha`,
  encerre. Senão crie-o com `{"status":"produzindo"}` (trava contra rodada dupla).
- HeyGen `get_current_user`: guarde `premium_credits.remaining` no meta.json como `saldo_antes`.
  Antes de 29/11 20h22Z (renovação), some o gasto do ciclo nos meta.json: passou de `creditos.teto_ate_renovacao`, trate como saldo baixo.
  Se o post do dia usa voz e `saldo - custo_previsto < 40` (`creditos.piso_saldo`), troque o molde por um de
  texto (sem voz) e anote `motivo_troca` no meta.json; a prévia avisa.
- Metricool `getScheduledPosts` do blogId da marca para ALVO (dia inteiro): liste os horários já ocupados.
  Papo: some o Papo News das 20h nos dias ímpares de 15/11 a 11/12 (ele não aparece no Metricool; está em `queue/`).

## 1. Assunto (nunca repetido)
Fontes, nesta ordem: `assunto_sugerido` da grade (se houver); vidIQ (`vidiq_instagram_tiktok_outlier_search`,
`vidiq_outliers`, `vidiq_trending_videos`) com termos dos `focos` da marca em português; o banco de famosos
(https://claude.ai/artifact/BqkpegPkLgzb8rbKkjKdPV, ArtifactData, ou `/mnt/project-files/famosos-saude/`);
notícias médicas das últimas 48 h (WebSearch).
Risque tudo que já foi feito: `diario/TEMAS-PRODUZIDOS.md`, `esteira2s/TEMAS.md`, `diario/*/meta.json`,
`/mnt/project-files/esteira2s/*/*/meta.json` e os posts dos últimos 30 dias da marca no Metricool.
Tema da outra marca também conta como feito para esta (cada conta tem conteúdo próprio).
Precisa de fonte primária (PubMed pelo conector, ou DOI). Sem fonte, descarte. Nota do Jev 0-10 (critérios em
`pipeline/DIARIO-CLOUD.md` passo 2); fique com a maior. Grave candidatos e notas no meta.json.

## 2. Molde e edição
O molde vem da grade. Pode trocar só se o assunto vencedor não couber, e nunca para o molde de ontem da mesma
marca. Rode a skill `agente-de-edicao` (se não estiver disponível, siga a tabela "Qual edição para cada molde" do
estudo https://claude.ai/artifact/2rtBREPj8a56g5PQTyyTXG). Saída: mapa de cenas com cada frase marcada como
ROSTO, NARRAÇÃO ou VIRAL, e custo previsto = segundos de clone novo × 0,9 + segundos de voz × 0,23.
ROSTO sai SEMPRE do Banco de Rostos (passo 4). Clone novo só com ok do Wagner. Custo > 12 → corte frases.

## 3. Roteiro
Siga `esteira2s/GUIA-FALA-ENGAJAMENTO.md` (gancho, retenção, chamada, por molde) e o banco `esteira2s/ASSUNTOS.md`.
Skill `formula-heygen-papo-medico` e `voz-papo-medico` se disponíveis. Fertilidade: tom de acolhimento,
fala ao casal, nunca julga. Fala natural (né, tá, cara, olha só), 90 a 130 palavras para ~40 s.
Proibido: promessa de cura, remédio ou dose, diagnóstico de famoso ("o caso dela levanta uma dúvida comum"),
número sem fonte. Fecho manda procurar o médico. React: até 12 s do viral, @ do autor na tela e na legenda.

## 4. Voz e rosto
- Voz (só se `voz` = true): HeyGen `create_speech_without_player` (ou `create_speech`) com voiceId
  `c4755690737746ffa3bcc01c32d84751`, model `heygen-voice-1`, SEM speed, language ou outputFormat (o speed dá
  erro 500). Depois `ffmpeg -filter:a atempo=1.3`. Chame UMA vez. Falhou: tente de novo uma vez após 60 s;
  falhou de novo, status `falha_voz`, vaga vazia, avise (passo 9). NUNCA gere vídeo de avatar para pegar a voz.
- Rosto: `esteira2s/banco-rostos/indice.json` lista os clipes (tipo abertura | fecho | virada | ouvindo | troca | seguir, arquivo,
  frase, usado_em). Sorteie um do tipo pedido que não foi usado nos últimos 30 dias e grave a data em
  `usado_em`. A frase do clipe entra no roteiro exatamente como está.
- COBRANÇA "SEGUE E CURTE" (todo vídeo, regra do Wagner 11/11): frase bem-humorada no MEIO, logo depois da
  entrega, escrita para o assunto (GUIA seção 4). Vai na narração, com adesivo "segue + curte" e o @ por 2 s.
  Roteiro de rosto: clipe tipo `troca` do banco. `pronto` e `midia_final` já estão falados: neles entra só o
  adesivo na tela, logo depois da virada, sem mexer na fala. Post `ja_agendado` não é alterado.
- Reels de texto NÃO existe mais (Wagner, 11/11: "muito ruim"). Todo Reels tem voz. Saldo baixo = carrossel Papo News no lugar.
- Rosto parado é proibido: em narração só entra imagem (trava no `planejar.py`; o plano precisa de `broll` com fotos do `bg_bank`). Rosto só em clipe do Banco de Rostos ou em bruto gravado inteiro.
- Chaves do plano: `pele` (mesa, noite, jornal, quadro, clinico, arquivo; nunca a mesma em dois Reels seguidos da conta), `broll`, `seguir` {quando, texto, arroba} (adesivo de curte e segue no meio), `caixa_pergunta` (gancho do 1º segundo dentro da caixinha "Faça uma pergunta" do Instagram; usa `titulo`), cena `celular` (comentário ou `modo: manchete`).
- Uma mídia de assinatura por molde (lista em `esteira2s/grade.json`, `regras_edicao.midia_por_molde`): Mito ou verdade = caixinha de pergunta + carimbo do veredito; Notícia de famoso = manchete no celular; Responder comentário = comentário no celular; Linha do tempo = régua; Lista para salvar = checklist; História real = documento e mapa de arquivo; React = tela dividida (viral em cima, rosto embaixo); Tela dividida = rosto em cima e prova embaixo.
- Foto: no máximo 2 por Reels (Wagner, 11/11). A narração sem cena vira FRASE animada (automático no `planejar.py`); `broll` no plano é opcional e só as 2 primeiras entram. Fertilidade nunca usa foto com tag `gravida`.
- Gancho do 1º segundo sempre animado: `caixa_pergunta: true` (Mito), `caixa_pergunta: {estilo: comentario, texto, usuario}` (Responder comentário), cena `celular` modo manchete logo após a abertura (Notícia). Nunca título solto.
- História real com vídeo já gravado: `formato: dinamica` + `estilo_painel: dossie` (como o Rosenhan), rosto o tempo todo.
- React (só tela dividida; veja a decisão abaixo): `python esteira2s/react_abertura.py viral.mp4 esteira2s/banco-rostos/ouvindo_01.mp4 dividida|canto abertura.mp4 --dur 9.6 --credito "@autor"`; a resposta é um Reels normal da esteira (começa com clipe `virada_*`, `titulo` vazio) e junta com `react_abertura.py --juntar abertura.mp4 corpo.mp4 final.mp4`. Viral: trecho de até 10 s, com crédito ao @; baixar só de link público, sem contornar bloqueio do site; nunca diagnosticar quem fala.
- Emenda e respiro (Wagner, 11/11 13h): o `--juntar` corta sozinho o silêncio do começo do corpo (a emenda viral > comentário dava uma travada de 1 s); o `montar_bruto.py` dá sempre 0,5 s de respiro depois de cada fala de rosto antes de entrar a cena. No `react_abertura.py` a frase do viral tem de terminar 1,6 s antes do fim de `--dur` (é onde entra o "Hum, será?"). Vale para os próximos; vídeo pronto não se refaz.
- Antes de gravar a narração, listar os temas da marca na `grade.json` (um react repetiu o assunto de 15/11 por falta dessa conferência). Não fazer react contra "desparasitar pela lua": o app do Wagner usa as fases da lua.
- React, decisão do Wagner (11/11 04h54): SEMPRE em TELA DIVIDIDA (`react_abertura.py ... dividida`). O formato do canto foi reprovado ("ficou ruim"): não usar.
- Clipe de rosto do banco sempre aparece (trava `_rosto_gerado_aparece`): nenhuma cena cobre a fala de verdade, principalmente o "curte e segue".
- HyperFrames (Wagner, 11/11 04h26): nas próximas produções, usar as skills `hyperframes`, `hyperframes-cli` e `hyperframes-registry` para o que for animação pronta: vinheta de abertura, transição entre cenas, título e legenda animados, gráfico animado, glitch, granulado. Antes de desenhar um efeito à mão no `comp.html`, procurar no registry (cerca de 450 blocos). Roda na nuvem (Node 22, FFmpeg e Chrome já instalados; conferido com `npx hyperframes doctor --json`). Na primeira vez da sessão: `npx hyperframes telemetry disable`; nunca rodar `events` nem mandar feedback. Padrão 1080x1920 a 30 fps; quem escolhe a edição continua sendo o agente de edição e a grade. A peça HyperFrames entra como abertura, transição ou cena e junta com o resto pelo filtro concat.
- Norte de tudo: viralizar (gancho no 1º segundo, corte a cada 2 a 4 s, cobrança no meio, um pedido só no fim).

## 4b. Montar o bruto (sem clone novo)
`python esteira2s/montar_bruto.py montagem.json /tmp/e2s/bruto.mp4`: clipes ROSTO do banco + trechos de
narração sobre a foto parada (use `esteira2s/banco-rostos/foto.jpg`, um quadro do clipe "ouvindo", para o
fundo bater com o rosto; se faltar, `reel_kit/foto_wagner.png`). Esse bruto entra no editor no lugar do vídeo
do HeyGen. React: o viral entra como cena do plano, não como trecho do bruto.

## 5. Edição e Porteiro
(`pip install -q playwright faster-whisper pillow` antes.)
Editor: `bash reel_kit/diario/editar.sh` (formatos tela_dividida, dinamica + dossie/celular, mapeamento;
modelos em `reel_kit/diario/exemplo_plano*.json`). Linha do tempo = cenas `regua` (marcos, `ate` sobe a cada cena); Lista para salvar = cenas `checklist` (itens, `marcados` sobe a cada cena), ambas no formato mapeamento. Corrija pelo plano.json, nunca pelo timeline.json.
Carrossel (regra do Wagner, 11/11: TODO carrossel, das duas contas, sai no estilo Papo News): monte o JSON como
`pipeline/exemplo_news.json` e rode `NEWS_OUT=pasta python pipeline/template_news.py news.json` e depois
`python esteira2s/fotografar_news.py pasta` (gera 01.jpg... em 1080x1350; nenhum slide pode dar VAZA). Selo:
`"marca":["PAPO","NEWS"]` no Papo e `["FERTILIDADE","A DOIS"]` na Fertilidade. 6 a 7 slides: capa com foto forte e
manchete curta com a palavra-chave em `<span class="hl">`; internos numerados; a cobrança de seguir e curtir num
slide do meio; último slide com a chamada no `destaque` e a fonte com DOI + "Conteúdo educativo — não substitui
consulta médica." Fotos do `bg_bank/` (veja `index.json`); faltando foto que combine, baixe do Pexels
(`images.pexels.com`), confira olhando e acrescente ao banco. `telas.py` fica só para os stories.
Porteiro (todos têm que passar; senão ajuste e rode de novo, no máximo 3 vezes, depois `falha_edicao`):
volume medido a cada 3 s sem buraco; quadros em volta de cada emenda; boca do rosto sem sorriso com dentes e
sem dedos contando; nenhuma tela vazia; legenda dentro da tela; @ do autor visível no react; duração 25-75 s;
arquivo final < 48 MB. Depois o sabor: `pipeline/sabor/camuflar_forte.py` + `conferir_sabor.py` (tem que sair 0).

Edições HyperFrames (linguagens novas, 11/11): bruto pelo `montar_bruto.py`, palavras pelo `transcrever.py`, depois
`python esteira2s/hf/<edicao>.py bruto.mp4 words.json plano.json projeto_dir saida.mp4`. `notas.py` = lista no bloco
de notas + cartão (a lista inteira fica ANTES do rosto do meio; depois dele só o cartão); `dossie.py` = linguagem
`arquivo` (pasta, folhas batidas à máquina, carimbo), para história real; `conversa.py` = conversa de mensagens,
para pergunta de seguidor e relato. Balão, item ou folha nova a cada 6 s no máximo, senão o Porteiro reprova.

## 6. Legenda
Própria desta marca (nunca o texto da outra conta). Skills `instagram-agent:ig-caption` e `ig-human`.
Primeira linha que segura antes do "mais", corpo curto, uma chamada só, fonte com DOI, "Converse com seu médico".
Até 5 hashtags, conjunto diferente do usado pela outra marca e do post anterior desta. Título do YouTube Short.

## 7. Stories (2 por dia, todos os dias)
`esteira2s/telas.py` com formato `story` gera 2 cartões 1080x1920 (uma tela por spec): (1) chamada para o post de amanhã (ou, em dia `ja_agendado`, para o post de hoje); (2) uma pergunta para responder no direct. Horários: o 1º 1 a 2 h depois do post, o 2º à
noite (20h-22h), minutos sorteados.

## 8. Publicar a mídia e agendar
- Comite `esteira2s/<ALVO>/<marca>/` (mídia final, roteiro, plano, legenda, meta.json) e os índices mudados
  (`banco-rostos/indice.json`, `TEMAS.md`) no seu branch e dê push. URL da mídia = raw do GitHub PELO SHA do
  commit (`https://raw.githubusercontent.com/wpnjunior/publer-media/<sha>/...`; a URL pelo nome do branch pode
  vir 404 em cache). Confira 200 e content-length = tamanho do arquivo. Copie também para
  `/mnt/project-files/esteira2s/<ALVO>/<marca>/`.
- Horário: sorteie um minuto dentro da `janela` da grade que fique a 3 h ou mais de qualquer post da marca
  naquele dia (Metricool + Papo News) e que não seja minuto redondo (:00, :15, :30, :45).
- Metricool `createScheduledPost`, blogId da marca, autoPublish true, publicationDate {dateTime, timezone
  America/Sao_Paulo}. Reels: providers instagram + tiktok + youtube; instagramData {type REEL, showReelOnFeed
  true, isAiGenerated = true se tem voz/rosto de IA}; tiktokData {privacyOption PUBLIC_TO_EVERYONE, isAigc
  idem, title}; youtubeData {title, type short, privacy public, madeForKids false, category EDUCATION,
  isAiGeneratedContent idem}. Carrossel: só instagram, type POST, media = as telas na ordem.
  Stories: instagram type STORY, sem text.
- Grave no meta.json: status `agendado`, metricool_id e uuid de cada post, horário, raw_url, tamanho_bytes,
  sha, custo real (saldo depois − antes), tema, molde, edição, nota do Jev, fontes, legenda.
- Acrescente o tema em `esteira2s/TEMAS.md` (data, marca, tema, molde).

## 9. Prévia
A rodada roda na própria thread dona do fluxo: mande você mesmo UMA mensagem curta ao Wagner com a mídia anexada,
o horário e como vetar ("Não postar" na aba Programação 30 dias da Mesa, ou responder na thread). Atualize o doc
`programacao/<ALVO>` da Mesa da marca (status, titulo, horario, link). Em falha (voz, edição, saldo), grave o
status e avise em uma linha.

## Veto
"não posta", "segura", "não posta <marca>" ou "pausa tudo" antes do horário → `updateScheduledPost` do mesmo
post com `draft: true` (conteúdo idêntico), status `vetado` no meta.json. "pausa tudo" também cria
`/mnt/project-files/esteira2s/PAUSADO`.

## Fotos e letra do carrossel (Wagner, 11/11)

- Fotos: usar o banco novo `bg_bank/px_<assunto>_<id>.jpg` (83 fotos Pexels, tags em `bg_bank/index.json`); não repetir a mesma foto no mesmo carrossel nem em carrosséis da mesma semana. Faltou assunto: buscar no Pexels (WebSearch em pexels.com dá o id; baixar por `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=1260`), olhar a foto antes de usar e registrar no índice.
- Letra: o molde Papo News cresce o texto sozinho até sobrar só a faixa de foto no alto (variável `--k` em `pipeline/template_news.py`). Manchete curta (até 4 palavras por linha, com `<br>`) é o que deixa a letra grande.

## Erros, causas e travas (regra do Wagner, 11/11: identificar todo erro, ver por que errou e criar mecanismo para não repetir)

Todo erro novo entra aqui na hora, nas três colunas. Erro sem trava não está resolvido.

| Erro | Por que aconteceu | Trava (mecanismo) |
| --- | --- | --- |
| Edições "sempre as mesmas" (reclamado 2 vezes em 11/11) | Troquei só a `pele` (cor e cenário); o esqueleto frase + cartão + etiqueta era igual. Conferi como autor, não como espectador. | `python esteira2s/trava_mesmice.py DATA MARCA LINGUAGEM` antes de produzir: a linguagem não pode repetir a dos 3 Reels anteriores da conta. Todo `meta.json` de Reels grava `linguagem`. Linguagem nova só mostrando 1 exemplo ao Wagner antes do lote. |
| Reels de lista (notas) com papel em branco por 12 s | Pus itens da lista depois do rosto do meio; a edição `notas` troca para o cartão ali. | Montagem: todos os itens antes do rosto do meio (pode ter 2 trechos de voz seguidos). Porteiro acusa tela parada. |
| React com rosto no canto "ficou ruim" | Produzi 2 formatos sem ele pedir o segundo desse jeito. | React só em tela dividida; `react_abertura.py ... dividida`. |
| MKUltra com avatar antigo | Reaproveitei bruto de outubro para economizar crédito, sem checar o avatar. | Vídeo com rosto só entra se o avatar for o 1d7e. Bruto antigo de `prontos/` de documentário nunca é publicado; regrava-se com o mesmo roteiro. |
| Foto de grávida na Fertilidade | Banco de fotos sem etiqueta de conteúdo sensível. | Tag `gravida` no `bg_bank/index.json`; Fertilidade nunca usa foto com essa tag. Na dúvida, marca e troca. |
| Fotos demais no Reels | Preenchi a narração com banco de imagem. | No máximo 2 fotos por Reels (`planejar.py` corta). |
| Gancho em título branco "sem graça" | Título solto no 1º segundo. | Gancho sempre animado (caixinha, comentário digitado, manchete). |
| Gráfico de barras cortado na lateral | 3 barras não cabem em 1080 px. | Cena `barra` com no máximo 2 barras; conferir a folha de quadros antes de salvar. |
| Rosto coberto na cobrança de seguir | Cena gráfica por cima do clipe de rosto. | Trava `_rosto_gerado_aparece` no `planejar.py`. |
| Narração gerada como vídeo do clone (49 créditos em vez de ~21, 10/11) | Usei vídeo para obter a voz. | Narração só em áudio (`create_speech`); clone só onde o rosto aparece. |
| Reel da vacina saiu sem edição (09/11) | Arquivo editado não existia; plano B publicado sem ok. | Só publica a mídia aprovada; `porteiro.py` e conferência do arquivo antes de agendar. |
| Perda de foco na entrega (Wagner, 11/11: "se perdeu nas produções, na organização, na meta e em entregar tudo pronto") | Cada pedido virou frente nova sem fechar a anterior; "pronto" era "arquivo existe"; estado espalhado em 5 lugares; aviso por peça. | `python3 esteira2s/quadro.py` é o quadro único. Pronto só conta agendado. Entrega por lote na ordem do calendário; pedido novo entra na fila com vaga no lote. Um aviso por lote, com o quadro. |
| 3 "prontos" de outubro (whey, ereção, glúten) contados como prontos com avatar antigo | Marquei `pronto` na grade sem abrir o vídeo. | Antes de marcar pronto, tirar um quadro do rosto e comparar com `banco-rostos` (jaleco branco = 1d7e). Vale para qualquer arquivo de `prontos/` e dos acervos antigos: aproveita-se roteiro e fonte, nunca o vídeo. |
| Ofereci refazer Reels já prontos | Não separei "corrigir o próximo" de "refazer o feito". | Mudança de regra vale para os próximos; o pronto não se refaz. |

Conferência final de todo Reels, olhando como espectador: (1) trava da mesmice passou; (2) folha de quadros aberta e olhada; (3) nenhum texto cortado; (4) rosto visível na cobrança; (5) fonte com DOI no fim.
