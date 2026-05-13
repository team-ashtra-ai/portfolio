#!/usr/bin/env python3
"""Apply portfolio-wide visual QA fixes and section-copy polish."""

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

GENERIC_CARD_LABELS = {
    "Prepare",
    "Reassure",
    "Continue",
    "Invitation",
    "Discretion",
    "Request",
}

SECTION_TONES = {
    "problem": ("friction", "risk", "decision pressure"),
    "solution": ("promise", "change", "outcome"),
    "services": ("scope", "fit", "route"),
    "process": ("start", "review", "continue"),
    "pricing": ("fit", "scope", "terms"),
    "trust": ("evidence", "standard", "confidence"),
    "results": ("before", "after", "proof"),
    "reviews": ("situation", "experience", "change"),
    "profiles": ("role", "credibility", "handoff"),
    "resources": ("topic", "use", "next route"),
    "contact": ("details", "timing", "reply"),
    "utility": ("policy", "access", "recovery"),
    "faq": ("question", "answer", "next step"),
    "cta": ("ready", "details", "response"),
    "editorial": ("context", "judgment", "direction"),
}

CTA_ACTIONS = {
    "book appointment": "book an appointment",
    "discuss research": "discuss the research fit",
    "book consultation": "book a consultation",
    "request it audit": "request an IT audit",
    "schedule demo": "schedule a demo",
    "check coverage": "check coverage",
    "request audit": "request an audit",
    "plan dashboard": "plan a dashboard",
    "book advisor call": "book an advisor call",
    "request quote": "request a quote",
    "send brief": "send a brief",
    "book trial": "book a trial",
    "start hiring": "start hiring",
    "get valuation": "get a valuation",
    "request estimate": "request an estimate",
    "discuss project": "discuss the project",
    "start design": "start the design",
    "send rfq": "send an RFQ",
    "ask engineer": "ask an engineer",
    "calculate savings": "calculate savings",
    "request service": "request service",
    "book audit": "book an audit",
    "plan visit": "plan a visit",
    "request trade info": "request trade information",
    "reserve table": "reserve a table",
    "check availability": "check availability",
    "plan trip": "plan a trip",
    "book ride": "book a ride",
    "book test drive": "book a test drive",
    "request charter": "request a charter",
    "request shipping": "request shipping",
    "visit shop": "visit the shop",
    "browse market": "browse the market",
    "shop collection": "shop the collection",
    "build routine": "build a routine",
    "advertise with us": "advertise with the team",
    "view tickets": "view tickets",
    "subscribe": "subscribe",
    "send campaign brief": "send a campaign brief",
    "start project": "start the project",
    "join class": "join a class",
    "enquire date": "enquire about a date",
    "start request": "start a request",
    "donate today": "donate today",
    "book visit": "book a visit",
    "request private access": "request private access",
    "book appearance": "book an appearance",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=False)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def human(value: str) -> str:
    value = value.replace("-", " ").replace("_", " ").strip()
    return re.sub(r"\s+", " ", value).title()


