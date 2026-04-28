# tools
import math
import pygame
from collections import deque


# Shape drawing helpers
def draw_rectangle(surf, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    w, h = abs(x2 - x1), abs(y2 - y1)
    top_left = (min(x1, x2), min(y1, y2))
    pygame.draw.rect(surf, color, (*top_left, w, h), thickness)


def draw_circle(surf, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    r = max(abs(x2 - x1), abs(y2 - y1)) // 2
    pygame.draw.circle(surf, color, (cx, cy), r, thickness)


def draw_square(surf, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    top_left = (min(x1, x2), min(y1, y2))
    pygame.draw.rect(surf, color, (*top_left, side, side), thickness)


def draw_right_triangle(surf, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    pts = [start, (x2, y2), (x1, y2)]
    pygame.draw.polygon(surf, color, pts, thickness)


def draw_eq_triangle(surf, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    w = abs(x2 - x1)
    h = (math.sqrt(3) / 2) * w
    tl = (min(x1, x2), min(y1, y2))
    pts = [
        (tl[0], tl[1] + h),
        (tl[0] + w // 2, tl[1]),
        (tl[0] + w, tl[1] + h),
    ]
    pygame.draw.polygon(surf, color, pts, thickness)


def draw_rhombus(surf, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    w, h = abs(x2 - x1), abs(y2 - y1)
    tl = (min(x1, x2), min(y1, y2))
    pts = [
        (tl[0] + w // 2, tl[1]),
        (tl[0] + w, tl[1] + h // 2),
        (tl[0] + w // 2, tl[1] + h),
        (tl[0], tl[1] + h // 2),
    ]
    pygame.draw.polygon(surf, color, pts, thickness)


def draw_line(surf, color, start, end, thickness):
    pygame.draw.line(surf, color, start, end, thickness)


# Flood fill
def flood_fill(surf, pos, fill_color):
    """BFS flood-fill on a pygame.Surface."""
    x, y = int(pos[0]), int(pos[1])
    w, h = surf.get_size()

    if not (0 <= x < w and 0 <= y < h):
        return

    target_color = surf.get_at((x, y))[:3]   # ignore alpha
    fill_rgb = fill_color[:3]

    if target_color == fill_rgb:
        return

    queue = deque()
    queue.append((x, y))
    visited = set()
    visited.add((x, y))

    while queue:
        cx, cy = queue.popleft()
        surf.set_at((cx, cy), fill_color)

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in visited and 0 <= nx < w and 0 <= ny < h:
                if surf.get_at((nx, ny))[:3] == target_color:
                    visited.add((nx, ny))
                    queue.append((nx, ny))