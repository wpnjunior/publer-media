"""Transforma o plano de edição (escrito pela rotina) numa linha do tempo exata.

Uso: python planejar.py plano.json words.json duracao_segundos timeline.json

O plano marca cada elemento por um trecho do roteiro ("quando": "Um estudo americano").
Aqui cada trecho vira segundos (pela fala real do words.json) e montamos os enquadramentos:
- tela cheia no gancho, nos closes, nos números gigantes e nos carimbos;
- no resto, o formato escolhido (tela_dividida ou dinamica), com troca de enquadramento
  a cada 2 a 3 s, sempre num limite de palavra.
O comp.html só desenha o que está na timeline; o mix.py usa os mesmos tempos para os efeitos.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

FIM_DUR = 2.6  # cartão final depois da última palavra


def n(p: str) -> str:
    p = unicodedata.normalize("NFD", p.lower())
    p = "".join(c for c in p if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", p)


def achar(words: list[dict], trecho: str, depois: float = 0.0) -> tuple[float, float, int]:
    """Início e fim (s) do trecho no roteiro falado, e o índice da 1ª palavra."""
    alvo = [n(x) for x in trecho.split() if n(x)]
    ws = [n(w["w"]) for w in words]
    melhor = None
    for i in range(len(ws)):
        if words[i]["s"] < depois - 0.01:
            continue
        ok = 0
        for k, a in enumerate(alvo):
            if i + k < len(ws) and ws[i + k] == a:
                ok += 1
        if ok == len(alvo):
            j = i + len(alvo) - 1
            return words[i]["s"], words[j]["e"], i
        if ok and (melhor is None or ok > melhor[0]):
            melhor = (ok, i)
    if melhor and melhor[0] >= max(1, len(alvo) // 2):
        i = melhor[1]
        j = min(len(words) - 1, i + len(alvo) - 1)
        return words[i]["s"], words[j]["e"], i
    raise SystemExit(f"trecho não encontrado no roteiro falado: {trecho!r}")


def fim_da_frase(words: list[dict], i: int) -> float:
    for j in range(i, len(words)):
        if words[j]["w"].rstrip().endswith((".", "?", "!")):
            return words[j]["e"]
    return words[-1]["e"]


def corte_proximo(words: list[dict], t: float) -> float:
    """Início de palavra mais perto de t (cortes caem entre palavras)."""
    return min((w["s"] for w in words), key=lambda s: abs(s - t))


def main() -> None:
    plano = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    words = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    dur = float(sys.argv[3])
    fala_fim = words[-1]["e"]
    total = round(max(dur, fala_fim) + FIM_DUR, 2)
    formato = plano.get("formato", "tela_dividida")

    tl: dict = {
        "fps": 25,
        "dur_video": dur,
        "total": total,
        "fala_fim": fala_fim,
        "formato": formato,
        "estilo_painel": plano.get("estilo_painel", "caderno"),
        "trilha": plano.get("trilha", ""),
        "pele": plano.get("pele", "mesa"),
        "caixa": plano.get("caixa_pergunta") or None,  # gancho dentro da caixinha de pergunta: true ou {"cab":..., "res":...}
        "titulo": plano.get("titulo", ""),
        "rosto": plano.get("rosto", [0.44, 0.37]),
        "words": words,
        "destaques": sorted({n(d) for d in plano.get("destaques", []) if n(d)}),
        "paineis": [],
        "carimbos": [],
        "numeros": [],
        "fonte": None,
        "fim": plano.get("fim", {}),
        "shots": [],
        "eventos": [],  # para o mix (whoosh, thud, pop, ding)
    }

    # painéis do caderno: cada um fica até o próximo começar
    pans = []
    for p in plano.get("paineis", []):
        t0, _, _ = achar(words, p["quando"])
        q = dict(p)
        q["t0"] = round(t0, 3)
        pans.append(q)
    pans.sort(key=lambda x: x["t0"])
    for k, p in enumerate(pans):
        p["t1"] = pans[k + 1]["t0"] if k + 1 < len(pans) else fala_fim
        tl["paineis"].append(p)
        tl["eventos"].append({"t": p["t0"], "sfx": "pop"})

    forcados = []  # trechos de tela cheia: (t0, t1, tipo)
    g_fim = min(fim_da_frase(words, 0), 3.2)
    forcados.append((0.0, g_fim, "gancho"))

    for c in plano.get("carimbos", []):
        t0, _, _ = achar(words, c["quando"])
        tl["carimbos"].append({"t0": round(t0, 3), "t1": round(t0 + 1.4, 3), "texto": c["texto"]})
        forcados.append((t0, t0 + 1.4, "carimbo"))
        tl["eventos"].append({"t": t0, "sfx": "thud"})
    for c in plano.get("numeros", []):
        t0, _, _ = achar(words, c["quando"])
        tl["numeros"].append({"t0": round(t0, 3), "t1": round(t0 + 1.9, 3), "texto": c["texto"], "legenda": c.get("legenda", "")})
        forcados.append((t0, t0 + 1.9, "numero"))
        tl["eventos"].append({"t": t0, "sfx": "thud"})
    for c in plano.get("closes", []):
        t0, t1, _ = achar(words, c)
        forcados.append((t0, max(t1, t0 + 1.5), "close"))

    if plano.get("fonte"):
        f = plano["fonte"]
        t0, _, _ = achar(words, f["quando"])
        t1 = achar(words, f["ate"], depois=t0)[1] if f.get("ate") else t0 + 6
        tl["fonte"] = {"t0": round(t0, 3), "t1": round(t1, 3), "texto": f["texto"]}
        tl["eventos"].append({"t": t0, "sfx": "ding"})

    if plano.get("seguir"):  # adesivo "curte + segue" na tela, junto da cobrança falada no meio
        sg = plano["seguir"]
        t0, t1, _ = achar(words, sg["quando"])
        tl["seguir"] = {"t0": round(t0, 3), "t1": round(max(t1, t0 + 3.0), 3), "texto": sg.get("texto", "curte + segue"),
                        "arroba": sg.get("arroba", "@dr.wagnernovaesjr")}
        tl["eventos"].append({"t": t0, "sfx": "pop"})

    if formato == "mapeamento":
        tl["_pasta"] = str(Path(sys.argv[4]).parent)
        mapeamento(plano, words, tl, forcados, fala_fim, total)
        tl.pop("_pasta", None)
        Path(sys.argv[4]).write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
        tipos: dict = {}
        for c in tl["cenas"]:
            tipos[c["tipo"]] = tipos.get(c["tipo"], 0) + 1
        print(f"total {total}s, mapeamento: {len(tl['shots'])} enquadramentos, cenas {tipos}")
        return

    # junta os forçados que se sobrepõem
    forcados.sort()
    fz: list[list] = []
    for a, b, tipo in forcados:
        if fz and a <= fz[-1][1] + 0.3:
            fz[-1][1] = max(fz[-1][1], b)
        else:
            fz.append([a, b, tipo])

    # monta os enquadramentos
    shots = []
    cur = 0.0
    zooms_full = [1.18, 1.38, 1.05]
    zooms_base = [1.0, 1.12] if formato == "tela_dividida" else [1.0, 1.16, 1.3]
    kz = 0
    for a, b, tipo in fz + [[fala_fim, fala_fim, "fim"]]:
        a = max(a, cur)
        # trecho livre entre cur e a: formato base, troca a cada ~2,6 s
        t = cur
        while a - t > 0.4:
            alvo = t + 2.6
            if a - alvo < 1.2:
                alvo = a
            else:
                alvo = corte_proximo(words, alvo)
                if alvo <= t + 0.8:
                    alvo = a
            modo = "split" if formato == "tela_dividida" else "full"
            shots.append({"t0": round(t, 3), "t1": round(alvo, 3), "modo": modo, "zoom": zooms_base[kz % len(zooms_base)], "pan": [-1, 1][kz % 2]})
            kz += 1
            t = alvo
        if tipo != "fim" and b > a:
            z = 1.0 if tipo == "gancho" else zooms_full[kz % len(zooms_full)]
            if tipo == "close":
                z = 1.38
            shots.append({"t0": round(a, 3), "t1": round(b, 3), "modo": "full", "zoom": z, "pan": 0, "tipo": tipo})
            kz += 1
            cur = b
        else:
            cur = max(cur, a)
    if shots:
        shots[-1]["t1"] = round(fala_fim, 3)
    shots.append({"t0": round(fala_fim, 3), "t1": total, "modo": "fim", "zoom": 1.0, "pan": 0})
    # emenda buracos
    for k in range(1, len(shots)):
        shots[k]["t0"] = shots[k - 1]["t1"]
    tl["shots"] = [s for s in shots if s["t1"] - s["t0"] > 0.05]
    for s in tl["shots"][1:]:
        tl["eventos"].append({"t": s["t0"], "sfx": "whoosh"})
    tl["eventos"].append({"t": fala_fim, "sfx": "brilho"})
    tl["eventos"].sort(key=lambda e: e["t"])

    Path(sys.argv[4]).write_text(json.dumps(tl, ensure_ascii=False, indent=1), encoding="utf-8")
    modos = {}
    for s in tl["shots"]:
        modos[s["modo"]] = modos.get(s["modo"], 0) + 1
    print(f"total {total}s, {len(tl['shots'])} enquadramentos {modos}, {len(tl['paineis'])} painéis, "
          f"{len(tl['carimbos'])} carimbos, {len(tl['numeros'])} números")


TIPOS_CENA = {"rosto", "mapa", "cartao", "foto", "documento", "bolinhas", "citacao", "etiqueta", "barra",
              "regua", "checklist", "broll", "celular", "frase"}  # regua = Linha do tempo; checklist = Lista para salvar;
# broll = foto real em tela cheia; celular = comentário, post ou manchete na tela de um telefone
BG_BANK = Path(__file__).resolve().parents[2] / "bg_bank"


def _imagem(nome: str, pasta: str) -> str:
    """Nome de foto do bg_bank vira img/<nome> dentro da pasta de trabalho (o comp.html só enxerga a pasta)."""
    if not nome or "/" in nome:
        return nome
    origem = BG_BANK / nome
    if not origem.exists():
        raise SystemExit(f"foto não existe no bg_bank: {nome}")
    dest = Path(pasta) / "img"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / nome).write_bytes(origem.read_bytes())
    return f"img/{nome}"


def _norm(x: str) -> str:
    import unicodedata
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(ch for ch in x if ch.isalnum() or ch == " ")


def _eh_destaque(w: str, dest: set) -> bool:
    return _norm(w).strip() in dest


def _rosto_gerado_aparece(cenas: list[dict], pasta: str) -> list[dict]:
    """Clipe de rosto do banco (fala de verdade) sempre aparece: nenhuma cena gráfica fica por cima dele."""
    arq = Path(pasta) / "trechos.json"
    if not arq.exists():
        return cenas
    rostos = [(m["t0"], m["t1"]) for m in json.loads(arq.read_text()) if m["tipo"] == "rosto"]
    out = [dict(c) for c in cenas]
    for a, b in rostos:
        a, b = a + 0.05, b - 0.05
        novo: list[dict] = []
        for c in out:
            if c["tipo"] == "rosto" or c["t1"] <= a or c["t0"] >= b:
                novo.append(c)
                continue
            if a - c["t0"] > 0.6:
                novo.append(dict(c, t1=round(a, 3)))
            novo.append({"tipo": "rosto", "t0": round(max(a, c["t0"]), 3), "t1": round(min(b, c["t1"]), 3)})
            if c["t1"] - b > 0.6:
                novo.append(dict(c, t0=round(b, 3)))
        out = novo
    # junta rostos vizinhos
    junt: list[dict] = []
    for c in out:
        if junt and c["tipo"] == "rosto" and junt[-1]["tipo"] == "rosto" and not junt[-1].get("gancho") and abs(c["t0"] - junt[-1]["t1"]) < 0.7:
            junt[-1]["t1"] = c["t1"]
        else:
            junt.append(c)
    return junt


def _sem_rosto_na_narracao(cenas: list[dict], words: list[dict], plano: dict, pasta: str) -> list[dict]:
    """TRAVA: nos trechos de narração (voz sobre foto parada) o rosto nunca aparece. O pedaço de cena
    "rosto" que cair numa narração vira foto real em tela cheia (broll), trocando a cada ~3 s."""
    arq = Path(pasta) / "trechos.json"
    if not arq.exists():
        return cenas
    vozes = [(m["t0"], m["t1"]) for m in json.loads(arq.read_text()) if m["tipo"] == "voz"]
    dest = {t for d in plano.get("destaques", []) for t in _norm(d).split() if len(t) > 3}
    out: list[dict] = []
    kf = 0
    for c in cenas:
        if c["tipo"] != "rosto":
            if c.get("pip") and any(a < c["t1"] and b > c["t0"] for a, b in vozes):
                c = dict(c, pip=False)  # a bolha também é rosto parado
            out.append(c)
            continue
        t = c["t0"]
        pedacos = []
        for a, b in vozes:
            a2, b2 = max(a - 0.12, c["t0"]), min(b + 0.12, c["t1"])
            if b2 - a2 > 0.25:
                pedacos.append((a2, b2))
        for a, b in pedacos:
            if a - t > 0.25:
                out.append(dict(c, t0=round(t, 3), t1=round(a, 3)))
            else:
                a = t
            x = a
            while b - x > 0.05:
                y = b if b - x < 3.6 else corte_proximo(words, x + 2.5)
                if y <= x + 1.0 or y > b:
                    y = b
                # Reels é todo edição (Wagner, 11/11): sem foto de banco; o trecho sem cena vira FRASE animada
                toks = [{"w": w["w"], "t": round(max(w["s"] - x, 0), 2), "d": _eh_destaque(w["w"], dest)}
                        for w in words if x - 0.05 <= w["s"] < y - 0.05]
                if toks:
                    out.append({"tipo": "frase", "palavras": toks, "t0": round(x, 3), "t1": round(y, 3), "k": kf})
                    kf += 1
                elif out and out[-1]["tipo"] != "rosto":
                    out[-1]["t1"] = round(y, 3)
                x = y
            t = b
        if c["t1"] - t > 0.25:
            resto = {k: v for k, v in c.items() if k != "gancho"} if t > c["t0"] else c
            out.append(dict(resto, t0=round(t, 3)))
    # no máximo 2 fotos por Reels (Wagner, 11/11): só duas frases, bem separadas, viram foto
    fotos = list(plano.get("broll", []))[: int(plano.get("max_fotos", 2))]
    fr = [i for i, c in enumerate(out) if c["tipo"] == "frase"]
    if fotos and len(fr) >= 4:
        alvos = [fr[len(fr) // 3], fr[(2 * len(fr)) // 3]][: len(fotos)]
        for j, i in enumerate(alvos):
            out[i] = {"tipo": "broll", "imagem": fotos[j], "t0": out[i]["t0"], "t1": out[i]["t1"], "k": j}
    return out


def mapeamento(plano: dict, words: list[dict], tl: dict, forcados: list, fala_fim: float, total: float) -> None:
    """Formato Mapeamento: explicador em cenas gráficas de tela cheia (mapa 3D em papel antigo,
    cartões coloridos, fotos com fita, bolinhas de porcentagem, citação, etiqueta de data, barra)
    intercaladas com ele em tela cheia. Cada cena vale do seu "quando" até a próxima começar.
    Gancho e closes são sempre o rosto dele. Cenas gráficas longas ganham a bolha dele no canto
    quando a cena pede ("pip": true)."""
    cenas = []
    for c in plano.get("cenas", []):
        if c.get("tipo") not in TIPOS_CENA:
            raise SystemExit(f"cena com tipo desconhecido: {c.get('tipo')!r} (use {sorted(TIPOS_CENA)})")
        t0, _, _ = achar(words, c["quando"])
        q = dict(c)
        q["t0"] = round(t0, 3)
        cenas.append(q)
    cenas.sort(key=lambda x: x["t0"])
    g_fim = forcados[0][1]  # fim do gancho
    # closes viram cenas de rosto (por cima do que estiver no ar)
    for a, b, tipo in forcados[1:]:
        if tipo == "close":
            cenas.append({"tipo": "rosto", "t0": round(a, 3), "close": True, "ate": round(b, 3)})
    cenas = [c for c in cenas if c["t0"] >= g_fim - 0.01]
    cenas.append({"tipo": "rosto", "t0": 0.0, "gancho": True})
    cenas.sort(key=lambda x: (x["t0"], 0 if x.get("close") else 1))
    out: list[dict] = []
    for c in cenas:
        if out and abs(c["t0"] - out[-1]["t0"]) < 0.3:
            if c.get("close"):
                out[-1] = c
            continue
        out.append(c)
    # duração: até a próxima; um close devolve a cena interrompida depois do seu trecho
    final = []
    for k, c in enumerate(out):
        prox = out[k + 1]["t0"] if k + 1 < len(out) else fala_fim
        if c.get("close") and c.get("ate", prox) + 0.6 < prox and final:
            final.append(dict(c, t1=round(c["ate"], 3)))
            ant = dict(next(x for x in reversed(final[:-1]) if not x.get("close")))
            ant.update({"t0": round(c["ate"], 3), "t1": round(prox, 3), "volta": True})
            final.append(ant)
        else:
            final.append(dict(c, t1=round(prox, 3)))
    # ritmo do modelo: cena gráfica não passa de ~4 s; o resto volta para o rosto dele
    ritmo = []
    for c in final:
        if c["tipo"] != "rosto" and c["t1"] - c["t0"] > 5.5:
            corte = corte_proximo(words, c["t0"] + 3.8)
            if c["t0"] + 2.5 < corte < c["t1"] - 1.2:
                ritmo.append(dict(c, t1=round(corte, 3)))
                ritmo.append({"tipo": "rosto", "t0": round(corte, 3), "t1": c["t1"]})
                continue
        ritmo.append(c)
    ritmo = _rosto_gerado_aparece(ritmo, tl["_pasta"])
    ritmo = _sem_rosto_na_narracao(ritmo, words, plano, tl["_pasta"])
    for c in ritmo:
        if c.get("imagem"):
            c["imagem"] = _imagem(c["imagem"], tl["_pasta"])
    tl["cenas"] = [c for c in ritmo if c["t1"] - c["t0"] > 0.05]

    shots = []
    zooms = [1.0, 1.15, 1.3, 1.08]
    kz = 0
    for i, c in enumerate(tl["cenas"]):
        if c["tipo"] != "rosto":
            shots.append({"t0": c["t0"], "t1": c["t1"], "modo": "cena", "cena": i, "zoom": 1.0, "pan": 0})
            tl["eventos"].append({"t": c["t0"], "sfx": "whoosh" if c["tipo"] == "mapa" else "pop"})
            continue
        # rosto: troca de zoom a cada ~2,6 s (corte seco, como no modelo)
        t = c["t0"]
        while c["t1"] - t > 0.05:
            alvo = c["t1"] if c["t1"] - t < 3.8 else corte_proximo(words, t + 2.6)
            if alvo <= t + 0.8:
                alvo = c["t1"]
            z = 1.0 if c.get("gancho") and t == 0 else (1.38 if c.get("close") else zooms[kz % len(zooms)])
            tipo = "gancho" if c.get("gancho") and t == 0 else ("close" if c.get("close") else None)
            s = {"t0": round(t, 3), "t1": round(alvo, 3), "modo": "full", "zoom": z, "pan": [-1, 1][kz % 2]}
            if tipo:
                s["tipo"] = tipo
            shots.append(s)
            kz += 1
            t = alvo
    shots.append({"t0": round(fala_fim, 3), "t1": total, "modo": "fim", "zoom": 1.0, "pan": 0})
    for k in range(1, len(shots)):
        shots[k]["t0"] = shots[k - 1]["t1"]
    tl["shots"] = [s for s in shots if s["t1"] - s["t0"] > 0.05]
    tl["eventos"].append({"t": fala_fim, "sfx": "brilho"})
    tl["eventos"].sort(key=lambda e: e["t"])


if __name__ == "__main__":
    main()
