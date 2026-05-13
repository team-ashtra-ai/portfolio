# Theme Guide

## Anti-Template Rule

HarborLine must feel like a standalone premium website for Maritime, Shipping & Marine Services, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 01, 17, 41.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | marine operations |
| Visual mood | Maritime corporate clarity with pale blue, logistics forms, and route tracking |
| Industry tone | maritime operational assurance |
| Buyer psychology | cargo reliability and reach |
| Trust style | capacity and tracking proof |
| Conversion style | Primary-reference CTA hierarchy using Request Shipping |
| Content density | dense |
| Image personality | Ships, containers, ports, route maps, logistics docs |
| Level of formality | dark |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | A shipping site with ocean-blue service panels, cargo quote logic, port schedules, and tracking proof |
| Commercial feeling | Primary-reference CTA hierarchy using Request Shipping |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Aptos, "Segoe UI", system-ui, sans-serif |
| Body font role | Georgia, "Times New Roman", serif |
| Accent font role | Verdana, Geneva, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Cargo service cards and Maritime corporate clarity with pale blue, logistics forms, and route tracking |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #ecf8ff, #40b4e5, #9ad7f5, #003a5d, #003a5d |
| Surface style | Maritime corporate clarity with pale blue, logistics forms, and route tracking |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Cargo service cards with unique radius and border strength |
| Texture usage | Maritime corporate clarity with pale blue, logistics forms, and route tracking texture; no generic repeated decorative background |
| Dark/light balance | dark mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A shipping site with ocean-blue service panels, cargo quote logic, port schedules, and tracking proof
- Brand mood: marine operations
- Buyer psychology: cargo reliability and reach
- Layout archetype: Blue ocean logistics portal
- Density: dense
- Shape language: Cargo service cards
- Surface/material: Maritime corporate clarity with pale blue, logistics forms, and route tracking
- Image system: Ships, containers, ports, route maps, logistics docs
- Interaction model: Shipping route hero
- CTA style: Primary-reference CTA hierarchy using Request Shipping
- Pricing style: cargo quote cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 01, 17, 41.

## Static Authorship Pass

This site folder is now treated as the editable static source for `HarborLine`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Maersk` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

HarborLine now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Maersk inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Shipping`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `map` for `Port`, shaped by `Blue ocean logistics portal`, `Cargo service cards`, `Vessel filter, port schedule, cargo quote form`, and `dark` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Port` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
