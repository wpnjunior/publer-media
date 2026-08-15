# ESTEIRA — REEL COMENTADO DO DIA

Quarto post da grade. Nasce do que está **em alta agora**, não do estoque: o radar acha o
assunto, a evidência é conferida, o roteiro toma posição, o clone comenta e o vídeo sobe.

**Grade depois desta esteira:** 10h comentado · 14h card · 18h Reel "Frasco para X" · 20h carrossel.
(10h escolhido pelos dados do próprio perfil: mediana 44 em 10 posts, o melhor horário livre —
19h é o melhor de todos mas 18h e 20h já estão ocupados. Fácil de mudar.)

---

## LINHA EDITORIAL (decidida por Wagner em 15/08/2026)

**Pró-integrativa, sem inimigo fixo.** Defende jejum, alimentação carnívora, suplementação e
medicina integrativa **pelo que elas entregam**, com nome e número. Não elege vilão, não abre
roteiro atacando categoria, não usa "a indústria quer que você não saiba".

Na prática:
- **Toma posição, sim.** "Isso funciona e aqui está o porquê" é posição. Ficar em cima do muro
  ("depende de cada caso, procure seu médico") é o que mata o post — a ressalva entra no fim,
  não no lugar do conteúdo.
- **Defende com o que sustenta.** Se o dado é bom, cita o dado. Se é experiência de consultório,
  diz que é experiência de consultório. **Nunca vender opinião como evidência** — é isso que
  separa o Wagner do influencer de protocolo, e é o que segura no CRM.
- **Admite o limite da própria tese.** "O jejum ajuda nisso e NÃO ajuda naquilo" ganha mais
  autoridade que "o jejum resolve tudo". É a marca dele: a meia-verdade desmontada
  (ver [[reference_tese_clinica_wagner]]).
- **Quando o assunto envolve remédio**, o critério é risco x benefício naquele caso — não
  torcida. Nunca orientar a parar medicação.

## COMPLIANCE — inegociável (CFM 2.336/2023)
Proibido: prometer cura, garantir resultado, "o melhor / o único / milagroso", "especialista em",
comparar-se a colegas, prometer emagrecimento em X dias, citar marca comercial, dar dose para o
público geral, número ou estudo inventado, orientar suspensão de tratamento.
Obrigatório: logo + CRM-RJ 0127554-2 no vídeo · "Este conteúdo é educativo e não substitui a
consulta médica" na legenda.

---

## AS 7 ETAPAS

### 1. Radar — o que está em alta
```
/last30days <tema do nicho>
```
Fontes ativas: TikTok, Instagram, Reddit, YouTube (com transcrição), Hacker News, web.
Rodízio de temas para não repetir assunto: jejum · carnívoro · suplementação · resistência
insulínica · longevidade · sono · hormônios · exames.

**Critério de escolha do tema** — só entra o que tem as três:
1. Volume real de conversa nos últimos 30 dias (não é achismo meu).
2. Uma **verdade incômoda** disponível: o que as pessoas acham x o que acontece no consultório.
3. Evidência ou experiência clínica que o Wagner assine embaixo.

Se o radar não trouxer nada com as três, **o dia não tem comentado** — melhor pular do que
publicar raso. Avisar o Wagner e não inventar tema.

### 2. Conexão com o mundo
```
skill: rastrear
```
Cruza o tema com notícia recente, cena de filme/série ou fato histórico. É daqui que sai o gancho
que faz o vídeo não parecer aula. Escolher 1 das 5 conexões.

### 3. Evidência e prova visual
- Buscar o estudo/diretriz que sustenta a tese. **Preferência: 2020-2026 e independente**
  (ver [[feedback_estudos_novos_independentes]]).
- Print da ficha do artigo: Europe PMC (sem captcha) → headless → crop.
  Receita em [[reference_print_artigo_video]].
- **Regra dura:** nenhum número entra no roteiro sem fonte conferida. Na dúvida, escrever sem número.

### 4. Roteiro
```
skill: diretor
```
Estrutura: hook → cena → virada → ponte → saída → CTA.
**Tamanho: 45 a 60 segundos.** A conta é `segundos ≈ palavras ÷ 2` (a voz sai a 124 palavras/min).
Ou seja: **130 a 170 palavras, ponto.** Passar disso queima crédito à toa — ver
[[erro_heygen_custo_credito]].
Escrever em blocos separados por `---`, um bloco por slide/cena.

### 5. Caçar as cenas
```
skill: caça cena          (para material citável: journal médico, notícia)
python buscar_broll.py "<termo em ingles>" <slug>     (Pexels, licença comercial livre)
python mosaico.py broll contato.png                   (folha de contato para eu escolher)
```
**Olhar a folha de contato e escolher na mão.** Critério: empatia, desconforto ou revolta.
**3 a 4 clipes**, nunca mais — mais que isso vira videoclipe e o conteúdo some.
Descartar o que foge do tema e o que compromete perfil médico (cigarro, bebida, cena apelativa).

### 6. Produção
```powershell
# clone (MCP HeyGen, nesta sessão):
#   create_video_from_avatar
#   avatarId da4fdcdc723c4e4d8f8a7f5b6ab51976 · engine avatar_v
#   voiceId 105a65310b5744fb91a366320678f668 · 9:16 · 1080p · outputFormat webm
python tempos.py roteiro.txt clone_alpha.webm
python montar_comentado.py <pasta_slides> clone_alpha.webm reel.mp4 "<tempos>" broll.json
.\acelerar.ps1                    # 1.1x — OBRIGATÓRIO, gera reel_FINAL.mp4
```
Conferir `get_current_user` **antes e depois** — é a única forma de saber o custo real.

### 7. Publicação
Legenda humana + ressalva educativa + 4-5 hashtags. Agendar às **10h** (13:00Z) pelo Publer,
com folga de 50 min. Vídeo exige ≥45 min de antecedência.

---

## CUSTO E LIMITE
- 45-60s de Avatar V ≈ **15 a 20 créditos**. Diário ≈ **450-600/mês**.
- Se o saldo cair abaixo de 40, **avisar o Wagner antes de gerar** e segurar a esteira.
- Trabalho por peça: 30 a 50 min, sendo a checagem de evidência a parte lenta — e a que não se pula.

## O QUE NÃO FAZER
- Publicar tema sem as três condições da etapa 1.
- Inventar número, estudo ou percentual.
- Passar de 170 palavras no roteiro.
- Mais de 4 b-rolls.
- Pular o 1.1x.
