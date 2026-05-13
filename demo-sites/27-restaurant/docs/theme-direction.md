# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | Sketch London (https://sketch.london/) |
| Layout archetype | Surreal reservation stage |
| Header | Reservation theatre header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | location and hours footer |
| Typography | "Palatino Linotype" display with "Trebuchet MS" body and Aptos accent labels |
| Colour/surface | #f8d7e8, #1b1b1b, #f2c94c, #7b406c, #ffffff; Restaurant experience with surreal pastel rooms, dramatic menus, and reservation focus |
| Hero | Pastel dining-room hero |
| Section rhythm | image-rich density with varied composition and Room-scene reveal |
| Cards | Ornate menu cards |
| Forms | Reservation form |
| CTA flow | Primary-reference CTA hierarchy using Reserve Table using `Reserve Table` |
| Assets | Dining rooms, plates, cocktails, theatrical interiors |
| JS interactions | Menu filter, allergen toggle, reservation widget, gallery |
| Motion | Room-scene reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `TableFlame`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `hospitality` footer pattern for the `Sketch London` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

TableFlame now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Sketch London inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Reserve Table`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `shelf` for `Table`, shaped by `Surreal reservation stage`, `Ornate menu cards`, `Menu filter, allergen toggle, reservation widget, gallery`, and `hospitality` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Table` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
