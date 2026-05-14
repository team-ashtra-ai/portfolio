#!/usr/bin/env node
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import os from "node:os";
import fs from "node:fs/promises";
import { spawn } from "node:child_process";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const DEMO_ROOT = path.join(ROOT, "demo-sites");
const REPORT_ROOT = path.join(ROOT, "premium-static-site-system", "reports", "section-visual-audit");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const arg = process.argv[index];
  if (!arg.startsWith("--")) continue;
  const [key, value] = arg.includes("=") ? arg.split("=", 2) : [arg, process.argv[index + 1]];
  args.set(key, value && !value.startsWith("--") ? value : "true");
  if (value && !value.startsWith("--") && !arg.includes("=")) index += 1;
}

const onlySite = args.get("--site");
const includeRootPages = args.get("--include-root") === "true";
const limitPages = Number(args.get("--limit-pages") || 0);
const offsetPages = Math.max(0, Number(args.get("--offset-pages") || 0));
const screenshotMode = args.get("--screenshots") || "all"; // all, issues, false
const browserBatchSize = Math.max(1, Math.min(12, Number(args.get("--batch-size") || 8)));
const concurrency = Math.max(1, Math.min(6, Number(args.get("--concurrency") || 1)));
const progressEvery = Math.max(1, Number(args.get("--progress-every") || 10));
const viewport = {
  width: Number(args.get("--width") || 1440),
  height: Number(args.get("--height") || 960),
  mobile: args.get("--mobile") === "true",
  quality: Number(args.get("--quality") || 68),
};
const maxSectionHeight = Math.max(600, Number(args.get("--max-section-height") || 2200));

async function exists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function walkHtml(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (["assets", "docs", "partials"].includes(entry.name)) continue;
      files.push(...await walkHtml(full));
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      files.push(full);
    }
  }
  return files;
}

function siteNumberFor(file) {
  const first = path.relative(DEMO_ROOT, file).split(path.sep)[0];
  return first.match(/^(\d{2})-/)?.[1] || "";
}

function safeName(value) {
  return String(value || "section")
    .toLowerCase()
    .replace(/&amp;/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 90) || "section";
}

function waitForEvent(client, eventName, timeout = 25000, predicate = () => true) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      unsubscribe();
      reject(new Error(`Timed out waiting for ${eventName}`));
    }, timeout);
    const unsubscribe = client.on(eventName, (params) => {
      if (!predicate(params)) return;
      clearTimeout(timer);
      unsubscribe();
      resolve(params);
    });
  });
}

async function evaluate(client, expression) {
  const response = await client.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (response.exceptionDetails) {
    const message = response.exceptionDetails.exception?.description || response.exceptionDetails.text || "Runtime evaluation failed";
    throw new Error(message);
  }
  return response.result?.value;
}

async function waitForAssets(client) {
  await evaluate(client, `(${async () => {
    const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    await new Promise((resolve) => {
      const existing = [...document.scripts].find((script) => (script.getAttribute("src") || "").endsWith("js/main.js"));
      if (existing) {
        delay(500).then(resolve);
        return;
      }
      const script = document.createElement("script");
      script.src = "js/main.js";
      script.defer = true;
      script.onload = resolve;
      script.onerror = resolve;
      document.head.appendChild(script);
      setTimeout(resolve, 1200);
    });
    if (!document.getElementById("codex-section-audit-visible")) {
      const style = document.createElement("style");
      style.id = "codex-section-audit-visible";
      style.textContent = [
        ".reveal-ready{opacity:1!important;transform:none!important}",
        ".portfolio-component,.content-section{content-visibility:visible!important;contain:none!important;contain-intrinsic-size:auto!important}",
        "html{scroll-behavior:auto!important}",
      ].join("");
      document.head.appendChild(style);
    }
    document.querySelectorAll("img[loading='lazy']").forEach((img) => {
      img.loading = "eager";
    });
    const max = Math.min(Math.max(document.body.scrollHeight, document.documentElement.scrollHeight), 60000);
    const step = Math.max(520, Math.floor(innerHeight * 0.75));
    let scrollSteps = 0;
    for (let y = 0; y < max && scrollSteps < 120; y += step, scrollSteps += 1) {
      scrollTo(0, y);
      await delay(10);
    }
    scrollTo(0, 0);
    document.querySelectorAll(".reveal-ready").forEach((item) => {
      item.classList.add("is-visible");
      item.style.removeProperty("opacity");
      item.style.removeProperty("transform");
    });
    await Promise.race([
      Promise.all([...document.images].map((img) => img.decode?.().catch(() => undefined) || Promise.resolve())),
      delay(1800),
    ]);
    await delay(80);
  }})()`);
}

