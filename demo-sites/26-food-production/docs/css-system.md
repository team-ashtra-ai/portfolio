# CSS System

Each site owns its own `css/styles.css`. Shared organisation is allowed; visible design language is not.

## CSS Plan

| System | Decision |
| --- | --- |
| Typography | display/body/accent/mono font roles plus text scale, line-height, and tracking tokens |
| Colour | #f5ead2, #004b8d, #f26b3a, #111111, #ffdf3d plus semantic success/warning/error/link/CTA tokens |
| Spacing | image-rich density expressed through --space-* and --space-section |
| Grid/layout | Playful product manifesto with container-sm/md/lg/xl/fluid tokens |
| Surface | Food brand with playful packaging, chunky copy blocks, and offbeat product shelves with raised/surface/gradient/overlay tokens |
| Radius/border/shadow | Chunky ingredient cards using radius, border, and shadow tokens |
| Motion | Poster-style reveal with fast/base/slow/ease and reduced-motion rules |
| Print/accessibility | print removes chrome; focus-visible token and high-contrast states remain required |

## Required Editable CSS Tokens

- --font-display
- --font-body
- --font-accent
- --font-mono
- --text-xs
- --text-sm
- --text-md
- --text-lg
- --text-xl
- --text-hero
- --line-tight
- --line-normal
- --line-loose
- --tracking-tight
- --tracking-normal
- --tracking-wide
- --color-bg
- --color-bg-alt
- --color-surface
- --color-surface-raised
- --color-text
- --color-muted
- --color-primary
- --color-secondary
- --color-accent
- --color-border
- --color-success
- --color-warning
- --color-error
- --gradient-primary
- --gradient-surface
- --overlay-dark
- --overlay-light
- --container-sm
- --container-md
- --container-lg
- --container-xl
- --container-fluid
- --space-xs
- --space-sm
- --space-md
- --space-lg
- --space-xl
- --space-section
- --radius-none
- --radius-sm
- --radius-md
- --radius-lg
- --radius-xl
- --radius-pill
- --shadow-none
- --shadow-soft
- --shadow-medium
- --shadow-strong
- --shadow-glow
- --border-thin
- --border-medium
- --border-strong
- --motion-fast
- --motion-base
- --motion-slow
- --motion-ease

## Component Families To Redesign Per Site

- site-header
- mobile-menu
- footer
- hero
- section
- section-header
- content-grid
- card
- button
- form
- input
- textarea
- select
- checkbox
- badge
- tag
- breadcrumb
- accordion
- tabs
- pricing
- table
- timeline
- gallery
- lightbox
- testimonial
- metric
- case-study
- article-card
- download-card
- profile-card
- product-card
- listing-card
- CTA-strip
- cookie-banner
- legal-page
- error-page
- thanks-page

## CSS States To Include

- default
- hover
- focus
- focus-visible
- active
- disabled
- loading
- success
- error
- empty
- expanded
- collapsed
- selected
- current
- sticky
- scrolled
- reduced-motion

## Site-Specific CSS Direction

- Theme class: `theme-food-production`
- Mode class: `mode-commerce`
- Layout signature: Playful product manifesto
- Header type: Food brand header
- Hero type: Packaging shelf hero
- Card style: Chunky ingredient cards
- Form style: Trade enquiry form
- Pricing style: trade pack cards
- FAQ/resource style: Primary-reference resource rhythm
- Cookie/legal style: Primary-reference compact consent / Primary-reference plain legal notes

## Static Authorship Pass

This site folder is now treated as the editable static source for `HarvestPack`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `hospitality` footer pattern for the `Oatly` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.

## Portfolio Section Component Pass - 2026-05-11

HarvestPack now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Oatly inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Trade Info`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Grain`, shaped by `Playful product manifesto`, `Chunky ingredient cards`, `Product/allergen filter, stockist finder, recipe tabs`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Grain` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `Food Production, Packaged Goods & Consumer Foods` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `product theatre` artwork for desktop, tablet, and mobile. The image direction remains tied to `Cartons, ingredients, recipe panels, hand-made notes` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
