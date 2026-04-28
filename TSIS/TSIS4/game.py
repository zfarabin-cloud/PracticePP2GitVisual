"""
game.py — Core Snake gameplay logic.

Covers:
  • Snake movement, growth, self-collision
  • Weighted food (3 tiers) with expiry timers
  • Poison food (shrinks snake, game-over if too short)
  • Power-ups: speed-boost, slow-motion, shield (with field + effect TTLs)
  • Obstacle walls from level 3
  • Level progression & speed scaling
  • Grid drawing
"""

import random
import pygame
from config import (
    BLOCK, COLS, ROWS, PANEL_H,
    FOOD_PER_LEVEL, FPS_BASE, FPS_MAX,
    OBSTACLE_COUNT, POISON_SHORTEN,
    POWERUP_FIELD_TTL, POWERUP_EFFECT_TTL,
    PU_SPEED, PU_SLOW, PU_SHIELD,
    C_SNAKE_DEF, C_SNAKE_EYE,
    C_FOOD_LIGHT, C_FOOD_MEDIUM, C_FOOD_HEAVY,
    C_POISON, C_OBSTACLE,
    C_PU_SPEED, C_PU_SLOW, C_PU_SHIELD,
    C_GRID, C_DARK,
    C_RED, C_GREEN, C_WHITE, C_TEXT_HI, C_TEXT_LO,
    WIDTH, HEIGHT,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rand_cell(exclude: set) -> tuple[int, int]:
    """Pick a random (col, row) cell not in `exclude`."""
    for _ in range(1000):
        c = random.randint(0, COLS - 1)
        r = random.randint(0, ROWS - 1)
        if (c, r) not in exclude:
            return c, r
    raise RuntimeError("No free cell found")


def _cell_to_px(col: int, row: int) -> tuple[int, int]:
    return col * BLOCK, PANEL_H + row * BLOCK


# ---------------------------------------------------------------------------
# Snake
# ---------------------------------------------------------------------------

class Snake:
    DIRS = {
        "UP":    ( 0, -1),
        "DOWN":  ( 0,  1),
        "LEFT":  (-1,  0),
        "RIGHT": ( 1,  0),
    }
    OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

    def __init__(self, color=C_SNAKE_DEF):
        self.color    = color
        self.shield   = False        # shield power-up flag
        self._reset()

    def _reset(self):
        mid_c = COLS // 2
        mid_r = ROWS // 2
        self.body      = [(mid_c - i, mid_r) for i in range(4)]  # head first
        self.direction = "RIGHT"
        self._queued   = "RIGHT"
        self.grow_flag = 0            # pending segments to add

    def change_dir(self, new_dir: str):
        if new_dir != self.OPPOSITE[self.direction]:
            self._queued = new_dir

    def move(self) -> tuple[int, int]:
        """Advance one tick. Returns the new head cell."""
        self.direction = self._queued
        dc, dr = self.DIRS[self.direction]
        head   = (self.body[0][0] + dc, self.body[0][1] + dr)
        self.body.insert(0, head)
        if self.grow_flag > 0:
            self.grow_flag -= 1
        else:
            self.body.pop()
        return head

    def grow(self, n: int = 1):
        self.grow_flag += n

    def shrink(self, n: int):
        """Remove segments from the tail (used by poison)."""
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()

    @property
    def head(self):
        return self.body[0]

    @property
    def occupied(self) -> set:
        return set(self.body)

    def hits_self(self) -> bool:
        return self.head in self.body[1:]

    def hits_wall(self) -> bool:
        c, r = self.head
        return not (0 <= c < COLS and 0 <= r < ROWS)

    def draw(self, surf: pygame.Surface):
        for i, (c, r) in enumerate(self.body):
            x, y = _cell_to_px(c, r)
            color = self.color
            # Slightly darker for body segments
            if i > 0:
                color = tuple(max(0, v - 40) for v in color)
            rect = pygame.Rect(x + 1, y + 1, BLOCK - 2, BLOCK - 2)
            pygame.draw.rect(surf, color, rect, border_radius=4)
        # Eyes on head
        hc, hr = self.body[0]
        hx, hy = _cell_to_px(hc, hr)
        for ox, oy in ((4, 4), (BLOCK - 6, 4)):
            pygame.draw.circle(surf, C_SNAKE_EYE, (hx + ox, hy + oy), 2)
        # Shield aura
        if self.shield:
            hx, hy = _cell_to_px(hc, hr)
            pygame.draw.rect(surf, C_PU_SHIELD,
                             pygame.Rect(hx, hy, BLOCK, BLOCK), 2, border_radius=4)


# ---------------------------------------------------------------------------
# Food
# ---------------------------------------------------------------------------

FOOD_TIERS = [
    (1, 10, C_FOOD_LIGHT,  (5, 10)),   # weight, points, colour, (min,max) lifetime s
    (2, 25, C_FOOD_MEDIUM, (4,  8)),
    (3, 50, C_FOOD_HEAVY,  (3,  6)),
]


class Food:
    def __init__(self, exclude: set):
        self.cell    = _rand_cell(exclude)
        tier         = random.choices(FOOD_TIERS, weights=[6, 3, 1])[0]
        self.weight, self.points, self.color, lt_range = tier
        self._spawn_ticks = pygame.time.get_ticks()
        self.lifetime_ms  = random.randint(*lt_range) * 1000

    @property
    def occupied(self) -> set:
        return {self.cell}

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self._spawn_ticks > self.lifetime_ms

    def draw(self, surf: pygame.Surface):
        c, r = self.cell
        x, y = _cell_to_px(c, r)
        size = BLOCK - 2 + (self.weight - 1) * 2
        offset = (BLOCK - size) // 2
        pygame.draw.rect(surf, self.color,
                         pygame.Rect(x + offset, y + offset, size, size),
                         border_radius=4)
        # Timer bar
        elapsed = pygame.time.get_ticks() - self._spawn_ticks
        ratio   = max(0.0, 1.0 - elapsed / self.lifetime_ms)
        bar_w   = int(BLOCK * ratio)
        pygame.draw.rect(surf, C_GREEN, pygame.Rect(x, y + BLOCK - 3, bar_w, 3))


class PoisonFood:
    LIFETIME_MS = 8_000

    def __init__(self, exclude: set):
        self.cell        = _rand_cell(exclude)
        self._spawn_time = pygame.time.get_ticks()

    @property
    def occupied(self) -> set:
        return {self.cell}

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self._spawn_time > self.LIFETIME_MS

    def draw(self, surf: pygame.Surface):
        c, r = self.cell
        x, y = _cell_to_px(c, r)
        cx, cy = x + BLOCK // 2, y + BLOCK // 2
        pygame.draw.circle(surf, C_POISON, (cx, cy), BLOCK // 2 - 1)
        # Skull-ish cross
        pygame.draw.line(surf, C_WHITE, (cx - 4, cy - 4), (cx + 4, cy + 4), 2)
        pygame.draw.line(surf, C_WHITE, (cx + 4, cy - 4), (cx - 4, cy + 4), 2)


# ---------------------------------------------------------------------------
# Power-up
# ---------------------------------------------------------------------------

PU_COLORS = {PU_SPEED: C_PU_SPEED, PU_SLOW: C_PU_SLOW, PU_SHIELD: C_PU_SHIELD}
PU_LABELS = {PU_SPEED: "⚡", PU_SLOW: "❄", PU_SHIELD: "🛡"}


class PowerUp:
    def __init__(self, kind: str, exclude: set):
        self.kind        = kind
        self.cell        = _rand_cell(exclude)
        self._spawn_time = pygame.time.get_ticks()

    @property
    def occupied(self) -> set:
        return {self.cell}

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self._spawn_time > POWERUP_FIELD_TTL

    def draw(self, surf: pygame.Surface):
        c, r = self.cell
        x, y = _cell_to_px(c, r)
        color = PU_COLORS[self.kind]
        pygame.draw.rect(surf, color,
                         pygame.Rect(x + 2, y + 2, BLOCK - 4, BLOCK - 4),
                         border_radius=6)
        font = pygame.font.SysFont("segoeui", 12, bold=True)
        lbl  = PU_LABELS[self.kind]
        txt  = font.render(lbl, True, C_WHITE)
        surf.blit(txt, txt.get_rect(center=(x + BLOCK // 2, y + BLOCK // 2)))


# ---------------------------------------------------------------------------
# GameSession — ties everything together
# ---------------------------------------------------------------------------

class GameSession:
    def __init__(self, snake_color=C_SNAKE_DEF, personal_best: int = 0):
        self.snake        = Snake(color=snake_color)
        self.score        = 0
        self.level        = 1
        self.food_count   = 0          # foods eaten this level
        self.personal_best = personal_best
        self.speed        = FPS_BASE

        self.obstacles: set[tuple[int, int]] = set()

        # Spawn initial food
        self.food    = Food(self._all_occupied())
        self.poison  = None           # PoisonFood | None
        self.powerup = None           # PowerUp | None

        # Active effect tracking
        self._effect_kind    = None   # PU_SPEED / PU_SLOW / PU_SHIELD
        self._effect_end_ms  = 0
        self._base_speed     = self.speed

        # Timers for spawning
        self._poison_timer   = pygame.time.get_ticks() + 10_000
        self._pu_timer       = pygame.time.get_ticks() + 15_000

        self.game_over       = False
        self.reason          = ""     # death reason string

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _all_occupied(self) -> set:
        occ = self.snake.occupied | self.obstacles
        if hasattr(self, "food")   and self.food:   occ |= self.food.occupied
        if hasattr(self, "poison") and self.poison:  occ |= self.poison.occupied
        if hasattr(self, "powerup") and self.powerup: occ |= self.powerup.occupied
        return occ

    def _place_obstacles(self):
        """Add obstacle blocks for the current level (cumulative)."""
        count = OBSTACLE_COUNT * (self.level - 2)   # level-3 → 1×, level-4 → 2×...
        for _ in range(count):
            c = _rand_cell(self._all_occupied() | self.obstacles)
            self.obstacles.add(c)

    # -----------------------------------------------------------------------
    # Tick — call once per game step
    # -----------------------------------------------------------------------

    def tick(self) -> bool:
        """
        Advance the game one step.
        Returns False when the game is over.
        """
        if self.game_over:
            return False

        now = pygame.time.get_ticks()

        # --- Effect expiry ---
        if self._effect_kind and now >= self._effect_end_ms:
            self._clear_effect()

        # --- Move snake ---
        self.snake.move()
        head = self.snake.head

        # --- Collision: wall ---
        if self.snake.hits_wall():
            if self.snake.shield:
                self._consume_shield()
                # Bounce back to a safe cell
                self.snake.body[0] = self.snake.body[1]
            else:
                self._die("Hit the wall!")
                return False

        # --- Collision: self ---
        if self.snake.hits_self():
            if self.snake.shield:
                self._consume_shield()
            else:
                self._die("Hit yourself!")
                return False

        # --- Collision: obstacle ---
        if head in self.obstacles:
            if self.snake.shield:
                self._consume_shield()
                self.snake.body[0] = self.snake.body[1]
            else:
                self._die("Hit a wall block!")
                return False

        # --- Eat normal food ---
        if head == self.food.cell:
            self.score      += self.food.points
            self.food_count += 1
            self.snake.grow(self.food.weight)
            self.food = Food(self._all_occupied())
            self._check_level_up()

        elif self.food.is_expired():
            self.food = Food(self._all_occupied())

        # --- Eat poison ---
        if self.poison and head == self.poison.cell:
            self.snake.shrink(POISON_SHORTEN)
            self.poison = None
            if len(self.snake.body) <= 1:
                self._die("Poisoned to death!")
                return False

        elif self.poison and self.poison.is_expired():
            self.poison = None

        # --- Eat power-up ---
        if self.powerup and head == self.powerup.cell:
            self._apply_effect(self.powerup.kind)
            self.powerup = None

        elif self.powerup and self.powerup.is_expired():
            self.powerup = None

        # --- Spawn poison periodically ---
        if not self.poison and now >= self._poison_timer:
            self.poison = PoisonFood(self._all_occupied())
            self._poison_timer = now + random.randint(12_000, 20_000)

        # --- Spawn power-up periodically ---
        if not self.powerup and now >= self._pu_timer:
            kind = random.choice([PU_SPEED, PU_SLOW, PU_SHIELD])
            self.powerup = PowerUp(kind, self._all_occupied())
            self._pu_timer = now + random.randint(18_000, 30_000)

        return True

    # -----------------------------------------------------------------------
    # Level up
    # -----------------------------------------------------------------------

    def _check_level_up(self):
        if self.food_count >= FOOD_PER_LEVEL:
            self.food_count  = 0
            self.level      += 1
            self._base_speed = min(FPS_MAX, FPS_BASE + (self.level - 1) * 2)
            if self._effect_kind != PU_SLOW:
                self.speed = self._base_speed
            if self.level >= 3:
                self._place_obstacles()

    # -----------------------------------------------------------------------
    # Effects
    # -----------------------------------------------------------------------

    def _apply_effect(self, kind: str):
        now = pygame.time.get_ticks()
        self._clear_effect()
        self._effect_kind   = kind
        self._effect_end_ms = now + POWERUP_EFFECT_TTL
        if kind == PU_SPEED:
            self.speed = min(FPS_MAX, self._base_speed + 6)
        elif kind == PU_SLOW:
            self.speed = max(4, self._base_speed - 5)
        elif kind == PU_SHIELD:
            self.snake.shield = True

    def _clear_effect(self):
        if self._effect_kind == PU_SHIELD:
            self.snake.shield = False
        self.speed        = self._base_speed
        self._effect_kind = None

    def _consume_shield(self):
        self.snake.shield   = False
        self._effect_kind   = None

    # -----------------------------------------------------------------------
    # Death
    # -----------------------------------------------------------------------

    def _die(self, reason: str = ""):
        self.game_over = True
        self.reason    = reason

    # -----------------------------------------------------------------------
    # Draw
    # -----------------------------------------------------------------------

    def draw(self, surf: pygame.Surface, show_grid: bool = True):
        surf.fill(C_DARK)
        # Grid
        if show_grid:
            for col in range(COLS):
                for row in range(ROWS):
                    x, y = _cell_to_px(col, row)
                    pygame.draw.rect(surf, C_GRID,
                                     pygame.Rect(x, y, BLOCK, BLOCK), 1)
        # Obstacles
        for c, r in self.obstacles:
            x, y = _cell_to_px(c, r)
            pygame.draw.rect(surf, C_OBSTACLE,
                             pygame.Rect(x + 1, y + 1, BLOCK - 2, BLOCK - 2),
                             border_radius=3)

        # Items
        self.food.draw(surf)
        if self.poison:  self.poison.draw(surf)
        if self.powerup: self.powerup.draw(surf)

        # Snake
        self.snake.draw(surf)

    def draw_hud(self, surf: pygame.Surface, username: str):
        """Draw the top HUD panel."""
        from config import PANEL_H, WIDTH
        pygame.draw.rect(surf, (30, 30, 45), pygame.Rect(0, 0, WIDTH, PANEL_H))
        font = pygame.font.SysFont("segoeui", 18, bold=True)
        font_sm = pygame.font.SysFont("segoeui", 14)

        items = [
            f"👤 {username}",
            f"⭐ Score: {self.score}",
            f"🏆 Best: {self.personal_best}",
            f"📈 Level: {self.level}",
        ]
        x = 10
        for item in items:
            txt = font.render(item, True, C_TEXT_HI)
            surf.blit(txt, (x, 14))
            x += txt.get_width() + 30

        # Active effect badge
        if self._effect_kind:
            remain = max(0, self._effect_end_ms - pygame.time.get_ticks())
            badge_colors = {PU_SPEED: C_PU_SPEED, PU_SLOW: C_PU_SLOW, PU_SHIELD: C_PU_SHIELD}
            label = {PU_SPEED: f"⚡ Speed {remain//1000+1}s",
                     PU_SLOW:  f"❄ Slow {remain//1000+1}s",
                     PU_SHIELD:f"🛡 Shield"}[self._effect_kind]
            etxt = font_sm.render(label, True, badge_colors[self._effect_kind])
            surf.blit(etxt, (WIDTH - etxt.get_width() - 10, 16))

        pygame.draw.line(surf, (60, 60, 90), (0, PANEL_H - 1), (WIDTH, PANEL_H - 1), 2)
