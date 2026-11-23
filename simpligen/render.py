"""simpligen VideoStudio — local, zero-API video generation.

A scene file (JSON) becomes an MP4:
  Pillow draws each slide -> local TTS voices the narration -> ffmpeg
  times each slide to its audio, crossfades, and concatenates.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30
FADE = 0.5
MIN_SCENE = 2.5
PAD = 0.6  # seconds of breathing room after narration

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


@dataclass
class Scene:
    title: str
    narration: str = ""
    subtitle: str = ""
    bg: str = "#111827"
    fg: str = "#F9FAFB"
    accent: str = "#22D3EE"
    duration: float | None = None


@dataclass
class Project:
    scenes: list[Scene]
    voice: str | None = None
    meta: dict = field(default_factory=dict)


def load_project(path: str | Path) -> Project:
    data = json.loads(Path(path).read_text())
    raw = data["scenes"] if isinstance(data, dict) else data
    if not raw:
        raise ValueError("scene file has no scenes")
    scenes = []
    for i, s in enumerate(raw):
        if "title" not in s:
            raise ValueError(f"scene {i} is missing 'title'")
        scenes.append(Scene(**s))
    voice = data.get("voice") if isinstance(data, dict) else None
    return Project(scenes=scenes, voice=voice)


def _font(size: int) -> ImageFont.FreeTypeFont:
    for f in FONT_CANDIDATES:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default(size)


def draw_slide(scene: Scene, index: int, total: int, out: Path) -> Path:
    img = Image.new("RGB", (W, H), scene.bg)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 24, H], fill=scene.accent)
    title_font, sub_font, small = _font(110), _font(48), _font(30)
    lines = textwrap.wrap(scene.title, width=26) or [""]
    y = H // 2 - (len(lines) * 130) // 2 - (40 if scene.subtitle else 0)
    for line in lines:
        d.text((140, y), line, font=title_font, fill=scene.fg)
        y += 130
    if scene.subtitle:
        for line in textwrap.wrap(scene.subtitle, width=60):
            d.text((144, y + 30), line, font=sub_font, fill=scene.accent)
            y += 62
    d.text((140, H - 90), "simpligen", font=small, fill=scene.accent)
    d.text((W - 220, H - 90), f"{index + 1} / {total}", font=small, fill=scene.fg)
    img.save(out)
    return out


def tts_engine() -> str | None:
    for name in ("say", "espeak-ng", "espeak"):
        if shutil.which(name):
            return name
    return None


def synthesize(text: str, out_wav: Path, voice: str | None = None) -> bool:
    """Write narration to WAV with whatever offline TTS exists. False if none."""
    engine = tts_engine()
    if not text.strip() or engine is None:
        return False
    if engine == "say":
        aiff = out_wav.with_suffix(".aiff")
        cmd = ["say", "-o", str(aiff)] + (["-v", voice] if voice else []) + [text]
        subprocess.run(cmd, check=True)
        _ff(["-i", str(aiff), "-ar", "44100", "-ac", "2", str(out_wav)])
    else:
        subprocess.run([engine, "-w", str(out_wav), text], check=True)
    return True


def media_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def scene_length(scene: Scene, audio_seconds: float | None) -> float:
    if scene.duration:
        return float(scene.duration)
    if audio_seconds is None:
        return MIN_SCENE
    return max(MIN_SCENE, audio_seconds + PAD)


def _ff(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def render_clip(png: Path, wav: Path | None, seconds: float, out: Path) -> Path:
    fade_out = max(0.0, seconds - FADE)
    vf = f"fade=t=in:st=0:d={FADE},fade=t=out:st={fade_out:.3f}:d={FADE},format=yuv420p"
    audio = (["-i", str(wav)] if wav else
             ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"])
    _ff(["-loop", "1", "-framerate", str(FPS), "-i", str(png), *audio,
         "-t", f"{seconds:.3f}", "-vf", vf, "-af", "apad",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-c:a", "aac", "-b:a", "160k", "-r", str(FPS), str(out)])
    return out


def render(scene_file: str | Path, output: str | Path, workdir: Path | None = None) -> dict:
    t0 = time.perf_counter()
    project = load_project(scene_file)
    tmp = Path(workdir or tempfile.mkdtemp(prefix="simpligen-"))
    tmp.mkdir(parents=True, exist_ok=True)
    clips = []
    total = len(project.scenes)
    for i, sc in enumerate(project.scenes):
        png = draw_slide(sc, i, total, tmp / f"s{i:03}.png")
        wav = tmp / f"s{i:03}.wav"
        has_audio = synthesize(sc.narration, wav, project.voice)
        secs = scene_length(sc, media_duration(wav) if has_audio else None)
        clips.append(render_clip(png, wav if has_audio else None, secs, tmp / f"c{i:03}.mp4"))
    listing = tmp / "list.txt"
    listing.write_text("".join(f"file '{c}'\n" for c in clips))
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    _ff(["-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy",
         "-movflags", "+faststart", str(out)])
    stats = {
        "output": str(out),
        "scenes": total,
        "video_seconds": round(media_duration(out), 2),
        "render_seconds": round(time.perf_counter() - t0, 2),
        "bytes": out.stat().st_size,
        "tts": tts_engine() or "none",
    }
    return stats


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        print("usage: simpligen <scenes.json> <out.mp4>")
        return 2
    print(json.dumps(render(argv[0], argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
