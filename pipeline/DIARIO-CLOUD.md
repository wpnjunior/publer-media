# VÍDEO DIÁRIO DO PAPO DE MÉDICO (@dr.wagnernovaesjr) — você produz e edita; a publicação é às 18h

Ordem do Dr. Wagner em 10/11/2026: "no Papo de Médico ele vai achar o tema mais viral do dia, avaliar qual o
Jev acha que tem maior potencial de viralizar, fazer um vídeo no HeyGen com meu avatar e minha voz no molde
padrão dos últimos, voz 1.3x, editar com a edição que mais tem a cara do vídeo e publicar sempre às 18h; o
processo pode iniciar às 8 da manhã". Isso é autorização permanente para gerar 1 vídeo por dia no HeyGen.

Quem publica NÃO é você: você entrega a pasta `diario/AAAA-MM-DD/` com o vídeo editado e chama a prévia.
A thread "Automatizar vídeo diário do Papo de Médico" manda a prévia ao Wagner, segura o veto até 17h e agenda
no Metricool para 18h (Instagram, TikTok e YouTube).

## 0. Travas (antes de gastar qualquer coisa)
- Código: o editor vive em `reel_kit/diario/`. Se essa pasta não existir no master, traga do branch de trabalho
  sem comitar: `git fetch origin claude/project-thread-wkec50 && git checkout origin/claude/project-thread-wkec50 --
  reel_kit/diario pipeline/sabor/conferir_sabor.py diario/TEMAS-PRODUZIDOS.md && git reset -q`. Comite SÓ `diario/<hoje>/`
  e `diario/TEMAS-PRODUZIDOS.md`, no branch em que você trabalha.
- ESTADO COMPARTILHADO: a pasta do projeto `/mnt/project-files/diario/<hoje>/` (outras etapas leem dali).
- Data de hoje no fuso America/Bahia. Se já existe `/mnt/project-files/diario/<hoje>/meta.json`, ENCERRE ("já coberto").
- Se existe `/mnt/project-files/diario/PAUSADO`, ENCERRE ("pausado pelo Wagner").
- Logo que passar das travas, crie `/mnt/project-files/diario/<hoje>/meta.json` com {"data":..., "status":"produzindo"}
  (é a trava contra duas rotinas no mesmo dia).
- HeyGen `get_current_user`: se `premium_credits.remaining` < 150 + custo estimado (47 créditos por minuto de
  vídeo), NÃO gere. Grave status "sem_credito" e o saldo no meta.json da pasta do projeto e siga ao passo 8.

## 1. Tema mais viral do dia (3 a 5 candidatos)
Fontes, nesta ordem: vidIQ (`vidiq_trending_videos`, `vidiq_outliers`, `vidiq_instagram_tiktok_outlier_search`
com termos de saúde em português), notícias médicas das últimas 48 h (WebSearch), e o que está bombando nos
focos do Wagner: jejum intermitente, desparasitação/vermes, fertilidade masculina e feminina, ganho de massa
magra e força, intestino e intolerância alimentar, canetas emagrecedoras, mitos de saúde.
Descarte: tema já feito (veja `diario/*/meta.json`, `pipeline/TEMAS-USADOS.md`, `queue/` e os posts dos últimos
30 dias no Metricool, marca 7510655), tema sem fonte primária confiável, tema que exige indicar remédio/dose.

## 1b. Tema repetido é proibido (regra do Wagner, 10/11/2026)
Antes do Jev, abra `diario/TEMAS-PRODUZIDOS.md` e confira as fontes listadas lá. Risque todo candidato cujo
tema (história, experimento, personagem ou pergunta central) já foi produzido, mesmo com outro título. Só
repita com autorização expressa do Wagner. Se sobrarem menos de 3 candidatos, busque mais temas (história da
medicina tem muito: experimentos famosos, erros de diagnóstico, descobertas por acaso). Depois de produzir,
acrescente o tema do dia em `diario/TEMAS-PRODUZIDOS.md` e comite junto com `diario/<hoje>/`.

