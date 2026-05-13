# Theme Guide

## Anti-Template Rule

StageCurrent must feel like a standalone premium website for Entertainment, Music & Performance, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 07, 23, 47.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | live energy |
| Visual mood | Entertainment with black cinema mood, poster grids, and understated weirdness |
| Industry tone | high-energy live culture |
| Buyer psychology | excitement and access |
| Trust style | event and access proof |
| Conversion style | Primary-reference CTA hierarchy using View Tickets |
| Content density | theatrical |
| Image personality | Film posters, stage stills, credits, audience moments |
| Level of formality | dark |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | An entertainment site with film-poster rhythm, dark editorial cards, ticket routes, and venue proof |
| Commercial feeling | Primary-reference CTA hierarchy using View Tickets |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Verdana, Geneva, sans-serif |
| Body font role | Georgia, "Times New Roman", serif |
| Accent font role | Arial, Helvetica, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Poster event cards and Entertainment with black cinema mood, poster grids, and understated weirdness |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #050505, #ffffff, #c69a55, #ffffff, #e24a2e |
| Surface style | Entertainment with black cinema mood, poster grids, and understated weirdness |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Poster event cards with unique radius and border strength |
| Texture usage | Entertainment with black cinema mood, poster grids, and understated weirdness texture; no generic repeated decorative background |
| Dark/light balance | dark mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: An entertainment site with film-poster rhythm, dark editorial cards, ticket routes, and venue proof
- Brand mood: live energy
- Buyer psychology: excitement and access
- Layout archetype: Indie film poster system
- Density: theatrical
- Shape language: Poster event cards
- Surface/material: Entertainment with black cinema mood, poster grids, and understated weirdness
- Image system: Film posters, stage stills, credits, audience moments
- Interaction model: Dark poster hero
- CTA style: Primary-reference CTA hierarchy using View Tickets
- Pricing style: ticket tier cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 07, 23, 47.

## Static Authorship Pass

This site folder is now treated as the editable static source for `StageCurrent`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `A24` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

StageCurrent now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the A24 inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `View Tickets`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `private` for `Stage`, shaped by `Indie film poster system`, `Poster event cards`, `Event calendar, ticket selector, artist filter`, and `dark` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Stage` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
