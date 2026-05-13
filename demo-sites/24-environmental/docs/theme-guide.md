# Theme Guide

## Anti-Template Rule

TerraMetric must feel like a standalone premium website for Environmental, Sustainability & Climate Services, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 07, 31, 41.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | impact evidence |
| Visual mood | Climate software with serious green, evidence dashboards, and enterprise clarity |
| Industry tone | evidence-led climate responsibility |
| Buyer psychology | accountability and measurable change |
| Trust style | impact and methodology proof |
| Conversion style | Primary-reference CTA hierarchy using Book Audit |
| Content density | medium |
| Image personality | Carbon dashboards, climate reports, data rooms |
| Level of formality | technical |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | A climate-accounting site with emissions dashboards, report proof, methodology panels, and audit CTAs |
| Commercial feeling | Primary-reference CTA hierarchy using Book Audit |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Palatino Linotype", Palatino, serif |
| Body font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Accent font role | "Trebuchet MS", Arial, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Carbon evidence cards and Climate software with serious green, evidence dashboards, and enterprise clarity |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f4fbf7, #083d31, #00a878, #083d31, #244bff |
| Surface style | Climate software with serious green, evidence dashboards, and enterprise clarity |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Carbon evidence cards with unique radius and border strength |
| Texture usage | Climate software with serious green, evidence dashboards, and enterprise clarity texture; no generic repeated decorative background |
| Dark/light balance | technical mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A climate-accounting site with emissions dashboards, report proof, methodology panels, and audit CTAs
- Brand mood: impact evidence
- Buyer psychology: accountability and measurable change
- Layout archetype: Climate data operating system
- Density: medium
- Shape language: Carbon evidence cards
- Surface/material: Climate software with serious green, evidence dashboards, and enterprise clarity
- Image system: Carbon dashboards, climate reports, data rooms
- Interaction model: Emissions dashboard hero
- CTA style: Primary-reference CTA hierarchy using Book Audit
- Pricing style: audit roadmap cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 07, 31, 41.

## Static Authorship Pass

This site folder is now treated as the editable static source for `TerraMetric`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Watershed` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

TerraMetric now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Watershed inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Audit`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `map` for `Terra`, shaped by `Climate data operating system`, `Carbon evidence cards`, `Impact metric filters, ESG report archive, audit route selector`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Terra` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
