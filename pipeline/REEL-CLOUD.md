# REEL DIÁRIO "FRASCO PARA X" — 18h (você monta, o GitHub publica)

Companheiro do carrossel: **18h Reel (isca) → 20h carrossel (dossiê)**, mesmo tema do dia.

## Passos
1. **Tema do dia:** leia `queue/` — pegue a pasta mais recente (o carrossel que a esteira montou hoje).
   Use o MESMO tema. Se não houver carrossel hoje, escolha um tema de frasco do estoque e siga.
   Antes de gastar: se já existir pasta em `reels_queue/` com `schedule_at` de hoje, ENCERRE ("já coberto").

2. **Monte a fórmula do frasco** (4-5 ativos + dose) para o tema. Critério do Wagner: **frasco bonito e
   de uso popular** — não precisa ser o mais evidenciado; vale prática de manipulação/consenso popular.
   Fontes: conhecimento consolidado, buscas na web, formulações comuns de manipulação.
   Sempre coerente e com dose plausível. Nada de dose absurda.

3. **Gere o overlay** com `reel_kit/gen_overlay.py` a partir de um JSON como `reel_kit/exemplo_frasco.json`:
   ```json
   {"tema":"Tireoide",
    "urgencia1":"Isso aqui é ouro!! Pode printar!",
    "urgencia2":"Isso não se vê todo dia — segue e curte!",
    "formula":[["Selênio","200 mcg"],["Zinco bisglicinato","15 mg"]],
    "posologia":"Uso: 1 dose pela manhã, por 30 dias.",
    "dica":"<hábito simples e barato que ajuda no tema>"}
   ```
   As duas frases de urgência saem em DOURADO e CAIXA ALTA (já está no CSS). Varie um pouco as frases
   entre os dias, mantendo o tom "isso é ouro / printa isso / não se vê todo dia".
   `python reel_kit/gen_overlay.py meu.json overlay.html`

4. **Renderize o overlay** (transparente) e **monte o vídeo** (15s, foto PARADA — sem zoom):
   ```bash
   npx playwright screenshot --viewport-size=1080,1920 --full-page=false overlay.html overlay.png
   ffmpeg -y -loop 1 -i reel_kit/foto_wagner.png -i overlay.png -i reel_kit/trilha_wagner.m4a \
     -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=-0.04,fps=30[bg];[bg][1:v]overlay=0:0[v]" \
     -map "[v]" -map 2:a -t 15 -af "atrim=0:15,afade=t=out:st=13.6:d=1.4" \
     -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k reel.mp4
   ```
   (Se o overlay sair com fundo preto em vez de transparente, renderize com Chromium headless usando
   `--default-background-color=00000000`.)

5. **Entregue** criando `reels_queue/YYYY-MM-DD-<slug>/` com `reel.mp4` + `meta.json`:
   ```json
   {"tema":"...","titulo":"Frasco para ...","caption":"<legenda humana>",
    "schedule_at":"<HOJE>T21:00:00Z","published":false}
   ```
   `21:00Z = 18h de Brasília`. **Regra dura do Publer: vídeo precisa de ≥45 min de antecedência**
   (o publicador ajusta sozinho se estiver apertado). `git add reels_queue/... && git commit && git push`
   → o workflow `reel-publica` agenda no Instagram.

6. **Legenda humana** (obrigatória): cena de consultório/verdade + a promessa do carrossel das 20h +
   ressalva honesta ("nenhum frasco vence rotina ruim") + "ISSO NÃO É UMA RECOMENDAÇÃO. Procure o seu médico."
   + 4-5 hashtags.

7. **Reporte** em 3 linhas: tema, pasta enviada, horário-alvo.

## Regras inegociáveis
- Advertência vermelha no vídeo (já no template) + na legenda.
- Logo + CRM-RJ 0127554-2 no vídeo (já no template).
- CFM: proibido "cura/garante/melhor/especialista".
- Zona segura do Instagram já está no CSS — não mexa nas margens.
