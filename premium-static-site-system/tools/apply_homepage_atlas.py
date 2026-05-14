#!/usr/bin/env python3
"""Apply the 50-site homepage flow cleanup pass to the editable static demos."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = ROOT / "demo-sites"
SYSTEM_DOCS = ROOT / "premium-static-site-system" / "docs"
DEMO_DOCS = DEMO_ROOT / "docs"

REQUIRED_PACK_FILES = [
    "docs/inspiration-audit.md",
    "docs/design-extraction.md",
    "docs/theme-direction.md",
    "docs/theme-guide.md",
    "docs/layout-system.md",
    "docs/partials-system.md",
    "docs/component-system.md",
    "docs/css-system.md",
    "docs/js-system.md",
    "docs/js-interaction-plan.md",
    "docs/asset-system.md",
    "docs/asset-direction.md",
    "docs/page-section-style-map.md",
    "docs/mobile-system.md",
    "docs/mobile-behaviour.md",
    "docs/conversion-system.md",
    "docs/cross-site-difference-report.md",
]

UTILITY_ORDER = [
    "privacy.html",
    "cookies.html",
    "terms.html",
    "accessibility.html",
    "sitemap.html",
    "thanks.html",
    "404.html",
]

VARIANTS = [
    "constellation",
    "split-index",
    "ledger",
    "map",
    "magazine",
    "command",
    "shelf",
    "journey",
    "civic",
    "private",
]

PASS_TITLE = "Homepage Flow Cleanup Pass - 2026-05-13"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def title_from_file(filename: str) -> str:
    if filename == "404.html":
        return "404 recovery"
    return filename.removesuffix(".html").replace("-", " ").title()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def core_and_utility_pages(site_root: Path, config: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    config_pages = [page for page in config.get("pages", []) if isinstance(page, dict)]
    core = [page for page in config_pages if page.get("file") != "index.html"]
    core_files = {str(page.get("file")) for page in core}
    all_html = {path.name for path in site_root.glob("*.html") if path.name != "index.html"}
    utility_files = [name for name in UTILITY_ORDER if name in all_html and name not in core_files]
    utility_files.extend(sorted(all_html - core_files - set(utility_files)))
    utilities = [{"name": title_from_file(name), "file": name} for name in utility_files]
    return core, utilities


def target_for_section(section: str, core_pages: list[dict[str, object]], index: int) -> dict[str, object]:
    lower = section.lower()
    names = {
        "service": ["Services", "Product", "Products", "Shop", "Menu", "Programs", "Treatments"],
        "product": ["Product", "Products", "Shop", "Catalogue"],
        "price": ["Pricing", "Plans", "Fees", "Rates", "Tickets"],
        "fee": ["Pricing", "Fees", "Rates"],
        "question": ["FAQ", "Support", "Contact"],
        "faq": ["FAQ", "Support", "Contact"],
        "review": ["Reviews", "Results", "Outcomes", "Testimonials"],
        "proof": ["Proof", "Results", "Outcomes", "Work", "Portfolio"],
        "evidence": ["Evidence", "Results", "Outcomes", "Resources"],
        "result": ["Results", "Outcomes", "Impact", "Work"],
        "process": ["Process", "Journey", "Planning", "Booking"],
        "path": ["Journey", "Process", "Planning", "Booking"],
        "resource": ["Resources", "Guides", "Journal", "Insights", "Blog"],
        "guide": ["Guides", "Resources", "Journal", "Insights"],
        "story": ["Story", "Brand", "Company", "Profile", "Organisation"],
    }
    for key, candidates in names.items():
        if key in lower:
            for candidate in candidates:
                match = next((page for page in core_pages if str(page.get("name")) == candidate), None)
                if match:
                    return match
    return core_pages[index % len(core_pages)]


def hero_atlas_nav(config: dict[str, object], home_sections: list[str]) -> str:
    cta = str(config["cta"])
    section_links = [section for section in home_sections if section not in {"Hero", "CTA"}]
    first = section_links[0] if section_links else "Services"
    second = next((section for section in section_links if section in {"Services", "Products", "Shop", "Menu", "Programs", "Work", "Impact"}), section_links[min(1, len(section_links) - 1)] if section_links else "CTA")
    third = section_links[min(2, len(section_links) - 1)] if section_links else "Questions"
    return f"""
