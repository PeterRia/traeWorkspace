from datetime import datetime
import math
import os
import time

import pygame

from . import achievements, asset_generator, config, image_loader, paths, score_card
from .audio import AudioManager
from .board import Board
from .effects import ParticleBurst
from .save_manager import SaveManager
from .ui import Button, draw_panel, draw_text, get_font


class Game:
    def __init__(self):
        asset_generator.ensure_assets()
        pygame.init()
        pygame.display.set_caption(config.TITLE)
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fonts = {
            "tiny": get_font(18),
            "small": get_font(22),
            "body": get_font(26),
            "button": get_font(24, True),
            "h2": get_font(34, True),
            "title": get_font(64, True),
        }
        self.save_manager = SaveManager()
        settings = self.save_manager.data["settings"]
        self.audio = AudioManager(settings.get("sound", True), settings.get("volume", 0.65))
        self.images = image_loader.list_available_images()
        if not self.images:
            asset_generator.ensure_assets(force=True)
            self.images = image_loader.list_available_images()
        self.state = "menu"
        self.buttons = []
        self.cards = []
        self.selected_image_id = settings.get("image_id") or self.images[0]["id"]
        self.difficulty = int(settings.get("difficulty", 3))
        self.mode = config.MODE_STANDARD
        self.board = None
        self.tile_size = config.BOARD_PIXELS // self.difficulty
        self.board_rect = pygame.Rect(config.BOARD_LEFT, config.BOARD_TOP, config.BOARD_PIXELS, config.BOARD_PIXELS)
        self.tile_surfaces = {}
        self.reference_surface = None
        self.steps = 0
        self.hints = 0
        self.start_time = 0.0
        self.paused_total = 0.0
        self.pause_started = 0.0
        self.history = []
        self.redo_stack = []
        self.highlight_movable = False
        self.hint_until = 0.0
        self.hint_cells = []
        self.hint_text = ""
        self.victory_result = None
        self.new_achievements = []
        self.effects = ParticleBurst()
        self.menu_art = self._load_menu_art()

    def _load_menu_art(self):
        cover = paths.resolve_asset("images", "imagegen_cover.png")
        if os.path.exists(cover):
            try:
                return image_loader.load_reference_surface(cover, 780)
            except Exception:
                return None
        return None

    def run(self, max_frames=None):
        frames = 0
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()
            pygame.display.flip()
            frames += 1
            if max_frames is not None and frames >= max_frames:
                self.running = False
        pygame.quit()

    def current_image(self):
        for item in self.images:
            if item["id"] == self.selected_image_id:
                return item
        return self.images[0]

    def current_elapsed(self):
        if self.start_time <= 0:
            return 0
        now = self.pause_started if self.state == "paused" else time.monotonic()
        return max(0, int(now - self.start_time - self.paused_total))

    def start_game(self, image_id=None, difficulty=None):
        if image_id:
            self.selected_image_id = image_id
        if difficulty:
            self.difficulty = difficulty
        self.save_manager.update_settings(image_id=self.selected_image_id, difficulty=self.difficulty)
        image = self.current_image()
        self.tile_size = config.BOARD_PIXELS // self.difficulty
        pixels = self.tile_size * self.difficulty
        self.board_rect = pygame.Rect(config.BOARD_LEFT, config.BOARD_TOP, pixels, pixels)
        self.tile_surfaces = image_loader.build_tile_surfaces(image["path"], self.difficulty, self.tile_size)
        self.reference_surface = image_loader.load_reference_surface(image["path"], 276)
        self.board = Board(self.difficulty)
        self.board.shuffle(config.SHUFFLE_MOVES[self.difficulty])
        self.steps = 0
        self.hints = 0
        self.history = []
        self.redo_stack = []
        self.hint_cells = []
        self.hint_text = ""
        self.victory_result = None
        self.new_achievements = []
        self.start_time = time.monotonic()
        self.paused_total = 0.0
        self.pause_started = 0.0
        self.state = "playing"
        self.audio.play("click")

    def pause(self):
        if self.state == "playing":
            self.pause_started = time.monotonic()
            self.state = "paused"
            self.audio.play("click")

    def resume(self):
        if self.state == "paused":
            self.paused_total += time.monotonic() - self.pause_started
            self.pause_started = 0.0
            self.state = "playing"
            self.audio.play("click")

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.handle_key(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def handle_key(self, event):
        ctrl = bool(event.mod & pygame.KMOD_CTRL)
        if event.key == pygame.K_ESCAPE:
            if self.state == "playing":
                self.pause()
            elif self.state == "paused":
                self.resume()
            elif self.state in ("image_select", "difficulty_select", "gallery"):
                self.state = "menu"
            return
        if self.state != "playing":
            return
        if event.key == pygame.K_p:
            self.pause()
        elif event.key == pygame.K_h:
            self.highlight_movable = not self.highlight_movable
        elif event.key == pygame.K_g:
            self.show_manhattan_hint()
        elif ctrl and event.key == pygame.K_z:
            self.undo()
        elif ctrl and event.key == pygame.K_y:
            self.redo()
        elif event.key == pygame.K_r:
            self.start_game(self.selected_image_id, self.difficulty)

    def handle_click(self, pos):
        for button in self.buttons:
            if button.hit(pos):
                self.perform_action(button.action)
                return
        if self.state == "image_select":
            for card in self.cards:
                if card["rect"].collidepoint(pos):
                    self.selected_image_id = card["id"]
                    self.state = "difficulty_select"
                    self.audio.play("click")
                    return
        if self.state == "difficulty_select":
            for card in self.cards:
                if card["rect"].collidepoint(pos):
                    self.start_game(self.selected_image_id, card["size"])
                    return
        if self.state == "playing":
            self.handle_board_click(pos)

    def perform_action(self, action):
        if action == "start":
            self.state = "image_select"
        elif action == "gallery":
            self.state = "gallery"
        elif action == "quit":
            self.running = False
        elif action == "menu":
            self.state = "menu"
        elif action == "restart":
            self.start_game(self.selected_image_id, self.difficulty)
        elif action == "pause":
            self.pause()
        elif action == "resume":
            self.resume()
        elif action == "image_select":
            self.state = "image_select"
        elif action == "difficulty_select":
            self.state = "difficulty_select"
        elif action == "hint":
            self.show_manhattan_hint()
        elif action == "undo":
            self.undo()
        elif action == "redo":
            self.redo()
        elif action == "sound":
            enabled = not self.audio.enabled
            self.audio.set_enabled(enabled)
            self.save_manager.update_settings(sound=enabled)
        self.audio.play("click")

    def handle_board_click(self, pos):
        if self.board is None or not self.board_rect.collidepoint(pos):
            return
        col = (pos[0] - self.board_rect.left) // self.tile_size
        row = (pos[1] - self.board_rect.top) // self.tile_size
        before = self.board.snapshot()
        before_steps = self.steps
        if self.board.move(row, col):
            self.history.append((before, before_steps))
            self.redo_stack.clear()
            self.steps += 1
            self.audio.play("move")
            self.hint_cells = []
            if self.board.is_solved():
                self.finish_game()
        else:
            self.audio.play("error")

    def undo(self):
        if self.state != "playing" or not self.history:
            return
        self.redo_stack.append((self.board.snapshot(), self.steps))
        snapshot, steps = self.history.pop()
        self.board.load_snapshot(snapshot)
        self.steps = steps
        self.audio.play("click")

    def redo(self):
        if self.state != "playing" or not self.redo_stack:
            return
        self.history.append((self.board.snapshot(), self.steps))
        snapshot, steps = self.redo_stack.pop()
        self.board.load_snapshot(snapshot)
        self.steps = steps
        self.audio.play("click")

    def show_manhattan_hint(self):
        if not self.board:
            return
        self.hints += 1
        base = self.board.manhattan_distance()
        best_cells, best_distance = [], None
        snapshot = self.board.snapshot()
        for row, col in self.board.legal_moves():
            self.board.move(row, col)
            distance = self.board.manhattan_distance()
            if best_distance is None or distance < best_distance:
                best_distance, best_cells = distance, [(row, col)]
            elif distance == best_distance:
                best_cells.append((row, col))
            self.board.load_snapshot(snapshot)
        self.hint_cells = best_cells
        self.hint_text = f"当前曼哈顿距离 {base}，高亮候选块可降低或保持距离"
        self.hint_until = time.monotonic() + 4.0
        self.audio.play("click")

    def finish_game(self):
        elapsed = self.current_elapsed()
        image = self.current_image()
        result = {
            "image_id": image["id"],
            "image_title": image["title"],
            "difficulty": self.difficulty,
            "mode": self.mode,
            "elapsed": elapsed,
            "steps": self.steps,
            "hints": self.hints,
            "rating": self.rate_result(elapsed, self.steps, self.hints, self.difficulty),
            "finished_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        new_achievements = achievements.evaluate_result(self.save_manager.data, result)
        try:
            result["score_card"] = score_card.create_score_card(result, image["path"])
        except Exception:
            result["score_card"] = None
        self.save_manager.record_result(result)
        for achievement_id, _title, _desc in new_achievements:
            self.save_manager.unlock_achievement(achievement_id)
        self.new_achievements = new_achievements
        self.victory_result = result
        self.state = "victory"
        self.audio.play("win")
        self.effects.burst(self.board_rect.center, 120)

    def rate_result(self, elapsed, steps, hints, difficulty):
        target_steps = difficulty * difficulty * 8
        target_time = {3: 75, 4: 180, 5: 330}[difficulty]
        score = (2 if steps <= target_steps else 1 if steps <= target_steps * 1.7 else 0)
        score += 2 if elapsed <= target_time else 1 if elapsed <= target_time * 1.8 else 0
        score += 1 if hints == 0 else 0
        return "S" if score >= 5 else "A" if score >= 4 else "B" if score >= 2 else "C"

    def update(self, dt):
        self.effects.update(dt)
        if self.hint_cells and time.monotonic() > self.hint_until:
            self.hint_cells = []
            self.hint_text = ""

    def draw(self):
        self.buttons = []
        self.cards = []
        self.draw_background()
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "image_select":
            self.draw_image_select()
        elif self.state == "difficulty_select":
            self.draw_difficulty_select()
        elif self.state == "gallery":
            self.draw_gallery()
        elif self.state == "playing":
            self.draw_playing()
        elif self.state == "paused":
            self.draw_playing(dim=True)
            self.draw_pause_overlay()
        elif self.state == "victory":
            self.draw_playing(dim=True)
            self.draw_victory()
        self.effects.draw(self.screen)

    def draw_background(self):
        w, h = self.screen.get_size()
        t = pygame.time.get_ticks() / 1000.0
        self.screen.fill(config.COLORS["bg"])
        for y in range(0, h, 4):
            ratio = y / h
            pygame.draw.rect(self.screen, (int(20 + 24 * ratio), int(24 + 18 * ratio), int(32 + 28 * ratio)), (0, y, w, 4))
        points = [(x, int(620 + math.sin(x * 0.012 + t * 0.55) * 22)) for x in range(-40, w + 80, 42)]
        pygame.draw.polygon(self.screen, (75, 189, 180), points + [(w, h), (0, h)])

    def add_button(self, action, text, rect, enabled=True, active=False):
        button = Button(action, text, pygame.Rect(rect), enabled)
        button.draw(self.screen, self.fonts["button"], active)
        self.buttons.append(button)

    def draw_menu(self):
        if self.menu_art:
            self.screen.blit(pygame.transform.smoothscale(self.menu_art, (760, 760)), (450, 34))
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 20, 115))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, "幻彩滑动拼图", self.fonts["title"], config.COLORS["ink"], (86, 116))
        draw_text(self.screen, "Pillow 切图 · pygame 交互 · random 可解打乱", self.fonts["h2"], config.COLORS["gold"], (90, 196))
        draw_text(self.screen, "课程作业版", self.fonts["body"], config.COLORS["muted"], (92, 246))
        self.add_button("start", "开始游戏", (92, 336, 230, 58), active=True)
        self.add_button("gallery", "图鉴冒险", (92, 412, 230, 58))
        self.add_button("sound", "音效：开" if self.audio.enabled else "音效：关", (92, 488, 230, 58))
        self.add_button("quit", "退出", (92, 564, 230, 58))
        panel = pygame.Rect(86, 654, 410, 108)
        draw_panel(self.screen, panel, (34, 40, 49), 8, config.COLORS["line"])
        draw_text(self.screen, "最近成绩", self.fonts["small"], config.COLORS["teal"], (108, 668))
        recent = self.save_manager.data.get("history", [])[:3]
        if not recent:
            draw_text(self.screen, "暂无记录", self.fonts["small"], config.COLORS["muted"], (108, 708))
        for index, item in enumerate(recent):
            text = f"{item['image_title']} {item['difficulty']}x{item['difficulty']} {score_card.format_time(item['elapsed'])} {item['rating']}"
            draw_text(self.screen, text, self.fonts["tiny"], config.COLORS["muted"], (108, 702 + index * 24))

    def draw_image_select(self):
        draw_text(self.screen, "选择图片", self.fonts["title"], config.COLORS["ink"], (64, 48))
        self.add_button("menu", "返回菜单", (1050, 58, 154, 48))
        gallery = self.save_manager.data.get("gallery", {})
        for index, image in enumerate(self.images):
            row, col = divmod(index, 4)
            rect = pygame.Rect(68 + col * 292, 154 + row * 270, 250, 230)
            draw_panel(self.screen, rect, config.COLORS["panel"], 8, config.COLORS["line"])
            self.screen.blit(image_loader.load_reference_surface(image["path"], 168), (rect.x + 41, rect.y + 18))
            draw_text(self.screen, image["title"], self.fonts["small"], config.COLORS["ink"], (rect.centerx, rect.y + 196), "center")
            unlocked = gallery.get(image["id"], {}).get("unlocked", False)
            draw_text(self.screen, "已收录" if unlocked else "待收录", self.fonts["tiny"], config.COLORS["gold"] if unlocked else config.COLORS["muted"], (rect.x + 14, rect.y + 12))
            self.cards.append({"rect": rect, "id": image["id"]})

    def draw_difficulty_select(self):
        image = self.current_image()
        draw_text(self.screen, "选择难度", self.fonts["title"], config.COLORS["ink"], (64, 48))
        draw_text(self.screen, image["title"], self.fonts["h2"], config.COLORS["teal"], (68, 128))
        self.add_button("image_select", "换图", (1030, 58, 98, 48))
        self.add_button("menu", "菜单", (1142, 58, 98, 48))
        self.screen.blit(image_loader.load_reference_surface(image["path"], 330), (776, 206))
        for index, (size, title, desc) in enumerate([(3, "悠闲", "适合热身"), (4, "进阶", "更有挑战"), (5, "大师", "耐心和空间感")]):
            rect = pygame.Rect(92 + index * 210, 264, 168, 168)
            draw_panel(self.screen, rect, config.COLORS["panel"], 8, config.COLORS["line"])
            draw_text(self.screen, f"{size}x{size}", self.fonts["h2"], config.COLORS["gold"], (rect.centerx, rect.y + 42), "center")
            draw_text(self.screen, title, self.fonts["body"], config.COLORS["ink"], (rect.centerx, rect.y + 91), "center")
            draw_text(self.screen, desc, self.fonts["tiny"], config.COLORS["muted"], (rect.centerx, rect.y + 128), "center")
            self.cards.append({"rect": rect, "size": size})

    def draw_gallery(self):
        draw_text(self.screen, "图鉴冒险", self.fonts["title"], config.COLORS["ink"], (64, 48))
        self.add_button("menu", "返回菜单", (1050, 58, 154, 48))
        gallery = self.save_manager.data.get("gallery", {})
        ach = self.save_manager.data.get("achievements", {})
        draw_text(self.screen, f"成就 {len(ach)}/{len(config.ACHIEVEMENT_DEFS)}", self.fonts["body"], config.COLORS["gold"], (70, 126))
        for index, image in enumerate(self.images):
            row, col = divmod(index, 5)
            rect = pygame.Rect(64 + col * 236, 184 + row * 248, 216, 218)
            draw_panel(self.screen, rect, config.COLORS["panel"], 8, config.COLORS["line"])
            thumb = image_loader.load_reference_surface(image["path"], 142)
            unlocked = gallery.get(image["id"], {}).get("unlocked", False)
            if not unlocked:
                shade = pygame.Surface(thumb.get_size(), pygame.SRCALPHA)
                shade.fill((10, 12, 16, 160))
                thumb.blit(shade, (0, 0))
            self.screen.blit(thumb, (rect.x + 37, rect.y + 18))
            draw_text(self.screen, image["title"] if unlocked else "未收录", self.fonts["small"], config.COLORS["ink"], (rect.centerx, rect.y + 176), "center")
            completed = gallery.get(image["id"], {}).get("completed", 0)
            draw_text(self.screen, f"完成 {completed}", self.fonts["tiny"], config.COLORS["muted"], (rect.centerx, rect.y + 200), "center")
        for index, (achievement_id, (title, _desc)) in enumerate(config.ACHIEVEMENT_DEFS.items()):
            color = config.COLORS["ok"] if achievement_id in ach else config.COLORS["muted"]
            draw_text(self.screen, title if achievement_id in ach else "未解锁", self.fonts["tiny"], color, (64 + index * 178, 680))

    def draw_playing(self, dim=False):
        image = self.current_image()
        draw_text(self.screen, image["title"], self.fonts["h2"], config.COLORS["ink"], (56, 34))
        if not dim:
            self.add_button("restart", "重开", (516, 38, 90, 44))
            self.add_button("pause", "暂停", (616, 38, 90, 44))
            self.add_button("image_select", "换图", (716, 38, 90, 44))
            self.add_button("difficulty_select", "难度", (816, 38, 90, 44))
            self.add_button("hint", "提示", (916, 38, 90, 44))
            self.add_button("undo", "撤销", (1016, 38, 90, 44), enabled=bool(self.history))
            self.add_button("redo", "重做", (1116, 38, 90, 44), enabled=bool(self.redo_stack))
        self.draw_board()
        self.draw_side_panel()
        if self.hint_text:
            draw_text(self.screen, self.hint_text, self.fonts["small"], config.COLORS["gold"], (58, 784))
        if dim:
            shade = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            shade.fill((10, 12, 18, 150))
            self.screen.blit(shade, (0, 0))

    def draw_board(self):
        draw_panel(self.screen, self.board_rect.inflate(18, 18), (14, 17, 23), 8, config.COLORS["line"])
        if not self.board:
            return
        movable = set(self.board.legal_moves()) if self.highlight_movable else set()
        hint_cells = set(self.hint_cells)
        for row in range(self.board.size):
            for col in range(self.board.size):
                rect = pygame.Rect(self.board_rect.left + col * self.tile_size, self.board_rect.top + row * self.tile_size, self.tile_size, self.tile_size)
                tile = self.board.grid[row][col]
                if tile is None:
                    pygame.draw.rect(self.screen, config.COLORS["blank"], rect, border_radius=6)
                    pygame.draw.rect(self.screen, (65, 70, 77), rect.inflate(-12, -12), width=2, border_radius=6)
                    continue
                self.screen.blit(self.tile_surfaces[tile.tile_id], rect.topleft)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, width=2)
                if (row, col) in movable or (row, col) in hint_cells:
                    overlay = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
                    overlay.fill((255, 218, 112, 72))
                    self.screen.blit(overlay, rect.topleft)
                    pygame.draw.rect(self.screen, config.COLORS["gold"], rect.inflate(-4, -4), width=4, border_radius=6)

    def draw_side_panel(self):
        x = 744
        panel = pygame.Rect(x, 136, 468, 628)
        draw_panel(self.screen, panel, (34, 41, 51), 8, config.COLORS["line"])
        draw_text(self.screen, "原图参考", self.fonts["body"], config.COLORS["teal"], (x + 28, 160))
        if self.reference_surface:
            self.screen.blit(self.reference_surface, (x + 28, 202))
        stats = [
            ("用时", score_card.format_time(self.current_elapsed())),
            ("步数", self.steps),
            ("难度", config.DIFFICULTIES[self.difficulty]),
            ("提示次数", self.hints),
            ("模式", config.MODE_LABELS[self.mode]),
        ]
        y = 512
        for label, value in stats:
            draw_text(self.screen, label, self.fonts["small"], config.COLORS["muted"], (x + 32, y))
            draw_text(self.screen, value, self.fonts["body"], config.COLORS["ink"], (x + 164, y - 4))
            y += 44
        key = self.save_manager.ranking_key(self.selected_image_id, str(self.difficulty), self.mode)
        rank = self.save_manager.data.get("rankings", {}).get(key)
        if rank:
            best = score_card.format_time(rank["best_time"]) if rank.get("best_time") is not None else "--"
            draw_text(self.screen, f"最佳 {best} / 最少 {rank.get('min_steps', '--')} 步", self.fonts["small"], config.COLORS["gold"], (x + 32, 716))

    def draw_pause_overlay(self):
        rect = pygame.Rect(416, 242, 448, 300)
        draw_panel(self.screen, rect, (36, 43, 52), 8, config.COLORS["line"])
        draw_text(self.screen, "已暂停", self.fonts["title"], config.COLORS["ink"], (rect.centerx, rect.y + 48), "center")
        self.add_button("resume", "继续", (rect.x + 74, rect.y + 150, 130, 54), active=True)
        self.add_button("restart", "重开", (rect.x + 242, rect.y + 150, 130, 54))
        self.add_button("menu", "返回菜单", (rect.x + 144, rect.y + 224, 160, 50))

    def draw_victory(self):
        result = self.victory_result or {}
        rect = pygame.Rect(332, 116, 616, 590)
        draw_panel(self.screen, rect, (35, 42, 52), 8, config.COLORS["line"])
        draw_text(self.screen, "复原成功", self.fonts["title"], config.COLORS["gold"], (rect.centerx, rect.y + 44), "center")
        rows = [
            ("图片", result.get("image_title", "")),
            ("难度", f"{result.get('difficulty', '')}x{result.get('difficulty', '')}"),
            ("用时", score_card.format_time(result.get("elapsed", 0))),
            ("步数", result.get("steps", 0)),
            ("提示次数", result.get("hints", 0)),
            ("评级", result.get("rating", "")),
        ]
        y = rect.y + 136
        for label, value in rows:
            draw_text(self.screen, label, self.fonts["small"], config.COLORS["muted"], (rect.x + 92, y))
            draw_text(self.screen, value, self.fonts["body"], config.COLORS["ink"], (rect.x + 232, y - 4))
            y += 44
        if self.new_achievements:
            names = "、".join(item[1] for item in self.new_achievements)
            draw_text(self.screen, f"新成就：{names}", self.fonts["small"], config.COLORS["ok"], (rect.centerx, rect.y + 426), "center")
        elif result.get("score_card"):
            draw_text(self.screen, "成绩卡已保存", self.fonts["small"], config.COLORS["ok"], (rect.centerx, rect.y + 426), "center")
        self.add_button("restart", "再来一局", (rect.x + 80, rect.y + 486, 132, 52), active=True)
        self.add_button("image_select", "换图", (rect.x + 244, rect.y + 486, 112, 52))
        self.add_button("menu", "返回菜单", (rect.x + 388, rect.y + 486, 140, 52))
