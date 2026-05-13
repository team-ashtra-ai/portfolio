# Theme Guide

## Anti-Template Rule

LineaMode must feel like a standalone premium website for Fashion, Apparel & Accessories, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 04, 20, 44.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | fashion editorial |
| Visual mood | Fashion with sunny surrealism, oversized imagery, and campaign-led commerce |
| Industry tone | editorial fashion restraint |
| Buyer psychology | taste, status and movement |
| Trust style | craft and collection proof |
| Conversion style | Primary-reference CTA hierarchy using Shop Collection |
| Content density | theatrical |
| Image personality | Campaign imagery, fabric closeups, product scale, runway detail |
| Level of formality | editorial |
| Level of emotion | high |
| Level of technical detail | moderate |
| Premium feeling | A fashion lookbook site with warm yellow, playful scale shifts, collection cards, and sizing routes |
| Commercial feeling | Primary-reference CTA hierarchy using Shop Collection |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Verdana, Geneva, sans-serif |
| Body font role | Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Accent font role | Georgia, "Times New Roman", serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Sunny lookbook cards and Fashion with sunny surrealism, oversized imagery, and campaign-led commerce |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #fff2b8, #111111, #ffde00, #111111, #d97b4f |
| Surface style | Fashion with sunny surrealism, oversized imagery, and campaign-led commerce |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Sunny lookbook cards with unique radius and border strength |
| Texture usage | Fashion with sunny surrealism, oversized imagery, and campaign-led commerce texture; no generic repeated decorative background |
| Dark/light balance | editorial mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A fashion lookbook site with warm yellow, playful scale shifts, collection cards, and sizing routes
- Brand mood: fashion editorial
- Buyer psychology: taste, status and movement
- Layout archetype: Sunlit campaign lookbook
- Density: theatrical
- Shape language: Sunny lookbook cards
- Surface/material: Fashion with sunny surrealism, oversized imagery, and campaign-led commerce
- Image system: Campaign imagery, fabric closeups, product scale, runway detail
- Interaction model: Oversized campaign hero
- CTA style: Primary-reference CTA hierarchy using Shop Collection
- Pricing style: collection drop cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 04, 20, 44.

## Static Authorship Pass

This site folder is now treated as the editable static source for `LineaMode`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `Jacquemus` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

LineaMode now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Jacquemus inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Shop Collection`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `shelf` for `Linea`, shaped by `Sunlit campaign lookbook`, `Sunny lookbook cards`, `Lookbook slider, size guide, collection filter`, and `editorial` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Linea` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
