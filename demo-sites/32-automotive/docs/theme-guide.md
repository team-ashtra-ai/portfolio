# Theme Guide

## Anti-Template Rule

MotorArc must feel like a standalone premium website for Automotive, Vehicles & Mobility Products, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 15, 39, 49.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | showroom performance |
| Visual mood | Automotive minimalism with cool greys, product focus, and restrained configurator energy |
| Industry tone | vehicle purchase confidence |
| Buyer psychology | purchase confidence and desire |
| Trust style | inventory and service proof |
| Conversion style | Primary-reference CTA hierarchy using Book Test Drive |
| Content density | spacious |
| Image personality | EV silhouettes, interiors, chargers, specification panels |
| Level of formality | dark |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | A vehicle showroom site with precise white space, car-card rhythm, finance paths, and test-drive CTAs |
| Commercial feeling | Primary-reference CTA hierarchy using Book Test Drive |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Aptos, "Segoe UI", system-ui, sans-serif |
| Body font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Accent font role | Constantia, Georgia, serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Precise vehicle cards and Automotive minimalism with cool greys, product focus, and restrained configurator energy |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f8f8f8, #111111, #d8dadd, #111111, #8a8f98 |
| Surface style | Automotive minimalism with cool greys, product focus, and restrained configurator energy |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Precise vehicle cards with unique radius and border strength |
| Texture usage | Automotive minimalism with cool greys, product focus, and restrained configurator energy texture; no generic repeated decorative background |
| Dark/light balance | dark mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A vehicle showroom site with precise white space, car-card rhythm, finance paths, and test-drive CTAs
- Brand mood: showroom performance
- Buyer psychology: purchase confidence and desire
- Layout archetype: Minimal EV showroom
- Density: spacious
- Shape language: Precise vehicle cards
- Surface/material: Automotive minimalism with cool greys, product focus, and restrained configurator energy
- Image system: EV silhouettes, interiors, chargers, specification panels
- Interaction model: Stark vehicle product hero
- CTA style: Primary-reference CTA hierarchy using Book Test Drive
- Pricing style: finance calculator cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 15, 39, 49.

## Static Authorship Pass

This site folder is now treated as the editable static source for `MotorArc`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Polestar` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

MotorArc now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Polestar inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Test Drive`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `split-index` for `Motor`, shaped by `Minimal EV showroom`, `Precise vehicle cards`, `Inventory filter, finance calculator, test-drive form`, and `dark` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Motor` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
