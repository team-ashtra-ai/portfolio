# Theme Guide

## Anti-Template Rule

ForgeBuild must feel like a standalone premium website for Construction, Building & Renovation, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 24, 34, 50.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | practical strong |
| Visual mood | Construction software with orange action, black contrast, and worksite proof |
| Industry tone | site-ready construction assurance |
| Buyer psychology | certainty around cost and disruption |
| Trust style | process and safety proof |
| Conversion style | Primary-reference CTA hierarchy using Request Estimate |
| Content density | dense |
| Image personality | Job sites, schedule boards, build dashboards |
| Level of formality | formal |
| Level of emotion | controlled |
| Level of technical detail | moderate |
| Premium feeling | A build-management site with construction CTAs, project panels, safety proof, and estimate routing |
| Commercial feeling | Primary-reference CTA hierarchy using Request Estimate |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Trebuchet MS", Arial, sans-serif |
| Body font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Accent font role | Aptos, "Segoe UI", system-ui, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Project control cards and Construction software with orange action, black contrast, and worksite proof |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #fff7ed, #ff6a00, #111827, #1f2937, #ffd166 |
| Surface style | Construction software with orange action, black contrast, and worksite proof |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Project control cards with unique radius and border strength |
| Texture usage | Construction software with orange action, black contrast, and worksite proof texture; no generic repeated decorative background |
| Dark/light balance | professional mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A build-management site with construction CTAs, project panels, safety proof, and estimate routing
- Brand mood: practical strong
- Buyer psychology: certainty around cost and disruption
- Layout archetype: Construction platform grid
- Density: dense
- Shape language: Project control cards
- Surface/material: Construction software with orange action, black contrast, and worksite proof
- Image system: Job sites, schedule boards, build dashboards
- Interaction model: Worksite software hero
- CTA style: Primary-reference CTA hierarchy using Request Estimate
- Pricing style: stage cost panels
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 24, 34, 50.

## Static Authorship Pass

This site folder is now treated as the editable static source for `ForgeBuild`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Procore` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

ForgeBuild now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Procore inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Estimate`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `shelf` for `Forge`, shaped by `Construction platform grid`, `Project control cards`, `Project estimator form, before/after slider, upload photos`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Forge` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