function sectionAuditDom() {
  const visible = (el) => {
    const style = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) > 0.05 && rect.width > 1 && rect.height > 1;
  };
  const selectorFor = (el) => {
    if (el.id) return `${el.tagName.toLowerCase()}#${el.id}`;
    const classes = [...el.classList].slice(0, 4).join(".");
    return classes ? `${el.tagName.toLowerCase()}.${classes}` : el.tagName.toLowerCase();
  };
  const viewportWidth = document.documentElement.clientWidth;
  const sections = [...document.querySelectorAll("main > section")].map((section, index) => {
    const rect = section.getBoundingClientRect();
    const top = rect.top + scrollY;
    const h2 = section.querySelector("h1,h2")?.textContent?.trim().replace(/\s+/g, " ") || section.getAttribute("data-section-label") || section.id || `Section ${index + 1}`;
    const sectionType = section.getAttribute("data-section-type") || "";
    const label = section.getAttribute("data-section") || section.getAttribute("data-section-label") || h2;
    const textLength = (section.innerText || "").trim().length;
    const sectionText = (section.innerText || "").trim().replace(/\s+/g, " ");
    const images = [...section.querySelectorAll("img")];
    const visibleSignaturePanels = [...section.querySelectorAll(".signature-panel")].filter(visible).length;
    const visiblePrimaryGrids = [...section.querySelectorAll(":scope > .section-grid")].filter(visible).length;
    const brokenImages = images
      .filter((img) => !img.complete || img.naturalWidth === 0 || img.naturalHeight === 0)
      .map((img) => img.getAttribute("src"))
      .slice(0, 10);
    const overflowing = [...section.querySelectorAll("*")]
      .filter(visible)
      .filter((el) => !el.matches(".honeypot,[aria-hidden='true']"))
      .filter((el) => {
        const childRect = el.getBoundingClientRect();
        return childRect.right > viewportWidth + 3 || childRect.left < -3;
      })
      .slice(0, 12)
      .map(selectorFor);
    const issues = [];
    if (rect.width > viewportWidth + 3 || overflowing.length) issues.push("horizontal-overflow");
    if (brokenImages.length) issues.push("broken-images");
    if (rect.height > 1800 && textLength < 180) issues.push("oversized-sparse-section");
    if (rect.height < 80 && textLength > 20) issues.push("compressed-section");
    if (rect.height > 220 && textLength < 24 && images.length === 0) issues.push("blank-or-hidden-section");
    if (sectionType === "hero" && rect.height > innerHeight * 1.35) issues.push("oversized-hero");
    if (sectionType === "cta" && /^CTA$/i.test(h2)) issues.push("generic-cta-heading");
    if (sectionType && sectionType !== "hero" && sectionType !== "homepage-atlas" && h2.trim().split(/\s+/).length <= 1) issues.push("weak-section-heading");
    if (/Every route through/i.test(sectionText)) issues.push("generic-route-copy");
    if (visibleSignaturePanels) issues.push("visible-repeated-signature-panel");
    if (sectionType === "cta" && visiblePrimaryGrids && section.querySelector(".cta-panel")) issues.push("cta-has-competing-generic-grid");
    if (section.matches(".content-section") && !section.querySelector(".section-copy,.cta-panel,.form-panel,.resource-board,.faq-list")) {
      issues.push("missing-primary-content-block");
    }
    return {
      index: index + 1,
      id: section.id || "",
      label,
      heading: h2,
      sectionType,
      patternFamily: section.getAttribute("data-pattern-family") || "",
      layoutVariation: section.getAttribute("data-layout-variation") || "",
      rect: {
        x: Math.max(0, Math.round(rect.left + scrollX)),
        y: Math.max(0, Math.round(top)),
        width: Math.max(1, Math.ceil(Math.min(viewportWidth, rect.width || viewportWidth))),
        height: Math.max(1, Math.ceil(rect.height)),
      },
      textLength,
      imageCount: images.length,
      visibleSignaturePanels,
      brokenImages,
      overflowing,
      issues,
    };
  });
  return {
    title: document.title,
    url: location.href,
    viewport: { width: innerWidth, height: innerHeight },
    documentSize: { width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight },
    pageOverflow: document.documentElement.scrollWidth > viewportWidth + 3,
    sectionCount: sections.length,
    sections,
  };
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.nextId = 1;
    this.pending = new Map();
    this.listeners = new Map();
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.addEventListener("open", () => resolve());
      this.ws.addEventListener("error", (event) => reject(new Error(event.message || "WebSocket connection failed")), { once: true });
      this.ws.addEventListener("message", (event) => this.handleMessage(event.data));
      this.ws.addEventListener("close", () => {
        for (const { reject: rejectPending } of this.pending.values()) {
          rejectPending(new Error("Chrome DevTools connection closed"));
        }
        this.pending.clear();
      });
    });
  }

  handleMessage(raw) {
    const message = JSON.parse(raw);
    if (message.id) {
      const pending = this.pending.get(message.id);
      if (!pending) return;
      this.pending.delete(message.id);
      if (message.error) pending.reject(new Error(`${message.error.message}${message.error.data ? `: ${message.error.data}` : ""}`));
      else pending.resolve(message.result || {});
      return;
    }
    if (message.method) {
      for (const listener of this.listeners.get(message.method) || []) listener(message.params || {});
    }
  }

  send(method, params = {}) {
    const id = this.nextId++;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
    });
  }

  on(method, callback) {
    if (!this.listeners.has(method)) this.listeners.set(method, new Set());
    this.listeners.get(method).add(callback);
    return () => this.listeners.get(method)?.delete(callback);
  }

  close() {
    this.ws?.close();
  }
}

