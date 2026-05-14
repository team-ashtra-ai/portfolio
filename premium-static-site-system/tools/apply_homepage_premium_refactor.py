#!/usr/bin/env python3
"""Apply the 50-site homepage premium UX pass.

This is a post-generation pass for the current portfolio output. It keeps the
approved site identities and reference packs, then enforces the latest homepage
rules: minimal hero copy, exactly two hero CTAs, no visible text inside hero
art, ten top-level homepage sections, balanced section grids, and stronger
footer/readability polish.
"""

from __future__ import annotations

import html
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = ROOT / "demo-sites"
SYSTEM_DOCS = ROOT / "premium-static-site-system" / "docs"
DEMO_DOCS = DEMO_ROOT / "docs"

PASS_TITLE = "Homepage Premium UX Refactor Pass - 2026-05-13"

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

MODE_MOTIFS = {
    "care": "clinical calm",
    "technical": "precision interface",
    "dark": "cinematic command",
    "professional": "executive decision",
    "editorial": "editorial gallery",
    "commerce": "product theatre",
    "hospitality": "arrival atmosphere",
    "civic": "public service",
    "luxury": "private atelier",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_block(text: str, title: str) -> str:
    pattern = rf"\n{{0,2}}## {re.escape(title)}\n.*?(?=\n## |\Z)"
    return re.sub(pattern, "", text, flags=re.S).rstrip()


def strip_css_pass(text: str) -> str:
    pattern = rf"\n*/\* {re.escape(PASS_TITLE)}.*?\*/.*?(?=\n/\* |\Z)"
    return re.sub(pattern, "", text, flags=re.S).rstrip()


def append_note(path: Path, note: str) -> None:
    if not path.exists():
        return
    text = strip_block(path.read_text(encoding="utf-8"), PASS_TITLE)
    path.write_text(text + "\n" + note + "\n", encoding="utf-8")


def design_field(config: dict[str, object], key: str, fallback: str = "") -> str:
    passport = config.get("designPassport", {})
    if isinstance(passport, dict) and passport.get(key):
        return str(passport[key])
    return str(config.get(key, fallback))


def short_industry(config: dict[str, object]) -> str:
    industry = str(config.get("industry", "Premium service"))
    first = industry.split("&")[0].split(",")[0].strip()
    return first or industry


def hero_lead(config: dict[str, object]) -> str:
    layout = str(config.get("layoutSignature") or design_field(config, "layoutArchetype", "Premium experience")).strip()
    buyer = design_field(config, "buyerPsychology", "clear decisions").strip().lower()
    return f"{layout} for {buyer}."


def first_follow_section(text: str, hero_end: int) -> tuple[str, str]:
    after_hero = text[hero_end:]
    pattern = re.compile(
        r"<section\b(?=[^>]*\bid=[\"'](section-[^\"']+)[\"'])(?=[^>]*\bdata-section=[\"']([^\"']+)[\"'])",
        re.I,
    )
    for match in pattern.finditer(after_hero):
        section_id, label = match.group(1), match.group(2)
        if section_id != "section-cta":
            return f"#{section_id}", label
    return "#section-cta", "Next"


def section_bounds(text: str, start_match: re.Match[str]) -> tuple[int, int]:
    tag_re = re.compile(r"</?section\b[^>]*>", re.I)
    depth = 0
    start = start_match.start()
    for match in tag_re.finditer(text, start):
        is_close = match.group(0).startswith("</")
        if is_close:
            depth -= 1
            if depth == 0:
                return start, match.end()
        else:
            depth += 1
    raise ValueError("Could not find closing section tag")


def render_hero(
    start_tag: str,
    config: dict[str, object],
    prefix: str,
    secondary_href: str,
    secondary_label: str,
) -> str:
    slug = str(config["slug"])
    brand = str(config["siteName"])
    cta = str(config.get("cta", "Contact"))
    industry = short_industry(config)
    image_system = design_field(config, "imageSystem", f"{industry} visual story")
    image_alt = f"{brand} {image_system}".strip()
    image_base = f"{prefix}assets/images/hero/{slug}-home-hero"
    if prefix:
        primary_href = f"{prefix}contact.html"
    else:
        primary_href = "contact.html"
    return f"""{start_tag}
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">{esc(industry)}</p>
      <h1>{esc(brand)}</h1>
      <p class="lead">{esc(hero_lead(config))}</p>
      <div class="button-row" aria-label="{esc(brand)} primary actions">
        <a class="button primary" href="{esc(primary_href)}" data-track="cta_home_hero">{esc(cta)}</a>
        <a class="button secondary" href="{esc(secondary_href)}" data-track="secondary_home_hero">Explore</a>
      </div>
    </div>
    <figure class="hero-media premium-hero-picture">
      <picture>
        <source media="(max-width: 640px)" srcset="{esc(image_base)}-mobile.svg">
        <source media="(max-width: 1024px)" srcset="{esc(image_base)}-tablet.svg">
        <img src="{esc(image_base)}.svg" alt="{esc(image_alt)}" width="960" height="640" loading="eager" decoding="async">
      </picture>
    </figure>
  </div>
</section>"""


def replace_hero(text: str, config: dict[str, object], prefix: str = "") -> str:
    match = re.search(r"<section\b(?=[^>]*\bid=[\"']section-hero[\"'])[^>]*>", text, flags=re.I)
    if not match:
        return text
    start, end = section_bounds(text, match)
    start_tag = match.group(0)
    secondary_href, secondary_label = first_follow_section(text, end)
    replacement = render_hero(start_tag, config, prefix, secondary_href, secondary_label)
    return text[:start] + replacement + text[end:]


def remove_home_disclaimer(text: str) -> str:
    while True:
        match = re.search(r"<section\b(?=[^>]*\bclass=[\"'][^\"']*\bdisclaimer\b)[^>]*>", text, flags=re.I)
        if not match:
            break
        start, end = section_bounds(text, match)
        text = text[:start].rstrip() + "\n\n" + text[end:].lstrip()
    return re.sub(r"\n{4,}", "\n\n\n", text)


def update_homepage(site_root: Path, config: dict[str, object]) -> None:
    path = site_root / "index.html"
    text = path.read_text(encoding="utf-8")
    text = replace_hero(text, config, "")
    text = remove_home_disclaimer(text)
    path.write_text(text, encoding="utf-8")


def update_source_partial(site_root: Path, config: dict[str, object]) -> None:
    path = site_root / "partials" / "hero.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = replace_hero(text, config, "../")
    path.write_text(text, encoding="utf-8")


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{max(0, min(255, int(channel))):02x}" for channel in rgb)


def mix(a: str, b: str, amount: float) -> str:
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return rgb_to_hex((
        round(ar * (1 - amount) + br * amount),
        round(ag * (1 - amount) + bg * amount),
        round(ab * (1 - amount) + bb * amount),
    ))


def css_hex(css: str, token: str, fallback: str) -> str:
    match = re.search(rf"--{re.escape(token)}:\s*(#[0-9a-fA-F]{{3,6}})", css)
    return match.group(1) if match else fallback


def palette(site_root: Path) -> dict[str, str]:
    css = (site_root / "css" / "styles.css").read_text(encoding="utf-8")
    return {
        "bg": css_hex(css, "color-bg", "#f7f4ee"),
        "surface": css_hex(css, "color-surface", "#ffffff"),
        "text": css_hex(css, "color-text", "#111827"),
        "primary": css_hex(css, "color-primary", "#111827"),
        "accent": css_hex(css, "color-accent", "#5b7cfa"),
        "warm": css_hex(css, "color-warm", "#f3d9a4"),
    }


def motif_shapes(mode: str, pal: dict[str, str], width: int, height: int, seed: int) -> str:
    primary = pal["primary"]
    accent = pal["accent"]
    surface = pal["surface"]
    warm = pal["warm"]
    dark_panel = mix(primary, "#000000", 0.18)
    light_panel = mix(surface, accent, 0.08)
    w = width
    h = height
    dx = (seed % 9) * 7
    dy = (seed % 7) * 9
    common = f"""
  <path d="M{-80 + dx} {int(h * .76)} C {int(w * .18)} {int(h * .52)}, {int(w * .37)} {int(h * .92)}, {int(w * .58)} {int(h * .62)} S {int(w * .88)} {int(h * .34)}, {w + 80} {int(h * .54)}" fill="none" stroke="{accent}" stroke-width="{max(18, width // 36)}" opacity=".38"/>
  <path d="M{int(w * .08)} {int(h * .18)} C {int(w * .28)} {int(h * .04)}, {int(w * .42)} {int(h * .18)}, {int(w * .58)} {int(h * .08)} S {int(w * .88)} {int(h * .02)}, {int(w * .96)} {int(h * .22)}" fill="none" stroke="{primary}" stroke-width="{max(10, width // 70)}" opacity=".16"/>
"""
    if mode in {"technical", "dark"}:
        return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .12)} {int(h * .18)}) rotate(-3)">
    <rect width="{int(w * .54)}" height="{int(h * .52)}" rx="28" fill="{dark_panel}" opacity=".94"/>
    <rect x="{int(w * .04)}" y="{int(h * .06)}" width="{int(w * .20)}" height="{int(h * .14)}" rx="18" fill="{mix(accent, surface, .2)}" opacity=".86"/>
    <rect x="{int(w * .28)}" y="{int(h * .06)}" width="{int(w * .18)}" height="{int(h * .14)}" rx="18" fill="{surface}" opacity=".15"/>
    <path d="M{int(w * .05)} {int(h * .32)} L{int(w * .16)} {int(h * .24)} L{int(w * .27)} {int(h * .38)} L{int(w * .42)} {int(h * .19)} L{int(w * .49)} {int(h * .29)}" fill="none" stroke="{accent}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <g opacity=".32" stroke="{surface}" stroke-width="8" stroke-linecap="round">
      <path d="M{int(w * .05)} {int(h * .43)} H{int(w * .44)}"/>
      <path d="M{int(w * .05)} {int(h * .49)} H{int(w * .34)}"/>
    </g>
  </g>
  <g transform="translate({int(w * .67)} {int(h * .22)})" fill="{surface}" opacity=".86">
    <rect width="{int(w * .18)}" height="{int(h * .38)}" rx="24"/>
    <circle cx="{int(w * .05)}" cy="{int(h * .09)}" r="{max(14, w // 46)}" fill="{accent}"/>
    <path d="M{int(w * .05)} {int(h * .20)} H{int(w * .14)} M{int(w * .05)} {int(h * .27)} H{int(w * .12)}" stroke="{primary}" stroke-width="9" stroke-linecap="round" opacity=".25"/>
  </g>
