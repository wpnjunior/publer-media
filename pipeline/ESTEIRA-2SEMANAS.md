# ESTEIRA DE 2 SEMANAS — Papo de Médico e Fertilidade a Dois (14 a 27/11/2026)

Hospital caso 004 (doc: https://claude.ai/artifact/ABfNmo7rfJ4pxEvKXoRr6G). Cada marca tem a SUA rodada diária,
que produz os posts de AMANHÃ, já agenda no Metricool e manda a prévia. O Wagner só veta se quiser
(silêncio = sai). Você roda para UMA marca, dada no pedido: `papo` ou `fertilidade`.

Regra de ouro: o que vai ao ar é byte a byte o que foi para a prévia. Se algo falhar, a vaga fica vazia e você
avisa. Nunca troque mídia, nunca caia para plano B que gaste crédito, nunca gere vídeo de clone para usar a voz.

## 0. Travas (antes de gastar qualquer coisa)
- Datas no fuso America/Bahia. ALVO = amanhã. Leia `esteira2s/grade.json`: `marcas.<marca>.dias[ALVO]`.
  Se não existe (fora do ciclo) ou `tipo` = `folga`: faça só os 2 stories (passo 7) e encerre.
- Pausa: se existe `/mnt/project-files/esteira2s/PAUSADO` ou `/mnt/project-files/esteira2s/PAUSADO-<marca>`, encerre.
- Já feito: se existe `/mnt/project-files/esteira2s/<ALVO>/<marca>/meta.json` com status diferente de `falha`,
  encerre. Senão crie-o com `{"status":"produzindo"}` (trava contra rodada dupla).
- HeyGen `get_current_user`: guarde `premium_credits.remaining` no meta.json como `saldo_antes`.
  Se o post do dia usa voz e `saldo - custo_previsto < 40` (`creditos.piso_saldo`), troque o molde por um de
  texto (sem voz) e anote `motivo_troca` no meta.json; a prévia avisa.
- Metricool `getScheduledPosts` do blogId da marca para ALVO (dia inteiro): liste os horários já ocupados.
  Papo: some o Papo News das 20h nos dias ímpares de 15 a 27/11 (ele não aparece no Metricool; está em `queue/`).

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
Skill `formula-heygen-papo-medico` e `voz-papo-medico` se disponíveis. Fertilidade: tom de acolhimento,
fala ao casal, nunca julga. Fala natural (né, tá, cara, olha só), 90 a 130 palavras para ~40 s.
Proibido: promessa de cura, remédio ou dose, diagnóstico de famoso ("o caso dela levanta uma dúvida comum"),
número sem fonte. Fecho manda procurar o médico. React: até 12 s do viral, @ do autor na tela e na legenda.

## 4. Voz e rosto
- Voz (só se `voz` = true): HeyGen `create_speech_without_player` (ou `create_speech`) com voiceId
  `c4755690737746ffa3bcc01c32d84751`, model `heygen-voice-1`, SEM speed, language ou outputFormat (o speed dá
  erro 500). Depois `ffmpeg -filter:a atempo=1.3`. Chame UMA vez. Falhou: tente de novo uma vez após 60 s;
  falhou de novo, status `falha_voz`, vaga vazia, avise (passo 9). NUNCA gere vídeo de avatar para pegar a voz.
- Rosto: `esteira2s/banco-rostos/indice.json` lista os clipes (tipo abertura | fecho | ouvindo, arquivo,
  frase, usado_em). Sorteie um do tipo pedido que não foi usado nos últimos 30 dias e grave a data em
  `usado_em`. A frase do clipe entra no roteiro exatamente como está.
- Sem voz: Reels de texto com trilha de `reel_kit/trilhas/` (nunca música de terceiros).

## 5. Edição e Porteiro
Editor: `bash reel_kit/diario/editar.sh` (formatos tela_dividida, dinamica + dossie/celular, mapeamento;
modelos em `reel_kit/diario/exemplo_plano*.json`). Corrija pelo plano.json, nunca pelo timeline.json.
Carrossel: `esteira2s/carrossel.py` (1080x1350, 6 a 8 telas, capa que faz deslizar, última tela com a
chamada e "conteúdo educativo, não substitui consulta").
Porteiro (todos têm que passar; senão ajuste e rode de novo, no máximo 3 vezes, depois `falha_edicao`):
volume medido a cada 3 s sem buraco; quadros em volta de cada emenda; boca do rosto sem sorriso com dentes e
sem dedos contando; nenhuma tela vazia; legenda dentro da tela; @ do autor visível no react; duração 25-75 s;
arquivo final < 48 MB. Depois o sabor: `pipeline/sabor/camuflar_forte.py` + `conferir_sabor.py` (tem que sair 0).

## 6. Legenda
Própria desta marca (nunca o texto da outra conta). Skills `instagram-agent:ig-caption` e `ig-human`.
Primeira linha que segura antes do "mais", corpo curto, uma chamada só, fonte com DOI, "Converse com seu médico".
Até 5 hashtags, conjunto diferente do usado pela outra marca e do post anterior desta. Título do YouTube Short.

## 7. Stories (2 por dia, também nos dias de folga)
`esteira2s/stories.py` gera 2 cartões 1080x1920: (1) chamada para o post de amanhã (ou, na folga, uma dica
curta com fonte); (2) uma pergunta para responder no direct. Horários: o 1º 1 a 2 h depois do post, o 2º à
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
Dispare a tarefa de prévia (fire_trigger, id em `esteira2s/README.md`) com o texto
`PRÉVIA <marca> <ALVO>`. Ela manda ao Wagner a mídia, o horário e a regra do veto. Você não fala com o Wagner.
Em falha (voz, edição, saldo), grave o status e dispare a prévia do mesmo jeito: ela avisa em uma linha.
Termine com 4 linhas: marca e data, tema e nota, molde e edição, custo e status.

## Veto (feito pela tarefa de prévia, não por você)
"não posta", "segura", "não posta <marca>" ou "pausa tudo" antes do horário → `updateScheduledPost` do mesmo
post com `draft: true` (conteúdo idêntico), status `vetado` no meta.json. "pausa tudo" também cria
`/mnt/project-files/esteira2s/PAUSADO`.
