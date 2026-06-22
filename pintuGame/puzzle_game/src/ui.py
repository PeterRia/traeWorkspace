from dataclasses import dataclass

import pygame

from . import config


def get_font(size, bold=False):
    for name in ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS", "Arial"]:
        path = pygame.font.match_font(name, bold=bold)
        if path:
            try:
                return pygame.font.Font(path, size)
            except Exception:
                pass
    return pygame.font.Font(None, size)


def draw_text(surface, text, font, color, pos, anchor="topleft"):
    rendered = font.render(str(text), True, color)
    rect = rendered.get_rect()
    setattr(rect, anchor, pos)
    surface.blit(rendered, rect)
    return rect


def draw_panel(surface, rect, color=None, radius=8, border=None):
    pygame.draw.rect(surface, color or config.COLORS["panel"], rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width=1, border_radius=radius)


@dataclass
class Button:
    action: str
    text: str
    rect: pygame.Rect
    enabled: bool = True

    def hit(self, pos):
        return self.enabled and self.rect.collidepoint(pos)

    def draw(self, surface, font, active=False):
        if not self.enabled:
            fill, text_color = (58, 62, 68), (135, 140, 146)
        elif active:
            fill, text_color = config.COLORS["gold"], (25, 25, 26)
        else:
            fill, text_color = config.COLORS["panel_alt"], config.COLORS["ink"]
        pygame.draw.rect(surface, fill, self.rect, border_radius=8)
        pygame.draw.rect(surface, config.COLORS["line"], self.rect, width=1, border_radius=8)
        draw_text(surface, self.text, font, text_color, self.rect.center, "center")
