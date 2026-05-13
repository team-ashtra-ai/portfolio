#!/usr/bin/env python3
"""Apply the 50-site homepage atlas pass to the editable static demos."""

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
    "asset-system.html",
    "sitemap.html",
    "privacy.html",
    "cookies.html",
    "terms.html",
    "accessibility.html",
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


def page_summary(page: dict[str, object], config: dict[str, object], index: int) -> str:
    sections = [str(item) for item in page.get("sections", [])]
    focus = ", ".join(sections[1:4]) if len(sections) > 4 else str(page["name"])
    industry = str(config["industry"]).lower()
    return (
        f"Open the {str(page['name']).lower()} route for {focus.lower()} so {industry} visitors can compare context, proof, and next steps."
    )


def utility_summary(filename: str, config: dict[str, object]) -> str:
    label = title_from_file(filename).lower()
    brand = str(config["siteName"])
    summaries = {
        "asset-system.html": f"Review the local assets, icons, OG images, and static handoff materials used by {brand}.",
        "sitemap.html": f"Use the full sitemap to recover any route and verify the whole {brand} structure.",
        "privacy.html": "Read the privacy route before sending personal details through the static form.",
        "cookies.html": "Manage consent and understand the privacy-safe analytics approach.",
        "terms.html": "Check the demonstration terms and the final-client review requirement.",
        "accessibility.html": "Review accessibility expectations, keyboard access, and remediation routes.",
        "thanks.html": "Preview the post-submit recovery path for returning to the site.",
        "404.html": "Open the recovery page used when a visitor lands on a missing route.",
    }
    return summaries.get(filename, f"Open the {label} support route for this static site.")


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
    return f"""
<!-- Homepage atlas pass: hero routes -->
      <nav class="hero-atlas-links" aria-label="{esc(config['siteName'])} fast homepage routes">
        <a href="#site-atlas" data-track="hero_atlas_open">Site atlas</a>
        <a href="#section-{esc(slugify(first))}" data-track="hero_atlas_{esc(slugify(first))}">{esc(first)}</a>
        <a href="#section-{esc(slugify(second))}" data-track="hero_atlas_{esc(slugify(second))}">{esc(second)}</a>
        <a href="contact.html" data-track="hero_atlas_contact">{esc(cta)}</a>
      </nav>
<!-- /Homepage atlas pass: hero routes -->""".rstrip()


