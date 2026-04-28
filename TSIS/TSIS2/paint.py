# paint
import pygame
import math
import datetime
import sys

from tools import (
    draw_rectangle, draw_circle, draw_square,
    draw_right_triangle, draw_eq_triangle, draw_rhombus,
    draw_line, flood_fill,
)

# Constants
FPS           = 60
WIDTH, HEIGHT = 1200, 800
TOOLBAR_H     = 110          # height of the top toolbar area
WHITE         = (255, 255, 255)
BLACK         = (0, 0, 0)
LIGHT_GRAY    = (220, 220, 220)
MID_GRAY      = (180, 180, 180)
DARK_GRAY     = (100, 100, 100)
HIGHLIGHT     = (173, 216, 230)   # light-blue selection highlight

BRUSH_SIZES   = {1: 2, 2: 5, 3: 10}   # key → pixel width

PALETTE_COLORS = [
    (0,   0,   0),    # black
    (255, 255, 255),  # white
    (200, 200, 200),  # light grey
    (128, 128, 128),  # grey
    (255,   0,   0),  # red
    (180,   0,   0),  # dark red
    (255, 165,   0),  # orange
    (255, 255,   0),  # yellow
    (0,   200,   0),  # green
    (0,   128,   0),  # dark green
    (0,   255, 255),  # cyan
    (0,     0, 255),  # blue
    (0,     0, 180),  # dark blue
    (148,   0, 211),  # purple
    (255,  20, 147),  # pink
    (139,  69,  19),  # brown
]

# Tool definitions: (label, shortcut hint)
TOOL_DEFS = [
    ("pencil",      "P"),
    ("line",        "L"),
    ("rectangle",   "R"),
    ("circle",      "C"),
    ("square",      "Q"),
    ("tri_right",   "T"),
    ("tri_eq",      "E"),
    ("rhombus",     "D"),
    ("fill",        "F"),
    ("text",        "X"),
    ("eraser",      "W"),
]

# UI helpers
def make_tool_button(label, x, y, w=60, h=36):
    """Return (label, rect)."""
    return label, pygame.Rect(x, y, w, h)


