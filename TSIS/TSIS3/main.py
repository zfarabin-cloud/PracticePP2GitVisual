"""
main.py — Entry point for Racer TSIS3.

Flow:
  Main Menu
    ├── Play  → Username → Game Loop → Game Over → (Retry | Main Menu)
    ├── Leaderboard → back
    ├── Settings    → back
    └── Quit

Run with:
    python main.py
"""

import sys
import pygame

from config   import WIDTH, HEIGHT, FPS
from persistence import load_settings, add_score, load_leaderboard
from ui       import (
    screen_username,
    screen_main_menu,
    screen_settings,
    screen_leaderboard,
    screen_game_over,
    draw_hud,
)
from racer    import GameSession


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _best_score(username: str) -> int:
    """Return the personal best score for username from the leaderboard."""
    entries = load_leaderboard()
    scores  = [e["score"] for e in entries if e.get("username") == username]
    return max(scores) if scores else 0


def run_game(surf: pygame.Surface, clock: pygame.time.Clock,
             username: str, cfg: dict) -> str:
    """
    Run one race.  Returns "retry" or "menu".
    """
    car_color  = tuple(cfg.get("car_color",  [0, 120, 255]))
    difficulty = cfg.get("difficulty", "Normal")

    prev_best = _best_score(username)
    session   = GameSession(car_color, difficulty)

    running = True
    while running:
        # ---- Events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False   # ESC → game over immediately

        keys = pygame.key.get_pressed()

        # ---- Update ----
        alive = session.tick(keys)
        if not alive:
            running = False

        # ---- Draw ----
        session.draw(surf)
        draw_hud(
            surf,
            score        = session.score,
            distance     = session.distance,
            coins        = session.coins,
            powerup      = session.current_pu,
            pu_frames    = session.pu_frames_left,
            shield_active= session.shield_active,
            speed        = session.display_speed,
        )

        pygame.display.flip()
        clock.tick(FPS)

    # ---- Save score ----
    add_score(username, session.score, session.distance, session.coins)
    is_new_best = session.score > prev_best

    # ---- Game Over screen ----
    return screen_game_over(
        surf,
        clock,
        score      = session.score,
        distance   = session.distance,
        coins      = session.coins,
        is_new_best= is_new_best,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    surf  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🏎  Racer — TSIS 3")
    clock = pygame.time.Clock()

    username: str | None = None

    while True:
        action = screen_main_menu(surf, clock)

        if action == "quit":
            pygame.quit()
            sys.exit()

        elif action == "leaderboard":
            screen_leaderboard(surf, clock)

        elif action == "settings":
            screen_settings(surf, clock)

        elif action == "play":
            # Ask for username once per session (re-use if already set)
            if username is None:
                username = screen_username(surf, clock)
                if username is None:        # window closed
                    pygame.quit()
                    sys.exit()

            # Game + retry loop
            while True:
                cfg    = load_settings()    # re-read in case settings changed
                result = run_game(surf, clock, username, cfg)

                if result == "retry":
                    continue                # same username, new race
                else:
                    username = None         # reset so next Play asks again
                    break                   # back to main menu


if __name__ == "__main__":
    main()