def atlas_section(site_root: Path, config: dict[str, object], variant: str) -> str:
    brand = str(config["siteName"])
    industry = str(config["industry"])
    cta = str(config["cta"])
    mode = str(config["themeMode"])
    layout = str(config["layoutSignature"])
    premium = str(config["premiumDirection"])
    pages, utilities = core_and_utility_pages(site_root, config)
    home = next((page for page in config.get("pages", []) if isinstance(page, dict) and page.get("file") == "index.html"), {})
    home_sections = [str(item) for item in home.get("sections", []) if str(item) not in {"Hero", "CTA"}]
    premium_sentence = premium.rstrip()
    if premium_sentence and premium_sentence[-1] not in ".!?":
        premium_sentence += "."
    quick_links = "".join(
        f'<a href="#section-{esc(slugify(section))}"><span>{index:02d}</span>{esc(section)}</a>'
        for index, section in enumerate(home_sections, start=2)
    )
    route_cards = []
    for index, page in enumerate(pages, start=1):
        route_cards.append(
            f'<article class="atlas-route-card"><a href="{esc(page["file"])}" data-track="atlas_page_{esc(slugify(str(page["name"])))}">'
            f'<span>{index:02d} / Core route</span><h3>{esc(page["name"])}</h3><p>{esc(page_summary(page, config, index))}</p><small>Open {esc(page["name"])}</small></a></article>'
        )
    utility_links = "".join(
        f'<a href="{esc(item["file"])}" data-track="atlas_utility_{esc(slugify(item["name"]))}">{esc(item["name"])}</a>'
        for item in utilities
    )
    utility_cards = "".join(
        f'<article class="atlas-route-card atlas-support-card"><a href="{esc(item["file"])}" data-track="atlas_support_{esc(slugify(item["name"]))}">'
        f'<span>Support route</span><h3>{esc(item["name"])}</h3><p>{esc(utility_summary(item["file"], config))}</p><small>Open {esc(item["name"])}</small></a></article>'
        for item in utilities[:4]
    )
    return f"""
<!-- Homepage atlas pass: full site index -->
<section id="site-atlas" class="section homepage-atlas portfolio-component wp-template-section atlas-variant-{esc(variant)} atlas-mode-{esc(mode)}" aria-labelledby="site-atlas-title" data-component-id="{esc(config['slug'])}-index-site-atlas" data-section-type="homepage-atlas" data-section-label="Site atlas" data-layout-variation="{esc(variant)}-site-index" data-pattern-family="homepage-atlas" data-wp-fields="admin_title,visibility,heading,subheading,route_repeater,section_anchor_repeater,utility_link_repeater,primary_cta_label,primary_cta_url,mobile_stack_rule,theme_colour" data-mobile-stack="source-order" data-theme-surface="{esc(mode)}">
  <div class="container atlas-shell">
    <div class="atlas-intro">
      <div>
        <p class="eyebrow">Site atlas</p>
        <h2 id="site-atlas-title">Every route through {esc(brand)}</h2>
        <p class="lead">This homepage is the working index for {esc(industry.lower())}: it explains the offer, points to every deeper page, and keeps the final action visible without making the visitor hunt.</p>
        <p>{esc(premium_sentence)} The page links problem, promise, services, process, proof, questions, support, legal routes, and conversion paths into one clear decision map.</p>
      </div>
      <div class="atlas-actions">
        <a class="button primary" href="contact.html" data-track="atlas_primary_cta">{esc(cta)}</a>
        <a class="button secondary" href="sitemap.html" data-track="atlas_sitemap">Open Sitemap</a>
      </div>
    </div>
    <nav class="atlas-quick" aria-label="{esc(brand)} homepage section links">
      {quick_links}
    </nav>
    <div class="atlas-route-grid" aria-label="{esc(brand)} core page routes">
      {"".join(route_cards)}
      {utility_cards}
    </div>
    <div class="atlas-utility-row" aria-label="{esc(brand)} support and legal routes">
      <span>{esc(layout)}</span>
      {utility_links}
    </div>
  </div>
</section>
<!-- /Homepage atlas pass: full site index -->""".strip()


def remove_between_markers(text: str, label: str) -> str:
    return re.sub(
        rf"\n?<!-- Homepage atlas pass: {re.escape(label)} -->.*?<!-- /Homepage atlas pass: {re.escape(label)} -->\n?",
        "\n",
        text,
        flags=re.S,
    )


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