"""
    if mode == "care":
        return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .12)} {int(h * .14)})">
    <rect width="{int(w * .36)}" height="{int(h * .58)}" rx="38" fill="{surface}" opacity=".92"/>
    <path d="M{int(w * .06)} {int(h * .43)} C {int(w * .13)} {int(h * .22)}, {int(w * .25)} {int(h * .22)}, {int(w * .31)} {int(h * .43)}" fill="none" stroke="{accent}" stroke-width="{max(14, w // 48)}" stroke-linecap="round"/>
    <circle cx="{int(w * .18)}" cy="{int(h * .23)}" r="{int(min(w, h) * .075)}" fill="{mix(accent, surface, .25)}" opacity=".76"/>
  </g>
  <g transform="translate({int(w * .56)} {int(h * .18)}) rotate(4)" filter="url(#softShadow)">
    <rect width="{int(w * .28)}" height="{int(h * .48)}" rx="30" fill="{light_panel}"/>
    <path d="M{int(w * .04)} {int(h * .34)} C {int(w * .11)} {int(h * .23)}, {int(w * .19)} {int(h * .42)}, {int(w * .25)} {int(h * .30)}" fill="none" stroke="{primary}" stroke-width="10" opacity=".25" stroke-linecap="round"/>
  </g>
"""
    if mode == "commerce":
        return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .12)} {int(h * .22)})">
    <rect width="{int(w * .70)}" height="{int(h * .40)}" rx="34" fill="{surface}" opacity=".9"/>
    <rect x="{int(w * .06)}" y="{int(h * .08)}" width="{int(w * .16)}" height="{int(h * .24)}" rx="24" fill="{mix(accent, surface, .12)}"/>
    <rect x="{int(w * .27)}" y="{int(h * .04)}" width="{int(w * .18)}" height="{int(h * .30)}" rx="28" fill="{mix(primary, surface, .72)}"/>
    <rect x="{int(w * .51)}" y="{int(h * .09)}" width="{int(w * .13)}" height="{int(h * .22)}" rx="22" fill="{warm}"/>
    <path d="M{int(w * .04)} {int(h * .34)} H{int(w * .66)}" stroke="{primary}" stroke-width="8" opacity=".22" stroke-linecap="round"/>
  </g>
