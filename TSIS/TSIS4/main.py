"""
main.py — Entry point & screen manager for Snake TSIS4.

Screens:
  • Main Menu  — username input, Play / Leaderboard / Settings / Quit
  • Game       — actual gameplay
  • Game Over  — score recap, Retry / Main Menu
  • Leaderboard— Top-10 table from PostgreSQL
  • Settings   — snake color, grid toggle, (sound toggle)
"""

import sys
import json
import random
import pygame

from config import (
    WIDTH, HEIGHT, PANEL_H, BLOCK,
    C_BLACK, C_WHITE, C_DARK, C_PANEL, C_GRID,
    C_BTN, C_BTN_HI, C_TEXT_HI, C_TEXT_LO, C_RED, C_GREEN,
    C_PU_SPEED, C_PU_SLOW, C_PU_SHIELD, C_SNAKE_DEF,
)
import db
from game import GameSession

# ---------------------------------------------------------------------------
# Settings I/O
# ---------------------------------------------------------------------------
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": list(C_SNAKE_DEF),
    "grid":  True,
    "sound": False,
}


def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE) as f:
            data = json.load(f)
        # Fill any missing keys
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(cfg: dict):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(cfg, f, indent=4)
    except Exception as e:
        print(f"[Settings] Could not save: {e}")


# ---------------------------------------------------------------------------
# Generic UI helpers
# ---------------------------------------------------------------------------