async function waitForDevToolsUrl(process) {
  return new Promise((resolve, reject) => {
    let buffer = "";
    const timer = setTimeout(() => reject(new Error(`Timed out waiting for Chrome DevTools endpoint. Output: ${buffer.slice(-1000)}`)), 15000);
    process.stderr.on("data", (chunk) => {
      buffer += chunk.toString();
      const match = buffer.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (!match) return;
      clearTimeout(timer);
      resolve(match[1]);
    });
    process.once("exit", (code) => {
      clearTimeout(timer);
      reject(new Error(`Chrome exited before DevTools was ready with code ${code}. Output: ${buffer.slice(-1000)}`));
    });
  });
}

async function connectToFirstPage(httpBase) {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    try {
      const response = await fetch(`${httpBase}/json/list`);
      const targets = await response.json();
      const page = targets.find((target) => target.type === "page" && target.webSocketDebuggerUrl);
      if (page) {
        const client = new CDPClient(page.webSocketDebuggerUrl);
        await client.connect();
        return client;
      }
    } catch {
      // Chrome may need a moment.
    }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("Unable to find a Chrome page target for auditing.");
}

async function launchChrome(chromePath) {
  const userDataDir = await fs.mkdtemp(path.join(os.tmpdir(), "section-audit-chrome-"));
  const child = spawn(chromePath, [
    "--headless=new",
    "--remote-debugging-port=0",
    `--user-data-dir=${userDataDir}`,
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-crash-reporter",
    "--disable-crashpad",
    "--disable-breakpad",
    "--no-first-run",
    "--no-default-browser-check",
    "--allow-file-access-from-files",
    "about:blank",
  ], { stdio: ["ignore", "ignore", "pipe"] });
  const browserWs = await waitForDevToolsUrl(child);
  const url = new URL(browserWs);
  return { process: child, userDataDir, httpBase: `http://${url.host}` };
}

async function configureViewport(client) {
  await client.send("Emulation.setDeviceMetricsOverride", {
    width: viewport.width,
    height: viewport.height,
    deviceScaleFactor: 1,
    mobile: viewport.mobile,
  });
  await client.send("Emulation.setEmulatedMedia", {
    features: [{ name: "prefers-reduced-motion", value: "reduce" }],
  });
}

