# Theme Guide

## Anti-Template Rule

ChainPilot must feel like a standalone premium website for Logistics, Delivery & Supply Chain, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 14, 38, 48.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | networked |
| Visual mood | Logistics platform with blue enterprise polish, orange action, and shipment dashboards |
| Industry tone | networked delivery control |
| Buyer psychology | visibility and delivery control |
| Trust style | tracking and network proof |
| Conversion style | Primary-reference CTA hierarchy using Request Quote |
| Content density | dense |
| Image personality | Ports, shipment dashboards, containers, trade lanes |
| Level of formality | technical |
| Level of emotion | controlled |
| Level of technical detail | high |
| Premium feeling | A freight-command site with shipment dashboards, network maps, quote modules, and status proof |
| Commercial feeling | Primary-reference CTA hierarchy using Request Quote |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Aptos, "Segoe UI", system-ui, sans-serif |
| Body font role | Arial, Helvetica, sans-serif |
| Accent font role | "Arial Narrow", Arial, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Tracking dashboard cards and Logistics platform with blue enterprise polish, orange action, and shipment dashboards |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f4f8ff, #2563eb, #ff7a1a, #0f172a, #a7c7ff |
| Surface style | Logistics platform with blue enterprise polish, orange action, and shipment dashboards |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Tracking dashboard cards with unique radius and border strength |
| Texture usage | Logistics platform with blue enterprise polish, orange action, and shipment dashboards texture; no generic repeated decorative background |
| Dark/light balance | technical mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A freight-command site with shipment dashboards, network maps, quote modules, and status proof
- Brand mood: networked
- Buyer psychology: visibility and delivery control
- Layout archetype: Global freight command
- Density: dense
- Shape language: Tracking dashboard cards
- Surface/material: Logistics platform with blue enterprise polish, orange action, and shipment dashboards
- Image system: Ports, shipment dashboards, containers, trade lanes
- Interaction model: Shipment dashboard hero
- CTA style: Primary-reference CTA hierarchy using Request Quote
- Pricing style: shipment quote calculator
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 14, 38, 48.

## Static Authorship Pass

This site folder is now treated as the editable static source for `ChainPilot`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Flexport` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

ChainPilot now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Flexport inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Quote`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `constellation` for `Chain`, shaped by `Global freight command`, `Tracking dashboard cards`, `Tracking mockup, quote calculator, network map filter`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Chain` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
