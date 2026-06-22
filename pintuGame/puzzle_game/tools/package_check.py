import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src import config, image_loader, paths

REQUIRED = [
    "main.py",
    "requirements.txt",
    "README.md",
    "用户手册.md",
    "run_game.bat",
    "build_exe.bat",
    os.path.join("src", "board.py"),
    os.path.join("src", "game.py"),
    os.path.join("tools", "generate_assets.py"),
    os.path.join("tools", "smoke_test.py"),
]


def main():
    missing = [item for item in REQUIRED if not os.path.exists(os.path.join(ROOT, item))]
    if missing:
        raise SystemExit("missing files: " + ", ".join(missing))
    with open(os.path.join(ROOT, "build_exe.bat"), "r", encoding="utf-8") as handle:
        build_text = handle.read()
    required_command = 'pyinstaller --noconfirm --windowed --name PuzzleGame --add-data "assets;assets" main.py'
    if required_command not in build_text:
        raise SystemExit("build_exe.bat does not contain required pyinstaller command")
    images = image_loader.list_available_images()
    pil_count = sum(1 for item in images if item["id"] in config.PIL_THEME_IDS)
    if pil_count < 6:
        raise SystemExit("expected at least 6 generated PIL theme images")
    if paths.save_dir().endswith("_MEIPASS"):
        raise SystemExit("save dir must not point to _MEIPASS")
    print("package check ok")


if __name__ == "__main__":
    main()
