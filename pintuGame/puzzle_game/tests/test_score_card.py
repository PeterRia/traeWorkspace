import os
import tempfile
import unittest

from PIL import Image

from src.score_card import create_score_card


class ScoreCardTests(unittest.TestCase):
    def test_score_card_png_is_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            image_path = os.path.join(tmp, "source.png")
            output_path = os.path.join(tmp, "score.png")
            Image.new("RGBA", (256, 256), (75, 189, 180, 255)).save(image_path)
            path = create_score_card(
                {"image_title": "测试图", "difficulty": 3, "elapsed": 18, "steps": 9, "hints": 0, "rating": "S"},
                image_path,
                output_path,
            )
            self.assertEqual(path, output_path)
            self.assertTrue(os.path.exists(path))
            self.assertGreater(os.path.getsize(path), 1000)


if __name__ == "__main__":
    unittest.main()
