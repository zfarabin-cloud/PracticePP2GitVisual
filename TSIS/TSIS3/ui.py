"""
ui.py — Reusable UI components and all non-gameplay screens.

Screens:
  screen_username  → str
  screen_main_menu → str  ("play"|"leaderboard"|"settings"|"quit")
  screen_settings  → None (saves to disk)
  screen_leaderboard → None
  screen_game_over → str  ("retry"|"menu")
"""

import pygame
import sys
from config import (
    WIDTH, HEIGHT, C_PANEL, C_WHITE, C_BLACK, C_HUD_HI, C_HUD_LO,
    C_BTN, C_BTN_HI, C_RED_BTN, C_RED_BTN_H, CAR_COLORS,
    C_ROAD, C_GRASS, C_SKY, C_PU,
    PU_NITRO, PU_SHIELD, PU_REPAIR,
)
from persistence import load_settings, save_settings, load_leaderboard

# ---------------------------------------------------------------------------
# Fonts (lazy-cached)
# ---------------------------------------------------------------------------

_font_cache: dict = {}

def _font(size: int, bold: bool = False) -> pygame.font.Font:
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont("segoeui", size, bold=bold)
    return _font_cache[key]


# ---------------------------------------------------------------------------
# Button
# ---------------------------------------------------------------------------

class Button:
    def __init__(self, text: str, rect: pygame.Rect,
                 color=None, hover=None,
                 text_color=C_WHITE, font_size: int = 22):
        self.text       = text
        self.rect       = rect
        self.color      = color or C_BTN
        self.hover      = hover or C_BTN_HI
        self.text_color = text_color
        self._fs        = font_size

    def draw(self, surf: pygame.Surface):
        mp    = pygame.mouse.get_pos()
        color = self.hover if self.rect.collidepoint(mp) else self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        pygame.draw.rect(surf, C_HUD_LO, self.rect, 1, border_radius=8)
        txt = _font(self._fs, bold=True).render(self.text, True, self.text_color)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# ---------------------------------------------------------------------------
# Background helpers
# ---------------------------------------------------------------------------

