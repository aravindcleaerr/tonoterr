#!/usr/bin/env node
/*
 * Drives the live TestOK app through one full evaluation and records it to a
 * .webm via puppeteer's screencast. Encoding/joining is done by build.sh.
 *
 * Env:
 *   APP_URL         app to record   (default: the bench origin)
 *   CHROME          chrome binary   (default: /usr/bin/google-chrome)
 *   OUT             output webm     (default: ./walk.webm)
 *   PUPPETEER_CORE  override module path for puppeteer-core (optional)
 *
 * The selectors below mirror design/TestOK/app.jsx in the TestOK app repo;
 * if that UI changes, update them here and re-run build.sh.
 */
const path = require('path');

let puppeteer;
try { puppeteer = require(process.env.PUPPETEER_CORE || 'puppeteer-core'); }
catch (e) {
  console.error('Missing puppeteer-core — run `npm install` in this folder');
  console.error('(or set PUPPETEER_CORE to an existing puppeteer-core path).');
  process.exit(1);
}

const APP_URL = process.env.APP_URL || 'https://testok-w654.onrender.com/';
const CHROME  = process.env.CHROME  || '/usr/bin/google-chrome';
const OUT     = process.env.OUT     || path.join(__dirname, 'walk.webm');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function click(page, sel, nth = 0) {
  const ok = await page.evaluate((s, n) => {
    const e = [...document.querySelectorAll(s)]; if (!e[n]) return false; e[n].click(); return true;
  }, sel, nth);
  if (!ok) throw new Error('no element: ' + sel);
}
async function clickText(page, sel, text) {
  const ok = await page.evaluate((s, t) => {
    const els = [...document.querySelectorAll(s)];
    const el = els.find((e) => e.textContent.trim() === t) || els.find((e) => e.textContent.trim().includes(t));
    if (!el) return false;
    (el.closest('button,a,[role="button"]') || el).click(); return true;
  }, sel, text);
  if (!ok) throw new Error(`no "${text}" in ${sel}`);
}
const closeModal = (page) => page.evaluate(() => {
  const b = document.querySelector('.schematic-modal-close'); if (b) b.click();
});

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--force-color-profile=srgb'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1672, height: 941, deviceScaleFactor: 1 });

  console.error('loading ' + APP_URL);
  await page.goto(APP_URL, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await page.waitForFunction(() => document.body.innerText.includes('Run evaluation'), { timeout: 90000 });
  await sleep(1200);

  console.error('recording -> ' + OUT);
  const rec = await page.screencast({ path: OUT });
  await sleep(1500);                                                            // show loaded app

  // 1 — context tour (datasheet / BOM / test procedure / schematic), then collapse
  await click(page, '.context-handle');                              await sleep(1300);
  await clickText(page, '.ctx-tab', 'Datasheet');                    await sleep(1300);
  await clickText(page, '.ctx-tab', 'BOM');                          await sleep(1300);
  await clickText(page, '.ctx-tab', 'Test procedure');               await sleep(1300);
  await clickText(page, '.ctx-tab', 'Schematic');                    await sleep(1700);
  await click(page, '.panel-close');                                 await sleep(1100);

  // 2/3/4 — select board, model, test
  await click(page, '.board-picker-trigger');                        await sleep(1000);
  await clickText(page, '.bp-item-name', 'HW-131');                  await sleep(1100);
  await click(page, '.backend-trigger');                             await sleep(900);
  await clickText(page, '.backend-option-name', 'mock');             await sleep(1000);
  await click(page, '.scenario-trigger');                            await sleep(900);
  await clickText(page, '.scenario-option-name', 'Marginal ripple'); await sleep(1100);

  // 5/6 — run + diagnosis
  await clickText(page, 'button', 'Run evaluation');
  await page.waitForFunction(() => !document.body.innerText.includes('Waiting on the loop'), { timeout: 20000 }).catch(() => {});
  await sleep(3800);

  // 7 — schematic fault highlight
  await clickText(page, 'button', 'Show on schematic');              await sleep(2800);
  await closeModal(page);                                            await sleep(900);
  // 8 — PCB fault highlight
  await clickText(page, 'button', 'Show on board');                  await sleep(2800);
  await closeModal(page);                                            await sleep(900);

  // 9 — download report
  await click(page, '.export-trigger');                              await sleep(1100);
  await clickText(page, '.export-option-name', 'PDF');               await sleep(2000);

  await rec.stop();
  await browser.close();
  console.error('done');
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