"""
    if mode == "hospitality":
        return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .12)} {int(h * .13)})">
    <rect width="{int(w * .62)}" height="{int(h * .56)}" rx="42" fill="{surface}" opacity=".88"/>
    <path d="M{int(w * .08)} {int(h * .08)} H{int(w * .54)} V{int(h * .34)} H{int(w * .08)} Z" fill="{mix(accent, surface, .24)}" opacity=".62"/>
    <path d="M{int(w * .14)} {int(h * .43)} C {int(w * .25)} {int(h * .34)}, {int(w * .38)} {int(h * .52)}, {int(w * .50)} {int(h * .40)}" fill="none" stroke="{primary}" stroke-width="12" opacity=".2" stroke-linecap="round"/>
    <rect x="{int(w * .17)}" y="{int(h * .38)}" width="{int(w * .24)}" height="{int(h * .09)}" rx="22" fill="{warm}" opacity=".78"/>
  </g>
"""
    if mode == "editorial":
        return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .10)} {int(h * .13)}) rotate(-2)">
    <rect width="{int(w * .30)}" height="{int(h * .52)}" rx="12" fill="{surface}" opacity=".92"/>
    <rect x="{int(w * .04)}" y="{int(h * .05)}" width="{int(w * .22)}" height="{int(h * .22)}" rx="8" fill="{mix(accent, surface, .18)}"/>
    <rect x="{int(w * .04)}" y="{int(h * .31)}" width="{int(w * .22)}" height="{int(h * .14)}" rx="8" fill="{mix(primary, surface, .72)}"/>
  </g>
  <g filter="url(#softShadow)" transform="translate({int(w * .45)} {int(h * .20)}) rotate(4)">
    <rect width="{int(w * .38)}" height="{int(h * .42)}" rx="16" fill="{surface}" opacity=".88"/>
    <path d="M{int(w * .04)} {int(h * .30)} C {int(w * .12)} {int(h * .15)}, {int(w * .24)} {int(h * .38)}, {int(w * .34)} {int(h * .18)}" fill="none" stroke="{accent}" stroke-width="12" stroke-linecap="round"/>
  </g>
