# Premium Static Site Quality System

Reusable rulebooks and automation for premium static front-end only websites.

The system assumes plain HTML, CSS, and JavaScript deployed as static files. It rejects paid builders, paid plugins, backend application dependencies, and proprietary lock-in for core website functionality.

## Contents

- `MASTER_CHECKLIST.md`: master index and governing rules.
- `checklists/`: 30 separate comprehensive quality checklists.
- `tools/static_site_quality.py`: dependency-free Python audit and safe-fix toolkit.
- `tools/validate_transformation_packs.py`: verifies every numbered demo site has the required transformation-pack docs, source partial references, CSS tokens, and difference score.
- `tools/site-quality.config.example.json`: reusable audit/fix configuration example.
- `tools/AUTOMATION_MATRIX.md`: what the Python scripts can fix versus what requires human review.
- `tools/build_checklists.py`: generator for the checklist Markdown files.
- `REFERENCES.md`: official and authoritative baseline references used by the system.

## Use

Run an audit against a static site folder:

```bash
python3 premium-static-site-system/tools/static_site_quality.py audit ./public --base-url https://example.com --out quality-report.json --report-md quality-report.md
```

Or use a config file:

```bash
python3 premium-static-site-system/tools/static_site_quality.py --config premium-static-site-system/tools/site-quality.config.example.json audit ./public
```

Preview safe fixes:

```bash
python3 premium-static-site-system/tools/static_site_quality.py fix ./public --base-url https://example.com --site-name "Example"
```

Write safe fixes:

```bash
python3 premium-static-site-system/tools/static_site_quality.py fix ./public --base-url https://example.com --site-name "Example" --write
```

Create only support templates without rewriting existing HTML:

```bash
python3 premium-static-site-system/tools/static_site_quality.py scaffold ./public --base-url https://example.com --site-name "Example" --write
```

Regenerate checklists after editing the generator:

```bash
python3 premium-static-site-system/tools/build_checklists.py
```

Regenerate all 50 demo sites and their transformation packs:

```bash
python3 premium-static-site-system/tools/build_demo_sites.py
```

Validate that the transformation-pack contract is complete:

```bash
python3 premium-static-site-system/tools/validate_transformation_packs.py
```

Each numbered demo site also carries an inspiration-stage pack. Before visual coding, it must document at least 8 references: 3 direct industry references, 2 adjacent references, 2 contrast references, and 1 interaction or UI pattern reference. The generator writes the master pool to `premium-static-site-system/docs/inspiration-reference-library.md`.

## Automation Boundary

The Python tooling can detect and safely fix mechanical issues such as missing metadata, sitemap files, robots.txt, security header templates, image loading attributes, and target blank rel attributes. It cannot approve legal compliance, brand strength, content accuracy, accessibility conformance, or conversion quality without human review.

Audit findings include severity, checklist category, issue code, affected file/page, evidence, fixability, and how-to-fix guidance. The generated Markdown report is designed for human QA sign-off, while the JSON report is suitable for CI or repeatable checks.
