# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | SSENSE (https://www.ssense.com/) |
| Layout archetype | Monochrome catalogue system |
| Header | Compact shop header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | seller support footer |
| Typography | Aptos display with "Lucida Sans" body and "Gill Sans" accent labels |
| Colour/surface | #ffffff, #000000, #777777, #000000, #d9d9d9; E-commerce with monochrome grid discipline, compact type, and catalogue authority |
| Hero | Fashion-commerce grid hero |
| Section rhythm | compact density with varied composition and Grid snap reveal |
| Cards | Monochrome product cards |
| Forms | Support routing form |
| CTA flow | Primary-reference CTA hierarchy using Browse Market using `Browse Market` |
| Assets | Product grids, editorial crops, order panels, marketplace lists |
| JS interactions | Catalogue filter, seller/customer support routing |
| Motion | Grid snap reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `MarketPulse`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `SSENSE` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

MarketPulse now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the SSENSE inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Browse Market`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Market`, shaped by `Monochrome catalogue system`, `Monochrome product cards`, `Catalogue filter, seller/customer support routing`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Market` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
