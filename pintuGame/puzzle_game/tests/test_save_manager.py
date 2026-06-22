import json
import os
import tempfile
import unittest

from src.save_manager import SaveManager


class SaveManagerTests(unittest.TestCase):
    def test_missing_save_is_created_and_result_updates_ranking(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_path = os.path.join(tmp, "save_data.json")
            manager = SaveManager(save_path)
            self.assertTrue(os.path.exists(save_path))
            manager.record_result(
                {
                    "image_id": "star_lighthouse",
                    "image_title": "星海灯塔",
                    "difficulty": 3,
                    "mode": "standard",
                    "elapsed": 42,
                    "steps": 30,
                    "hints": 1,
                    "rating": "A",
                    "finished_at": "2026-06-22 12:00:00",
                    "score_card": None,
                }
            )
            key = manager.ranking_key("star_lighthouse", "3", "standard")
            self.assertEqual(manager.data["rankings"][key]["best_time"], 42)
            self.assertEqual(manager.data["rankings"][key]["min_steps"], 30)

    def test_corrupt_save_is_backed_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_path = os.path.join(tmp, "save_data.json")
            with open(save_path, "w", encoding="utf-8") as handle:
                handle.write("{bad json")
            manager = SaveManager(save_path)
            self.assertIn("settings", manager.data)
            backups = [name for name in os.listdir(tmp) if name.endswith(".bak")]
            self.assertTrue(backups)
            with open(save_path, "r", encoding="utf-8") as handle:
                self.assertIsInstance(json.load(handle), dict)


if __name__ == "__main__":
    unittest.main()