def draw_toolbar(surf, tool_buttons, current_tool, brush_size,
                 palette_rects, color_brush):
    """Render the full toolbar."""
    pygame.draw.rect(surf, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(surf, MID_GRAY, (0, TOOLBAR_H), (WIDTH, TOOLBAR_H), 2)

    font_sm = pygame.font.SysFont("segoeui", 13)
    font_key = pygame.font.SysFont("segoeui", 11, bold=True)

    # --- Tool buttons ---
    for label, rect in tool_buttons:
        bg = HIGHLIGHT if current_tool == label else WHITE
        pygame.draw.rect(surf, bg, rect, border_radius=5)
        pygame.draw.rect(surf, DARK_GRAY, rect, 1, border_radius=5)

        nice = {
            "pencil":    "Pencil",
            "line":      "Line",
            "rectangle": "Rect",
            "circle":    "Circle",
            "square":    "Square",
            "tri_right": "Tri-R",
            "tri_eq":    "Tri-E",
            "rhombus":   "Rhomb",
            "fill":      "Fill",
            "text":      "Text",
            "eraser":    "Eraser",
        }
        txt = font_sm.render(nice.get(label, label), True, BLACK)
        surf.blit(txt, txt.get_rect(center=rect.center))

    # --- Brush-size buttons ---
    bx, by = 10, 72
    for key, px in BRUSH_SIZES.items():
        r = pygame.Rect(bx + (key - 1) * 44, by, 40, 28)
        bg = HIGHLIGHT if brush_size == px else WHITE
        pygame.draw.rect(surf, bg, r, border_radius=4)
        pygame.draw.rect(surf, DARK_GRAY, r, 1, border_radius=4)
        lbl = font_sm.render(f"{key} ({px}px)", True, BLACK)
        surf.blit(lbl, lbl.get_rect(center=r.center))

    # --- Palette ---
    for rect, color in palette_rects:
        pygame.draw.rect(surf, color, rect)
        border = BLACK if color_brush == color else DARK_GRAY
        bw = 2 if color_brush == color else 1
        pygame.draw.rect(surf, border, rect, bw)

    # --- Current color swatch ---
    swatch = pygame.Rect(WIDTH - 60, 10, 45, 45)
    pygame.draw.rect(surf, color_brush, swatch)
    pygame.draw.rect(surf, BLACK, swatch, 2)
    lbl = font_key.render("Color", True, DARK_GRAY)
    surf.blit(lbl, (swatch.x + 3, swatch.bottom + 2))

    # --- Shortcut hints strip ---
    hints = "P=Pencil  L=Line  R=Rect  C=Circle  Q=Square  T=Tri  E=EqTri  D=Rhomb  F=Fill  X=Text  W=Eraser  1/2/3=Size  Ctrl+S=Save"
    htxt = font_key.render(hints, True, DARK_GRAY)
    surf.blit(htxt, (145, 82))


# Shape preview (draws on a temporary surface overlay)
SHAPE_TOOLS = {"rectangle", "circle", "square", "tri_right", "tri_eq", "rhombus", "line"}

DRAW_FN = {
    "rectangle": draw_rectangle,
    "circle":    draw_circle,
    "square":    draw_square,
    "tri_right": draw_right_triangle,
    "tri_eq":    draw_eq_triangle,
    "rhombus":   draw_rhombus,
    "line":      draw_line,
}


def commit_shape(canvas, tool, color, start, end, thickness):
    fn = DRAW_FN.get(tool)
    if fn:
        fn(canvas, color, start, end, thickness)


def draw_preview(screen, canvas, tool, color, start, end, thickness):
    """Blit canvas then draw a transparent preview on top."""
    screen.blit(canvas, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # Use a semi-transparent version of the color for preview
    preview_color = (*color, 180)
    fn = DRAW_FN.get(tool)
    if fn:
        fn(overlay, preview_color, start, end, thickness)
    screen.blit(overlay, (0, 0))


# Main
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint — TSIS2")
    clock = pygame.time.Clock()

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(WHITE)

    # Build tool buttons (two rows)
    tool_buttons = []
    cols, bw, bh, gap = 11, 62, 36, 4
    start_x, start_y = 142, 10
    for i, (label, _) in enumerate(TOOL_DEFS):
        x = start_x + i * (bw + gap)
        _, rect = make_tool_button(label, x, start_y, bw, bh)
        tool_buttons.append((label, rect))

    # Build palette
    palette_rects = []
    pal_x, pal_y, pal_w, pal_h = WIDTH - 340, 10, 22, 22
    per_row = 8
    for i, color in enumerate(PALETTE_COLORS):
        col = i % per_row
        row = i // per_row
        rect = pygame.Rect(pal_x + col * (pal_w + 2), pal_y + row * (pal_h + 2), pal_w, pal_h)
        palette_rects.append((rect, color))

    # Brush-size hit rects (for mouse clicks)
    size_rects = []
    bx, by2 = 10, 72
    for key, px in BRUSH_SIZES.items():
        r = pygame.Rect(bx + (key - 1) * 44, by2, 40, 28)
        size_rects.append((r, px))

    # App state
    current_tool  = "pencil"
    color_brush   = BLACK
    brush_size    = BRUSH_SIZES[2]   # medium by default
    drawing       = False
    start_pos     = None
    prev_pos      = None

    # Text tool state
    text_active   = False
    text_pos      = (0, 0)
    text_buffer   = ""
    font_text     = pygame.font.SysFont("segoeui", 24)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # KEYDOWN
            if event.type == pygame.KEYDOWN:

                # Text mode captures all printable keys
                if text_active:
                    if event.key == pygame.K_RETURN:
                        # Commit text to canvas
                        rendered = font_text.render(text_buffer, True, color_brush)
                        canvas.blit(rendered, text_pos)
                        text_active  = False
                        text_buffer  = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_buffer = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]
                    else:
                        ch = event.unicode
                        if ch and ch.isprintable():
                            text_buffer += ch
                    continue   # don't process other shortcuts while typing

                # Ctrl+S — save canvas
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    name = f"canvas_{ts}.png"
                    pygame.image.save(canvas, name)
                    pygame.display.set_caption(f"Paint — saved: {name}")
                    continue

                # Tool shortcuts
                key_tool = {
                    pygame.K_p: "pencil",
                    pygame.K_l: "line",
                    pygame.K_r: "rectangle",
                    pygame.K_c: "circle",
                    pygame.K_q: "square",
                    pygame.K_t: "tri_right",
                    pygame.K_e: "tri_eq",
                    pygame.K_d: "rhombus",
                    pygame.K_f: "fill",
                    pygame.K_x: "text",
                    pygame.K_w: "eraser",
                }
                if event.key in key_tool:
                    current_tool = key_tool[event.key]

                # Brush size shortcuts
                if event.key == pygame.K_1: brush_size = BRUSH_SIZES[1]
                if event.key == pygame.K_2: brush_size = BRUSH_SIZES[2]
                if event.key == pygame.K_3: brush_size = BRUSH_SIZES[3]

            # MOUSE BUTTON DOWN
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Check toolbar tool buttons
                for label, rect in tool_buttons:
                    if rect.collidepoint(event.pos):
                        current_tool = label
                        break

                # Check palette
                for rect, color in palette_rects:
                    if rect.collidepoint(event.pos):
                        color_brush = color
                        break

                # Check brush-size buttons
                for rect, px in size_rects:
                    if rect.collidepoint(event.pos):
                        brush_size = px
                        break

                # Canvas area interaction
                if event.pos[1] > TOOLBAR_H:
                    if current_tool == "fill":
                        flood_fill(canvas, event.pos, color_brush)

                    elif current_tool == "text":
                        text_active = True
                        text_pos    = event.pos
                        text_buffer = ""

                    elif current_tool in SHAPE_TOOLS:
                        drawing   = True
                        start_pos = event.pos

                    elif current_tool in ("pencil", "eraser"):
                        drawing   = True
                        prev_pos  = event.pos

            # MOUSE BUTTON UP  — commit shape / line
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and current_tool in SHAPE_TOOLS and start_pos:
                    commit_shape(canvas, current_tool, color_brush,
                                 start_pos, event.pos, brush_size)
                drawing   = False
                start_pos = None
                prev_pos  = None

        # Continuous pencil / eraser drawing
        if pygame.mouse.get_pressed()[0]:
            if current_tool in ("pencil", "eraser") and mouse_pos[1] > TOOLBAR_H:
                color = WHITE if current_tool == "eraser" else color_brush
                size  = brush_size * 3 if current_tool == "eraser" else brush_size
                if prev_pos:
                    pygame.draw.line(canvas, color, prev_pos, mouse_pos, size)
                prev_pos = mouse_pos
            else:
                if not drawing:
                    prev_pos = None

        # RENDER
        # 1. Draw canvas (with live shape preview if dragging)
        if drawing and current_tool in SHAPE_TOOLS and start_pos:
            draw_preview(screen, canvas, current_tool, color_brush,
                         start_pos, mouse_pos, brush_size)
        else:
            screen.blit(canvas, (0, 0))

        # 2. Text cursor / live text preview
        if text_active:
            preview = font_text.render(text_buffer + "|", True, color_brush)
            screen.blit(preview, text_pos)

        # 3. Toolbar (drawn last so it always sits on top)
        draw_toolbar(screen, tool_buttons, current_tool, brush_size,
                     palette_rects, color_brush)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()