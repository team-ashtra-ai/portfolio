# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

| Partial | Visual Style | Spacing/Layout | CSS Classes | JS Hooks | Asset Requirements | Difference Rule |
| --- | --- | --- | --- | --- | --- | --- |
| header | Fashion campaign header | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| desktop navigation | Fashion campaign header | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| mobile menu | Primary-reference mobile navigation | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-menu-toggle/data-header | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| footer | stockist footer | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| hero | Oversized campaign hero | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| CTA | Primary-reference CTA hierarchy using Shop Collection | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| form | Styling enquiry form | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-contact-form/data-form-status | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| cards | Sunny lookbook cards | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| resources | Primary-reference resource rhythm | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| pricing | collection drop cards | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| FAQ | editorial FAQ with section-specific proof notes | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| cookie banner | Primary-reference compact consent | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-cookie-banner/data-cookie-accept | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| WhatsApp widget | fixed quick enquiry route with per-site brand styling and neutral tracking | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-whatsapp-widget/data-track | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| back-to-top | fixed scroll recovery control with visible focus and reduced-motion fallback | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-back-to-top | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| legal layout | Primary-reference plain legal notes | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| 404 page | brand-consistent recovery page with sitemap and home routes | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |
| thanks page | confirmation page that reinforces Primary-reference CTA hierarchy using Shop Collection follow-up | theatrical spacing with Sunny lookbook cards | classes use theme-fashion modifiers plus component-specific classes | data-track/data-component | assets follow Campaign imagery, fabric closeups, product scale, runway detail | must not resemble partials in sites 04, 20, 44 |

## Header Plan

| Header Field | Decision |
| --- | --- |
| Header height | unique --header-height token in css/styles.css |
| Logo position | matched to Fashion campaign header |
| Nav layout | Fashion campaign header with desktop density chosen for theatrical |
| CTA position | Shop Collection positioned as the primary route without crowding utility links |
| Top/search/booking bars | selected by site mode in generated header utility layer |
| Scroll behaviour | data-header toggles is-scrolled |
| Mobile breakpoint | 980px with a menu style derived from the site passport |

## Mobile Menu Plan

- Type: Primary-reference mobile navigation
- Open animation: controlled by `body.menu-open`, site-specific drawer/sheet/overlay CSS, and reduced-motion rules
- Close behaviour: link click and menu button state reset
- Nav grouping: primary routes first, then conversion and utility routes
- CTA placement: Shop Collection remains visible in desktop header and discoverable in mobile menu
- Tap target size: minimum 44px
- Accessibility focus: button has `aria-expanded`; final QA must verify keyboard reachability and focus visibility
- Background treatment: Fashion with sunny surrealism, oversized imagery, and campaign-led commerce

## Footer Plan

| Footer Field | Decision |
| --- | --- |
| Footer layout | stockist footer |
| Footer density | theatrical |
| Column structure | sitemap-first with site-specific brand/contact/resource emphasis |
| CTA block | Primary-reference CTA hierarchy using Shop Collection |
| Trust/disclaimer area | craft and collection proof |
| Mobile stacking | single-column with legal and conversion routes preserved |

## Static Authorship Pass

This site folder is now treated as the editable static source for `LineaMode`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `Jacquemus` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

LineaMode now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Jacquemus inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Shop Collection`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `shelf` for `Linea`, shaped by `Sunlit campaign lookbook`, `Sunny lookbook cards`, `Lookbook slider, size guide, collection filter`, and `editorial` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Linea` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
