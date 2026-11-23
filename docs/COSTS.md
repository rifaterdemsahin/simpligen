# simpligen VideoStudio — cost of use

_Measured 2026-11-23 on an Apple M1 Max (macOS, ffmpeg 9.0.2, Python 3.15, Pillow 13)._

## TL;DR

| Item | Cost |
|---|---|
| Software licences | **$0** (Python, Pillow, ffmpeg, macOS `say` — all free / bundled) |
| API / per-render fees | **$0** (no network calls, no keys) |
| Render compute (local) | ~**16 s of laptop time per minute of video** |
| Electricity per minute of video | ~**$0.00004** (≈30 W × 16 s at $0.30/kWh) |
| Hosting the PoC site on Fly.io | **$0–$2.19 / month** (see below) |

## Measured render (the demo video in this repo)

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
