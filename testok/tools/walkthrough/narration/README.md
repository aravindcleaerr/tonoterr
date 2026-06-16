# Walkthrough narration + captions

Voiceover + captions for the `/testok` "Watch it run" video.

## How captions ship

The video on `/testok` is **clean** (no baked-in text); captions are a **soft
`<track>`** (`images/walkthrough.vtt`), shown by default and toggleable via the
player's CC button. Their look is set by the `video::cue` rule in
`testok/index.html`. (A burned-in copy is available too — see `--burn`.)

## Files

- **`subtitles.srt` / `subtitles.vtt`** — the timed captions (`.vtt` is the soft track).
- **`make-narration.py`** — places per-line audio on the beats, writes the captions,
  and muxes the audio over the clean walkthrough video.
- **`audio/`** — per-line audio (`line_00.wav … line_10.wav`). *Git-ignored.*

Script lines live in `make-narration.py` (`SPOKEN` = read-aloud, `SUBS` = on-screen).
The human-recording practice script is in the private `testok` repo at
`pitch/walkthrough-narration.md`.

## Current voice

Interim **Sarvam TTS** — `bulbul:v2`, `en-IN`, speaker **`abhilash`** (calm male
Indian-English). To be replaced with a human voice via the same pipeline.

## Re-voice it (e.g. with your own recording)

1. Put one clip per line in `audio/` as `line_00.wav … line_10.wav` (in order; mono WAV).
2. Run:
   ```bash
   python3 make-narration.py
   ```
   → writes `walkthrough-narrated.mp4` (clean + audio) and `subtitles.vtt`.
3. Ship it:
   ```bash
   cp walkthrough-narrated.mp4 ../../../images/walkthrough.mp4
   cp subtitles.vtt            ../../../images/walkthrough.vtt
   ```
   then commit.

### Regenerate the interim TTS instead
```bash
SARVAM_KEY=your_key python3 make-narration.py --tts
```

### Standalone burned-in copy (e.g. WhatsApp, where soft subs don't travel)
```bash
python3 make-narration.py --burn    # -> walkthrough-narrated-burned.mp4
```

## Notes

- `BEATS` is the timing contract with the video — each line lands on its beat and is
  nudged only enough to avoid overlap, so a new voice re-syncs automatically.
- Requires `ffmpeg` / `ffprobe`. `--tts` also needs a Sarvam key + network.
