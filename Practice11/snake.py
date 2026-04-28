# snake
import pygame
import time
import random

# --- КОНСТАНТЫ ---
WIDTH, HEIGHT = 720, 480
BLOCK_SIZE = 10
FPS_INITIAL = 15

# Цвета
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_RED   = pygame.Color(255, 0, 0)
COLOR_GREEN = pygame.Color(0, 255, 0)

# --- КЛАССЫ ---

class Snake:
    def __init__(self):
        self.pos = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def change_dir(self, new_dir):
        """Проверка, чтобы змея не развернулась в себя."""
        dirs = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_dir != dirs[self.direction]:
            self.direction = new_dir

    def move(self):
        if self.direction == 'UP':    self.pos[1] -= BLOCK_SIZE
        if self.direction == 'DOWN':  self.pos[1] += BLOCK_SIZE
        if self.direction == 'LEFT':  self.pos[0] -= BLOCK_SIZE
        if self.direction == 'RIGHT': self.pos[0] += BLOCK_SIZE
        # Добавляем новую голову
        self.body.insert(0, list(self.pos))

class Food:
    def __init__(self):
        self.spawn()
        
    def spawn(self):
        """Создание еды с весом и таймером."""
        self.x = random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE
        self.y = random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE
        self.weight = random.randint(1, 3)
        self.points = self.weight * 10
        self.size = BLOCK_SIZE + (self.weight - 1) * 2 # Немного увеличиваем визуально
        self.lifetime = random.randint(5, 10)
        self.start_time = time.time()

    def is_expired(self):
        return time.time() - self.start_time > self.lifetime

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_WHITE, (self.x, self.y, self.size, self.size))

# --- ФУНКЦИИ ИГРЫ ---

def show_info(surface, score, level):
    font = pygame.font.SysFont('times new roman', 20)
    score_surf = font.render(f'Score: {score} | Level: {level}', True, COLOR_WHITE)
    surface.blit(score_surf, (10, 10))

def game_over(surface, score):
    font = pygame.font.SysFont('times new roman', 50)
    go_surf = font.render(f'Game Over! Score: {score}', True, COLOR_RED)
    rect = go_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    surface.fill(COLOR_BLACK)
    surface.blit(go_surf, rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    exit()

# --- ОСНОВНОЙ ЦИКЛ ---

def main():
    pygame.init()
    pygame.display.set_caption('Snake Game')
    game_window = pygame.display.set_mode((WIDTH, HEIGHT))
    fps_controller = pygame.time.Clock()

    # Инициализация объектов
    snake = Snake()
    food = Food()
    
    score = 0
    level = 1
    food_count = 0
    current_speed = FPS_INITIAL

    while True:
        # 1. События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    snake.change_dir('UP')
                if event.key == pygame.K_DOWN:  snake.change_dir('DOWN')
                if event.key == pygame.K_LEFT:  snake.change_dir('LEFT')
                if event.key == pygame.K_RIGHT: snake.change_dir('RIGHT')

        # 2. Логика движения
        snake.move()

        # Проверка поедания еды
        # Используем небольшую погрешность для разного размера еды
        if abs(snake.pos[0] - food.x) < BLOCK_SIZE and abs(snake.pos[1] - food.y) < BLOCK_SIZE:
            score += food.points
            food_count += 1
            food.spawn()
            
            # Уровни
            if food_count >= 4:
                level += 1
                current_speed += 2
                food_count = 0
        else:
            snake.body.pop() # Если не съели — убираем хвост

        # Проверка срока годности еды
        if food.is_expired():
            food.spawn()

        # 3. Проверка столкновений
        # Стены
        if snake.pos[0] < 0 or snake.pos[0] > WIDTH - BLOCK_SIZE: game_over(game_window, score)
        if snake.pos[1] < 0 or snake.pos[1] > HEIGHT - BLOCK_SIZE: game_over(game_window, score)
        # Самоубийство
        for block in snake.body[1:]:
            if snake.pos == block:
                game_over(game_window, score)

        # 4. Отрисовка
        game_window.fill(COLOR_BLACK)
        
        for pos in snake.body:
            pygame.draw.rect(game_window, COLOR_GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        food.draw(game_window)
        show_info(game_window, score, level)

        pygame.display.update()
        fps_controller.tick(current_speed)

if __name__ == "__main__":
    main()