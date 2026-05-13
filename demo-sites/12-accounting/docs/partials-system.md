# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

| Partial | Visual Style | Spacing/Layout | CSS Classes | JS Hooks | Asset Requirements | Difference Rule |
| --- | --- | --- | --- | --- | --- | --- |
| header | Blue product header | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| desktop navigation | Blue product header | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| mobile menu | Primary-reference mobile navigation | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| footer | filing support footer | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| hero | Rounded ledger dashboard hero | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| CTA | Primary-reference CTA hierarchy using Request Quote | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| form | Filing quote form | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-contact-form/data-form-status | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| cards | Ledger dashboard cards | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| resources | Primary-reference resource rhythm | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| pricing | filing package grid | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| FAQ | professional FAQ with section-specific proof notes | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| cookie banner | Primary-reference compact consent | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-cookie-banner/data-cookie-accept | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| WhatsApp widget | fixed quick enquiry route with per-site brand styling and neutral tracking | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-whatsapp-widget/data-track | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| back-to-top | fixed scroll recovery control with visible focus and reduced-motion fallback | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-back-to-top | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| legal layout | Primary-reference plain legal notes | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| 404 page | brand-consistent recovery page with sitemap and home routes | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |
| thanks page | confirmation page that reinforces Primary-reference CTA hierarchy using Request Quote follow-up | compact spacing with Ledger dashboard cards | classes use theme-accounting modifiers plus component-specific classes | data-track/data-component | assets follow Bookkeeping dashboards, invoices, payroll cards | must not resemble partials in sites 19, 29, 45 |

## Header Plan

| Header Field | Decision |
| --- | --- |
| Header height | unique --header-height token in css/styles.css |
| Logo position | matched to Blue product header |
| Nav layout | Blue product header with desktop density chosen for compact |
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
- Background treatment: Accounting clarity with sky blue, rounded dashboards, and friendly admin paths

## Footer Plan

| Footer Field | Decision |
| --- | --- |
| Footer layout | filing support footer |
| Footer density | compact |
| Column structure | sitemap-first with site-specific brand/contact/resource emphasis |
| CTA block | Primary-reference CTA hierarchy using Request Quote |
| Trust/disclaimer area | deadline and compliance proof |
| Mobile stacking | single-column with legal and conversion routes preserved |

## Static Authorship Pass

This site folder is now treated as the editable static source for `LedgerFlow`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Xero` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

LedgerFlow now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Xero inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Quote`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `split-index` for `Ledger`, shaped by `Cloud accounting dashboard`, `Ledger dashboard cards`, `Deadline calendar, document checklist, package comparison`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Ledger` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