<!-- Homepage flow pass: hero shortcuts -->
      <nav class="hero-flow-links" aria-label="{esc(config['siteName'])} homepage section shortcuts">
        <a href="#section-{esc(slugify(first))}" data-track="hero_flow_{esc(slugify(first))}">{esc(first)}</a>
        <a href="#section-{esc(slugify(second))}" data-track="hero_flow_{esc(slugify(second))}">{esc(second)}</a>
        <a href="#section-{esc(slugify(third))}" data-track="hero_flow_{esc(slugify(third))}">{esc(third)}</a>
        <a href="contact.html" data-track="hero_flow_contact">{esc(cta)}</a>
      </nav>
<!-- /Homepage flow pass: hero shortcuts -->""".rstrip()


def remove_between_markers(text: str, label: str) -> str:
    for marker in ("Homepage atlas pass", "Homepage flow pass"):
        text = re.sub(
            rf"\n?<!-- {marker}: {re.escape(label)} -->.*?<!-- /{marker}: {re.escape(label)} -->\n?",
            "\n",
            text,
            flags=re.S,
        )
    return text


def move_disclaimer_before_cta(text: str) -> str:
    match = re.search(r"\n\s*<section class=\"section disclaimer\b.*?</section>\n", text, flags=re.S)
    if not match:
        return text
    disclaimer = match.group(0)
    text = text[: match.start()] + "\n" + text[match.end() :]
    cta_match = re.search(r"\n\s*<section\b[^>]*(?:id=\"section-cta\"|data-section=\"CTA\")[^>]*>", text)
    if not cta_match:
        return text + disclaimer
    return text[: cta_match.start()] + disclaimer + text[cta_match.start() :]


def add_missing_section_ids(text: str, sections: list[str]) -> str:
    for section in sections:
        slug = slugify(section)
        section_id = f"section-{slug}"
        if f'id="{section_id}"' in text:
            continue
        pattern = rf'(<section\b(?![^>]*\sid=)[^>]*\bdata-section="{re.escape(section)}"[^>]*>)'

        def add_id(match: re.Match[str]) -> str:
            return match.group(1).replace("<section", f'<section id="{section_id}"', 1)

        text = re.sub(pattern, add_id, text, count=1)
    return text


def replace_hero_secondary_cta(text: str, home_sections: list[str]) -> str:
    section_links = [section for section in home_sections if section not in {"Hero", "CTA"}]
    target = section_links[0] if section_links else "Services"
    label = f"Explore {target}"
    text = text.replace(
        'href="https://ash-tra.com/discovery/" data-track="secondary_home_hero">Discuss build</a>',
        f'href="#section-{slugify(target)}" data-track="secondary_home_flow">{esc(label)}</a>',
    )
    legacy_anchor = "site-" + "atlas"
    text = re.sub(
        rf'href="#{legacy_anchor}" data-track="secondary_home_atlas">.*?</a>',
        f'href="#section-{slugify(target)}" data-track="secondary_home_flow">{esc(label)}</a>',
        text,
        count=1,
        flags=re.S,
    )
    if 'data-track="secondary_home_flow"' in text:
        return text
    return re.sub(
        r'(<div class="button-row">(?:(?!</div>).)*?<a class="button primary"[^>]*>.*?</a>)<a class="button secondary"[^>]*>.*?</a>',
        rf'\1<a class="button secondary" href="#section-{esc(slugify(target))}" data-track="secondary_home_flow">{esc(label)}</a>',
        text,
        count=1,
        flags=re.S,
    )


def update_homepage(site_root: Path, config: dict[str, object], variant: str) -> None:
    index_path = site_root / "index.html"
    text = index_path.read_text(encoding="utf-8")
    home = next((page for page in config.get("pages", []) if isinstance(page, dict) and page.get("file") == "index.html"), {})
    home_sections = [str(item) for item in home.get("sections", [])]
    pages, _utilities = core_and_utility_pages(site_root, config)

    text = remove_between_markers(text, "hero routes")
    text = remove_between_markers(text, "hero shortcuts")
    text = remove_between_markers(text, "full site index")
    text = add_missing_section_ids(text, home_sections)
    text = replace_hero_secondary_cta(text, home_sections)
    text = text.replace("      <h2>CTA</h2>", f"      <h2>{esc(config['cta'])}</h2>")

    hero_nav = hero_atlas_nav(config, home_sections)
    text = re.sub(
        r"(\n\s*<div class=\"button-row\">.*?</div>)(\s*\n\s*<div class=\"hero-proof\")",
        rf"\1\n{hero_nav}\2",
        text,
        count=1,
        flags=re.S,
    )

    for index, section in enumerate([item for item in home_sections if item not in {"Hero", "CTA"}]):
        target = target_for_section(section, pages, index)
        old = (
            f'<a class="text-link" href="index.html" data-track="inline_home_{slugify(section)}">Explore Home</a>'
        )
        new = (
            f'<a class="text-link" href="{esc(target["file"])}" data-track="inline_home_{esc(slugify(section))}">Open {esc(target["name"])}</a>'
        )
        text = text.replace(old, new)

    text = move_disclaimer_before_cta(text)
    index_path.write_text(text, encoding="utf-8")


def atlas_css(slug: str) -> str:
    selector = f"body.theme-{slug}"
    return f"""
