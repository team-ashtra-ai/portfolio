#!/usr/bin/env node
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import os from "node:os";
import fs from "node:fs/promises";
import { spawn } from "node:child_process";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const DEMO_ROOT = path.join(ROOT, "demo-sites");
const REPORT_ROOT = path.join(ROOT, "premium-static-site-system", "reports", "homepage-atlas");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const arg = process.argv[index];
  if (arg.startsWith("--")) {
    const [key, value] = arg.includes("=") ? arg.split("=", 2) : [arg, process.argv[index + 1]];
    args.set(key, value && !value.startsWith("--") ? value : "true");
    if (value && !value.startsWith("--") && !arg.includes("=")) index += 1;
  }
}

const screenshotPages = args.get("--screenshots") !== "false";
const maxScreenshotHeight = Math.max(1200, Number(args.get("--max-screenshot-height") || 10000));
const browserBatchSize = Math.max(1, Math.min(10, Number(args.get("--batch-size") || 5)));
const VIEWPORTS = {
  desktop: { width: 1440, height: 960, mobile: false, quality: 70 },
  mobile: { width: 390, height: 844, mobile: true, quality: 72 },
};

async function exists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function siteDirs() {
  const entries = await fs.readdir(DEMO_ROOT, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isDirectory() && /^\d{2}-/.test(entry.name))
    .map((entry) => path.join(DEMO_ROOT, entry.name))
    .sort((a, b) => a.localeCompare(b));
}

async function htmlFiles(siteDir) {
  const entries = await fs.readdir(siteDir, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(".html") && entry.name !== "index.html")
    .map((entry) => entry.name)
    .sort((a, b) => a.localeCompare(b));
}

function siteNumber(siteDir) {
  return path.basename(siteDir).slice(0, 2);
}

function normalizeHref(value) {
  if (
    !value ||
    value.startsWith("http:") ||
    value.startsWith("https:") ||
    value.startsWith("mailto:") ||
    value.startsWith("tel:") ||
    value.startsWith("#")
  ) {
    return "";
  }
  return value.split("#")[0].split("?")[0].replace(/^\.\//, "");
}

function auditDom(expectedFiles) {
  function normalizePageHref(value) {
    if (
      !value ||
      value.startsWith("http:") ||
      value.startsWith("https:") ||
      value.startsWith("mailto:") ||
      value.startsWith("tel:") ||
      value.startsWith("#")
    ) {
      return "";
    }
    return value.split("#")[0].split("?")[0].replace(/^\.\//, "");
  }
  const directSections = [...document.querySelectorAll("main > section")];
  const first = directSections[0];
  const last = directSections[directSections.length - 1];
  const anchors = [...document.querySelectorAll("a[href]")].map((link) => link.getAttribute("href"));
  const normalized = new Set(anchors.map(normalizePageHref).filter(Boolean));
  const missingLinks = expectedFiles.filter((file) => !normalized.has(file));
  const brokenImages = [...document.images]
    .filter((img) => !img.complete || img.naturalWidth === 0 || img.naturalHeight === 0)
    .map((img) => img.getAttribute("src"))
    .slice(0, 20);
  const viewportWidth = document.documentElement.clientWidth;
  const overflow = document.documentElement.scrollWidth > viewportWidth + 3;
  const overflowing = [...document.body.querySelectorAll("body *")]
    .filter((el) => {
      const style = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 1 && (rect.right > viewportWidth + 3 || rect.left < -3);
    })
    .slice(0, 10)
    .map((el) =>
      el.id
        ? `${el.tagName.toLowerCase()}#${el.id}`
        : el.className
          ? `${el.tagName.toLowerCase()}.${String(el.className).split(/\s+/).slice(0, 3).join(".")}`
          : el.tagName.toLowerCase(),
    );
  const atlas = document.querySelector("#site-atlas");
  const hero = document.querySelector("main > section[data-section='Hero']");
  const cta = document.querySelector("main > section[data-section='CTA']");
  const heroLinks = document.querySelectorAll(".hero-atlas-links a").length;
  const atlasLinks = atlas ? atlas.querySelectorAll("a[href]").length : 0;
  return {
    title: document.title,
    firstSection: first?.getAttribute("data-section") || first?.id || "",
    lastSection: last?.getAttribute("data-section") || last?.id || "",
    hasHero: Boolean(hero),
    hasAtlas: Boolean(atlas),
    hasFinalCta: Boolean(cta && last === cta),
    heroFastLinks: heroLinks,
    atlasLinkCount: atlasLinks,
    missingLinks,
    brokenImages,
    overflow,
    overflowing,
    documentHeight: document.documentElement.scrollHeight,
  };
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
    await delay(180);
    if (!document.getElementById("codex-audit-reveal-visible")) {
      const style = document.createElement("style");
      style.id = "codex-audit-reveal-visible";
      style.textContent = ".reveal-ready{opacity:1!important;transform:none!important}.portfolio-component,.content-section{content-visibility:visible!important;contain:none!important;contain-intrinsic-size:auto!important}";
      document.head.appendChild(style);
    }
    document.querySelectorAll("img[loading='lazy']").forEach((img) => {
      img.loading = "eager";
    });
    const max = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    const step = Math.max(520, Math.floor(innerHeight * 0.75));
    for (let y = 0; y < max; y += step) {
      scrollTo(0, y);
      await delay(12);
    }
    scrollTo(0, 0);
    document.querySelectorAll(".reveal-ready").forEach((item) => {
      item.classList.add("is-visible");
      item.style.removeProperty("opacity");
      item.style.removeProperty("transform");
    });
    await Promise.race([
      Promise.all([...document.images].map((img) => img.decode?.().catch(() => undefined) || Promise.resolve())),
      delay(1500),
    ]);
    await delay(80);
  }})()`);
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
      for (const listener of this.listeners.get(message.method) || []) {
        listener(message.params || {});
      }
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
    const timer = setTimeout(() => {
      reject(new Error(`Timed out waiting for Chrome DevTools endpoint. Output: ${buffer.slice(-1000)}`));
    }, 15000);
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
      // Chrome may need a moment after exposing the browser endpoint.
    }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error("Unable to find a Chrome page target for auditing.");
}

async function launchChrome(chromePath) {
  const userDataDir = await fs.mkdtemp(path.join(os.tmpdir(), "homepage-atlas-chrome-"));
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
  return {
    process: child,
    userDataDir,
    browserWs,
    httpBase: `http://${url.host}`,
  };
}

