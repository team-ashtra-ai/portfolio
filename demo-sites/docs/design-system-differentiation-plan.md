# ASH-TRA 50 Demo Sites: Design System Differentiation Plan

## Objective

All 50 demo sites must keep the same delivery standard while looking and behaving like 50 different brands. The technical baseline stays shared: static HTML/CSS/JS, 10 core pages, 10 sections per core page, utility pages, local assets, SEO, forms, docs, QA, print styles, accessibility, and WordPress export notes.

The design language must not be shared. Each site needs distinct tokens, typography, colour psychology, layout rhythm, header, footer, hero, section model, cards, buttons, forms, pricing, FAQ, resources, cookie banner, utility pages, imagery, motion, and visible JavaScript behaviour.

## Current State

- The repo has 50 numbered demo sites under `demo-sites/01-*` through `demo-sites/50-*`.
- Each site already has `site.config.json`, `css/styles.css`, `js/main.js`, docs, utility pages, assets, and QA files.
- `demo-sites/docs/cross-site-diversity-report.md` already defines a useful theme DNA matrix.
- The CSS currently uses a shared base structure with per-site overrides. That is a good foundation, but the shared skeleton is still too visible.
- Required `partials/*.html` files do not currently exist. Header/footer/hero/form/card patterns are embedded directly in pages, so partialization should be introduced as a source/handoff layer or a generation layer, not as fragile client-side rendering.

## Non-Negotiable Rule

Two sites may share build discipline, accessibility rules, SEO structure, and progressive enhancement patterns. They must not share a recognizable design system.

A site fails review if it visibly reuses another site's hero, card grid, button shape, pricing layout, footer, mobile menu, cookie banner, form composition, resource cards, FAQ treatment, image treatment, motion rhythm, or section pacing without a deliberate industry reason.

## Implementation Phases

### Phase 1: Inventory And Similarity Audit

1. Parse every `site.config.json` and produce a working matrix with industry, visual direction, layout signature, hero type, header type, footer type, card style, form style, JavaScript signature, and theme mode.
2. Snapshot each current home page, pricing/contact page, utility page, and mobile menu at desktop and mobile widths.
3. Score each site against the design layers in this plan: brand, typography, colour, layout, spacing, shape, material, image direction, component treatment, and JavaScript behaviour.
4. Mark collisions where two sites share the same font pairing, palette structure, hero split, card shape, footer grid, pricing cards, form layout, mobile menu, or motion style.

### Phase 2: Token Expansion

Every site gets a complete token block at the top of `css/styles.css`. Values must be unique to the site's theme.

Required token set:

```css
:root {
  --font-display: ;
  --font-body: ;
  --font-accent: ;

  --color-bg: ;
  --color-surface: ;
  --color-surface-alt: ;
  --color-text: ;
  --color-muted: ;
  --color-primary: ;
  --color-secondary: ;
  --color-accent: ;
  --color-border: ;
  --color-success: ;
  --color-warning: ;
  --color-error: ;
  --color-link: ;
  --color-cta: ;
  --color-footer: ;
  --color-field: ;

  --container: ;
  --container-wide: ;
  --section-padding: ;
  --grid-gap: ;
  --content-measure: ;

  --radius-sm: ;
  --radius-md: ;
  --radius-lg: ;
  --radius-xl: ;

  --shadow-soft: ;
  --shadow-medium: ;
  --shadow-strong: ;

  --motion-fast: ;
  --motion-base: ;
  --motion-slow: ;

  --header-height: ;
}
```

Keep the naming organized, but change the values, proportions, and component rules per site.

### Phase 3: Static Partial Architecture

Add source partials to each site. These should support maintenance and WordPress export, while final pages remain normal static HTML.

Required source partials per site:

- `partials/header.html`
- `partials/mobile-menu.html`
- `partials/footer.html`
- `partials/hero.html`
- `partials/cta.html`
- `partials/form.html`
- `partials/cards.html`
- `partials/resources.html`
- `partials/pricing.html`
- `partials/faq.html`
- `partials/cookie.html`
- `partials/legal.html`

Rules:

- Do not make pages depend on JavaScript to load partials.
- Use partials as source templates or handoff references.
- Each site's partials must use distinct class modifiers, content patterns, and component composition.
- Utility pages must use the same brand system but lighter layouts appropriate to legal, cookies, accessibility, 404, sitemap, and thanks pages.

