# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | IDEO (https://www.ideo.com/) |
| Layout archetype | Editorial innovation studio |
| Header | Studio index header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | insight archive footer |
| Typography | Georgia display with Aptos body and "Arial Narrow" accent labels |
| Colour/surface | #ffffff, #111111, #ff5a1f, #111111, #0066ff; Creative consulting with editorial whitespace, bold project thinking, and case-study rhythm |
| Hero | Idea-led editorial hero |
| Section rhythm | medium density with varied composition and Project tile reveal |
| Cards | Case thinking cards |
| Forms | Brief workshop form |
| CTA flow | Primary-reference CTA hierarchy using Send Brief using `Send Brief` |
| Assets | Workshops, prototypes, research walls, creative teams |
| JS interactions | Diagnostic quiz, framework tabs, case filter |
| Motion | Project tile reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `VectorNorth`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `IDEO` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

VectorNorth now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the IDEO inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Send Brief`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `ledger` for `Vector`, shaped by `Editorial innovation studio`, `Case thinking cards`, `Diagnostic quiz, framework tabs, case filter`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Vector` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
