# Cross-Site Difference Report

| Register Field | Value |
| --- | --- |
| Site number | 48 |
| Industry | Pets, Animals & Veterinary Services |
| Theme name | PawHealth |
| Layout archetype | Modern clinic care flow |
| Typography system | "Arial Narrow" display with Georgia body and "Courier New" accent labels |
| Colour system | #fff7ef, #256a5e, #ffb199, #256a5e, #21413a |
| Surface style | Veterinary care with warm clinic colours, rounded forms, and friendly triage |
| Asset style | Clinic rooms, pets, care teams, appointment panels |
| Header type | Friendly clinic header |
| Mobile menu type | Primary-reference mobile navigation |
| Footer type | care guide footer |
| Hero type | Warm appointment hero |
| Card style | Rounded care cards |
| Form style | Appointment form |
| Pricing style | care plan cards |
| FAQ style | care proof/support accordion |
| Resource style | Primary-reference resource rhythm |
| Gallery style | Clinic rooms, pets, care teams, appointment panels gallery or visual strip |
| JS signature | Emergency symptom helper, appointment form, care guide filter |
| Motion style | Triage card reveal |
| Conversion flow | Warm appointment hero |
| What this site must not resemble | 05, 15, 31 |
| Similarity risk | low-medium around shared static utility pages |
| Difference score | 5 |
| QA notes | compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance |

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: 5.

## Static Authorship Pass

This site folder is now treated as the editable static source for `PawHealth`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `hospitality` footer pattern for the `Modern Animal` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

PawHealth now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Modern Animal inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Visit`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Paw`, shaped by `Modern clinic care flow`, `Rounded care cards`, `Emergency symptom helper, appointment form, care guide filter`, and `care` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Paw` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
