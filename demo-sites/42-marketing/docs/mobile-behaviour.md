# Mobile Behaviour

| Area | Behaviour |
| --- | --- |
| Reference translation | extract task priority, tap target, and menu lessons from references without copying UI |
| Mobile menu | Primary-reference mobile navigation |
| Mobile hero | Immersive case-study hero simplified for first-screen clarity |
| Mobile section rhythm | medium density with deliberate stack, crop, or scroll decisions |
| Mobile cards | Dark campaign cards remains visually distinct in one-column or scroll treatment |
| Mobile forms | Brief form keeps labels, consent, validation, and status visible |
| Mobile CTA | `Send Campaign Brief` appears after proof and remains reachable from contact/footer |
| Mobile footer | case study footer stacks into sitemap, conversion, contact, legal, and trust areas |
| Accessibility | minimum 44px controls, visible focus, readable text, and no overlap |

## Static Authorship Pass

This site folder is now treated as the editable static source for `SignalCraft`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `AKQA` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

SignalCraft now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the AKQA inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Send Campaign Brief`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `split-index` for `Spark`, shaped by `Dark agency case system`, `Dark campaign cards`, `Case study filter, campaign result tabs, brief form`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Spark` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
