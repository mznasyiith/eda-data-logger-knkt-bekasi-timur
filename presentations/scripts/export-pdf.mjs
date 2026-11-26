import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
import { resolve } from "node:path";

const html = resolve("presentations/dist/eda-knkt-bekasi-timur.html");
const pdf = resolve("presentations/dist/eda-knkt-bekasi-timur.pdf");

await mkdir(resolve("presentations/dist"), { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({
    viewport: { width: 1600, height: 900 },
    deviceScaleFactor: 1,
  });
  const response = await page.goto(`file://${html}?print-pdf`, {
    waitUntil: "networkidle",
    timeout: 60000,
  });
  if (!response && !(await page.locator(".reveal .slides section").count())) {
    throw new Error("Reveal.js presentation did not load");
  }
  await page.emulateMedia({ media: "print" });
  await page.waitForTimeout(1000);
  await page.pdf({
    path: pdf,
    format: "A4",
    landscape: true,
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: "0mm", right: "0mm", bottom: "0mm", left: "0mm" },
  });
  console.log(`PDF exported: ${pdf}`);
} finally {
  await browser.close();
}