## 2. Jev escolhe (nota 0-10 de potencial viral)
Dê a cada candidato nota 0-10 e uma linha de motivo. Critérios do Jev (vindos do reel Efeito Rosenhan, o que
mais rendeu entre os recentes):
- +3 se é história real com data, cientista e números (experimento famoso, caso histórico, estudo grande).
- +2 se o médico expõe erro, viés ou mito da própria medicina/indústria (indignação moral, "poderia ser comigo").
- +2 se tem polêmica atual (está nas buscas/notícias hoje) e conflito claro (crença popular x estudo).
- +1 se cabe em uma frase-gancho de 3 partes: nome do fenômeno + conflito + consequência.
- +1 se é dos focos do Wagner. +1 se tem número concreto que vira imagem (52 dias, 1.815 mulheres).
- −3 se depende de promessa de cura, remédio ou dose (CFM). −2 se é parecido com o vídeo de ontem (tema já produzido nem entra: ver 1b).
Fique com a maior nota. Guarde os candidatos, notas e motivos no meta.json.

## 3. Roteiro (molde da vacina + achados do Rosenhan)
Siga a skill `formula-heygen-papo-medico` se estiver disponível. Resumo obrigatório:
- 180 a 190 palavras (~58 s). Não passe de 70 s sem o Wagner liberar vídeos longos.
- 4 parágrafos = 4 atos. Gancho: nos primeiros 5 s, 3 frases curtas (fenômeno + conflito + consequência) OU a fala
  do paciente em 1ª pessoa ("Ah, doutor, ...né?") seguida de empatia e "Mas olha só...". Ciência: história/estudo
  real com número concreto e explicação leiga entre vírgulas, pergunta seca com resposta curta ("A diferença?
  Nenhuma, tá?"). Virada: devolve a pergunta do público, "Olha que coisa.", o motivo de verdade e uma analogia
  popular nova. Fecho: "Agora, cá entre nós..." (o ÚNICO "..."), critério prático de quando ir ao médico e uma
  frase-lição em contraste. Guarde uma segunda virada para o fim quando o tema permitir.
- Fala natural do Wagner: "né?", "tá?", "cara", "olha só", "aí" emendando frases; 3-4 perguntas de verdade; micro-
  pergunta a cada 10-15 s; até 3 palavras soltas de impacto ("Todos.", "Ninguém."), nunca duas seguidas.
- Proibido: "Tsc." solto, duas frases de uma palavra seguidas, "viu", "meu rei", "Oxe", "Ó paí ó", MAIÚSCULAS,
  tags, promessa de cura, remédio/dose, número sem fonte. Todo número vem do PubMed (conector PubMed) com DOI.
- Grave `diario/<hoje>/roteiro.txt` (só o texto falado) e as fontes no meta.json.

## 4. HeyGen (molde único — não mude nada)
`create_video_from_avatar` com:
- avatarId `1d7e528beec9442ebcb4651a5b74bec6` ("Dr. Wagner Novaes podcasting", de jaleco no estúdio; padrão do Wagner desde 11/11/2026 para toda produção, o antigo 6cd9 não se usa mais), voiceId `c4755690737746ffa3bcc01c32d84751`, voiceSettings `{"speed": 1.3}`
- engine `{"type": "avatar_v", "more_blinking": true}`, aspectRatio `9:16`, resolution `1080p`
- title `Diário AAAA-MM-DD: <tema>`; script = roteiro.txt exato
- motionPrompt: "Serious, credible doctor talking with energy, but NEVER a wide smile: no teeth-showing grin, no
  laughing, no beaming. Face stays mostly neutral and focused; irony shows only as one raised eyebrow, slightly
  narrowed eyes or a tiny closed-lip half smile at the corner of the mouth. Concerned, attentive look while
  explaining the studies; firm, warm look at the end. Varied natural hand gestures, each used once: <4 a 6 gestos
  diferentes dos do vídeo de ontem, ex.: open palm toward camera, a small shrug, hands together, palms down
  calming, head tilt with open hands>, and pointing at the camera only in the last sentence. NEVER show numbers
  with the fingers: no counting on fingers, no holding up fingers, no raised index finger as 'one'."
  PROIBIDO (regra do Wagner, 10/11/2026): o clone NUNCA mostra número com os dedos. Não escolha gestos de contar,
  levantar dedos ou "raised index finger"; números aparecem só na edição (painel/número gigante). Na conferência
  dos quadros, se aparecer dedo contando, anote no meta.json.
Chame UMA vez. Espere com `get_video` (30 s entre consultas, até 25 min). Se falhar, NÃO gere de novo: grave
status "falha_heygen" com a mensagem e siga ao passo 8. Baixe o mp4 (`curl -L -o bruto.mp4 "<video_url>"`)
para `/tmp/diario/bruto.mp4` (não comite o bruto).
Confira 6 quadros (`ffmpeg -ss`): sem sorrisão, rosto sem deformar. Se deformou, anote no meta.json (não refaça).

## 5. Formato da edição (escolha pela cara do vídeo)
- `tela_dividida` (Explicador em tela dividida, o padrão da vacina): mito x fato, estudo com dados. Painel de
  caderno em cima, ele embaixo. `estilo_painel: "caderno"`.
- `dinamica` + `estilo_painel: "dossie"` (Dossiê confidencial): história real, experimento famoso, erro da medicina.
  Tela cheia com cortes a cada 2-3 s, painel em pasta "CONFIDENCIAL".
- `dinamica` + `estilo_painel: "celular"` (Réplica à polêmica): notícia/polêmica do dia, painel como manchete.
- `mapeamento` (Mapeamento: explicador em cenas, pedido do Wagner em 10/11): tema com lugar, data, estudo de outro país,
  porcentagem, "o mundo todo faz X", história com linha do tempo. Cenas gráficas de tela cheia trocando a cada 2-4 s
  (mapa 3D em papel antigo, cartão colorido com ícone, foto com fita, bolinhas de %, citação, etiqueta de data, barra),
  intercaladas com ele em tela cheia; legenda serifada palavra a palavra em cima. Plano próprio (veja 6b).
- Edição full (3D, recorte) NÃO roda aqui; nunca prometa.
Empate: não repita o formato de ontem. Grave em meta.json `formato` e `motivo_formato`.

## 6. Plano de edição e render
Escreva `diario/<hoje>/plano.json` (modelo completo em `reel_kit/diario/exemplo_plano.json`). Regras:
- `quando` = trecho EXATO de 2-4 palavras do roteiro (o editor acha o tempo pela fala).
- 7 a 10 `paineis` (tipos: fala, texto, numero, comparacao, checklist, manchete), um por ideia, com emoji. No estilo `dossie` NÃO use `manchete` (sai texto branco no papel claro, ilegível): use `texto`. Na folha de conferência, o painel nunca pode cobrir os olhos dele.
  Texto curto (até 7 palavras). Comparação só com números reais do estudo.
- 1 ou 2 `carimbos` (palavra de impacto), 0-2 `numeros` gigantes (o número-chave do estudo), 2-3 `closes`
  (frases de impacto: "Olha que coisa", a frase-lição), `destaques` (6-10 palavras-chave em amarelo).
- `fonte` aparece do início ao fim do trecho do estudo; `fim` traz a frase-lição e as referências com DOI.
- `trilha`: uma de `reel_kit/trilhas/` (dark_cinematic, educacional, background_calmo, future_bass, ...);
  tensa para dossiê, leve para explicador, energética para réplica. Nunca música de terceiros.
### 6b. Plano do formato `mapeamento` (modelo: `reel_kit/diario/exemplo_plano_mapeamento.json`)
No lugar de `paineis`/`carimbos`/`numeros`, escreva `cenas` (12 a 18, uma a cada 2-4 s de fala; cada uma vale do seu
`quando` até a próxima; cena gráfica com mais de 5,5 s é cortada para o rosto dele sozinha). Tipos:
- `mapa`: `paises` (português ou inglês: "EUA", "Brasil", "Suécia", "Europa", "Escandinávia", "América Latina"), `cor`
  (vermelho, amarelo, azul, laranja, verde, preto, roxo), opcional `outros` {paises, cor}, `setas` [["A","B"]],
  `etiqueta` ("1984 · Perth"), `pip`: true (bolha dele no canto). Use para o país do estudo, de onde veio, onde proibiram.
- `cartao`: `emoji`, `cor`, `rotulo` (até 3 palavras), opcional `fundo` (vermelho/amarelo/azul, tela inteira colorida).
- `foto`: `emoji` ou `imagem` (arquivo em `<pasta_trabalho>/img/`), `cor` do bloco, `legenda` curta.
- `documento`: `imagem` (print da página do estudo ou jornal de época em `<pasta_trabalho>/img/`), `grifo` [y0, y1]
  (faixa da página, de 0 a 1, grifada em amarelo), `legenda` (referência). É a fonte mostrada na tela.
  Fotos de arquivo e páginas: só domínio público ou fonte oficial (Wikimedia Commons, PubMed/PMC), com crédito na legenda.
- `bolinhas`: `valor` (0-100, só número real do estudo), `cor`, `legenda`, `mini` (citação curta da fonte).
- `citacao`: `texto` (frase curta), `destaque` (trecho grifado em amarelo), `autor`.
- `etiqueta`: `texto` ("10 dias", "1870 – 1950"), `sub`, `cor`.
- `barra`: `barras` [{rotulo, valor, texto, cor}] (até 3).
- `rosto`: volta para ele em tela cheia (use 3-5 vezes, nas viradas e micro-perguntas).
Gancho e `closes` são sempre o rosto dele. `fonte`, `fim`, `titulo`, `destaques` e `trilha` valem igual.
Na folha de conferência: o país certo aceso, a legenda de cima legível, nenhuma cena vazia.

Rode:
```bash
pip install -q faster-whisper pillow
bash reel_kit/diario/editar.sh /tmp/diario/bruto.mp4 diario/<hoje>/roteiro.txt diario/<hoje>/plano.json /tmp/diario/w /tmp/diario/editado.mp4
```
Leva ~3 min. OLHE `/tmp/diario/w/conferir/folha.jpg` (Read): legenda dentro da tela, painel legível, carimbo
no lugar. Se algo saiu errado, ajuste o plano e rode de novo (no máximo 3 vezes). Depois o sabor:
```bash
python pipeline/sabor/camuflar_forte.py /tmp/diario/editado.mp4 --saida /tmp/diario/sabor
python pipeline/sabor/conferir_sabor.py /tmp/diario/sabor --origem /tmp/diario   # tem que sair 0
cp /tmp/diario/sabor/editado-sabor.mp4 diario/<hoje>/reel.mp4   # grave no meta.json tamanho_bytes_raw = tamanho deste arquivo (o portão das 17h compara com o raw_url)
cp /tmp/diario/w/conferir/folha.jpg diario/<hoje>/folha.jpg
```
Confira: reel.mp4 existe, > 1 MB, < 48 MB (limite de 50 MB do agendador), duração entre 90% e 110% do bruto + 2,6 s do cartão final.

## 7. Legenda e meta.json
Legenda humana (skill ig-caption/ig-human se houver): 1ª linha = pergunta pessoal ao público ("Você já...? Me
conta aqui embaixo."), 2-4 linhas contando o achado, a fonte (autor, revista, ano), "Isso não substitui consulta.
Converse com seu médico.", 3 a 5 hashtags incluindo #papodemedico. Sem travessão longo, sem cara de IA.
`diario/<hoje>/meta.json`:
```json
{"data":"AAAA-MM-DD","status":"previa","tema":"...","nota_jev":9,"candidatos":[{"tema":"...","nota":7,"motivo":"..."}],
 "heygen_id":"...","heygen_link":"https://app.heygen.com/videos/<id>","creditos_antes":0,"creditos_depois":0,
 "formato":"tela_dividida","motivo_formato":"...","duracao_s":60.8,"tamanho_mb":27.2,"trilha":"...",
 "fontes":[{"ref":"Autor et al., Revista Ano","doi":"..."}],"legenda":"...","titulo_yt":"<até 90 caracteres> #Shorts",
 "publicar_em":"AAAA-MM-DDT18:00:00-03:00","branch":"...","raw_url":"https://raw.githubusercontent.com/..."}
```
`git add diario/<hoje> && git commit -m "diario: <tema>" && git push -u origin <seu branch>` (repita até 4x se falhar).
Grave no meta.json `branch` e `raw_url` = `https://raw.githubusercontent.com/wpnjunior/publer-media/<branch>/diario/<hoje>/reel.mp4`
(é a URL pública que o Metricool baixa; confira com `curl -sI` que responde 200 e o tamanho bate).
Copie meta.json, roteiro.txt, plano.json, folha.jpg e reel.mp4 para `/mnt/project-files/diario/<hoje>/` e releia
depois de 10 s (a pasta é de rede). Não abra pull request para a pasta do dia.

## 8. Chamar a prévia
Dispare a tarefa agendada `trig_013gXUvYv8Bbym4fBeYf6Cg4` ("Vídeo diário: prévia pronta") com `fire_trigger`
(ferramenta do claude-code-remote). É ela que mostra o vídeo ao Wagner. Se não conseguir disparar, diga isso no relatório final.

## 9. Relatório final (4 linhas)
Tema e nota do Jev · formato e motivo · link HeyGen e créditos restantes · pasta enviada (ou o motivo de parar).

## Regras inegociáveis
- Um vídeo por dia, uma geração no HeyGen por dia. Nunca gere de novo para "melhorar".
- Nunca publique nada você mesmo e nunca entregue o bruto como se fosse editado.
- Ética CFM: sem cura, sem remédio/dose, sem "garante/melhor/especialista"; fecho sempre manda ao médico.
- Número sem fonte não entra. Estudo inventado é proibido.
