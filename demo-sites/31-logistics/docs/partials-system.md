# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

| Partial | Visual Style | Spacing/Layout | CSS Classes | JS Hooks | Asset Requirements | Difference Rule |
| --- | --- | --- | --- | --- | --- | --- |
| header | Logistics platform header | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| desktop navigation | Logistics platform header | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| mobile menu | Primary-reference mobile navigation | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| footer | network footer | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| hero | Shipment dashboard hero | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| CTA | Primary-reference CTA hierarchy using Request Quote | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| form | Freight quote form | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-contact-form/data-form-status | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| cards | Tracking dashboard cards | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| resources | Primary-reference resource rhythm | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| pricing | shipment quote calculator | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| FAQ | technical FAQ with section-specific proof notes | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| cookie banner | Primary-reference compact consent | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-cookie-banner/data-cookie-accept | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| WhatsApp widget | fixed quick enquiry route with per-site brand styling and neutral tracking | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-whatsapp-widget/data-track | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| back-to-top | fixed scroll recovery control with visible focus and reduced-motion fallback | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-back-to-top | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| legal layout | Primary-reference plain legal notes | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| 404 page | brand-consistent recovery page with sitemap and home routes | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |
| thanks page | confirmation page that reinforces Primary-reference CTA hierarchy using Request Quote follow-up | dense spacing with Tracking dashboard cards | classes use theme-logistics modifiers plus component-specific classes | data-track/data-component | assets follow Ports, shipment dashboards, containers, trade lanes | must not resemble partials in sites 14, 38, 48 |

## Header Plan

| Header Field | Decision |
| --- | --- |
| Header height | unique --header-height token in css/styles.css |
| Logo position | matched to Logistics platform header |
| Nav layout | Logistics platform header with desktop density chosen for dense |
| CTA position | Request Quote positioned as the primary route without crowding utility links |
| Top/search/booking bars | selected by site mode in generated header utility layer |
| Scroll behaviour | data-header toggles is-scrolled |
| Mobile breakpoint | 980px with a menu style derived from the site passport |

## Mobile Menu Plan

- Type: Primary-reference mobile navigation
- Open animation: controlled by `body.menu-open`, site-specific drawer/sheet/overlay CSS, and reduced-motion rules
- Close behaviour: link click and menu button state reset
- Nav grouping: primary routes first, then conversion and utility routes
- CTA placement: Request Quote remains visible in desktop header and discoverable in mobile menu
- Tap target size: minimum 44px
- Accessibility focus: button has `aria-expanded`; final QA must verify keyboard reachability and focus visibility
- Background treatment: Logistics platform with blue enterprise polish, orange action, and shipment dashboards

## Footer Plan

| Footer Field | Decision |
| --- | --- |
| Footer layout | network footer |
| Footer density | dense |
| Column structure | sitemap-first with site-specific brand/contact/resource emphasis |
| CTA block | Primary-reference CTA hierarchy using Request Quote |
| Trust/disclaimer area | tracking and network proof |
| Mobile stacking | single-column with legal and conversion routes preserved |

## Static Authorship Pass

This site folder is now treated as the editable static source for `ChainPilot`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Flexport` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.

## Portfolio Section Component Pass - 2026-05-11

ChainPilot now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Flexport inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Quote`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `constellation` for `Chain`, shaped by `Global freight command`, `Tracking dashboard cards`, `Tracking mockup, quote calculator, network map filter`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Chain` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `Logistics, Delivery & Supply Chain` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `precision interface` artwork for desktop, tablet, and mobile. The image direction remains tied to `Ports, shipment dashboards, containers, trade lanes` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
