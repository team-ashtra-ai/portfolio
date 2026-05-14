# Theme Guide

## Anti-Template Rule

SkinTheory must feel like a standalone premium website for Beauty, Cosmetics & Aesthetic Products, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites 05, 21, 45.

## Brand Difference Plan

| Dimension | Decision |
| --- | --- |
| Brand personality | texture-led |
| Visual mood | Beauty retail with muted apothecary surfaces, serif detail, and calm product education |
| Industry tone | ingredient-conscious beauty care |
| Buyer psychology | self-care confidence |
| Trust style | ingredient and results proof |
| Conversion style | Primary-reference CTA hierarchy using Build Routine |
| Content density | relaxed |
| Image personality | Bottles, textures, counters, botanical ingredient details |
| Level of formality | commerce |
| Level of emotion | controlled |
| Level of technical detail | moderate |
| Premium feeling | A routine site with restrained product education, ingredient notes, tactile cards, and consultation routes |
| Commercial feeling | Primary-reference CTA hierarchy using Build Routine |

## Typography Transformation Plan

| Role | Decision |
| --- | --- |
| Display font role | Verdana, Geneva, sans-serif |
| Body font role | Arial, Helvetica, sans-serif |
| Accent font role | "Courier New", ui-monospace, monospace |
| Monospace use | technical labels, utility metadata, tracking notes, and compact evidence where useful |
| Heading treatment | site-specific weight, size, and line-height tokens in css/styles.css |
| Paragraph measure | bounded by --content-measure for reading comfort |
| Button/nav text | short, confident, and matched to the conversion style |
| Stats/quotes/eyebrows | accented through Ingredient education cards and Beauty retail with muted apothecary surfaces, serif detail, and calm product education |
| Mobile type scale | reduced by CSS clamp values without viewport-width font scaling |

## Colour And Surface Transformation Plan

| Layer | Decision |
| --- | --- |
| Primary palette | #f3eadc, #35291f, #8c6a4f, #35291f, #c9b28c |
| Surface style | Beauty retail with muted apothecary surfaces, serif detail, and calm product education |
| Shadow style | generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow |
| Border style | matched to Ingredient education cards with unique radius and border strength |
| Texture usage | Beauty retail with muted apothecary surfaces, serif detail, and calm product education texture; no generic repeated decorative background |
| Dark/light balance | commerce mode |
| Gradient usage | only through the site's primary/surface gradient tokens |

## Premium Design Passport

- Premium direction: A routine site with restrained product education, ingredient notes, tactile cards, and consultation routes
- Brand mood: texture-led
- Buyer psychology: self-care confidence
- Layout archetype: Apothecary routine journal
- Density: relaxed
- Shape language: Ingredient education cards
- Surface/material: Beauty retail with muted apothecary surfaces, serif detail, and calm product education
- Image system: Bottles, textures, counters, botanical ingredient details
- Interaction model: Muted product education hero
- CTA style: Primary-reference CTA hierarchy using Build Routine
- Pricing style: routine bundle cards
- Resource style: Primary-reference resource rhythm
- Mobile menu style: Primary-reference mobile navigation
- Cookie style: Primary-reference compact consent
- Legal style: Primary-reference plain legal notes

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites 05, 21, 45.

## Static Authorship Pass

This site folder is now treated as the editable static source for `SkinTheory`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `Aesop` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.

## Portfolio Section Component Pass - 2026-05-11

SkinTheory now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Aesop inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Build Routine`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Skin`, shaped by `Apothecary routine journal`, `Ingredient education cards`, `Routine finder, ingredient glossary, product filter`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Skin` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `Beauty, Cosmetics & Aesthetic Products` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `product theatre` artwork for desktop, tablet, and mobile. The image direction remains tied to `Bottles, textures, counters, botanical ingredient details` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
