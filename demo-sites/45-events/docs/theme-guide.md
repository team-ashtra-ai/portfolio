# Theme Guide

## Anti-Template Rule

VowVenue must feel like a standalone premium website for Events, Weddings & Experience Production, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 02, 12, 28.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | celebratory planning |
| Visual mood | Events with clean cards, soft gradients, calendar utility, and quick RSVP routes |
| Industry tone | experience-led celebration planning |
| Buyer psychology | emotion and confidence |
| Trust style | portfolio and planning proof |
| Conversion style | Primary-reference CTA hierarchy using Enquire Date |
| Content density | image-rich |
| Image personality | Event cards, calendars, guest lists, venue details |
| Level of formality | hospitality |
| Level of emotion | high |
| Level of technical detail | moderate |
| Premium feeling | An events site with elegant event cards, date filters, host proof, and RSVP-style enquiry |
| Commercial feeling | Primary-reference CTA hierarchy using Enquire Date |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Arial Narrow", Arial, sans-serif |
| Body font role | Arial, Helvetica, sans-serif |
| Accent font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through RSVP event cards and Events with clean cards, soft gradients, calendar utility, and quick RSVP routes |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f7f8ff, #6c47ff, #14b8a6, #111827, #ffb703 |
| Surface style | Events with clean cards, soft gradients, calendar utility, and quick RSVP routes |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to RSVP event cards with unique radius and border strength |
| Texture usage | Events with clean cards, soft gradients, calendar utility, and quick RSVP routes texture; no generic repeated decorative background |
| Dark/light balance | hospitality mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: An events site with elegant event cards, date filters, host proof, and RSVP-style enquiry
- Brand mood: celebratory planning
- Buyer psychology: emotion and confidence
- Layout archetype: Clean event calendar system
- Density: image-rich
- Shape language: RSVP event cards
- Surface/material: Events with clean cards, soft gradients, calendar utility, and quick RSVP routes
- Image system: Event cards, calendars, guest lists, venue details
- Interaction model: Event card hero
- CTA style: Primary-reference CTA hierarchy using Enquire Date
- Pricing style: package calculator cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 02, 12, 28.

## Static Authorship Pass

This site folder is now treated as the editable static source for `VowVenue`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Luma` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

VowVenue now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Luma inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Enquire Date`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `magazine` for `Vow`, shaped by `Clean event calendar system`, `RSVP event cards`, `Event type selector, venue filter, package calculator`, and `hospitality` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Vow` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
