import copy
from datetime import datetime
import json
import os
import shutil

from . import config, paths


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def default_data():
    gallery = {}
    for index, theme in enumerate(config.THEMES):
        gallery[theme["id"]] = {"unlocked": index <= 1, "completed": 0, "title": theme["title"]}
    return {
        "version": 1,
        "created_at": _now(),
        "updated_at": _now(),
        "settings": copy.deepcopy(config.DEFAULT_SETTINGS),
        "gallery": gallery,
        "rankings": {},
        "achievements": {},
        "history": [],
    }


class SaveManager:
    def __init__(self, file_path=None):
        self.file_path = file_path or paths.save_file()
        self.data = default_data()
        self.load()

    def load(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self.save()
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as handle:
                self.data = self._merge_defaults(json.load(handle))
        except Exception:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            try:
                shutil.copy2(self.file_path, self.file_path + f".broken_{stamp}.bak")
            except OSError:
                pass
            self.data = default_data()
            self.save()

    def _merge_defaults(self, loaded):
        data = default_data()
        if isinstance(loaded, dict):
            for key, value in loaded.items():
                if isinstance(data.get(key), dict) and isinstance(value, dict):
                    data[key].update(value)
                else:
                    data[key] = value
        for theme in config.THEMES:
            data["gallery"].setdefault(theme["id"], {"unlocked": False, "completed": 0})
            data["gallery"][theme["id"]]["title"] = theme["title"]
        for key, value in config.DEFAULT_SETTINGS.items():
            data["settings"].setdefault(key, value)
        return data

    def save(self):
        self.data["updated_at"] = _now()
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as handle:
            json.dump(self.data, handle, ensure_ascii=False, indent=2)

    def update_settings(self, **settings):
        self.data["settings"].update(settings)
        self.save()

    def ranking_key(self, image_id, difficulty, mode):
        return f"{image_id}|{difficulty}|{mode}"

    def record_result(self, result):
        key = self.ranking_key(result["image_id"], str(result["difficulty"]), result["mode"])
        rank = self.data["rankings"].setdefault(
            key,
            {
                "image_id": result["image_id"],
                "difficulty": str(result["difficulty"]),
                "mode": result["mode"],
                "completed": 0,
                "best_time": None,
                "min_steps": None,
                "best_rating": None,
            },
        )
        rank["completed"] += 1
        if rank["best_time"] is None or result["elapsed"] < rank["best_time"]:
            rank["best_time"] = result["elapsed"]
        if rank["min_steps"] is None or result["steps"] < rank["min_steps"]:
            rank["min_steps"] = result["steps"]
        rank["best_rating"] = _best_rating(rank.get("best_rating"), result["rating"])

        gallery = self.data["gallery"].setdefault(result["image_id"], {"unlocked": True, "completed": 0})
        gallery["unlocked"] = True
        gallery["completed"] = int(gallery.get("completed", 0)) + 1
        self._unlock_next_theme(result["image_id"])

        self.data["history"].insert(
            0,
            {
                "finished_at": result["finished_at"],
                "image_id": result["image_id"],
                "image_title": result["image_title"],
                "difficulty": str(result["difficulty"]),
                "mode": result["mode"],
                "elapsed": result["elapsed"],
                "steps": result["steps"],
                "hints": result["hints"],
                "rating": result["rating"],
                "score_card": result.get("score_card"),
            },
        )
        self.data["history"] = self.data["history"][:30]
        self.save()

    def _unlock_next_theme(self, image_id):
        ids = [theme["id"] for theme in config.THEMES]
        if image_id in ids and ids.index(image_id) + 1 < len(ids):
            next_id = ids[ids.index(image_id) + 1]
            self.data["gallery"].setdefault(next_id, {"unlocked": False, "completed": 0})
            self.data["gallery"][next_id]["unlocked"] = True

    def unlock_achievement(self, achievement_id):
        if achievement_id in self.data["achievements"]:
            return False
        title, desc = config.ACHIEVEMENT_DEFS[achievement_id]
        self.data["achievements"][achievement_id] = {"title": title, "desc": desc, "unlocked_at": _now()}
        self.save()
        return True


def _best_rating(current, incoming):
    order = {"S": 4, "A": 3, "B": 2, "C": 1}
    if current is None:
        return incoming
    return incoming if order.get(incoming, 0) > order.get(current, 0) else current
