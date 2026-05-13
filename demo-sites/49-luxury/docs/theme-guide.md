# Theme Guide

## Anti-Template Rule

MaisonVale must feel like a standalone premium website for Luxury, Premium & High-End Services, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 06, 16, 32.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | quiet exclusive |
| Visual mood | Luxury with deep green, gold restraint, heritage pacing, and private product focus |
| Industry tone | quiet high-end discretion |
| Buyer psychology | status and discretion |
| Trust style | discretion and craft proof |
| Conversion style | Primary-reference CTA hierarchy using Request Private Access |
| Content density | spacious |
| Image personality | Craft details, watches, private rooms, heritage materials |
| Level of formality | formal |
| Level of emotion | controlled |
| Level of technical detail | moderate |
| Premium feeling | A luxury service site with green-gold maison mood, heritage cards, private access routes, and discreet proof |
| Commercial feeling | Primary-reference CTA hierarchy using Request Private Access |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Arial Narrow", Arial, sans-serif |
| Body font role | "Trebuchet MS", Arial, sans-serif |
| Accent font role | Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Gold hairline cards and Luxury with deep green, gold restraint, heritage pacing, and private product focus |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #081f18, #0b5f3a, #d4af37, #f4efe2, #111111 |
| Surface style | Luxury with deep green, gold restraint, heritage pacing, and private product focus |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Gold hairline cards with unique radius and border strength |
| Texture usage | Luxury with deep green, gold restraint, heritage pacing, and private product focus texture; no generic repeated decorative background |
| Dark/light balance | luxury mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A luxury service site with green-gold maison mood, heritage cards, private access routes, and discreet proof
- Brand mood: quiet exclusive
- Buyer psychology: status and discretion
- Layout archetype: Heritage luxury maison
- Density: spacious
- Shape language: Gold hairline cards
- Surface/material: Luxury with deep green, gold restraint, heritage pacing, and private product focus
- Image system: Craft details, watches, private rooms, heritage materials
- Interaction model: Deep-green private hero
- CTA style: Primary-reference CTA hierarchy using Request Private Access
- Pricing style: concierge invitation cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 06, 16, 32.

## Static Authorship Pass

This site folder is now treated as the editable static source for `MaisonVale`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Rolex` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

MaisonVale now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Rolex inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Private Access`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `civic` for `Maison`, shaped by `Heritage luxury maison`, `Gold hairline cards`, `Private enquiry reveal, membership request, concierge stepper`, and `luxury` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Maison` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
