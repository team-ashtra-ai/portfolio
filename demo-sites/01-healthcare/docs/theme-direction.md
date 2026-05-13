# Theme Direction

This site will be different from the previous sites because:

| Dimension | Direction |
| --- | --- |
| Primary inspiration | Neko Health (https://www.nekohealth.com/) |
| Layout archetype | Scan-first health check journey |
| Header | Minimal scan header |
| Mobile menu | Primary-reference mobile navigation |
| Footer | care route sitemap |
| Typography | Inter display with Arial body and Didot accent labels |
| Colour/surface | #f7fbff, #101820, #20b8d8, #07141e, #d7f7ff; Clean health-tech with scan-first white space, black copy, and electric blue data accents |
| Hero | Body scan split hero |
| Section rhythm | spacious density with varied composition and Soft reveal with data-point counters |
| Cards | Rounded diagnostic data cards |
| Forms | Scan booking form |
| CTA flow | Primary-reference CTA hierarchy using Book Appointment using `Book Appointment` |
| Assets | Body-scan rooms, data visualisations, calm clinical detail |
| JS interactions | Appointment pathway, service filter, reassurance FAQ |
| Motion | Soft reveal with data-point counters |
| Mobile behaviour | Primary-reference mobile navigation |

If these differences cannot be defended before coding, the site is not ready to build.

## Static Authorship Pass

This site folder is now treated as the editable static source for `AsterCare`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `professional` footer pattern for the `Neko Health` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

AsterCare now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Neko Health inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Appointment`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `constellation` for `Aster`, shaped by `Scan-first health check journey`, `Rounded diagnostic data cards`, `Appointment pathway, service filter, reassurance FAQ`, and `care` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Aster` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
