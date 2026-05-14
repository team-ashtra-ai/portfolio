# Inspiration Audit

## Core Instruction

Do not design this ASH-TRA website from one visual template. Page names and section names are fixed by the matrix, so difference must come from research, layout archetype, partials, CSS system, JS behaviour, asset direction, mobile pattern, and conversion pattern.

## Primary User-Specified Inspiration

The strongest visual translation target for this site is Snohetta: https://snohetta.com/.

Use this target for recognizable design-language pressure: page rhythm, header attitude, colour temperature, surface shape, hero emphasis, CTA posture, motion feel, and interaction priority. Keep ASH-TRA branding, existing copy, local generated assets, and original implementation.

## Reference Mix

Required mix: 3 direct industry references, 2 adjacent industry references, 2 contrast references, and 1 interaction/UI pattern reference.

Actual mix:

- Direct references: 3
- Adjacent references: 2
- Contrast references: 2
- Interaction/UI references: 1
- Total references: 8

| Type | Reference | URL |
| --- | --- | --- |
| direct | Snohetta | https://snohetta.com/ |
| direct | BIG | https://big.dk |
| direct | Foster and Partners | https://www.fosterandpartners.com |
| adjacent | Dezeen | https://www.dezeen.com |
| adjacent | Heatherwick Studio | https://www.heatherwick.com |
| contrast | Aesop | https://www.aesop.com |
| contrast | Aman | https://www.aman.com |
| interaction | Mobbin portfolio gallery patterns | https://mobbin.com |

## Non-Copy Rule

These references are research inputs, not source material. Do not copy code, copy, logos, images, brand assets, exact layouts, exact animations, or proprietary identity.

Inspired by these patterns, this ASH-TRA site will use an original design system with different branding, copy, layout, CSS, assets, and interactions.

## Static Authorship Pass

This site folder is now treated as the editable static source for `AtelierGrid`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `Snohetta` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

AtelierGrid now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Snohetta inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Flow Cleanup Pass - 2026-05-13

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Discuss Project`.
- The former public homepage atlas was removed so the homepage follows the approved section order directly from Hero into the first content section.
- The hero secondary CTA and shortcut chips now point to real homepage sections instead of an inserted route-index block.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `journey` for `Craft`, shaped by `Spatial project index`, `Architectural index cards`, `Project gallery, planning stage stepper, image reveal`, and `editorial` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Craft` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- One-word section headings were rewritten into decision-focused labels so each page scans like a designed journey rather than a content matrix.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.


## Portfolio Design Refactor Pass - 2026-05-13

- The former public homepage route index is removed so the homepage follows the approved `Architecture, Planning & Built Environment` section flow directly from hero into the first content section.
- The repeated signature widget is visually suppressed to remove duplicated Start/Review/Book panels and reduce hero/section clutter while preserving the static HTML, JS, and routing surface.
- Visible SVG placeholder labels such as asset-type/local-asset annotations were removed so hero and card visuals read as finished industry artwork instead of asset inventory screens.
- Site-local CSS now tightens vertical rhythm, restores real hero grid columns, prevents full-bleed visual layers from sitting over copy, improves card padding, CTA hierarchy, form spacing, FAQ spacing, footer wrapping, and responsive grid collapse across mobile, tablet, desktop, and ultrawide widths.
- The pass keeps the approved references, local assets, page structure, and cross-site difference score while improving visible polish and reducing template-generated repetition.


## Homepage Premium UX Refactor Pass - 2026-05-13

- The homepage now preserves the 10-section flow by removing the extra Important notes section from `index.html`; legal/disclaimer context remains available through utility pages and footer routes.
- The hero is reduced to one eyebrow, one H1, one short lead, and exactly two actions: the site primary CTA plus one secondary Explore route. Repeated hero shortcut navs, proof chips, signature controls, target-stage UI text, and figcaptions were removed from the homepage hero and source hero partial.
- The local homepage hero image set was regenerated as no-visible-text `editorial gallery` artwork for desktop, tablet, and mobile. The image direction remains tied to `Architecture photography, plans, models, site context` and does not copy any reference asset.
- Site-local CSS now strengthens premium visual hierarchy, responsive section balance, equal-height card/media groups, readable H1-H6 rhythm, button icon affordances, hover/reveal transitions, and high-contrast footer treatment.
- The pass keeps the approved 8-reference transformation pack and cross-site difference score target of 4-5 while addressing visible polish, proportion, and readability issues.
