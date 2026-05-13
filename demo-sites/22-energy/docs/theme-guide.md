# Theme Guide

## Anti-Template Rule

SunVault must feel like a standalone premium website for Energy, Power & Renewable Solutions, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 05, 29, 39.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | future savings |
| Visual mood | Minimal product marketing with stark surfaces, centered copy, and energy-product proof |
| Industry tone | renewable value clarity |
| Buyer psychology | cost reduction and resilience |
| Trust style | savings and assumptions proof |
| Conversion style | Primary-reference CTA hierarchy using Calculate Savings |
| Content density | medium |
| Image personality | Solar roofs, batteries, energy app panels |
| Level of formality | technical |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | A renewable energy product site with minimalist hero, savings modules, battery/solar cards, and direct calculator |
| Commercial feeling | Primary-reference CTA hierarchy using Calculate Savings |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Palatino Linotype", Palatino, serif |
| Body font role | Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Accent font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Product output cards and Minimal product marketing with stark surfaces, centered copy, and energy-product proof |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f7f7f7, #111111, #e82127, #111111, #bfc7d5 |
| Surface style | Minimal product marketing with stark surfaces, centered copy, and energy-product proof |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Product output cards with unique radius and border strength |
| Texture usage | Minimal product marketing with stark surfaces, centered copy, and energy-product proof texture; no generic repeated decorative background |
| Dark/light balance | technical mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A renewable energy product site with minimalist hero, savings modules, battery/solar cards, and direct calculator
- Brand mood: future savings
- Buyer psychology: cost reduction and resilience
- Layout archetype: Minimal energy product landing
- Density: medium
- Shape language: Product output cards
- Surface/material: Minimal product marketing with stark surfaces, centered copy, and energy-product proof
- Image system: Solar roofs, batteries, energy app panels
- Interaction model: Centered product hero
- CTA style: Primary-reference CTA hierarchy using Calculate Savings
- Pricing style: project output calculator
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 05, 29, 39.

## Static Authorship Pass

This site folder is now treated as the editable static source for `SunVault`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Tesla Energy` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

SunVault now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Tesla Energy inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Calculate Savings`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `split-index` for `Vault`, shaped by `Minimal energy product landing`, `Product output cards`, `Savings estimator, battery/solar toggle, project output counters`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Vault` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
