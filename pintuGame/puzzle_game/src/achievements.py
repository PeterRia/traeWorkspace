from . import config


def evaluate_result(save_data, result):
    unlocked = set(save_data.get("achievements", {}))
    new_ids = []

    def add(achievement_id, condition):
        if condition and achievement_id not in unlocked:
            new_ids.append(achievement_id)

    total_before = sum(int(rank.get("completed", 0)) for rank in save_data.get("rankings", {}).values())
    collected = {
        image_id
        for image_id, item in save_data.get("gallery", {}).items()
        if item.get("unlocked") or image_id == result["image_id"]
    }
    tile_count = result["difficulty"] * result["difficulty"]
    add("first_win", total_before == 0)
    add("no_hint", result["hints"] == 0)
    add("hard_clear", result["difficulty"] == 5)
    add("swift_3", result["difficulty"] == 3 and result["elapsed"] <= 60)
    add("steady_hands", result["steps"] <= tile_count * 8)
    add("collector", len(collected) >= 6)
    return [(achievement_id, *config.ACHIEVEMENT_DEFS[achievement_id]) for achievement_id in new_ids]
