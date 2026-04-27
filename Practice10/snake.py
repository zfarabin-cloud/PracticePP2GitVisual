# snake
import pygame
import time
import random

# КОНСТАНТЫ И НАСТРОЙКИ
WINDOW_X = 720
WINDOW_Y = 480
BLOCK_SIZE = 10  # Размер одного сегмента змейки и еды

# Цвета
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED   = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

# Настройки сложности
INITIAL_SPEED = 15
FOOD_PER_LEVEL = 4  # Сколько еды нужно съесть для повышения уровня
SPEED_INCREMENT = 2 # На сколько увеличивается скорость за уровень

# ИНИЦИАЛИЗАЦИЯ 
pygame.init()
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
fps_controller = pygame.time.Clock()

# СОСТОЯНИЕ ИГРЫ
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Генерация первой еды
fruit_pos = [random.randrange(1, (WINDOW_X // BLOCK_SIZE)) * BLOCK_SIZE,
             random.randrange(1, (WINDOW_Y // BLOCK_SIZE)) * BLOCK_SIZE]

direction = 'RIGHT'
change_to = direction

score = 0
level = 1
food_count = 0
current_speed = INITIAL_SPEED

# ФУНКЦИИ

def show_score(color, font_name, size):
    """Отображает текущий счет и уровень на экране."""
    score_font = pygame.font.SysFont(font_name, size)
    
    # Рендерим текст
    score_surface = score_font.render(f'Score: {score}', True, color)
    level_surface = score_font.render(f'Level: {level}', True, color)
    
    # Отрисовываем (Счет слева, Уровень справа)
    game_window.blit(score_surface, (10, 10))
    level_rect = level_surface.get_rect()
    level_rect.topright = (WINDOW_X - 10, 10)
    game_window.blit(level_surface, level_rect)

def game_over():
    """Логика завершения игры."""
    my_font = pygame.font.SysFont('times new roman', 50)
    go_surface = my_font.render(f'Game Over! Score: {score}', True, RED)
    go_rect = go_surface.get_rect(center=(WINDOW_X/2, WINDOW_Y/2))
    
    game_window.fill(BLACK)
    game_window.blit(go_surface, go_rect)
    pygame.display.flip()
    
    time.sleep(2)
    pygame.quit()
    exit()

def spawn_fruit():
    """Создает координаты еды, которая не пересекается с телом змейки."""
    while True:
        new_pos = [random.randrange(1, (WINDOW_X // BLOCK_SIZE)) * BLOCK_SIZE,
                   random.randrange(1, (WINDOW_Y // BLOCK_SIZE)) * BLOCK_SIZE]
        if new_pos not in snake_body:
            return new_pos

# ОСНОВНОЙ ЦИКЛ
while True:
    # 1. Обработка ввода
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:    change_to = 'UP'
            if event.key == pygame.K_DOWN:  change_to = 'DOWN'
            if event.key == pygame.K_LEFT:  change_to = 'LEFT'
            if event.key == pygame.K_RIGHT: change_to = 'RIGHT'
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 2. Проверка направления (запрет разворота на 180 градусов)
    if change_to == 'UP'    and direction != 'DOWN':  direction = 'UP'
    if change_to == 'DOWN'  and direction != 'UP':    direction = 'DOWN'
    if change_to == 'LEFT'  and direction != 'RIGHT': direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':  direction = 'RIGHT'

    # 3. Движение головы
    if direction == 'UP':    snake_pos[1] -= BLOCK_SIZE
    if direction == 'DOWN':  snake_pos[1] += BLOCK_SIZE
    if direction == 'LEFT':  snake_pos[0] -= BLOCK_SIZE
    if direction == 'RIGHT': snake_pos[0] += BLOCK_SIZE

    # 4. Механика роста и еды
    snake_body.insert(0, list(snake_pos))
    
    if snake_pos[0] == fruit_pos[0] and snake_pos[1] == fruit_pos[1]:
        score += level * 10
        food_count += 1
        fruit_pos = spawn_fruit()
        
        # Проверка повышения уровня
        if food_count >= FOOD_PER_LEVEL:
            level += 1
            current_speed += SPEED_INCREMENT
            food_count = 0
    else:
        snake_body.pop() # Убираем хвост, если ничего не съели

    # 5. Отрисовка
    game_window.fill(BLACK)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
    pygame.draw.rect(game_window, WHITE, (fruit_pos[0], fruit_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # 6. Проверка столкновений
    # Стены
    if snake_pos[0] < 0 or snake_pos[0] > WINDOW_X - BLOCK_SIZE: game_over()
    if snake_pos[1] < 0 or snake_pos[1] > WINDOW_Y - BLOCK_SIZE: game_over()
    
    # Самопересечение
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # 7. Финализация кадра
    show_score(WHITE, 'times new roman', 20)
    pygame.display.update()
    fps_controller.tick(current_speed)