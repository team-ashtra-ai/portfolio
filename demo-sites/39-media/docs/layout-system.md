# Layout System

This site will not reuse the same layout structure as the previous sites.

This site will not use the same hero-card-grid-FAQ-CTA rhythm unless redesigned completely.

## Layout Difference Plan

| Layer | Rule |
| --- | --- |
| Overall layout archetype | Neon editorial news grid |
| Page width system | uses --container-sm/md/lg/xl/fluid with per-site values in css/styles.css |
| Container system | Neon editorial news grid containers with compact density |
| Section rhythm | paced around Ticker and story reveal and varied section composition |
| Grid/column structure | Angled story cards and Angled story cards control grid emphasis |
| Asymmetry rules | each page rotates at least one asymmetric, full-bleed, sticky, or report-led section |
| Full-bleed rules | allowed for Angular media hero, gallery, proof, and CTA moments only |
| Boxed/split rules | boxed surfaces use Media system with black surfaces, neon accents, angular modules, and dense story grids; split sections must not repeat image-left/text-right by default |
| Sidebar/sticky rules | use only on resource, proof, contact, pricing, or utility pages when it supports conversion |
| Overlap/negative space | controlled by compact spacing and not copied from avoid-list sites |
| Visual hierarchy | Verdana display with "Segoe UI" body and Inter accent labels plus clear primary/secondary CTA hierarchy |
| Page density | compact |

## Page-By-Page Layout Plan

| Page | Goal | Presentation Type | Hero Type | Section Order | Media/Background | CTA Style | JS Behaviour | Mobile Behaviour |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Home | establish the brand system, orient the buyer, and move the visitor to the primary conversion route | form-led | Angular media hero | Hero, Promise, Featured, Shows, Schedule, Audience, Advertise, Trust, Questions, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Network | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | map-led | Angular media hero adapted to network | Hero, Mission, Team, Standards, Audience, Reach, Values, Voice, Trust, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Shows | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | catalogue-led | Angular media hero adapted to shows | Hero, Programs, Episodes, Hosts, Topics, Archive, Clips, Schedule, Watch, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Content | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | map-led | Angular media hero adapted to content | Hero, Video, Audio, Articles, Categories, Featured, Latest, Popular, Related, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Schedule | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | timeline-led | Angular media hero adapted to schedule | Hero, Programming, Days, Times, Live, Reminders, Events, Updates, Subscribe, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Advertise | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | report-led | Angular media hero adapted to advertise | Hero, Audience, Formats, Packages, Metrics, Campaigns, Proof, Kit, Contact, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Press | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | catalogue-led | Angular media hero adapted to press | Hero, Kit, Logos, Bios, Releases, Photos, Mentions, Media, Download, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Careers | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | map-led | Angular media hero adapted to careers | Hero, Roles, Culture, Internships, Departments, Requirements, Benefits, Steps, Apply, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| FAQ | answer a specific media, broadcasting & digital content buyer question with audience-first media programming and route to Advertise With Us | gallery-led | Angular media hero adapted to faq | Hero, Access, Submissions, Advertising, Rights, Accounts, Usage, Support, Contact, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |
| Contact | convert qualified visitors through the Advertise kit form with clear privacy and follow-up expectations | map-led | Angular media hero adapted to contact | Hero, Editorial, Advertising, Support, Press, Form, Routing, Response, Submit, CTA | Media system with black surfaces, neon accents, angular modules, and dense story grids with News cards, studio images, episode panels, neon lines | Advertise With Us via Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download where useful | mobile layout follows Primary-reference mobile navigation |

## Page Template Transformation Plan

| Template | Hero Type | Section Pattern | Component Mix | Asset Style | CTA Rhythm | JS/Mobile Behaviour |
| --- | --- | --- | --- | --- | --- | --- |
| Home | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Company/About | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Services | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Specific offer/product/listing | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Process/Method/Journey | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Results/Proof/Portfolio | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Pricing | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Resources/Blog/Journal | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| FAQ/Questions | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Contact/Booking/Quote | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Legal/Utility | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |
| Error/Thanks | Angular media hero or a lighter derivative | Neon editorial news grid with compact density | Angled story cards; Primary-reference resource rhythm; sponsorship cards | News cards, studio images, episode panels, neon lines | Primary-reference CTA hierarchy using Advertise With Us | Show schedule filter, episode cards, advertise kit download |

## Section Composition Library

Uses:
- filter grid
- product shelf
- FAQ accordion
- quote/testimonial block
- process ladder
- document checklist
- CTA banner
- sticky sidebar section
- case-study block
- full-bleed image

Avoids unless redesigned:
- gallery wall
- quote/testimonial block
- form panel
- case-study block
- card grid

## Static Authorship Pass

This site folder is now treated as the editable static source for `WaveCast`. The duplicate secondary header route strip was removed from the static HTML, and the footer markup/CSS was rewritten directly in the site files using the `editorial` footer pattern for the `The Verge` inspiration direction. Future edits should happen in this site folder rather than regenerating shared templates.

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.

## Portfolio Section Component Pass - 2026-05-11

WaveCast now treats every main-body section as a static, WordPress-ready component with a component ID, section type, layout variation, pattern family, mobile stacking rule, and editable field map. The pass keeps the The Verge inspiration as a principle reference only while using original local markup, CSS, JS, and assets. Repeated section names are deliberately varied so Hero, Services, Process, Results, FAQ, Contact, and CTA patterns do not collapse into one shared layout.


## Homepage Atlas Pass - 2026-05-12

- Homepage content now remains hero-first and CTA-final; the notes/disclaimer block is placed before the final CTA so the page closes on `Advertise With Us`.
- The hero secondary CTA scrolls to `#site-atlas`, and the atlas links every core page plus support, legal, sitemap, recovery, and asset-system routes.
- Homepage section text links now route deeper into the site instead of looping back to Home.
- Atlas variant: `civic` for `Wave`, shaped by `Neon editorial news grid`, `Angled story cards`, `Show schedule filter, episode cards, advertise kit download`, and `professional` mobile behaviour.
- No new external inspiration was added; the existing reference pack remains the source for layout, header, navigation, footer, typography, colour, cards, forms, assets, motion, mobile behaviour, and non-copy rules.


## Portfolio Visual QA Pass - 2026-05-12

- Section copy was tightened so reusable blocks explain `Wave` with clearer role, proof, fit, and next-step language instead of repeated placeholder patterns.
- Generic card labels were replaced with section-purpose labels across services, trust, results, editorial, FAQ, and CTA blocks.
- CSS now keeps screenshot and no-JS states visible, disables problematic `content-visibility` reservations for portfolio review, prevents horizontal overflow, and avoids awkward mid-word breaks.
- The pass preserves each site's existing inspiration pack, local assets, component families, section rhythm, and cross-site identity while improving presentation quality across all pages.
