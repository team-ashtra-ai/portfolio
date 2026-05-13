# Theme Guide

## Anti-Template Rule

StudioFrame must feel like a standalone premium website for Creative, Design & Visual Production, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 10, 26, 50.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | visual craft |
| Visual mood | Design portfolio with stark white, red accents, huge typography, and rigorous grids |
| Industry tone | visual production taste |
| Buyer psychology | taste and production trust |
| Trust style | portfolio and usage proof |
| Conversion style | Primary-reference CTA hierarchy using Start Project |
| Content density | spacious |
| Image personality | Brand systems, posters, design boards, case images |
| Level of formality | editorial |
| Level of emotion | high |
| Level of technical detail | moderate |
| Premium feeling | A creative portfolio with identity-led project tiles, typographic scale, lightbox logic, and studio enquiry |
| Commercial feeling | Primary-reference CTA hierarchy using Start Project |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Verdana, Geneva, sans-serif |
| Body font role | "Lucida Sans", "Segoe UI", sans-serif |
| Accent font role | Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Identity project cards and Design portfolio with stark white, red accents, huge typography, and rigorous grids |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #ffffff, #111111, #e30613, #111111, #0057ff |
| Surface style | Design portfolio with stark white, red accents, huge typography, and rigorous grids |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Identity project cards with unique radius and border strength |
| Texture usage | Design portfolio with stark white, red accents, huge typography, and rigorous grids texture; no generic repeated decorative background |
| Dark/light balance | editorial mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A creative portfolio with identity-led project tiles, typographic scale, lightbox logic, and studio enquiry
- Brand mood: visual craft
- Buyer psychology: taste and production trust
- Layout archetype: Graphic design portfolio grid
- Density: spacious
- Shape language: Identity project cards
- Surface/material: Design portfolio with stark white, red accents, huge typography, and rigorous grids
- Image system: Brand systems, posters, design boards, case images
- Interaction model: Typographic work hero
- CTA style: Primary-reference CTA hierarchy using Start Project
- Pricing style: production package cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 10, 26, 50.

## Static Authorship Pass

This site folder is now treated as the editable static source for `StudioFrame`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `Pentagram` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

StudioFrame now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Pentagram inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Start Project`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `ledger` for `Studio`, shaped by `Graphic design portfolio grid`, `Identity project cards`, `Portfolio filter, project lightbox, file/brief upload`, and `editorial` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Studio` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
