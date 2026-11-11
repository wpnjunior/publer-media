#!/usr/bin/env python3
"""Quadro único dos 30 dias: uma linha por dia, uma coluna por perfil.
Fonte da verdade: esteira2s/<data>/<marca>/meta.json (status) + grade.json (o que está previsto).
Uso: python3 esteira2s/quadro.py [saida.md]   (sem saída, imprime)
"Pronto" só conta quando o status é agendado ou publicado."""
import json, sys, pathlib, datetime
R = pathlib.Path(__file__).parent
g = json.loads((R / "grade.json").read_text())
ROT = {"agendado": "AGENDADO", "publicado": "PUBLICADO", "pronto_para_agendar": "pronto, falta agendar",
       "aguardando_wagner_ver_edicao": "esperando o Wagner ver", "reprovado_refazer": "REFAZER"}
def celula(marca, data, d):
    m = R / data / marca / "meta.json"
    st = json.loads(m.read_text()).get("status") if m.exists() else None
    if not st:
        st = "agendado" if d.get("agendado") else ("pronto_antigo" if d.get("pronto") else "falta")
    rot = ROT.get(st, {"pronto_antigo": "pronto antigo, conferir avatar", "falta": "FALTA PRODUZIR"}.get(st, st))
    tipo = d.get("formato") or d.get("tipo") or "carrossel"
    return st, f"{rot} · {tipo} · {(d.get('tema') or d.get('assunto') or '')[:40]}"
linhas, conta = [], {}
datas = sorted(set().union(*[set(v["dias"]) for v in g["marcas"].values()]))
marcas = list(g["marcas"])
for data in datas:
    cols = []
    for mk in marcas:
        st, txt = celula(mk, data, g["marcas"][mk]["dias"].get(data, {}))
        conta.setdefault(mk, {}).setdefault(st, 0); conta[mk][st] += 1
        cols.append(txt)
    linhas.append(f"| {data[8:]}/{data[5:7]} | " + " | ".join(cols) + " |")
out = [f"Quadro gerado em {datetime.date.today():%d/%m/%Y}", ""]
for mk in marcas:
    out.append(f"- {mk}: " + ", ".join(f"{k} {v}" for k, v in sorted(conta[mk].items())))
out += ["", "| Dia | " + " | ".join(marcas) + " |", "|---|" + "---|" * len(marcas)] + linhas
txt = "\n".join(out) + "\n"
(pathlib.Path(sys.argv[1]).write_text(txt) if len(sys.argv) > 1 else print(txt))