async function configureViewport(client, viewport) {
  await client.send("Emulation.setDeviceMetricsOverride", {
    width: viewport.width,
    height: viewport.height,
    deviceScaleFactor: 1,
    mobile: viewport.mobile,
  });
  await client.send("Emulation.setTouchEmulationEnabled", { enabled: viewport.mobile });
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

async function captureScreenshot(client, outDir, relativeFile, viewport) {
  await fs.mkdir(path.dirname(path.join(outDir, relativeFile)), { recursive: true });
  const metrics = await client.send("Page.getLayoutMetrics");
  const content = metrics.cssContentSize || metrics.contentSize || { x: 0, y: 0, width: viewport.width, height: viewport.height };
  const width = Math.max(viewport.width, Math.ceil(content.width));
  const height = Math.min(maxScreenshotHeight, Math.max(viewport.height, Math.ceil(content.height)));
  const screenshot = await client.send("Page.captureScreenshot", {
    format: "jpeg",
    quality: viewport.quality,
    captureBeyondViewport: true,
    fromSurface: true,
    clip: { x: 0, y: 0, width, height, scale: 1 },
  });
  await fs.writeFile(path.join(outDir, relativeFile), Buffer.from(screenshot.data, "base64"));
}

async function auditSite(client, siteDir, outDir) {
  const expectedFiles = await htmlFiles(siteDir);
  const file = path.join(siteDir, "index.html");
  const record = {
    site: siteNumber(siteDir),
    folder: path.relative(DEMO_ROOT, siteDir),
    file: path.relative(ROOT, file),
    expectedFiles,
    desktop: null,
    mobile: null,
    pageErrors: [],
    consoleErrors: [],
  };

  for (const [label, viewport] of Object.entries(VIEWPORTS)) {
    const removeConsole = client.on("Runtime.consoleAPICalled", (event) => {
      if (event.type === "error") {
        const text = (event.args || []).map((arg) => arg.value || arg.description || "").join(" ").slice(0, 400);
        record.consoleErrors.push({ viewport: label, text });
      }
    });
    const removeException = client.on("Runtime.exceptionThrown", (event) => {
      const details = event.exceptionDetails || {};
      record.pageErrors.push({ viewport: label, text: String(details.exception?.description || details.text || "Page exception").slice(0, 400) });
    });
    try {
      await configureViewport(client, viewport);
      await navigate(client, pathToFileURL(file).href);
      await waitForAssets(client);
      const audit = await evaluate(client, `(${auditDom.toString()})(${JSON.stringify(expectedFiles)})`);
      if (screenshotPages) {
        const screenshot = path.join("screenshots", label, `${record.folder}.jpg`);
        await captureScreenshot(client, outDir, screenshot, viewport);
        audit.screenshot = screenshot;
      }
      record[label] = audit;
    } catch (error) {
      record[label] = { error: String(error.message || error) };
    } finally {
      removeConsole();
      removeException();
    }
  }
  return record;
}

function failed(record) {
  for (const label of ["desktop", "mobile"]) {
    const audit = record[label];
    if (!audit || audit.error) return true;
    if (!audit.hasHero || !audit.hasAtlas || !audit.hasFinalCta) return true;
    if (audit.firstSection !== "Hero" || audit.lastSection !== "CTA") return true;
    if (audit.heroFastLinks < 4 || audit.atlasLinkCount < record.expectedFiles.length) return true;
    if (audit.missingLinks?.length || audit.brokenImages?.length || audit.overflow) return true;
  }
  if (record.pageErrors.length || record.consoleErrors.length) return true;
  return false;
}

async function writeJson(file, value) {
  await fs.writeFile(file, `${JSON.stringify(value, null, 2)}\n`);
}

async function startAuditBrowser(chromePath) {
  const chrome = await launchChrome(chromePath);
  const client = await connectToFirstPage(chrome.httpBase);
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Log.enable");
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

async function main() {
  const chromePath = process.env.CHROME_PATH || "/usr/bin/google-chrome-stable";
  if (!(await exists(chromePath))) {
    throw new Error(`Chrome not found at ${chromePath}. Set CHROME_PATH to a Chromium executable.`);
  }
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const outDir = path.join(REPORT_ROOT, stamp);
  await fs.mkdir(outDir, { recursive: true });

  let browser;
  try {
    let sites = await siteDirs();
    const siteFilter = args.get("--site");
    if (siteFilter && siteFilter !== "true") {
      sites = sites.filter((site) => path.basename(site).includes(siteFilter));
    }
    const results = [];
    for (let index = 0; index < sites.length; index += 1) {
      if (!browser) {
        browser = await startAuditBrowser(chromePath);
      }
      results.push(await auditSite(browser.client, sites[index], outDir));
      if ((index + 1) % browserBatchSize === 0 || index + 1 === sites.length) {
        console.log(`Audited ${index + 1}/${sites.length}`);
        await stopAuditBrowser(browser);
        browser = null;
      }
    }

    const failures = results.filter(failed);
    const summary = {
      generatedAt: new Date().toISOString(),
      totalHomepages: results.length,
      failures: failures.length,
      desktopScreenshots: screenshotPages ? path.relative(ROOT, path.join(outDir, "screenshots", "desktop")) : "",
      mobileScreenshots: screenshotPages ? path.relative(ROOT, path.join(outDir, "screenshots", "mobile")) : "",
      outputDirectory: path.relative(ROOT, outDir),
    };
    await writeJson(path.join(outDir, "homepage-atlas-audit.json"), { summary, results });
    const markdown = [
      "# Homepage Atlas Audit",
      "",
      `- Generated: ${summary.generatedAt}`,
      `- Homepages audited: ${summary.totalHomepages}`,
      `- Failures: ${summary.failures}`,
      `- Desktop screenshots: \`${summary.desktopScreenshots}\``,
      `- Mobile screenshots: \`${summary.mobileScreenshots}\``,
      "",
      "| Site | Hero first | Atlas | CTA final | Missing links | Broken images | Overflow |",
      "| --- | --- | --- | --- | ---: | ---: | --- |",
      ...results.map((record) => {
        const desktop = record.desktop || {};
        const mobile = record.mobile || {};
        const missing = Math.max(desktop.missingLinks?.length || 0, mobile.missingLinks?.length || 0);
        const broken = Math.max(desktop.brokenImages?.length || 0, mobile.brokenImages?.length || 0);
        const overflow = desktop.overflow || mobile.overflow ? "yes" : "no";
        return `| ${record.folder} | ${desktop.firstSection === "Hero" && mobile.firstSection === "Hero" ? "yes" : "no"} | ${desktop.hasAtlas && mobile.hasAtlas ? "yes" : "no"} | ${desktop.lastSection === "CTA" && mobile.lastSection === "CTA" ? "yes" : "no"} | ${missing} | ${broken} | ${overflow} |`;
      }),
    ].join("\n");
    await fs.writeFile(path.join(outDir, "homepage-atlas-summary.md"), `${markdown}\n`);
    console.log(JSON.stringify(summary, null, 2));
    process.exitCode = failures.length ? 1 : 0;
  } finally {
    await stopAuditBrowser(browser);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
