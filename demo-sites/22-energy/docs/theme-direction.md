# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | Tesla Energy (https://www.tesla.com/energy) |
| Layout archetype | Minimal energy product landing |
| Header | Minimal energy header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | project output footer |
| Typography | "Palatino Linotype" display with Inter body and "Segoe UI" accent labels |
| Colour/surface | #f7f7f7, #111111, #e82127, #111111, #bfc7d5; Minimal product marketing with stark surfaces, centered copy, and energy-product proof |
| Hero | Centered product hero |
| Section rhythm | medium density with varied composition and Clean product reveal |
| Cards | Product output cards |
| Forms | Savings calculator form |
| CTA flow | Primary-reference CTA hierarchy using Calculate Savings using `Calculate Savings` |
| Assets | Solar roofs, batteries, energy app panels |
| JS interactions | Savings estimator, battery/solar toggle, project output counters |
| Motion | Clean product reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `SunVault`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Tesla Energy` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

SunVault now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Tesla Energy inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Calculate Savings`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `split-index` for `Vault`, shaped by `Minimal energy product landing`, `Product output cards`, `Savings estimator, battery/solar toggle, project output counters`, and `technical` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Vault` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
