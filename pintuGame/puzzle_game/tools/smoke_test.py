import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src import asset_generator, image_loader, score_card
from src.board import Board


def main():
    asset_generator.ensure_assets()
    import pygame

    pygame.init()
    pygame.display.set_mode((1, 1))
    images = image_loader.list_available_images()
    assert images, "no images available"
    board = Board(3)
    board.shuffle(30, seed=123)
    assert board.is_solvable(), "shuffled board must be solvable"
    row, col = board.legal_moves()[0]
    assert board.move(row, col), "legal move failed"
    tiles = image_loader.build_tile_surfaces(images[0]["path"], 3, 64)
    assert len(tiles) == 8, "3x3 should create 8 visible tiles"
    path = score_card.create_score_card(
        {"image_title": images[0]["title"], "difficulty": 3, "elapsed": 12, "steps": 8, "hints": 0, "rating": "S"},
        images[0]["path"],
    )
    assert os.path.exists(path), "score card was not created"
    pygame.quit()
    print("smoke ok")


if __name__ == "__main__":
    main()
