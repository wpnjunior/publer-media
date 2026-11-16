# -*- coding: utf-8 -*-
"""Publica REELS do @aquacultivonovaes pela API do Instagram (login do Instagram, graph.instagram.com).
Roda no GitHub Actions (.github/workflows/camarao-reels.yml). O carrossel continua no publish_queue_ig.py.

  python pipeline/publish_reels_ig.py publicar            -> publica UM Reels vencido da fila (o mais antigo)
  python pipeline/publish_reels_ig.py publicar --seco     -> ensaio: simula as respostas da API, nada sai
  python pipeline/publish_reels_ig.py checar              -> confere a fila (campos, datas, URL) sem rede

Fila: camarao/reels_queue/<AAAA-MM-DD>-<slug>/meta.json (o mp4 NAO vai para o git):
  {"video_url": "https://...mp4", "caption": "...", "publicar_em": "2026-11-20 18:00",
   "share_to_feed": true, "cover_ms": 1500, "published": false}
publicar_em e hora de Brasilia (sem fuso = BRT, -03:00). O cron do GitHub atrasa horas neste repo,
por isso o script publica o item vencido mais antigo, um por execucao. Item com mais de ATRASO_MAX_H
de atraso nao sai sozinho (em 23/10 um carrossel velho foi ao ar por falta dessa trava).

Fluxo da API: POST /{ig}/media (media_type=REELS, video_url, caption, share_to_feed, thumb_offset)
-> GET /{container}?fields=status_code a cada ~15 s ate FINISHED (ERROR/EXPIRED ou ~10 min = erro claro)
-> POST /{ig}/media_publish (creation_id) -> grava no meta.json: published, status, ig_media, published_at.
Nunca duplica: item publicado e pulado; container ja criado e reaproveitado; e antes de publicar o
script confere se a mesma legenda ja esta no ar na conta (se o commit do meta.json tiver falhado).
O token nunca e impresso (toda saida passa por limpa()).
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

IG = os.environ.get("IG_ID", "17841452090508191")
GRAPH = os.environ.get("GRAPH_URL", "https://graph.instagram.com/v25.0")
FILA = os.environ.get("FILA_REELS", "camarao/reels_queue")
ATRASO_MAX_H = float(os.environ.get("ATRASO_MAX_H", "48"))
INTERVALO_MIN_H = float(os.environ.get("INTERVALO_MIN_H", "3"))   # entre dois Reels da mesma conta
ESPERA_S = 15                 # intervalo entre consultas do container
ESPERA_MAX_S = 600            # ~10 min
BRT = dt.timezone(dt.timedelta(hours=-3))   # o Brasil nao tem horario de verao desde 2019


_AGORA = None   # so em teste (--agora): finge outra hora


def agora_utc():
    return _AGORA or dt.datetime.now(dt.timezone.utc)


def limpa(texto):
    """Tira o token de qualquer texto antes de imprimir."""
    texto = str(texto)
    tok = os.environ.get("IG_TOKEN", "").strip()
    if tok:
        texto = texto.replace(tok, "***")
        texto = texto.replace(urllib.parse.quote(tok, safe=""), "***")
    return texto


def log(*partes):
    print(limpa(" ".join(str(p) for p in partes)), flush=True)


# ---------------------------------------------------------------- API (real e simulada)
class ApiReal:
    seco = False

    def __init__(self):
        self.tok = os.environ.get("IG_TOKEN", "").strip()
        if not self.tok:
            raise SystemExit("ERRO: falta o segredo IG_TOKEN (IG_TOKEN_CAMARAO no GitHub). Nada foi publicado.")

    def req(self, m, p, params=None):
        params = dict(params or {}, access_token=self.tok)
        data = urllib.parse.urlencode(params).encode()
        url = GRAPH + p
        if m == "GET":
            url, data = url + "?" + data.decode(), None
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, data=data, method=m), timeout=120)
            return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            return {"_err": e.code, "_b": limpa(e.read().decode()[:600])}
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return {"_err": "rede", "_b": limpa(repr(e))[:300]}

    def dormir(self, s):
        time.sleep(s)


class ApiSeca:
    """Respostas falsas no formato da Graph API. Nenhuma chamada de rede."""
    seco = True

    def __init__(self, cenario="ok"):
        self.cenario = cenario
        self.no_ar = []                 # legendas que a conta "ja tem" (cenario ja_no_ar)
        self.consultas = 0
        self.chamadas = []

    def req(self, m, p, params=None):
        params = dict(params or {})
        self.chamadas.append((m, p, sorted(params)))
        if m == "GET" and p.endswith("/media"):
            itens = [{"id": "seco-antigo-%d" % i, "caption": c, "media_product_type": "REELS",
                      "timestamp": (agora_utc() - dt.timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%S+0000"),
                      "permalink": "https://www.instagram.com/reel/SECO%d/" % i} for i, c in enumerate(self.no_ar)]
            return {"data": itens}
        if m == "POST" and p.endswith("/media"):
            return {"id": "seco-container-17900000000000001"}
        if m == "GET" and "fields" in params and "status_code" in params["fields"]:
            self.consultas += 1
            if self.cenario == "erro":
                return {"status_code": "ERROR", "status": "Error: video com proporcao invalida (simulado)",
                        "id": p.strip("/")}
            if self.cenario == "expira":
                return {"status_code": "EXPIRED", "id": p.strip("/")}
            if self.cenario == "demora" or self.consultas < 3:
                return {"status_code": "IN_PROGRESS", "id": p.strip("/")}
            return {"status_code": "FINISHED", "id": p.strip("/")}
        if m == "POST" and p.endswith("/media_publish"):
            return {"id": "seco-media-18000000000000001"}
        if m == "GET" and "permalink" in params.get("fields", ""):
            return {"permalink": "https://www.instagram.com/reel/SECO/", "id": p.strip("/")}
        return {"_err": 400, "_b": "chamada inesperada no modo seco: %s %s" % (m, p)}

    def dormir(self, s):
        pass


# ---------------------------------------------------------------- fila
def ler(pasta):
    with open(os.path.join(pasta, "meta.json"), encoding="utf-8") as f:
        return json.load(f)


def gravar(pasta, meta):
    caminho = os.path.join(pasta, "meta.json")
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, caminho)


def quando(meta):
    """publicar_em em BRT -> datetime UTC. Aceita '2026-11-20 18:00', '2026-11-20T18:00', com ou sem fuso."""
    txt = str(meta.get("publicar_em") or "").strip().replace(" ", "T")
    if not txt:
        raise ValueError("sem publicar_em")
    t = dt.datetime.fromisoformat(txt.replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=BRT)
    return t.astimezone(dt.timezone.utc)


def expira_em(url):
    """URL assinada (HeyGen/CloudFront/S3) traz Expires=<epoch> ou X-Amz-Date+X-Amz-Expires."""
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    try:
        if "Expires" in q:
            return dt.datetime.fromtimestamp(int(q["Expires"][0]), dt.timezone.utc)
        if "X-Amz-Date" in q and "X-Amz-Expires" in q:
            ini = dt.datetime.strptime(q["X-Amz-Date"][0], "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)
            return ini + dt.timedelta(seconds=int(q["X-Amz-Expires"][0]))
    except (ValueError, OverflowError):
        return None
    return None


def problemas(meta):
    """Lista o que impede a publicacao (sem rede)."""
    p = []
    url = str(meta.get("video_url") or "")
    if not url.startswith("https://"):
        p.append("video_url precisa ser https publica (o mp4 nao vai para o git)")
    cap = meta.get("caption")
    if not isinstance(cap, str) or not cap.strip():
        p.append("caption vazia")
    else:
        if len(cap) > 2200:
            p.append("caption com %d caracteres (limite do Instagram: 2200)" % len(cap))
        if cap.count("#") > 30:
            p.append("caption com mais de 30 hashtags")
    if "cover_ms" in meta and not (isinstance(meta["cover_ms"], int) and meta["cover_ms"] >= 0):
        p.append("cover_ms precisa ser inteiro >= 0 (milissegundos)")
    if "share_to_feed" in meta and not isinstance(meta["share_to_feed"], bool):
        p.append("share_to_feed precisa ser true ou false")
    try:
        quando(meta)
    except ValueError as e:
        p.append("publicar_em invalido (%s); use '2026-11-20 18:00' (hora de Brasilia)" % e)
    exp = expira_em(url) if url else None
    if exp and exp <= agora_utc():
        p.append("video_url EXPIROU em %s UTC: gere o link de novo ou hospede o mp4 em lugar fixo" % exp.strftime("%d/%m %H:%M"))
    return p


def pastas_da_fila():
    return sorted(d.rstrip("/\\") for d in glob.glob(os.path.join(FILA, "*", "")) if os.path.exists(os.path.join(d, "meta.json")))


def escolher(agora):
    pastas = pastas_da_fila()
    if not pastas:
        return None, "fila vazia (%s)" % FILA
    ultimo = None
    for d in pastas:
        m = ler(d)
        if m.get("published") and m.get("published_at"):
            try:
                t = dt.datetime.fromisoformat(m["published_at"].replace("Z", "+00:00"))
            except ValueError:
                continue
            ultimo = t if ultimo is None or t > ultimo else ultimo
    if ultimo and agora - ultimo < dt.timedelta(hours=INTERVALO_MIN_H):
        return None, "um Reels saiu ha menos de %g h (%s UTC); o proximo fica para a proxima execucao" % (
            INTERVALO_MIN_H, ultimo.strftime("%d/%m %H:%M"))
    motivos = []
    for d in pastas:
        m = ler(d)
        nome = os.path.basename(d)
        if m.get("published"):
            continue
        if str(m.get("status", "")).startswith("erro_"):
            motivos.append(nome + ": travado (a Meta recusou o video); corrija e apague container_id, status e erro")
            continue
        try:
            t = quando(m)
        except ValueError:
            motivos.append(nome + ": publicar_em invalido")
            continue
        if t > agora:
            motivos.append(nome + ": ainda nao venceu (%s BRT)" % t.astimezone(BRT).strftime("%d/%m %H:%M"))
            continue
        if agora - t > dt.timedelta(hours=ATRASO_MAX_H):
            motivos.append(nome + ": atrasado mais de %g h, nao sai sozinho (mude publicar_em para reagendar)" % ATRASO_MAX_H)
            continue
        return d, ""
    return None, "nenhum Reels vencido. " + "; ".join(motivos)


# ---------------------------------------------------------------- publicacao
def ja_no_ar(api, caption):
    """Procura a mesma legenda entre as ultimas midias da conta (rede de seguranca contra duplicar)."""
    r = api.req("GET", "/%s/media" % IG, {"fields": "id,caption,media_product_type,timestamp,permalink", "limit": "12"})
    if "_err" in r:
        log("AVISO: nao consegui listar as midias da conta para checar duplicata:", json.dumps(r)[:300])
        return None
    alvo = caption.strip()
    for item in r.get("data", []):
        if (item.get("caption") or "").strip() == alvo:
            return item
    return None


def video_acessivel(url):
    """Baixa 1 KB do mp4 (Range) para saber se a Meta vai conseguir buscar o arquivo."""
    pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Range": "bytes=0-1023"})
    try:
        r = urllib.request.urlopen(pedido, timeout=60)
        tipo = r.headers.get("Content-Type", "")
        r.read(1024)
        if "video" not in tipo and "octet-stream" not in tipo:
            return False, "Content-Type inesperado: %s" % (tipo or "vazio")
        return True, tipo
    except urllib.error.HTTPError as e:
        return False, "HTTP %s" % e.code
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return False, repr(e)[:200]


def esperar_container(api, cid):
    passos = ESPERA_MAX_S // ESPERA_S
    ultimo = None
    for i in range(passos):
        s = api.req("GET", "/" + cid, {"fields": "status_code,status"})
        if "_err" in s:
            log("  consulta %d: falha de rede/API, tento de novo:" % (i + 1), json.dumps(s)[:200])
            api.dormir(ESPERA_S)
            continue
        ultimo = s.get("status_code")
        log("  consulta %d: status_code=%s" % (i + 1, ultimo))
        if ultimo in ("FINISHED", "PUBLISHED"):
            return ultimo, s
        if ultimo in ("ERROR", "EXPIRED"):
            return ultimo, s
        api.dormir(ESPERA_S)
    return "TEMPO", {"status_code": ultimo}


def publicar(api, pasta, gravar_meta=True, conferir_url=True):
    meta = ler(pasta)
    nome = os.path.basename(pasta)
    if meta.get("published"):
        log("ja publicado, nada a fazer:", nome)
        return 0
    erros = problemas(meta)
    if erros:
        log("ERRO no meta.json de %s:" % nome)
        for e in erros:
            log("  -", e)
        return 1

    def salvar(**campos):
        meta.update(campos)
        if gravar_meta:
            gravar(pasta, meta)
        elif api.seco:
            log("  (seco) gravaria no meta.json:", json.dumps(campos, ensure_ascii=False))

    no_ar = ja_no_ar(api, meta["caption"])
    if no_ar:
        log("JA ESTAVA NO AR (mesma legenda): media", no_ar.get("id"), "- so marco o meta.json, nao publico de novo")
        salvar(published=True, status="publicado", ig_media=no_ar.get("id"), permalink=no_ar.get("permalink", ""),
               published_at=agora_utc().strftime("%Y-%m-%dT%H:%M:%SZ"), obs="achado ja no ar pela checagem de duplicata")
        return 0

    if conferir_url and not api.seco:
        ok, info = video_acessivel(meta["video_url"])
        if not ok:
            log("ERRO: a URL do video nao abre (%s). Gere o link de novo; nada foi enviado ao Instagram." % info)
            return 1
    exp = expira_em(meta["video_url"])
    if exp:
        log("  link do video vale ate %s UTC" % exp.strftime("%d/%m %H:%M"))

    cid = meta.get("container_id")
    if cid:
        log("retomando container ja criado:", cid)
    else:
        params = {"media_type": "REELS", "video_url": meta["video_url"], "caption": meta["caption"],
                  "share_to_feed": "true" if meta.get("share_to_feed", True) else "false"}
        if isinstance(meta.get("cover_ms"), int):
            params["thumb_offset"] = str(meta["cover_ms"])
        c = api.req("POST", "/%s/media" % IG, params)
        if "id" not in c:
            log("ERRO ao criar o container do Reels:", json.dumps(c)[:500])
            return 1
        cid = c["id"]
        log("container criado:", cid)
        salvar(container_id=cid, status="processando",
               container_em=agora_utc().strftime("%Y-%m-%dT%H:%M:%SZ"))

    status, info = esperar_container(api, cid)
    if status == "PUBLISHED":                          # saiu numa execucao anterior e o meta.json nao subiu
        no_ar = ja_no_ar(api, meta["caption"])
        if no_ar:
            log("o container ja tinha sido publicado: media", no_ar.get("id"), "- so marco o meta.json")
            salvar(published=True, status="publicado", ig_media=no_ar.get("id"), permalink=no_ar.get("permalink", ""),
                   published_at=agora_utc().strftime("%Y-%m-%dT%H:%M:%SZ"))
            return 0
        log("ERRO: container %s consta PUBLISHED mas nao achei a midia na conta; confira no app antes de mexer." % cid)
        return 1
    if status in ("ERROR", "EXPIRED"):
        log("ERRO: a Meta recusou o video (status_code=%s): %s" % (status, info.get("status", "sem detalhe")))
        log("  Confira o mp4 (MP4 H.264 + AAC, vertical 9:16) e a URL; para tentar de novo, apague container_id, status e erro do meta.json.")
        salvar(status="erro_" + status.lower(), erro=str(info.get("status", ""))[:300])
        return 1
    if status == "TEMPO":
        log("ERRO: o video ainda processava depois de ~%d min (ultimo status: %s). O container_id ficou no"
            " meta.json e a proxima execucao retoma dele, sem criar outro." % (ESPERA_MAX_S // 60, info.get("status_code")))
        return 1

    p = api.req("POST", "/%s/media_publish" % IG, {"creation_id": cid})
    if "id" not in p:
        log("ERRO no media_publish:", json.dumps(p)[:500])
        no_ar = ja_no_ar(api, meta["caption"])       # resposta perdida? confere antes de deixar repetir
        if no_ar:
            log("  ...mas o Reels apareceu na conta (media %s). Marcando publicado." % no_ar.get("id"))
            salvar(published=True, status="publicado", ig_media=no_ar.get("id"), permalink=no_ar.get("permalink", ""),
                   published_at=agora_utc().strftime("%Y-%m-%dT%H:%M:%SZ"))
            return 0
        return 1
    mid = p["id"]
    salvar(published=True, status="publicado", ig_media=mid,
           published_at=agora_utc().strftime("%Y-%m-%dT%H:%M:%SZ"))
    link = api.req("GET", "/" + mid, {"fields": "permalink"})
    if link.get("permalink"):
        salvar(permalink=link["permalink"])
    log("PUBLICADO no Instagram:", nome, "media", mid, link.get("permalink", ""))
    return 0


# ---------------------------------------------------------------- linha de comando
def cmd_publicar(a):
    global _AGORA
    if a.agora:
        t = dt.datetime.fromisoformat(a.agora)
        _AGORA = (t if t.tzinfo else t.replace(tzinfo=BRT)).astimezone(dt.timezone.utc)
    agora = agora_utc()
    api = ApiSeca(a.cenario) if a.seco else ApiReal()
    if a.seco:
        log("MODO SECO: respostas simuladas, nenhuma chamada ao Instagram (cenario=%s)" % a.cenario)
    pasta, motivo = escolher(agora)
    if not pasta:
        log("NADA A FAZER:", motivo)
        return 0
    log("Reels da vez:", pasta)
    if a.seco and a.cenario == "ja_no_ar":
        api.no_ar = [ler(pasta).get("caption", "")]     # finge que a conta ja tem esta legenda
    r = publicar(api, pasta, gravar_meta=(not a.seco) or a.gravar)
    if a.seco:
        resumo = []
        for m, p, k in api.chamadas:
            txt = "%s %s %s" % (m, p.replace(IG, "{ig}"), ",".join(k))
            if resumo and resumo[-1][0] == txt:
                resumo[-1][1] += 1
            else:
                resumo.append([txt, 1])
        log("chamadas simuladas:", "; ".join(t + (" (x%d)" % n if n > 1 else "") for t, n in resumo))
    return r


def cmd_checar(a):
    pastas = pastas_da_fila()
    if not pastas:
        log("fila vazia:", FILA)
        return 0
    ruim = 0
    for d in pastas:
        m = ler(d)
        nome = os.path.basename(d)
        if m.get("published"):
            log("OK  ", nome, "publicado", m.get("published_at", ""), m.get("ig_media", ""))
            continue
        e = problemas(m)
        if e:
            ruim += 1
            log("ERRO", nome, "|", " | ".join(e))
            continue
        if str(m.get("status", "")).startswith("erro_"):
            ruim += 1
            log("ERRO", nome, "| a Meta recusou o video:", m.get("erro", ""), "| corrija e apague container_id, status e erro")
            continue
        t = quando(m)
        if agora_utc() - t > dt.timedelta(hours=ATRASO_MAX_H):
            log("AVISO", nome, "atrasado mais de %g h: NAO sai sozinho; mude publicar_em para reagendar" % ATRASO_MAX_H)
        else:
            extra = " (" + m["status"] + ", container " + m.get("container_id", "?") + ")" if m.get("status") else ""
            log("OK  ", nome, "sai a partir de", t.astimezone(BRT).strftime("%d/%m %H:%M"), "BRT" + extra)
    return 1 if ruim else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Reels do camarao pela API do Instagram")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("publicar")
    p.add_argument("--seco", action="store_true", help="simula a API (nao publica nada)")
    p.add_argument("--cenario", default="ok", choices=["ok", "erro", "expira", "demora", "ja_no_ar"])
    p.add_argument("--gravar", action="store_true", help="no modo seco, grava o meta.json (so para teste)")
    p.add_argument("--agora", help="finge outra hora (BRT), so para teste: 2026-11-20T19:00")
    sub.add_parser("checar")
    args = ap.parse_args()
    sys.exit({"publicar": cmd_publicar, "checar": cmd_checar}[args.cmd](args))
