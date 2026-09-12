// Screenshot a local page at a real phone viewport.
//
// Chrome's --window-size clamps to a 500px minimum, so a 390px phone layout
// cannot be captured that way: you get a 500px layout cropped to 390, which
// misrepresents the page. This drives the DevTools Protocol instead, where
// Emulation.setDeviceMetricsOverride accepts any width, and asks Chrome to
// emulate prefers-color-scheme and prefers-reduced-motion rather than
// rewriting the page's own media queries.
//
// Node 22+ only, for the built-in WebSocket. No dependencies.
//
//   node capture.mjs <jobs.json>
//
// Each job: { page, out, width, height, scale, dark, reduceMotion, fullPage }

import { spawn } from "node:child_process";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const CANDIDATES = [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
];
const PORT = 9333;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForChrome() {
  for (let i = 0; i < 60; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      if (res.ok) return await res.json();
    } catch {}
    await sleep(250);
  }
  throw new Error("Chrome did not open a debugging port");
}

class Session {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.listeners = new Map();
    ws.addEventListener("message", (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
      } else if (msg.method && this.listeners.has(msg.method)) {
        this.listeners.get(msg.method).forEach((fn) => fn(msg.params));
      }
    });
  }

  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      setTimeout(() => {
        if (this.pending.delete(id)) reject(new Error(`${method} timed out`));
      }, 60000);
    });
  }

  once(method) {
    return new Promise((resolve) => {
      const list = this.listeners.get(method) || [];
      const fn = (params) => {
        this.listeners.set(
          method,
          (this.listeners.get(method) || []).filter((f) => f !== fn),
        );
        resolve(params);
      };
      list.push(fn);
      this.listeners.set(method, list);
    });
  }
}

const jobsPath = process.argv[2];
if (!jobsPath) {
  console.error("usage: node capture.mjs <jobs.json>");
  process.exit(1);
}
const jobs = JSON.parse(readFileSync(jobsPath, "utf8"));
const browser = CANDIDATES.find(existsSync);
if (!browser) {
  console.error("no Chrome or Edge found");
  process.exit(1);
}

const child = spawn(
  browser,
  [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    `--remote-debugging-port=${PORT}`,
    "about:blank",
  ],
  { stdio: "ignore" },
);

let failures = 0;
try {
  await waitForChrome();
  const created = await fetch(
    `http://127.0.0.1:${PORT}/json/new?about:blank`,
    { method: "PUT" },
  ).then((r) => r.json());
  const ws = new WebSocket(created.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });
  const cdp = new Session(ws);
  await cdp.send("Page.enable");

  for (const job of jobs) {
    const {
      page, out, width, height, scale = 1,
      dark = false, reduceMotion = false, fullPage = true,
    } = job;
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width, height, deviceScaleFactor: scale, mobile: width < 768,
    });
    await cdp.send("Emulation.setEmulatedMedia", {
      media: "screen",
      features: [
        { name: "prefers-color-scheme", value: dark ? "dark" : "light" },
        {
          name: "prefers-reduced-motion",
          value: reduceMotion ? "reduce" : "no-preference",
        },
      ],
    });

    const loaded = cdp.once("Page.loadEventFired");
    await cdp.send("Page.navigate", { url: pathToFileURL(page).href });
    await loaded;
    // Long enough for every transition out of @starting-style to finish, so
    // no capture is a mid-flight frame.
    await sleep(2200);

    const shot = await cdp.send("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: fullPage,
      optimizeForSpeed: false,
    });
    writeFileSync(out, Buffer.from(shot.data, "base64"));
    const kb = Math.round(Buffer.from(shot.data, "base64").length / 1024);
    const flags = [dark ? "dark" : null, reduceMotion ? "no-motion" : null]
      .filter(Boolean)
      .join(" ");
    console.log(
      `  ok  ${out.split(/[\\/]/).pop().padEnd(30)} ${width}x${height} ` +
      `@${scale}x ${kb}KB ${flags}`,
    );
  }
} catch (error) {
  console.error(`  capture failed: ${error.message}`);
  failures = 1;
} finally {
  child.kill();
}
process.exit(failures);