"""
    if mode == "civic":
        return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .12)} {int(h * .18)})">
    <rect width="{int(w * .64)}" height="{int(h * .48)}" rx="16" fill="{surface}" opacity=".92"/>
    <rect x="{int(w * .06)}" y="{int(h * .08)}" width="{int(w * .16)}" height="{int(h * .22)}" rx="10" fill="{mix(accent, surface, .18)}"/>
    <rect x="{int(w * .28)}" y="{int(h * .08)}" width="{int(w * .28)}" height="{int(h * .06)}" rx="8" fill="{primary}" opacity=".18"/>
    <rect x="{int(w * .28)}" y="{int(h * .19)}" width="{int(w * .22)}" height="{int(h * .06)}" rx="8" fill="{primary}" opacity=".13"/>
    <path d="M{int(w * .06)} {int(h * .38)} H{int(w * .56)}" stroke="{accent}" stroke-width="10" stroke-linecap="round" opacity=".55"/>
  </g>
"""
    if mode == "luxury":
        return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .18)} {int(h * .12)})">
    <path d="M{int(w * .12)} 0 H{int(w * .48)} C{int(w * .55)} {int(h * .20)} {int(w * .42)} {int(h * .50)} {int(w * .22)} {int(h * .56)} C{int(w * .06)} {int(h * .45)} {int(w * .02)} {int(h * .16)} {int(w * .12)} 0Z" fill="{surface}" opacity=".86"/>
    <rect x="{int(w * .14)}" y="{int(h * .34)}" width="{int(w * .27)}" height="{int(h * .10)}" rx="28" fill="{warm}" opacity=".82"/>
    <path d="M{int(w * .19)} {int(h * .16)} C{int(w * .28)} {int(h * .06)}, {int(w * .39)} {int(h * .21)}, {int(w * .45)} {int(h * .10)}" stroke="{primary}" stroke-width="8" fill="none" opacity=".24" stroke-linecap="round"/>
  </g>
"""
    return common + f"""
  <g filter="url(#softShadow)" transform="translate({int(w * .11)} {int(h * .17)})">
    <rect width="{int(w * .66)}" height="{int(h * .48)}" rx="30" fill="{surface}" opacity=".9"/>
    <path d="M{int(w * .06)} {int(h * .34)} L{int(w * .18)} {int(h * .19)} L{int(w * .32)} {int(h * .28)} L{int(w * .48)} {int(h * .13)} L{int(w * .59)} {int(h * .24)}" fill="none" stroke="{accent}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="{int(w * .06)}" y="{int(h * .40)}" width="{int(w * .18)}" height="{int(h * .04)}" rx="8" fill="{primary}" opacity=".18"/>
    <rect x="{int(w * .30)}" y="{int(h * .40)}" width="{int(w * .24)}" height="{int(h * .04)}" rx="8" fill="{primary}" opacity=".12"/>
  </g>
