# Cross-Site Difference Report

| Register Field | Value |
| --- | --- |
| Site number | 47 |
| Industry | Nonprofit, Charity & Social Impact |
| Theme name | CommonGood |
| Layout archetype | Transparent donation impact flow |
| Typography system | "Arial Narrow" display with Verdana body and Inter accent labels |
| Colour system | #ffffff, #ffc907, #2b6cb0, #111111, #ffc907 |
| Surface style | Nonprofit with yellow urgency, human impact proof, and donation clarity |
| Asset style | Community photos, water projects, donor reports, maps |
| Header type | Donation campaign header |
| Mobile menu type | Primary-reference mobile navigation |
| Footer type | impact footer |
| Hero type | Yellow impact hero |
| Card style | Impact story cards |
| Form style | Donation form |
| Pricing style | donation impact cards |
| FAQ style | professional proof/support accordion |
| Resource style | Primary-reference resource rhythm |
| Gallery style | Community photos, water projects, donor reports, maps gallery or visual strip |
| JS signature | Donation selector, impact calculator, volunteer role filter |
| Motion style | Impact counter reveal |
| Conversion flow | Yellow impact hero |
| What this site must not resemble | 04, 14, 30 |
| Similarity risk | low with required visual QA against avoid-list sites |
| Difference score | 4 |
| QA notes | compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance |

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: 4.

## Static Authorship Pass

This site folder is now treated as the editable static source for `CommonGood`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `charity: water` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

CommonGood now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the charity: water inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Donate Today`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `shelf` for `Good`, shaped by `Transparent donation impact flow`, `Impact story cards`, `Donation selector, impact calculator, volunteer role filter`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Good` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
