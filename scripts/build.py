#!/usr/bin/env python3
"""Genera el sitio completo a partir de src/template.html y data/frases.json.

Salida:
  index.html              Página principal (lector con filtros), con la lista inicial ya escrita en el HTML
  frase/<id>/index.html   Una página estática por frase (608)
  tema/<slug>/index.html  Una página por tema (10)
  sitemap.xml, robots.txt, 404.html

Uso:  python3 scripts/build.py
"""
import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://gzacur.github.io/smg-quotes-web/"
TODAY = date.today().isoformat()
GTM_ID = "GTM-KQHR3TV3"
PAGE = 40  # tarjetas que se muestran al abrir la página principal

THEMES = {  # código: (nombre corto, nombre completo, slug, color del punto)
    "VD": ("Voluntad de Dios", "Voluntad de Dios y disponibilidad", "voluntad-de-dios", "#8fb07a"),
    "OB": ("Obediencia y humildad", "Obediencia y humildad", "obediencia-y-humildad", "#c9a77c"),
    "AM": ("Amor de Dios", "Amor de Dios y Sagrado Corazón", "amor-de-dios", "#d48a8f"),
    "CO": ("Confianza", "Confianza y abandono en Dios", "confianza", "#7fa7c9"),
    "OR": ("Oración y vida interior", "Oración, vida interior y santidad", "oracion-y-vida-interior", "#a998cf"),
    "CR": ("Cruz y paciencia", "Cruz, sufrimiento y paciencia", "cruz-y-paciencia", "#b98468"),
    "AN": ("Ánimo y alegría", "Ánimo, alegría y paz interior", "animo-y-alegria", "#e0b25e"),
    "CF": ("Caridad fraterna", "Caridad fraterna y vida comunitaria", "caridad-fraterna", "#7fbfab"),
    "GO": ("Gobierno y acompañamiento", "Gobierno y acompañamiento", "gobierno-y-acompanamiento", "#8a94a6"),
    "MI": ("Misión y educación", "Misión, celo apostólico y educación", "mision-y-educacion", "#a3a95f"),
}
ABOUT = {  # para usar dentro de una oración: «Frases sobre …»
    "VD": "la voluntad de Dios y la disponibilidad", "OB": "la obediencia y la humildad",
    "AM": "el amor de Dios y el Sagrado Corazón", "CO": "la confianza y el abandono en Dios",
    "OR": "la oración, la vida interior y la santidad", "CR": "la cruz, el sufrimiento y la paciencia",
    "AN": "el ánimo, la alegría y la paz interior", "CF": "la caridad fraterna y la vida comunitaria",
    "GO": "el gobierno y el acompañamiento", "MI": "la misión, el celo apostólico y la educación",
}
TOMO = {"I": "Tomo I", "II": "Tomo II", "III": "Tomo III"}

PERSON = {
    "@type": "Person",
    "@id": BASE + "#san-miguel-garicoits",
    "name": "San Miguel Garicoïts",
    "alternateName": ["Michel Garicoïts", "Miguel Garicoits", "Santo de la Disponibilidad"],
    "birthDate": "1797-04-15",
    "deathDate": "1863-05-14",
    "description": "Sacerdote vasco francés, fundador de la Congregación del Sagrado Corazón de Jesús de Betharram.",
    "sameAs": [
        "https://es.wikipedia.org/wiki/Miguel_Garicoits",
        "https://en.wikipedia.org/wiki/Michael_Garicoits",
    ],
}
SOURCE = {
    "@type": "Book",
    "name": "Correspondencia de San Miguel Garicoïts",
    "editor": {"@type": "Person", "name": "Pierre Miéyaa"},
    "translator": [{"@type": "Person", "name": "Miguel Martínez"}, {"@type": "Person", "name": "Angelo Recalcati"}],
    "inLanguage": "es",
}

e = lambda s: html.escape(str(s), quote=True)


