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

  await page.goto(`file://${html}?print-pdf`, {
    waitUntil: "networkidle",
    timeout: 60000,
  });
  await page.waitForSelector(".reveal .slides section", { timeout: 30000 });

  await page.evaluate(async () => {
    if (window.Reveal?.isReady) await window.Reveal.isReady();
    if (document.fonts?.ready) await document.fonts.ready;
    await Promise.all(
      [...document.images].map((image) =>
        image.decode().catch(() => undefined)
      )
    );
  });

  const slideCount = await page.locator(".reveal .slides section").count();
  if (slideCount < 30) {
    throw new Error(`Expected at least 30 rendered slide sections, found ${slideCount}`);
  }

  await page.addStyleTag({
    content: `
      @page { size: 16in 9in; margin: 0; }
      html, body { margin: 0 !important; padding: 0 !important; }
    `,
  });

  await page.pdf({
    path: pdf,
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: false,
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
  });
  console.log(`PDF exported: ${pdf} (${slideCount} rendered slide sections)`);
} finally {
  await browser.close();
}