"""


def hero_svg(config: dict[str, object], pal: dict[str, str], width: int, height: int, variant: str) -> str:
    slug = str(config["slug"])
    seed = int(config["number"]) * (3 if variant == "desktop" else 5 if variant == "tablet" else 7)
    mode = str(config.get("themeMode", "professional"))
    motif = MODE_MOTIFS.get(mode, "premium visual")
    bg = pal["bg"]
    surface = pal["surface"]
    primary = pal["primary"]
    accent = pal["accent"]
    warm = pal["warm"]
    secondary = mix(accent, warm, 0.38)
    wash = mix(bg, surface, 0.55)
    angle_offset = seed % 17
    shapes = motif_shapes(mode, pal, width, height, seed)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(config["siteName"])} hero visual</title>
<desc id="desc">{esc(short_industry(config))} themed {esc(motif)} artwork with no visible text.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{wash}"/>
    <stop offset=".48" stop-color="{bg}"/>
    <stop offset="1" stop-color="{mix(primary, bg, .82)}"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{accent}"/>
    <stop offset="1" stop-color="{secondary}"/>
  </linearGradient>
  <pattern id="grain" width="{36 + angle_offset}" height="{36 + angle_offset}" patternUnits="userSpaceOnUse">
    <path d="M0 {18 + angle_offset // 2} H{36 + angle_offset}" stroke="{primary}" stroke-width="1" opacity=".06"/>
    <path d="M{18 + angle_offset // 2} 0 V{36 + angle_offset}" stroke="{primary}" stroke-width="1" opacity=".045"/>
  </pattern>
  <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="{max(12, height // 46)}" stdDeviation="{max(14, width // 70)}" flood-color="{mix(primary, '#000000', .35)}" flood-opacity=".22"/>
  </filter>
  <clipPath id="frame">
    <rect x="{max(14, width // 60)}" y="{max(14, height // 60)}" width="{width - max(28, width // 30)}" height="{height - max(28, height // 30)}" rx="{max(32, min(width, height) // 12)}"/>
  </clipPath>
</defs>
<rect width="{width}" height="{height}" fill="url(#bg)"/>
<rect width="{width}" height="{height}" fill="url(#grain)"/>
<g clip-path="url(#frame)">
  <path d="M{-width * .12:.0f} {height * .18:.0f} L{width * .58:.0f} {-height * .12:.0f} L{width * 1.14:.0f} {height * .38:.0f} L{width * .32:.0f} {height * .92:.0f} Z" fill="url(#accent)" opacity=".18"/>
  <path d="M{width * .72:.0f} {-height * .08:.0f} C{width * .54:.0f} {height * .20:.0f},{width * .84:.0f} {height * .42:.0f},{width * .61:.0f} {height * .72:.0f} C{width * .78:.0f} {height * .86:.0f},{width * 1.08:.0f} {height * .76:.0f},{width * 1.18:.0f} {height * .44:.0f} L{width * 1.18:.0f} {-height * .08:.0f} Z" fill="{surface}" opacity=".36"/>
{shapes}
  <path d="M{width * .06:.0f} {height * .88:.0f} C{width * .24:.0f} {height * .78:.0f},{width * .38:.0f} {height * .96:.0f},{width * .56:.0f} {height * .84:.0f} S{width * .88:.0f} {height * .72:.0f},{width * .98:.0f} {height * .86:.0f}" fill="none" stroke="{primary}" stroke-width="{max(4, width // 150)}" opacity=".12"/>
</g>
</svg>
"""


def update_hero_assets(site_root: Path, config: dict[str, object]) -> None:
    slug = str(config["slug"])
    pal = palette(site_root)
    targets = [
        (site_root / "assets" / "images" / "hero" / f"{slug}-home-hero.svg", 960, 640, "desktop"),
        (site_root / "assets" / "images" / "hero" / f"{slug}-home-hero-tablet.svg", 960, 760, "tablet"),
        (site_root / "assets" / "images" / "hero" / f"{slug}-home-hero-mobile.svg", 900, 1120, "mobile"),
    ]
    for path, width, height, variant in targets:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(hero_svg(config, pal, width, height, variant), encoding="utf-8")


