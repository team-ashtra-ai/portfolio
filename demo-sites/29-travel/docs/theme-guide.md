# Theme Guide

## Anti-Template Rule

AtlasKind must feel like a standalone premium website for Travel, Tourism & Destination Experiences, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 12, 36, 46.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | destination-led |
| Visual mood | Travel editorial with black contrast, immersive destinations, and itinerary storytelling |
| Industry tone | curated destination expertise |
| Buyer psychology | wanderlust and practical planning |
| Trust style | itinerary and safety proof |
| Conversion style | Primary-reference CTA hierarchy using Plan Trip |
| Content density | spacious |
| Image personality | Remote places, maps, itinerary details, travel photography |
| Level of formality | editorial |
| Level of emotion | high |
| Level of technical detail | moderate |
| Premium feeling | A travel-planning site with dark editorial hero, trip story cards, itinerary accordions, and bespoke enquiry |
| Commercial feeling | Primary-reference CTA hierarchy using Plan Trip |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | "Palatino Linotype", Palatino, serif |
| Body font role | "Lucida Sans", "Segoe UI", sans-serif |
| Accent font role | "Segoe UI", Tahoma, Geneva, sans-serif |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Journey story cards and Travel editorial with black contrast, immersive destinations, and itinerary storytelling |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #0b0b0b, #ffffff, #b4874a, #f1eee8, #8bb8e8 |
| Surface style | Travel editorial with black contrast, immersive destinations, and itinerary storytelling |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Journey story cards with unique radius and border strength |
| Texture usage | Travel editorial with black contrast, immersive destinations, and itinerary storytelling texture; no generic repeated decorative background |
| Dark/light balance | editorial mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A travel-planning site with dark editorial hero, trip story cards, itinerary accordions, and bespoke enquiry
- Brand mood: destination-led
- Buyer psychology: wanderlust and practical planning
- Layout archetype: Dark destination magazine
- Density: spacious
- Shape language: Journey story cards
- Surface/material: Travel editorial with black contrast, immersive destinations, and itinerary storytelling
- Image system: Remote places, maps, itinerary details, travel photography
- Interaction model: Immersive trip hero
- CTA style: Primary-reference CTA hierarchy using Plan Trip
- Pricing style: trip package cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 12, 36, 46.

## Static Authorship Pass

This site folder is now treated as the editable static source for `AtlasKind`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Black Tomato` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

AtlasKind now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Black Tomato inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Plan Trip`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `civic` for `Atlas`, shaped by `Dark destination magazine`, `Journey story cards`, `Trip finder, destination filter, itinerary accordion`, and `editorial` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Atlas` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
