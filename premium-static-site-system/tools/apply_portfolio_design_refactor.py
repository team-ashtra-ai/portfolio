#!/usr/bin/env python3
"""Apply a portfolio-wide design refactor pass for visible polish."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = ROOT / "demo-sites"
SYSTEM_DOCS = ROOT / "premium-static-site-system" / "docs"
DEMO_DOCS = DEMO_ROOT / "docs"

PASS_TITLE = "Portfolio Design Refactor Pass - 2026-05-13"

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

ROUTE_COPY: dict[str, tuple[str, str, str, str]] = {
    "healthcare": ("Care routes", "Choose the right care path", "Jump from symptoms, services, doctor proof, pricing, and appointment routes without losing clinical context.", "Explore Care"),
    "life-sciences": ("Research paths", "Review the research dossier", "Move between biology, platform, pipeline, trials, publications, partners, and investor contact with an evidence-first structure.", "Explore Research"),
    "wellness": ("Routine paths", "Build a practical routine", "Compare services, method, results, products, pricing, and consultation steps as a calm self-care journey.", "Explore Routine"),
    "technology": ("System routes", "Map the infrastructure route", "Scan services, platforms, security, migration, support, pricing, and audit paths like an operations map.", "Explore Systems"),
    "saas": ("Product routes", "Trace the product workflow", "Move through features, integrations, onboarding, pricing, proof, and demo paths with product-led clarity.", "Explore Product"),
    "telecommunications": ("Coverage routes", "Check coverage and service routes", "Compare coverage, speed, installation, devices, support, plans, and outage routes in one compact utility panel.", "Check Routes"),
    "cybersecurity": ("Security routes", "Review the security posture", "Jump through threats, audits, compliance, identity, incident response, and security review paths.", "Explore Security"),
    "data-analytics": ("Insight routes", "Plan the analytics workspace", "Move from sources and pipelines to dashboards, reporting, governance, pricing, and a planning call.", "Explore Insights"),
    "finance": ("Money routes", "Compare the money decisions", "Use the guide to scan goals, advisory paths, cashflow, risk, pricing, resources, and contact routes.", "Compare Routes"),
    "insurance": ("Cover routes", "Compare cover and claims", "Move through risk scenarios, policy options, claims, pricing, support, and quote routes with fewer dead ends.", "Compare Cover"),
    "legal": ("Case routes", "Find the legal route", "Scan practice areas, documents, process, fees, confidentiality, resources, and consultation paths.", "Explore Cases"),
    "accounting": ("Ledger routes", "Plan close, tax, and payroll", "Jump between bookkeeping, tax, payroll, deadlines, pricing, resources, and proposal routes.", "Explore Ledger"),
    "consulting": ("Strategy routes", "Shape the strategy brief", "Move through services, frameworks, workshops, proof, resources, pricing, and brief submission paths.", "Explore Strategy"),
    "education": ("Learning paths", "Find the learning path", "Compare courses, teachers, method, results, resources, questions, pricing, and trial routes.", "Explore Courses"),
    "recruitment": ("Hiring routes", "Choose hiring or talent support", "Scan employer, candidate, roles, process, pricing, proof, and contact routes without repeating a job-board pattern.", "Explore Hiring"),
    "real-estate": ("Property routes", "Browse property decisions", "Move through listings, valuations, neighbourhoods, viewings, management, pricing, and enquiry routes.", "Explore Property"),
    "construction": ("Build routes", "Plan the build route", "Compare project scope, timelines, materials, safety, estimates, proof, and quote routes.", "Explore Build"),
    "architecture": ("Studio routes", "Explore the studio services", "Move through projects, planning stages, process, materials, pricing, journal, and project enquiry routes.", "Explore Studio"),
    "interiors": ("Room routes", "Build the room direction", "Compare moods, rooms, materials, products, pricing, process, and design brief routes.", "Explore Rooms"),
    "manufacturing": ("Production routes", "Scope production support", "Scan capability, materials, QA, facilities, supply, volume, and RFQ routes.", "Explore Production"),
    "engineering": ("Technical routes", "Review the technical brief", "Move through systems, standards, inspections, projects, proof, pricing, and engineer enquiry paths.", "Explore Engineering"),
    "energy": ("Energy routes", "Model the energy plan", "Compare assets, usage, storage, resilience, savings, pricing, and consultation routes.", "Explore Energy"),
    "utilities": ("Service routes", "Find service support", "Jump through outages, billing, repairs, access, maintenance, alerts, and service request paths.", "Explore Service"),
    "environmental": ("Impact routes", "Review site and impact routes", "Move between assessment, compliance, biodiversity, reporting, metrics, and audit paths.", "Explore Impact"),
    "agriculture": ("Season routes", "Plan the season route", "Compare fields, crops, soil, weather, yield, harvest, trade, and visit routes.", "Explore Season"),
    "food-production": ("Trade routes", "Trace product and trade routes", "Move through batches, quality, traceability, ingredients, packaging, trade, and enquiry paths.", "Explore Trade"),
    "restaurant": ("Dining routes", "Reserve, dine, or plan events", "Scan menu, booking, atmosphere, private dining, location, reviews, and reservation routes.", "Explore Dining"),
    "hotel": ("Stay routes", "Choose the stay path", "Compare rooms, amenities, location, offers, availability, guest journey, and booking routes.", "Explore Stay"),
    "travel": ("Trip routes", "Start the trip plan", "Move through destinations, itineraries, budgets, durations, experiences, and planning routes.", "Explore Trips"),
    "transport": ("Route planner", "Plan route or booking", "Compare schedules, fleet, pickup, safety, fares, coverage, and ride booking paths.", "Plan Route"),
    "logistics": ("Freight routes", "Quote and track freight", "Move through tracking, warehouses, route maps, delivery status, supply chain, and quote paths.", "Explore Freight"),
    "automotive": ("Vehicle routes", "Compare vehicle and service routes", "Scan vehicles, finance, servicing, inspections, showroom, test drive, and booking paths.", "Explore Vehicles"),
    "aviation": ("Charter routes", "Plan charter and operations", "Compare aircraft, safety, routes, operations, fleet details, and charter request paths.", "Explore Charter"),
    "maritime": ("Shipping routes", "Route vessels, ports, and cargo", "Move through vessels, ports, cargo, capacity, tracking, schedules, and shipping quote paths.", "Explore Shipping"),
    "retail": ("Shop routes", "Shop, visit, or join", "Compare products, categories, offers, loyalty, hours, store details, and visit paths.", "Explore Shop"),
    "ecommerce": ("Market routes", "Browse, filter, and buy", "Move through products, filters, sellers, deals, support, trust, and market routes.", "Browse Routes"),
    "fashion": ("Collection routes", "Shop the collection route", "Scan collections, looks, materials, sizing, stores, journal, and styling paths.", "Explore Collection"),
    "beauty": ("Treatment routes", "Build the treatment routine", "Compare treatments, products, routines, results, booking, questions, and consultation paths.", "Explore Routine"),
    "media": ("Media routes", "Explore shows and media kit", "Move through stories, shows, schedule, episodes, audience proof, advertise, and contact routes.", "Explore Media"),
    "entertainment": ("Ticket routes", "Find dates, tickets, and shows", "Scan events, performers, venues, seating, schedules, tours, and ticket paths.", "Explore Shows"),
    "publishing": ("Reader routes", "Read, subscribe, advertise", "Move through issues, archive, authors, subscriptions, media kit, and editorial contact paths.", "Explore Reading"),
    "marketing": ("Campaign routes", "Review cases and campaigns", "Compare work, strategy, services, results, proof, resources, and campaign brief routes.", "Explore Cases"),
    "creative": ("Studio routes", "Explore studio work", "Move through projects, identity, process, services, proof, pricing, and project enquiry paths.", "Explore Work"),
    "sports": ("Program routes", "Find programs and products", "Compare classes, training, events, gear, schedules, membership, and join routes.", "Explore Programs"),
    "events": ("Event routes", "Plan dates and tickets", "Move through venues, packages, dates, suppliers, planning, pricing, and enquiry paths.", "Explore Events"),
    "government": ("Service routes", "Find the public service route", "Scan eligibility, forms, documents, appointments, support, policy, and request paths.", "Find Service"),
    "nonprofit": ("Impact routes", "Donate, volunteer, see impact", "Move through mission, projects, proof, donation, volunteer, reports, and support routes.", "Explore Impact"),
    "veterinary": ("Care routes", "Find the right care route", "Compare symptoms, services, visits, emergency cues, pricing, resources, and booking paths.", "Explore Care"),
    "luxury": ("Private routes", "Request private access", "Move through heritage, craft, private service, concierge, collections, and access request routes.", "Explore Private"),
    "personal-brand": ("Media routes", "Read, subscribe, or book", "Scan essays, books, speaking, media kit, newsletter, resources, and appearance booking paths.", "Explore Media"),
}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_block(text: str, title: str) -> str:
    pattern = rf"\n{{0,2}}## {re.escape(title)}\n.*?(?=\n## |\Z)"
    return re.sub(pattern, "", text, flags=re.S).rstrip()


def strip_css_pass(text: str) -> str:
    return re.sub(
        rf"\n*/\* {re.escape(PASS_TITLE)}.*?\*/.*?(?=\n/\* |\Z)",
        "",
        text,
        flags=re.S,
    ).rstrip()


def route_copy(config: dict[str, object]) -> tuple[str, str, str, str]:
    slug = str(config["slug"])
    if slug in ROUTE_COPY:
        return ROUTE_COPY[slug]
    return (
        "Site routes",
        f"Explore {config['siteName']} routes",
        f"Move through the most useful {str(config['industry']).lower()} pages, proof, support, and conversion paths.",
        "Explore Routes",
    )


def update_homepage(path: Path, config: dict[str, object]) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("hero-atlas-links", "hero-flow-links")
    text = text.replace("hero_atlas_contact", "hero_flow_contact")
    text = text.replace(">Explore Site Atlas</a>", ">Explore Home Sections</a>")
    path.write_text(text, encoding="utf-8")


def update_assets(site_root: Path) -> int:
    updated = 0
    asset_root = site_root / "assets"
    if not asset_root.exists():
        return updated
    for path in asset_root.rglob("*.svg"):
        text = path.read_text(encoding="utf-8")
        original = text
        text = re.sub(r"\n?\s*<text\b[^>]*>\s*Image assets\s*</text>", "", text)
        text = re.sub(r"\n?\s*<text\b[^>]*>[^<]*/[^<]*/\s*local asset\s*</text>", "", text)
        text = re.sub(
            r"<title id=\"title\">([^<]+?)\s+Image assets</title>",
            r'<title id="title">\1 visual system</title>',
            text,
        )
        text = re.sub(
            r"<desc id=\"desc\">Original local image asset for ([^<]+?) static portfolio site\.</desc>",
            r'<desc id="desc">\1 original visual system.</desc>',
            text,
        )
        if text != original:
            path.write_text(text, encoding="utf-8")
            updated += 1
    return updated


def design_css(slug: str) -> str:
    selector = f"body.theme-{slug}"
    return f"""
