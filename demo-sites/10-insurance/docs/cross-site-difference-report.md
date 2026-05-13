# Cross-Site Difference Report

| Register Field | Value |
| --- | --- |
| Site number | 10 |
| Industry | Insurance, Protection & Risk Cover |
| Theme name | Shieldline |
| Layout archetype | Pink quote journey |
| Typography system | Georgia display with "Segoe UI" body and "Palatino Linotype" accent labels |
| Colour system | #fff2f7, #ff0083, #ffb3d9, #251024, #ffffff |
| Surface style | Insurance quote flow with hot pink, friendly copy, and simple white cards |
| Asset style | Quote flows, policy cards, soft character-free illustrations |
| Header type | Simple insurance header |
| Mobile menu type | Primary-reference mobile navigation |
| Footer type | policy support footer |
| Hero type | Friendly quote hero |
| Card style | Rounded policy cards |
| Form style | Quote route form |
| Pricing style | premium factors cards |
| FAQ style | professional proof/support accordion |
| Resource style | Primary-reference resource rhythm |
| Gallery style | Quote flows, policy cards, soft character-free illustrations gallery or visual strip |
| JS signature | Cover comparison, claims stepper, quote form logic |
| Motion style | Friendly step reveal |
| Conversion flow | Friendly quote hero |
| What this site must not resemble | 17, 27, 43 |
| Similarity risk | medium if the layout falls back to generic card-grid pacing |
| Difference score | 4 |
| QA notes | compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance |

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: 4.

## Static Authorship Pass

This site folder is now treated as the editable static source for `Shieldline`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Lemonade` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

Shieldline now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Lemonade inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Quote`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `private` for `Shield`, shaped by `Pink quote journey`, `Rounded policy cards`, `Cover comparison, claims stepper, quote form logic`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Shield` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
