# JS Behaviour System

## Site JS Plan

| Area | Decision |
| --- | --- |
| JS purpose | progressively enhance Athletic product-program system and Big sport campaign hero |
| Interactive components | Timetable filter, membership toggle, coach selector, Big sport campaign hero, Primary-reference resource rhythm filters or archive interactions, membership cards comparison/toggle/calculator behaviour |
| Page-specific behaviours | only attach where matching sections exist; never hide core Sports, Fitness & Recreation content |
| Form behaviours | Trial class form with validation, status, honeypot, Formspree, and thanks route |
| Tracking events | neutral custom events; no personal data in event payloads |
| Cookie behaviour | Primary-reference compact consent |
| Accessibility controls | aria-expanded, focus-visible, keyboard reachable controls, reduced-motion fallback |
| Fallback behaviour | all copy, navigation, CTAs, legal pages, and forms remain readable without JS |

## Required Base JS

- mobile menu
- header scroll state
- active page state
- form validation
- Formspree submission
- cookie consent
- analytics consent
- FAQ accordion
- WhatsApp widget
- back-to-top
- scroll reveal
- CTA tracking
- download tracking
- 404 helper

## Site-Specific Optional JS

- Timetable filter, membership toggle, coach selector
- Big sport campaign hero
- Primary-reference resource rhythm filters or archive interactions
- membership cards comparison/toggle/calculator behaviour

## Static Authorship Pass

This site folder is now treated as the editable static source for `PulseClub`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `immersive` footer pattern for the `Nike` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

PulseClub now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the Nike inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Join Class`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `map` for `Pulse`, shaped by `Athletic product-program system`, `Performance program cards`, `Timetable filter, membership toggle, coach selector`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Pulse` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
