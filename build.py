#!/usr/bin/env python3
"""Build the static site from the markdown sources.

    python3 build.py                 # site for Vercel: index.html, rapport.html, en/
    python3 build.py --artifact DIR  # self-contained preview pages (CSS and JS inlined) in DIR

Sources:  content/summary.{fr,en}.md   short synthesis pages (with {{diagram:name}} markers)
          content/report.{fr,en}.md    full sourced report

Requires: python-markdown (pip install markdown).
"""
import html
import pathlib
import re
import sys

import markdown

from diagrams import MARKERS, figure

ROOT = pathlib.Path(__file__).parent
VERSION = "v0.2"
SITE_NAME = "EKO Matrice Follow"

UI = {
    "fr": dict(
        date="12 octobre 2026", eyebrow="Dossier R&D", internal="Document interne",
        nav_summary="Synthèse", nav_report="Rapport complet", toc="Sommaire",
        theme="Thème clair ou sombre", print="Imprimer ou enregistrer en PDF", print_short="PDF",
        summary_href="index.html", report_href="rapport.html",
        nav_proposal="Proposition", proposal_href="proposition.html",
        footer="Kreativ Labs · EKO · Document interne de R&D, non destiné à la diffusion publique.",
        sources="Toutes les sources sont en lien dans le rapport complet. Prix relevés le 11 octobre 2026.",
        other="English", other_code="EN",
        report_lede="Le rapport complet : chaque affirmation garde sa source en lien, et ce qui n'a pas pu être confirmé est marqué comme tel.",
        abstract="Résumé",
    ),
    "en": dict(
        date="12 October 2026", eyebrow="R&D dossier", internal="Internal document",
        nav_summary="Summary", nav_report="Full report", toc="Contents",
        theme="Light or dark theme", print="Print or save as PDF", print_short="PDF",
        summary_href="index.html", report_href="report.html",
        nav_proposal="Proposal", proposal_href="proposal.html",
        footer="Kreativ Labs · EKO · Internal R&D document, not intended for public distribution.",
        sources="All sources are linked in the full report. Prices seen on 11 October 2026.",
        other="Français", other_code="FR",
        report_lede="The full report: every statement keeps its source as a link, and whatever could not be confirmed is marked as such.",
        abstract="Abstract",
    ),
}

PAGES = [
    dict(lang="fr", kind="summary", src="content/summary.fr.md", out="index.html", alt="en/index.html"),
    dict(lang="fr", kind="report", src="content/report.fr.md", out="rapport.html", alt="en/report.html"),
    dict(lang="fr", kind="proposal", src="content/proposal.fr.md", out="proposition.html", alt="en/proposal.html"),
    dict(lang="en", kind="summary", src="content/summary.en.md", out="en/index.html", alt="index.html"),
    dict(lang="en", kind="proposal", src="content/proposal.en.md", out="en/proposal.html", alt="proposition.html"),
    dict(lang="en", kind="report", src="content/report.en.md", out="en/report.html", alt="rapport.html"),
]

