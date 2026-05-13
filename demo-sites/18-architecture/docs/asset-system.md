# Asset System

## Asset Transformation Plan

| Asset Layer | Decision |
| --- | --- |
| Image style | Architecture photography, plans, models, site context |
| Photo style | Architecture photography, plans, models, site context |
| Illustration/icon style | local SVG mark and diagrams following Architecture portfolio with radical restraint, huge imagery, and project-index logic |
| Texture/background pattern | Architecture portfolio with radical restraint, huge imagery, and project-index logic |
| Diagram style | supports portfolio and planning proof and Spatial project index |
| Thumbnail/Open Graph | page-specific local SVG/PNG assets generated now; no stock, hotlinked, copied, or unclear-licence imagery |
| Crop ratios | hero ratios vary per site through css/styles.css; cards use component-specific crops |
| Border/overlay treatment | Architectural index cards and Architecture portfolio with radical restraint, huge imagery, and project-index logic |
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

This site folder is now treated as the editable static source for `AtelierGrid`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `Snohetta` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

AtelierGrid now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Snohetta inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Discuss Project`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Craft`, shaped by `Spatial project index`, `Architectural index cards`, `Project gallery, planning stage stepper, image reveal`, and `editorial` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Craft` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
