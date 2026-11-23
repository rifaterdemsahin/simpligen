# simpligen VideoStudio — cost of use

_Measured 2026-11-23 on an Apple M1 Max (macOS, ffmpeg 9.0.2, Python 3.15, Pillow 13).
v0.2.0 numbers use Kokoro-82M TTS in Docker (`kokoro-fastapi-cpu`)._

## TL;DR

| Item | Cost |
|---|---|
| Software licences | **$0** (Python, Pillow, ffmpeg, librsvg, Kokoro Apache 2.0) |
| API / per-render fees | **$0** (no network calls, no keys) |
| Render compute (local) | ~**30 s per minute of video** with Kokoro (~16 s with macOS `say`) |
| Electricity per minute of video | ~**$0.0001** (≈40 W × 30 s at $0.30/kWh) |
| Kokoro container | ~2.1 GB RAM while running, 5.6 GB image on disk |
| Hosting the PoC site on Fly.io | **$0–$2.19 / month** (see below) |

## v0.4.0: animated intro + HyperFrames comparison scene

| Metric | Value |
|---|---|
| Scenes | 9 (animated intro + 8 slides) |
| Intro animation | ~50 ms per 1080p frame (180 frames in 8.6 s standalone) |
| Video | 2:03, rendered in 95–160 s (Kokoro speed varies run to run) |

## v0.3.0: AI images + emojis

| Metric | Value |
|---|---|
| Scenes | 8 (each: AI background, emoji, SVG diagram, Kokoro narration) |
| Image model | FLUX.2 Klein 4B, 8-bit, via mflux (one-time download ~15 GB, ~7.5 min) |
| Image time | 31–42 s per 1344×768 image, **34 s average** (M1 Max) |
| Image peak memory | 9.3 GB |
| Prompt writer | gemma3:12b in Ollama (already installed) |
| Video | 75.7 s, rendered in 44 s, 5.8 MB |
| Cost per image | **$0** (≈40 W × 34 s ≈ $0.0001 electricity) |

Locally, the cost of an image is laptop time, not money.

## v0.2.0 render: Kokoro voice + SVG diagrams

| Metric | Value |
|---|---|
| Scenes | 7 (each with an SVG diagram) |
| Output length | 63.7 s, 1920×1080, H.264 + AAC, 2.25 MB |
| Render, Kokoro warm | ~30–31 s (about 2× faster than real time) |
| Render, Kokoro cold (first request) | 78 s |
| Kokoro container memory | 2.14 GiB |

| Videos / month (1 min each) | Laptop time | Electricity (est.) | API fees |
|---|---|---|---|
| 10 | ~5 min | ~$0.001 | $0 |
| 100 | ~50 min | ~$0.01 | $0 |
| 1,000 | ~8–9 h | ~$0.10 | $0 |

For comparison, cloud TTS at a typical ~$15 per million characters would cost about
$0.015 per minute of narration (~1,000 characters). Kokoro makes that $0.

## v0.1.0 render: macOS `say`, no diagrams

```
python3 -m simpligen examples/demo.json site/demo.mp4
```

| Metric | Value |
|---|---|
| Scenes | 6 |
| Output length | 42.7 s, 1920×1080, H.264 + AAC |
| Wall-clock render | 11.6 s (**3.7× faster than real time**) |
| CPU time | 22.5 s user + 2.2 s sys |
| Peak memory | ~600 MB |
| File size | 1.28 MB (~1.8 MB per minute) |

Scaling (linear, since each scene is rendered independently):

| Videos / month (1 min each) | Laptop time | Electricity (est.) | API fees |
|---|---|---|---|
| 10 | ~3 min | < $0.01 | $0 |
| 100 | ~27 min | ~$0.004 | $0 |
| 1,000 | ~4.5 h | ~$0.04 | $0 |

The real cost is **your time writing scene files**, not compute.

## Hosting on Fly.io

The deployed site is static (`index.html` + a 1.3 MB MP4) served by nginx on one
`shared-cpu-1x` / 256 MB machine with `auto_stop_machines` enabled.

| Scenario | Monthly cost |
|---|---|
| Machine running 24/7 | $2.19 (Fly list price, effective 2026-10-01) |
| Auto-stop, low traffic (machine mostly stopped) | cents (rootfs storage while stopped) |
| Bandwidth | ~1.3 MB per full video view; 1,000 views ≈ 1.3 GB egress |

Check current rates at <https://fly.io/pricing> — egress pricing for 2026 was
not confirmed when this was written.

### Rendering *on* Fly (not done in this PoC)

Running the renderer server-side would need a bigger machine (ffmpeg peaked at
~600 MB) and Linux TTS (`espeak-ng`, already supported as a fallback). A
`shared-cpu-1x` / 1 GB machine that only runs while rendering would cost
fractions of a cent per video.

## Cost compared with HyperFrames

See [HYPERFRAMES-COMPARISON.md](HYPERFRAMES-COMPARISON.md). In short, both are
free open-source renderers with no per-render fees. HyperFrames' paid
costs come from its **optional** Studio Pro plan ($25/month for generative
models and 25,000 credits) and cloud/Lambda rendering. simpligen has no paid
tier at all.
