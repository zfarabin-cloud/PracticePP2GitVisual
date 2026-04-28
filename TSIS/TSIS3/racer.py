"""
racer.py — Game sprites and GameSession.

All graphics drawn procedurally; no image files required.

Sprites:
  PlayerCar, TrafficCar          — vehicles
  CoinSprite                     — weighted collectible
  PowerUpSprite                  — Nitro / Shield / Repair
  OilSpill                       — slows player
  Barrier                        — crash hazard
  NitroStrip                     — road-event speed boost
  HazardRow                      — simultaneous lane hazards

GameSession:
  .tick(keys)  → bool (False = game over)
  .draw(surf)
"""

import pygame
import random
from config import (
    WIDTH, HEIGHT, FPS,
    ROAD_L, ROAD_R, ROAD_W, LANES, LANE_W,
    PLAYER_W, PLAYER_H, TRAFFIC_W, TRAFFIC_H,
    PLAYER_SPEED, SCROLL_BASE, TRAFFIC_BASE,
    COIN_SPAWN_INTERVAL, OBSTACLE_SPAWN_INTERVAL,
    PU_SPAWN_INTERVAL, PU_FIELD_FRAMES, PU_REPAIR_BONUS,
    PU_NITRO, PU_SHIELD, PU_REPAIR,
    PU_NITRO_FRAMES,
    C_ROAD, C_LANE_MRK, C_KERB_A, C_KERB_B,
    C_GRASS, C_SKY, C_BLACK, C_WHITE,
    C_OIL, C_BARRIER, C_NITRO_STR, C_PU,
    C_HUD_HI, C_HUD_LO, C_PANEL,
    DIFFICULTY, DIST_PX_PER_POINT,
)

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def _draw_car(surf: pygame.Surface, rect: pygame.Rect,
              body_color: tuple, is_player: bool = False):
    """Draw a car at the given rect with a body colour."""
    r = rect
    # Body
    pygame.draw.rect(surf, body_color, r, border_radius=7)
    # Windshield
    win_color = (150, 210, 255)
    wm = 7   # margin
    if is_player:
        pygame.draw.rect(surf, win_color,
                         pygame.Rect(r.x + wm, r.y + r.h // 4, r.w - wm * 2, r.h // 3),
                         border_radius=3)
    else:
        pygame.draw.rect(surf, win_color,
                         pygame.Rect(r.x + wm, r.y + r.h // 3, r.w - wm * 2, r.h // 4),
                         border_radius=3)
    # Wheels
    wheel_color = (25, 25, 25)
    wheel_w, wheel_h = 9, 18
    for wx, wy in [(r.x - 4, r.y + 8), (r.right - 5, r.y + 8),
                   (r.x - 4, r.bottom - 26), (r.right - 5, r.bottom - 26)]:
        pygame.draw.rect(surf, wheel_color,
                         pygame.Rect(wx, wy, wheel_w, wheel_h), border_radius=2)
    # Lights
    light_clr = (255, 255, 140) if is_player else (255, 70, 70)
    for lx in [r.x + 5, r.right - 13]:
        ly = r.y + 4 if is_player else r.bottom - 8
        pygame.draw.rect(surf, light_clr, pygame.Rect(lx, ly, 8, 4), border_radius=2)
    # Shine stripe
    shine = tuple(min(255, c + 60) for c in body_color)
    pygame.draw.rect(surf, shine,
                     pygame.Rect(r.x + r.w // 2 - 4, r.y + 4, 6, r.h - 8), border_radius=2)


def _draw_coin(surf: pygame.Surface, cx: int, cy: int,
               weight: int, alpha_ratio: float = 1.0):
    base_r = 12 + (weight - 1) * 3
    color  = [(255, 215, 0), (255, 170, 0), (255, 100, 0)][weight - 1]
    pygame.draw.circle(surf, color, (cx, cy), base_r)
    pygame.draw.circle(surf, (200, 150, 0), (cx, cy), base_r, 2)
    f = pygame.font.SysFont("segoeui", 12, bold=True)
    t = f.render(str(weight * 10), True, C_WHITE)
    surf.blit(t, t.get_rect(center=(cx, cy)))


def _draw_powerup(surf: pygame.Surface, rect: pygame.Rect, kind: str):
    color = C_PU[kind]
    pygame.draw.rect(surf, color, rect, border_radius=8)
    pygame.draw.rect(surf, C_WHITE, rect, 2, border_radius=8)
    label = {"nitro": "⚡", "shield": "🛡", "repair": "🔧"}[kind]
    f = pygame.font.SysFont("segoeui", 18, bold=True)
    t = f.render(label, True, C_WHITE)
    surf.blit(t, t.get_rect(center=rect.center))


def _draw_oil(surf: pygame.Surface, rect: pygame.Rect):
    pygame.draw.ellipse(surf, C_OIL, rect)
    pygame.draw.ellipse(surf, (60, 0, 100), rect, 2)
    # Sheen
    sheen = pygame.Rect(rect.x + rect.w // 4, rect.y + rect.h // 4,
                        rect.w // 2, rect.h // 4)
    pygame.draw.ellipse(surf, (100, 50, 160), sheen)


def _draw_barrier(surf: pygame.Surface, rect: pygame.Rect):
    pygame.draw.rect(surf, C_BARRIER, rect, border_radius=4)
    # Stripes
    stripe_w = 10
    for i in range(0, rect.w + stripe_w, stripe_w * 2):
        sr = pygame.Rect(rect.x + i, rect.y, stripe_w, rect.h)
        sr = sr.clip(rect)
        pygame.draw.rect(surf, C_WHITE, sr)
    pygame.draw.rect(surf, (80, 30, 0), rect, 2, border_radius=4)


def _draw_nitro_strip(surf: pygame.Surface, rect: pygame.Rect):
    pygame.draw.rect(surf, C_NITRO_STR, rect, border_radius=3)
    pygame.draw.rect(surf, (0, 240, 255), rect, 2, border_radius=3)
    f = pygame.font.SysFont("segoeui", 12, bold=True)
    t = f.render("NITRO", True, C_WHITE)
    surf.blit(t, t.get_rect(center=rect.center))


# ---------------------------------------------------------------------------
# Sprite classes
# ---------------------------------------------------------------------------

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self, color: tuple):
        super().__init__()
        self.color  = color
        self.image  = pygame.Surface((PLAYER_W, PLAYER_H), pygame.SRCALPHA)
        self.rect   = self.image.get_rect(
            centerx=WIDTH // 2, bottom=HEIGHT - 20)
        self.shield = False
        self.slowed = 0       # frames remaining of oil-slow
        self.nitro  = 0       # frames remaining of nitro boost
        self._refresh()

    def _refresh(self):
        self.image.fill((0, 0, 0, 0))
        _draw_car(self.image, pygame.Rect(0, 0, PLAYER_W, PLAYER_H),
                  self.color, is_player=True)
        if self.shield:
            pygame.draw.rect(self.image, (255, 215, 0),
                             pygame.Rect(0, 0, PLAYER_W, PLAYER_H), 3, border_radius=7)

    def move(self, keys):
        speed = PLAYER_SPEED
        if self.nitro  > 0: speed = int(PLAYER_SPEED * 1.9)
        if self.slowed > 0: speed = max(2, speed // 2)

        if keys[pygame.K_LEFT]  and self.rect.left  > ROAD_L + 4:
            self.rect.move_ip(-speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_R - 4:
            self.rect.move_ip(speed, 0)

        if self.nitro  > 0: self.nitro  -= 1
        if self.slowed > 0: self.slowed -= 1

    def grant_shield(self):
        self.shield = True
        self._refresh()

    def consume_shield(self):
        self.shield = False
        self._refresh()

    def grant_nitro(self):
        self.nitro = PU_NITRO_FRAMES

    def apply_oil(self):
        self.slowed = 120   # 2 s @ 60 FPS

    @property
    def effective_speed(self) -> float:
        """Return current speed for HUD display."""
        spd = float(PLAYER_SPEED)
        if self.nitro  > 0: spd *= 1.9
        if self.slowed > 0: spd = max(2, spd / 2)
        return spd

    def draw(self, surf: pygame.Surface):
        self._refresh()
        surf.blit(self.image, self.rect)


class TrafficCar(pygame.sprite.Sprite):
    COLORS = [(200, 40, 40), (240, 140, 0), (140, 40, 200),
              (40, 160, 200), (200, 200, 40), (40, 200, 120)]

    def __init__(self, speed: float, exclude_x: int | None = None):
        super().__init__()
        self.image = pygame.Surface((TRAFFIC_W, TRAFFIC_H), pygame.SRCALPHA)
        lane = random.choice([l for l in LANES if exclude_x is None
                              or abs(l - exclude_x) > LANE_W // 2])
        self.rect  = self.image.get_rect(
            centerx=lane, bottom=-10)
        self.color = random.choice(self.COLORS)
        self.speed = speed
        self._draw()

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        _draw_car(self.image, pygame.Rect(0, 0, TRAFFIC_W, TRAFFIC_H),
                  self.color, is_player=False)

    def update(self):
        self.rect.y += int(self.speed)
        if self.rect.top > HEIGHT + 20:
            self.kill()


class CoinSprite(pygame.sprite.Sprite):
    def __init__(self, speed: float, occupied_xs: list[int]):
        super().__init__()
        self.weight = random.choices([1, 2, 3], weights=[6, 3, 1])[0]
        r           = 12 + (self.weight - 1) * 3
        self.image  = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        self.score_value = self.weight * 10
        lane         = random.choice(LANES)
        self.rect    = self.image.get_rect(centerx=lane, bottom=-10)
        self.speed   = speed
        self._r      = r
        self._draw()

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        cx = cy = self._r + 2
        _draw_coin(self.image, cx, cy, self.weight)

    def update(self):
        self.rect.y += int(self.speed)
        if self.rect.top > HEIGHT + 10:
            self.kill()


class PowerUpSprite(pygame.sprite.Sprite):
    SIZE = 36

    def __init__(self, kind: str, speed: float):
        super().__init__()
        self.kind    = kind
        self.image   = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        lane         = random.choice(LANES)
        self.rect    = self.image.get_rect(centerx=lane, bottom=-10)
        self.speed   = speed
        self.frames_left = PU_FIELD_FRAMES
        self._draw()

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        _draw_powerup(self.image,
                      pygame.Rect(0, 0, self.SIZE, self.SIZE), self.kind)

    def update(self):
        self.rect.y      += int(self.speed)
        self.frames_left -= 1
        if self.rect.top > HEIGHT + 10 or self.frames_left <= 0:
            self.kill()


class OilSpill(pygame.sprite.Sprite):
    def __init__(self, speed: float, lane: int):
        super().__init__()
        self.image = pygame.Surface((60, 28), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(centerx=lane, bottom=-10)
        self.speed = speed
        _draw_oil(self.image, pygame.Rect(0, 0, 60, 28))

    def update(self):
        self.rect.y += int(self.speed)
        if self.rect.top > HEIGHT + 10:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    def __init__(self, speed: float, lane: int):
        super().__init__()
        self.image = pygame.Surface((LANE_W - 10, 20), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(centerx=lane, bottom=-10)
        self.speed = speed
        _draw_barrier(self.image, pygame.Rect(0, 0, self.image.get_width(), 20))

    def update(self):
        self.rect.y += int(self.speed)
        if self.rect.top > HEIGHT + 10:
            self.kill()


class NitroStrip(pygame.sprite.Sprite):
    def __init__(self, speed: float):
        super().__init__()
        w          = random.randint(LANE_W, LANE_W * 2)
        lane_idx   = random.randint(0, len(LANES) - 1)
        cx         = LANES[lane_idx]
        self.image = pygame.Surface((w, 16), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(centerx=cx, bottom=-10)
        self.speed = speed
        _draw_nitro_strip(self.image, pygame.Rect(0, 0, w, 16))

    def update(self):
        self.rect.y += int(self.speed)
        if self.rect.top > HEIGHT + 10:
            self.kill()


# ---------------------------------------------------------------------------
# Road renderer
# ---------------------------------------------------------------------------

class Road:
    KERB_W    = 12
    DASH_H    = 30
    DASH_GAP  = 20
    MARK_W    = 4

    def __init__(self):
        self.offset = 0.0

    def scroll(self, speed: float):
        self.offset = (self.offset + speed) % (self.DASH_H + self.DASH_GAP)

    def draw(self, surf: pygame.Surface):
        # Sky / grass flanks
        surf.fill((22, 48, 22))   # grass green
        pygame.draw.rect(surf, (20, 60, 20),
                         pygame.Rect(0, 52, ROAD_L, HEIGHT - 52))
        pygame.draw.rect(surf, (20, 60, 20),
                         pygame.Rect(ROAD_R, 52, WIDTH - ROAD_R, HEIGHT - 52))

        # Road surface
        pygame.draw.rect(surf, C_ROAD,
                         pygame.Rect(ROAD_L, 52, ROAD_W, HEIGHT - 52))

        # Kerb (animated stripes)
        for side_x in [ROAD_L - self.KERB_W, ROAD_R]:
            stripe = False
            y = 52 - int(self.offset)
            while y < HEIGHT:
                clr = C_KERB_A if stripe else C_KERB_B
                pygame.draw.rect(surf, clr,
                                 pygame.Rect(side_x, y, self.KERB_W,
                                             self.DASH_H + self.DASH_GAP))
                y      += self.DASH_H + self.DASH_GAP
                stripe  = not stripe

        # Lane dashes
        for lx in [LANES[0] + LANE_W // 2, LANES[1] + LANE_W // 2]:
            y = 52 - int(self.offset)
            while y < HEIGHT:
                pygame.draw.rect(surf, C_LANE_MRK,
                                 pygame.Rect(lx - self.MARK_W // 2, y,
                                             self.MARK_W, self.DASH_H))
                y += self.DASH_H + self.DASH_GAP

        # Road edge lines
        for ex in [ROAD_L, ROAD_R]:
            pygame.draw.line(surf, (200, 200, 200),
                             (ex, 52), (ex, HEIGHT), 2)


# ---------------------------------------------------------------------------
# GameSession
# ---------------------------------------------------------------------------

class GameSession:
    def __init__(self, car_color: tuple, difficulty: str):
        dcfg = DIFFICULTY.get(difficulty, DIFFICULTY["Normal"])
        self.speed_mult  = dcfg["speed_mult"]
        self.spawn_mult  = dcfg["spawn_mult"]
        self.traffic_n   = dcfg["traffic_n"]

        self.road         = Road()
        self.player       = PlayerCar(car_color)

        self.traffic      = pygame.sprite.Group()
        self.coins_group  = pygame.sprite.Group()
        self.powerups     = pygame.sprite.Group()
        self.oils         = pygame.sprite.Group()
        self.barriers     = pygame.sprite.Group()
        self.nitro_strips = pygame.sprite.Group()
        self.all_sprites  = pygame.sprite.Group(self.player)

        # State
        self.score        = 0
        self.coins        = 0
        self.distance_px  = 0
        self.scroll_speed = SCROLL_BASE * self.speed_mult
        self.traffic_speed = TRAFFIC_BASE * self.speed_mult

        self.shield_active = False
        self.nitro_frames  = 0     # active nitro remaining
        self.current_pu    : str | None = None

        # Timers
        self._frame       = 0
        self._coin_timer  = 0
        self._obs_timer   = 0
        self._pu_timer    = 0
        self._nitro_strip_timer = 0

        # Progression
        self._dist_pts    = 0      # distance points accumulated

        self.game_over    = False

        # Spawn initial traffic
        for _ in range(self.traffic_n):
            self._spawn_traffic()

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _current_scroll(self) -> float:
        s = self.scroll_speed
        if self.player.nitro > 0:
            s *= 1.4
        return s

    def _spawn_traffic(self):
        tc = TrafficCar(self.traffic_speed, self.player.rect.centerx)
        tc.rect.y = random.randint(-300, -TRAFFIC_H)
        self.traffic.add(tc)
        self.all_sprites.add(tc)

    def _spawn_coin(self):
        c = CoinSprite(self._current_scroll() * 0.7, [self.player.rect.centerx])
        self.coins_group.add(c)
        self.all_sprites.add(c)

    def _spawn_powerup(self):
        if self.powerups:
            return
        kind = random.choice([PU_NITRO, PU_SHIELD, PU_REPAIR])
        pu = PowerUpSprite(kind, self._current_scroll() * 0.6)
        self.powerups.add(pu)
        self.all_sprites.add(pu)

    def _spawn_hazard_row(self):
        """Hazard row: block 1-2 lanes with barriers or oil spills, leave at least 1 safe."""
        hazard_lanes = random.sample(LANES, k=random.randint(1, 2))
        safe_y = random.randint(-80, -40)
        for lane in hazard_lanes:
            kind = random.choice(["oil", "oil", "barrier"])
            if kind == "oil":
                s = OilSpill(self._current_scroll() * 0.8, lane)
                s.rect.y = safe_y
                self.oils.add(s)
                self.all_sprites.add(s)
            else:
                b = Barrier(self._current_scroll() * 0.8, lane)
                b.rect.y = safe_y
                self.barriers.add(b)
                self.all_sprites.add(b)

    def _spawn_nitro_strip(self):
        ns = NitroStrip(self._current_scroll() * 0.9)
        ns.rect.y = -20
        self.nitro_strips.add(ns)
        self.all_sprites.add(ns)

    def _increase_difficulty(self):
        self.scroll_speed  = min(SCROLL_BASE * self.speed_mult + self._dist_pts / 500,
                                 SCROLL_BASE * self.speed_mult * 2.5)
        self.traffic_speed = min(TRAFFIC_BASE * self.speed_mult + self._dist_pts / 400,
                                 TRAFFIC_BASE * self.speed_mult * 2.8)
        for tc in self.traffic:
            tc.speed = self.traffic_speed

    # -----------------------------------------------------------------------
    # Tick
    # -----------------------------------------------------------------------

    def tick(self, keys) -> bool:
        if self.game_over:
            return False

        self._frame += 1

        # Move player
        self.player.move(keys)

        # Scroll road
        spd = self._current_scroll()
        self.road.scroll(spd)
        self.distance_px  += spd
        self._dist_pts     = int(self.distance_px / DIST_PX_PER_POINT)
        self.score         = self.coins * 10 + self._dist_pts

        # Difficulty ramp
        self._increase_difficulty()

        # Update sprites
        self.traffic.update()
        self.coins_group.update()
        self.powerups.update()
        self.oils.update()
        self.barriers.update()
        self.nitro_strips.update()

        # Replenish traffic
        if len(self.traffic) < self.traffic_n:
            self._spawn_traffic()

        # ---- Spawn timers ----
        ci = max(30, int(COIN_SPAWN_INTERVAL / self.spawn_mult))
        if self._frame - self._coin_timer >= ci:
            self._spawn_coin()
            self._coin_timer = self._frame

        oi = max(80, int(OBSTACLE_SPAWN_INTERVAL / self.spawn_mult))
        if self._frame - self._obs_timer >= oi:
            self._spawn_hazard_row()
            self._obs_timer = self._frame

        pi = max(150, int(PU_SPAWN_INTERVAL / self.spawn_mult))
        if self._frame - self._pu_timer >= pi:
            self._spawn_powerup()
            self._pu_timer = self._frame

        nsi = max(200, int(400 / self.spawn_mult))
        if self._frame - self._nitro_strip_timer >= nsi:
            self._spawn_nitro_strip()
            self._nitro_strip_timer = self._frame

        # ---- Collisions: coins ----
        for c in pygame.sprite.spritecollide(self.player, self.coins_group, True):
            self.coins += c.weight
            self.score += c.score_value

        # ---- Collisions: power-ups ----
        for pu in pygame.sprite.spritecollide(self.player, self.powerups, True):
            if pu.kind == PU_NITRO:
                self.player.grant_nitro()
                self.current_pu   = PU_NITRO
            elif pu.kind == PU_SHIELD:
                self.player.grant_shield()
                self.shield_active = True
                self.current_pu    = PU_SHIELD
            elif pu.kind == PU_REPAIR:
                self.score += PU_REPAIR_BONUS
                # Clear nearest obstacle
                for grp in (self.oils, self.barriers):
                    closest = min(grp, key=lambda s: abs(s.rect.centery - self.player.rect.centery),
                                  default=None)
                    if closest:
                        closest.kill()
                        break

        # ---- Collisions: oil spills ----
        for _ in pygame.sprite.spritecollide(self.player, self.oils, True):
            self.player.apply_oil()

        # ---- Collisions: barriers ----
        if pygame.sprite.spritecollideany(self.player, self.barriers):
            if self.player.shield:
                # Consume shield, clear barrier
                self.player.consume_shield()
                self.shield_active = False
                self.current_pu    = None
                for b in pygame.sprite.spritecollide(self.player, self.barriers, True):
                    pass
            else:
                self.game_over = True
                return False

        # ---- Collisions: traffic ----
        if pygame.sprite.spritecollideany(self.player, self.traffic):
            if self.player.shield:
                self.player.consume_shield()
                self.shield_active = False
                self.current_pu    = None
                for tc in pygame.sprite.spritecollide(self.player, self.traffic, True):
                    tc.kill()
            else:
                self.game_over = True
                return False

        # ---- Nitro strip road event ----
        for ns in pygame.sprite.spritecollide(self.player, self.nitro_strips, True):
            self.player.grant_nitro()
            self.current_pu = PU_NITRO

        # Update current_pu display tracking
        if self.current_pu == PU_NITRO and self.player.nitro <= 0:
            self.current_pu = None

        return True

    # -----------------------------------------------------------------------
    # Draw
    # -----------------------------------------------------------------------

    def draw(self, surf: pygame.Surface):
        self.road.draw(surf)
        # Draw sprites in painter order (back → front)
        for grp in (self.nitro_strips, self.oils, self.barriers,
                    self.coins_group, self.powerups, self.traffic):
            for sprite in grp:
                surf.blit(sprite.image, sprite.rect)
        self.player.draw(surf)

    # -----------------------------------------------------------------------
    # Properties for HUD
    # -----------------------------------------------------------------------

    @property
    def distance(self) -> int:
        return self._dist_pts

    @property
    def pu_frames_left(self) -> int:
        if self.current_pu == PU_NITRO:
            return self.player.nitro
        return 0

    @property
    def display_speed(self) -> float:
        return self.player.effective_speed