/* Homepage Flow Cleanup Pass - 2026-05-13: keep homepage order, remove public atlas section, and expose compact section shortcuts. */
html{{overflow-x:hidden;max-width:100%}}
{selector}{{max-width:100%;overflow-x:hidden}}
{selector} *,{selector} *::before,{selector} *::after{{min-width:0}}
{selector} main,{selector} .site-header,{selector} .site-footer,{selector} .container,{selector} .hero-grid,{selector} .section-grid,{selector} .card-grid,{selector} .dashboard-panel,{selector} .visual-card-stack,{selector} .pricing-grid,{selector} .resource-board{{max-width:100%}}
{selector} h1,{selector} h2,{selector} h3,{selector} p,{selector} a,{selector} span,{selector} small,{selector} strong{{overflow-wrap:break-word}}
{selector} .button,{selector} .nav-cta,{selector} .button-row a,{selector} .hero-flow-links a{{white-space:normal;max-width:100%}}
{selector} .hero-copy,{selector} .section-copy,{selector} .cta-panel,{selector} .finder-panel,{selector} .signature-panel{{max-width:100%}}
{selector} .card-grid{{flex-wrap:wrap;overflow-x:visible}}
{selector} .card-grid>*{{max-width:100%}}
{selector} .mini-card,{selector} .price-card,{selector} .metric-card,{selector} .resource-card{{max-width:100%;overflow-wrap:break-word;word-break:normal}}
{selector} .mini-card .card-thumb,{selector} .resource-card img,{selector} .visual-card-stack img{{max-width:100%;min-width:0}}
{selector} .immersive-footer-row{{max-width:100%;grid-template-columns:minmax(0,1fr) minmax(0,.8fr) minmax(0,auto)}}
{selector} .immersive-footer-row>*{{max-width:100%;min-width:0}}
{selector} .whatsapp-widget{{max-width:calc(100vw - 2rem)}}
{selector} .whatsapp-button{{max-width:100%;min-width:0;white-space:normal}}
{selector} .back-to-top{{max-width:calc(100vw - 2rem)}}
{selector} .hero-flow-links{{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}}
{selector} .hero-flow-links a{{display:inline-flex;align-items:center;justify-content:center;min-height:40px;padding:.55rem .78rem;border:1px solid var(--color-border);border-radius:var(--radius-pill);background:color-mix(in srgb,var(--color-surface) 82%,transparent);color:inherit;text-decoration:none;font-weight:850;font-size:var(--text-sm);box-shadow:var(--shadow-soft)}}
@media (max-width:980px){{{selector} .hero-grid,{selector} .section-grid,{selector} .cta-panel,{selector} .form-panel,{selector} .visual-card-stack,{selector} .immersive-footer-row{{grid-template-columns:minmax(0,1fr)!important}}{selector} .hero-copy,{selector} .section-copy{{width:100%!important;max-width:100%!important}}{selector} .card-grid{{display:grid!important;grid-template-columns:minmax(0,1fr)!important;overflow:visible!important}}{selector} .hero-flow-links a{{flex:1 1 145px}}{selector} .whatsapp-widget{{right:.65rem!important;max-width:calc(100vw - 1.3rem)}}{selector} .back-to-top{{right:.65rem!important;max-width:calc(100vw - 1.3rem)}}}}
""".strip()


def update_css(site_root: Path, slug: str) -> None:
    path = site_root / "css" / "styles.css"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n?/\* Homepage Atlas Pass - 2026-05-12:.*?(?=\n/\* |\Z)",
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"\n?/\* Homepage Flow Cleanup Pass - 2026-05-13:.*?(?=\n/\* |\Z)",
        "",
        text,
        flags=re.S,
    )
    path.write_text(text.rstrip() + "\n\n" + atlas_css(slug) + "\n", encoding="utf-8")


def pack_note(config: dict[str, object], variant: str) -> str:
    return f"""

