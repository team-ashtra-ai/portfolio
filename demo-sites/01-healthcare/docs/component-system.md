# Component System

## Component Transformation Plan

| Component | Layout/Shape | Spacing | Surface | Image/Icon Usage | States | JS Behaviour | Mobile Behaviour |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hero component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | Body-scan rooms, data visualisations, calm clinical detail | hover/focus-visible/active/disabled states from css/styles.css | Appointment pathway, service filter, reassurance FAQ | single-column or horizontal scroll only when explicitly designed |
| section intro component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| service card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| feature card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| profile card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| proof card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| metric card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| pricing card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | Appointment pathway, service filter, reassurance FAQ | single-column or horizontal scroll only when explicitly designed |
| resource card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| article card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| download card | Rounded diagnostic data cards | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| FAQ component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| form component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| CTA component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| gallery component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | Body-scan rooms, data visualisations, calm clinical detail | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| testimonial/review component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| process/timeline component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| comparison component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| table component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| badge/tag component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| breadcrumb component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| legal content component | Scan-first health check journey | spacious | Clean health-tech with scan-first white space, black copy, and electric blue data accents | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |

## Explicit Reuse Prevention

- No same cards everywhere: Rounded diagnostic data cards controls card construction for this site only.
- No same FAQ everywhere: FAQ styling follows care mode and Primary-reference plain legal notes proof tone.
- No same pricing table everywhere: pricing follows consultation fees pathway.
- No same form everywhere: forms follow Scan booking form with industry-specific fields.
- No same testimonial/resource block everywhere: proof follows standards and care notes and resources follow Primary-reference resource rhythm.

## Static Authorship Pass

This site folder is now treated as the editable static source for `AsterCare`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `professional` footer pattern for the `Neko Health` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

AsterCare now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Neko Health inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Appointment`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `constellation` for `Aster`, shaped by `Scan-first health check journey`, `Rounded diagnostic data cards`, `Appointment pathway, service filter, reassurance FAQ`, and `care` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Aster` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
