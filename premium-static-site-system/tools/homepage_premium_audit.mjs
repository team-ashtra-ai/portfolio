#!/usr/bin/env node
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import os from "node:os";
import fsSync from "node:fs";
import fs from "node:fs/promises";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    const npxRoot = path.join(os.homedir(), ".npm", "_npx");
    if (fsSync.existsSync(npxRoot)) {
      for (const entry of fsSync.readdirSync(npxRoot)) {
        const packagePath = path.join(npxRoot, entry, "node_modules", "playwright", "package.json");
        if (fsSync.existsSync(packagePath)) {
          return createRequire(packagePath)("playwright");
        }
      }
    }
    throw error;
  }
}
const { chromium } = loadPlaywright();

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const DEMO_ROOT = path.join(ROOT, "demo-sites");
const REPORT_ROOT = path.join(ROOT, "premium-static-site-system", "reports", "homepage-premium-audit");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const arg = process.argv[index];
  if (!arg.startsWith("--")) continue;
  const [key, value] = arg.includes("=") ? arg.split("=", 2) : [arg, process.argv[index + 1]];
  args.set(key, value && !value.startsWith("--") ? value : "true");
  if (value && !value.startsWith("--") && !arg.includes("=")) index += 1;
}

const screenshotPages = args.get("--screenshots") !== "false";
const concurrency = Math.max(1, Math.min(8, Number(args.get("--concurrency") || 4)));
const reusePage = args.get("--reuse-page") !== "false";
const reuseBatchSize = Math.max(1, Math.min(20, Number(args.get("--reuse-batch-size") || 10)));
const screenshotTimeout = Math.max(10000, Number(args.get("--screenshot-timeout") || 60000));
const onlySite = args.get("--site");
const VIEWPORTS = {
  desktop: { width: Number(args.get("--desktop-width") || 1440), height: Number(args.get("--desktop-height") || 1040), quality: 70 },
  mobile: { width: Number(args.get("--mobile-width") || 390), height: Number(args.get("--mobile-height") || 844), quality: 72 },
};

async function siteDirs() {
  const entries = await fs.readdir(DEMO_ROOT, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isDirectory() && /^\d{2}-/.test(entry.name))
    .filter((entry) => !onlySite || entry.name.startsWith(String(onlySite).padStart(2, "0")))
    .map((entry) => path.join(DEMO_ROOT, entry.name))
    .sort((a, b) => a.localeCompare(b));
}

function rel(file) {
  return path.relative(ROOT, file);
}