async function navigate(client, url) {
  const load = waitForEvent(client, "Page.loadEventFired", 25000).catch(() => undefined);
  await client.send("Page.navigate", { url });
  await load;
  await evaluate(client, "document.readyState");
}

async function captureSection(client, outDir, relativeFile, rect) {
  await fs.mkdir(path.dirname(path.join(outDir, relativeFile)), { recursive: true });
  const clip = {
    x: 0,
    y: Math.max(0, rect.y),
    width: viewport.width,
    height: Math.max(1, Math.min(maxSectionHeight, rect.height)),
    scale: 1,
  };
  const screenshot = await client.send("Page.captureScreenshot", {
    format: "jpeg",
    quality: viewport.quality,
    captureBeyondViewport: true,
    fromSurface: true,
    clip,
  });
  await fs.writeFile(path.join(outDir, relativeFile), Buffer.from(screenshot.data, "base64"));
}

async function startAuditBrowser(chromePath) {
  const chrome = await launchChrome(chromePath);
  const client = await connectToFirstPage(chrome.httpBase);
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Log.enable");
  await configureViewport(client);
  return { chrome, client };
}

async function stopAuditBrowser(browser) {
  if (!browser) return;
  browser.client?.close();
  browser.chrome.process.kill("SIGTERM");
  await new Promise((resolve) => {
    const timer = setTimeout(resolve, 1200);
    browser.chrome.process.once("exit", () => {
      clearTimeout(timer);
      resolve();
    });
  });
  await fs.rm(browser.chrome.userDataDir, { recursive: true, force: true, maxRetries: 5, retryDelay: 150 });
}

function sectionShotName(file, section) {
  const rel = path.relative(DEMO_ROOT, file).replace(/\.html$/, "");
  return path.join("screenshots", rel, `${String(section.index).padStart(2, "0")}-${safeName(section.id || section.label || section.heading)}.jpg`);
}

async function auditFile(client, file, outDir) {
  const record = {
    file: path.relative(ROOT, file),
    site: siteNumberFor(file),
    url: pathToFileURL(file).href,
    pageErrors: [],
    consoleErrors: [],
  };
  const removeConsole = client.on("Runtime.consoleAPICalled", (event) => {
    if (event.type === "error") {
      const text = (event.args || []).map((arg) => arg.value || arg.description || "").join(" ").slice(0, 500);
      record.consoleErrors.push(text);
    }
  });
  const removeException = client.on("Runtime.exceptionThrown", (event) => {
    const details = event.exceptionDetails || {};
    record.pageErrors.push(String(details.exception?.description || details.text || "Page exception").slice(0, 500));
  });
  try {
    await navigate(client, record.url);
    await waitForAssets(client);
    const audit = await evaluate(client, `(${sectionAuditDom.toString()})()`);
    for (const section of audit.sections) {
      const shouldCapture = screenshotMode === "all" || (screenshotMode === "issues" && section.issues.length);
      if (!shouldCapture) continue;
      const screenshot = sectionShotName(file, section);
      await captureSection(client, outDir, screenshot, section.rect);
      section.screenshot = screenshot;
    }
    return { ...record, audit };
  } catch (error) {
    return { ...record, error: String(error.message || error) };
  } finally {
    removeConsole();
    removeException();
  }
}

async function writeJson(file, value) {
  await fs.writeFile(file, `${JSON.stringify(value, null, 2)}\n`);
}

