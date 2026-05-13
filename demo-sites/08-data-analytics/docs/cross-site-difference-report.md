# Cross-Site Difference Report

| Register Field | Value |
| --- | --- |
| Site number | 08 |
| Industry | Data, Analytics & Business Intelligence |
| Theme name | PrismBI |
| Layout archetype | Context layer data workspace |
| Typography system | Georgia display with Inter body and "Segoe UI" accent labels |
| Colour system | #f7f1e7, #2357ff, #25d0a3, #151a2d, #ffb84d |
| Surface style | Context-layer data site with warm surfaces, blue product depth, and collaborative metadata cards |
| Asset style | Data catalogues, lineage graphs, metadata workspaces |
| Header type | Data product header |
| Mobile menu type | Primary-reference mobile navigation |
| Footer type | data library footer |
| Hero type | Metadata dashboard hero |
| Card style | Collaborative data cards |
| Form style | Dashboard planning form |
| Pricing style | reporting packages |
| FAQ style | technical proof/support accordion |
| Resource style | Primary-reference resource rhythm |
| Gallery style | Data catalogues, lineage graphs, metadata workspaces gallery or visual strip |
| JS signature | Dashboard tabs, KPI filters, tool stack selector |
| Motion style | Dashboard stack reveal |
| Conversion flow | Metadata dashboard hero |
| What this site must not resemble | 15, 25, 41 |
| Similarity risk | low with required visual QA against avoid-list sites |
| Difference score | 5 |
| QA notes | compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance |

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: 5.

## Static Authorship Pass

This site folder is now treated as the editable static source for `PrismBI`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Atlan` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

PrismBI now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Atlan inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Plan Dashboard`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Prism`, shaped by `Context layer data workspace`, `Collaborative data cards`, `Dashboard tabs, KPI filters, tool stack selector`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Prism` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
