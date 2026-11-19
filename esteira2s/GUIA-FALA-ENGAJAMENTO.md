# Guia de fala e engajamento — Papo de Médico e Fertilidade a Dois

Vale para todo roteiro, legenda, carrossel e story da esteira de 30 dias. Não troca a fórmula padrão
(skill `formula-heygen-papo-medico`): soma a ela.

## 1. Padrão fixo de produção (decidido pelo Wagner)
- Voz: "Wagner comunidade" do HeyGen (c4755690737746ffa3bcc01c32d84751), 1.3x. Rosto: avatar 1d7e, HeyGen IV.
- Rosto só em cortes curtos (Banco de Rostos); narração só em áudio. Sem sorrisão, nunca contar nos dedos.
- Fala: "né?", "tá?", "cara", "olha só", "aí". Proibido: "meu rei", "viu", "Oxe", "Tsc.", MAIÚSCULAS.
- Tema sempre novo. CFM: sem promessa de cura, sem remédio/dose, sem diagnosticar famoso, todo número com fonte.

## 2. Os primeiros 3 segundos (gancho)
Uma destas aberturas, nunca a mesma em dois dias seguidos na mesma conta:
1. Frase do paciente: "Ah, doutor, minha prima cortou o glúten e sarou, né?"
2. Número que não bate com o senso comum: "Uma em cada cem. Só uma."
3. Pergunta que a pessoa responde por dentro: "Você toma vermífugo todo ano?"
4. Contradição: "O exame deu normal. E ela não engravida."
5. Cena: "Viena, 1847. As mães morriam mais na ala dos médicos."
6. Aviso de lista: "Salva esse vídeo antes de começar o jejum."
7. Famoso como porta: "O Zé Felipe contou que colocou chip de testosterona." (comenta o tema, nunca a pessoa)
Regras: a tese aparece ESCRITA na tela no primeiro segundo; a primeira frase tem até 12 palavras; nada de
"oi, gente" nem de se apresentar.

## 3. Segurar até o fim (retenção)
- Promessa aberta no gancho e paga só no ato 3 ("e o motivo de verdade é outro").
- Troca visual a cada 2 a 4 s (cena, cartão, número, rosto). Nunca mais de 6 s de tela parada.
- Uma micro-pergunta a cada 10 a 15 s ("E sabe o que aconteceu?").
- Um "Olha que coisa." antes da virada. Uma analogia popular por vídeo (cano, tijolo e pedreiro, galo e sol).
- Número grande na tela quando ele é falado. Fonte visível enquanto o estudo é citado.
- Duração: 35 a 60 s. Lista e linha do tempo podem ir a 60; mito e notícia ficam em 35 a 45.

## 4. A cobrança no MEIO ("segue e curte") e o fecho (regra do Wagner, 11/11)
**A cobrança bem-humorada, em todo vídeo.** Logo depois da ENTREGA (o dado que desmonta o mito, a virada da
história, o item mais forte da lista), entra UMA frase leve cobrando o seguir e o curtir como se fosse o dever
de quem acabou de receber aquilo. Nunca no fim, nunca como pedido formal ("segue e curte aí").
- Modelo do próprio Wagner: "Depois de desfazer essa minhoca na sua cabeça, não me seguir é atestado de
  sadomasoquista."
- A frase é ESCRITA PARA O ASSUNTO do vídeo, usa a imagem que o vídeo acabou de usar e tem graça. Receita:
  [o que eu acabei de te entregar] + [não seguir/curtir vira um absurdo engraçado].
  Outros exemplos do tom: "Te poupei três anos de dieta errada. Um curtir é o mínimo, né?" /
  "Eu li o estudo inteiro pra você não precisar. Seguir aqui é pagar o pedágio." /
  "Se depois dessa você não me segue, o problema já não é o glúten."
- Cada vídeo tem a sua; não repetir a mesma piada em 30 dias (grave a frase em `meta.json` campo `cobranca`).
- Vai na NARRAÇÃO (só áudio, custo de voz) com um adesivo "segue + curte" e o @ na tela por 2 s. Se o roteiro
  for de rosto do banco, use um clipe tipo `troca` (frases de troca já gravadas com o clone).