def replace_hero_secondary_cta(text: str) -> str:
    text = text.replace(
        'href="https://ash-tra.com/discovery/" data-track="secondary_home_hero">Discuss build</a>',
        'href="#site-atlas" data-track="secondary_home_atlas">Explore Site Atlas</a>',
    )
    if 'data-track="secondary_home_atlas"' in text:
        return text
    return re.sub(
        r'(<div class="button-row">(?:(?!</div>).)*?<a class="button primary"[^>]*>.*?</a>)<a class="button secondary"[^>]*>.*?</a>',
        r'\1<a class="button secondary" href="#site-atlas" data-track="secondary_home_atlas">Explore Site Atlas</a>',
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
    text = remove_between_markers(text, "full site index")
    text = add_missing_section_ids(text, home_sections)
    text = replace_hero_secondary_cta(text)
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

    atlas = atlas_section(site_root, config, variant)
    insertion = re.search(r"\n\s*<section id=\"section-(?!hero\b)[^\"]+\" class=\"section content-section", text)
    if insertion:
        text = text[: insertion.start()] + "\n" + atlas + "\n" + text[insertion.start() :]

    text = move_disclaimer_before_cta(text)
    index_path.write_text(text, encoding="utf-8")


def atlas_css(slug: str) -> str:
    selector = f"body.theme-{slug}"
    luxury_light_band_css = ""
    if slug == "luxury":
        luxury_light_band_css = f"""
{selector} #section-services .section-copy,{selector} #section-portfolio .section-copy,{selector} #section-trust .section-copy,{selector} #section-questions .section-copy{{color:#081f18}}
{selector} #section-services .section-copy h2,{selector} #section-services .section-copy h3,{selector} #section-services .section-copy p,{selector} #section-services .section-copy a,{selector} #section-services .section-copy .eyebrow,{selector} #section-portfolio .section-copy h2,{selector} #section-portfolio .section-copy h3,{selector} #section-portfolio .section-copy p,{selector} #section-portfolio .section-copy a,{selector} #section-portfolio .section-copy .eyebrow,{selector} #section-trust .section-copy h2,{selector} #section-trust .section-copy h3,{selector} #section-trust .section-copy p,{selector} #section-trust .section-copy a,{selector} #section-trust .section-copy .eyebrow,{selector} #section-questions .section-copy h2,{selector} #section-questions .section-copy h3,{selector} #section-questions .section-copy p,{selector} #section-questions .section-copy a,{selector} #section-questions .section-copy .eyebrow{{color:#081f18}}
""".strip()
    return f"""
/* Homepage Atlas Pass - 2026-05-12: hero-first, CTA-final internal site index. */
html{{overflow-x:hidden;max-width:100%}}
{selector}{{max-width:100%;overflow-x:hidden}}
{selector} *,{selector} *::before,{selector} *::after{{min-width:0}}
{selector} main,{selector} .site-header,{selector} .site-footer,{selector} .container,{selector} .hero-grid,{selector} .section-grid,{selector} .card-grid,{selector} .dashboard-panel,{selector} .visual-card-stack,{selector} .pricing-grid,{selector} .resource-board{{max-width:100%}}
{selector} h1,{selector} h2,{selector} h3,{selector} p,{selector} a,{selector} span,{selector} small,{selector} strong{{overflow-wrap:break-word}}
{selector} .button,{selector} .nav-cta,{selector} .button-row a,{selector} .hero-atlas-links a{{white-space:normal;max-width:100%}}
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
{luxury_light_band_css}
{selector} .hero-atlas-links{{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}}
{selector} .hero-atlas-links a{{display:inline-flex;align-items:center;justify-content:center;min-height:40px;padding:.55rem .78rem;border:1px solid var(--color-border);border-radius:var(--radius-pill);background:color-mix(in srgb,var(--color-surface) 82%,transparent);color:inherit;text-decoration:none;font-weight:850;font-size:var(--text-sm);box-shadow:var(--shadow-soft)}}
{selector} .homepage-atlas{{scroll-margin-top:calc(var(--header-height) + 24px);background:linear-gradient(135deg,color-mix(in srgb,var(--color-primary) 7%,var(--color-bg)),var(--color-bg-alt));border-block:1px solid var(--color-border);overflow:hidden}}
{selector} .atlas-shell{{display:grid;gap:clamp(1rem,3vw,2rem)}}
{selector} .atlas-intro{{display:grid;grid-template-columns:minmax(0,.76fr) auto;gap:clamp(1rem,4vw,3rem);align-items:end}}
{selector} .atlas-intro h2{{font-size:clamp(2rem,5vw,5.2rem);max-width:11ch}}
{selector} .atlas-actions{{display:grid;gap:.65rem;justify-items:stretch;min-width:min(280px,100%)}}
{selector} .atlas-quick{{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:.55rem}}
{selector} .atlas-quick a{{display:flex;align-items:center;gap:.55rem;min-height:48px;padding:.65rem .8rem;border:1px solid var(--color-border);border-radius:var(--radius-sm);background:color-mix(in srgb,var(--color-surface) 84%,transparent);color:var(--color-text);text-decoration:none;font-weight:850}}
{selector} .atlas-quick span{{font-family:var(--font-mono);font-size:var(--text-xs);color:var(--color-link)}}
{selector} .atlas-route-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:clamp(.75rem,2vw,1.15rem)}}
{selector} .atlas-route-card{{min-width:0}}
{selector} .atlas-route-card a{{display:grid;align-content:space-between;gap:.7rem;min-height:100%;padding:var(--card-padding);border:1px solid var(--color-border);border-radius:var(--radius-md);background:color-mix(in srgb,var(--color-surface) 92%,transparent);color:var(--color-text);text-decoration:none;box-shadow:var(--shadow-soft);transition:transform var(--motion-base) var(--motion-ease),box-shadow var(--motion-base) var(--motion-ease),border-color var(--motion-base) var(--motion-ease)}}
{selector} .atlas-route-card a:hover{{transform:translateY(-3px);box-shadow:var(--shadow-medium);border-color:var(--color-primary)}}
{selector} .atlas-route-card span,{selector} .atlas-route-card small{{font-family:var(--font-mono);font-size:var(--text-xs);font-weight:900;text-transform:uppercase;letter-spacing:var(--tracking-wide);color:var(--color-link)}}
{selector} .atlas-route-card h3{{margin:0;font-size:clamp(1.15rem,2vw,1.55rem)}}
{selector} .atlas-route-card p{{margin:0;color:var(--color-muted)}}
{selector} .atlas-support-card a{{background:color-mix(in srgb,var(--color-accent) 12%,var(--color-surface));border-style:dashed}}
{selector} .atlas-utility-row{{display:flex;align-items:center;flex-wrap:wrap;gap:.55rem;padding-top:.25rem}}
{selector} .atlas-utility-row span{{font-weight:900;color:var(--color-muted);margin-right:.35rem}}
{selector} .atlas-utility-row a{{padding:.42rem .65rem;border:1px solid var(--color-border);border-radius:var(--radius-pill);background:color-mix(in srgb,var(--color-surface) 76%,transparent);text-decoration:none;font-weight:850;color:inherit}}
{selector} .atlas-variant-constellation .atlas-route-grid{{grid-template-columns:repeat(12,minmax(0,1fr))}}
{selector} .atlas-variant-constellation .atlas-route-card{{grid-column:span 3}}
{selector} .atlas-variant-constellation .atlas-route-card:nth-child(1),{selector} .atlas-variant-constellation .atlas-route-card:nth-child(6){{grid-column:span 6}}
{selector} .atlas-variant-split-index .atlas-shell{{grid-template-columns:minmax(260px,.42fr) minmax(0,1fr);align-items:start}}
{selector} .atlas-variant-split-index .atlas-intro{{grid-template-columns:1fr;position:sticky;top:calc(var(--header-height) + 28px)}}
{selector} .atlas-variant-split-index .atlas-quick,{selector} .atlas-variant-split-index .atlas-utility-row{{grid-column:1 / -1}}
{selector} .atlas-variant-ledger .atlas-route-grid{{grid-template-columns:1fr;gap:0;border:1px solid var(--color-border);background:var(--color-surface)}}
{selector} .atlas-variant-ledger .atlas-route-card a{{grid-template-columns:140px minmax(0,1fr) auto;align-items:center;border-width:0 0 1px;border-radius:0;box-shadow:none}}
{selector} .atlas-variant-map .atlas-route-card a{{border-left:var(--border-strong) solid var(--color-primary);border-radius:var(--radius-sm)}}
{selector} .atlas-variant-map .atlas-route-grid{{background-image:linear-gradient(90deg,color-mix(in srgb,var(--color-primary) 18%,transparent) 1px,transparent 1px),linear-gradient(0deg,color-mix(in srgb,var(--color-primary) 18%,transparent) 1px,transparent 1px);background-size:46px 46px;padding:1px}}
{selector} .atlas-variant-magazine .atlas-route-grid{{grid-template-columns:1.2fr .8fr .8fr}}
{selector} .atlas-variant-magazine .atlas-route-card:first-child{{grid-row:span 2}}
{selector} .atlas-variant-command .atlas-route-card a{{border-radius:10px;background:linear-gradient(180deg,color-mix(in srgb,var(--color-surface) 88%,var(--color-primary)),var(--color-surface))}}
{selector} .atlas-variant-shelf .atlas-route-grid{{align-items:end}}
{selector} .atlas-variant-shelf .atlas-route-card:nth-child(odd) a{{min-height:260px}}
{selector} .atlas-variant-journey .atlas-route-grid{{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}}
{selector} .atlas-variant-journey .atlas-route-card a{{position:relative;padding-left:calc(var(--card-padding) + 1rem)}}
{selector} .atlas-variant-journey .atlas-route-card a::before{{content:"";position:absolute;left:.9rem;top:var(--card-padding);bottom:var(--card-padding);width:3px;background:var(--color-primary);border-radius:999px}}
{selector} .atlas-variant-civic .atlas-route-card a,{selector} .atlas-variant-civic .atlas-quick a{{border-radius:0;box-shadow:none;border-width:2px}}
{selector} .atlas-variant-private .atlas-route-card a,{selector} .atlas-variant-private .atlas-quick a{{border-radius:0;box-shadow:none;background:transparent}}
{selector} .atlas-variant-private .atlas-intro{{border-block:1px solid var(--color-border);padding-block:clamp(1rem,3vw,2rem)}}
@media (max-width:1180px){{{selector} .atlas-variant-constellation .atlas-route-grid,{selector} .atlas-variant-magazine .atlas-route-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}{selector} .atlas-variant-constellation .atlas-route-card,{selector} .atlas-variant-constellation .atlas-route-card:nth-child(1),{selector} .atlas-variant-constellation .atlas-route-card:nth-child(6){{grid-column:auto}}}}
@media (max-width:980px){{{selector} .hero-grid,{selector} .section-grid,{selector} .cta-panel,{selector} .form-panel,{selector} .visual-card-stack,{selector} .immersive-footer-row{{grid-template-columns:minmax(0,1fr)!important}}{selector} .hero-copy,{selector} .section-copy{{width:100%!important;max-width:100%!important}}{selector} .card-grid{{display:grid!important;grid-template-columns:minmax(0,1fr)!important;overflow:visible!important}}{selector} .atlas-intro,{selector} .atlas-variant-split-index .atlas-shell,{selector} .atlas-variant-magazine .atlas-route-grid,{selector} .atlas-variant-ledger .atlas-route-card a{{grid-template-columns:1fr}}{selector} .atlas-variant-split-index .atlas-intro{{position:static}}{selector} .atlas-actions{{justify-items:start;min-width:0}}{selector} .hero-atlas-links a{{flex:1 1 145px}}{selector} .whatsapp-widget{{right:.65rem!important;max-width:calc(100vw - 1.3rem)}}{selector} .back-to-top{{right:.65rem!important;max-width:calc(100vw - 1.3rem)}}}}
""".strip()


def update_css(site_root: Path, slug: str) -> None:
    path = site_root / "css" / "styles.css"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n?/\* Homepage Atlas Pass - 2026-05-12:.*", "", text, flags=re.S)
    path.write_text(text.rstrip() + "\n\n" + atlas_css(slug) + "\n", encoding="utf-8")


def pack_note(config: dict[str, object], variant: str) -> str:
    return f"""

## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `{config['cta']}`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
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
        text = re.sub(r"\n## Homepage Atlas Pass - 2026-05-12\n.*", "", text, flags=re.S)
        path.write_text(text.rstrip() + "\n" + note + "\n", encoding="utf-8")


def master_note() -> str:
    return """

## Homepage Atlas Pass - 2026-05-12

All 50 editable static homepages now receive a dedicated `#site-atlas` section. The pass preserves the required inspiration mix and cross-site difference scores while adding hero-first, CTA-final homepage structure, complete internal links to every site page, section anchor navigation, utility/legal/recovery links, and variant-specific atlas layouts so the pages do not collapse into one shared template.
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
        text = re.sub(r"\n## Homepage Atlas Pass - 2026-05-12\n.*", "", text, flags=re.S)
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
