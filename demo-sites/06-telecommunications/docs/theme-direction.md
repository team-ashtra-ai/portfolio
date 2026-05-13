# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | Starlink (https://www.starlink.com/) |
| Layout archetype | Space coverage landing |
| Header | Uppercase utility header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | coverage support footer |
| Typography | Inter display with Aptos body and "Trebuchet MS" accent labels |
| Colour/surface | #050505, #ffffff, #8b949e, #f5f5f5, #b8c7d9; Black space utility with full-bleed contrast, uppercase navigation, and availability CTAs |
| Hero | Black full-bleed coverage hero |
| Section rhythm | practical density with varied composition and Slow parallax and signal reveal |
| Cards | Satellite coverage cards |
| Forms | Availability checker form |
| CTA flow | Primary-reference CTA hierarchy using Check Coverage using `Check Coverage` |
| Assets | Satellite fields, night skies, coverage maps, hardware silhouettes |
| JS interactions | Coverage checker mockup, plan filter, outage alert panel |
| Motion | Slow parallax and signal reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `SignalNorth`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Starlink` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

SignalNorth now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Starlink inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Check Coverage`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `command` for `Signal`, shaped by `Space coverage landing`, `Satellite coverage cards`, `Coverage checker mockup, plan filter, outage alert panel`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Signal` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