function safeName(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

async function readJson(file) {
  return JSON.parse(await fs.readFile(file, "utf8"));
}

function auditDom() {
  const parseColor = (value) => {
    const text = String(value || "").trim();
    const srgb = text.match(/color\(srgb\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)(?:\s*\/\s*([0-9.]+))?\)/);
    if (srgb) {
      return {
        r: Number.parseFloat(srgb[1]) * 255,
        g: Number.parseFloat(srgb[2]) * 255,
        b: Number.parseFloat(srgb[3]) * 255,
        a: srgb[4] ? Number.parseFloat(srgb[4]) : 1,
      };
    }
    const rgb = text.match(/rgba?\(([^)]+)\)/);
    if (!rgb) return null;
    const raw = rgb[1].includes(",") ? rgb[1].split(/,\s*/) : rgb[1].split(/\s+\/?\s*/);
    const parts = raw.filter(Boolean).map((part) => Number.parseFloat(part));
    if (parts.length < 3) return null;
    return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
  };
  const luminance = ({ r, g, b }) => {
    const channel = (raw) => {
      const value = raw / 255;
      return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
  };
  const contrast = (a, b) => {
    const first = luminance(a);
    const second = luminance(b);
    const lighter = Math.max(first, second);
    const darker = Math.min(first, second);
    return (lighter + 0.05) / (darker + 0.05);
  };
  const composite = (fg, bg) => {
    const alpha = fg.a + bg.a * (1 - fg.a);
    if (alpha <= 0) return { r: 255, g: 255, b: 255, a: 1 };
    return {
      r: ((fg.r * fg.a) + (bg.r * bg.a * (1 - fg.a))) / alpha,
      g: ((fg.g * fg.a) + (bg.g * bg.a * (1 - fg.a))) / alpha,
      b: ((fg.b * fg.a) + (bg.b * bg.a * (1 - fg.a))) / alpha,
      a: alpha,
    };
  };
  const visible = (el) => {
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0.05 && rect.width > 1 && rect.height > 1;
  };
  const backgroundFor = (el) => {
    const stack = [];
    let node = el;
    while (node && node.nodeType === Node.ELEMENT_NODE) {
      const color = parseColor(getComputedStyle(node).backgroundColor);
      if (color && color.a > 0.01) stack.push(color);
      node = node.parentElement;
    }
    return stack.reverse().reduce((current, color) => composite(color, current), { r: 255, g: 255, b: 255, a: 1 });
  };

  const topSections = [...document.querySelectorAll("main > section")];
  const hero = topSections[0];
  const last = topSections[topSections.length - 1];
  const heroButtons = hero ? [...hero.querySelectorAll(".hero-copy .button-row .button")].filter(visible) : [];
  const allHeroButtons = hero ? [...hero.querySelectorAll(".button")] : [];
  const forbiddenHero = hero ? [...hero.querySelectorAll(".hero-flow-links,.hero-proof,.signature-panel,.target-stage,figcaption,h2")].map((el) => {
    if (el.id) return `${el.tagName.toLowerCase()}#${el.id}`;
    return `${el.tagName.toLowerCase()}.${[...el.classList].slice(0, 3).join(".")}`;
  }) : [];
  const heroCopyText = hero?.querySelector(".hero-copy")?.innerText?.trim().replace(/\s+/g, " ") || "";
  const heroImage = hero?.querySelector(".premium-hero-picture img");
  const brokenImages = [...document.images]
    .filter((img) => !img.complete || img.naturalWidth === 0 || img.naturalHeight === 0)
    .map((img) => img.getAttribute("src"))
    .slice(0, 20);
  const viewportWidth = document.documentElement.clientWidth;
  const overflowing = [...document.body.querySelectorAll("body *")]
    .filter(visible)
    .filter((el) => !el.matches(".honeypot,[aria-hidden='true']"))
    .filter((el) => {
      const rect = el.getBoundingClientRect();
      return rect.right > viewportWidth + 3 || rect.left < -3;
    })
    .slice(0, 20)
    .map((el) => el.id ? `${el.tagName.toLowerCase()}#${el.id}` : `${el.tagName.toLowerCase()}.${[...el.classList].slice(0, 3).join(".")}`);

  const footerLowContrast = [];
  const footer = document.querySelector(".site-footer");
  if (footer) {
    const footerText = [...footer.querySelectorAll("*")]
      .filter(visible)
      .filter((el) => [...el.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0));
    for (const el of footerText) {
      const text = (el.innerText || el.textContent || "").trim().replace(/\s+/g, " ");
      if (text.length < 2) continue;
      const style = getComputedStyle(el);
      const fg = parseColor(style.color);
      const bg = backgroundFor(el);
      if (!fg || !bg) continue;
      const ratio = contrast(fg.a < 1 ? composite(fg, bg) : fg, bg);
      const size = Number.parseFloat(style.fontSize);
      const weight = Number.parseFloat(style.fontWeight);
      const required = size >= 24 || (size >= 18.66 && weight >= 700) ? 3 : 4.5;
      if (ratio + 0.05 < required) {
        footerLowContrast.push({ text: text.slice(0, 80), ratio: Number(ratio.toFixed(2)), required });
      }
      if (footerLowContrast.length >= 10) break;
    }
  }

  const issues = [];
  if (topSections.length !== 10) issues.push(`section-count-${topSections.length}`);
  if (!hero || hero.getAttribute("data-section") !== "Hero") issues.push("missing-first-hero");
  if (!last || last.getAttribute("data-section") !== "CTA") issues.push("final-section-not-cta");
  if (heroButtons.length !== 2 || allHeroButtons.length !== 2) issues.push(`hero-buttons-${heroButtons.length}/${allHeroButtons.length}`);
  if (forbiddenHero.length) issues.push("hero-extra-text-or-controls");
  if (!heroImage) issues.push("missing-premium-hero-image");
  if (heroImage && (!heroImage.complete || heroImage.naturalWidth === 0)) issues.push("broken-hero-image");
  if (heroCopyText.length > 180) issues.push(`hero-copy-too-long-${heroCopyText.length}`);
  if (brokenImages.length) issues.push("broken-images");
  if (document.documentElement.scrollWidth > viewportWidth + 3 || overflowing.length) issues.push("horizontal-overflow");
  if (footerLowContrast.length) issues.push("footer-low-contrast");

  return {
    title: document.title,
    sectionCount: topSections.length,
    firstSection: hero?.getAttribute("data-section") || "",
    lastSection: last?.getAttribute("data-section") || "",
    heroButtons: heroButtons.length,
    allHeroButtons: allHeroButtons.length,
    heroCopyLength: heroCopyText.length,
    forbiddenHero,
    heroImage: heroImage ? {
      src: heroImage.getAttribute("src"),
      naturalWidth: heroImage.naturalWidth,
      naturalHeight: heroImage.naturalHeight,
    } : null,
    brokenImages,
    overflowing,
    footerLowContrast,
    documentSize: {
      width: document.documentElement.scrollWidth,
      height: document.documentElement.scrollHeight,
    },
    issues,
  };
}

