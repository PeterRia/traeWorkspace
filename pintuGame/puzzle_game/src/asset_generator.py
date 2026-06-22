import math
import os
import random
import wave

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import config, paths

SIZE = 1024


def _font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _gradient(top, bottom):
    image = Image.new("RGBA", (SIZE, SIZE), top + (255,))
    px = image.load()
    for y in range(SIZE):
        t = y / (SIZE - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (255,)
        for x in range(SIZE):
            px[x, y] = color
    return image


def _label(draw, title, subtitle):
    draw.rounded_rectangle((54, 56, 500, 156), radius=22, fill=(14, 18, 26, 150))
    draw.text((84, 72), title, font=_font(62, True), fill=(255, 246, 220, 255))
    draw.text((86, 136), subtitle, font=_font(27), fill=(210, 222, 218, 230))


def _finish(image):
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for i in range(1, 4):
        p = SIZE * i // 4
        draw.line((p, 0, p, SIZE), fill=(255, 255, 255, 32), width=5)
        draw.line((0, p, SIZE, p), fill=(255, 255, 255, 32), width=5)
    draw.rounded_rectangle((18, 18, SIZE - 18, SIZE - 18), radius=42, outline=(255, 255, 255, 78), width=8)
    return Image.alpha_composite(image, overlay).filter(ImageFilter.UnsharpMask(radius=1.2, percent=130))


def _draw_lighthouse(draw):
    rng = random.Random(1)
    for _ in range(130):
        x, y = rng.randrange(20, 1000), rng.randrange(20, 450)
        r = rng.choice([1, 2, 3])
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 241, 185, rng.randrange(130, 235)))
    draw.polygon((0, 680, 250, 540, 510, 690, 830, 520, 1024, 700, 1024, 1024, 0, 1024), fill=(20, 50, 62, 255))
    draw.rectangle((455, 355, 555, 782), fill=(236, 226, 197, 255))
    draw.polygon((424, 310, 505, 230, 586, 310), fill=(224, 93, 77, 255))
    draw.rectangle((434, 310, 576, 365), fill=(42, 58, 68, 255))
    for y in range(430, 745, 82):
        draw.rectangle((475, y, 535, y + 34), fill=(37, 63, 76, 255))
    draw.polygon((505, 300, 995, 160, 995, 455), fill=(255, 214, 103, 68))


def _draw_peach(draw):
    for offset, color in [(0, (92, 132, 120)), (160, (72, 112, 111)), (310, (48, 88, 93))]:
        draw.polygon((0, 580 + offset, 220, 350 + offset, 430, 610 + offset, 660, 330 + offset, 1024, 650 + offset, 1024, 1024, 0, 1024), fill=color + (255,))
    draw.polygon((450, 1024, 575, 590, 670, 1024), fill=(238, 210, 158, 255))
    rng = random.Random(2)
    for _ in range(95):
        x, y = rng.randrange(40, 980), rng.randrange(130, 560)
        color = rng.choice([(251, 139, 146), (255, 183, 178), (245, 101, 129), (255, 211, 188)])
        draw.ellipse((x - 18, y - 12, x + 18, y + 12), fill=color + (205,))
    for x in range(70, 990, 130):
        draw.line((x, 640, x - 42, 860), fill=(78, 85, 61, 255), width=12)
        draw.ellipse((x - 80, 555, x + 72, 690), fill=(75, 153, 111, 240))


def _draw_market(draw):
    for i, x in enumerate(range(-40, 980, 180)):
        y = 410 + (i % 2) * 45
        draw.polygon((x, y, x + 110, y - 86, x + 255, y), fill=(185, 74, 67, 255))
        draw.rectangle((x + 35, y, x + 225, 790), fill=(58, 62, 76, 255))
        for wx in range(x + 68, x + 200, 55):
            draw.rectangle((wx, y + 70, wx + 30, y + 128), fill=(245, 177, 93, 255))
    rng = random.Random(3)
    for _ in range(72):
        x, y, r = rng.randrange(20, 1004), rng.randrange(125, 430), rng.randrange(13, 26)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(239, 89, 74, 215))
        draw.line((x, y + r, x, y + r + 38), fill=(255, 205, 126, 145), width=2)
    draw.rectangle((0, 790, 1024, 1024), fill=(33, 37, 49, 255))


def _gear(draw, cx, cy, r, color):
    for i in range(14):
        a = math.tau * i / 14
        draw.line((cx + math.cos(a) * r, cy + math.sin(a) * r, cx + math.cos(a) * (r + 32), cy + math.sin(a) * (r + 32)), fill=(55, 68, 66, 255), width=18)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (255,), outline=(55, 68, 66, 255), width=8)
    draw.ellipse((cx - r * 0.36, cy - r * 0.36, cx + r * 0.36, cy + r * 0.36), fill=(28, 40, 43, 255))


