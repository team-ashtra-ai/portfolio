# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | Apple Store (https://www.apple.com/store) |
| Layout archetype | Minimal product store |
| Header | Clean shop header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | store finder footer |
| Typography | Aptos display with "Trebuchet MS" body and "Palatino Linotype" accent labels |
| Colour/surface | #f5f5f7, #1d1d1f, #0071e3, #1d1d1f, #a1a1a6; Retail minimalism with soft grey surfaces, product tiles, and clear shopping paths |
| Hero | Soft product shelf hero |
| Section rhythm | medium density with varied composition and Polished product reveal |
| Cards | Rounded product tiles |
| Forms | Store finder form |
| CTA flow | Primary-reference CTA hierarchy using Visit Shop using `Visit Shop` |
| Assets | Product tiles, store spaces, service cards, device-like panels |
| JS interactions | Product/category filter, loyalty signup, store finder |
| Motion | Polished product reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `CornerGoods`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Apple Store` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

CornerGoods now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Apple Store inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Visit Shop`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `magazine` for `Corner`, shaped by `Minimal product store`, `Rounded product tiles`, `Product/category filter, loyalty signup, store finder`, and `commerce` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Corner` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `Retail, Shops & Consumer Sales` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `product theatre` artwork for desktop, tablet, and mobile. The image direction remains tied to `Product tiles, store spaces, service cards, device-like panels` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