def make_font(size: int, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("segoeui", size, bold=bold)


class Button:
    def __init__(self, text: str, rect: pygame.Rect,
                 color=C_BTN, hover=C_BTN_HI, text_color=C_WHITE,
                 font_size: int = 22):
        self.text       = text
        self.rect       = rect
        self.color      = color
        self.hover      = hover
        self.text_color = text_color
        self._font      = make_font(font_size, bold=True)

    def draw(self, surf: pygame.Surface):
        mp    = pygame.mouse.get_pos()
        color = self.hover if self.rect.collidepoint(mp) else self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        pygame.draw.rect(surf, C_TEXT_LO, self.rect, 1, border_radius=8)
        txt = self._font.render(self.text, True, self.text_color)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


def draw_bg(surf: pygame.Surface):
    surf.fill(C_DARK)


def draw_title(surf: pygame.Surface, text: str,
               y: int = 60, size: int = 52):
    font = make_font(size, bold=True)
    txt  = font.render(text, True, C_TEXT_HI)
    surf.blit(txt, txt.get_rect(centerx=WIDTH // 2, y=y))


def draw_subtitle(surf: pygame.Surface, text: str, y: int, color=C_TEXT_LO):
    font = make_font(18)
    txt  = font.render(text, True, color)
    surf.blit(txt, txt.get_rect(centerx=WIDTH // 2, y=y))


# ---------------------------------------------------------------------------
# Screen: Main Menu
# ---------------------------------------------------------------------------

def screen_main_menu(surf: pygame.Surface, clock: pygame.time.Clock) -> dict | None:
    """
    Returns {"username": str, "action": "play"} or
            {"action": "leaderboard" | "settings" | "quit"}
    or None if the window was closed.
    """
    settings = load_settings()

    username  = ""
    input_active = True

    btn_w, btn_h = 220, 46
    cx = WIDTH // 2
    btn_play   = Button("▶  Play",        pygame.Rect(cx - btn_w // 2, 300, btn_w, btn_h))
    btn_board  = Button("🏆  Leaderboard", pygame.Rect(cx - btn_w // 2, 360, btn_w, btn_h))
    btn_cfg    = Button("⚙  Settings",    pygame.Rect(cx - btn_w // 2, 420, btn_w, btn_h))
    btn_quit   = Button("✕  Quit",        pygame.Rect(cx - btn_w // 2, 480, btn_w, btn_h),
                        color=(100, 40, 40), hover=(150, 60, 60))
    buttons    = [btn_play, btn_board, btn_cfg, btn_quit]

    font_input = make_font(24)
    font_hint  = make_font(15)
    input_rect = pygame.Rect(cx - 150, 230, 300, 44)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username.strip():
                        pass   # Enter triggers Play below
                else:
                    ch = event.unicode
                    if ch.isprintable() and len(username) < 20:
                        username += ch

            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_rect.collidepoint(event.pos)

            if btn_play.clicked(event):
                if username.strip():
                    return {"action": "play", "username": username.strip(),
                            "settings": load_settings()}
            if btn_board.clicked(event):
                return {"action": "leaderboard"}
            if btn_cfg.clicked(event):
                return {"action": "settings"}
            if btn_quit.clicked(event):
                return {"action": "quit"}

        draw_bg(surf)
        draw_title(surf, "🐍  SNAKE", y=100)
        draw_subtitle(surf, "Enter your username", y=200)

        # Username input box
        border_color = C_TEXT_HI if input_active else C_TEXT_LO
        pygame.draw.rect(surf, (40, 40, 60), input_rect, border_radius=6)
        pygame.draw.rect(surf, border_color, input_rect, 2, border_radius=6)
        display = username + ("|" if input_active else "")
        txt = font_input.render(display or "username…", True,
                                C_WHITE if username else C_TEXT_LO)
        surf.blit(txt, txt.get_rect(midleft=(input_rect.x + 10, input_rect.centery)))

        for b in buttons:
            b.draw(surf)

        hint = font_hint.render("Tip: use arrow keys to control the snake", True, C_TEXT_LO)
        surf.blit(hint, hint.get_rect(centerx=cx, y=HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Screen: Gameplay
# ---------------------------------------------------------------------------

def screen_game(surf: pygame.Surface, clock: pygame.time.Clock,
                username: str, settings: dict) -> dict:
    """
    Returns {"action": "retry"| "menu", "score": int, "level": int}
    """
    snake_color = tuple(settings.get("snake_color", list(C_SNAKE_DEF)))
    show_grid   = settings.get("grid", True)

    # DB: get/create player and personal best
    player_id = db.get_or_create_player(username)
    personal_best = db.get_personal_best(player_id) if player_id else 0

    session = GameSession(snake_color=snake_color, personal_best=personal_best)

    direction_queue = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.save_session(player_id, session.score, session.level)
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                key_dir = {
                    pygame.K_UP:    "UP",
                    pygame.K_w:     "UP",
                    pygame.K_DOWN:  "DOWN",
                    pygame.K_s:     "DOWN",
                    pygame.K_LEFT:  "LEFT",
                    pygame.K_a:     "LEFT",
                    pygame.K_RIGHT: "RIGHT",
                    pygame.K_d:     "RIGHT",
                }
                if event.key in key_dir:
                    direction_queue.append(key_dir[event.key])
                if event.key == pygame.K_ESCAPE:
                    db.save_session(player_id, session.score, session.level)
                    return {"action": "menu",
                            "score": session.score, "level": session.level}

        # Apply buffered direction
        if direction_queue:
            session.snake.change_dir(direction_queue.pop(0))

        alive = session.tick()

        # Draw
        session.draw(surf, show_grid=show_grid)
        session.draw_hud(surf, username)
        pygame.display.flip()
        clock.tick(session.speed)

        if not alive:
            # Save to DB
            db.save_session(player_id, session.score, session.level)
            return {"action": "game_over",
                    "score": session.score, "level": session.level,
                    "personal_best": personal_best,
                    "reason": session.reason}


# ---------------------------------------------------------------------------
# Screen: Game Over
# ---------------------------------------------------------------------------

def screen_game_over(surf: pygame.Surface, clock: pygame.time.Clock,
                     score: int, level: int,
                     personal_best: int, reason: str) -> str:
    """Returns 'retry' or 'menu'."""
    cx = WIDTH // 2
    btn_retry = Button("↺  Retry",     pygame.Rect(cx - 240, 420, 200, 50))
    btn_menu  = Button("⌂  Main Menu", pygame.Rect(cx + 40,  420, 200, 50))

    font_big = make_font(48, bold=True)
    font_med = make_font(26)
    font_sm  = make_font(18)

    is_new_best = score > personal_best

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_retry.clicked(event): return "retry"
            if btn_menu.clicked(event):  return "menu"

        draw_bg(surf)

        # Title
        go_txt = font_big.render("GAME OVER", True, C_RED)
        surf.blit(go_txt, go_txt.get_rect(centerx=cx, y=120))

        # Reason
        if reason:
            r_txt = font_sm.render(reason, True, C_TEXT_LO)
            surf.blit(r_txt, r_txt.get_rect(centerx=cx, y=185))

        # Stats
        for i, line in enumerate([
            f"Score:  {score}",
            f"Level:  {level}",
            f"Personal Best:  {max(score, personal_best)}",
        ]):
            color = C_TEXT_HI if (i == 2 and is_new_best) else C_WHITE
            txt = font_med.render(line, True, color)
            surf.blit(txt, txt.get_rect(centerx=cx, y=240 + i * 52))

        if is_new_best:
            nb = font_sm.render("🎉 New Personal Best!", True, C_GREEN)
            surf.blit(nb, nb.get_rect(centerx=cx, y=398))

        btn_retry.draw(surf)
        btn_menu.draw(surf)

        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Screen: Leaderboard
# ---------------------------------------------------------------------------

def screen_leaderboard(surf: pygame.Surface, clock: pygame.time.Clock) -> None:
    cx  = WIDTH // 2
    btn = Button("← Back", pygame.Rect(cx - 70, HEIGHT - 70, 140, 44))

    rows = db.get_leaderboard(10)

    font_title = make_font(38, bold=True)
    font_hdr   = make_font(17, bold=True)
    font_row   = make_font(16)

    COL_X = [60, 200, 440, 580, 720]
    HEADERS = ["Rank", "Username", "Score", "Level", "Date"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn.clicked(event):
                return

        draw_bg(surf)
        draw_title(surf, "🏆  Leaderboard", y=40, size=38)

        # Header row
        pygame.draw.line(surf, C_TEXT_LO, (40, 105), (WIDTH - 40, 105), 1)
        for i, h in enumerate(HEADERS):
            t = font_hdr.render(h, True, C_TEXT_HI)
            surf.blit(t, (COL_X[i], 82))
        pygame.draw.line(surf, C_TEXT_LO, (40, 112), (WIDTH - 40, 112), 1)

        # Data rows
        if not rows:
            msg = font_row.render("No scores yet — be the first!", True, C_TEXT_LO)
            surf.blit(msg, msg.get_rect(centerx=cx, y=250))
        for ri, r in enumerate(rows):
            y    = 122 + ri * 36
            bg   = (35, 35, 55) if ri % 2 == 0 else (28, 28, 45)
            pygame.draw.rect(surf, bg, pygame.Rect(40, y, WIDTH - 80, 32), border_radius=4)
            date = str(r["played_at"])[:10] if r["played_at"] else "—"
            vals = [str(r["rank"]), r["username"], str(r["score"]),
                    str(r["level_reached"]), date]
            for i, v in enumerate(vals):
                color = C_TEXT_HI if ri == 0 else C_WHITE
                t = font_row.render(v, True, color)
                surf.blit(t, (COL_X[i] + 4, y + 8))

        btn.draw(surf)
        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Screen: Settings
# ---------------------------------------------------------------------------

COLOR_PRESETS = [
    ("Lime",    (80,  220,  80)),
    ("Cyan",    (0,   220, 255)),
    ("Orange",  (255, 160,   0)),
    ("Pink",    (255, 100, 180)),
    ("White",   (220, 220, 220)),
    ("Yellow",  (255, 215,   0)),
]


def screen_settings(surf: pygame.Surface, clock: pygame.time.Clock) -> None:
    cfg = load_settings()

    cx  = WIDTH // 2
    btn_save = Button("💾  Save & Back", pygame.Rect(cx - 110, HEIGHT - 80, 220, 48))

    font_lbl = make_font(22, bold=True)
    font_val = make_font(20)

    # Build color-preset button rects
    cp_rects = []
    for i, (name, _) in enumerate(COLOR_PRESETS):
        rx = 220 + i * 82
        cp_rects.append(pygame.Rect(rx, 250, 70, 34))

    # Toggle rects
    tog_grid  = pygame.Rect(cx + 60, 330, 80, 36)
    tog_sound = pygame.Rect(cx + 60, 390, 80, 36)

    def draw_toggle(surf, rect, state, label):
        color  = C_GREEN if state else C_RED
        pygame.draw.rect(surf, color, rect, border_radius=8)
        t = font_val.render("ON" if state else "OFF", True, C_WHITE)
        surf.blit(t, t.get_rect(center=rect.center))
        lbl = font_lbl.render(label, True, C_WHITE)
        surf.blit(lbl, (rect.x - 200, rect.y + 6))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if btn_save.clicked(event):
                save_settings(cfg)
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Color preset
                for i, (_, color) in enumerate(COLOR_PRESETS):
                    if cp_rects[i].collidepoint(event.pos):
                        cfg["snake_color"] = list(color)
                # Toggles
                if tog_grid.collidepoint(event.pos):
                    cfg["grid"] = not cfg["grid"]
                if tog_sound.collidepoint(event.pos):
                    cfg["sound"] = not cfg["sound"]

        draw_bg(surf)
        draw_title(surf, "⚙  Settings", y=60, size=38)

        # Snake color
        lbl = font_lbl.render("Snake Color:", True, C_WHITE)
        surf.blit(lbl, (220, 210))
        for i, (name, color) in enumerate(COLOR_PRESETS):
            r = cp_rects[i]
            pygame.draw.rect(surf, color, r, border_radius=6)
            # Highlight selected
            if list(color) == cfg["snake_color"]:
                pygame.draw.rect(surf, C_WHITE, r, 3, border_radius=6)
            n = font_val.render(name, True, C_WHITE)
            surf.blit(n, n.get_rect(centerx=r.centerx, y=r.bottom + 4))

        draw_toggle(surf, tog_grid,  cfg["grid"],  "Grid Overlay:")
        draw_toggle(surf, tog_sound, cfg["sound"], "Sound:")

        btn_save.draw(surf)
        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# App entry
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    surf  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake — TSIS4")
    clock = pygame.time.Clock()

    db.ensure_schema()

    username = ""
    settings = load_settings()
    screen   = "menu"

    # Result carry-over
    last_score = 0
    last_level = 1
    last_best  = 0
    last_reason = ""

    while True:
        if screen == "menu":
            result = screen_main_menu(surf, clock)
            if result is None:
                break
            action = result["action"]
            if action == "play":
                username = result["username"]
                settings = result["settings"]
                screen   = "game"
            elif action == "leaderboard":
                screen = "leaderboard"
            elif action == "settings":
                screen = "settings"
            elif action == "quit":
                break

        elif screen == "game":
            result = screen_game(surf, clock, username, settings)
            action = result["action"]
            last_score  = result.get("score",  0)
            last_level  = result.get("level",  1)
            last_best   = result.get("personal_best", 0)
            last_reason = result.get("reason", "")
            if action == "game_over":
                screen = "game_over"
            elif action == "menu":
                screen = "menu"

        elif screen == "game_over":
            choice = screen_game_over(surf, clock,
                                      last_score, last_level,
                                      last_best, last_reason)
            screen = "game" if choice == "retry" else "menu"

        elif screen == "leaderboard":
            screen_leaderboard(surf, clock)
            screen = "menu"

        elif screen == "settings":
            screen_settings(surf, clock)
            settings = load_settings()
            screen   = "menu"

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