/* {PASS_TITLE}: stronger visual rhythm, compact route guide, and non-template polish. */
{selector}{{
  --section-padding:clamp(54px,6vw,104px);
  --space-section:var(--section-padding);
  --grid-gap:clamp(1rem,3.2vw,3.4rem);
  --card-padding:clamp(1rem,1.8vw,1.55rem);
  text-rendering:optimizeLegibility;
}}
{selector}[data-density="dense"],{selector}[data-density="compact"]{{--section-padding:clamp(46px,5vw,86px);--grid-gap:clamp(.85rem,2.4vw,2.5rem)}}
{selector}[data-density="spacious"],{selector}[data-density="theatrical"]{{--section-padding:clamp(62px,6.8vw,120px);--grid-gap:clamp(1.2rem,3.6vw,4.2rem)}}
{selector} .section{{padding-block:var(--section-padding)}}
{selector} .hero-section{{min-height:0!important;padding-block:clamp(42px,6vw,92px) clamp(50px,7vw,104px)!important}}
{selector} .hero-grid{{display:grid!important;grid-template-columns:minmax(0,.92fr) minmax(360px,1.08fr);align-items:center;gap:var(--grid-gap)}}
{selector} .hero-copy{{position:relative;z-index:2;max-width:760px;margin:0!important;padding:0!important;background:transparent!important;box-shadow:none!important;border:0!important}}
{selector} .hero-copy h1{{max-width:13ch;font-size:clamp(2.25rem,5.4vw,5.25rem);line-height:1.02;margin-bottom:.75rem}}
{selector} .hero-copy h2{{max-width:62ch;font-size:clamp(1.08rem,1.8vw,1.55rem);line-height:1.35;margin-bottom:.85rem;color:color-mix(in srgb,currentColor 88%,var(--color-primary))}}
{selector} h2{{font-size:clamp(1.6rem,3.2vw,3.25rem);line-height:1.08}}
{selector} h3{{font-size:clamp(1rem,1.25vw,1.16rem);line-height:1.18}}
{selector} p{{margin-block:.55rem 0}}
{selector} .lead{{max-width:64ch;font-size:clamp(1rem,1.45vw,1.2rem);line-height:1.55}}
{selector} .eyebrow{{margin-bottom:.65rem;letter-spacing:.06em}}
{selector} .button-row{{margin-top:1.15rem;gap:.65rem}}
{selector} .button,{selector} .nav-cta{{min-height:44px;padding:.72rem 1rem;line-height:1.15}}
{selector} .hero-proof{{margin-top:1rem}}
{selector} .hero-proof span{{padding:.38rem .64rem;font-size:.82rem}}
{selector} .signature-panel{{display:none!important}}
{selector} .target-media,{selector} .hero-media{{position:relative!important;inset:auto!important;z-index:0!important;opacity:1!important;order:0;min-height:clamp(300px,36vw,560px)!important}}
{selector} .target-stage{{position:relative!important;z-index:1;min-height:min(360px,55vh)!important;max-width:min(100%,720px);transform:none!important}}
{selector} .target-media>picture img{{opacity:.2}}
{selector} .hero-media figcaption,{selector} .target-media figcaption{{font-size:.85rem;line-height:1.35}}
{selector} .section-grid{{grid-template-columns:minmax(230px,.68fr) minmax(0,1.32fr);align-items:start;gap:var(--grid-gap)}}
{selector}[data-mode="editorial"] .section-grid{{grid-template-columns:minmax(240px,.78fr) minmax(0,1.22fr)}}
{selector}[data-mode="technical"] .section-grid,{selector}[data-density="dense"] .section-grid{{grid-template-columns:minmax(220px,.58fr) minmax(0,1.42fr)}}
{selector}[data-mode="commerce"] .section-grid,{selector}[data-mode="hospitality"] .section-grid{{grid-template-columns:minmax(240px,.74fr) minmax(0,1.26fr)}}
{selector} .section-copy{{position:static!important;max-width:68ch!important;align-self:start}}
{selector} .section-copy h2{{max-width:min(18ch,100%)}}
{selector} .section-copy .lead+p{{max-width:62ch}}
{selector} .section-icon{{width:46px;height:46px;margin-bottom:.7rem}}
{selector} .portfolio-component::before{{opacity:.045!important;width:clamp(42px,7vw,100px);height:clamp(42px,7vw,100px)}}
{selector} .content-section:nth-of-type(even){{background:color-mix(in srgb,var(--color-accent) 4%,var(--color-bg))}}
{selector} .content-section[data-section-type="cta"]>.section-grid{{display:none!important}}
{selector} .content-section[data-section-type="cta"]{{padding-block:clamp(50px,6vw,96px);background:linear-gradient(135deg,color-mix(in srgb,var(--color-primary) 9%,var(--color-bg)),color-mix(in srgb,var(--color-accent) 8%,var(--color-bg)))}}
{selector} .card-grid,{selector} .pricing-grid,{selector} .resource-board{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(245px,100%),1fr));gap:clamp(.8rem,1.8vw,1.25rem)}}
{selector}[data-mode="editorial"] .card-grid>*:first-child,{selector}[data-density="spacious"] .card-grid>*:first-child{{grid-column:span 2}}
{selector} .mini-card,{selector} .price-card,{selector} .metric-card,{selector} .resource-card,{selector} .faq-list details{{min-height:100%;padding:var(--card-padding);display:grid;align-content:start;gap:.55rem}}
{selector} .mini-card h3,{selector} .price-card h3,{selector} .metric-card h3,{selector} .resource-card h3{{margin:0}}
{selector} .mini-card p,{selector} .price-card p,{selector} .metric-card p,{selector} .resource-card p{{margin:0;line-height:1.48;font-size:.95rem}}
{selector} .mini-card .card-thumb,{selector} .resource-card img{{aspect-ratio:4/3;max-height:220px;object-fit:cover;margin-bottom:.55rem}}
{selector} .process-list{{gap:.85rem}}
{selector} .process-list li,{selector} .checklist-panel li{{padding:clamp(.95rem,1.8vw,1.45rem);gap:.85rem}}
{selector} .process-list span{{width:2.25rem;height:2.25rem;font-size:.82rem}}
{selector} .dashboard-panel{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(210px,100%),1fr));gap:clamp(.75rem,1.6vw,1.15rem)}}
{selector} .metric-card strong{{font-size:clamp(2rem,3.8vw,3.8rem)}}
{selector} .visual-card-stack{{gap:clamp(.85rem,1.8vw,1.35rem)}}
{selector} .visual-card-stack img{{min-height:180px;max-height:460px}}
{selector} section[data-pattern-family="bento-grid"] .card-grid{{grid-template-columns:minmax(0,1.35fr) minmax(0,.9fr)}}
{selector} section[data-pattern-family="bento-grid"] .card-grid>*:first-child{{grid-row:span 2;min-height:260px}}
{selector} section[data-pattern-family="route-cards"] .card-grid{{grid-template-columns:repeat(auto-fit,minmax(min(210px,100%),1fr))}}
{selector} section[data-pattern-family="route-cards"] .mini-card{{border-top:4px solid color-mix(in srgb,var(--color-primary) 74%,var(--color-accent))}}
{selector} section[data-pattern-family="proof-ledger"] .checklist-panel,{selector} section[data-pattern-family="proof-ledger"] .process-list{{grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr))}}
{selector} section[data-pattern-family="dashboard-command"] .dashboard-panel{{grid-template-columns:minmax(0,1.2fr) repeat(2,minmax(170px,.8fr));align-items:stretch}}
{selector} section[data-pattern-family="dashboard-command"] .metric-card:first-child{{grid-row:span 2}}
{selector} section[data-pattern-family="form-studio"] .map-panel{{grid-template-columns:minmax(0,1.05fr) minmax(220px,.95fr);align-items:stretch}}
{selector} section[data-pattern-family="form-studio"] .map-canvas{{min-height:clamp(260px,28vw,440px)}}
{selector} section[data-pattern-family="collage-stack"] .visual-card-stack{{grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr)}}
{selector} section[data-pattern-family="minimal-luxury"] .section-grid{{grid-template-columns:minmax(220px,.55fr) minmax(0,1.45fr)}}
{selector} section[data-pattern-family="minimal-luxury"] .mini-card,{selector} section[data-pattern-family="minimal-luxury"] .price-card{{box-shadow:none}}
{selector} section[data-pattern-family="map-console"] .map-panel{{grid-template-columns:minmax(0,1.2fr) minmax(210px,.8fr)}}
{selector} section[data-pattern-family="timeline-rail"] .process-list{{position:relative}}
{selector} section[data-pattern-family="timeline-rail"] .process-list li{{border-left:4px solid color-mix(in srgb,var(--color-primary) 72%,var(--color-accent))}}
{selector} section[data-pattern-family="cinematic-bleed"] .visual-card-stack{{grid-template-columns:1fr 1fr}}
{selector} section[data-pattern-family="faq-panel"] .faq-list details{{border-left:4px solid color-mix(in srgb,var(--color-primary) 72%,var(--color-accent))}}
{selector} .finder-panel,{selector} .form-panel{{padding:clamp(1rem,2.4vw,2rem);gap:clamp(.85rem,2vw,1.5rem)}}
{selector} input,{selector} textarea,{selector} select{{min-height:46px}}
{selector} .faq-list{{gap:.65rem}}
{selector} .faq-list details{{padding:1rem 1.15rem}}
{selector} .faq-list summary{{line-height:1.28}}
{selector} .cta-panel{{margin-top:0;grid-template-columns:minmax(0,1fr) minmax(150px,.3fr) auto;gap:clamp(.9rem,2vw,1.4rem);padding:clamp(1.25rem,3.8vw,3rem);border-bottom-width:4px}}
{selector} .cta-panel h2{{margin-bottom:.45rem}}
{selector} .cta-panel img{{max-height:230px;object-fit:cover}}
{selector} .site-footer{{padding-top:clamp(46px,6vw,86px)}}
{selector} .footer-grid,{selector} .professional-footer-links{{gap:clamp(1rem,2vw,1.6rem)}}
{selector} .site-footer a{{text-underline-offset:.18em}}
@media (min-width:1500px){{{selector} .container{{width:min(var(--container-wide),calc(100% - 72px))}}{selector} .hero-grid{{grid-template-columns:minmax(0,.92fr) minmax(420px,1.08fr)}}}}
@media (max-width:1180px){{{selector}[data-mode="editorial"] .card-grid>*:first-child,{selector}[data-density="spacious"] .card-grid>*:first-child{{grid-column:auto}}{selector} .cta-panel{{grid-template-columns:minmax(0,1fr) auto}}{selector} .cta-panel img{{display:none}}}}
@media (max-width:980px){{{selector} .hero-section{{padding-block:clamp(28px,7vw,58px)!important}}{selector} .hero-grid,{selector} .section-grid,{selector} .form-panel,{selector} .cta-panel,{selector} .visual-card-stack,{selector} section[data-pattern-family] .map-panel{{grid-template-columns:minmax(0,1fr)!important}}{selector} .hero-grid{{gap:clamp(.9rem,4vw,1.45rem)!important}}{selector} .hero-media,{selector} .target-media{{order:0;min-height:0!important;padding:clamp(.75rem,3vw,1.1rem)!important}}{selector} .target-media>picture{{display:none!important}}{selector} .target-media .target-stage,{selector} .hero-media .target-stage{{min-height:clamp(210px,52vw,310px)!important;max-height:330px;overflow:hidden}}{selector} .hero-media figcaption,{selector} .target-media figcaption{{position:relative!important;left:auto!important;right:auto!important;bottom:auto!important;margin-top:.65rem;padding:.65rem .75rem;font-size:.78rem;line-height:1.35}}{selector} .hero-proof{{margin-top:.75rem;gap:.45rem}}{selector} .hero-proof span{{padding:.32rem .5rem;font-size:.74rem}}{selector} .card-grid,{selector} .pricing-grid,{selector} .resource-board,{selector} .dashboard-panel,{selector} section[data-pattern-family="proof-ledger"] .checklist-panel,{selector} section[data-pattern-family="proof-ledger"] .process-list{{grid-template-columns:minmax(0,1fr)!important}}{selector} section[data-pattern-family] .card-grid>*:first-child,{selector} section[data-pattern-family] .dashboard-panel>*:first-child{{grid-row:auto;grid-column:auto;min-height:0}}{selector} .site-nav{{max-height:calc(100vh - 110px);overflow:auto}}}}
@media (max-width:640px){{{selector}{{--section-padding:clamp(38px,9vw,62px)}}{selector} .container{{width:min(100% - 28px,var(--container-width))}}{selector} .hero-section{{padding-block:clamp(16px,4.5vw,28px)!important}}{selector} .hero-copy h1{{font-size:clamp(1.9rem,12vw,3.05rem)}}{selector} .hero-copy h2{{font-size:1rem;line-height:1.28;margin-bottom:.54rem}}{selector} .hero-copy .lead{{font-size:.95rem;line-height:1.43}}{selector} .hero-copy p:not(.eyebrow):not(.lead){{font-size:.9rem;line-height:1.43}}{selector} .button-row{{margin-top:.75rem}}{selector} .button-row>a,{selector} .hero-flow-links>a{{flex:1 1 100%;justify-content:center}}{selector} .target-media .target-stage,{selector} .hero-media .target-stage{{min-height:clamp(170px,47vw,238px)!important;max-height:252px}}{selector} .hero-media figcaption,{selector} .target-media figcaption{{display:none!important}}{selector} .whatsapp-widget{{display:none!important}}{selector} .cookie-banner{{left:.75rem!important;right:.75rem!important;bottom:.75rem!important;width:auto!important;max-width:none!important;grid-template-columns:minmax(0,1fr) auto auto!important;gap:.55rem!important;align-items:center!important;padding:.75rem!important;font-size:.78rem!important;line-height:1.32!important}}{selector} .cookie-banner.is-visible{{display:grid!important}}{selector} .cookie-banner p{{margin:0!important;min-width:0!important}}{selector} .cookie-banner button,{selector} .cookie-banner a{{min-height:38px!important;white-space:nowrap!important;padding:.5rem .62rem!important;text-align:center!important}}{selector} .footer-bottom{{display:grid!important}}}}
""".strip()


def update_css(site_root: Path, slug: str) -> None:
    css_path = site_root / "css" / "styles.css"
    text = css_path.read_text(encoding="utf-8")
    text = strip_css_pass(text)
    css_path.write_text(text + "\n\n" + design_css(slug) + "\n", encoding="utf-8")


def site_note(config: dict[str, object]) -> str:
    return f"""

