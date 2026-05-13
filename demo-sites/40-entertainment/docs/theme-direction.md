# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | A24 (https://a24films.com/) |
| Layout archetype | Indie film poster system |
| Header | Film studio header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | venue footer |
| Typography | Verdana display with Georgia body and Arial accent labels |
| Colour/surface | #050505, #ffffff, #c69a55, #ffffff, #e24a2e; Entertainment with black cinema mood, poster grids, and understated weirdness |
| Hero | Dark poster hero |
| Section rhythm | theatrical density with varied composition and Poster fade reveal |
| Cards | Poster event cards |
| Forms | Ticket enquiry form |
| CTA flow | Primary-reference CTA hierarchy using View Tickets using `View Tickets` |
| Assets | Film posters, stage stills, credits, audience moments |
| JS interactions | Event calendar, ticket selector, artist filter |
| Motion | Poster fade reveal |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `StageCurrent`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `A24` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

StageCurrent now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the A24 inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `View Tickets`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `private` for `Stage`, shaped by `Indie film poster system`, `Poster event cards`, `Event calendar, ticket selector, artist filter`, and `dark` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Stage` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
