# Asset System

## Asset Transformation Plan

| Asset Layer | Decision |
| --- | --- |
| Image style | Product grids, editorial crops, order panels, marketplace lists |
| Photo style | Product grids, editorial crops, order panels, marketplace lists |
| Illustration/icon style | local SVG mark and diagrams following E-commerce with monochrome grid discipline, compact type, and catalogue authority |
| Texture/background pattern | E-commerce with monochrome grid discipline, compact type, and catalogue authority |
| Diagram style | supports trust and checkout proof and Monochrome catalogue system |
| Thumbnail/Open Graph | page-specific local SVG/PNG assets generated now; no stock, hotlinked, copied, or unclear-licence imagery |
| Crop ratios | hero ratios vary per site through css/styles.css; cards use component-specific crops |
| Border/overlay treatment | Monochrome product cards and E-commerce with monochrome grid discipline, compact type, and catalogue authority |
| Compression rules | local, optimized, descriptive filenames, no hotlinking |
| Alt text rules | specific purpose-first alt text; decorative images use empty alt |
| License tracking | all generated assets are recorded in docs/asset-licenses.md; future external additions require source/licence proof before launch |

## Required Asset Inventory

- hero images
- section images
- card images
- background textures
- icons
- illustrations
- diagrams
- gallery images
- blog/resource thumbnails
- Open Graph images
- download covers
- logo mark or wordmark treatment
- favicon
- fallback images

## Naming And License Rules

- Use `assets/images/hero/`, `assets/images/pages/`, `assets/images/sections/`, `assets/images/cards/`, `assets/images/gallery/`, `assets/images/backgrounds/`, and `assets/images/utility/` for page and component imagery.
- Use `assets/brand/` for logo, symbol, favicons, app icon, and social avatar.
- Use `assets/og/` for page-specific social preview assets.
- Do not hotlink assets.
- Record source, generation note, license, filename, alt text, crop notes, compression notes, and page usage in `docs/asset-licenses.md` and `docs/asset-inventory.md`.

## Static Authorship Pass

This site folder is now treated as the editable static source for `MarketPulse`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `SSENSE` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.

## Portfolio Section Component Pass - 2026-05-11

MarketPulse now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the SSENSE inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Browse Market`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Market`, shaped by `Monochrome catalogue system`, `Monochrome product cards`, `Catalogue filter, seller/customer support routing`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Market` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `E-commerce, Marketplaces & Digital Commerce` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `product theatre` artwork for desktop, tablet, and mobile. The image direction remains tied to `Product grids, editorial crops, order panels, marketplace lists` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