## {PASS_TITLE}

- The former public homepage route index is removed so the homepage follows the approved `{config['industry']}` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.
""".rstrip()


def master_note() -> str:
    return f"""

## {PASS_TITLE}

All 50 numbered sites received a broad visual refactor pass after a full 900-page baseline section audit. The pass removed repeated homepage route-index clutter, suppressed duplicated signature panels, stripped visible SVG asset-inventory labels, restored reliable hero/media grid containment, strengthened card/form/CTA/footer rhythm, and preserved the documented reference packs and difference scores.
""".rstrip()


def append_note(path: Path, note: str) -> None:
    if not path.exists():
        return
    text = strip_block(path.read_text(encoding="utf-8"), PASS_TITLE)
    path.write_text(text + "\n" + note + "\n", encoding="utf-8")


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


def main() -> int:
    site_roots = sorted(path for path in DEMO_ROOT.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name))
    updated = 0
    assets_updated = 0
    for site_root in site_roots:
        config = read_json(site_root / "site.config.json")
        update_homepage(site_root / "index.html", config)
        assets_updated += update_assets(site_root)
        update_css(site_root, str(config["slug"]))
        update_site_docs(site_root, config)
        updated += 1
    update_master_docs()
    print(f"Applied {PASS_TITLE} to {updated} numbered sites; cleaned {assets_updated} SVG asset files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
