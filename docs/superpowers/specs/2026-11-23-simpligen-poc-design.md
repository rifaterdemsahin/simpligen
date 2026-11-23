# simpligen PoC — design (short)

**Intent:** prove "local video generation" end to end: script in, narrated MP4
out, on a laptop, with no cloud APIs. Then show it publicly.

**Goals:** JSON scene file → 1080p MP4; offline TTS; tests; demo video made by
the tool itself; cost write-up; comparison with HyperFrames; public page on Fly.io.

**Non-goals:** generative AI footage, a GUI editor, server-side rendering.

**Approaches considered**
1. *Pillow + OS TTS + ffmpeg* (chosen): minimal dependencies, fast, deterministic.
2. *HTML + headless Chrome (HyperFrames/Remotion style)*: richer motion, heavier
   toolchain. Documented as the comparison and a future back-end.
3. *Local diffusion video models*: GBs of weights and slow on a laptop, too heavy for a PoC.

**Decisions:** JSON rather than YAML (no extra dependency). Scene length is the
narration length + 0.6 s, with a 2.5 s minimum. Deploy as a static nginx site on Fly.io with
auto-stop. The user said "go" and skipped the design questions.