### Phase 4: Component Redesign Pass

For every site, redesign these visible pieces:

- Header: height, logo treatment, nav density, utility bar, CTA placement, scroll state, search/booking/alert controls.
- Mobile menu: overlay, drawer, bottom sheet, service finder, editorial index, booking-first menu, command drawer, or civic directory.
- Footer: sitemap density, contact layout, trust strip, legal block, newsletter, resource columns, map/contact panel, or brand story.
- Hero: text-only, image-first, split, search, booking, map, dashboard, command centre, editorial masthead, product shelf, timeline, private invitation, or gallery.
- Cards: icon, image, metric, spec, menu, listing, room, vehicle, article, case, document, dashboard, or profile cards.
- Forms: contact, quote, booking, upload, consultation, donation, reservation, route selector, public request, eligibility, or private enquiry.
- Pricing: plans, fees, calculators, package menus, comparison grids, membership toggles, quote panels, or editorial rate cards.
- FAQ: accordion, document list, civic help centre, support cards, compact legal notes, conversational prompts, or technical checklist.
- Resources/blog: archive, editorial feed, report library, recipe cards, destination stories, media kit, case studies, or document hub.
- Cookie banner: shape, placement, tone, CTA style, and settings treatment must match the site.

### Phase 5: JavaScript Differentiation

The JS foundation may stay shared for cookies, forms, tracking events, back-to-top, and reduced-motion support. The visible interaction layer must differ per site.

Each site needs at least three theme-specific progressive enhancements, such as:

- Healthcare: appointment pathway, service filter, reassurance FAQ.
- Cybersecurity: risk matrix, compliance checklist, incident response stepper.
- Restaurant: menu filter, allergen toggle, reservation widget, gallery.
- Government: service search, form finder, document filter, alert controls.
- Luxury: private enquiry reveal, membership request, concierge stepper.

Rules:

- No critical content may rely on JS-only rendering.
- Navigation, CTAs, forms, contact routes, and legal pages must work without custom JS.
- Reduced motion must disable non-essential animation.
- Track interactions with neutral custom events only after consent where analytics is added.

### Phase 6: Asset And Image Direction

Every site gets a visual asset brief:

- Photo style and crop rules.
- Required image ratios.
- Overlay or no-overlay rule.
- Icon style.
- Pattern/texture/material direction.
- OG image treatment.
- What imagery to avoid.

Use local assets only in final deliverables. Do not rely on remote images.

### Phase 7: QA And Acceptance

For each site, verify:

- All 10 core pages exist and keep 10 sections.
- Utility pages exist: privacy, cookies, terms, accessibility, sitemap, thanks, 404.
- Header, footer, mobile menu, hero, cards, forms, pricing, resources, FAQ, CTA, legal, cookie banner, and print styles match the site's unique design system.
- Desktop, tablet, and mobile screenshots show no overlap or broken text.
- Forms validate and route correctly.
- Cookie banner works.
- Keyboard navigation and focus states are visible.
- Reduced-motion works.
- Print CSS removes chrome and prints readable content.
- SEO metadata, canonical URLs, sitemap, robots, manifest, OG image, and schema are valid.
- `docs/theme-guide.md`, `docs/cross-site-diversity-report.md`, `docs/qa-report.md`, `docs/handoff.md`, and `docs/wordpress-export.md` are updated.

## Implementation Waves

Work in waves so each pass changes one type of design layer across all 50 sites before deeper polishing.

| Wave | Scope | Output |
|---|---|---|
| 1 | Audit and matrix lock | Similarity report with collisions and approved design DNA per site |
| 2 | Token expansion | Complete unique token block for every `css/styles.css` |
| 3 | Header, footer, mobile menu | 50 distinct navigation systems and footer systems |
| 4 | Hero and section rhythm | 50 distinct home-page first impressions and page pacing models |
| 5 | Cards, resources, pricing, FAQ | Distinct reusable component families per industry |
| 6 | Forms and CTA patterns | Industry-specific form flows, CTA language, and consent states |
| 7 | JavaScript behaviours | Theme-specific progressive enhancements per site |
| 8 | Utility pages and cookie/legal treatment | Legal, cookies, accessibility, 404, sitemap, thanks pages aligned to each brand |
| 9 | Asset and image refresh | Local image/icon/OG direction applied consistently |
| 10 | QA, docs, WordPress notes | Screenshots, validation, docs, export notes, and final acceptance |

