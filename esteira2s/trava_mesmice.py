#!/usr/bin/env python3
"""Trava da mesmice (Wagner, 11/11: "estou vendo usar sempre a mesma edição").

Uso: python esteira2s/trava_mesmice.py AAAA-MM-DD papo|fertilidade LINGUAGEM
Sai com erro (código 1) se a LINGUAGEM de edição repetir a de algum dos 3 Reels
anteriores da mesma conta. Rode ANTES de gastar voz ou render.

LINGUAGEM é o esqueleto visual, não a cor: trocar só a `pele` não muda a linguagem.
Cada meta.json de Reels grava o campo "linguagem". Linguagens conhecidas:
  mapeamento   frase animada + cartão + etiqueta (qualquer pele)
  dossie       rosto o tempo todo com painéis de arquivo
  tela_dividida, react_dividido
  notas        bloco de notas do celular sendo digitado (HyperFrames)
  conversa     conversa de mensagens no celular (HyperFrames)
  slam         tipografia gigante, uma palavra por vez (HyperFrames)
  dados        gráfico animado em tela cheia (HyperFrames)
  arquivo      documentário de papel rasgado e colagem (HyperFrames)
Edição nova = nome novo aqui e no runbook.
"""
import json, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
JANELA = 3


def linguagem_de(meta: dict) -> str | None:
    if meta.get("linguagem"):
        return meta["linguagem"]
    ed = (meta.get("edicao") or "").lower()
    if meta.get("molde") == "carrossel":
        return None
    for chave in ("dossi", "tela dividida", "react"):
        if chave in ed:
            return {"dossi": "dossie", "tela dividida": "tela_dividida", "react": "react_dividido"}[chave]
    return "mapeamento" if "mapeamento" in ed else None


def anteriores(data: str, marca: str) -> list[tuple[str, str]]:
    achados = []
    for pasta in sorted(RAIZ.glob("20??-??-??"), reverse=True):
        if pasta.name >= data:
            continue
        meta = pasta / marca / "meta.json"
        if not meta.exists():
            continue
        ling = linguagem_de(json.loads(meta.read_text()))
        if ling:
            achados.append((pasta.name, ling))
        if len(achados) == JANELA:
            break
    return achados


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    data, marca, nova = sys.argv[1:]
    ant = anteriores(data, marca)
    repetidas = [d for d, l in ant if l == nova]
    print(json.dumps({"data": data, "marca": marca, "linguagem": nova, "anteriores": ant,
                      "aprovado": not repetidas}, ensure_ascii=False))
    if repetidas:
        print(f"MESMICE: '{nova}' já foi usada em {', '.join(repetidas)}. Escolha outra linguagem.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