async function preparePage(page) {
  await page.evaluate(async () => {
    const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    if (!document.getElementById("codex-homepage-premium-audit")) {
      const style = document.createElement("style");
      style.id = "codex-homepage-premium-audit";
      style.textContent = [
        ".reveal-ready{opacity:1!important;transform:none!important}",
        ".portfolio-component,.content-section{content-visibility:visible!important;contain:none!important;contain-intrinsic-size:auto!important}",
        ".cookie-banner,.whatsapp-widget,.back-to-top{display:none!important}",
        "html{scroll-behavior:auto!important}",
      ].join("");
      document.head.appendChild(style);
    }
    document.querySelectorAll("img[loading='lazy']").forEach((img) => {
      img.loading = "eager";
    });
    const max = Math.min(Math.max(document.body.scrollHeight, document.documentElement.scrollHeight), 60000);
    const step = Math.max(520, Math.floor(innerHeight * 0.75));
    for (let y = 0; y < max; y += step) {
      scrollTo(0, y);
      await delay(12);
    }
    scrollTo(0, 0);
    await Promise.race([
      Promise.all([...document.images].map((img) => img.decode?.().catch(() => undefined) || Promise.resolve())),
      delay(1500),
    ]);
    await delay(100);
  });
}

async function auditOne(browser, siteDir, viewportName, viewport, outDir) {
  const config = await readJson(path.join(siteDir, "site.config.json"));
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  const record = {
    site: path.basename(siteDir),
    slug: config.slug,
    viewport: viewportName,
    file: rel(path.join(siteDir, "index.html")),
    url: pathToFileURL(path.join(siteDir, "index.html")).href,
  };
  try {
    await page.goto(record.url, { waitUntil: "load", timeout: 25000 });
    await preparePage(page);
    const audit = await page.evaluate(auditDom);
    let screenshot = "";
    if (screenshotPages) {
      const screenshotDir = path.join(outDir, "screenshots", viewportName);
      await fs.mkdir(screenshotDir, { recursive: true });
      screenshot = path.join("screenshots", viewportName, `${safeName(path.basename(siteDir))}.jpg`);
      await page.screenshot({
        path: path.join(outDir, screenshot),
        fullPage: true,
        type: "jpeg",
        quality: viewport.quality,
        animations: "disabled",
        timeout: screenshotTimeout,
      });
    }
    const heroDir = path.join(siteDir, "assets", "images", "hero");
    const heroSvgs = [
      `${config.slug}-home-hero.svg`,
      `${config.slug}-home-hero-tablet.svg`,
      `${config.slug}-home-hero-mobile.svg`,
    ];
    const svgTextFindings = [];
    for (const file of heroSvgs) {
      const text = await fs.readFile(path.join(heroDir, file), "utf8");
      if (/<text\b/i.test(text)) svgTextFindings.push(file);
    }
    if (svgTextFindings.length) audit.issues.push("hero-svg-visible-text");
    return { ...record, screenshot, audit: { ...audit, svgTextFindings } };
  } catch (error) {
    return { ...record, error: String(error.message || error) };
  } finally {
    await page.close();
    await context.close();
  }
}

async function auditWithPage(page, siteDir, viewportName, viewport, outDir) {
  const config = await readJson(path.join(siteDir, "site.config.json"));
  const record = {
    site: path.basename(siteDir),
    slug: config.slug,
    viewport: viewportName,
    file: rel(path.join(siteDir, "index.html")),
    url: pathToFileURL(path.join(siteDir, "index.html")).href,
  };
  try {
    await page.goto(record.url, { waitUntil: "load", timeout: 25000 });
    await preparePage(page);
    const audit = await page.evaluate(auditDom);
    let screenshot = "";
    if (screenshotPages) {
      const screenshotDir = path.join(outDir, "screenshots", viewportName);
      await fs.mkdir(screenshotDir, { recursive: true });
      screenshot = path.join("screenshots", viewportName, `${safeName(path.basename(siteDir))}.jpg`);
      await page.screenshot({
        path: path.join(outDir, screenshot),
        fullPage: true,
        type: "jpeg",
        quality: viewport.quality,
        animations: "disabled",
        timeout: screenshotTimeout,
      });
    }
    const heroDir = path.join(siteDir, "assets", "images", "hero");
    const heroSvgs = [
      `${config.slug}-home-hero.svg`,
      `${config.slug}-home-hero-tablet.svg`,
      `${config.slug}-home-hero-mobile.svg`,
    ];
    const svgTextFindings = [];
    for (const file of heroSvgs) {
      const text = await fs.readFile(path.join(heroDir, file), "utf8");
      if (/<text\b/i.test(text)) svgTextFindings.push(file);
    }
    if (svgTextFindings.length) audit.issues.push("hero-svg-visible-text");
    return { ...record, screenshot, audit: { ...audit, svgTextFindings } };
  } catch (error) {
    return { ...record, error: String(error.message || error) };
  }
}

