# Asset Direction

| Asset Area | Decision |
| --- | --- |
| Reference translation | extract image principles from the inspiration audit but use only original/local assets |
| Image style | Villas, landscapes, spa spaces, calm interiors |
| Photo personality | Villas, landscapes, spa spaces, calm interiors |
| Texture/material | Hospitality with quiet luxury, large tranquil imagery, and restrained booking paths |
| Icon/illustration | local SVG and diagrams aligned to Hospitality with quiet luxury, large tranquil imagery, and restrained booking paths |
| Hero assets | Serene full-bleed stay hero needs a first-screen image or visual system that does not copy references |
| Section assets | section visuals must support the fixed section names while changing composition and crop rhythm |
| Resource/download assets | covers and thumbnails follow Primary-reference resource rhythm |
| Open Graph | local OG asset with original brand, no scraped or hotlinked imagery |
| License record | `docs/asset-licenses.md` and `docs/asset-inventory.md` record every generated asset; no external images are used in this build |

## Static Authorship Pass

This site folder is now treated as the editable static source for `StayHaven`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Aman` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

StayHaven now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Aman inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Check Availability`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Stay`, shaped by `Quiet retreat booking flow`, `Retreat room cards`, `Room filter, booking panel, offer selector, amenities tabs`, and `hospitality` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Stay` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