def sentence(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    if value and value[-1] not in ".!?":
        value += "."
    return value


def brand_from_html(text: str, config: dict[str, object]) -> str:
    match = re.search(r"<a class=\"brand\"[^>]*>.*?<strong>(.*?)</strong>", text, flags=re.S)
    if match:
        return re.sub(r"<.*?>", "", match.group(1)).strip()
    return str(config.get("siteName", "This site"))


def page_from_file(path: Path, config: dict[str, object]) -> str:
    file = path.name
    for page in config.get("pages", []):
        if isinstance(page, dict) and page.get("file") == file:
            return str(page.get("name", human(path.stem)))
    return human(path.stem)


def compact_industry(config: dict[str, object]) -> str:
    industry = str(config.get("industry", "visitors")).lower()
    first = industry.split("&")[0].split(",")[0].strip()
    return first or industry


def full_industry(config: dict[str, object]) -> str:
    return str(config.get("industry", "visitors")).lower()


def design_field(config: dict[str, object], key: str, fallback: str = "") -> str:
    passport = config.get("designPassport", {})
    if isinstance(passport, dict) and passport.get(key):
        return str(passport[key])
    return str(config.get(key, fallback))


def buyer_driver(config: dict[str, object]) -> str:
    return design_field(config, "buyerPsychology", "a clear decision").lower()


def layout_signature(config: dict[str, object]) -> str:
    return str(config.get("layoutSignature", "site journey")).lower()


def premium_direction(config: dict[str, object]) -> str:
    return sentence(str(config.get("premiumDirection", "A focused site experience")))


def decision_phrase(config: dict[str, object]) -> str:
    cta = str(config.get("cta", "contact us")).lower()
    if cta in CTA_ACTIONS:
        return CTA_ACTIONS[cta]
    if cta.startswith(("book", "request", "schedule", "join", "start", "browse", "shop", "donate", "buy")):
        return cta
    return f"choose whether to {cta}"


def lead_copy(
    brand: str,
    config: dict[str, object],
    page: str,
    section: str,
    section_type: str,
) -> str:
    industry = compact_industry(config)
    action = decision_phrase(config)
    mode = str(config.get("themeMode", "premium"))
    driver = buyer_driver(config)
    signature = layout_signature(config)
    lower = section.lower()
    if section == "Hero":
        return f"{page} opens as a clear {industry} decision hub: what {brand} offers, who it helps, why it matters, and which route to take first."
    if section_type == "cta" or lower == "cta":
        return f"{brand} closes the {page.lower()} route with a clear action, a quick reminder of the value, and a low-friction way to {action}."
    if section_type == "contact":
        return f"{section} makes the contact path concrete: what to send, how the response works, and what {brand} needs before visitors {action}."
    if section_type == "pricing":
        return f"{section} makes commercial comparison easier by showing fit, scope, and terms before {industry} visitors ask for the next step."
    if section_type == "process":
        return f"{section} explains the operating sequence so visitors can see how the first request becomes a clear recommendation and follow-up."
    if section_type == "resources":
        return f"{section} gives researching visitors a practical route into guides, checklists, and comparison material without leaving the site structure."
    if section_type == "profiles":
        return f"{section} introduces the people, roles, or specialist credibility behind {brand} so the decision feels less anonymous."
    if section_type == "reviews":
        return f"{section} converts customer proof into a useful buying signal: the problem, the experience, and what changed afterward."
    if section_type == "utility":
        return f"{section} keeps the support layer readable, with policy, access, and recovery information shaped for real visitors."
    if section_type == "services":
        return f"{section} explains the practical scope, best-fit situations, and expected outcome so {industry} visitors can compare options without decoding jargon."
    if section_type == "trust":
        return f"{section} gives the proof layer for {page.lower()}: standards, evidence, and reassurance that make the next decision feel grounded."
    if section_type == "results":
        return f"{section} shows what changes after the work: clearer decisions, visible progress, and proof points that connect the offer to real outcomes."
    if section_type == "problem":
        return f"{section} frames the pressure behind the visit, then connects it to a practical path visitors can recognise and act on."
    if section_type == "solution":
        return f"{section} defines the better state {brand} is built to create, with enough detail to make the promise believable."
    if section_type == "faq":
        return f"{section} handles buying doubts directly so visitors can understand timing, fit, limits, and the safest next step."
    return f"{section} adds {mode} context to the {page.lower()} route, using the {signature} structure to support {driver} before visitors choose a next step."


def body_copy(
    brand: str,
    config: dict[str, object],
    page: str,
    section: str,
    section_type: str,
) -> str:
    industry = compact_industry(config)
    action = decision_phrase(config)
    premium = sentence(str(config.get("premiumDirection", "")))
    card_style = str(config.get("cardStyle", "section cards")).lower()
    driver = buyer_driver(config)
    lower = section.lower()
    if section == "Hero":
        return f"The first screen combines positioning, proof, primary action, and fast internal navigation, so people can act immediately or compare the rest of the {page.lower()} route with context."
    if section_type == "cta" or lower == "cta":
        return f"Visitors who are ready can use the primary action. Visitors who are still comparing can scan the section links, proof, and support routes before they {action}."
    if section_type == "contact":
        return f"The section reduces contact friction by naming the channel, expected detail, privacy path, and response expectation instead of dropping visitors into a generic form."
    if section_type == "pricing":
        return f"The layout keeps price-sensitive decisions honest: it separates starting scope, fuller delivery, and ongoing support so the visitor can ask a sharper question."
    if section_type == "process":
        return f"The steps are written from the visitor side: what they do first, what {brand} clarifies, what they receive, and how support continues."
    if section_type == "resources":
        return f"Each resource behaves like a useful internal link, giving cold and warm visitors a way to learn, compare, and return to the action path."
    if section_type == "profiles":
        return f"The copy ties names, roles, credentials, or availability back to the decision on the page instead of treating profiles as decorative biographies."
    if section_type == "reviews":
        return f"Proof stays believable by focusing on situation, service experience, and practical change rather than vague praise or unsupported results."
    if section_type == "utility":
        return f"Utility content is kept plain and scannable so legal, accessibility, sitemap, and recovery routes feel like part of the experience, not an afterthought."
    if section_type == "services":
        return f"The section keeps the offer concrete: what is included, who it is best for, what decision it supports, and which linked route gives the deeper detail."
    if section_type == "trust":
        return f"Instead of relying on vague claims, {brand} presents visible standards, process cues, and proof artifacts that help {industry} visitors judge fit."
    if section_type == "results":
        return f"The layout connects before-and-after thinking with measured outcomes, making the result easy to scan without promising what the business cannot guarantee."
    if section_type == "problem":
        return f"The copy avoids blame and panic. It shows the common friction, the practical consequence, and the calmer route {brand} uses to move people forward."
    if section_type == "solution":
        return f"{premium} The section grounds that direction in concrete benefits, visible tradeoffs, and a next route visitors can use when the promise feels relevant."
    if section_type == "faq":
        return f"Answers are short by design: enough to remove hesitation, not so much that the page turns into documentation before the visitor can act."
    return f"{brand} uses {card_style} and focused copy to make the decision easier to scan, aligning the section with {driver} rather than filling space."


def card_set(
    brand: str,
    config: dict[str, object],
    page: str,
    section: str,
    section_type: str,
) -> list[tuple[str, str]]:
    action = decision_phrase(config)
    industry = full_industry(config)
    driver = buyer_driver(config)
    card_style = str(config.get("cardStyle", "cards")).lower()
    tones = SECTION_TONES.get(section_type, SECTION_TONES["editorial"])
    if str(config.get("themeMode")) == "luxury":
        return [
            ("Invitation", f"{section} is framed with restraint, enough detail to feel considered, and a private route forward."),
            ("Provenance", f"The proof appears through standards, context, and carefully chosen visual evidence rather than volume."),
            ("Private Next Step", f"The next action explains what to send, when to expect a response, and how access is handled."),
        ]
    if section_type == "problem":
        return [
            ("Pressure", f"{section} names the real friction visitors bring to the {page.lower()} route, so the page feels relevant before any claim is made."),
            ("Consequence", f"The copy connects that friction to practical risk, delay, confusion, or missed opportunity without exaggerating it."),
            ("Safer Step", f"The final cue moves visitors toward a clearer route instead of leaving them with the problem alone."),
        ]
    if section_type == "solution":
        return [
            ("Better State", f"{section} defines what becomes clearer, easier, or safer when {brand} is the chosen route."),
            ("Practical Gain", f"The benefit is tied to {driver}, not a vague quality claim."),
            ("Proof Route", f"Visitors get a linked path to compare the promise against services, standards, or examples."),
        ]
    if section_type == "services":
        return [
            ("Best Fit", f"Who should use {section.lower()} and when it belongs in the {page.lower()} journey."),
            ("What Changes", f"The practical benefit visitors should expect after choosing this route."),
            ("Deeper Route", f"Where to compare details, pricing, support, or contact options before committing."),
        ]
    if section_type == "process":
        return [
            ("Start", f"How visitors begin this route and what detail is useful at the first step."),
            ("Clarify", f"What {brand} reviews, filters, or explains before recommending the next move."),
            ("Continue", f"What the visitor receives afterward, including support, proof, or a handoff to the next page."),
        ]
    if section_type == "pricing":
        return [
            ("Fit", f"Who the offer is for, which scope it suits, and when a different route may be better."),
            ("Scope", f"What is included clearly enough for {industry} visitors to compare value without hidden jargon."),
            ("Terms", f"The practical details that should be confirmed before someone asks to {action}."),
        ]
    if section_type == "trust":
        return [
            ("Evidence", f"Visible proof that helps visitors believe the claims behind {section.lower()}."),
            ("Standard", f"The quality, safety, or operating expectation this section makes explicit."),
            ("Reassurance", f"What becomes clearer before someone decides whether to {action}."),
        ]
    if section_type == "results":
        return [
            ("Before", f"The uncertainty, delay, or missed opportunity visitors bring into {section.lower()}."),
            ("After", f"The clearer, safer, or more valuable state {brand} is designed to support."),
            ("Proof", f"The visible cue that connects {section.lower()} to a believable decision, not a loose claim."),
        ]
    if section_type == "reviews":
        return [
            ("Situation", f"What the visitor needed before choosing {brand}, written with enough context to feel real."),
            ("Experience", f"How the service, product, or support felt during the process, not just that it was good."),
            ("Change", f"What became easier to decide, complete, buy, book, or trust after the interaction."),
        ]
    if section_type == "profiles":
        return [
            ("Role", f"The person, team, or specialist function connected to {section.lower()} is easy to understand."),
            ("Credibility", f"Credentials, responsibilities, or availability are tied to the visitor's decision, not listed for decoration."),
            ("Handoff", f"The section explains how to move from profile interest to a practical conversation or booking path."),
        ]
    if section_type == "resources":
        return [
            ("Guide", f"A useful entry point for visitors who need more context before they {action}."),
            ("Checklist", f"A scannable comparison aid that makes research usable before the next decision."),
            ("Questions", f"A route back to support, services, or contact when the visitor is ready to act."),
        ]
    if section_type == "contact":
        return [
            ("Details", f"What information helps {brand} respond with a useful answer instead of a generic reply."),
            ("Timing", f"How the visitor should think about response, urgency, location, or availability."),
            ("Reply", f"The expected next message keeps scope, timing, and the first practical step clear."),
        ]
    if section_type == "utility":
        return [
            ("Policy", f"The rules, notices, or accessibility details are written in plain language."),
            ("Access", f"The route helps visitors recover, navigate, or understand the site without contacting support first."),
            ("Recovery", f"Links and support cues keep the experience useful even on legal, sitemap, thanks, or error pages."),
        ]
    if section_type == "cta" or section.lower() == "cta":
        return [
            ("Ready", f"Use the primary CTA when the fit is clear and timing matters."),
            ("Compare", f"Review linked proof, questions, and support routes if more context is needed."),
            ("Response", f"{brand} keeps the next reply focused on scope, timing, and the right first step."),
        ]
    return [
        (human(tones[0]), f"{section} gives the page a specific angle instead of repeating the navigation label."),
        (human(tones[1]), f"The {card_style} show what to compare, what to avoid, and what matters most for {industry} visitors."),
        (human(tones[2]), f"The final cue points to a useful internal route so the section keeps the journey moving."),
    ]


def replace_lead_and_body(block: str, lead: str, body: str) -> str:
    block = re.sub(r'(<p class="lead">).*?(</p>)', rf"\1{esc(lead)}\2", block, count=1, flags=re.S)
    block = re.sub(
        r'(<p class="lead">.*?</p>\s*)<p>(?!(?:<|$)).*?</p>',
        rf"\1<p>{esc(body)}</p>",
        block,
        count=1,
        flags=re.S,
    )
    return block


def replace_generic_cards(block: str, cards: list[tuple[str, str]]) -> str:
    card_index = 0

    def next_card() -> tuple[str, str]:
        nonlocal card_index
        card = cards[card_index % len(cards)]
        card_index += 1
        return card

    def h3_pair(match: re.Match[str]) -> str:
        heading = match.group(1)
        if heading not in GENERIC_CARD_LABELS:
            return match.group(0)
        title, text = next_card()
        return f"<h3>{esc(title)}</h3><p>{esc(text)}</p>"

    block = re.sub(
        r"<h3>(Prepare|Reassure|Continue|Invitation|Discretion|Request)</h3><p>.*?</p>",
        h3_pair,
        block,
        flags=re.S,
    )

    card_index = 0

    def figcaption(match: re.Match[str]) -> str:
        label = match.group(1)
        if label not in GENERIC_CARD_LABELS:
            return match.group(0)
        title, text = next_card()
        return f"<figcaption><strong>{esc(title)}</strong>{esc(text)}</figcaption>"

    block = re.sub(
        r"<figcaption><strong>(Prepare|Reassure|Continue|Invitation|Discretion|Request)</strong>.*?</figcaption>",
        figcaption,
        block,
        flags=re.S,
    )

    for title, original in zip([card[0] for card in cards], ["Prepare", "Reassure", "Continue"]):
        block = block.replace(f"<button type=\"button\">{original}</button>", f"<button type=\"button\">{esc(title)}</button>", 1)
    return block


def replace_visual_microcopy(
    block: str,
    brand: str,
    config: dict[str, object],
    page: str,
    section: str,
    section_type: str,
    cards: list[tuple[str, str]],
) -> str:
    card_index = 0

    def next_card() -> tuple[str, str]:
        nonlocal card_index
        card = cards[card_index % len(cards)]
        card_index += 1
        return card

    def h3_pair(match: re.Match[str]) -> str:
        title, text = next_card()
        return f"{match.group(1)}<h3>{esc(title)}</h3><p>{esc(text)}</p>{match.group(2)}"

    pair_patterns = [
        r'(<article class="mini-card"[^>]*>(?:\s*<img\b[^>]*>\s*)?)<h3>.*?</h3><p>.*?</p>(</article>)',
        r'(<li><span>.*?</span>)<h3>.*?</h3><p>.*?</p>(</li>)',
        r'(<li><span></span><div>)<h3>.*?</h3><p>.*?</p>(</div></li>)',
        r'(<article>)<h3>.*?</h3><p>.*?</p>(</article>)',
    ]
    for pattern in pair_patterns:
        card_index = 0
        block = re.sub(pattern, h3_pair, block, flags=re.S)

    card_index = 0

    def figcaption(match: re.Match[str]) -> str:
        title, text = next_card()
        return f"<figcaption><strong>{esc(title)}</strong>{esc(text)}</figcaption>"

    block = re.sub(r"<figcaption><strong>.*?</strong>.*?</figcaption>", figcaption, block, flags=re.S)

    card_index = 0

    def metric_replace(match: re.Match[str]) -> str:
        _, text = next_card()
        return f"{match.group(1)}<p>{esc(text)}</p>{match.group(2)}"

    block = re.sub(
        r'(<article class="metric-card">.*?<strong>.*?</strong>)<p>.*?</p>(</article>)',
        metric_replace,
        block,
        flags=re.S,
    )

    card_index = 0

    def resource_replace(match: re.Match[str]) -> str:
        label = re.sub(r"<.*?>", "", match.group(2)).strip().lower() or "resource"
        _, text = next_card()
        title = f"{brand} {section.lower()} {label}"
        return f"{match.group(1)}<h3>{esc(title)}</h3><p>{esc(text)}</p>{match.group(3)}"

    block = re.sub(
        r'(<article class="resource-card">.*?<span>(.*?)</span>)<h3>.*?</h3><p>.*?</p>(<a\b)',
        resource_replace,
        block,
        flags=re.S,
    )

    card_index = 0

    def price_replace(match: re.Match[str]) -> str:
        _, text = next_card()
        return f"{match.group(1)}<p>{esc(text)}</p>{match.group(2)}"

    block = re.sub(
        r'(<article class="price-card(?: featured)?"><h3>.*?</h3>)<p>.*?</p>(<strong>.*?</strong></article>)',
        price_replace,
        block,
        flags=re.S,
    )

    block = re.sub(r'alt="[^"]* visual cue for ([^"]+)"', rf'alt="{esc(brand)} visual cue for \1"', block)
    return block


def replace_generic_panel_copy(
    block: str,
    brand: str,
    config: dict[str, object],
    page: str,
    section: str,
    section_type: str,
    cards: list[tuple[str, str]],
) -> str:
    action = decision_phrase(config)
    card_words = ", ".join(card[0].lower() for card in cards[:2])
    panel_copy = (
        f"{brand} structures {section.lower()} around {card_words}, and a clear next route "
        f"so visitors can compare the block quickly before they {action}."
    )
    if section_type == "cta" or section == "CTA":
        panel_copy = "The final block keeps the choice simple: act now, compare one more proof route, or send enough detail for a focused response."
    elif section_type == "contact":
        panel_copy = f"{brand} keeps {section.lower()} practical: send the key details, choose the right contact route, and know what kind of reply to expect."
    elif section_type == "pricing":
        panel_copy = f"{brand} frames {section.lower()} around fit, scope, and terms so visitors can compare cost without losing the outcome."

    generic_patterns = [
        rf"<p>{re.escape(brand)} turns .*?</p>",
        rf"<p>{re.escape(brand)} presents .*?</p>",
        r"<p>Plain language, visible reassurance, and practical details make .*?</p>",
        r"<p>Visitors leave with .*?</p>",
        r"<p>Primary-reference resource rhythm for .*?</p>",
    ]
    for pattern in generic_patterns:
        block = re.sub(pattern, f"<p>{esc(panel_copy)}</p>", block, flags=re.S)

    button_markup = "".join(f'<button type="button">{esc(title)}</button>' for title, _ in cards[:3])
    block = re.sub(
        r'(<div class="[^"]*\bfinder-panel\b[^"]*"[^>]*><p>).*?(</p><div>).*?(</div><a\b)',
        rf"\1{esc(panel_copy)}\2{button_markup}\3",
        block,
        flags=re.S,
    )

    signature_copy = (
        f"Select the closest route and {brand} keeps the next step, proof, and follow-up expectation aligned with "
        f"{buyer_driver(config)}."
    )
    block = re.sub(
        r'(<div class="[^"]*\bsignature-panel\b[^"]*"[^>]*>.*?<h3>.*?</h3>\s*)<p>.*?</p>',
        rf"\1<p>{esc(signature_copy)}</p>",
        block,
        flags=re.S,
    )

    cta_panel_copy = (
        f"{premium_direction(config)} {page} ends with a direct path to {action}, plus enough context for visitors who still need to compare."
    )
    block = re.sub(
        r'(<div class="[^"]*\bcta-panel\b[^"]*"[^>]*>\s*<div>.*?<h2>.*?</h2>\s*)<p>.*?</p>',
        rf"\1<p>{esc(cta_panel_copy)}</p>",
        block,
        flags=re.S,
    )
    return block


def transform_section(
    block: str,
    brand: str,
    config: dict[str, object],
    page: str,
) -> str:
    section_match = re.search(r'data-section="([^"]+)"', block)
    if not section_match:
        return block
    section = section_match.group(1)
    type_match = re.search(r'data-section-type="([^"]+)"', block)
    section_type = type_match.group(1) if type_match else "editorial"
    if section == "CTA":
        block = block.replace("<h2>CTA</h2>", f"<h2>{esc(config.get('cta', 'Next Step'))}</h2>")
    lead = lead_copy(brand, config, page, section, section_type)
    body = body_copy(brand, config, page, section, section_type)
    block = replace_lead_and_body(block, lead, body)
    cards = card_set(brand, config, page, section, section_type)
    block = replace_generic_cards(block, cards)
    block = replace_visual_microcopy(block, brand, config, page, section, section_type, cards)
    block = replace_generic_panel_copy(block, brand, config, page, section, section_type, cards)
    return block


def update_html_page(path: Path, config: dict[str, object]) -> None:
    text = path.read_text(encoding="utf-8")
    brand = brand_from_html(text, config)
    page = page_from_file(path, config)

    def section_replace(match: re.Match[str]) -> str:
        return transform_section(match.group(0), brand, config, page)

    text = re.sub(r"<section\b[^>]*data-section=\"[^\"]+\"[^>]*>.*?</section>", section_replace, text, flags=re.S)
    path.write_text(text, encoding="utf-8")


def visual_polish_css(slug: str) -> str:
    selector = f"body.theme-{slug}"
    return f"""
/* Portfolio Visual QA Pass - 2026-05-12: section screenshots, layout polish, visible reusable blocks. */
{selector}{{overflow-x:hidden}}
{selector} .portfolio-component,{selector} .content-section{{content-visibility:visible!important;contain:none!important;contain-intrinsic-size:auto!important}}
{selector} .reveal-ready{{opacity:1!important;transform:none!important}}
{selector} .container,{selector} .hero-grid,{selector} .section-grid,{selector} .card-grid,{selector} .dashboard-panel,{selector} .visual-card-stack,{selector} .map-panel,{selector} .cta-panel{{min-width:0;max-width:100%}}
{selector} .section-grid>*,{selector} .hero-grid>*,{selector} .card-grid>*,{selector} .visual-card-stack>*,{selector} .dashboard-panel>*{{min-width:0}}
{selector} h1,{selector} h2,{selector} h3{{text-wrap:balance;overflow-wrap:break-word;word-break:normal;hyphens:manual}}
{selector} p,{selector} li,{selector} a,{selector} small,{selector} span{{overflow-wrap:break-word;word-break:normal;hyphens:manual}}
{selector} .mini-card,{selector} .price-card,{selector} .metric-card,{selector} .resource-card,{selector} .finder-panel,{selector} .faq-list details{{overflow-wrap:break-word;word-break:normal;min-width:0}}
{selector} .mini-card .card-thumb,{selector} .resource-card img,{selector} .visual-card-stack img,{selector} .cta-panel img{{max-width:100%;min-width:0;object-fit:cover}}
{selector} .visual-card-stack figcaption strong{{display:block;margin-bottom:.25rem}}
{selector} .process-list li{{grid-template-columns:auto minmax(0,1fr)}}
{selector} .map-list{{grid-template-columns:repeat(auto-fit,minmax(min(180px,100%),1fr))}}
{selector} .button,{selector} .nav-cta,{selector} .text-link{{white-space:normal}}
{selector} .disclaimer{{position:relative;z-index:1}}
{selector} .whatsapp-widget{{max-width:calc(100vw - 1.5rem)}}
{selector} .whatsapp-button{{max-width:100%;min-width:0}}
@media (max-width:1180px){{{selector} .card-grid,{selector} .pricing-grid,{selector} .resource-board{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:760px){{{selector} .hero-grid,{selector} .section-grid,{selector} .form-panel,{selector} .cta-panel,{selector} .visual-card-stack,{selector} .dashboard-panel,{selector} .pricing-grid,{selector} .resource-board{{grid-template-columns:minmax(0,1fr)!important}}{selector} .card-grid{{grid-template-columns:minmax(0,1fr)!important;display:grid!important;overflow:visible!important}}{selector} .hero-copy,{selector} .section-copy{{width:100%!important;max-width:100%!important}}{selector} .button-row,{selector} .hero-atlas-links,{selector} .hero-proof{{max-width:100%}}{selector} .button-row>a,{selector} .hero-atlas-links>a{{flex:1 1 min(150px,100%)}}}}
""".strip()


def update_css(site_root: Path, slug: str) -> None:
    path = site_root / "css" / "styles.css"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n?/\* Portfolio Visual QA Pass - 2026-05-12:.*", "", text, flags=re.S)
    path.write_text(text.rstrip() + "\n\n" + visual_polish_css(slug) + "\n", encoding="utf-8")


def pack_note(config: dict[str, object]) -> str:
    return f"""

## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `{config['siteName']}` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
""".rstrip()


def update_pack_docs(site_root: Path, config: dict[str, object]) -> None:
    note = pack_note(config)
    for rel in REQUIRED_PACK_FILES:
        path = site_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"\n## Portfolio Visual QA Pass - 2026-05-12\n.*", "", text, flags=re.S)
        path.write_text(text.rstrip() + "\n" + note + "\n", encoding="utf-8")


def master_note() -> str:
    return """

## Portfolio Visual QA Pass - 2026-05-12

The 50-site portfolio received a section-level visual QA polish pass across all numbered site pages. The update improves screenshot readiness, visible reusable section states, responsive wrapping, repeated card copy, CTA labeling, and section-specific narrative clarity without changing the approved inspiration reference mix or reducing cross-site diversity.
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
        text = re.sub(r"\n## Portfolio Visual QA Pass - 2026-05-12\n.*", "", text, flags=re.S)
        path.write_text(text.rstrip() + "\n" + master_note() + "\n", encoding="utf-8")


def main() -> int:
    site_roots = sorted(path for path in DEMO_ROOT.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name))
    pages = 0
    for site_root in site_roots:
        config = read_json(site_root / "site.config.json")
        for html_path in sorted(site_root.glob("*.html")):
            update_html_page(html_path, config)
            pages += 1
        update_css(site_root, str(config["slug"]))
        update_pack_docs(site_root, config)
    update_master_docs()
    print(f"Applied portfolio visual polish to {pages} pages across {len(site_roots)} sites.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
