# Asset Performance Report

| Area | Result |
| --- | --- |
| Format choice | SVG for illustrations, diagrams, mockups, cards, gallery, OG; PNG only for browser/app icons. |
| Loading | Hero image eager/preloaded; non-critical images lazy-loaded with width/height attributes. |
| No bloat | No base64, no remote images, no videos, no copied heavy screenshots. |
| Reusable CSS | Object-fit/aspect-ratio prevents layout shift and stretched crops. |

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.
