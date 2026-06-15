# /testok walkthrough recorder

Regenerates the **"Watch it run"** video on `tonoterr.vercel.app/testok` by
driving the *live* TestOK app through one full evaluation, then encoding it and
appending a scroll through the generated PDF report.

Outputs (committed assets the page references):
- `../../images/walkthrough.mp4`
- `../../images/walkthrough-poster.jpg`

## Run it

```bash
npm install          # once — pulls puppeteer-core
./build.sh           # records, encodes, joins, writes the two assets above
```

Then commit the two regenerated files.

## What it does

`record.js` (puppeteer + `page.screencast`) drives these beats on the app:

1. open the **context** panel → Datasheet → BOM → Test procedure → Schematic → collapse
2. select **board** (HW-131 LDO) · **model** (mock) · **test** (Marginal ripple)
3. **Run evaluation** → diagnosis
4. **Show on schematic** → fault component (COUT) highlighted → close
5. **Show on board** → PCB fault highlighted → close
6. **Export → PDF**

`build.sh` then: encodes the recording (H.264, 1500-wide), renders
`../../examples/sample-report.pdf` into a vertical "report scroll" segment, and
crossfade-joins them into `walkthrough.mp4` (+ a poster frame).

## Requirements

- **node** + `npm install` here (puppeteer-core)
- **Chrome/Chromium** — set `CHROME` or default `/usr/bin/google-chrome`
- **ffmpeg / ffprobe**, **pdftoppm** (poppler-utils), **python3 + Pillow**

## Tuning / gotchas

- Records against `APP_URL` (default `https://testok-w654.onrender.com/`, the
  Render origin). Override e.g. `APP_URL=https://testok-bench.vercel.app/ ./build.sh`.
  The free Render service sleeps after 15 min idle; the script warms it first.
- The closing scroll uses `../../examples/sample-report.pdf` (override with
  `REPORT=...`). If the report format changes, regenerate that PDF first.
- **Selectors** (`.ctx-tab`, `.board-picker-trigger`, `.show-on-schematic`,
  `.schematic-modal-close`, …) mirror `design/TestOK/app.jsx` in the **TestOK
  app repo**. If that UI changes, update the selectors in `record.js`.
- Pacing lives in the `sleep(...)` calls in `record.js` — adjust to taste.
