# Theme Guide

## Anti-Template Rule

StayHaven must feel like a standalone premium website for Hospitality, Hotels & Guest Accommodation, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 11, 35, 45.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | restful hospitality |
| Visual mood | Hospitality with quiet luxury, large tranquil imagery, and restrained booking paths |
| Industry tone | restful guest confidence |
| Buyer psychology | comfort and availability |
| Trust style | availability and policy proof |
| Conversion style | Primary-reference CTA hierarchy using Check Availability |
| Content density | spacious |
| Image personality | Villas, landscapes, spa spaces, calm interiors |
| Level of formality | hospitality |
| Level of emotion | high |
| Level of technical detail | moderate |
| Premium feeling | A hotel site with serene full-bleed rooms, understated booking modules, experience cards, and policy calm |
| Commercial feeling | Primary-reference CTA hierarchy using Check Availability |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Palatino Linotype", Palatino, serif |
| Body font role | Aptos, Calibri, sans-serif |
| Accent font role | Didot, Bodoni 72, Georgia, serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Retreat room cards and Hospitality with quiet luxury, large tranquil imagery, and restrained booking paths |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f3efe7, #2f2a24, #b89b72, #2f2a24, #6c756b |
| Surface style | Hospitality with quiet luxury, large tranquil imagery, and restrained booking paths |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Retreat room cards with unique radius and border strength |
| Texture usage | Hospitality with quiet luxury, large tranquil imagery, and restrained booking paths texture; no generic repeated decorative background |
| Dark/light balance | hospitality mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A hotel site with serene full-bleed rooms, understated booking modules, experience cards, and policy calm
- Brand mood: restful hospitality
- Buyer psychology: comfort and availability
- Layout archetype: Quiet retreat booking flow
- Density: spacious
- Shape language: Retreat room cards
- Surface/material: Hospitality with quiet luxury, large tranquil imagery, and restrained booking paths
- Image system: Villas, landscapes, spa spaces, calm interiors
- Interaction model: Serene full-bleed stay hero
- CTA style: Primary-reference CTA hierarchy using Check Availability
- Pricing style: room rate cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 11, 35, 45.

## Static Authorship Pass

This site folder is now treated as the editable static source for `StayHaven`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Aman` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

StayHaven now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Aman inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Check Availability`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Stay`, shaped by `Quiet retreat booking flow`, `Retreat room cards`, `Room filter, booking panel, offer selector, amenities tabs`, and `hospitality` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Stay` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
