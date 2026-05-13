# CSS System

Each site owns its own `css/styles.css`. Shared organisation is allowed; visible design language is not.

## CSS Plan

| System | Decision |
| --- | --- |
| Typography | display/body/accent/mono font roles plus text scale, line-height, and tracking tokens |
| Colour | #ffffff, #000000, #777777, #000000, #d9d9d9 plus semantic success/warning/error/link/CTA tokens |
| Spacing | compact density expressed through --space-* and --space-section |
| Grid/layout | Monochrome catalogue system with container-sm/md/lg/xl/fluid tokens |
| Surface | E-commerce with monochrome grid discipline, compact type, and catalogue authority with raised/surface/gradient/overlay tokens |
| Radius/border/shadow | Monochrome product cards using radius, border, and shadow tokens |
| Motion | Grid snap reveal with fast/base/slow/ease and reduced-motion rules |
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

- Theme class: `theme-ecommerce`
- Mode class: `mode-commerce`
- Layout signature: Monochrome catalogue system
- Header type: Compact shop header
- Hero type: Fashion-commerce grid hero
- Card style: Monochrome product cards
- Form style: Support routing form
- Pricing style: seller/customer route cards
- FAQ/resource style: Primary-reference resource rhythm
- Cookie/legal style: Primary-reference compact consent / Primary-reference plain legal notes

## Static Authorship Pass

This site folder is now treated as the editable static source for `MarketPulse`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `SSENSE` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

MarketPulse now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the SSENSE inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Browse Market`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Market`, shaped by `Monochrome catalogue system`, `Monochrome product cards`, `Catalogue filter, seller/customer support routing`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Market` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
