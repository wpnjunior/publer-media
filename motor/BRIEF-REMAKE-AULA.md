# Brief do ajudante de PRODUÇÃO do remake com aula (14/11/2026)

Leia primeiro `/tmp/claude-0/motor/BRIEF-AJUDANTE.md` inteiro (inclusive o adendo no fim) e depois o roteiro do seu vídeo em `/mnt/project-files/reacts/remakes/<slug>.md` (escrito e conferido por outro ajudante: siga-o; se achar erro de fato médico ou de tempo, corrija e diga no relatório).

Você NÃO publica, NÃO mexe no Metricool, NÃO faz commit, NÃO fala com o usuário, NÃO edita arquivos compartilhados do motor.

## O que fazer
1. O vídeo atual continua valendo até o novo ficar pronto: NÃO sobrescreva nada dele. Trabalhe com um plano NOVO de id `<id>_aula` (ex.: `react_ivete_aula`), gerado por um script novo `scripts/plano_<nome>_aula.py` (copie do script/plano atual e adapte; se só existir o JSON, carregue o JSON no script e transforme).
2. Voz nova: UMA chamada de HeyGen `create_speech` (voz `c4755690737746ffa3bcc01c32d84751`, language pt, withTimestamps) só com o "TEXTO NOVO A GRAVAR" do roteiro. Teto: 30 s de áudio bruto (6 créditos). Se a chamada der erro ou tempo esgotado, confira antes se o áudio saiu; não repita às cegas. Depois `ffmpeg -af atempo=1.3`, salve `assets/midia/<P>_aula_voz.wav` e o `.words.json` (tempos ÷ 1,3, formato `[{"w","s","e"}]`). Se o roteiro pedir voz Murilo de contexto (`d703f08d1ef34302a36945aa3efc7b3f`), mais 1 chamada curta. NÃO gere rosto: os rostos (entrada, reação, CTA) ficam os que o vídeo já tem.
3. Narração antiga: reaproveite cortando por tempo (`ms`/`d` nas entradas de `audio.voz`) exatamente os trechos que o roteiro manda manter; nenhuma frase cortada no meio (confira nos tempos das palavras e deixe ~0,15 s de respiro).
4. Aula: camada `fisio` em cima de b-roll (veja `scripts/plano_cariani2.py`: BR(), TT(), `fixo:True`, trilha `m_investiga` baixinha). Desenhos novos do roteiro viram `fisio_extra/<nome>.svg`. B-roll do Mixkit cortado em vertical em `assets/midia/<P>_br_*.mp4`. Cartela ≥1,5 s, até 5 palavras, sem termo técnico. A legenda da fala (lima/pílula) desce para ~y 1730 durante a aula para não cobrir os órgãos.
5. A aula entra onde o roteiro diz (depois da resposta do rosto, antes do estudo). Tudo que vem depois anda para frente no tempo (camadas, voz, efeitos, janelas da legenda). Mantenha a mesma pele e a mesma entrada que o vídeo já usa (rode `pele.py`/`entrada.py` do mesmo jeito que o original; veja ESTADO-LOTE.md).
6. Confira antes de renderizar: `python3 audio_plano.py planos/<id>_aula.json`, `python3 leitura.py planos/<id>_aula.json` (0 problemas) e quadros da aula e das emendas com `npx hyperframes snapshot --at ... --no-end -o <dir>` dentro de `amostras/<id>_aula` (gere com `python3 gerar.py planos/<id>_aula.json amostras/<id>_aula`). OLHE os quadros: rótulos não podem se sobrepor, texto tem de caber, órgão não pode ficar atrás de cartela.
7. Render: acrescente o id numa linha de `saida/fila.txt` (a fila roda um por vez; outros ajudantes também estão na fila, pode demorar). Espere `saida/<id>_aula.gate` com FIM. Portões: parado ≤10%, maior_parado ≤3 s, LUFS -16..-12, buraco <1,2 s. Reprovou: corrija e reenfileire (tire o id de `saida/feitos.txt`).
8. Assista por amostra o mp4 final (quadros a cada ~5 s) antes de devolver.

## Relatório final (curto)
Caminho do mp4, portões, duração, texto novo gravado, trechos antigos mantidos, créditos HeyGen gastos (saldo antes e depois com `get_current_user`), b-roll usado (ids), e qualquer ponto que o Wagner possa querer vetar.

## Adendo 14/11 07h BRT (Wagner): VARIAR A EDIÇÃO DA AULA
Leia `/tmp/claude/memory/team/silo/regra-variar-edicao-aula.md`. b-roll + camada fisio NÃO é mais o padrão (já usado em Cariani, fígado, TDAH invenção, Ivete). Cada remake novo usa a edição que a thread principal indicar no seu pedido, com o que o motor já tem:
- caixinha: `cartao` creme com aba lima se desenhando (`desenho` setas/círculos/X/check, `texto` Caveat, `numero`, `barra`), fundo escuro liso ou com `grao`; os desenhos de fisio_extra podem entrar DENTRO da caixinha (camada fisio com escala menor), um por cena.
- edição full: `gigante` (palavras Anton enormes, cheias e só contorno), `artigo` em perspectiva 3D com grifo, `numero` grande com sombra 3D (CSS perspective/rotateX), `carimbo`, `celular` com manchete; recorte do rosto só nos trechos que já têm rosto (r1/CTA), se der.
- mapa: `mapa` em papel antigo com pinos/rotas, quando o tema tem lugar.
Regras: uma ideia por cena (nunca 3 desenhos + frase longa no mesmo quadro); cartela grande; texto da voz sem expressão popular que confunde ("de tabela"); troca visual a cada 2-4 s.

## Adendo 14/11 07h15 BRT (Wagner): VOZ COM EMOÇÃO E RITMO CALMO (vale para Paraguai, Claudia, esperma, café)
Leia `/tmp/claude/memory/team/silo/regra-ritmo-voz-e-regua-da-vo.md`. Isso SUBSTITUI a regra "reusar a narração antiga + 1 create_speech da aula":
- Regrave a NARRAÇÃO INTEIRA (tudo que é só voz, sem rosto) com a voz `c4755690737746ffa3bcc01c32d84751`, em BLOCOS por clima, um create_speech por bloco (language pt, withTimestamps, model omitido), SEM atempo (velocidade nativa pelo parâmetro speed):
  - indignado (veredito, desmentir, "isso é mentira"): speed 1.15, pitchVariance 1.6, pitchShift 0.5
  - alegre (boa notícia, CTA, fecho leve): speed 1.15, pitchVariance 1.5, pitchShift 1
  - manso (aula, acolher, explicar): speed 1.1, pitchVariance 1.1, pitchShift -0.5 (o manso 1.0/-1 foi reprovado: lento)
  - neutro/explicando estudo: speed 1.15, pitchVariance 1.3, pitchShift 0
- Pausa entre frases: `<break time="0.7s"/>` dentro do texto (no manso, até 0,5 s). Junte os blocos com 0,6-0,8 s entre eles, ambiente/trilha por baixo, sem silêncio digital.
- Custo: 1 crédito a cada 5 s brutos, arredondado por áudio: prefira 3-4 blocos. Teto por vídeo: 14 créditos. Confira o saldo (get_current_user) antes e depois e informe.
- Texto: régua da vó (palavras do dia a dia, sem "de tabela"), uma ideia por cena. Rostos (r1, CTA, entrada) continuam os mesmos arquivos.
