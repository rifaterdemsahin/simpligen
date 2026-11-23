# simpligen
Local video generation.

**simpligen VideoStudio** turns a JSON script into a narrated 1080p MP4 on your
own machine. It uses Pillow for slides, offline TTS (`say` on macOS,
`espeak-ng` on Linux) and ffmpeg. There are no API keys and no per-render cost.

## Install

```bash
brew install ffmpeg          # or apt install ffmpeg espeak-ng
python3 -m pip install pillow
```

## Use

```bash
python3 -m simpligen examples/demo.json site/demo.mp4
```

Scene fields: `title` (required), `subtitle`, `narration`, `bg`, `fg`, `accent`, `duration`.
Top-level `voice` picks the TTS voice.

## Test

```bash
python3 -m unittest discover -s tests -t . -v
```

## Docs
- [Cost of use](docs/COSTS.md)
- [simpligen vs HyperFrames](docs/HYPERFRAMES-COMPARISON.md)
- [Design](docs/superpowers/specs/2026-11-23-simpligen-poc-design.md)

## Deploy (Fly.io)

```bash
fly launch --copy-config --no-deploy   # first time
fly deploy
```

`site/` (index.html + demo.mp4) is served by nginx on an auto-stopping
shared-cpu-1x machine.
