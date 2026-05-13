#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))

def html_files():
    return sorted(ROOT.glob("*.html"))

def check():
    errors = []
    expected = CONFIG["pages"]
    for page in expected:
        path = ROOT / page["file"]
        if not path.exists():
            errors.append(f"missing page {page['file']}")
            continue
        text = path.read_text(encoding="utf-8")
        sections = re.findall(r"<section\b[^>]*data-section=\"([^\"]+)\"", text)
        core_sections = sections
        if core_sections != page["sections"]:
            errors.append(f"section mismatch in {page['file']}: {core_sections}")
        if len(core_sections) != 10:
            errors.append(f"wrong section count in {page['file']}")
        if len(set(core_sections)) != len(core_sections):
            errors.append(f"duplicate sections in {page['file']}")
        if not re.search(r"<h1\b", text):
            errors.append(f"missing h1 in {page['file']}")
    for utility in ["privacy.html","cookies.html","terms.html","accessibility.html","sitemap.html","thanks.html","404.html"]:
        if not (ROOT / utility).exists():
            errors.append(f"missing utility {utility}")
    for partial in ["header.html","mobile-menu.html","footer.html","hero.html","cta.html","form.html","cards.html","resources.html","pricing.html","faq.html","cookie.html","legal.html"]:
        if not (ROOT / "partials" / partial).exists():
            errors.append(f"missing partial {partial}")
    if errors:
        print("\n".join(errors))
        return 1
    print("Structural check passed.")
    return 0

def sitemap():
    urls = []
    for path in html_files():
        name = "" if path.name == "index.html" else path.name
        urls.append(CONFIG["baseUrl"].rstrip("/") + "/" + name)
    body = "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '\n</urlset>\n', encoding="utf-8")
    print("sitemap.xml updated.")
    return 0

def audit():
    tool = ROOT.parents[1] / "premium-static-site-system" / "tools" / "static_site_quality.py"
    if not tool.exists():
        print("static_site_quality.py not found; run from portfolio checkout.")
        return 1
    return subprocess.call([sys.executable, str(tool), "audit", str(ROOT), "--base-url", CONFIG["baseUrl"], "--out", str(ROOT / "quality-report.json"), "--report-md", str(ROOT / "quality-report.md"), "--fail-on", "critical"])

def seo(write=False):
    tool = ROOT.parents[1] / "premium-static-site-system" / "tools" / "static_site_quality.py"
    args = [sys.executable, str(tool), "fix", str(ROOT), "--base-url", CONFIG["baseUrl"], "--site-name", CONFIG["siteName"]]
    if write:
        args.append("--write")
    return subprocess.call(args)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["check","sitemap","audit","seo","all"])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.command == "check": return check()
    if args.command == "sitemap": return sitemap()
    if args.command == "audit": return audit()
    if args.command == "seo": return seo(args.write)
    status = sitemap() or check() or seo(True) or audit()
    return status

if __name__ == "__main__":
    raise SystemExit(main())
