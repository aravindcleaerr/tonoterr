#!/usr/bin/env bash
#
# Re-records the /testok "full walkthrough" video end-to-end and writes:
#   ../images/walkthrough.mp4
#   ../images/walkthrough-poster.jpg
#
# Usage:   npm install        # once, pulls puppeteer-core
#          ./build.sh
#
# Prereqs: node, Chrome (CHROME env or /usr/bin/google-chrome), ffmpeg,
#          pdftoppm (poppler-utils), python3 + Pillow.
#
# Env overrides: APP_URL (app to record), REPORT (pdf for the closing scroll),
#                CHROME (chrome binary).
set -euo pipefail
cd "$(dirname "$0")"

APP_URL="${APP_URL:-https://testok-w654.onrender.com/}"
REPORT="${REPORT:-../../examples/sample-report.pdf}"   # testok/examples/
OUTDIR="../../images"                                  # testok/images/
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for bin in node ffmpeg ffprobe pdftoppm python3; do
  command -v "$bin" >/dev/null || { echo "missing dependency: $bin" >&2; exit 1; }
done
[ -d node_modules/puppeteer-core ] || command -v puppeteer-core >/dev/null 2>&1 || \
  echo "note: if record.js fails, run 'npm install' here first" >&2

echo "==> warming $APP_URL (Render free tier sleeps after 15 min idle)"
curl -s -o /dev/null --max-time 90 "$APP_URL" || true
curl -s -o /dev/null --max-time 60 "${APP_URL%/}/api/boards" || true

echo "==> recording walkthrough"
OUT="$TMP/walk.webm" APP_URL="$APP_URL" node record.js

echo "==> encoding walk.mp4"
ffmpeg -y -loglevel error -i "$TMP/walk.webm" -vf "scale=1500:-2,fps=24" \
  -c:v libx264 -pix_fmt yuv420p -crf 30 -an -movflags +faststart "$TMP/walk.mp4"

echo "==> building report scroll from $REPORT"
pdftoppm -png -r 150 "$REPORT" "$TMP/page"
python3 - "$TMP" <<'PY'
import sys, glob, os
from PIL import Image
tmp = sys.argv[1]
pages = sorted(glob.glob(os.path.join(tmp, 'page*.png')))
W, content, gap, pad = 1500, 1080, 34, 70
sc = []
for p in pages:
    im = Image.open(p).convert('RGB'); r = content / im.width
    sc.append(im.resize((content, int(im.height * r))))
H = pad * 2 + sum(i.height for i in sc) + gap * (len(sc) - 1)
strip = Image.new('RGB', (W, H), (243, 239, 229)); y = pad
for im in sc:
    strip.paste(im, ((W - content) // 2, y)); y += im.height + gap
strip.save(os.path.join(tmp, 'strip.png'))
PY
ffmpeg -y -loglevel error -loop 1 -framerate 24 -t 7 -i "$TMP/strip.png" \
  -vf "crop=1500:844:0:'(ih-844)*min(1,max(0,(t-1.0)/5.0))',format=yuv420p" \
  -c:v libx264 -crf 28 -movflags +faststart "$TMP/report.mp4"

echo "==> joining with crossfade"
WD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/walk.mp4")
OFF=$(python3 -c "print(round($WD - 0.6, 3))")
ffmpeg -y -loglevel error -i "$TMP/walk.mp4" -i "$TMP/report.mp4" -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=0.6:offset=$OFF,format=yuv420p,fps=24" \
  -c:v libx264 -crf 29 -movflags +faststart "$OUTDIR/walkthrough.mp4"

echo "==> poster"
ffmpeg -y -loglevel error -ss 22 -i "$OUTDIR/walkthrough.mp4" -vframes 1 "$TMP/poster.png"
python3 -c "from PIL import Image; Image.open('$TMP/poster.png').convert('RGB').save('$OUTDIR/walkthrough-poster.jpg', quality=82, optimize=True)"

echo "==> done:"
echo "    $OUTDIR/walkthrough.mp4 ($(du -h "$OUTDIR/walkthrough.mp4" | cut -f1))"
echo "    $OUTDIR/walkthrough-poster.jpg"