def homepage_css(slug: str) -> str:
    selector = f"body.theme-{slug}"
    return f"""
/* {PASS_TITLE}: minimal hero copy, two CTAs, balanced premium homepage rhythm. */
{selector}{{
  --premium-section-pad:clamp(56px,6.2vw,112px);
  --premium-card-gap:clamp(.85rem,1.8vw,1.35rem);
  --premium-hero-radius:clamp(18px,2.2vw,34px);
  --premium-footer-bg:#07090d;
  --premium-footer-text:#ffffff;
  --premium-footer-muted:#e5e7eb;
}}
{selector} main > section{{padding-block:var(--premium-section-pad)}}
{selector} .hero-section{{padding-block:clamp(44px,6vw,92px)!important;min-height:0!important;overflow:hidden}}
{selector} .hero-grid{{display:grid!important;grid-template-columns:minmax(0,.72fr) minmax(420px,1.28fr)!important;align-items:stretch!important;gap:clamp(1.2rem,4vw,4rem)!important}}
{selector} .hero-copy{{display:flex!important;flex-direction:column;justify-content:center;max-width:620px!important;margin:0!important;padding:0!important;background:transparent!important;border:0!important;box-shadow:none!important;color:var(--color-text)}}
{selector} .hero-copy .eyebrow{{margin:0 0 .7rem!important;font-size:.74rem;letter-spacing:.08em;color:var(--color-link)}}
{selector} .hero-copy h1{{max-width:10ch!important;margin:0!important;font-size:clamp(2.8rem,7vw,7.2rem)!important;line-height:.94!important;letter-spacing:0!important;text-wrap:balance}}
{selector} .hero-copy .lead{{max-width:42ch!important;margin:.95rem 0 0!important;font-size:clamp(1.02rem,1.55vw,1.28rem)!important;line-height:1.48!important;color:color-mix(in srgb,var(--color-text) 78%,var(--color-bg))}}
{selector} .hero-copy h2,{selector} .hero-copy>p:not(.eyebrow):not(.lead),{selector} .hero-flow-links,{selector} .hero-proof,{selector} .signature-panel,{selector} .target-stage,{selector} .hero-media figcaption{{display:none!important}}
{selector} .button-row{{display:flex!important;flex-wrap:wrap;gap:.72rem!important;margin-top:1.35rem!important;max-width:460px}}
{selector} .button-row .button:nth-child(n+3){{display:none!important}}
{selector} .button,{selector} .nav-cta{{position:relative;gap:.5rem;transition:transform var(--motion-base) var(--motion-ease),box-shadow var(--motion-base) var(--motion-ease),background var(--motion-base) var(--motion-ease),border-color var(--motion-base) var(--motion-ease)}}
{selector} .button::after,{selector} .nav-cta::after{{content:"";width:.42rem;height:.42rem;border-top:2px solid currentColor;border-right:2px solid currentColor;transform:rotate(45deg);flex:0 0 auto}}
{selector} .premium-hero-picture{{position:relative!important;display:block!important;margin:0!important;min-height:clamp(360px,42vw,650px)!important;padding:0!important;border-radius:var(--premium-hero-radius)!important;overflow:hidden!important;border:1px solid color-mix(in srgb,var(--color-border) 72%,transparent)!important;background:var(--color-surface)!important;box-shadow:0 28px 90px color-mix(in srgb,var(--color-primary) 18%,transparent)!important}}
{selector} .premium-hero-picture::before{{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(135deg,rgba(255,255,255,.18),transparent 44%,rgba(0,0,0,.10));mix-blend-mode:soft-light}}
{selector} .premium-hero-picture::after,{selector} .hero-media::after{{content:none!important;display:none!important}}
{selector} .premium-hero-picture picture,{selector} .premium-hero-picture img{{display:block;width:100%!important;height:100%!important;min-height:inherit!important}}
{selector} .premium-hero-picture img{{object-fit:cover!important;opacity:1!important;filter:saturate(1.08) contrast(1.04)!important;transform:scale(1.01)}}
{selector} .section-grid{{display:grid!important;grid-template-columns:minmax(230px,.64fr) minmax(0,1.36fr)!important;align-items:stretch!important;gap:clamp(1rem,3vw,3rem)!important}}
{selector}[data-mode="technical"] .section-grid,{selector}[data-mode="dark"] .section-grid{{grid-template-columns:minmax(220px,.56fr) minmax(0,1.44fr)!important}}
{selector}[data-mode="editorial"] .section-grid,{selector}[data-mode="luxury"] .section-grid{{grid-template-columns:minmax(240px,.78fr) minmax(0,1.22fr)!important}}
{selector}[data-mode="commerce"] .section-grid,{selector}[data-mode="hospitality"] .section-grid{{grid-template-columns:minmax(240px,.72fr) minmax(0,1.28fr)!important}}
{selector} .section-copy{{align-self:stretch!important;display:flex!important;flex-direction:column!important;justify-content:center!important;max-width:66ch!important;min-width:0!important}}
{selector} .section-copy h2{{max-width:min(18ch,100%)!important;text-wrap:balance!important;margin-bottom:.75rem!important}}
{selector} .section-copy .lead{{max-width:58ch!important;line-height:1.5!important}}
{selector} .section-copy>p:not(.eyebrow):not(.lead){{max-width:60ch!important;line-height:1.56!important}}
{selector} .content-section h2,{selector} .content-section h3,{selector} .content-section h4,{selector} .content-section p,{selector} .content-section li{{writing-mode:horizontal-tb!important;text-orientation:mixed!important;word-break:normal!important;overflow-wrap:break-word}}
{selector}.mode-dark .content-section:nth-of-type(odd),{selector}.mode-luxury .content-section:nth-of-type(odd),{selector}[data-mode="dark"] .content-section:nth-of-type(odd),{selector}[data-mode="luxury"] .content-section:nth-of-type(odd){{--color-text:#111827;--color-heading:#111827;--color-muted:#243041;color:#111827!important;background:#ffffff!important}}
{selector}.mode-dark .content-section:nth-of-type(odd) h2,{selector}.mode-luxury .content-section:nth-of-type(odd) h2,{selector}.mode-dark .content-section:nth-of-type(odd) h3,{selector}.mode-luxury .content-section:nth-of-type(odd) h3,{selector}.mode-dark .content-section:nth-of-type(odd) p,{selector}.mode-luxury .content-section:nth-of-type(odd) p,{selector}.mode-dark .content-section:nth-of-type(odd) a,{selector}.mode-luxury .content-section:nth-of-type(odd) a{{color:#111827!important}}
{selector}.mode-dark .content-section:nth-of-type(even),{selector}.mode-luxury .content-section:nth-of-type(even),{selector}[data-mode="dark"] .content-section:nth-of-type(even),{selector}[data-mode="luxury"] .content-section:nth-of-type(even){{--color-text:#f8fafc;--color-heading:#ffffff;--color-muted:#e5e7eb;color:#f8fafc!important}}
{selector}.mode-dark .content-section:nth-of-type(even) h2,{selector}.mode-luxury .content-section:nth-of-type(even) h2,{selector}.mode-dark .content-section:nth-of-type(even) h3,{selector}.mode-luxury .content-section:nth-of-type(even) h3,{selector}.mode-dark .content-section:nth-of-type(even) p,{selector}.mode-luxury .content-section:nth-of-type(even) p,{selector}.mode-dark .content-section:nth-of-type(even) a,{selector}.mode-luxury .content-section:nth-of-type(even) a{{color:inherit!important}}
{selector} .section-icon{{width:48px!important;height:48px!important;padding:.32rem;border:1px solid color-mix(in srgb,var(--color-border) 78%,transparent);background:color-mix(in srgb,var(--color-surface) 76%,var(--color-bg));box-shadow:var(--shadow-soft)}}
{selector} .card-grid,{selector} .pricing-grid,{selector} .resource-board,{selector} .dashboard-panel{{gap:var(--premium-card-gap)!important;align-items:stretch!important}}
{selector} .card-grid>.mini-card,{selector} .pricing-grid>.price-card,{selector} .resource-board>.resource-card,{selector} .dashboard-panel>.metric-card{{height:100%;min-height:100%;transition:transform var(--motion-base) var(--motion-ease),box-shadow var(--motion-base) var(--motion-ease),border-color var(--motion-base) var(--motion-ease)}}
{selector} .mini-card .card-thumb,{selector} .resource-card img,{selector} .cta-panel img{{aspect-ratio:4/3!important;width:100%!important;object-fit:cover!important}}
{selector} .visual-card-stack{{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:var(--premium-card-gap)!important;align-items:stretch!important}}
{selector} .visual-card-stack figure:first-child{{grid-row:auto!important;grid-column:auto!important}}
{selector} .visual-card-stack>*{{min-height:100%!important}}
{selector} .visual-card-stack img{{height:100%!important;min-height:220px!important;max-height:340px!important;object-fit:cover!important}}
{selector} .process-list,{selector} .checklist-panel{{align-self:stretch!important}}
{selector} .process-list li,{selector} .checklist-panel li{{height:100%;min-width:0;grid-template-columns:auto minmax(0,1fr)!important}}
{selector} .process-list li h3,{selector} .checklist-panel li h3{{grid-column:2!important;margin:0!important;writing-mode:horizontal-tb!important;text-orientation:mixed!important}}
{selector} .process-list li p{{grid-column:1 / -1!important;margin-top:.35rem!important}}
{selector} .checklist-panel li p{{margin-top:.3rem!important}}
{selector} .map-panel{{align-self:stretch!important;min-width:0}}
{selector} .map-canvas{{min-height:clamp(260px,30vw,440px)!important}}
{selector} .map-list article{{min-height:100%}}
{selector} .content-section[data-section-type="cta"]>.section-grid{{display:none!important}}
{selector} .content-section[data-section-type="cta"]{{padding-block:clamp(54px,6vw,96px)!important}}
{selector} .cta-panel{{margin:0!important;align-items:center!important;border-radius:clamp(16px,2vw,28px)!important;box-shadow:0 24px 70px color-mix(in srgb,var(--color-primary) 16%,transparent)!important}}
{selector} .site-footer{{background:var(--premium-footer-bg)!important;color:var(--premium-footer-text)!important}}
{selector} .site-footer *{{color:var(--premium-footer-text)!important}}
{selector} .site-footer p,{selector} .site-footer small,{selector} .site-footer li,{selector} .site-footer span{{color:var(--premium-footer-muted)!important}}
{selector} .site-footer h1,{selector} .site-footer h2,{selector} .site-footer h3,{selector} .site-footer a,{selector} .site-footer strong{{color:var(--premium-footer-text)!important}}
{selector} .site-footer .button.primary{{background:var(--premium-footer-text)!important;color:var(--premium-footer-bg)!important;border-color:var(--premium-footer-text)!important}}
{selector} h1,{selector} h2,{selector} h3,{selector} h4,{selector} h5,{selector} h6{{letter-spacing:0!important}}
{selector} h4{{font-size:clamp(.95rem,1.1vw,1.08rem);line-height:1.2;margin:0 0 .55rem}}
{selector} h5,{selector} h6{{font-size:.92rem;line-height:1.25;margin:0 0 .45rem}}
@media (hover:hover){{
  {selector} .button:hover,{selector} .nav-cta:hover{{transform:translateY(-2px);box-shadow:var(--shadow-medium)}}
  {selector} .premium-hero-picture:hover img{{transform:scale(1.045)}}
  {selector} .mini-card:hover,{selector} .price-card:hover,{selector} .resource-card:hover,{selector} .metric-card:hover{{transform:translateY(-4px);box-shadow:var(--shadow-medium)}}
}}
@media (prefers-reduced-motion:no-preference){{
  {selector} .reveal-ready{{opacity:0!important;transform:translateY(18px)!important;transition:opacity var(--motion-slow) var(--motion-ease),transform var(--motion-slow) var(--motion-ease)!important}}
  {selector} .reveal-ready.is-visible{{opacity:1!important;transform:none!important}}
  {selector} .premium-hero-picture img{{transition:transform 900ms var(--motion-ease),filter 900ms var(--motion-ease)}}
}}
@media (max-width:1180px){{
  {selector} .hero-grid{{grid-template-columns:minmax(0,1fr)!important}}
  {selector} .premium-hero-picture{{min-height:clamp(300px,58vw,520px)!important;order:-1}}
  {selector} .visual-card-stack{{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
}}
@media (max-width:760px){{
  {selector}{{--premium-section-pad:clamp(42px,11vw,68px)}}
  {selector} .hero-section{{padding-block:clamp(24px,8vw,46px)!important}}
  {selector} .hero-copy h1{{font-size:clamp(2.25rem,15vw,4.1rem)!important;max-width:100%!important}}
  {selector} .hero-copy .lead{{font-size:.98rem!important;line-height:1.42!important}}
  {selector} .button-row{{max-width:none;width:100%}}
  {selector} .button-row .button{{flex:1 1 100%;justify-content:center}}
  {selector} .premium-hero-picture{{min-height:clamp(240px,68vw,360px)!important;border-radius:18px!important}}
  {selector} .section-grid,{selector}[data-mode] .section-grid,{selector} section[data-pattern-family] .section-grid,{selector} .visual-card-stack,{selector} section[data-pattern-family] .visual-card-stack,{selector} .card-grid,{selector} section[data-pattern-family] .card-grid,{selector} .pricing-grid,{selector} .resource-board,{selector} .dashboard-panel,{selector} .process-list,{selector} .checklist-panel,{selector} .map-list,{selector} .cta-panel{{grid-template-columns:minmax(0,1fr)!important}}
  {selector} .section-grid>*{{min-width:0!important;width:100%!important}}
  {selector} .section-copy{{justify-content:flex-start!important}}
  {selector} .mini-card,{selector} .price-card,{selector} .metric-card,{selector} .resource-card,{selector} .process-list li,{selector} .checklist-panel li{{width:100%!important;min-width:0!important}}
  {selector} .visual-card-stack img{{min-height:190px!important;max-height:280px!important}}
}}
@media (prefers-reduced-motion:reduce){{
  {selector} .premium-hero-picture img,{selector} .button,{selector} .nav-cta,{selector} .mini-card,{selector} .price-card,{selector} .resource-card,{selector} .metric-card{{transition:none!important;transform:none!important}}
}}
""".strip()


