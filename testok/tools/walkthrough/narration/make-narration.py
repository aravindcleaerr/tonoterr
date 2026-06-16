#!/usr/bin/env python3
"""
Assemble the narrated + subtitled /testok walkthrough.

Pipeline:
  per-line audio (TTS or your own recordings)
    -> placed on the beat timeline
    -> narration.wav + subtitles.srt
    -> burned-in subtitles + muxed audio over ../../images/walkthrough.mp4
    -> walkthrough-narrated.mp4   (copy that over ../../images/walkthrough.mp4 to ship)

Re-voicing (the whole point of keeping this):
  - Record/obtain one clip per LINE below, named line_00.wav .. line_10.wav,
    in ./audio/ (in order), then:   python3 make-narration.py
  - Or regenerate the interim TTS voice (Sarvam bulbul:v2 / en-IN / "abhilash"):
        SARVAM_KEY=xxx python3 make-narration.py --tts

The BEATS list is the timing contract with the video; the placement logic lands
each line on its beat and nudges later lines only enough to avoid overlap, then
writes subtitles.srt to match. So a new voice re-syncs automatically.

Requires: ffmpeg, ffprobe, python3.  (--tts also needs a Sarvam key + network.)
"""
import os, sys, json, base64, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(HERE, "audio")
VIDEO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "images", "walkthrough.mp4"))
OUT   = os.path.join(HERE, "walkthrough-narrated.mp4")
SRT   = os.path.join(HERE, "subtitles.srt")
WAV   = os.path.join(HERE, "narration.wav")

# Beat start (seconds) each narration line should land on — the timing contract.
BEATS = [1, 5, 10, 15, 21, 25, 30, 35, 39, 43, 48]

# Spoken text (TTS / read aloud) — flows naturally end to end.
SPOKEN = [
 "TestOK is an AI layer that sits on top of your bench instruments.",
 "It first reads the board's design — the datasheet, the BOM, the test procedure, and the schematic.",
 "You simply select the board, the model, and the test you wish to run.",
 "On Run, it drives the power supply, load, multimeter and scope itself — logging every SCPI command on the wire.",
 "Within seconds, you get a verdict: this board has failed.",
 "And here is the most important part — the diagnosis.",
 "High output ripple, but clean DC regulation — the likely cause is the output capacitor.",
 "TestOK then points to the exact component on the schematic,",
 "and on the actual board.",
 "Finally, it exports a complete, audit-ready report,",
 "with the verdict, the measurements and the reasoning, all in one place.",
]

# Subtitle text (continuation ellipses on the split lines 8-11).
SUBS = [
 "TestOK is an AI layer that sits on top of your bench instruments.",
 "It first reads the board's design — datasheet, BOM, test procedure and schematic.",
 "You simply select the board, the model, and the test you wish to run.",
 "On Run, it drives the power supply, load, multimeter and scope itself — logging every SCPI command on the wire.",
 "Within seconds, you get a verdict: this board has failed.",
 "And here is the most important part — the diagnosis.",
 "High output ripple, but clean DC regulation — the likely cause is the output capacitor.",
 "TestOK then points to the exact component on the schematic…",
 "…and on the actual board.",
 "Finally, it exports a complete, audit-ready report…",
 "…with the verdict, the measurements and the reasoning, all in one place.",
]

# Burned-in subtitle styling (libass force_style): white text, translucent box.
SUB_STYLE = ("FontName=DejaVu Sans,FontSize=25,PrimaryColour=&H00FFFFFF,"
             "BorderStyle=3,Outline=2,Shadow=0,BackColour=&H64000000,"
             "Alignment=2,MarginV=30")

# Interim TTS voice used for the first cut.
TTS = dict(model="bulbul:v2", language="en-IN", speaker="abhilash",
           pitch=0, pace=1.0, loudness=1.0, sample_rate=22050)


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out)


def sarvam_tts(key):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audios = []
    for i in range(0, len(SPOKEN), 3):                 # API caps inputs at 3
        req = {"inputs": SPOKEN[i:i+3], "target_language_code": TTS["language"],
               "speaker": TTS["speaker"], "pitch": TTS["pitch"], "pace": TTS["pace"],
               "loudness": TTS["loudness"], "speech_sample_rate": TTS["sample_rate"],
               "enable_preprocessing": True, "model": TTS["model"]}
        r = urllib.request.Request("https://api.sarvam.ai/text-to-speech",
                                   data=json.dumps(req).encode(),
                                   headers={"api-subscription-key": key,
                                            "Content-Type": "application/json"})
        audios += json.load(urllib.request.urlopen(r, timeout=60))["audios"]
    for i, a in enumerate(audios):
        open(os.path.join(AUDIO_DIR, f"line_{i:02d}.wav"), "wb").write(base64.b64decode(a))
    print(f"  wrote {len(audios)} TTS lines -> {AUDIO_DIR}")


def srt_ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main():
    if "--tts" in sys.argv:
        key = os.environ.get("SARVAM_KEY")
        if not key:
            sys.exit("set SARVAM_KEY=... to use --tts")
        sarvam_tts(key)

    files = [os.path.join(AUDIO_DIR, f"line_{i:02d}.wav") for i in range(len(BEATS))]
    missing = [os.path.basename(f) for f in files if not os.path.exists(f)]
    if missing:
        sys.exit(f"missing audio {missing[:3]}… — put line_00.wav..line_{len(BEATS)-1:02d}.wav "
                 f"in {AUDIO_DIR} (one per line, in order), or run with --tts")

    durs = [dur(f) for f in files]
    starts, prev = [], 0.0
    for i in range(len(BEATS)):
        s = max(BEATS[i], prev + 0.12)                 # land on beat; avoid overlap
        starts.append(s); prev = s + durs[i]

    # narration.wav: delay each clip to its start, then mix
    inp, filt = [], []
    for i, f in enumerate(files):
        inp += ["-i", f]
        filt.append(f"[{i}]adelay={int(starts[i]*1000)}[a{i}]")
    fc = ";".join(filt) + ";" + "[" + "][".join(f"a{i}" for i in range(len(files))) + \
         f"]amix=inputs={len(files)}:normalize=0:dropout_transition=0[out]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp,
                    "-filter_complex", fc, "-map", "[out]", WAV], check=True)

    # subtitles.srt — each line shows for its own duration (+0.3s linger)
    with open(SRT, "w") as fo:
        for i in range(len(BEATS)):
            end = starts[i] + durs[i] + 0.3
            if i < len(BEATS) - 1:
                end = min(end, starts[i+1])
            fo.write(f"{i+1}\n{srt_ts(starts[i])} --> {srt_ts(end)}\n{SUBS[i]}\n\n")

    # burn subtitles + mux narration audio over the (silent) walkthrough video
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VIDEO, "-i", WAV,
                    "-vf", f"subtitles={SRT}:force_style='{SUB_STYLE}'",
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "21",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                    "-movflags", "+faststart", OUT], check=True)
    print(f"  -> {SRT}")
    print(f"  -> {OUT}   (copy over ../../../images/walkthrough.mp4 to ship)")


if __name__ == "__main__":
    main()
