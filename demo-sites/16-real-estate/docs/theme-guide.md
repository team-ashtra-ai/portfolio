# Theme Guide

## Anti-Template Rule

UrbanNest must feel like a standalone premium website for Real Estate, Property & Land Services, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 23, 33, 49.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | local visual |
| Visual mood | Property editorial with quiet type, generous imagery, and thin-rule listings |
| Industry tone | local market confidence |
| Buyer psychology | market confidence and discovery |
| Trust style | market and area proof |
| Conversion style | Primary-reference CTA hierarchy using Get Valuation |
| Content density | spacious |
| Image personality | Modern homes, interiors, floor plans, neighbourhood details |
| Level of formality | formal |
| Level of emotion | controlled |
| Level of technical detail | moderate |
| Premium feeling | A real-estate editorial site with architecture-led listings, sparse navigation, area guides, and valuation flow |
| Commercial feeling | Primary-reference CTA hierarchy using Get Valuation |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Trebuchet MS", Arial, sans-serif |
| Body font role | Arial, Helvetica, sans-serif |
| Accent font role | Aptos, Calibri, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Thin-rule listing cards and Property editorial with quiet type, generous imagery, and thin-rule listings |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #fbfaf7, #111111, #8a8f83, #111111, #c7b299 |
| Surface style | Property editorial with quiet type, generous imagery, and thin-rule listings |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Thin-rule listing cards with unique radius and border strength |
| Texture usage | Property editorial with quiet type, generous imagery, and thin-rule listings texture; no generic repeated decorative background |
| Dark/light balance | professional mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A real-estate editorial site with architecture-led listings, sparse navigation, area guides, and valuation flow
- Brand mood: local visual
- Buyer psychology: market confidence and discovery
- Layout archetype: Minimal property journal
- Density: spacious
- Shape language: Thin-rule listing cards
- Surface/material: Property editorial with quiet type, generous imagery, and thin-rule listings
- Image system: Modern homes, interiors, floor plans, neighbourhood details
- Interaction model: Architectural listing hero
- CTA style: Primary-reference CTA hierarchy using Get Valuation
- Pricing style: commission and management cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 23, 33, 49.

## Static Authorship Pass

This site folder is now treated as the editable static source for `UrbanNest`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `The Modern House` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

UrbanNest now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the The Modern House inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Get Valuation`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Urban`, shaped by `Minimal property journal`, `Thin-rule listing cards`, `Property filter, gallery modal, map-style area cards`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Urban` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
