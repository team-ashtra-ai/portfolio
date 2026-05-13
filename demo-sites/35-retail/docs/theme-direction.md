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
