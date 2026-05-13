# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | Oatly (https://www.oatly.com/) |
| Layout archetype | Playful product manifesto |
| Header | Food brand header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | stockist footer |
| Typography | "Palatino Linotype" display with Georgia body and "Trebuchet MS" accent labels |
| Colour/surface | #f5ead2, #004b8d, #f26b3a, #111111, #ffdf3d; Food brand with playful packaging, chunky copy blocks, and offbeat product shelves |
| Hero | Packaging shelf hero |
| Section rhythm | image-rich density with varied composition and Poster-style reveal |
| Cards | Chunky ingredient cards |
| Forms | Trade enquiry form |
| CTA flow | Primary-reference CTA hierarchy using Request Trade Info using `Request Trade Info` |
| Assets | Cartons, ingredients, recipe panels, hand-made notes |
| JS interactions | Product/allergen filter, stockist finder, recipe tabs |
| Motion | Poster-style reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `HarvestPack`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `hospitality` footer pattern for the `Oatly` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

HarvestPack now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Oatly inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Trade Info`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Grain`, shaped by `Playful product manifesto`, `Chunky ingredient cards`, `Product/allergen filter, stockist finder, recipe tabs`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Grain` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
