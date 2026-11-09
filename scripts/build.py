#!/usr/bin/env python3
"""Genera index.html a partir de src/template.html y data/frases.json.

Uso:  python3 scripts/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
data = (ROOT / "data" / "frases.json").read_text(encoding="utf-8").replace("</", "<\\/")

page = template.replace("__DATA__", data)
head, _, rest = page.partition("<style>")
html = (
    '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + head + "<style>" + rest.replace("</style>", "</style>\n</head>\n<body>", 1)
    + "\n</body>\n</html>\n"
)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"index.html generado ({len(html)//1024} KB)")
