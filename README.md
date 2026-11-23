# 🎬 simpligen
Local video generation. **v0.2.1**

🌐 **Live demo:** https://simpligen-poc.fly.dev/ · 📼 **Video:** [site/demo.mp4](site/demo.mp4) · 🖼️ **Local images guide:** https://simpligen-poc.fly.dev/images.html

**simpligen VideoStudio** turns a JSON script into a narrated 1080p MP4 on your
own machine:

- 🗺️ **Slides + SVG diagrams**: Pillow draws text, `rsvg-convert` places a per-scene SVG
- 🔊 **Voice**: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) running locally in Docker
  ([kokoro-fastapi](https://github.com/remsky/Kokoro-FastAPI)), with automatic fallback to
  macOS `say` / `espeak-ng`
- ⚙️ **Encode**: ffmpeg times each slide to its narration, crossfades and concatenates

No API keys. No per-render cost.

## 📦 Install

```bash
brew install ffmpeg librsvg           # Linux: apt install ffmpeg librsvg2-bin espeak-ng
python3 -m pip install pillow
docker compose up -d kokoro           # local TTS on http://localhost:8880
```

## ▶️ Use

```bash
python3 -m simpligen examples/demo.json site/demo.mp4
```

Top level: `tts` (`auto` | `kokoro` | `say` | `espeak-ng` | `none`), `voice`
(Kokoro voice such as `af_heart` or `bm_george`, or a macOS voice name).
Scene fields: `title` (required), `subtitle`, `narration`, `svg` (path relative
to the scene file), `bg`, `fg`, `accent`, `duration`. Set `KOKORO_URL` to point
at another Kokoro server.

Example diagrams: [examples/svg/](examples/svg/)

## 🧪 Test

```bash
python3 -m unittest discover -s tests -t . -v
```

## 📚 Docs
- 💰 [Cost of use](docs/COSTS.md)
- ⚔️ [simpligen vs HyperFrames](docs/HYPERFRAMES-COMPARISON.md)
- 📐 [Design](docs/superpowers/specs/2026-11-23-simpligen-poc-design.md)
- 🏠 [Live page source](site/index.html)
- 🖼️ [Local image generation: what to install and load](site/images.html)

## 🔊 Audio credit

Demo narration: **Kokoro-82M** (hexgrad, Apache 2.0), voice `af_heart`, generated
locally via `ghcr.io/remsky/kokoro-fastapi-cpu`.

## 🚀 Deploy (Fly.io)

```bash
fly deploy
```

`site/` (index.html, images.html, demo.mp4, diagrams) is served by nginx on an
auto-stopping shared-cpu-1x machine (app `simpligen-poc`).
