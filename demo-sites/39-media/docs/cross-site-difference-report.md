# Cross-Site Difference Report

| Register Field | Value |
| --- | --- |
| Site number | 39 |
| Industry | Media, Broadcasting & Digital Content |
| Theme name | WaveCast |
| Layout archetype | Neon editorial news grid |
| Typography system | Verdana display with "Segoe UI" body and Inter accent labels |
| Colour system | #0b0b13, #e2127a, #fff200, #ffffff, #00d4ff |
| Surface style | Media system with black surfaces, neon accents, angular modules, and dense story grids |
| Asset style | News cards, studio images, episode panels, neon lines |
| Header type | Neon media header |
| Mobile menu type | Primary-reference mobile navigation |
| Footer type | audience footer |
| Hero type | Angular media hero |
| Card style | Angled story cards |
| Form style | Advertise kit form |
| Pricing style | sponsorship cards |
| FAQ style | professional proof/support accordion |
| Resource style | Primary-reference resource rhythm |
| Gallery style | News cards, studio images, episode panels, neon lines gallery or visual strip |
| JS signature | Show schedule filter, episode cards, advertise kit download |
| Motion style | Ticker and story reveal |
| Conversion flow | Angular media hero |
| What this site must not resemble | 06, 22, 46 |
| Similarity risk | low-medium around shared static utility pages |
| Difference score | 4 |
| QA notes | compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance |

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: 4.

## Static Authorship Pass

This site folder is now treated as the editable static source for `WaveCast`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `The Verge` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

WaveCast now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the The Verge inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Advertise With Us`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `civic` for `Wave`, shaped by `Neon editorial news grid`, `Angled story cards`, `Show schedule filter, episode cards, advertise kit download`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Wave` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
