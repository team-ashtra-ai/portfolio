#!/usr/bin/env node
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs/promises";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const DEMO_ROOT = path.join(ROOT, "demo-sites");
const REPORT_ROOT = path.join(ROOT, "premium-static-site-system", "reports", "visual-audit");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const arg = process.argv[index];
  if (arg.startsWith("--")) {
    const [key, value] = arg.includes("=") ? arg.split("=", 2) : [arg, process.argv[index + 1]];
    args.set(key, value && !value.startsWith("--") ? value : "true");
    if (value && !value.startsWith("--") && !arg.includes("=")) index += 1;
  }
}

const onlySite = args.get("--site");
const limit = args.has("--limit") ? Number(args.get("--limit")) : 0;
const width = args.has("--width") ? Number(args.get("--width")) : 1440;
const height = args.has("--height") ? Number(args.get("--height")) : 900;
const screenshotPages = args.get("--screenshots") !== "false";
const concurrency = Math.max(1, Math.min(12, args.has("--concurrency") ? Number(args.get("--concurrency")) : 1));

async function walk(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "partials" || entry.name === "assets" || entry.name === "docs") continue;
      files.push(...await walk(full));
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      files.push(full);
    }
  }
  return files;
}

function siteNumberFor(file) {
  const rel = path.relative(DEMO_ROOT, file);
  const first = rel.split(path.sep)[0];
  const match = first.match(/^(\d{2})-/);
  return match ? match[1] : "";
}

function screenshotName(file) {
  const rel = path.relative(DEMO_ROOT, file).replaceAll(path.sep, "__");
  return rel.replace(/\.html$/, ".jpg");
}

function pageLabel(file) {
  return path.relative(ROOT, file);
}

