# Cross-Site Difference Report

| Register Field | Value |
| --- | --- |
| Site number | 35 |
| Industry | Retail, Shops & Consumer Sales |
| Theme name | CornerGoods |
| Layout archetype | Minimal product store |
| Typography system | Aptos display with "Trebuchet MS" body and "Palatino Linotype" accent labels |
| Colour system | #f5f5f7, #1d1d1f, #0071e3, #1d1d1f, #a1a1a6 |
| Surface style | Retail minimalism with soft grey surfaces, product tiles, and clear shopping paths |
| Asset style | Product tiles, store spaces, service cards, device-like panels |
| Header type | Clean shop header |
| Mobile menu type | Primary-reference mobile navigation |
| Footer type | store finder footer |
| Hero type | Soft product shelf hero |
| Card style | Rounded product tiles |
| Form style | Store finder form |
| Pricing style | offer bundle cards |
| FAQ style | commerce proof/support accordion |
| Resource style | Primary-reference resource rhythm |
| Gallery style | Product tiles, store spaces, service cards, device-like panels gallery or visual strip |
| JS signature | Product/category filter, loyalty signup, store finder |
| Motion style | Polished product reveal |
| Conversion flow | Soft product shelf hero |
| What this site must not resemble | 02, 18, 42 |
| Similarity risk | medium if the layout falls back to generic card-grid pacing |
| Difference score | 4 |
| QA notes | compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance |

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: 4.

## Static Authorship Pass

This site folder is now treated as the editable static source for `CornerGoods`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Apple Store` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

CornerGoods now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Apple Store inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Visit Shop`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `magazine` for `Corner`, shaped by `Minimal product store`, `Rounded product tiles`, `Product/category filter, loyalty signup, store finder`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Corner` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
