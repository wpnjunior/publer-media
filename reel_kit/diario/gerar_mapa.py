"""Gera mapa_mundo.json (contornos dos países em SVG) para o formato Mapeamento.

Roda uma vez só (o json já fica no repositório). Fonte: world-atlas 2.0.2, Natural Earth 1:50m
(domínio público). Uso: python gerar_mapa.py countries-50m.json mapa_mundo.json
Projeção Miller, largura 2000; latitude cortada em -58..84 (sem Antártida).
"""
import json
import math
import sys
from pathlib import Path

W = 2000.0
# nomes em português e apelidos que o plano pode usar -> nome do Natural Earth
PT = {
    "brasil": "Brazil", "eua": "United States of America", "estados unidos": "United States of America",
    "usa": "United States of America", "canada": "Canada", "mexico": "Mexico", "argentina": "Argentina",
    "chile": "Chile", "colombia": "Colombia", "peru": "Peru", "venezuela": "Venezuela", "uruguai": "Uruguay",
    "paraguai": "Paraguay", "bolivia": "Bolivia", "equador": "Ecuador", "cuba": "Cuba",
    "reino unido": "United Kingdom", "inglaterra": "United Kingdom", "escocia": "United Kingdom",
    "irlanda": "Ireland", "franca": "France", "alemanha": "Germany", "italia": "Italy", "espanha": "Spain",
    "portugal": "Portugal", "holanda": "Netherlands", "paises baixos": "Netherlands", "belgica": "Belgium",
    "suica": "Switzerland", "austria": "Austria", "suecia": "Sweden", "noruega": "Norway",
    "dinamarca": "Denmark", "finlandia": "Finland", "islandia": "Iceland", "polonia": "Poland",
    "grecia": "Greece", "turquia": "Turkey", "russia": "Russia", "ucrania": "Ukraine", "hungria": "Hungary",
    "republica tcheca": "Czechia", "tchequia": "Czechia", "romenia": "Romania", "israel": "Israel",
    "ira": "Iran", "iraque": "Iraq", "arabia saudita": "Saudi Arabia", "egito": "Egypt",
    "africa do sul": "South Africa", "nigeria": "Nigeria", "quenia": "Kenya", "etiopia": "Ethiopia",
    "marrocos": "Morocco", "angola": "Angola", "mocambique": "Mozambique", "congo": "Dem. Rep. Congo",
    "china": "China", "japao": "Japan", "coreia do sul": "South Korea", "coreia": "South Korea",
    "india": "India", "paquistao": "Pakistan", "bangladesh": "Bangladesh", "indonesia": "Indonesia",
    "tailandia": "Thailand", "vietna": "Vietnam", "filipinas": "Philippines", "taiwan": "Taiwan",
    "australia": "Australia", "nova zelandia": "New Zealand", "singapura": "Singapore",
}
GRUPOS = {
    "europa": ["Portugal", "Spain", "France", "United Kingdom", "Ireland", "Belgium", "Netherlands", "Germany",
               "Denmark", "Norway", "Sweden", "Finland", "Poland", "Czechia", "Austria", "Switzerland", "Italy",
               "Slovenia", "Croatia", "Hungary", "Slovakia", "Greece", "Romania", "Bulgaria", "Serbia",
               "Bosnia and Herz.", "Albania", "Macedonia", "Montenegro", "Kosovo", "Estonia", "Latvia",
               "Lithuania", "Luxembourg", "Iceland"],
    "escandinavia": ["Norway", "Sweden", "Denmark", "Finland"],
    "america latina": ["Mexico", "Guatemala", "Honduras", "El Salvador", "Nicaragua", "Costa Rica", "Panama",
                       "Colombia", "Venezuela", "Ecuador", "Peru", "Bolivia", "Brazil", "Paraguay", "Uruguay",
                       "Argentina", "Chile", "Cuba", "Dominican Rep."],
}


def proj(lon: float, lat: float) -> tuple[float, float]:
    lat = max(-58.0, min(84.0, lat))
    x = (lon + 180.0) / 360.0 * W
    y = 1.25 * math.log(math.tan(math.pi / 4 + 0.4 * math.radians(lat)))
    return x, y


def main() -> None:
    topo = json.loads(Path(sys.argv[1]).read_text())
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)
    _, ytop = proj(0, 84)
    k = W / (2 * math.pi)  # escala y igual à de x
    def P(lon, lat):
        x, y = proj(lon, lat)
        return x, (ytop - y) * k

    def ring(idx: list[int]) -> list[tuple[float, float]]:
        out = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(a if not out else a[1:])
        return out

    paises = {}
    for g in topo["objects"]["countries"]["geometries"]:
        nome = g["properties"]["name"]
        if nome == "Antarctica" or g["type"] not in ("Polygon", "MultiPolygon"):
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        d = []
        for poly in polys:
            for r in poly:
                pts = [P(lon, lat) for lon, lat in ring(r)]
                # evita a costura do antimeridiano (Rússia, Fiji): quebra quando salta meio mapa
                seg = []
                last = None
                for x, y in pts:
                    q = (round(x), round(y))
                    if last and abs(q[0] - last[0]) > W / 2:
                        if len(seg) > 2: d.append(seg)
                        seg = []
                    if q != last:
                        seg.append(q)
                    last = q
                if len(seg) > 2:
                    d.append(seg)
        if not d:
            continue
        path = "".join("M" + "L".join(f"{x} {y}" for x, y in s) + "Z" for s in d)
        xs = [x for s in d for x, _ in s]; ys = [y for s in d for _, y in s]
        paises[nome] = {"d": path, "bbox": [min(xs), min(ys), max(xs), max(ys)]}
    altura = round(P(0, -58)[1])
    Path(sys.argv[2]).write_text(json.dumps({"largura": int(W), "altura": altura, "paises": paises,
                                             "apelidos": PT, "grupos": GRUPOS}, ensure_ascii=False, separators=(",", ":")))
    print(len(paises), "países, altura", altura)


if __name__ == "__main__":
    main()