- Estilo "praga de brincadeira" (do Wagner): "quem não me segue vai..." + um castigo cômico do assunto.
  Papo (frase do Wagner, vídeo de parasitas): "Quem não me seguir vai ficar com verme."
  Papo: "Quem não seguir vai passar o mês inteiro ouvindo o tio do zap falar de detox."
  Fertilidade: a praga fica do lado do casal, contra o que irrita eles, NUNCA sobre não engravidar, demorar
  para engravidar ou perder: "Quem não seguir vai ouvir da sogra 'e o neto, sai quando?' por mais dois anos." /
  "Quem não curtir vai explicar espermograma pro cunhado no churrasco." (A frase "vai ficar 2 anos sem
  engravidar" foi proposta pelo Wagner em 11/11 e ficou de fora por recomendação; só usar se ele confirmar.)
- Limites: o humor é contra a preguiça de seguir, nunca contra doente, corpo, religião ou a mulher que tenta
  engravidar. Fertilidade usa a versão acolhedora ("Eu trouxe o dado; vocês dois deixam o curtir. Fechado?").
  Assunto de luto ou perda gestacional: sem cobrança, sem humor.
- Carrossel: a cobrança é um slide no meio, no mesmo tom. (Reels de texto não existe mais.)

**Banco de CTAs:** `esteira2s/BANCO-CTA.json` guarda as frases por tipo e por conta, a pesquisa de retorno
(meio converte mais que fim; envio e curtida são os sinais que o Instagram mais pesa; metade assiste sem som,
então todo CTA vai também escrito) e o `usado_em`. Sorteie de lá, adapte ao assunto e grave a data. Grave em
`meta.json` os campos `cta_meio` e `cta_fim` (tipo + frase) para o relatório de segunda medir qual rende mais.

**O fecho**, uma chamada do conteúdo só, em rodízio:
- SALVAR: listas, exames, passo a passo ("Salva pra levar na consulta").
- MANDAR: mito e casal ("Manda pra quem vive dizendo isso").
- COMENTAR com pergunta fácil de responder ("E você, já cortou o glúten por conta própria?").
- PALAVRA-CHAVE (Fertilidade): "Comenta TENTANTE que eu te mando a lista", só quando a lista existir de verdade.
A última frase falada é a frase-lição em contraste ("Pote não faz músculo, treino faz.").

## 5. Por molde
| Molde | Gancho | Meio | Fecho |
|---|---|---|---|
| Mito ou verdade | a frase do mito, dita como o povo diz | 1 estudo, 1 número, "A diferença?" | veredito em 1 palavra na tela + mandar |
| Linha do tempo | "O que acontece no seu corpo em X horas/dias" | 4 a 5 marcos na régua, um fato por marco | quando procurar o médico + salvar |
| Lista para salvar | "Salva antes de..." | 4 a 6 itens, um por cena, marcando | "leva na consulta" + salvar |
| Notícia de famoso | manchete na tela, "o caso levanta uma dúvida comum" | o que a ciência sabe sobre o TEMA | critério prático + comentar |
| React | até 12 s do viral com o @ | pausa, "olha só", o que está certo e o que não está | frase-lição + mandar |
| Responder comentário | o comentário colado na tela | resposta direta em 1 frase, depois o porquê | convida a próxima pergunta |
| História real | data e lugar em 1 frase | a virada da história | o que isso muda hoje + comentar |
| Tela dividida | prova em cima, rosto embaixo | dado por dado no caderno | frase-lição |

## 6. Legenda (cada conta escreve a sua)
- Linha 1 repete o gancho com outras palavras e cabe antes do "mais" (até 90 caracteres).
- 3 a 5 linhas curtas, 1 número, fonte com DOI, "Converse com seu médico."
- Palavras de busca escritas como frase normal (o Instagram busca texto), até 5 hashtags.
- Papo fala com "você"; Fertilidade fala com "vocês dois" e nunca culpa ninguém.

## 7. Stories (2 por dia)
- Story 1 (1 a 2 h depois do post): chamada para o post, com uma pergunta de sim/não.
- Story 2 (noite): caixinha de pergunta ou enquete; as perguntas boas viram o molde "Responder comentário".

## 8. Tom por conta
- Papo de Médico: direto, com humor seco, desmonta boato sem humilhar quem acreditou.
- Fertilidade a Dois: acolhe primeiro, informa depois. Nunca "culpa", nunca "é só relaxar". Sempre o casal.
