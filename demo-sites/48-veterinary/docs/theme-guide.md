# Theme Guide

## Anti-Template Rule

PawHealth must feel like a standalone premium website for Pets, Animals & Veterinary Services, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 05, 15, 31.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | compassionate urgent |
| Visual mood | Veterinary care with warm clinic colours, rounded forms, and friendly triage |
| Industry tone | compassionate veterinary care |
| Buyer psychology | care and quick triage |
| Trust style | safety and care proof |
| Conversion style | Primary-reference CTA hierarchy using Book Visit |
| Content density | practical |
| Image personality | Clinic rooms, pets, care teams, appointment panels |
| Level of formality | care |
| Level of emotion | high |
| Level of technical detail | moderate |
| Premium feeling | A veterinary site with warm urgent-care modules, appointment paths, team proof, and symptom routing |
| Commercial feeling | Primary-reference CTA hierarchy using Book Visit |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Arial Narrow", Arial, sans-serif |
| Body font role | Georgia, "Times New Roman", serif |
| Accent font role | "Courier New", ui-monospace, monospace |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Rounded care cards and Veterinary care with warm clinic colours, rounded forms, and friendly triage |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #fff7ef, #256a5e, #ffb199, #256a5e, #21413a |
| Surface style | Veterinary care with warm clinic colours, rounded forms, and friendly triage |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Rounded care cards with unique radius and border strength |
| Texture usage | Veterinary care with warm clinic colours, rounded forms, and friendly triage texture; no generic repeated decorative background |
| Dark/light balance | care mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A veterinary site with warm urgent-care modules, appointment paths, team proof, and symptom routing
- Brand mood: compassionate urgent
- Buyer psychology: care and quick triage
- Layout archetype: Modern clinic care flow
- Density: practical
- Shape language: Rounded care cards
- Surface/material: Veterinary care with warm clinic colours, rounded forms, and friendly triage
- Image system: Clinic rooms, pets, care teams, appointment panels
- Interaction model: Warm appointment hero
- CTA style: Primary-reference CTA hierarchy using Book Visit
- Pricing style: care plan cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 05, 15, 31.

## Static Authorship Pass

This site folder is now treated as the editable static source for `PawHealth`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `hospitality` footer pattern for the `Modern Animal` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

PawHealth now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Modern Animal inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Visit`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Paw`, shaped by `Modern clinic care flow`, `Rounded care cards`, `Emergency symptom helper, appointment form, care guide filter`, and `care` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Paw` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
