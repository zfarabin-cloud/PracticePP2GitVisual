# paint
import pygame
import math

# --- КОНСТАНТЫ И НАСТРОЙКИ ---
FPS = 60
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Цвета палитры
COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "white": (255, 255, 255)
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint & Shape Drawing")
clock = pygame.time.Clock()

# Холст для рисования
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def load_icon(path, pos):
    """Загрузка иконки инструмента."""
    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (40, 40))
        return img, img.get_rect(topleft=pos)
    except:
        # Если картинки нет, создаем заглушку-квадрат
        surf = pygame.Surface((40, 40))
        surf.fill((200, 200, 200))
        return surf, surf.get_rect(topleft=pos)

def draw_eq_triangle(surf, color, start, width):
    """Рисование равностороннего треугольника."""
    h = (math.sqrt(3) / 2) * width
    pts = [start, (start[0] + width // 2, start[1] - h), (start[0] + width, start[1])]
    pygame.draw.polygon(surf, color, pts, 2)

def draw_rhombus(surf, color, start, w, h):
    """Рисование ромба."""
    pts = [
        (start[0] + w // 2, start[1]),
        (start[0] + w, start[1] + h // 2),
        (start[0] + w // 2, start[1] + h),
        (start[0], start[1] + h // 2)
    ]
    pygame.draw.polygon(surf, color, pts, 2)

# --- ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ---

# Иконки инструментов (пути нужно проверить)
tool_names = ["rectangle", "circle", "square", "triangle", "eq_triangle", "rhombus"]
tools = {}
for i, name in enumerate(tool_names):
    path = f"Practice11/images/{name}.png"
    tools[name] = load_icon(path, (10 + i * 50, 10))

# Палитра цветов
palette_rects = []
for i, color in enumerate(COLORS.values()):
    rect = pygame.Rect(10 + i * 40, 60, 30, 30)
    palette_rects.append((rect, color))

# --- СОСТОЯНИЕ ПРИЛОЖЕНИЯ ---
current_tool = "brush"
color_brush = BLACK
brush_size = 5
drawing = False
start_pos = None
prev_pos = None
running = True

# --- ОСНОВНОЙ ЦИКЛ ---
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Выбор инструмента или начало рисования
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1. Проверяем нажатие на иконки инструментов
            for name, (img, rect) in tools.items():
                if rect.collidepoint(event.pos):
                    current_tool = name

            # 2. Проверяем выбор цвета
            for rect, color in palette_rects:
                if rect.collidepoint(event.pos):
                    color_brush = color

            # 3. Если нажали не на UI — начинаем рисовать
            ui_area = pygame.Rect(0, 0, WIDTH, 100) # Примерная зона интерфейса
            if not ui_area.collidepoint(event.pos):
                drawing = True
                start_pos = event.pos

        # Завершение рисования фигуры
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and current_tool not in ["brush", "eraser"]:
                x1, y1 = start_pos
                x2, y2 = event.pos
                w, h = abs(x2 - x1), abs(y2 - y1)
                top_left = (min(x1, x2), min(y1, y2))

                if current_tool == "rectangle":
                    pygame.draw.rect(canvas, color_brush, (*top_left, w, h), 2)
                elif current_tool == "circle":
                    pygame.draw.circle(canvas, color_brush, (x1 + (x2-x1)//2, y1 + (y2-y1)//2), max(w, h)//2, 2)
                elif current_tool == "square":
                    side = min(w, h)
                    pygame.draw.rect(canvas, color_brush, (*top_left, side, side), 2)
                elif current_tool == "triangle":
                    pygame.draw.polygon(canvas, color_brush, [start_pos, (x2, y2), (x1, y2)], 2)
                elif current_tool == "eq_triangle":
                    draw_eq_triangle(canvas, color_brush, top_left, w)
                elif current_tool == "rhombus":
                    draw_rhombus(canvas, color_brush, top_left, w, h)
            
            drawing = False
            prev_pos = None

        # Горячие клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b: current_tool = "brush"
            if event.key == pygame.K_e: current_tool = "eraser"

    # Логика кисти и ластика (непрерывное рисование)
    if pygame.mouse.get_pressed()[0] and current_tool in ["brush", "eraser"]:
        # Рисуем только если мы ниже зоны кнопок
        if mouse_pos[1] > 100:
            color = WHITE if current_tool == "eraser" else color_brush
            if prev_pos:
                pygame.draw.line(canvas, color, prev_pos, mouse_pos, brush_size * 2)
            prev_pos = mouse_pos

    # --- ОТРИСОВКА ---
    screen.blit(canvas, (0, 0)) # Сначала холст

    # Рисуем интерфейс (поверх холста)
    for name, (img, rect) in tools.items():
        # Подсветка выбранного инструмента
        if current_tool == name:
            pygame.draw.rect(screen, (200, 200, 255), rect.inflate(4, 4))
        screen.blit(img, rect)

    for rect, color in palette_rects:
        pygame.draw.rect(screen, color, rect)
        if color_brush == color: # Рамка вокруг выбранного цвета
            pygame.draw.rect(screen, BLACK, rect, 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()