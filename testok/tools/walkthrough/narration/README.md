# Walkthrough narration + subtitles

Voiceover + burned-in subtitles for the `/testok` "Watch it run" video.

## Files

- **`subtitles.srt`** — the timed English subtitles currently burned into the video.
- **`make-narration.py`** — rebuilds the narrated + subtitled clip from per-line audio:
  places each line on its beat, writes `subtitles.srt`, then burns the subs and muxes
  the audio over `../../../images/walkthrough.mp4` → `walkthrough-narrated.mp4`.
- **`audio/`** — per-line audio (`line_00.wav … line_10.wav`), one clip per script line.
  *Git-ignored* (regenerable / your own recordings).

The script lines themselves live in `make-narration.py` (`SPOKEN` = read-aloud text,
`SUBS` = on-screen subtitle text). The practice script is in the private `testok` repo
at `pitch/walkthrough-narration.md`.

## Current voice

Interim **Sarvam TTS** — `bulbul:v2`, `en-IN`, speaker **`abhilash`** (calm male
Indian-English). To be replaced with a human voice using the same pipeline.

## Re-voice it (e.g. with your own recording)

1. Get one audio clip per line, named `line_00.wav … line_10.wav`, into `audio/`
   (in the same order as the script). Mono WAV is ideal.
2. Run:
   ```bash
   python3 make-narration.py
   ```
3. Review `walkthrough-narrated.mp4`, then copy it over `../../../images/walkthrough.mp4`
   and commit to ship it on `/testok`.

### Regenerate the interim TTS instead

```bash
SARVAM_KEY=your_key python3 make-narration.py --tts
```

## Notes

- `BEATS` in the script is the timing contract with the video — each line lands on its
  beat and is nudged only enough to avoid overlap, so a new voice re-syncs automatically.
- Requires `ffmpeg` / `ffprobe`. `--tts` also needs a Sarvam key + network.