async function main() {
  const chromePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";
  if (!(await exists(chromePath))) throw new Error(`Chrome not found at ${chromePath}. Set CHROME_PATH to a Chromium executable.`);

  const allFiles = (await walkHtml(DEMO_ROOT))
    .filter((file) => includeRootPages || siteNumberFor(file))
    .filter((file) => !onlySite || siteNumberFor(file) === String(onlySite).padStart(2, "0"))
    .sort((a, b) => path.relative(ROOT, a).localeCompare(path.relative(ROOT, b)));
  const files = limitPages > 0 ? allFiles.slice(offsetPages, offsetPages + limitPages) : allFiles.slice(offsetPages);
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const outDir = path.join(REPORT_ROOT, stamp);
  await fs.mkdir(outDir, { recursive: true });

  const results = Array(files.length);
  let nextIndex = 0;
  let completed = 0;

  async function worker() {
    let browser = null;
    let browserUses = 0;
    try {
      while (nextIndex < files.length) {
        const index = nextIndex;
        nextIndex += 1;
        if (!browser) {
          browser = await startAuditBrowser(chromePath);
          browserUses = 0;
        }
        results[index] = await auditFile(browser.client, files[index], outDir);
        browserUses += 1;
        completed += 1;
        if (completed % progressEvery === 0 || completed === files.length) {
          const sections = results.reduce((sum, record) => sum + (record?.audit?.sections?.length || 0), 0);
          console.log(`Audited ${completed}/${files.length} pages, ${sections} sections`);
        }
        if (browserUses >= browserBatchSize) {
          await stopAuditBrowser(browser);
          browser = null;
        }
      }
    } finally {
      await stopAuditBrowser(browser);
    }
  }

  await Promise.all(Array.from({ length: Math.min(concurrency, Math.max(1, files.length)) }, () => worker()));

  const pageIssues = results.filter((record) => record.error || record.pageErrors?.length || record.consoleErrors?.length || record.audit?.pageOverflow);
  const sectionIssues = [];
  for (const record of results) {
    for (const section of record.audit?.sections || []) {
      if (section.issues?.length) sectionIssues.push({ file: record.file, site: record.site, ...section });
    }
  }
  const sectionsCaptured = results.reduce((sum, record) => sum + (record.audit?.sections || []).filter((section) => section.screenshot).length, 0);
  const totalSections = results.reduce((sum, record) => sum + (record.audit?.sectionCount || 0), 0);
  const summary = {
    generatedAt: new Date().toISOString(),
    viewport,
    screenshotMode,
    offsetPages,
    totalPages: results.length,
    totalSections,
    sectionsCaptured,
    pagesWithIssues: pageIssues.length,
    sectionsWithIssues: sectionIssues.length,
    outputDirectory: path.relative(ROOT, outDir),
  };

  const bySite = {};
  for (const record of results) {
    const key = record.site || "portfolio";
    bySite[key] ||= { pages: 0, sections: 0, sectionIssues: 0, pageIssues: 0 };
    bySite[key].pages += 1;
    bySite[key].sections += record.audit?.sectionCount || 0;
    if (record.error || record.pageErrors?.length || record.consoleErrors?.length || record.audit?.pageOverflow) bySite[key].pageIssues += 1;
    bySite[key].sectionIssues += (record.audit?.sections || []).filter((section) => section.issues?.length).length;
  }

  await writeJson(path.join(outDir, "section-visual-audit.json"), { summary, bySite, sectionIssues, results });
  const markdown = [
    "# Section Visual Audit",
    "",
    `- Generated: ${summary.generatedAt}`,
    `- Viewport: ${viewport.width}x${viewport.height}`,
    `- Pages audited: ${summary.totalPages}`,
    `- Sections audited: ${summary.totalSections}`,
    `- Section screenshots captured: ${summary.sectionsCaptured}`,
    `- Pages with issues: ${summary.pagesWithIssues}`,
    `- Sections with issues: ${summary.sectionsWithIssues}`,
    `- Output: \`${summary.outputDirectory}\``,
    "",
    "## Site Summary",
    "",
    "| Site | Pages | Sections | Page issues | Section issues |",
    "| --- | ---: | ---: | ---: | ---: |",
    ...Object.entries(bySite).sort(([a], [b]) => a.localeCompare(b)).map(([site, stats]) => (
      `| ${site} | ${stats.pages} | ${stats.sections} | ${stats.pageIssues} | ${stats.sectionIssues} |`
    )),
    "",
    "## First Section Issues",
    "",
    "| File | Section | Issues | Screenshot |",
    "| --- | --- | --- | --- |",
    ...sectionIssues.slice(0, 120).map((section) => (
      `| ${section.file} | ${section.index}. ${section.heading} | ${section.issues.join(", ")} | ${section.screenshot ? `\`${section.screenshot}\`` : ""} |`
    )),
  ].join("\n");
  await fs.writeFile(path.join(outDir, "section-visual-summary.md"), `${markdown}\n`);
  console.log(JSON.stringify(summary, null, 2));
  if (pageIssues.length || sectionIssues.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