function auditScript() {
  const parseColor = (value) => {
    const text = String(value).trim();
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
    const parts = rgb[1].includes(",")
      ? rgb[1].split(/,\s*/).map((part) => Number.parseFloat(part))
      : rgb[1].split(/\s+\/?\s*/).filter(Boolean).map((part) => Number.parseFloat(part));
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
  const insideScrollableClip = (el) => {
    let node = el.parentElement;
    while (node && node !== document.body) {
      const style = getComputedStyle(node);
      if (/(auto|scroll|hidden|clip)/.test(style.overflowX) && node.scrollWidth > node.clientWidth + 2) return true;
      node = node.parentElement;
    }
    return false;
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
  const selectorFor = (el) => {
    if (el.id) return `${el.tagName.toLowerCase()}#${el.id}`;
    const classes = [...el.classList].slice(0, 3).join(".");
    return classes ? `${el.tagName.toLowerCase()}.${classes}` : el.tagName.toLowerCase();
  };
  const leafTextElements = [...document.body.querySelectorAll("body *")]
    .filter((el) => !["SCRIPT", "STYLE", "NOSCRIPT", "SVG", "PATH", "IMG", "PICTURE", "SOURCE", "META", "LINK"].includes(el.tagName))
    .filter(visible)
    .filter((el) => {
      const own = [...el.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0);
      return own || el.children.length === 0;
    });

  const lowContrast = [];
  for (const el of leafTextElements) {
    const text = (el.innerText || el.textContent || "").trim().replace(/\s+/g, " ");
    if (text.length < 2) continue;
    const style = getComputedStyle(el);
    const fg = parseColor(style.color);
    const bg = backgroundFor(el);
    if (!fg || !bg) continue;
    const ratio = contrast(fg.a < 1 ? composite(fg, bg) : fg, bg);
    const size = Number.parseFloat(style.fontSize);
    const weight = Number.parseFloat(style.fontWeight);
    const largeText = size >= 24 || (size >= 18.66 && weight >= 700);
    const required = largeText ? 3 : 4.5;
    if (ratio + 0.05 < required) {
      lowContrast.push({
        selector: selectorFor(el),
        text: text.slice(0, 90),
        ratio: Number(ratio.toFixed(2)),
        required,
        color: style.color,
        background: getComputedStyle(el).backgroundColor || getComputedStyle(document.body).backgroundColor,
      });
    }
    if (lowContrast.length >= 40) break;
  }

  const horizontalOverflow = [];
  const viewportWidth = document.documentElement.clientWidth;
  for (const el of [...document.body.querySelectorAll("body *")].filter(visible)) {
    if (el.matches(".honeypot") || insideScrollableClip(el)) continue;
    const rect = el.getBoundingClientRect();
    if (rect.right > viewportWidth + 3 || rect.left < -3) {
      horizontalOverflow.push({
        selector: selectorFor(el),
        left: Math.round(rect.left),
        right: Math.round(rect.right),
        width: Math.round(rect.width),
      });
    }
    if (horizontalOverflow.length >= 30) break;
  }

  const images = [...document.images].filter((img) => !img.complete || img.naturalWidth === 0 || img.naturalHeight === 0)
    .map((img) => ({ selector: selectorFor(img), src: img.getAttribute("src") })).slice(0, 20);

  const sections = [...document.querySelectorAll("main section")].map((section) => {
    const rect = section.getBoundingClientRect();
    return {
      id: section.id || "",
      className: section.className || "",
      top: Math.round(rect.top + scrollY),
      height: Math.round(rect.height),
      textLength: (section.innerText || "").trim().length,
    };
  });
  const verySparseSections = sections.filter((section) => section.height > 220 && section.textLength < 20).slice(0, 20);

  const header = document.querySelector(".site-header");
  const footer = document.querySelector(".site-footer");
  const nav = document.querySelector(".site-nav");
  const headerRect = header ? header.getBoundingClientRect() : null;
  const footerRect = footer ? footer.getBoundingClientRect() : null;
  const navRect = nav ? nav.getBoundingClientRect() : null;

  return {
    title: document.title,
    viewport: { width: innerWidth, height: innerHeight },
    documentSize: { width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight },
    sectionCount: sections.length,
    componentMetrics: {
      headerHeight: headerRect ? Math.round(headerRect.height) : 0,
      footerHeight: footerRect ? Math.round(footerRect.height) : 0,
      navWidth: navRect ? Math.round(navRect.width) : 0,
    },
    lowContrast,
    horizontalOverflow,
    brokenImages: images,
    verySparseSections,
    flags: {
      tallHeader: headerRect ? headerRect.height > 190 : false,
      footerMissing: !footer,
      headerMissing: !header,
      noSections: sections.length === 0,
      pageWiderThanViewport: document.documentElement.scrollWidth > viewportWidth + 3,
    },
  };
}

async function writeJson(file, value) {
  await fs.writeFile(file, `${JSON.stringify(value, null, 2)}\n`);
}

async function main() {
  const allFiles = (await walk(DEMO_ROOT))
    .filter((file) => !onlySite || siteNumberFor(file) === String(onlySite).padStart(2, "0"))
    .sort((a, b) => pageLabel(a).localeCompare(pageLabel(b)));
  const files = limit > 0 ? allFiles.slice(0, limit) : allFiles;
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const outDir = path.join(REPORT_ROOT, stamp);
  const shotDir = path.join(outDir, "screenshots");
  await fs.mkdir(shotDir, { recursive: true });

  const browser = await chromium.launch({
    executablePath: process.env.CHROME_PATH || "/usr/bin/google-chrome",
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });

  const results = Array(files.length);
  let nextIndex = 0;
  let completed = 0;
  async function auditFile(file) {
    const page = await context.newPage();
    const consoleMessages = [];
    const pageErrors = [];
    page.on("console", (message) => {
      if (["error", "warning"].includes(message.type())) {
        consoleMessages.push({ type: message.type(), text: message.text().slice(0, 500) });
      }
    });
    page.on("pageerror", (error) => pageErrors.push(String(error.message || error).slice(0, 500)));
    const record = { file: pageLabel(file), site: siteNumberFor(file), url: pathToFileURL(file).href };
    try {
      await page.goto(record.url, { waitUntil: "load", timeout: 25000 });
      await page.waitForTimeout(80);
      await page.evaluate(async () => {
        const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
        document.querySelectorAll("img[loading='lazy']").forEach((img) => {
          img.loading = "eager";
        });
        const max = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
        const step = Math.max(500, Math.floor(innerHeight * 0.8));
        for (let y = 0; y < max; y += step) {
          scrollTo(0, y);
          await delay(18);
        }
        scrollTo(0, 0);
        await Promise.race([
          Promise.all([...document.images].map((img) => img.decode?.().catch(() => undefined) || Promise.resolve())),
          delay(1200),
        ]);
        await delay(80);
      });
      const audit = await page.evaluate(auditScript);
      let screenshot = "";
      if (screenshotPages) {
        screenshot = path.join("screenshots", screenshotName(file));
        await page.screenshot({
          path: path.join(outDir, screenshot),
          fullPage: true,
          type: "jpeg",
          quality: 64,
          animations: "disabled",
        });
      }
      return { ...record, screenshot, consoleMessages, pageErrors, audit };
    } catch (error) {
      return { ...record, error: String(error.message || error), consoleMessages, pageErrors };
    } finally {
      await page.close();
    }
  }

  async function worker() {
    while (nextIndex < files.length) {
      const index = nextIndex;
      nextIndex += 1;
      results[index] = await auditFile(files[index]);
      completed += 1;
      if (completed % 25 === 0 || completed === files.length) {
        console.log(`Audited ${completed}/${files.length}`);
      }
    }
  }

  const workerCount = Math.min(concurrency, Math.max(1, files.length));
  await Promise.all(Array.from({ length: workerCount }, () => worker()));

  await browser.close();

  const summary = {
    generatedAt: new Date().toISOString(),
    viewport: { width, height },
    totalPages: results.length,
    pagesWithErrors: results.filter((item) => item.error || item.pageErrors?.length || item.consoleMessages?.some((msg) => msg.type === "error")).length,
    pagesWithLowContrast: results.filter((item) => item.audit?.lowContrast?.length).length,
    pagesWithOverflow: results.filter((item) => item.audit?.flags?.pageWiderThanViewport || item.audit?.horizontalOverflow?.length).length,
    pagesWithBrokenImages: results.filter((item) => item.audit?.brokenImages?.length).length,
    pagesWithTallHeaders: results.filter((item) => item.audit?.flags?.tallHeader).length,
    outputDirectory: path.relative(ROOT, outDir),
  };

  const bySite = {};
  for (const result of results) {
    const key = result.site || "portfolio";
    bySite[key] ||= { pages: 0, errors: 0, lowContrast: 0, overflow: 0, brokenImages: 0, tallHeaders: 0 };
    bySite[key].pages += 1;
    if (result.error || result.pageErrors?.length || result.consoleMessages?.some((msg) => msg.type === "error")) bySite[key].errors += 1;
    if (result.audit?.lowContrast?.length) bySite[key].lowContrast += 1;
    if (result.audit?.flags?.pageWiderThanViewport || result.audit?.horizontalOverflow?.length) bySite[key].overflow += 1;
    if (result.audit?.brokenImages?.length) bySite[key].brokenImages += 1;
    if (result.audit?.flags?.tallHeader) bySite[key].tallHeaders += 1;
  }

  await writeJson(path.join(outDir, "visual-audit-report.json"), { summary, bySite, results });
  const markdown = [
    "# Visual Render Audit",
    "",
    `- Generated: ${summary.generatedAt}`,
    `- Viewport: ${width}x${height}`,
    `- Pages audited: ${summary.totalPages}`,
    `- Pages with console/page errors: ${summary.pagesWithErrors}`,
    `- Pages with low contrast findings: ${summary.pagesWithLowContrast}`,
    `- Pages with horizontal overflow: ${summary.pagesWithOverflow}`,
    `- Pages with broken images: ${summary.pagesWithBrokenImages}`,
    `- Pages with tall desktop headers: ${summary.pagesWithTallHeaders}`,
    `- Screenshots: \`${path.relative(ROOT, shotDir)}\``,
    "",
    "## Site Summary",
    "",
    "| Site | Pages | Errors | Low contrast | Overflow | Broken images | Tall headers |",
    "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ...Object.entries(bySite).sort(([a], [b]) => a.localeCompare(b)).map(([site, stats]) => (
      `| ${site} | ${stats.pages} | ${stats.errors} | ${stats.lowContrast} | ${stats.overflow} | ${stats.brokenImages} | ${stats.tallHeaders} |`
    )),
  ].join("\n");
  await fs.writeFile(path.join(outDir, "visual-audit-summary.md"), `${markdown}\n`);
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
