from datetime import datetime
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import paths


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


def format_time(seconds):
    seconds = int(seconds)
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def create_score_card(result, image_path, output_path=None):
    paths.ensure_runtime_dirs()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_path or os.path.join(paths.screenshots_dir(), f"score_{stamp}.png")
    card = Image.new("RGBA", (980, 560), (25, 29, 38, 255))
    draw = ImageDraw.Draw(card)
    for y in range(card.height):
        t = y / card.height
        draw.line((0, y, card.width, y), fill=(int(26 + 38 * t), int(31 + 28 * t), int(42 + 20 * t), 255))
    try:
        art = Image.open(image_path).convert("RGBA")
        side = min(art.size)
        left, top = (art.width - side) // 2, (art.height - side) // 2
        art = art.crop((left, top, left + side, top + side)).resize((360, 360), Image.Resampling.LANCZOS)
    except Exception:
        art = Image.new("RGBA", (360, 360), (75, 189, 180, 255))
    shadow = Image.new("RGBA", (390, 390), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((15, 15, 375, 375), radius=26, fill=(0, 0, 0, 120))
    card.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)), (50, 94))
    mask = Image.new("L", art.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, art.width, art.height), radius=24, fill=255)
    card.paste(art, (64, 96), mask)

    draw.text((470, 72), "通关成绩卡", font=_font(50, True), fill=(255, 243, 219, 255))
    draw.text((472, 138), result["image_title"], font=_font(30, True), fill=(116, 213, 203, 255))
    rows = [
        ("难度", f"{result['difficulty']}x{result['difficulty']}"),
        ("用时", format_time(result["elapsed"])),
        ("步数", str(result["steps"])),
        ("提示次数", str(result["hints"])),
        ("评级", result["rating"]),
    ]
    y = 204
    for label, value in rows:
        draw.text((474, y), label, font=_font(24), fill=(184, 194, 197, 255))
        draw.text((620, y - 7), value, font=_font(36, True), fill=(255, 230, 153, 255))
        y += 58
    draw.text((64, 500), datetime.now().strftime("生成时间 %Y-%m-%d %H:%M:%S"), font=_font(20), fill=(190, 196, 190, 180))
    draw.text((470, 500), "Pillow + pygame 滑动拼图课程作业", font=_font(20), fill=(190, 196, 190, 180))
    card.save(output_path)
    return output_path
