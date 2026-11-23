# simpligen vs HyperFrames (HeyGen)

Sources: [heygen-com/hyperframes README](https://github.com/heygen-com/hyperframes),
[HyperFrames overview](https://developers.heygen.com/hyperframes-overview). Checked 2026-11-23.

| | **simpligen VideoStudio (this PoC)** | **HyperFrames** |
|---|---|---|
| What it is | Python CLI: JSON scenes + SVG diagrams → narrated slide video | Framework: HTML/CSS/JS compositions → MP4 |
| Authoring | JSON (title, subtitle, narration, colours) | HTML with `data-*` timing attributes; GSAP, Lottie, Three.js, CSS, WAAPI |
| Render engine | Pillow + rsvg + ffmpeg (static frames, fades) | Headless Chrome seeks each frame + ffmpeg |
| Voice | Kokoro-82M in local Docker, fallback to OS TTS (`say` / `espeak-ng`) | Bring your own audio or use HeyGen models via `/media-use` |
| Requirements | Python 3 + Pillow + ffmpeg + librsvg (+ Docker for Kokoro) | Node.js 22+ + ffmpeg (+ Chrome via Puppeteer) |
| Licence | Repo default (PoC) | Apache 2.0 |
| Per-render fees | None | None for the open-source CLI |
| Paid options | None | Studio Pro $25/mo (HeyGen Video 1, Seedance, Lyria, 25k credits); cloud render; AWS Lambda |
| Determinism | Yes (same input → same frames; TTS is deterministic per voice) | Yes, a core design goal |
| Agent support | Simple enough to author by hand or LLM | First-class: Claude Code / Codex / Cursor skills, MCP connector |
| Visual ceiling | Static slides + SVG diagrams with fades | Anything a browser can draw; ~450 registry blocks |
| Render speed (measured) | 63.7 s video in ~31 s on M1 Max (Kokoro warm) | Not measured here (per-frame browser capture is typically heavier) |
| Footprint | ~600 MB peak RAM + ~2.1 GB for the Kokoro container, no browser | Node toolchain + headless Chrome |

## When to use which

- **simpligen**: fast, cheap, explainable pipeline for narrated explainers,
  status updates, training slides, CI-generated reports. Nothing to sign up for.
- **HyperFrames**: anything with real motion graphics, kinetic type, captions,
  charts, 3D, or when you want agents to compose rich HTML scenes and optionally
  use HeyGen's generative models.

## Natural next step

simpligen's scene JSON could be compiled into a HyperFrames HTML composition,
so the same script can render "fast and plain" locally or "rich" through
HyperFrames. A HyperFrames back-end for simpligen is the obvious v0.2 experiment.
