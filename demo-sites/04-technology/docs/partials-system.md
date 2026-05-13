# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

| Partial | Visual Style | Spacing/Layout | CSS Classes | JS Hooks | Asset Requirements | Difference Rule |
| --- | --- | --- | --- | --- | --- | --- |
| header | Orange product navigation | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| desktop navigation | Orange product navigation | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| mobile menu | Primary-reference mobile navigation | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| footer | support desk footer | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| hero | Network diagram hero | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| CTA | Primary-reference CTA hierarchy using Request IT Audit | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| form | IT audit route form | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-contact-form/data-form-status | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| cards | Network service tiles | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| resources | Primary-reference resource rhythm | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| pricing | support retainer matrix | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| FAQ | technical FAQ with section-specific proof notes | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| cookie banner | Primary-reference compact consent | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-cookie-banner/data-cookie-accept | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| WhatsApp widget | fixed quick enquiry route with per-site brand styling and neutral tracking | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-whatsapp-widget/data-track | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| back-to-top | fixed scroll recovery control with visible focus and reduced-motion fallback | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-back-to-top | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| legal layout | Primary-reference plain legal notes | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| 404 page | brand-consistent recovery page with sitemap and home routes | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |
| thanks page | confirmation page that reinforces Primary-reference CTA hierarchy using Request IT Audit follow-up | dense spacing with Network service tiles | classes use theme-technology modifiers plus component-specific classes | data-track/data-component | assets follow Edge maps, server nodes, operational dashboards | must not resemble partials in sites 11, 21, 37 |

## Header Plan

| Header Field | Decision |
| --- | --- |
| Header height | unique --header-height token in css/styles.css |
| Logo position | matched to Orange product navigation |
| Nav layout | Orange product navigation with desktop density chosen for dense |
| CTA position | Request IT Audit positioned as the primary route without crowding utility links |
| Top/search/booking bars | selected by site mode in generated header utility layer |
| Scroll behaviour | data-header toggles is-scrolled |
| Mobile breakpoint | 980px with a menu style derived from the site passport |

## Mobile Menu Plan

- Type: Primary-reference mobile navigation
- Open animation: controlled by `body.menu-open`, site-specific drawer/sheet/overlay CSS, and reduced-motion rules
- Close behaviour: link click and menu button state reset
- Nav grouping: primary routes first, then conversion and utility routes
- CTA placement: Request IT Audit remains visible in desktop header and discoverable in mobile menu
- Tap target size: minimum 44px
- Accessibility focus: button has `aria-expanded`; final QA must verify keyboard reachability and focus visibility
- Background treatment: Infrastructure marketing with orange CTAs, network diagrams, and dense product routes

## Footer Plan

| Footer Field | Decision |
| --- | --- |
| Footer layout | support desk footer |
| Footer density | dense |
| Column structure | sitemap-first with site-specific brand/contact/resource emphasis |
| CTA block | Primary-reference CTA hierarchy using Request IT Audit |
| Trust/disclaimer area | uptime and support proof |
| Mobile stacking | single-column with legal and conversion routes preserved |

## Static Authorship Pass

This site folder is now treated as the editable static source for `NexusOps`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Cloudflare` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

NexusOps now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Cloudflare inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request IT Audit`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `map` for `Nexus`, shaped by `Edge network product system`, `Network service tiles`, `Support plan comparison, system status cards, ticket route selector`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Nexus` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
