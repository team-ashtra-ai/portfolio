# Component System

## Component Transformation Plan

| Component | Layout/Shape | Spacing | Surface | Image/Icon Usage | States | JS Behaviour | Mobile Behaviour |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hero component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | Cell imagery, robotic lab systems, data maps | hover/focus-visible/active/disabled states from css/styles.css | Pipeline tabs, publication filters, trial eligibility toggle | single-column or horizontal scroll only when explicitly designed |
| section intro component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| service card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| feature card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| profile card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| proof card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| metric card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| pricing card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | Pipeline tabs, publication filters, trial eligibility toggle | single-column or horizontal scroll only when explicitly designed |
| resource card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| article card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| download card | Pipeline evidence cards | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| FAQ component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| form component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| CTA component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| gallery component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | Cell imagery, robotic lab systems, data maps | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| testimonial/review component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| process/timeline component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| comparison component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| table component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| badge/tag component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| breadcrumb component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |
| legal content component | Scientific operating system dossier | compact | TechBio with dark scientific grids, microscopy panels, and pipeline evidence | icon/texture optional | hover/focus-visible/active/disabled states from css/styles.css | CTA/download tracking with no JS-only content dependency | single-column or horizontal scroll only when explicitly designed |

## Explicit Reuse Prevention

- No same cards everywhere: Pipeline evidence cards controls card construction for this site only.
- No same FAQ everywhere: FAQ styling follows technical mode and Primary-reference plain legal notes proof tone.
- No same pricing table everywhere: pricing follows trial eligibility tiers.
- No same form everywhere: forms follow Partner research form with industry-specific fields.
- No same testimonial/resource block everywhere: proof follows papers, pipeline, and ethics evidence and resources follow Primary-reference resource rhythm.

## Static Authorship Pass

This site folder is now treated as the editable static source for `HelixNova`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Recursion` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

HelixNova now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Recursion inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Discuss Research`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `split-index` for `Helix`, shaped by `Scientific operating system dossier`, `Pipeline evidence cards`, `Pipeline tabs, publication filters, trial eligibility toggle`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Helix` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