async function launchBrowser() {
  return chromium.launch({
    executablePath: process.env.CHROME_PATH || "/usr/bin/google-chrome",
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
      "--disable-extensions",
      "--disable-background-networking",
      "--disable-renderer-backgrounding",
      "--disable-background-timer-throttling",
    ],
  });
}

async function main() {
  const dirs = await siteDirs();
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const outDir = path.join(REPORT_ROOT, stamp);
  await fs.mkdir(outDir, { recursive: true });

  let results = [];
  if (reusePage) {
    let completed = 0;
    for (const [viewportName, viewport] of Object.entries(VIEWPORTS)) {
      for (let offset = 0; offset < dirs.length; offset += reuseBatchSize) {
        const browser = await launchBrowser();
        try {
          const context = await browser.newContext({
            viewport: { width: viewport.width, height: viewport.height },
            deviceScaleFactor: 1,
            reducedMotion: "reduce",
          });
          const page = await context.newPage();
          try {
            for (const siteDir of dirs.slice(offset, offset + reuseBatchSize)) {
              results.push(await auditWithPage(page, siteDir, viewportName, viewport, outDir));
              completed += 1;
              if (completed % 20 === 0 || completed === dirs.length * Object.keys(VIEWPORTS).length) {
                console.log(`Audited ${completed}/${dirs.length * Object.keys(VIEWPORTS).length}`);
              }
            }
          } finally {
            await page.close().catch(() => undefined);
            await context.close().catch(() => undefined);
          }
        } finally {
          await browser.close().catch(() => undefined);
        }
      }
    }
  } else {
    const browser = await launchBrowser();
    const jobs = [];
    for (const siteDir of dirs) {
      for (const [viewportName, viewport] of Object.entries(VIEWPORTS)) {
        jobs.push({ siteDir, viewportName, viewport });
      }
    }

    results = Array(jobs.length);
    let next = 0;
    let completed = 0;
    async function worker() {
      while (next < jobs.length) {
        const index = next;
        next += 1;
        const job = jobs[index];
        results[index] = await auditOne(browser, job.siteDir, job.viewportName, job.viewport, outDir);
        completed += 1;
        if (completed % 20 === 0 || completed === jobs.length) {
          console.log(`Audited ${completed}/${jobs.length}`);
        }
      }
    }
    await Promise.all(Array.from({ length: Math.min(concurrency, jobs.length) }, () => worker()));
    await browser.close();
  }

  const failed = results.filter((item) => item.error || item.audit?.issues?.length);
  const summary = {
    generatedAt: new Date().toISOString(),
    viewports: VIEWPORTS,
    totalHomepages: dirs.length,
    totalAudits: results.length,
    auditsWithIssues: failed.length,
    screenshots: screenshotPages ? rel(path.join(outDir, "screenshots")) : "",
    outputDirectory: rel(outDir),
  };
  await fs.writeFile(path.join(outDir, "homepage-premium-audit-report.json"), `${JSON.stringify({ summary, results }, null, 2)}\n`);
  const markdown = [
    "# Homepage Premium Audit",
    "",
    `- Generated: ${summary.generatedAt}`,
    `- Homepages: ${summary.totalHomepages}`,
    `- Viewport audits: ${summary.totalAudits}`,
    `- Audits with issues: ${summary.auditsWithIssues}`,
    screenshotPages ? `- Screenshots: \`${summary.screenshots}\`` : "- Screenshots: disabled",
    "",
    "## Issues",
    "",
    failed.length ? "| Site | Viewport | Issues |" : "No issues found.",
    failed.length ? "| --- | --- | --- |" : "",
    ...failed.map((item) => `| ${item.site} | ${item.viewport} | ${(item.error ? [item.error] : item.audit.issues).join(", ")} |`),
  ].filter(Boolean).join("\n");
  await fs.writeFile(path.join(outDir, "homepage-premium-audit-summary.md"), `${markdown}\n`);
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
