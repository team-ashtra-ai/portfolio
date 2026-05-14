# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

| Partial | Visual Style | Spacing/Layout | CSS Classes | JS Hooks | Asset Requirements | Difference Rule |
| --- | --- | --- | --- | --- | --- | --- |
| header | Apothecary shop header | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| desktop navigation | Apothecary shop header | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| mobile menu | Primary-reference mobile navigation | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| footer | ingredient footer | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| hero | Muted product education hero | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| CTA | Primary-reference CTA hierarchy using Build Routine | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| form | Routine advice form | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-contact-form/data-form-status | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| cards | Ingredient education cards | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| resources | Primary-reference resource rhythm | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| pricing | routine bundle cards | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| FAQ | commerce FAQ with section-specific proof notes | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| cookie banner | Primary-reference compact consent | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-cookie-banner/data-cookie-accept | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| WhatsApp widget | fixed quick enquiry route with per-site brand styling and neutral tracking | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-whatsapp-widget/data-track | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| back-to-top | fixed scroll recovery control with visible focus and reduced-motion fallback | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-back-to-top | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| legal layout | Primary-reference plain legal notes | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| 404 page | brand-consistent recovery page with sitemap and home routes | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |
| thanks page | confirmation page that reinforces Primary-reference CTA hierarchy using Build Routine follow-up | relaxed spacing with Ingredient education cards | classes use theme-beauty modifiers plus component-specific classes | data-track/data-component | assets follow Bottles, textures, counters, botanical ingredient details | must not resemble partials in sites 05, 21, 45 |

## Header Plan

| Header Field | Decision |
| --- | --- |
| Header height | unique --header-height token in css/styles.css |
| Logo position | matched to Apothecary shop header |
| Nav layout | Apothecary shop header with desktop density chosen for relaxed |
| CTA position | Build Routine positioned as the primary route without crowding utility links |
| Top/search/booking bars | selected by site mode in generated header utility layer |
| Scroll behaviour | data-header toggles is-scrolled |
| Mobile breakpoint | 980px with a menu style derived from the site passport |

## Mobile Menu Plan

- Type: Primary-reference mobile navigation
- Open animation: controlled by `body.menu-open`, site-specific drawer/sheet/overlay CSS, and reduced-motion rules
- Close behaviour: link click and menu button state reset
- Nav grouping: primary routes first, then conversion and utility routes
- CTA placement: Build Routine remains visible in desktop header and discoverable in mobile menu
- Tap target size: minimum 44px
- Accessibility focus: button has `aria-expanded`; final QA must verify keyboard reachability and focus visibility
- Background treatment: Beauty retail with muted apothecary surfaces, serif detail, and calm product education

## Footer Plan

| Footer Field | Decision |
| --- | --- |
| Footer layout | ingredient footer |
| Footer density | relaxed |
| Column structure | sitemap-first with site-specific brand/contact/resource emphasis |
| CTA block | Primary-reference CTA hierarchy using Build Routine |
| Trust/disclaimer area | ingredient and results proof |
| Mobile stacking | single-column with legal and conversion routes preserved |

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