## Per-Site Design Targets

| # | Site | Design System Target | Layout And Component Direction | JS Signature |
|---|---|---|---|---|
| 01 | Healthcare | Calm clinical care system with soft humanist type, white/blue/sage palette, rounded reassuring surfaces. | Appointment header, patient journey hero, reassurance cards, pathway pricing, care-route footer. | Appointment pathway, service filter, reassurance FAQ. |
| 02 | Life Sciences | Research institution system with precise typography, lab whites, blue/violet data accents, dossier surfaces. | Pipeline timeline hero, publication archive footer, evidence cards, trial eligibility form. | Pipeline tabs, publication filters, trial eligibility toggle. |
| 03 | Wellness | Warm routine-led lifestyle system with rounded type, soft neutrals, sage and clay accents. | Routine builder hero, soft service cards, journal footer, service-fit form. | Routine builder, service fit quiz, package toggle. |
| 04 | Technology | Operational infrastructure system with grid discipline, topology visuals, cool blue/teal status colours. | System topology hero, support header, infrastructure modules, ticket route form. | Support plan comparison, status cards, ticket route selector. |
| 05 | SaaS | Product-led dashboard system with clean UI typography, digital blues/greens, modular product surfaces. | Dashboard mockup hero, feature modules, pricing toggle, resource hub footer. | Pricing toggle, feature tabs, integration filter. |
| 06 | Telecommunications | Coverage and availability system with map surfaces, signal lines, speed/coverage colour logic. | Coverage map hero, availability header, coverage tiles, address check form. | Coverage checker, plan filter, outage alert panel. |
| 07 | Cybersecurity | Dark command-centre system with sharp panels, terminal labels, acid green and risk red accents. | Threat command hero, incident header, risk panels, secure audit form. | Risk matrix, compliance checklist, incident response stepper. |
| 08 | Data Analytics | KPI workbench system with dashboard density, chart cards, analytic blue and amber signal colours. | KPI dashboard hero, metric cards, data library footer, brief form. | Dashboard tabs, KPI filters, tool stack selector. |
| 09 | Finance | Restrained trust system with navy/ivory/gold, clear risk language, formal but readable typography. | Advisory calculator hero, regulated header, advisory cards, legal/trust footer. | Route selector, calculator estimate, risk toggles. |
| 10 | Insurance | Protection comparison system with calm blues, claims pathway visuals, practical policy components. | Claims pathway hero, quote/claims header, cover comparison cards, quote logic form. | Cover comparison, claims stepper, quote form logic. |
| 11 | Legal | Formal private case system with document structure, serif/sans discipline, discreet gold/charcoal accents. | Case route hero, jurisdiction footer, checklist cards, case type form. | Case type selector, document checklist, consultation route. |
| 12 | Accounting | Deadline-control system with ledgers, compact spacing, tax/calendar cues, green/yellow alert colours. | Deadline hero, filing header, deadline cards, document checklist form. | Deadline calendar, document checklist, package comparison. |
| 13 | Consulting | Executive framework system with roadmaps, diagnosis modules, boardroom restraint, strategic blue/amber. | Strategy framework hero, advisory header, framework cards, insight footer. | Diagnostic quiz, framework tabs, case filter. |
| 14 | Education | Progress pathway system with supportive clarity, course levels, warm learning colours, accessible density. | Learning path hero, school header, course path cards, placement form. | Level selector, course filter, timetable interaction. |
| 15 | Recruitment | Dual-audience talent system with employer/candidate split, human imagery, career-route components. | Split hero, talent header, audience cards, role routing form. | Employer/candidate toggle, role filter, CV upload flow. |
| 16 | Real Estate | Local property search system with map/listing rhythm, warm neutrals, area guide surfaces. | Property search hero, listing cards, map-style area blocks, valuation form. | Property filter, gallery modal, area cards. |
| 17 | Construction | Strong project-delivery system with hard edges, site-work colours, before/after proof modules. | Project timeline hero, build stage cards, handover footer, estimate form. | Project estimator, before/after slider, photo upload. |
| 18 | Architecture | Spatial editorial system with large imagery, thin rules, project index, material restraint. | Architectural masthead, large project cards, project index footer, brief form. | Project gallery, planning stepper, image reveal. |
| 19 | Interiors | Tactile moodboard system with swatches, material cards, warm refined palette, room selectors. | Moodboard hero, material swatch cards, materials footer, style brief form. | Moodboard filter, room selector, material palette. |
| 20 | Manufacturing | Industrial specification system with dense capability blocks, hard panels, orange/steel accents. | Factory floor hero, spec cards, capability footer, RFQ form. | Capability filter, spec table toggle, facility gallery. |
| 21 | Engineering | Validated technical system with diagrams, compliance blocks, precise spacing, teal/cyan accents. | System diagram hero, validation cards, technical footer, scope form. | Diagram tabs, compliance checklist, project filter. |
| 22 | Energy | Savings and output system with calculator-first layout, green/yellow power palette, metric counters. | Savings calculator hero, output metric cards, project footer, bill form. | Savings estimator, battery/solar toggle, output counters. |
| 23 | Utilities | Civic essential-service system with alert bars, practical forms, high readability, service access tiles. | Service access hero, public alert header, request tiles, public footer. | Service request finder, alert banner, report filter. |
| 24 | Environmental | ESG evidence system with impact metrics, field/report visuals, green/cyan scientific palette. | Impact report hero, metric cards, report archive footer, audit form. | Contextual filters, proof interactions, form routing. |
| 25 | Agriculture | Seasonal rural system with practical product/advice rhythm, earth/green palette, calendar cues. | Seasonal planner hero, product cards, seasonal footer, visit/order form. | Seasonal calendar, product filter, advice route selector. |
| 26 | Food Production | Ingredient and stockist system with shelf/product structure, allergen clarity, warm food palette. | Product shelf hero, ingredient cards, stockist footer, trade enquiry form. | Product/allergen filter, stockist finder, recipe tabs. |
| 27 | Restaurant | Sensory booking-first system with close food imagery, warm red/olive/wine palette, menu rhythm. | Food hero, reservation header, menu item cards, hours/location footer. | Menu filter, allergen toggle, reservation widget, gallery. |
| 28 | Hotel | Stay booking system with room cards, offer bands, amenity proof, hospitality blues and warm accents. | Room booking hero, hotel header, room cards, stay support footer. | Booking filters, form routing, room/gallery reveal. |
| 29 | Travel | Destination editorial system with places, stories, itineraries, map textures, vivid travel accents. | Destination masthead, trip cards, destination footer, planner form. | Trip finder, destination filter, itinerary accordion. |
| 30 | Transport | Route and fleet system with timetable logic, safe movement palette, fare/route modules. | Route booking hero, route cards, fleet footer, fare estimate form. | Route selector, fare estimate, fleet filter. |
| 31 | Logistics | Tracking command system with network maps, compact status cards, warehouse/route visuals. | Tracking hero, tracking cards, network footer, quote calculator form. | Tracking mockup, quote calculator, network map filter. |
| 32 | Automotive | Showroom performance system with inventory filters, dark polish, bold vehicle cards, finance modules. | Showroom search hero, vehicle cards, service bay footer, test-drive form. | Inventory filter, finance calculator, test-drive form. |
| 33 | Aviation | Premium operations system with fleet/spec precision, safety documentation, dark/navy technical surfaces. | Flight operations hero, fleet spec cards, compliance footer, charter form. | Fleet spec tabs, safety checklist, charter route form. |
| 34 | Maritime | Port operations system with vessel cards, cargo routes, marine blue/teal palette, schedule logic. | Port operations hero, vessel cards, port footer, cargo quote form. | Vessel filter, port schedule, cargo quote form. |
| 35 | Retail | Shopfront offer system with product/category rhythm, loyalty emphasis, warm commerce palette. | Shopfront hero, product cards, store finder footer, loyalty form. | Product/category filter, loyalty signup, store finder. |
| 36 | E-commerce | Marketplace catalogue system with seller/customer routes, trust badges, modular product grids. | Marketplace search hero, catalogue cards, seller footer, support routing form. | Catalogue filter, seller/customer routing. |
| 37 | Fashion | Editorial campaign system with dramatic imagery, lookbook movement, strong collection rhythm. | Lookbook campaign hero, lookbook cards, stockist footer, styling form. | Lookbook slider, size guide, collection filter. |
| 38 | Beauty | Texture and routine system with product education, soft capsules, ingredient/routine surfaces. | Routine finder hero, product education cards, ingredient footer, advice form. | Routine finder, ingredient glossary, product filter. |
| 39 | Media | Broadcast schedule system with show grids, audience/ad kit surfaces, schedule-forward layout. | Broadcast schedule hero, episode cards, audience footer, advertise form. | Show schedule filter, episode cards, ad kit download. |
| 40 | Entertainment | High-energy ticket system with dark stage palette, event cards, artist filters, motion-led CTAs. | Ticket stage hero, event cards, venue footer, ticket enquiry form. | Event calendar, ticket selector, artist filter. |
| 41 | Publishing | Knowledge archive system with library/search structure, article cards, author filters, paper surfaces. | Library masthead, article cards, archive footer, newsletter form. | Library search, author filter, newsletter modal. |
| 42 | Marketing | Campaign/results system with case-study modules, creative strategy language, result tabs. | Campaign case hero, case cards, agency header, brief form. | Case study filter, result tabs, brief form. |
| 43 | Creative | Studio portfolio system with project wall, lightbox, file/brief routes, visual production surfaces. | Portfolio wall hero, portfolio cards, project footer, creative brief form. | Portfolio filter, project lightbox, file/brief upload. |
| 44 | Sports | Energy and schedule system with class timetables, coach selectors, progress/community proof. | Class schedule hero, program cards, community footer, trial form. | Timetable filter, membership toggle, coach selector. |
| 45 | Events | Emotional planning system with moodboards, venue/supplier proof, package/date enquiry flow. | Event moodboard hero, portfolio cards, venue footer, date enquiry form. | Event type selector, venue filter, package calculator. |
| 46 | Government | Plain civic service system with high contrast, service search, alert controls, simple square containers. | Public service search hero, service tiles, directory footer, request form. | Service search, form finder, document filter, alert controls. |
| 47 | Nonprofit | Transparent impact system with donation routes, urgency without clutter, human proof, clear outcome cards. | Donation impact hero, impact cards, donation footer, donation form. | Donation selector, impact calculator, volunteer filter. |
| 48 | Veterinary | Caring/emergency care system with warm clinical palette, urgent route controls, care guide cards. | Emergency care hero, care cards, care guide footer, appointment form. | Emergency symptom helper, appointment form, care guide filter. |
| 49 | Luxury | Quiet maison system with black/ivory/champagne, huge whitespace, private invitation components. | Private invitation hero, editorial object cards, concierge footer, private enquiry form. | Private enquiry reveal, membership request, concierge stepper. |
| 50 | Personal Brand | Authority media-kit system with editorial typography, press assets, speaking/newsletter routes. | Media kit hero, media cards, press kit footer, booking form. | Media filter, speaking topic selector, press kit download. |

## Batch Acceptance Checklist

Before a batch is accepted, answer yes to each item:

- Does every site in the batch have a complete token system with distinct values?
- Can each site's header be identified without seeing the logo?
- Can each site's hero be identified without reading the copy?
- Are cards, buttons, form fields, pricing, FAQ, resources, cookie banner, and utility pages visually different from the other sites in the batch?
- Does mobile navigation have a theme-appropriate behaviour and layout?
- Does each site have at least three visible, industry-specific progressive enhancements?
- Are all interactions still usable without custom JS?
- Are screenshots clean at desktop, tablet, and mobile widths?
- Are docs updated so future edits preserve the difference?

## Suggested First Batch

Start with five sites that deliberately stress different design modes:

1. `01-healthcare`: soft clinical care.
2. `07-cybersecurity`: dark command centre.
3. `18-architecture`: spatial editorial portfolio.
4. `27-restaurant`: sensory reservation-first hospitality.
5. `46-government`: plain civic service portal.

This first batch proves that the same static build standard can support radically different executions before scaling the method across the remaining 45 sites.
