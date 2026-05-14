# CSS System

Each site owns its own `css/styles.css`. Shared organisation is allowed; visible design language is not.

## CSS Plan

| System | Decision |
| --- | --- |
| Typography | display/body/accent/mono font roles plus text scale, line-height, and tracking tokens |
| Colour | #f7fbff, #101820, #20b8d8, #07141e, #d7f7ff plus semantic success/warning/error/link/CTA tokens |
| Spacing | spacious density expressed through --space-* and --space-section |
| Grid/layout | Scan-first health check journey with container-sm/md/lg/xl/fluid tokens |
| Surface | Clean health-tech with scan-first white space, black copy, and electric blue data accents with raised/surface/gradient/overlay tokens |
| Radius/border/shadow | Rounded diagnostic data cards using radius, border, and shadow tokens |
| Motion | Soft reveal with data-point counters with fast/base/slow/ease and reduced-motion rules |
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

- Theme class: `theme-healthcare`
- Mode class: `mode-care`
- Layout signature: Scan-first health check journey
- Header type: Minimal scan header
- Hero type: Body scan split hero
- Card style: Rounded diagnostic data cards
- Form style: Scan booking form
- Pricing style: consultation fees pathway
- FAQ/resource style: Primary-reference resource rhythm
- Cookie/legal style: Primary-reference compact consent / Primary-reference plain legal notes

## Static Authorship Pass

This site folder is now treated as the editable static source for `AsterCare`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `professional` footer pattern for the `Neko Health` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.

## Portfolio Section Component Pass - 2026-05-11

AsterCare now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Neko Health inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Appointment`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `constellation` for `Aster`, shaped by `Scan-first health check journey`, `Rounded diagnostic data cards`, `Appointment pathway, service filter, reassurance FAQ`, and `care` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Aster` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `Healthcare, Medical Services & Patient Care` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `clinical calm` artwork for desktop, tablet, and mobile. The image direction remains tied to `Body-scan rooms, data visualisations, calm clinical detail` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
