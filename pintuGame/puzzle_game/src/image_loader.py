import os

from PIL import Image, ImageDraw
import pygame

from . import config, paths


def list_available_images():
    items = []
    for theme in config.THEMES:
        path = paths.resolve_asset("images", theme["file"])
        if os.path.exists(path):
            item = dict(theme)
            item["path"] = path
            items.append(item)
    return items


def _fallback(size=1024):
    image = Image.new("RGBA", (size, size), (42, 48, 58, 255))
    draw = ImageDraw.Draw(image)
    colors = [(238, 190, 96), (75, 189, 180), (234, 111, 91), (102, 184, 128)]
    step = size // 6
    for row in range(6):
        for col in range(6):
            draw.rectangle((col * step, row * step, (col + 1) * step, (row + 1) * step), fill=colors[(row + col) % 4] + (255,))
    return image


def load_square_pil(path, pixels):
    try:
        image = Image.open(path).convert("RGBA")
    except Exception:
        image = _fallback()
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side)).resize((pixels, pixels), Image.Resampling.LANCZOS)


def pil_to_surface(image):
    image = image.convert("RGBA")
    return pygame.image.frombuffer(image.tobytes(), image.size, "RGBA").convert_alpha()


def load_reference_surface(path, pixels):
    return pil_to_surface(load_square_pil(path, pixels))


def build_tile_surfaces(path, board_size, tile_pixels):
    image = load_square_pil(path, board_size * tile_pixels)
    tiles = {}
    for row in range(board_size):
        for col in range(board_size):
            if row == board_size - 1 and col == board_size - 1:
                continue
            tile_id = row * board_size + col
            crop = image.crop((col * tile_pixels, row * tile_pixels, (col + 1) * tile_pixels, (row + 1) * tile_pixels))
            tiles[tile_id] = pil_to_surface(crop)
    return tiles
