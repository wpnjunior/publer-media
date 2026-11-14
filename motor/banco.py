# banco.py - banco de rostos reaproveitáveis (Wagner, 13/11 23h40 BRT):
# "antes de produzir veja se tem algum que encaixa; se não, pode fazer o novo e gastar o crédito; com o tempo vamos aumentar a banca".
#
#   python3 banco.py procurar --tipo entrada_noticia [--avatar 6cd9...] [--marca caneta] [--frase "olha só"] [--dias 0]
#       -> imprime o caminho do clipe que encaixa (menos usado primeiro) ou "FALTA" e sai com código 1 (aí gera no HeyGen).
#   python3 banco.py adicionar arquivo.mp4 --tipo cta --frase "..." [--avatar ...] [--marca todas] [--palavras arquivo.json]
#   python3 banco.py usar arquivo.mp4 react_x       (marca o uso, para não repetir o mesmo CTA seguido no mesmo perfil)
#   python3 banco.py listar [--avatar ...]
import argparse, datetime, json, shutil, subprocess, sys, unicodedata
from pathlib import Path

BANCO = Path("/mnt/project-files/esteira2s/banco-rostos")
PADRAO = "6cd9ee3df3544397ad8d38fa091e14cc"  # avatar padrão desde 13/11 23h32 BRT (Wagner)


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def carregar():
    return json.load(open(BANCO / "indice.json"))


def salvar(i):
    json.dump(i, open(BANCO / "indice.json", "w"), ensure_ascii=False, indent=1)


def procurar(a):
    i = carregar()
    hoje = datetime.date.today()
    ok = []
    for c in i["clipes"]:
        if a.tipo not in (c["tipo"], c.get("tipo_extra")):
            continue
        if c.get("avatar") != a.avatar:
            continue
        if a.marca and c.get("marca") not in ("todas", a.marca):
            continue
        if a.frase and norm(a.frase) not in norm(c["frase"]):
            continue
        usos = [u for u in c.get("usado_em", []) if isinstance(u, dict)]
        recente = [u for u in usos if (hoje - datetime.date.fromisoformat(u["data"])).days < a.dias and (not a.marca or u.get("marca") == a.marca)]
        if recente:
            continue
        ok.append((len(usos), c))
    if not ok:
        print(f"FALTA: nenhum clipe {a.tipo} do avatar {a.avatar[:8]}"
              + (f" com '{a.frase}'" if a.frase else "") + ". Gerar no HeyGen e depois rodar banco.py adicionar.")
        sys.exit(1)
    ok.sort(key=lambda x: x[0])
    c = ok[0][1]
    print(BANCO / c["arquivo"])
    print(f"  frase: {c['frase']} | {c['duracao_s']} s | usado {ok[0][0]}x", file=sys.stderr)


def adicionar(a):
    src = Path(a.arquivo)
    dst = BANCO / src.name
    if dst.exists() and dst.resolve() != src.resolve():
        sys.exit(f"já existe {dst.name} no banco; renomeie")
    if dst.resolve() != src.resolve():
        shutil.copy(src, dst)
    if a.palavras:
        shutil.copy(a.palavras, BANCO / (src.stem + ".words.json"))
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dst)], capture_output=True, text=True).stdout)
    i = carregar()
    i["clipes"] = [c for c in i["clipes"] if c["arquivo"] != src.name]
    i["clipes"].append({"arquivo": src.name, "tipo": a.tipo, "marca": a.marca, "frase": a.frase, "duracao_s": round(d, 2),
                        "avatar": a.avatar, "usado_em": [], "entrou_em": str(datetime.date.today())})
    salvar(i)
    print("ok", dst, round(d, 2), "s")


def usar(a):
    i = carregar()
    for c in i["clipes"]:
        if c["arquivo"] == Path(a.arquivo).name:
            c.setdefault("usado_em", []).append({"data": str(datetime.date.today()), "video": a.video, "marca": a.marca})
            salvar(i)
            print("uso anotado", c["arquivo"], a.video)
            return
    sys.exit("clipe não está no banco")


def listar(a):
    for c in carregar()["clipes"]:
        if a.avatar and c.get("avatar") != a.avatar:
            continue
        print(f"{c.get('avatar', '?')[:8]} {c['tipo']:16} {c.get('marca', ''):11} {c['duracao_s']:5} {c['arquivo']:18} {c['frase']}")


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
p = sub.add_parser("procurar"); p.add_argument("--tipo", required=True); p.add_argument("--avatar", default=PADRAO)
p.add_argument("--marca"); p.add_argument("--frase"); p.add_argument("--dias", type=int, default=7, help="não repetir no mesmo perfil dentro de N dias")
p = sub.add_parser("adicionar"); p.add_argument("arquivo"); p.add_argument("--tipo", required=True); p.add_argument("--frase", required=True)
p.add_argument("--avatar", default=PADRAO); p.add_argument("--marca", default="todas"); p.add_argument("--palavras")
p = sub.add_parser("usar"); p.add_argument("arquivo"); p.add_argument("video"); p.add_argument("--marca")
p = sub.add_parser("listar"); p.add_argument("--avatar")
a = ap.parse_args()
{"procurar": procurar, "adicionar": adicionar, "usar": usar, "listar": listar}[a.cmd](a)
