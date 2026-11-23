import json
import tempfile
import unittest
from pathlib import Path

from simpligen.render import (MIN_SCENE, PAD, Scene, load_project,
                              media_duration, render, scene_length)


class SceneFileTests(unittest.TestCase):
    def _write(self, data):
        f = Path(tempfile.mkdtemp()) / "s.json"
        f.write_text(json.dumps(data))
        return f

    def test_loads_scenes_and_voice(self):
        p = load_project(self._write({"voice": "Samantha", "scenes": [{"title": "Hi"}]}))
        self.assertEqual(p.voice, "Samantha")
        self.assertEqual(p.scenes[0].title, "Hi")

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            load_project(self._write({"scenes": []}))

    def test_rejects_missing_title(self):
        with self.assertRaises(ValueError):
            load_project(self._write({"scenes": [{"narration": "x"}]}))


class TimingTests(unittest.TestCase):
    def test_explicit_duration_wins(self):
        self.assertEqual(scene_length(Scene("t", duration=7), 2.0), 7.0)

    def test_no_audio_uses_minimum(self):
        self.assertEqual(scene_length(Scene("t"), None), MIN_SCENE)

    def test_audio_plus_padding(self):
        self.assertAlmostEqual(scene_length(Scene("t"), 5.0), 5.0 + PAD)


class EndToEndTests(unittest.TestCase):
    def test_renders_mp4_of_expected_length(self):
        d = Path(tempfile.mkdtemp())
        f = d / "s.json"
        f.write_text(json.dumps({"scenes": [
            {"title": "One", "duration": 2},
            {"title": "Two", "duration": 3},
        ]}))
        stats = render(f, d / "out.mp4", workdir=d / "work")
        self.assertTrue((d / "out.mp4").exists())
        self.assertAlmostEqual(media_duration(d / "out.mp4"), 5.0, delta=0.3)
        self.assertEqual(stats["scenes"], 2)


if __name__ == "__main__":
    unittest.main()
