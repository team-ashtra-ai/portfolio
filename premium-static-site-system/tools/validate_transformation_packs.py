#!/usr/bin/env python3
"""Validate the 50-site transformation-pack contract.

This is intentionally narrow: it checks that every demo site has the required
planning documents, source partial references, CSS tokens, and measurable
cross-site difference score before a visual redesign can be treated as complete.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SYSTEM_ROOT = ROOT / "premium-static-site-system"
DEMO_ROOT = ROOT / "demo-sites"

REQUIRED_DOCS = [
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
    "docs/asset-licenses.md",
]

REQUIRED_PARTIALS = [
    "header.html",
    "mobile-menu.html",
    "footer.html",
    "hero.html",
    "cta.html",
    "form.html",
    "cards.html",
    "resources.html",
    "pricing.html",
    "faq.html",
    "cookie.html",
    "legal.html",
    "404.html",
    "thanks.html",
]

REQUIRED_CSS_TOKENS = [
    "--font-display",
    "--font-body",
    "--font-accent",
    "--font-mono",
    "--text-xs",
    "--text-sm",
    "--text-md",
    "--text-lg",
    "--text-xl",
    "--text-hero",
    "--line-tight",
    "--line-normal",
    "--line-loose",
    "--tracking-tight",
    "--tracking-normal",
    "--tracking-wide",
    "--color-bg",
    "--color-bg-alt",
    "--color-surface",
    "--color-surface-raised",
    "--color-text",
    "--color-muted",
    "--color-primary",
    "--color-secondary",
    "--color-accent",
    "--color-border",
    "--color-success",
    "--color-warning",
    "--color-error",
    "--gradient-primary",
    "--gradient-surface",
    "--overlay-dark",
    "--overlay-light",
    "--container-sm",
    "--container-md",
    "--container-lg",
    "--container-xl",
    "--container-fluid",
    "--space-xs",
    "--space-sm",
    "--space-md",
    "--space-lg",
    "--space-xl",
    "--space-section",
    "--radius-none",
    "--radius-sm",
    "--radius-md",
    "--radius-lg",
    "--radius-xl",
    "--radius-pill",
    "--shadow-none",
    "--shadow-soft",
    "--shadow-medium",
    "--shadow-strong",
    "--shadow-glow",
    "--border-thin",
    "--border-medium",
    "--border-strong",
    "--motion-fast",
    "--motion-base",
    "--motion-slow",
    "--motion-ease",
]

REQUIRED_MASTER_DOCS = [
    SYSTEM_ROOT / "docs" / "50-site-inspiration-diversity-brief.md",
    SYSTEM_ROOT / "docs" / "50-site-diversity-register.md",
    SYSTEM_ROOT / "docs" / "batch-diversity-review.md",
    SYSTEM_ROOT / "docs" / "inspiration-reference-library.md",
    DEMO_ROOT / "docs" / "50-site-diversity-register.md",
    DEMO_ROOT / "docs" / "batch-diversity-review.md",
    DEMO_ROOT / "docs" / "inspiration-reference-library.md",
]


def site_dirs() -> list[Path]:
    return sorted(
        path
        for path in DEMO_ROOT.iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name)
    )


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_site(site: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_DOCS:
        path = site / rel
        if not path.exists():
            errors.append(f"{site.name}: missing {rel}")
            continue
        if len(read(path).strip()) < 120:
            errors.append(f"{site.name}: {rel} is too thin")

    for partial in REQUIRED_PARTIALS:
        path = site / "partials" / partial
        if not path.exists():
            errors.append(f"{site.name}: missing partials/{partial}")
        elif not read(path).strip():
            errors.append(f"{site.name}: empty partials/{partial}")

    css_path = site / "css" / "styles.css"
    if not css_path.exists():
        errors.append(f"{site.name}: missing css/styles.css")
    else:
        css = read(css_path)
        missing_tokens = [token for token in REQUIRED_CSS_TOKENS if token not in css]
        if missing_tokens:
            errors.append(f"{site.name}: css/styles.css missing tokens {', '.join(missing_tokens)}")

    js_path = site / "js" / "main.js"
    if not js_path.exists():
        errors.append(f"{site.name}: missing js/main.js")
    else:
        js = read(js_path)
        for hook in ["data-menu-toggle", "data-cookie-banner", "data-contact-form", "data-component=\"faq\"", "ashtra:track"]:
            if hook not in js:
                errors.append(f"{site.name}: js/main.js missing behaviour hook {hook}")

    layout = site / "docs" / "layout-system.md"
    if layout.exists():
        text = read(layout)
        for phrase in [
            "This site will not reuse the same layout structure as the previous sites.",
            "This site will not use the same hero-card-grid-FAQ-CTA rhythm unless redesigned completely.",
        ]:
            if phrase not in text:
                errors.append(f"{site.name}: layout-system.md missing anti-template phrase")

    theme = site / "docs" / "theme-guide.md"
    if theme.exists() and "Brand Difference Plan" not in read(theme):
        errors.append(f"{site.name}: theme-guide.md missing Brand Difference Plan")

    section_map = site / "docs" / "page-section-style-map.md"
    if section_map.exists() and "Section-By-Section Style Plan" not in read(section_map):
        errors.append(f"{site.name}: page-section-style-map.md missing section style plan")

    inspiration = site / "docs" / "inspiration-audit.md"
    if inspiration.exists():
        text = read(inspiration)
        category_counts = {
            category: len(re.findall(rf"^\| {category} \|", text, flags=re.MULTILINE))
            for category in ["direct", "adjacent", "contrast", "interaction"]
        }
        if category_counts["direct"] < 3:
            errors.append(f"{site.name}: inspiration-audit.md needs at least 3 direct references")
        if category_counts["adjacent"] < 2:
            errors.append(f"{site.name}: inspiration-audit.md needs at least 2 adjacent references")
        if category_counts["contrast"] < 2:
            errors.append(f"{site.name}: inspiration-audit.md needs at least 2 contrast references")
        if category_counts["interaction"] < 1:
            errors.append(f"{site.name}: inspiration-audit.md needs at least 1 interaction reference")
        if "Inspired by these patterns, this ASH-TRA site will use an original design system" not in text:
            errors.append(f"{site.name}: inspiration-audit.md missing originality statement")

    extraction = site / "docs" / "design-extraction.md"
    if extraction.exists():
        text = read(extraction)
        if text.count("## ") < 9:
            errors.append(f"{site.name}: design-extraction.md should document at least 8 references")
        for field in [
            "Layout archetype",
            "Header structure",
            "Mobile menu behaviour",
            "Footer structure",
            "Hero type",
            "JS interaction ideas",
            "What must not be copied",
        ]:
            if field not in text:
                errors.append(f"{site.name}: design-extraction.md missing extraction field {field}")

    direction = site / "docs" / "theme-direction.md"
    if direction.exists():
        text = read(direction)
        for field in ["Layout archetype", "Header", "Mobile menu", "Footer", "Typography", "CTA flow", "Assets", "JS interactions", "Motion"]:
            if field not in text:
                errors.append(f"{site.name}: theme-direction.md missing difference field {field}")

    difference = site / "docs" / "cross-site-difference-report.md"
    if difference.exists():
        match = re.search(r"Difference score \| ([0-9])", read(difference))
        if not match:
            errors.append(f"{site.name}: cross-site-difference-report.md missing difference score")
        elif int(match.group(1)) < 4:
            errors.append(f"{site.name}: difference score below acceptance threshold")

    return errors


def main() -> int:
    errors: list[str] = []
    sites = site_dirs()
    if len(sites) != 50:
        errors.append(f"expected 50 numbered site folders, found {len(sites)}")

    for path in REQUIRED_MASTER_DOCS:
        if not path.exists():
            errors.append(f"missing master document {path.relative_to(ROOT)}")
        elif len(read(path).strip()) < 500:
            errors.append(f"master document is too thin: {path.relative_to(ROOT)}")

    register = SYSTEM_ROOT / "docs" / "50-site-diversity-register.md"
    if register.exists():
        text = read(register)
        rows = re.findall(r"^\| \d{2} \|", text, flags=re.MULTILINE)
        if len(rows) != 50:
            errors.append(f"50-site-diversity-register.md should contain 50 site rows, found {len(rows)}")

    for site in sites:
        errors.extend(validate_site(site))

    if errors:
        print("Transformation pack validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Transformation pack validation passed for {len(sites)} sites.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
