# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

| Partial | Visual Style | Spacing/Layout | CSS Classes | JS Hooks | Asset Requirements | Difference Rule |
| --- | --- | --- | --- | --- | --- | --- |
| header | Film studio header | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| desktop navigation | Film studio header | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| mobile menu | Primary-reference mobile navigation | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| footer | venue footer | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| hero | Dark poster hero | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| CTA | Primary-reference CTA hierarchy using View Tickets | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| form | Ticket enquiry form | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-contact-form/data-form-status | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| cards | Poster event cards | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| resources | Primary-reference resource rhythm | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| pricing | ticket tier cards | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| FAQ | dark FAQ with section-specific proof notes | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| cookie banner | Primary-reference compact consent | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-cookie-banner/data-cookie-accept | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| WhatsApp widget | fixed quick enquiry route with per-site brand styling and neutral tracking | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-whatsapp-widget/data-track | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| back-to-top | fixed scroll recovery control with visible focus and reduced-motion fallback | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-back-to-top | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| legal layout | Primary-reference plain legal notes | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| 404 page | brand-consistent recovery page with sitemap and home routes | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |
| thanks page | confirmation page that reinforces Primary-reference CTA hierarchy using View Tickets follow-up | theatrical spacing with Poster event cards | classes use theme-entertainment modifiers plus component-specific classes | data-track/data-component | assets follow Film posters, stage stills, credits, audience moments | must not resemble partials in sites 07, 23, 47 |

## Header Plan

| Header Field | Decision |
| --- | --- |
| Header height | unique --header-height token in css/styles.css |
| Logo position | matched to Film studio header |
| Nav layout | Film studio header with desktop density chosen for theatrical |
| CTA position | View Tickets positioned as the primary route without crowding utility links |
| Top/search/booking bars | selected by site mode in generated header utility layer |
| Scroll behaviour | data-header toggles is-scrolled |
| Mobile breakpoint | 980px with a menu style derived from the site passport |

## Mobile Menu Plan

- Type: Primary-reference mobile navigation
- Open animation: controlled by `body.menu-open`, site-specific drawer/sheet/overlay CSS, and reduced-motion rules
- Close behaviour: link click and menu button state reset
- Nav grouping: primary routes first, then conversion and utility routes
- CTA placement: View Tickets remains visible in desktop header and discoverable in mobile menu
- Tap target size: minimum 44px
- Accessibility focus: button has `aria-expanded`; final QA must verify keyboard reachability and focus visibility
- Background treatment: Entertainment with black cinema mood, poster grids, and understated weirdness

## Footer Plan

| Footer Field | Decision |
| --- | --- |
| Footer layout | venue footer |
| Footer density | theatrical |
| Column structure | sitemap-first with site-specific brand/contact/resource emphasis |
| CTA block | Primary-reference CTA hierarchy using View Tickets |
| Trust/disclaimer area | event and access proof |
| Mobile stacking | single-column with legal and conversion routes preserved |

## Static Authorship Pass

This site folder is now treated as the editable static source for `StageCurrent`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `A24` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.

## Portfolio Section Component Pass - 2026-05-11

StageCurrent now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the A24 inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `View Tickets`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `private` for `Stage`, shaped by `Indie film poster system`, `Poster event cards`, `Event calendar, ticket selector, artist filter`, and `dark` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Stage` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `Entertainment, Music & Performance` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `cinematic command` artwork for desktop, tablet, and mobile. The image direction remains tied to `Film posters, stage stills, credits, audience moments` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
