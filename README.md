# 🎬 simpligen
Local video generation. **v0.4.0**

🌐 **Live demo:** https://simpligen-poc.fly.dev/ · 📼 **Video:** [site/demo.mp4](site/demo.mp4) · 🏗️ **Architecture:** https://simpligen-poc.fly.dev/architecture.html · 🎨 **AI images:** https://simpligen-poc.fly.dev/gallery.html · 🖼️ **Local images guide:** https://simpligen-poc.fly.dev/images.html

**simpligen VideoStudio** turns a JSON script into a narrated 1080p MP4 on your
own machine:

- 🗺️ **Slides + SVG diagrams**: Pillow draws text, `rsvg-convert` places a per-scene SVG
- 🔊 **Voice**: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) running locally in Docker
  ([kokoro-fastapi](https://github.com/remsky/Kokoro-FastAPI)), with automatic fallback to
  macOS `say` / `espeak-ng`
- 🎨 **AI backgrounds**: per-scene `image`, generated locally by FLUX.2 Klein 4B (mflux) from prompts written by Ollama `gemma3:12b` ([tools/gen_images.py](tools/gen_images.py))
- ✨ **Animated intro**: `"animate": "intro"` draws a title sequence frame by frame ([simpligen/animate.py](simpligen/animate.py)); the same intro as a HyperFrames composition is in [comparisons/hyperframes-intro/](comparisons/hyperframes-intro/index.html)
- 😀 **Emoji**: per-scene `emoji`, drawn in colour above the title
- ⚙️ **Encode**: ffmpeg times each slide to its narration, crossfades and concatenates

No API keys. No per-render cost.

## 🧰 Claude Code skill: start to end

The whole workflow is packaged as a project skill: [`.claude/skills/simpligen-video/`](.claude/skills/simpligen-video/SKILL.md).
Claude Code picks it up automatically in this repo. Ask it to "make a new simpligen video" or "ship v0.5.0".

| File | What it is |
|---|---|
| [SKILL.md](.claude/skills/simpligen-video/SKILL.md) | The pipeline (preflight → script → images → render → look → pages → ship → verify), scene schema, site rules, common mistakes |
| [history.md](.claude/skills/simpligen-video/history.md) | How the PoC was built from v0.1 to v0.4.0: what each version added, measured numbers, and why |
| [scripts/preflight.sh](.claude/skills/simpligen-video/scripts/preflight.sh) | Read-only check of tools, Kokoro, Ollama, mflux, model cache, disk and Fly |
| [scripts/ship.sh](.claude/skills/simpligen-video/scripts/ship.sh) | Tests → version check → commit/tag/push → fly deploy → live verify (`--dry-run` supported) |
| [templates/scenes.example.json](.claude/skills/simpligen-video/templates/scenes.example.json) | Starter script for a new video |

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
to the scene file), `image` (background picture), `emoji`, `animate` (`intro`), `bg`, `fg`, `accent`, `duration`. Set `KOKORO_URL` to point
at another Kokoro server.

Example diagrams: [examples/svg/](examples/svg/)

## 🎨 Generate scene images (optional)

```bash
uv tool install mflux                       # FLUX.2 Klein 4B (~15 GB) downloads on first run
ollama pull gemma3:12b                      # writes the prompts
python3 tools/gen_images.py examples/demo.json examples/images
python3 tools/build_gallery.py              # site/gallery.html
```

## 🧪 Test

```bash
python3 -m unittest discover -s tests -t . -v
```

## 📚 Docs
- 💰 [Cost of use](docs/COSTS.md)
- ⚔️ [simpligen vs HyperFrames](docs/HYPERFRAMES-COMPARISON.md)
- 📐 [Design](docs/superpowers/specs/2026-11-23-simpligen-poc-design.md)
- 🏠 [Live page source](site/index.html)
- 🏗️ [Architecture: Ollama, mflux, Kokoro, simpligen](site/architecture.html)
- 🖼️ [Local image generation: what to install and load](site/images.html)
- 🎨 [AI image gallery with prompts](site/gallery.html) · [prompts.json](examples/images/prompts.json)

## 🔊 Audio credit

Demo narration: **Kokoro-82M** (hexgrad, Apache 2.0), voice `af_heart`, generated
locally via `ghcr.io/remsky/kokoro-fastapi-cpu`.
Demo images: **FLUX.2 Klein 4B** (Black Forest Labs, Apache 2.0) via mflux; prompts by **gemma3:12b** in Ollama.

## 🚀 Deploy (Fly.io)

```bash
fly deploy
```

`site/` (index.html, gallery.html, images.html, demo.mp4, gallery JPGs, diagrams) is served by nginx on an
auto-stopping shared-cpu-1x machine (app `simpligen-poc`).
