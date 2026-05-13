# Portfolio Agent Rules

When editing `demo-sites/` or `premium-static-site-system/tools/build_demo_sites.py`, keep the 50-site anti-template contract intact.

- Before building or rewriting a numbered site, update that site's full inspiration and transformation pack:
  `docs/inspiration-audit.md`, `docs/design-extraction.md`, `docs/theme-direction.md`, `docs/theme-guide.md`, `docs/layout-system.md`, `docs/partials-system.md`, `docs/component-system.md`, `docs/css-system.md`, `docs/js-system.md`, `docs/js-interaction-plan.md`, `docs/asset-system.md`, `docs/asset-direction.md`, `docs/page-section-style-map.md`, `docs/mobile-system.md`, `docs/mobile-behaviour.md`, `docs/conversion-system.md`, and `docs/cross-site-difference-report.md`.
- Each numbered site must use at least 8 inspiration references before coding: 3 direct industry references, 2 adjacent references, 2 contrast references, and 1 interaction or UI pattern reference.
- Extract principles from references only: layout archetype, header, navigation, mobile menu, footer, typography, colour/surface, hero, section rhythm, cards, forms, CTA flow, assets, image treatment, icons/illustration, JS ideas, motion, mobile behaviour, and what must not be copied.
- Do not accept a site that is only a recolour, font swap, copied partial set, repeated card grid, repeated footer, repeated hero, repeated JS experience, repeated asset style, or repeated page rhythm.
- Every numbered site must keep its own `css/styles.css`, `js/main.js`, source partials, local asset direction, mobile behaviour, and conversion flow.
- Maintain `premium-static-site-system/docs/inspiration-reference-library.md`, `premium-static-site-system/docs/50-site-diversity-register.md`, and `premium-static-site-system/docs/batch-diversity-review.md` when changing site identity, layout, components, references, or interactions.
- Run `python3 premium-static-site-system/tools/validate_transformation_packs.py` after regenerating or editing the 50-site portfolio.

Acceptance requires a cross-site difference score of 4 or 5. Scores 1, 2, and 3 fail and require redesign.