CITE = re.compile(r'\((<a href="[^"]+">[^<]+</a>(?:\s*;\s*<a href="[^"]+">[^<]+</a>)*)\)')
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700'
    '&amp;family=Barlow+Condensed:wght@600;700&amp;display=swap">'
)
THEME_INIT = "<script>try{var t=localStorage.getItem('eko-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>"
THEME_ICON = (
    '<svg aria-hidden="true" width="16" height="16" viewBox="0 0 16 16">'
    '<circle cx="8" cy="8" r="6.25" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    '<path d="M8 1.75a6.25 6.25 0 0 1 0 12.5z" fill="currentColor"/></svg>'
)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def render(md_text, lang):
    body = markdown.Markdown(extensions=["tables", "sane_lists"]).convert(md_text)

    # Title and lede: first <h1> and the paragraph that follows it.
    m = re.match(r"\s*<h1>(.*?)</h1>\s*<p>(.*?)</p>", body, re.S)
    title, lede = m.group(1), m.group(2)
    body = body[m.end():]

    # Diagrams.
    body = re.sub(r"<p>\{\{diagram:(\w+)\}\}</p>", lambda mm: figure(mm.group(1), lang), body)

    # Heading ids and table of contents.
    toc, counter = [], {"n": 0}

    def h2(mm):
        text = mm.group(1)
        num = re.match(r"(\d+)\.\s", strip_tags(text))
        counter["n"] += 1
        hid = f"s{num.group(1)}" if num else f"p{counter['n']}"
        toc.append((2, hid, strip_tags(text)))
        return f'<h2 id="{hid}">{text}</h2>'

    def h3(mm):
        text = mm.group(1)
        num = re.match(r"(\d+)\.(\d+)\s", strip_tags(text))
        if not num:
            return mm.group(0)
        hid = f"s{num.group(1)}-{num.group(2)}"
        toc.append((3, hid, strip_tags(text)))
        return f'<h3 id="{hid}">{text}</h3>'

    parts = re.split(r"(<h[23]>.*?</h[23]>)", body, flags=re.S)
    for i, part in enumerate(parts):
        if part.startswith("<h2>"):
            parts[i] = re.sub(r"<h2>(.*?)</h2>", h2, part, flags=re.S)
        elif part.startswith("<h3>"):
            parts[i] = re.sub(r"<h3>(.*?)</h3>", h3, part, flags=re.S)
    body = "".join(parts)

    # Compact parenthetical source groups, wrap tables, open external links in a new tab.
    lede = CITE.sub(r'<span class="cite">\1</span>', lede)
    body = CITE.sub(r'<span class="cite">\1</span>', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

    def ext(s):
        return s.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')

    return title, ext(lede), ext(body), toc


def toc_html(toc):
    out = []
    for level, hid, text in toc:
        text = re.sub(r"\s:\s.*$", "", text)  # keep the short half of "4.1 Title : subtitle"
        out.append(f'<a class="l{level}" href="#{hid}">{html.escape(text)}</a>')
    return "\n    ".join(out)


def page(p, artifact=False):
    """Return the HTML of one page.

    artifact=True inlines the stylesheet and script and drops the print button, so the
    pages can be published as a self-contained preview. The French summary is then
    emitted without <html>, <head> or <body>, as the preview host supplies them.
    """
    ui = UI[p["lang"]]
    base = "../" if "/" in p["out"] else ""
    title, lede, body, toc = render((ROOT / p["src"]).read_text(encoding="utf-8"), p["lang"])
    # Path to the same page in the other language, relative to this page.
    alt = ("../" + p["alt"]) if base else p["alt"]
    if p["kind"] == "report":
        body = f'<section class="abstract"><p class="abstract-title">{ui["abstract"]}</p><p>{lede}</p></section>\n' + body
        lede = ui["report_lede"]

    cur = ' aria-current="page"'
    nav = (
        '<a href="%s"%s>%s</a>' % (ui["summary_href"], cur if p["kind"] == "summary" else "", ui["nav_summary"])
        + '<a href="%s"%s>%s</a>' % (ui["proposal_href"], cur if p["kind"] == "proposal" else "", ui["nav_proposal"])
        + '<a href="%s"%s>%s</a>' % (ui["report_href"], cur if p["kind"] == "report" else "", ui["nav_report"])
    )
    print_btn = "" if artifact else (
        f'\n    <button class="tool" id="print" type="button" title="{ui["print"]}" aria-label="{ui["print"]}">{ui["print_short"]}</button>'
    )
    if artifact:
        css = f"<style>\n{(ROOT / 'assets/style.css').read_text(encoding='utf-8')}</style>"
        js = f"<script>\n{(ROOT / 'assets/site.js').read_text(encoding='utf-8')}</script>"
    else:
        css = f'<link rel="stylesheet" href="{base}assets/style.css">'
        js = f'<script src="{base}assets/site.js"></script>'

    page_title = SITE_NAME if p["out"] == "index.html" else f"{strip_tags(title)} · {SITE_NAME}"
    head = f"""<title>{html.escape(page_title)}</title>
<meta name="robots" content="noindex, nofollow">
{FONTS}
{css}
{THEME_INIT}"""
    content = f"""{MARKERS}
<div class="page {p['kind']}">
<header class="top">
  <a class="brand" href="{ui['summary_href']}"><span class="brand-eko">EKO</span><span class="brand-sub">Kreativ Labs</span></a>
  <nav class="pages">{nav}</nav>
  <div class="tools">
    <a class="tool lang" href="{alt}" hreflang="{ui['other_code'].lower()}" title="{ui['other']}">{ui['other_code']}</a>
    <button class="tool" id="theme" type="button" title="{ui['theme']}" aria-label="{ui['theme']}">{THEME_ICON}</button>{print_btn}
  </div>
</header>
<section class="hero">
  <div class="hero-in">
    <p class="eyebrow">{ui['eyebrow']} · {VERSION} · {ui['date']} · {ui['internal']}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
<div class="layout">
  <nav class="toc" aria-label="{ui['toc']}">
    <p class="toc-title">{ui['toc']}</p>
    {toc_html(toc)}
  </nav>
  <main>
{body}
    <p class="note">{ui['sources']}</p>
  </main>
</div>
<footer class="foot">{ui['footer']} · info@kreativlabs.tv</footer>
</div>
{js}
"""
    if artifact and p["out"] == "index.html":
        return head + "\n" + content
    # The public site is light by default; the preview pages follow the viewer's system theme.
    theme_attr = "" if artifact else ' data-theme="light"'
    return f"""<!doctype html>
<html lang="{p['lang']}"{theme_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head}
</head>
<body>
{content}</body>
</html>
"""


def main():
    artifact = "--artifact" in sys.argv
    out_root = pathlib.Path(sys.argv[sys.argv.index("--artifact") + 1]) if artifact else ROOT
    for p in PAGES:
        if not (ROOT / p["src"]).exists():
            print(f"skip  {p['out']}  (missing {p['src']})")
            continue
        out = out_root / p["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(p, artifact), encoding="utf-8")
        print(f"built {out.relative_to(out_root)}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
