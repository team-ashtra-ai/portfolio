# Theme Guide

## Anti-Template Rule

HelixNova must feel like a standalone premium website for Life Sciences, Pharmaceuticals & Biotechnology, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 09, 19, 35.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | research-grade |
| Visual mood | TechBio with dark scientific grids, microscopy panels, and pipeline evidence |
| Industry tone | research-grade scientific authority |
| Buyer psychology | evidence and scientific credibility |
| Trust style | papers, pipeline, and ethics evidence |
| Conversion style | Primary-reference CTA hierarchy using Discuss Research |
| Content density | compact |
| Image personality | Cell imagery, robotic lab systems, data maps |
| Level of formality | technical |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | A research platform story built around AI discovery, phase tables, partner proof, and data-scale credibility |
| Commercial feeling | Primary-reference CTA hierarchy using Discuss Research |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Inter, ui-sans-serif, system-ui, sans-serif |
| Body font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Accent font role | Georgia, "Times New Roman", serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Pipeline evidence cards and TechBio with dark scientific grids, microscopy panels, and pipeline evidence |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #050709, #5cffb1, #2f6dff, #f3f7ff, #9cffd3 |
| Surface style | TechBio with dark scientific grids, microscopy panels, and pipeline evidence |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Pipeline evidence cards with unique radius and border strength |
| Texture usage | TechBio with dark scientific grids, microscopy panels, and pipeline evidence texture; no generic repeated decorative background |
| Dark/light balance | technical mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A research platform story built around AI discovery, phase tables, partner proof, and data-scale credibility
- Brand mood: research-grade
- Buyer psychology: evidence and scientific credibility
- Layout archetype: Scientific operating system dossier
- Density: compact
- Shape language: Pipeline evidence cards
- Surface/material: TechBio with dark scientific grids, microscopy panels, and pipeline evidence
- Image system: Cell imagery, robotic lab systems, data maps
- Interaction model: AI biology lab hero
- CTA style: Primary-reference CTA hierarchy using Discuss Research
- Pricing style: trial eligibility tiers
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 09, 19, 35.

## Static Authorship Pass

This site folder is now treated as the editable static source for `HelixNova`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Recursion` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

HelixNova now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Recursion inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Discuss Research`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `split-index` for `Helix`, shaped by `Scientific operating system dossier`, `Pipeline evidence cards`, `Pipeline tabs, publication filters, trial eligibility toggle`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Helix` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
