# SABOR — o último passo antes de dar um material como pronto

Se você é uma esteira, um agente ou um script do Dr. Wagner e recebeu a instrução
*"passar no sabor antes de dar como concluído"*, é isto aqui.

## O que é

O sabor é uma passada final no arquivo que **apaga a identidade dele e deixa cada cópia única**.

Todo vídeo e toda imagem saem do editor com rastros: a etiqueta de qual programa codificou,
a data e a hora de criação, o código de tempo da edição e, no caso de material baixado de banco
de imagens, coisas como nome de site, coordenadas de GPS e identificador de direitos autorais.
Dois arquivos gerados pela mesma esteira também saem com a mesma assinatura técnica.

O sabor recodifica o arquivo do zero, zera todos esses campos e muda o conteúdo o suficiente
para que nenhuma cópia seja idêntica a outra, sem que ninguém perceba diferença assistindo.

**O que ele faz, em vídeo:** os mesmos itens da tela de camuflagem do site, feitos aqui no PC:

| item da tela do site | o que o script faz |
|---|---|
| Removedor (EXIF, GPS, câmera, timestamp) | zera todos os metadados, inclusive a etiqueta do codificador |
| Micro-rotação invisível | gira entre 0,25 e 0,35 grau, sorteado |
| Cortar primeiros e últimos 0,5 s | corta 0,5 s de cada ponta |
| Microvariação de velocidade | sorteia entre 0,97x e 1,03x |
| Ajustar pra proporção da plataforma | só com `--crop45` |
| Trocar fundo sonoro | só com `--trilha musica.mp3` |
| Espelhar horizontalmente | **não faz**: a caixa de pergunta tem texto e sairia invertida |

Além disso, por conta própria: zoom de 1,03 com deslocamento de um a dois pixels, ruído leve em
cada quadro, tom do áudio 0,3% mais alto e compressão diferente por arquivo. Sai em mp4
1080x1920, 30 quadros por segundo, sem nenhuma etiqueta.

A trilha segue a regra do site: a música entra por cima e o áudio original fica a 10%. **Nunca use
em reel falado**, porque a voz some.

**O que ele faz, em imagem:** encolhe de um a três pixels, altera o primeiro pixel, salva de novo
sem nenhum dado embutido e varia a qualidade.

**O que ele NÃO faz:** não esconde que o material foi feito com IA. Rosto e voz sintéticos se
reconhecem pela imagem e pelo som, não pelo arquivo. Se alguém prometer isso, está enganado.

## Como usar

```bash
python "C:\Users\Neves\Desktop\CATALOGO_MIDIA\camuflar_forte.py" <entrada> --saida <pasta>
```

- `<entrada>` pode ser **um arquivo** ou **uma pasta**. Com `--recursivo`, entra nas subpastas.
- Aceita `.mp4`, `.mov`, `.m4v`, `.jpg`, `.jpeg`, `.png`.
- Cada saída ganha o sufixo `-sabor` no nome. Vídeo sempre sai `.mp4`.
- Se a saída já existe, ele pula. Para regravar por cima, passe `--refazer`.
- `--crop45` corta de 9:16 para 4:5 tirando mais de baixo, para preservar o topo. Use só se pedirem.
- `--padrao "*-lento.mp4"` filtra por nome, quando a pasta mistura coisas.
- **Nunca passa sabor em cima de sabor.** Arquivo cujo nome termina em `-sabor`, `-s`, `-s2`... é ignorado sozinho. Em 23/09 uma pasta misturada fez o script camuflar cópias já camufladas e dobrar o tempo.

Custo: cerca de **100 segundos por vídeo de um minuto** e **1 segundo por imagem**, neste PC.
A rotação é o que mais pesa.

Exemplo de uma esteira que termina de montar os reels do dia:

```bash
python "C:\Users\Neves\Desktop\CATALOGO_MIDIA\camuflar_forte.py" "C:\saida\reels_de_hoje" --saida "C:\saida\reels_de_hoje\com_sabor"
```

O que vai para a publicação é o arquivo **com sabor**, nunca o original.

## Como conferir que passou de verdade

Um arquivo com sabor tem que passar nestes cinco testes. A conferência importa: em 23/09/2026
trinta arquivos saíram com a etiqueta do codificador de volta, porque limpar os metadados de
entrada não impede o programa de escrever a própria etiqueta na saída.

```bash
ffprobe -v error -show_entries format_tags -of default=nw=1 arquivo-sabor.mp4
```

1. Em `format_tags` só podem aparecer `major_brand`, `minor_version` e `compatible_brands`.
   Se aparecer `encoder`, `creation_time` ou `timecode`, **não passou**.
2. Nos primeiros 300 KB do arquivo não pode existir o texto `x264 core`, que revela versão e
   parâmetros de quem codificou.
3. Depois do último bloco do mp4 não pode sobrar nenhum byte. Lixo solto no fim do arquivo faz
   validador de upload recusar o vídeo.
4. O vídeo tem que continuar 1080x1920 a 30 quadros por segundo, com faixa de áudio presente.
5. A voz não pode sair do lugar. O atraso aceitável é de 40 milésimos de segundo.

O script `cacar_pistas.py`, na mesma pasta, varre uma pasta inteira e aponta o que ficou para trás:

```bash
python "C:\Users\Neves\Desktop\CATALOGO_MIDIA\cacar_pistas.py" <pasta>
```

Ele escreve um `pistas.csv` com uma linha por arquivo. Palavras suspeitas encontradas no meio dos
dados comprimidos costumam ser coincidência de bytes, não texto de verdade. Confira o contexto
antes de tratar como achado.

## O que não usar

**Não mande vídeo para o site de camuflagem** (`adsearcher.pro/dashboard/camuflagem`). Com qualquer
ajuste ligado, ele grava a tela em tempo real, e nesta máquina o resultado sai destruído: um reel
de 60 segundos virou 437 segundos com 967 quadros, ou seja, 2 quadros por segundo, com o áudio
arrastado e sem duração no cabeçalho. Foram 624 arquivos perdidos assim, medidos em 23/09/2026.
Para imagem o site funciona, mas o script local também faz e é mais rápido.