## {PASS_TITLE}

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `{config['cta']}`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `{variant}` for `{config['siteName']}`, shaped by `{config['layoutSignature']}`, `{config['cardStyle']}`, `{config['jsSignature']}`, and `{config['themeMode']}` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.
""".rstrip()


def update_pack_docs(site_root: Path, config: dict[str, object], variant: str) -> None:
    note = pack_note(config, variant)
    for rel in REQUIRED_PACK_FILES:
        path = site_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"\n## (?:Homepage Atlas Pass - 2026-05-12|Homepage Flow Cleanup Pass - 2026-05-13)\n.*", "", text, flags=re.S)
        path.write_text(text.rstrip() + "\n" + note + "\n", encoding="utf-8")


def master_note() -> str:
    return """

## Homepage Flow Cleanup Pass - 2026-05-13

All 50 editable static homepages now keep the approved section order without an inserted public atlas block. The pass preserves the required inspiration mix and cross-site difference scores while replacing the route-index section with compact hero shortcuts to real homepage sections and keeping utility/legal/recovery routes in footer and sitemap surfaces.
""".rstrip()


def update_master_docs() -> None:
    for path in [
        SYSTEM_DOCS / "inspiration-reference-library.md",
        SYSTEM_DOCS / "50-site-diversity-register.md",
        SYSTEM_DOCS / "batch-diversity-review.md",
        DEMO_DOCS / "inspiration-reference-library.md",
        DEMO_DOCS / "50-site-diversity-register.md",
        DEMO_DOCS / "batch-diversity-review.md",
    ]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"\n## (?:Homepage Atlas Pass - 2026-05-12|Homepage Flow Cleanup Pass - 2026-05-13)\n.*", "", text, flags=re.S)
        path.write_text(text.rstrip() + "\n" + master_note() + "\n", encoding="utf-8")


def main() -> int:
    site_roots = sorted(path for path in DEMO_ROOT.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name))
    for site_root in site_roots:
        config = read_json(site_root / "site.config.json")
        number = int(config["number"])
        variant = VARIANTS[(number - 1) % len(VARIANTS)]
        update_pack_docs(site_root, config, variant)
        update_homepage(site_root, config, variant)
        update_css(site_root, str(config["slug"]))
    update_master_docs()
    print(f"Applied homepage atlas pass to {len(site_roots)} sites.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
