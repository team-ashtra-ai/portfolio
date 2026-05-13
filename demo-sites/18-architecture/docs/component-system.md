# Component System

## Component Transformation Plan

| Component | Layout/Shape | Spacing | Surface | Image/Icon Usage | States | JS Behaviour | Mobile Behaviour |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hero component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | Architecture photography, plans, models, site context | hover/focus-visible/active/disabled states from css/styles.css | Project gallery, planning stage stepper, image reveal | single-column or horizontal scroll only when explicitly designed |
| section intro component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| service card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| feature card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| profile card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| proof card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| metric card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| pricing card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | Project gallery, planning stage stepper, image reveal | single-column or horizontal scroll only when explicitly designed |
| resource card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| article card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| download card | Architectural index cards | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| FAQ component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| form component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| CTA component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| gallery component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | Architecture photography, plans, models, site context | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| testimonial/review component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| process/timeline component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| comparison component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| table component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| badge/tag component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| breadcrumb component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| legal content component | Spatial project index | spacious | Architecture portfolio with radical restraint, huge imagery, and project-index logic | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |

## Explicit Reuse Prevention

- No same cards everywhere: Architectural index cards controls card construction for this site only.
- No same FAQ everywhere: FAQ styling follows editorial mode and Primary-reference plain legal notes proof tone.
- No same pricing table everywhere: pricing follows stage fee cards.
- No same form everywhere: forms follow Project brief form with industry-specific fields.
- No same testimonial/resource block everywhere: proof follows portfolio and planning proof and resources follow Primary-reference resource rhythm.

## Static Authorship Pass

This site folder is now treated as the editable static source for `AtelierGrid`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `Snohetta` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

AtelierGrid now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Snohetta inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Discuss Project`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Craft`, shaped by `Spatial project index`, `Architectural index cards`, `Project gallery, planning stage stepper, image reveal`, and `editorial` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Craft` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
