# Theme Guide

## Anti-Template Rule

CornerGoods must feel like a standalone premium website for Retail, Shops & Consumer Sales, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 02, 18, 42.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | shopfront |
| Visual mood | Retail minimalism with soft grey surfaces, product tiles, and clear shopping paths |
| Industry tone | friendly retail polish |
| Buyer psychology | convenience and offer discovery |
| Trust style | store and loyalty proof |
| Conversion style | Primary-reference CTA hierarchy using Visit Shop |
| Content density | medium |
| Image personality | Product tiles, store spaces, service cards, device-like panels |
| Level of formality | commerce |
| Level of emotion | controlled |
| Level of technical detail | moderate |
| Premium feeling | A retail shopfront with clean product shelves, rounded offer cards, service proof, and store-finder CTAs |
| Commercial feeling | Primary-reference CTA hierarchy using Visit Shop |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Aptos, "Segoe UI", system-ui, sans-serif |
| Body font role | "Trebuchet MS", Arial, sans-serif |
| Accent font role | "Palatino Linotype", Palatino, serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Rounded product tiles and Retail minimalism with soft grey surfaces, product tiles, and clear shopping paths |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f5f5f7, #1d1d1f, #0071e3, #1d1d1f, #a1a1a6 |
| Surface style | Retail minimalism with soft grey surfaces, product tiles, and clear shopping paths |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Rounded product tiles with unique radius and border strength |
| Texture usage | Retail minimalism with soft grey surfaces, product tiles, and clear shopping paths texture; no generic repeated decorative background |
| Dark/light balance | commerce mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A retail shopfront with clean product shelves, rounded offer cards, service proof, and store-finder CTAs
- Brand mood: shopfront
- Buyer psychology: convenience and offer discovery
- Layout archetype: Minimal product store
- Density: medium
- Shape language: Rounded product tiles
- Surface/material: Retail minimalism with soft grey surfaces, product tiles, and clear shopping paths
- Image system: Product tiles, store spaces, service cards, device-like panels
- Interaction model: Soft product shelf hero
- CTA style: Primary-reference CTA hierarchy using Visit Shop
- Pricing style: offer bundle cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 02, 18, 42.

## Static Authorship Pass

This site folder is now treated as the editable static source for `CornerGoods`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Apple Store` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

CornerGoods now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Apple Store inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Visit Shop`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `magazine` for `Corner`, shaped by `Minimal product store`, `Rounded product tiles`, `Product/category filter, loyalty signup, store finder`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Corner` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