def _draw_bg(surf: pygame.Surface):
    """Simple gradient-like dark background for menu screens."""
    surf.fill((20, 22, 38))
    # faint road strip for flavour
    pygame.draw.rect(surf, (40, 42, 55), pygame.Rect(WIDTH // 2 - 90, 0, 180, HEIGHT))


def _title(surf: pygame.Surface, text: str, y: int, size: int = 52):
    t = _font(size, bold=True).render(text, True, C_HUD_HI)
    surf.blit(t, t.get_rect(centerx=WIDTH // 2, y=y))


def _subtitle(surf: pygame.Surface, text: str, y: int,
               color=C_HUD_LO, size: int = 18):
    t = _font(size).render(text, True, color)
    surf.blit(t, t.get_rect(centerx=WIDTH // 2, y=y))


# ---------------------------------------------------------------------------
# HUD (drawn during gameplay)
# ---------------------------------------------------------------------------

def draw_hud(surf: pygame.Surface, score: int, distance: int,
             coins: int, powerup: str | None, pu_frames: int,
             shield_active: bool, speed: float):
    """Top panel drawn over the game surface."""
    panel = pygame.Surface((WIDTH, 52), pygame.SRCALPHA)
    panel.fill((18, 18, 28, 210))
    surf.blit(panel, (0, 0))

    f  = _font(16, bold=True)
    fs = _font(13)

    items = [
        (f"🏁 {distance}m",  10),
        (f"⭐ {score}",       120),
        (f"🪙 ×{coins}",      220),
    ]
    for txt, x in items:
        t = f.render(txt, True, C_HUD_HI)
        surf.blit(t, (x, 4))

    # Speed bar
    bar_x, bar_y, bar_w = 315, 6, 70
    pygame.draw.rect(surf, (40, 40, 60), pygame.Rect(bar_x, bar_y, bar_w, 10), border_radius=3)
    fill = int(bar_w * min(speed / 16, 1.0))
    clr  = (0, 220, 80) if speed < 10 else (255, 180, 0) if speed < 14 else (255, 50, 50)
    pygame.draw.rect(surf, clr, pygame.Rect(bar_x, bar_y, fill, 10), border_radius=3)
    surf.blit(fs.render("spd", True, C_HUD_LO), (bar_x, bar_y + 12))

    # Active power-up badge
    if shield_active and not powerup:
        t = fs.render("🛡 Shield", True, C_PU[PU_SHIELD])
        surf.blit(t, t.get_rect(centerx=WIDTH // 2, y=34))
    elif powerup == PU_NITRO:
        secs = max(0, pu_frames // 60)
        t = fs.render(f"⚡ Nitro {secs}s", True, C_PU[PU_NITRO])
        surf.blit(t, t.get_rect(centerx=WIDTH // 2, y=34))


# ---------------------------------------------------------------------------
# Screen: Username input
# ---------------------------------------------------------------------------

def screen_username(surf: pygame.Surface, clock: pygame.time.Clock) -> str | None:
    username    = ""
    input_rect  = pygame.Rect(WIDTH // 2 - 130, 280, 260, 48)
    font_in     = _font(24)
    btn_start   = Button("Start Racing  ▶", pygame.Rect(WIDTH // 2 - 110, 360, 220, 48))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN and username.strip():
                    return username.strip()
                else:
                    ch = event.unicode
                    if ch.isprintable() and len(username) < 18:
                        username += ch
            if btn_start.clicked(event) and username.strip():
                return username.strip()

        _draw_bg(surf)
        _title(surf, "🏎  RACER", y=90)
        _subtitle(surf, "Enter your username to begin", y=165)
        _subtitle(surf, "Use ← → arrow keys to steer", y=190, size=15)

        # Input box
        border = C_HUD_HI
        pygame.draw.rect(surf, (35, 38, 60), input_rect, border_radius=7)
        pygame.draw.rect(surf, border, input_rect, 2, border_radius=7)
        disp = username + "|"
        t    = font_in.render(disp if username else "username…", True,
                              C_WHITE if username else C_HUD_LO)
        surf.blit(t, t.get_rect(midleft=(input_rect.x + 10, input_rect.centery)))

        btn_start.draw(surf)
        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Screen: Main Menu
# ---------------------------------------------------------------------------

def screen_main_menu(surf: pygame.Surface, clock: pygame.time.Clock) -> str:
    cx = WIDTH // 2
    bw, bh = 210, 46
    buttons = [
        ("play",        Button("▶  Play",         pygame.Rect(cx - bw // 2, 240, bw, bh))),
        ("leaderboard", Button("🏆  Leaderboard",  pygame.Rect(cx - bw // 2, 302, bw, bh))),
        ("settings",    Button("⚙  Settings",     pygame.Rect(cx - bw // 2, 364, bw, bh))),
        ("quit",        Button("✕  Quit",          pygame.Rect(cx - bw // 2, 426, bw, bh),
                               color=C_RED_BTN, hover=C_RED_BTN_H)),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            for action, btn in buttons:
                if btn.clicked(event):
                    return action

        _draw_bg(surf)
        _title(surf, "🏎  RACER", y=100)
        _subtitle(surf, "Dodge traffic · collect coins · grab power-ups", y=178)
        for _, btn in buttons:
            btn.draw(surf)
        _subtitle(surf, "← →  to steer", y=HEIGHT - 30, size=14)

        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Screen: Settings
# ---------------------------------------------------------------------------

def screen_settings(surf: pygame.Surface, clock: pygame.time.Clock):
    cfg = load_settings()
    cx  = WIDTH // 2

    btn_save = Button("💾  Save & Back", pygame.Rect(cx - 100, HEIGHT - 80, 200, 46))

    # Car color swatches
    color_names = list(CAR_COLORS.keys())
    swatch_w, swatch_h = 44, 32
    swatch_cols = 3
    swatch_rects = []
    for i, name in enumerate(color_names):
        col = i % swatch_cols
        row = i // swatch_cols
        r = pygame.Rect(cx - swatch_w * swatch_cols // 2 + col * (swatch_w + 6),
                        240 + row * (swatch_h + 8), swatch_w, swatch_h)
        swatch_rects.append((name, r))

    # Difficulty buttons
    diffs = ["Easy", "Normal", "Hard"]
    diff_rects = []
    for i, d in enumerate(diffs):
        diff_rects.append((d, pygame.Rect(cx - 135 + i * 92, 370, 84, 34)))

    # Sound toggle
    snd_rect = pygame.Rect(cx + 40, 438, 80, 34)

    font_lbl = _font(20, bold=True)
    font_sm  = _font(15)

    def is_color_selected(name):
        return list(CAR_COLORS[name]) == cfg.get("car_color", [0, 120, 255])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_save.clicked(event):
                save_settings(cfg)
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, r in swatch_rects:
                    if r.collidepoint(event.pos):
                        cfg["car_color"] = list(CAR_COLORS[name])
                for d, r in diff_rects:
                    if r.collidepoint(event.pos):
                        cfg["difficulty"] = d
                if snd_rect.collidepoint(event.pos):
                    cfg["sound"] = not cfg["sound"]

        _draw_bg(surf)
        _title(surf, "⚙  Settings", y=60, size=38)

        # Car color
        surf.blit(font_lbl.render("Car Color:", True, C_WHITE), (cx - 135, 208))
        for name, r in swatch_rects:
            pygame.draw.rect(surf, CAR_COLORS[name], r, border_radius=5)
            if is_color_selected(name):
                pygame.draw.rect(surf, C_WHITE, r, 3, border_radius=5)
            t = font_sm.render(name, True, C_WHITE)
            surf.blit(t, t.get_rect(centerx=r.centerx, y=r.bottom + 2))

        # Difficulty
        surf.blit(font_lbl.render("Difficulty:", True, C_WHITE), (cx - 135, 340))
        for d, r in diff_rects:
            active = cfg.get("difficulty", "Normal") == d
            clr  = (70, 110, 70) if d == "Easy" else (70, 70, 110) if d == "Normal" else (110, 50, 50)
            hclr = tuple(min(255, c + 30) for c in clr)
            mp   = pygame.mouse.get_pos()
            pygame.draw.rect(surf, hclr if r.collidepoint(mp) else clr, r, border_radius=6)
            if active:
                pygame.draw.rect(surf, C_WHITE, r, 2, border_radius=6)
            surf.blit(font_sm.render(d, True, C_WHITE), font_sm.render(d, True, C_WHITE).get_rect(center=r.center))
            # re-blit for correct centering
            tt = font_sm.render(d, True, C_WHITE)
            surf.blit(tt, tt.get_rect(center=r.center))

        # Sound toggle
        surf.blit(font_lbl.render("Sound:", True, C_WHITE), (cx - 135, 444))
        s_on = cfg.get("sound", True)
        sc   = (50, 160, 50) if s_on else (110, 40, 40)
        pygame.draw.rect(surf, sc, snd_rect, border_radius=7)
        tt = font_sm.render("ON" if s_on else "OFF", True, C_WHITE)
        surf.blit(tt, tt.get_rect(center=snd_rect.center))

        btn_save.draw(surf)
        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Screen: Leaderboard
# ---------------------------------------------------------------------------

def screen_leaderboard(surf: pygame.Surface, clock: pygame.time.Clock):
    cx   = WIDTH // 2
    btn  = Button("← Back", pygame.Rect(cx - 70, HEIGHT - 66, 140, 42))
    rows = load_leaderboard()

    COLS = [14, 60, 170, 250, 318]
    HDRS = ["#", "Name", "Score", "Dist", "Date"]
    font_h = _font(15, bold=True)
    font_r = _font(14)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn.clicked(event):
                return

        _draw_bg(surf)
        _title(surf, "🏆  Leaderboard", y=42, size=36)

        # Header
        for i, h in enumerate(HDRS):
            surf.blit(font_h.render(h, True, C_HUD_HI), (COLS[i], 96))
        pygame.draw.line(surf, C_HUD_LO, (10, 114), (WIDTH - 10, 114), 1)

        if not rows:
            t = font_r.render("No runs yet — be the first!", True, C_HUD_LO)
            surf.blit(t, t.get_rect(centerx=cx, y=230))
        else:
            for ri, r in enumerate(rows):
                y  = 122 + ri * 34
                bg = (30, 32, 52) if ri % 2 == 0 else (24, 26, 44)
                pygame.draw.rect(surf, bg, pygame.Rect(8, y, WIDTH - 16, 30), border_radius=4)
                date = str(r.get("date", ""))[:10]
                vals = [str(r.get("rank", ri + 1)), r.get("username", "?"),
                        str(r.get("score", 0)), f"{r.get('distance', 0)}m", date]
                clr  = C_HUD_HI if ri == 0 else C_WHITE
                for i, v in enumerate(vals):
                    surf.blit(font_r.render(v, True, clr), (COLS[i] + 4, y + 8))

        btn.draw(surf)
        pygame.display.flip()
        clock.tick(60)


# ---------------------------------------------------------------------------
# Screen: Game Over
# ---------------------------------------------------------------------------

def screen_game_over(surf: pygame.Surface, clock: pygame.time.Clock,
                     score: int, distance: int, coins: int,
                     is_new_best: bool) -> str:
    cx = WIDTH // 2
    btn_retry = Button("↺  Retry",     pygame.Rect(cx - 220, 430, 180, 48))
    btn_menu  = Button("⌂  Main Menu", pygame.Rect(cx + 40,  430, 180, 48))
    font_big  = _font(50, bold=True)
    font_med  = _font(24)
    font_sm   = _font(17)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_retry.clicked(event): return "retry"
            if btn_menu.clicked(event):  return "menu"

        _draw_bg(surf)
        go = font_big.render("GAME OVER", True, (220, 50, 50))
        surf.blit(go, go.get_rect(centerx=cx, y=100))

        for i, (lbl, val) in enumerate([
            ("Score",    f"{score}"),
            ("Distance", f"{distance} m"),
            ("Coins",    f"{coins}"),
        ]):
            t = font_med.render(f"{lbl}:  {val}", True, C_WHITE)
            surf.blit(t, t.get_rect(centerx=cx, y=220 + i * 56))

        if is_new_best:
            nb = font_sm.render("🎉 New Personal Best!", True, (50, 220, 100))
            surf.blit(nb, nb.get_rect(centerx=cx, y=392))

        btn_retry.draw(surf)
        btn_menu.draw(surf)
        pygame.display.flip()
        clock.tick(60)
