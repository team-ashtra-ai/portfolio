# Theme Guide

## Anti-Template Rule

CivicAccess must feel like a standalone premium website for Government, Public Sector & Civic Services, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 03, 13, 29.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | plain civic |
| Visual mood | Public service with plain language, blue actions, and high-contrast forms |
| Industry tone | plain civic accessibility |
| Buyer psychology | public service access |
| Trust style | transparency and eligibility proof |
| Conversion style | Primary-reference CTA hierarchy using Start Request |
| Content density | practical |
| Image personality | Forms, service lists, notices, public task flows |
| Level of formality | civic |
| Level of emotion | controlled |
| Level of technical detail | moderate |
| Premium feeling | A civic service site with task-first pages, blue start buttons, form patterns, and accessibility-first structure |
| Commercial feeling | Primary-reference CTA hierarchy using Start Request |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Arial Narrow", Arial, sans-serif |
| Body font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Accent font role | "Lucida Sans", "Segoe UI", sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Square service boxes and Public service with plain language, blue actions, and high-contrast forms |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #ffffff, #1d70b8, #ffdd00, #0b0c0c, #ffdd00 |
| Surface style | Public service with plain language, blue actions, and high-contrast forms |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Square service boxes with unique radius and border strength |
| Texture usage | Public service with plain language, blue actions, and high-contrast forms texture; no generic repeated decorative background |
| Dark/light balance | civic mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A civic service site with task-first pages, blue start buttons, form patterns, and accessibility-first structure
- Brand mood: plain civic
- Buyer psychology: public service access
- Layout archetype: Public service task flow
- Density: practical
- Shape language: Square service boxes
- Surface/material: Public service with plain language, blue actions, and high-contrast forms
- Image system: Forms, service lists, notices, public task flows
- Interaction model: Plain service hero
- CTA style: Primary-reference CTA hierarchy using Start Request
- Pricing style: service eligibility cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 03, 13, 29.

## Static Authorship Pass

This site folder is now treated as the editable static source for `CivicAccess`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `civic` footer pattern for the `GOV.UK Design System` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

CivicAccess now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the GOV.UK Design System inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Start Request`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Forum`, shaped by `Public service task flow`, `Square service boxes`, `Service search, form finder, document filter, alert controls`, and `civic` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Forum` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