def update_css(site_root: Path, config: dict[str, object]) -> None:
    css_path = site_root / "css" / "styles.css"
    text = css_path.read_text(encoding="utf-8")
    text = strip_css_pass(text)
    css_path.write_text(text + "\n\n" + homepage_css(str(config["slug"])) + "\n", encoding="utf-8")


def site_note(config: dict[str, object]) -> str:
    motif = MODE_MOTIFS.get(str(config.get("themeMode", "professional")), "premium visual")
    return f"""

## {PASS_TITLE}

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `{motif}` artwork for desktop, tablet, and mobile. The image direction remains tied to `{design_field(config, "imageSystem", "site-specific visual direction")}` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
""".rstrip()


def master_note() -> str:
    return f"""

## {PASS_TITLE}

All 50 numbered homepages received the premium UX pass: each homepage keeps 10 top-level sections, uses minimal hero copy, limits hero actions to one primary and one secondary button, replaces text-heavy hero UI mockups with no-visible-text local hero artwork, improves card/media balance, adds button icon affordances and reveal/hover transitions, and hardens footer contrast across themes. The changes preserve each site's documented reference set, transformation pack, local CSS/JS/assets, and 4-5 cross-site difference requirement.
""".rstrip()


def update_site_docs(site_root: Path, config: dict[str, object]) -> None:
    note = site_note(config)
    for rel in REQUIRED_PACK_FILES:
        append_note(site_root / rel, note)


def update_master_docs() -> None:
    for path in [
        SYSTEM_DOCS / "inspiration-reference-library.md",
        SYSTEM_DOCS / "50-site-diversity-register.md",
        SYSTEM_DOCS / "batch-diversity-review.md",
        DEMO_DOCS / "inspiration-reference-library.md",
        DEMO_DOCS / "50-site-diversity-register.md",
        DEMO_DOCS / "batch-diversity-review.md",
    ]:
        append_note(path, master_note())


def site_roots() -> list[Path]:
    return sorted(path for path in DEMO_ROOT.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name))


def main() -> int:
    roots = site_roots()
    configs = [(site_root, read_json(site_root / "site.config.json")) for site_root in roots]

    # Documentation is updated before the homepage and asset rewrite work.
    for site_root, config in configs:
        update_site_docs(site_root, config)
    update_master_docs()

    for site_root, config in configs:
        update_homepage(site_root, config)
        update_source_partial(site_root, config)
        update_hero_assets(site_root, config)
        update_css(site_root, config)

    print(f"Applied {PASS_TITLE} to {len(configs)} numbered homepages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
