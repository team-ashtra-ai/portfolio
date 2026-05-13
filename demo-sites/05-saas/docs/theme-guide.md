# Theme Guide

## Anti-Template Rule

OrbitDesk must feel like a standalone premium website for Software, SaaS Platforms & Digital Products, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 12, 22, 38.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | product-led |
| Visual mood | Dark product system with glass UI, fine borders, gradient light, and app panels |
| Industry tone | product-led software directness |
| Buyer psychology | speed, clarity, and product confidence |
| Trust style | product usage and integrations proof |
| Conversion style | Primary-reference CTA hierarchy using Schedule Demo |
| Content density | medium |
| Image personality | Dark app screens, issue boards, roadmap panels |
| Level of formality | technical |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | A product-led SaaS site with a dark dashboard hero, precise modules, issue-like cards, and calm product copy |
| Commercial feeling | Primary-reference CTA hierarchy using Schedule Demo |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Inter, ui-sans-serif, system-ui, sans-serif |
| Body font role | "Trebuchet MS", Arial, sans-serif |
| Accent font role | Verdana, Geneva, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Fine-line app cards and Dark product system with glass UI, fine borders, gradient light, and app panels |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #08090d, #5e6ad2, #9b8cff, #f7f8ff, #37d67a |
| Surface style | Dark product system with glass UI, fine borders, gradient light, and app panels |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Fine-line app cards with unique radius and border strength |
| Texture usage | Dark product system with glass UI, fine borders, gradient light, and app panels texture; no generic repeated decorative background |
| Dark/light balance | technical mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A product-led SaaS site with a dark dashboard hero, precise modules, issue-like cards, and calm product copy
- Brand mood: product-led
- Buyer psychology: speed, clarity, and product confidence
- Layout archetype: Dark product dashboard system
- Density: medium
- Shape language: Fine-line app cards
- Surface/material: Dark product system with glass UI, fine borders, gradient light, and app panels
- Image system: Dark app screens, issue boards, roadmap panels
- Interaction model: App interface hero
- CTA style: Primary-reference CTA hierarchy using Schedule Demo
- Pricing style: plan comparison toggle
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 12, 22, 38.

## Static Authorship Pass

This site folder is now treated as the editable static source for `OrbitDesk`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Linear` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

OrbitDesk now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Linear inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Schedule Demo`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `magazine` for `Orbit`, shaped by `Dark product dashboard system`, `Fine-line app cards`, `Pricing toggle, feature tabs, integration filter, product UI display`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Orbit` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
