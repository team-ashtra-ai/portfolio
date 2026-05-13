# Inspiration Audit

## Core Instruction

Do not design this ASH-TRA website from one visual template. Page names and section names are fixed by the matrix, so difference must come from research, layout archetype, partials, CSS system, JS behaviour, asset direction, mobile pattern, and conversion pattern.

## Primary User-Specified Inspiration

The strongest visual translation target for this site is Wise: https://wise.com/.

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
| direct | Wise | https://wise.com/ |
| direct | Revolut | https://www.revolut.com |
| direct | Monzo | https://monzo.com |
| adjacent | Ramp | https://ramp.com |
| adjacent | Mercury | https://mercury.com |
| contrast | Apple Card | https://www.apple.com/apple-card |
| contrast | Financial Times | https://www.ft.com |
| interaction | Mobbin finance calculator flows | https://mobbin.com |

## Non-Copy Rule

These references are research inputs, not source material. Do not copy code, copy, logos, images, brand assets, exact layouts, exact animations, or proprietary identity.

Inspired by these patterns, this ASH-TRA site will use an original design system with different branding, copy, layout, CSS, assets, and interactions.

## Static Authorship Pass

This site folder is now treated as the editable static source for `HarborLedger`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Wise` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Portfolio Section Component Pass - 2026-05-11

HarborLedger now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Wise inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Book Advisor Call`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `civic` for `Harbor`, shaped by `Green calculator flow`, `Fee transparency cards`, `Advisory route selector, calculator-style estimate, risk toggles`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Harbor` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
