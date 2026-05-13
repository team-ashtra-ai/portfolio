# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

| Partial | Visual Style | Spacing/Layout | CSS Classes | JS Hooks | Asset Requirements | Difference Rule |
| --- | --- | --- | --- | --- | --- | --- |
| header | Friendly utility header | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| desktop navigation | Friendly utility header | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| mobile menu | Primary-reference mobile navigation | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| footer | public service footer | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| hero | Purple service hero | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| CTA | Primary-reference CTA hierarchy using Request Service | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| form | Service request form | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-contact-form/data-form-status | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| cards | Rounded tariff cards | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| resources | Primary-reference resource rhythm | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| pricing | service route cards | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| FAQ | civic FAQ with section-specific proof notes | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| cookie banner | Primary-reference compact consent | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-cookie-banner/data-cookie-accept | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| WhatsApp widget | fixed quick enquiry route with per-site brand styling and neutral tracking | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-whatsapp-widget/data-track | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| back-to-top | fixed scroll recovery control with visible focus and reduced-motion fallback | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-back-to-top | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| legal layout | Primary-reference plain legal notes | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| 404 page | brand-consistent recovery page with sitemap and home routes | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |
| thanks page | confirmation page that reinforces Primary-reference CTA hierarchy using Request Service follow-up | practical spacing with Rounded tariff cards | classes use theme-utilities modifiers plus component-specific classes | data-track/data-component | assets follow Energy accounts, meters, tariff calculators, service notices | must not resemble partials in sites 06, 30, 40 |

## Header Plan

| Header Field | Decision |
| --- | --- |
| Header height | unique --header-height token in css/styles.css |
| Logo position | matched to Friendly utility header |
| Nav layout | Friendly utility header with desktop density chosen for practical |
| CTA position | Request Service positioned as the primary route without crowding utility links |
| Top/search/booking bars | selected by site mode in generated header utility layer |
| Scroll behaviour | data-header toggles is-scrolled |
| Mobile breakpoint | 980px with a menu style derived from the site passport |

## Mobile Menu Plan

- Type: Primary-reference mobile navigation
- Open animation: controlled by `body.menu-open`, site-specific drawer/sheet/overlay CSS, and reduced-motion rules
- Close behaviour: link click and menu button state reset
- Nav grouping: primary routes first, then conversion and utility routes
- CTA placement: Request Service remains visible in desktop header and discoverable in mobile menu
- Tap target size: minimum 44px
- Accessibility focus: button has `aria-expanded`; final QA must verify keyboard reachability and focus visibility
- Background treatment: Utilities with playful purple energy, rounded service blocks, and transparent tariff flow

## Footer Plan

| Footer Field | Decision |
| --- | --- |
| Footer layout | public service footer |
| Footer density | practical |
| Column structure | sitemap-first with site-specific brand/contact/resource emphasis |
| CTA block | Primary-reference CTA hierarchy using Request Service |
| Trust/disclaimer area | service and report proof |
| Mobile stacking | single-column with legal and conversion routes preserved |

## Static Authorship Pass

This site folder is now treated as the editable static source for `ClearGrid`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `hospitality` footer pattern for the `Octopus Energy` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

ClearGrid now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Octopus Energy inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Service`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `ledger` for `Clear`, shaped by `Playful utility account flow`, `Rounded tariff cards`, `Service request finder, alert banner, report filter`, and `civic` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Clear` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
