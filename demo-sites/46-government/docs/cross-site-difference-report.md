# Cross-Site Difference Report

| Register Field | Value |
| --- | --- |
| Site number | 46 |
| Industry | Government, Public Sector & Civic Services |
| Theme name | CivicAccess |
| Layout archetype | Public service task flow |
| Typography system | "Arial Narrow" display with "Segoe UI" body and "Lucida Sans" accent labels |
| Colour system | #ffffff, #1d70b8, #ffdd00, #0b0c0c, #ffdd00 |
| Surface style | Public service with plain language, blue actions, and high-contrast forms |
| Asset style | Forms, service lists, notices, public task flows |
| Header type | GOV-style service header |
| Mobile menu type | Primary-reference mobile navigation |
| Footer type | service directory footer |
| Hero type | Plain service hero |
| Card style | Square service boxes |
| Form style | Public request form |
| Pricing style | service eligibility cards |
| FAQ style | civic proof/support accordion |
| Resource style | Primary-reference resource rhythm |
| Gallery style | Forms, service lists, notices, public task flows gallery or visual strip |
| JS signature | Service search, form finder, document filter, alert controls |
| Motion style | Minimal state reveal |
| Conversion flow | Plain service hero |
| What this site must not resemble | 03, 13, 29 |
| Similarity risk | low with required visual QA against avoid-list sites |
| Difference score | 4 |
| QA notes | compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance |

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: 4.

## Static Authorship Pass

This site folder is now treated as the editable static source for `CivicAccess`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `civic` footer pattern for the `GOV.UK Design System` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

CivicAccess now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the GOV.UK Design System inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Start Request`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Forum`, shaped by `Public service task flow`, `Square service boxes`, `Service search, form finder, document filter, alert controls`, and `civic` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Forum` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