def _draw_garden(draw):
    _gear(draw, 265, 365, 118, (187, 171, 108))
    _gear(draw, 720, 300, 96, (104, 178, 153))
    _gear(draw, 610, 720, 150, (229, 150, 94))
    rng = random.Random(4)
    for x in range(60, 1000, 100):
        draw.line((x, 1024, x + 28, 640), fill=(49, 98, 73, 255), width=10)
    for _ in range(60):
        x, y = rng.randrange(90, 945), rng.randrange(540, 930)
        draw.ellipse((x - 22, y - 22, x + 22, y + 22), fill=rng.choice([(237, 115, 92), (245, 190, 91), (116, 204, 175)]) + (230,))


def _draw_cosmos(draw):
    rng = random.Random(5)
    for _ in range(130):
        x, y = rng.randrange(20, 1000), rng.randrange(20, 1000)
        draw.rectangle((x, y, x + 3, y + 3), fill=(255, 237, 190, rng.randrange(120, 230)))
    for cx, cy, r, c1, c2 in [
        (278, 340, 96, (255, 162, 124), (255, 231, 170)),
        (690, 250, 126, (108, 206, 196), (66, 113, 156)),
        (760, 720, 158, (244, 203, 91), (228, 103, 113)),
        (315, 735, 72, (176, 125, 234), (90, 209, 178)),
    ]:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c1 + (255,))
        draw.arc((cx - r * 1.5, cy - r * 0.44, cx + r * 1.5, cy + r * 0.44), 0, 360, fill=c2 + (220,), width=12)


def _draw_study(draw):
    draw.rectangle((90, 150, 934, 810), fill=(92, 66, 52, 255))
    for shelf_y in [250, 390, 530, 670]:
        draw.rectangle((110, shelf_y, 914, shelf_y + 20), fill=(50, 37, 34, 255))
        x = 130
        rng = random.Random(shelf_y)
        while x < 880:
            w, h = rng.randrange(24, 48), rng.randrange(72, 126)
            color = rng.choice([(206, 104, 88), (86, 145, 153), (224, 174, 95), (125, 167, 111), (158, 122, 183)])
            draw.rounded_rectangle((x, shelf_y - h, x + w, shelf_y), radius=5, fill=color + (255,))
            x += w + rng.randrange(7, 16)
    draw.rectangle((392, 190, 632, 438), fill=(226, 213, 163, 255))
    draw.rectangle((414, 214, 610, 415), fill=(104, 172, 184, 255))
    draw.line((512, 214, 512, 415), fill=(231, 230, 210, 255), width=8)
    draw.line((414, 315, 610, 315), fill=(231, 230, 210, 255), width=8)
    draw.ellipse((454, 672, 723, 810), fill=(246, 221, 178, 255))


THEME_DRAW = {
    "star_lighthouse": ((18, 36, 70), (18, 95, 112), _draw_lighthouse, "可解滑块"),
    "peach_path": ((128, 207, 210), (242, 182, 144), _draw_peach, "春日图鉴"),
    "ancient_market": ((25, 31, 57), (96, 57, 75), _draw_market, "灯影成谜"),
    "mechanical_garden": ((42, 62, 62), (104, 134, 98), _draw_garden, "齿轮开花"),
    "candy_cosmos": ((33, 34, 80), (95, 55, 103), _draw_cosmos, "甜味星轨"),
    "quiet_study": ((59, 71, 78), (118, 93, 74), _draw_study, "窗边午后"),
}


def _image(theme, path):
    top, bottom, drawer, subtitle = THEME_DRAW[theme["id"]]
    image = _gradient(top, bottom)
    draw = ImageDraw.Draw(image)
    drawer(draw)
    _label(draw, theme["title"], subtitle)
    _finish(image).save(path)


def _tone(path, notes, duration=0.14, sample_rate=44100, volume=0.34):
    samples = int(duration * sample_rate)
    with wave.open(path, "w") as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(sample_rate)
        frames = bytearray()
        for i in range(samples):
            t = i / sample_rate
            env = min(1.0, i / (sample_rate * 0.01)) * max(0.0, 1 - i / samples)
            value = sum(math.sin(math.tau * freq * t) for freq in notes) / len(notes)
            sample = int(max(-1.0, min(1.0, value * env * volume)) * 32767)
            frames += sample.to_bytes(2, "little", signed=True)
        sound.writeframes(bytes(frames))


def ensure_assets(force=False):
    paths.ensure_runtime_dirs()
    generated = []
    for theme in config.THEMES:
        if theme["source"] != "pil":
            continue
        write_path = paths.generated_asset_path("images", theme["file"])
        if force or not os.path.exists(paths.resolve_asset("images", theme["file"])):
            _image(theme, write_path)
            generated.append(write_path)
    for filename, notes, duration in [
        ("move.wav", [460, 690], 0.08),
        ("click.wav", [520], 0.06),
        ("error.wav", [170, 135], 0.12),
        ("win.wav", [523, 659, 784], 0.44),
    ]:
        write_path = paths.generated_asset_path("sounds", filename)
        if force or not os.path.exists(paths.resolve_asset("sounds", filename)):
            _tone(write_path, notes, duration=duration)
            generated.append(write_path)
    return generated
