# -*- coding: utf-8 -*-
"""Escolhe a trilha do reel do dia, rodando o banco em vez de repetir sempre a mesma.

Uso: python reel_kit/escolhe_trilha.py [AAAA-MM-DD]
Imprime o caminho da trilha. Sem argumento, usa a data de hoje (UTC).

Rotacao deterministica pela data: a mesma data sempre dá a mesma faixa (o build é
reproduzível), mas dias seguidos nunca repetem — o passo 7 é primo com 11, entao a
sequencia percorre as 11 faixas antes de voltar ao começo.
"""
import os, sys, datetime as dt

BASE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(BASE, "trilhas")
PASSO = 7          # primo com o tamanho do banco -> ciclo completo sem repetir
EPOCA = dt.date(2026, 8, 12)


def main():
    faixas = sorted(f for f in os.listdir(DIR) if f.endswith((".m4a", ".mp3")))
    if not faixas:
        print("ERRO: nenhuma trilha em reel_kit/trilhas/", file=sys.stderr)
        return 1
    dia = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.datetime.now(dt.UTC).date()
    i = ((dia - EPOCA).days * PASSO) % len(faixas)
    print(os.path.join(DIR, faixas[i]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
