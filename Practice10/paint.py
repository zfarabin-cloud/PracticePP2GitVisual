# paint
import pygame

# КОНСТАНТЫ И НАСТРОЙКИ
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLORS = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), 
    (255, 255, 0), (255, 165, 0), (255, 255, 255)
]

# ИНИЦИАЛИЗАЦИЯ
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint App")
clock = pygame.time.Clock()

# Холст для рисования
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas.fill(WHITE)

# Загрузка интерфейса
try:
    image_rect = pygame.image.load("Practice10/images/rectangle.png")
    image_circ = pygame.image.load("Practice10/images/circle.png")
except pygame.error:
    # Заглушки, если картинки не найдены
    image_rect = pygame.Surface((40, 40)); image_rect.fill((200, 200, 200))
    image_circ = pygame.Surface((40, 40)); image_circ.fill((200, 200, 200))

# Позиции кнопок инструментов
rect_btn = image_rect.get_rect(topleft=(10, 10))
circ_btn = image_circ.get_rect(topleft=(60, 10))

# Создание прямоугольников для палитры
palette_rects = []
for i, color in enumerate(COLORS):
    r = pygame.Rect(10 + i * 40, 60, 30, 30)
    palette_rects.append((r, color))

# СОСТОЯНИЕ ПРОГРАММЫ
running = True
current_tool = "brush"  # brush, eraser, rectangle, circle
color_brush = BLACK
brush_size = 5
drawing = False
start_pos = None
prev_pos = None

def get_ui_rects():
    """Возвращает список всех областей интерфейса, чтобы не рисовать поверх них."""
    return [rect_btn, circ_btn] + [r for r, c in palette_rects]

# ОСНОВНОЙ ЦИКЛ
while running:
    mouse_pos = pygame.mouse.get_pos()
    ui_hovered = any(r.collidepoint(mouse_pos) for r in get_ui_rects())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Выбор цвета и инструментов
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect_btn.collidepoint(event.pos):
                current_tool = "rectangle"
            elif circ_btn.collidepoint(event.pos):
                current_tool = "circle"
            else:
                # Проверка выбора цвета
                for r, color in palette_rects:
                    if r.collidepoint(event.pos):
                        color_brush = color
                
                # Начало рисования фигур
                if not ui_hovered and current_tool in ["rectangle", "circle"]:
                    drawing = True
                    start_pos = event.pos

        # Завершение рисования фигур
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos
                w, h = abs(x2 - x1), abs(y2 - y1)
                top_left = (min(x1, x2), min(y1, y2))

                if current_tool == "rectangle":
                    pygame.draw.rect(canvas, color_brush, (*top_left, w, h), 2)
                elif current_tool == "circle":
                    pygame.draw.circle(canvas, color_brush, (x1 + (x2-x1)//2, y1 + (y2-y1)//2), max(w, h)//2, 2)
                
                drawing = False
            prev_pos = None

        # Горячие клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b: current_tool = "brush"
            if event.key == pygame.K_e: current_tool = "eraser"

    # Рисование кистью или ластиком (удержание кнопки)
    if pygame.mouse.get_pressed()[0] and not ui_hovered:
        if current_tool in ["brush", "eraser"]:
            color = WHITE if current_tool == "eraser" else color_brush
            if prev_pos:
                pygame.draw.line(canvas, color, prev_pos, mouse_pos, brush_size * 2)
            prev_pos = mouse_pos

    # ОТРИСОВКА
    screen.blit(canvas, (0, 0)) # Сначала холст

    # Интерфейс (поверх холста)
    screen.blit(image_rect, rect_btn)
    screen.blit(image_circ, circ_btn)
    for r, color in palette_rects:
        pygame.draw.rect(screen, color, r)
        pygame.draw.rect(screen, BLACK, r, 1) # Обводка кнопок цвета

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()