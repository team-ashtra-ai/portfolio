# Mobile System

The mobile experience must not be the same default stack everywhere. This site uses `Primary-reference mobile navigation` and `Construction platform grid` to control mobile rhythm.

| Breakpoint/Area | Decision |
| --- | --- |
| Desktop layout | Construction platform grid with full container range |
| Large screen layout | use --container-xl for premium breathing room; avoid simply stretching cards |
| Laptop layout | dense density with no overlapping text or controls |
| Tablet layout | collapse wide grids to one or two columns based on component intent |
| Mobile layout | Primary-reference mobile navigation plus single-column content rhythm |
| Small-phone layout | short labels, full-width CTAs, no hidden critical copy |
| Mobile hero style | Worksite software hero simplified without losing proof or CTA |
| Mobile card stacking | Project control cards stacks or scrolls only when intentional |
| Mobile form behaviour | Estimate form keeps labels visible and submits to Formspree |
| Mobile CTA placement | Request Estimate appears after proof and in contact routes |
| Mobile footer structure | handover footer stacks as sitemap, contact, legal, and trust |
| Mobile image cropping | Job sites, schedule boards, build dashboards |

## Static Authorship Pass

This site folder is now treated as the editable static source for `ForgeBuild`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `product` footer pattern for the `Procore` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

ForgeBuild now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Procore inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Request Estimate`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `shelf` for `Forge`, shaped by `Construction platform grid`, `Project control cards`, `Project estimator form, before/after slider, upload photos`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Forge` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
