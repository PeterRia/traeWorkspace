SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 820
FPS = 60
TITLE = "幻彩滑动拼图"
BOARD_PIXELS = 620
BOARD_LEFT = 56
BOARD_TOP = 144

DIFFICULTIES = {3: "悠闲 3x3", 4: "进阶 4x4", 5: "大师 5x5"}
SHUFFLE_MOVES = {3: 90, 4: 180, 5: 320}
MODE_STANDARD = "standard"
MODE_LABELS = {MODE_STANDARD: "标准模式"}

THEMES = [
    {"id": "imagegen_cover", "title": "幻彩拼图门", "file": "imagegen_cover.png", "source": "imagegen"},
    {"id": "star_lighthouse", "title": "星海灯塔", "file": "star_lighthouse.png", "source": "pil"},
    {"id": "peach_path", "title": "桃源山径", "file": "peach_path.png", "source": "pil"},
    {"id": "ancient_market", "title": "古城夜市", "file": "ancient_market.png", "source": "pil"},
    {"id": "mechanical_garden", "title": "机械花园", "file": "mechanical_garden.png", "source": "pil"},
    {"id": "candy_cosmos", "title": "糖果宇宙", "file": "candy_cosmos.png", "source": "pil"},
    {"id": "quiet_study", "title": "书房时光", "file": "quiet_study.png", "source": "pil"},
]
PIL_THEME_IDS = [item["id"] for item in THEMES if item["source"] == "pil"]
DEFAULT_SETTINGS = {"difficulty": 3, "image_id": "star_lighthouse", "sound": True, "volume": 0.65}

COLORS = {
    "bg": (20, 24, 32),
    "bg2": (31, 38, 46),
    "panel": (38, 45, 56),
    "panel_alt": (47, 56, 67),
    "ink": (244, 238, 224),
    "muted": (178, 188, 190),
    "gold": (238, 190, 96),
    "teal": (75, 189, 180),
    "coral": (234, 111, 91),
    "jade": (102, 184, 128),
    "line": (84, 97, 108),
    "blank": (18, 20, 24),
    "ok": (111, 203, 139),
}

ACHIEVEMENT_DEFS = {
    "first_win": ("初次复原", "完成任意一局拼图"),
    "no_hint": ("独立完成", "不使用提示完成一局"),
    "hard_clear": ("大师入门", "完成 5x5 难度"),
    "swift_3": ("三阶疾行", "60 秒内完成 3x3"),
    "steady_hands": ("稳扎稳打", "步数不超过格子数的 8 倍"),
    "collector": ("图鉴收藏家", "收录 6 张主题图"),
}