def cut(text, n):
    text = " ".join(str(text).split())
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def jsonld(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def gtm_snippet():
    return f"""<!-- Google Tag Manager -->
<script async src="https://www.googletagmanager.com/gtm.js?id={GTM_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  dataLayer.push({{'gtm.start': new Date().getTime(), event: 'gtm.js'}});
</script>
<!-- Fin Google Tag Manager -->"""


# ---------------------------------------------------------------- estilos de las páginas estáticas
SUB_CSS = """
:root{--canvas:#eeeee9;--card:#fff;--stone:#e3e4dc;--ink:#1f2421;--muted:#62675f;--line:#dcddd5;--sage:#e1ebd3;--sage-ink:#3c5a2a;
--serif:"Fraunces",Georgia,"Times New Roman",serif;--sans:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
@media (prefers-color-scheme:dark){:root{--canvas:#191b19;--card:#222522;--stone:#2b2f2b;--ink:#e7e9e3;--muted:#a3a89f;--line:#333733;--sage:#2c3a24;--sage-ink:#cfe3b8;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit}:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.wrap{max-width:880px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-block:20px 8px}
.home{display:inline-flex;align-items:center;gap:10px;font-weight:600;text-decoration:none}
.mark{width:28px;height:28px;border-radius:50%;background:var(--sage);color:var(--sage-ink);display:grid;place-items:center;font-family:var(--serif);font-size:18px}
.crumbs{font-size:13px;color:var(--muted);padding-block:8px 16px}.crumbs a{color:var(--muted)}
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}.crumbs li+li::before{content:"›";margin-right:6px}
.card{background:var(--card);border-radius:16px;padding:clamp(20px,4vw,40px);display:grid;gap:20px}
.theme{justify-self:start;display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;background:var(--sage);color:var(--sage-ink);border-radius:999px;padding:5px 12px 5px 10px;text-decoration:none}
.dot{width:8px;height:8px;border-radius:50%;background:var(--c)}
h1.q{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(26px,4vw,40px);line-height:1.25;text-wrap:pretty}
.label{font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:600;color:var(--muted);margin:0}
dl{margin:0;border-top:1px solid var(--line)}dl div{display:grid;grid-template-columns:120px minmax(0,1fr);gap:12px;padding-block:10px;border-bottom:1px solid var(--line)}dd{margin:0}
.ctx{background:var(--canvas);border-radius:12px;padding:16px}.ctx p{margin:6px 0 0}
.acts{display:flex;flex-wrap:wrap;gap:8px}
.btn{display:inline-flex;align-items:center;min-height:44px;border-radius:999px;padding:10px 18px;font-size:14px;font-weight:600;text-decoration:none}
.btn.primary{background:var(--ink);color:var(--card)}.btn.secondary{background:var(--stone)}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding-block:20px}
.pager a{background:var(--card);border-radius:12px;padding:14px 16px;text-decoration:none;display:grid;gap:2px;min-width:0}
.pager a.next{text-align:right}.pager span{font-family:var(--serif);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.intro{color:var(--muted);margin:8px 0 20px;max-width:65ch}
h1.t{font-family:var(--serif);font-weight:400;font-size:clamp(28px,4vw,40px);line-height:1.2;margin:0}
.list{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.list a{display:grid;gap:6px;background:var(--card);border-radius:16px;padding:18px 20px;text-decoration:none}
.list a:hover{outline:2px solid var(--line)}.list q{font-family:var(--serif);font-size:18px;line-height:1.45;quotes:"«" "»"}
.list small{color:var(--muted);font-size:13px}
footer{padding-block:32px 48px;font-size:13px;color:var(--muted)}footer ul{list-style:none;padding:0;margin:8px 0 20px;display:flex;flex-wrap:wrap;gap:6px 18px}
footer a{color:var(--ink)}
@media (max-width:560px){dl div{grid-template-columns:1fr;gap:2px}.pager{grid-template-columns:1fr}.pager a.next{text-align:left}}
"""


def sub_page(*, title, description, canonical, root, body, ld, og_type="article"):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
{gtm_snippet()}
<meta name="description" content="{e(description)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Frases de San Miguel Garicoïts">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{BASE}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{BASE}assets/og-image.png">
<meta name="theme-color" content="#eeeee9">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;1,9..144,400&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{root}assets/page.css">
<script type="application/ld+json">{jsonld(ld)}</script>
</head>
<body>
<header class="wrap top"><a class="home" href="{root}"><span class="mark" aria-hidden="true">«</span>Frases de San Miguel Garicoïts</a></header>
{body}
<footer class="wrap">
  <p class="label">Explorar por tema</p>
  <ul>{''.join(f'<li><a href="{root}tema/{t[2]}/">{e(t[1])}</a></li>' for t in THEMES.values())}</ul>
  <p>Fuente: <i>Correspondencia de San Miguel Garicoïts</i>, edición del P. Pierre Miéyaa, scj; traducción del P. Miguel Martínez y del P. Angelo Recalcati, scj. Las frases son literales; «…» indica un recorte.</p>
</footer>
</body>
</html>
"""


def crumbs(items, root):
    lis = []
    for name, href in items:
        lis.append(f'<li><a href="{href}">{e(name)}</a></li>' if href else f'<li aria-current="page">{e(name)}</li>')
    return f'<nav class="crumbs wrap" aria-label="Ruta de navegación"><ol>{"".join(lis)}</ol></nav>'


def crumbs_ld(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, **({"item": u} if u else {})}
            for i, (n, u) in enumerate(items)
        ],
    }


def quote_url(r):
    return f"{BASE}frase/{r['id']}/"


def theme_url(k):
    return f"{BASE}tema/{THEMES[k][2]}/"


def build_quote_page(r, prev, nxt):
    short, full, slug, color = THEMES[r["k"]]
    root = "../../"
    title = f"«{cut(r['f'], 70)}» — San Miguel Garicoïts"
    desc = cut(f"Frase de San Miguel Garicoïts (carta {r['c']}, {TOMO[r['t']]}{', ' + r['y'] if r['y'] else ''}). {r['x']}", 158)
    facts = [("Carta", f"Carta {r['c']} · {TOMO[r['t']]}"), ("Destinatario", r["d"]), ("Año", r["y"] or "Sin fecha en la carta"), ("Tema", full)]
    pager = '<nav class="pager wrap" aria-label="Otras frases">'
    pager += (f'<a class="prev" href="{root}frase/{prev["id"]}/" rel="prev"><small class="label">← Anterior</small><span>{e(prev["f"])}</span></a>' if prev else "<span></span>")
    pager += (f'<a class="next" href="{root}frase/{nxt["id"]}/" rel="next"><small class="label">Siguiente →</small><span>{e(nxt["f"])}</span></a>' if nxt else "<span></span>")
    pager += "</nav>"
    trail = [("Inicio", root), (short, f"{root}tema/{slug}/"), (f"Carta {r['c']}", None)]
    body = f"""{crumbs(trail, root)}
<main class="wrap">
  <article class="card">
    <a class="theme" href="{root}tema/{slug}/"><span class="dot" style="--c:{color}"></span>{e(full)}</a>
    <h1 class="q">«{e(r['f'])}»</h1>
    <dl>{''.join(f'<div><dt class="label">{a}</dt><dd>{e(b)}</dd></div>' for a, b in facts)}</dl>
    <section class="ctx" aria-labelledby="ctx-h"><h2 class="label" id="ctx-h">Contexto</h2><p>{e(r['x'] or 'Sin contexto disponible.')}</p></section>
    <div class="acts">
      <a class="btn primary" href="{root}#n-{r['id']}">Abrir en el lector de frases</a>
      <a class="btn secondary" href="{root}tema/{slug}/">Más frases sobre este tema</a>
    </div>
  </article>
</main>
{pager}"""
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Quotation",
                "@id": quote_url(r) + "#frase",
                "text": r["f"],
                "url": quote_url(r),
                "inLanguage": "es",
                "creator": {"@id": PERSON["@id"], "@type": "Person", "name": PERSON["name"]},
                "about": full,
                "description": r["x"],
                "isPartOf": {**SOURCE, "position": f"Carta {r['c']}, {TOMO[r['t']]}"},
                **({"dateCreated": r["y"][:4]} if r["y"][:4].isdigit() else {}),
            },
            crumbs_ld([("Inicio", BASE), (short, theme_url(r["k"])), (f"Carta {r['c']}", None)]),
        ],
    }
    return sub_page(title=title, description=desc, canonical=quote_url(r), root=root, body=body, ld=ld)


def build_theme_page(k, rows):
    short, full, slug, color = THEMES[k]
    root = "../../"
    title = f"{full}: {len(rows)} frases de San Miguel Garicoïts"
    desc = cut(f"{len(rows)} frases de San Miguel Garicoïts sobre {ABOUT[k]}, tomadas de sus cartas, con el destinatario, el año y el contexto de cada una. «{rows[0]['f']}»", 158)
    items = "".join(
        f'<li><a href="{root}frase/{r["id"]}/"><q>{e(r["f"])}</q><small>Carta {e(r["c"])}{" · " + e(r["y"]) if r["y"] else ""} · {e(r["d"])}</small></a></li>'
        for r in rows
    )
    body = f"""{crumbs([("Inicio", root), (full, None)], root)}
<main class="wrap">
  <h1 class="t">Frases sobre {e(ABOUT[k])}</h1>
  <p class="intro">{len(rows)} frases de San Miguel Garicoïts sobre este tema, en el orden de sus cartas. Toque una para leer a quién escribía y por qué, o <a href="{root}">abra el lector</a> para filtrar y buscar.</p>
  <ol class="list">{items}</ol>
</main>"""
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": theme_url(k),
                "name": f"Frases sobre {ABOUT[k]}",
                "description": desc,
                "inLanguage": "es",
                "about": {"@id": PERSON["@id"]},
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(rows),
                    "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": quote_url(r)} for i, r in enumerate(rows)],
                },
            },
            crumbs_ld([("Inicio", BASE), (full, None)]),
        ],
    }
    return sub_page(title=title, description=desc, canonical=theme_url(k), root=root, body=body, ld=ld, og_type="website")


def card_html(r, selected):
    short, _, _, color = THEMES[r["k"]]
    return (
        f'<li class="card"><button class="cardbtn" type="button" data-id="{r["id"]}" aria-current="{str(selected).lower()}">'
        f'<span class="q">{e(r["f"])}</span>'
        f'<span class="meta"><span class="t"><span class="dot" style="--c:{color}"></span>{e(short)}</span>'
        f'<span>Carta {e(r["c"])}{" · " + e(r["y"]) if r["y"] else ""}</span></span></button></li>'
    )


def build_index(data):
    template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
    first = data[0]
    _, full, _, color = THEMES[first["k"]]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": BASE + "#sitio",
                "url": BASE,
                "name": "Frases de San Miguel Garicoïts",
                "inLanguage": "es",
                "about": {"@id": PERSON["@id"]},
            },
            PERSON,
            {
                "@type": "CollectionPage",
                "@id": BASE + "#coleccion",
                "url": BASE,
                "name": "Frases de San Miguel Garicoïts",
                "description": f"{len(data)} frases breves de la correspondencia de San Miguel Garicoïts, con su contexto.",
                "isPartOf": {"@id": BASE + "#sitio"},
                "isBasedOn": SOURCE,
                "hasPart": [{"@type": "CollectionPage", "name": t[1], "url": f"{BASE}tema/{t[2]}/"} for t in THEMES.values()],
            },
        ],
    }
    page = template.replace("__JSONLD__", jsonld(ld))
    page = page.replace("__LIST__", "".join(card_html(r, i == 0) for i, r in enumerate(data[:PAGE])))
    page = page.replace("__THEMES__", "".join(f'<li><a href="tema/{t[2]}/">{e(t[1])}</a></li>' for t in THEMES.values()))
    # Detalle inicial ya escrito (la primera frase), para buscadores y para quien no tenga JavaScript
    page = page.replace('<span class="theme" id="d-theme"></span>', f'<span class="theme" id="d-theme"><span class="dot" style="--c:{color}"></span>{e(full)}</span>')
    page = page.replace('<blockquote class="bigq" id="d-quote"></blockquote>', f'<blockquote class="bigq" id="d-quote">«{e(first["f"])}»</blockquote>')
    page = page.replace('<dd id="d-carta"></dd>', f'<dd id="d-carta">Carta {e(first["c"])} · {TOMO[first["t"]]}</dd>')
    page = page.replace('<dd id="d-dest"></dd>', f'<dd id="d-dest">{e(first["d"])}</dd>')
    page = page.replace('<dd id="d-anio"></dd>', f'<dd id="d-anio">{e(first["y"] or "Sin fecha en la carta")}</dd>')
    page = page.replace('<p id="d-ctx"></p>', f'<p id="d-ctx">{e(first["x"])}</p>')
    page = page.replace('href="frase/">Ver la página', f'href="frase/{first["id"]}/">Ver la página')
    page = page.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    head, _, rest = page.partition("<style>")
    return (
        '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "<style>" + rest.replace("</style>", "</style>\n</head>\n<body>", 1)
        + "\n</body>\n</html>\n"
    )


def build_404():
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página no encontrada · Frases de San Miguel Garicoïts</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/smg-quotes-web/assets/favicon.svg" type="image/svg+xml">
<style>{SUB_CSS} main{{padding-block:64px}}</style></head>
<body><main class="wrap"><div class="card">
<h1 class="t">No encontramos esta página</h1>
<p>Puede que el enlace esté mal escrito o que la frase haya cambiado de dirección.</p>
<div class="acts"><a class="btn primary" href="/smg-quotes-web/">Ir a todas las frases</a></div>
</div></main></body></html>
"""


def main():
    data = json.loads((ROOT / "data" / "frases.json").read_text(encoding="utf-8"))

    (ROOT / "index.html").write_text(build_index(data), encoding="utf-8")
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "page.css").write_text(SUB_CSS.strip() + "\n", encoding="utf-8")

    for d in ("frase", "tema"):
        shutil.rmtree(ROOT / d, ignore_errors=True)
    for i, r in enumerate(data):
        out = ROOT / "frase" / str(r["id"])
        out.mkdir(parents=True, exist_ok=True)
        prev = data[i - 1] if i > 0 else None
        nxt = data[i + 1] if i < len(data) - 1 else None
        (out / "index.html").write_text(build_quote_page(r, prev, nxt), encoding="utf-8")
    for k, (_, _, slug, _) in THEMES.items():
        out = ROOT / "tema" / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(build_theme_page(k, [r for r in data if r["k"] == k]), encoding="utf-8")

    urls = [(BASE, "1.0", "weekly")]
    urls += [(theme_url(k), "0.8", "monthly") for k in THEMES]
    urls += [(quote_url(r), "0.6", "yearly") for r in data]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>" for u, p, c in urls]
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    (ROOT / "404.html").write_text(build_404(), encoding="utf-8")

    print(f"index.html + {len(data)} páginas de frase + {len(THEMES)} páginas de tema + sitemap ({len(urls)} URLs)")


if __name__ == "__main__":
    main()
