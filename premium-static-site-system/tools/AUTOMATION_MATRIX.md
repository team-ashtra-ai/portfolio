# Automation Matrix

The Python toolkit supports audits and safe mechanical fixes for static HTML, CSS, JavaScript, and asset files. It does not claim to automatically satisfy strategic, legal, brand, accessibility conformance, or conversion-quality requirements.

## Main Commands

- `audit`: reports issues by checklist category with severity, file, evidence, and fixability.
- `fix`: previews or writes safe mechanical fixes to existing HTML and support files.
- `scaffold`: creates support files only, without rewriting existing HTML.

Reports can be written as both machine-readable JSON and human-readable Markdown:

```bash
python3 premium-static-site-system/tools/static_site_quality.py audit ./public \
  --base-url https://example.com \
  --out quality-report.json \
  --report-md quality-report.md
```

Every automated finding includes severity, category, issue code, affected file/page, evidence, fixability, and how-to-fix guidance.

## Safe Mechanical Fixes

- Missing `<!doctype html>`.
- Missing `html lang`.
- Missing `meta charset`.
- Missing responsive viewport metadata.
- Missing canonical tags when `--base-url` is provided.
- Missing homepage Open Graph and Twitter card baseline metadata.
- `target="_blank"` links missing `rel="noopener noreferrer"`.
- Missing `loading` and `decoding` image attributes.
- Missing image `width` and `height` when the local image dimensions can be detected.
- Missing `robots.txt`.
- Missing `sitemap.xml`.
- Missing `404.html`.
- Missing static host security header template.
- Missing privacy and cookie notice templates.
- Missing terms/legal template.
- Missing accessibility statement template.
- Missing human-readable sitemap page.
- Missing analytics/tracking plan template.
- Missing launch QA evidence template.
- Missing monitoring and maintenance plan template.
- Missing consent-aware analytics loader template.
- Missing baseline focus and reduced-motion CSS helper.
- Missing `site.webmanifest`.
- Missing `.well-known/security.txt` template.

## Audit-Only Findings

- Strategy, positioning, brand quality, proof quality, and content usefulness.
- Purpose clarity, target audience fit, page narrative quality, premium first impression, and trustworthiness.
- Legal compliance, privacy compliance, consent validity, and regulated claims.
- Full WCAG conformance and assistive technology quality.
- Conversion quality, user intent match, lead quality, and ethical persuasion.
- Translation quality and cultural localization.
- Visual polish, layout judgment, and screenshot-level UI quality.
- Form provider compliance, data retention, and lead routing.
- Hosting account ownership, DNS governance, and contractual provider review.

## Checklist Coverage

- Planning & Strategy: audit evidence only; no automatic fix.
- Brand Strategy: audit evidence only; no automatic fix.
- Information Architecture: broken-link, sitemap, canonical, and orphan-risk checks.
- UX: viewport, placeholder links, missing landmarks, skip-link prompts, empty links, missing CTAs, contact-route risk, form state, and navigation risk checks.
- UI: focus CSS, reduced-motion CSS, viewport, image dimensions, iframe dimensions, metadata, and asset budget checks.
- Design System: CSS custom property token prompts, focus CSS, reduced motion, CSS-size checks; deeper review is manual.
- Content Strategy: metadata, headings, duplicates, generic link/button text, placeholders, thin-risk prompts, links, and stale/example content.
- Conversion Rate Optimisation: detectable CTAs, contact routes, generic button text, form-related checks, and contact-page risks.
- Front-End Development: doctype, charset, unsafe JS patterns, console/debug statements, blocking scripts, button types, file naming, and file structure checks.
- Static Website Architecture: homepage, 404, robots, sitemap, generated support files, internal links, anchors, support pages, and standalone page checks.
- Forms & Lead Capture: labels, form actions, methods, submit controls, input types, autocomplete hints, privacy presence, staging endpoints, and HTTPS action checks.
- SEO: titles, descriptions, canonicals, robots, sitemap freshness, headings, image alt, JSON-LD, Open Graph, Twitter cards, favicon, noindex, and links.
- Local SEO: phone, schema, and NAP checks where detectable; business fact quality is manual.
- Multilingual / Internationalisation: lang, canonical, and hreflang-risk checks where detectable.
- Accessibility: lang, landmarks, headings, duplicate IDs, form labels, button/link names, iframe titles, video/audio risks, focus CSS, reduced motion, skip-link prompts, and common static defects; full conformance requires manual and assistive technology review.
- QA: broken links, broken anchors, missing assets, invalid contact links, risky public files, placeholders, and production-readiness checks.
- Performance Optimisation: asset sizes, image dimensions, image loading/decoding, iframe dimensions, video posters, blocking scripts, third-party scripts, and file size budgets.
- Analytics: script inventory, consent template, privacy/cookie-page checks, and generated tracking plan.
- Tracking Analytics: tracking domain inventory, consent-risk checks, event-plan template, and privacy-safe reporting prompts.
- Monitoring & Observability: generated reports and monitoring plan template; live monitoring must be configured externally.
- Security: risky files, secret-like values, local file paths, local/staging references, mixed content, target blank, unsafe patterns, SVG risk, external script review, iframe review, and header templates.
- Legal, Privacy & Compliance: form/tracking inventory, policy templates, terms/accessibility/cookie templates, browser storage checks, and consent prompts; legal review required.
- Hosting & Infrastructure: header templates, production URL consistency, staging/local reference checks, sitemap/robots output, and deploy-output risk checks.
- DevOps / CI-CD: dependency-free command support and JSON reports for CI.
- Asset Management: large assets, dimensions, SVG risk, external domains, and missing assets.
- CMS & No-Code Export: exported HTML/CSS/JS quality checks.
- Static Blog & Content Production: metadata, headings, links, sitemap, and duplicate checks.
- Client Handoff & Documentation: reports and generated evidence only.
- Pre-Launch / Launch / Post-Launch: pre/post audit reports and scaffolded launch support files.
- Website Audit: full baseline static audit and JSON reporting.
