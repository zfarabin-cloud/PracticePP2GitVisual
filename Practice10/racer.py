# racer
import pygame
import random
import time
from itertools import chain

# НАСТРОЙКИ И КОНСТАНТЫ
WIDTH, HEIGHT = 400, 600
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# ИНИЦИАЛИЗАЦИЯ
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font_large.render("Game Over", True, BLACK)

# Загрузка ресурсов
try:
    bg = pygame.image.load("Practice10/images/AnimatedStreet.png")
    player_img = pygame.image.load('Practice10/images/Player.png')
    enemy_img = pygame.image.load('Practice10/images/Enemy.png')
    coin_img = pygame.image.load('Practice10/images/coin.png')
    
    pygame.mixer.music.load('Practice10/sounds/background.wav')
    crash_sound = pygame.mixer.Sound('Practice10/sounds/crash.wav')
except pygame.error as e:
    print(f"Ошибка загрузки файлов: {e}")
    pygame.quit()
    exit()

# КЛАССЫ ОБЪЕКТОВ

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - self.rect.height // 2 - 10)
    
    def update(self):
        """Обработка движения игрока."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(PLAYER_SPEED, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset()
    
    def update(self):
        """Движение врага вниз и респавн."""
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > HEIGHT:
            self.reset()
            
    def reset(self):
        """Сброс позиции врага наверх."""
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset()
    
    def update(self):
        """Движение монетки вниз."""
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        """Случайное появление монетки наверху."""
        self.rect.center = (random.randint(20, WIDTH - 20), -50)

# СОЗДАНИЕ ГРУПП И ОБЪЕКТОВ
player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group(enemy)
coins = pygame.sprite.Group(coin)
all_sprites = pygame.sprite.Group(player, enemy, coin)

# Глобальные переменные игры
score = 0
coin_score = 0
running = True

# Запуск музыки
pygame.mixer.music.play(-1)

# ОСНОВНОЙ ЦИКЛ
while running:
    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Обновление состояний (Логика)
    all_sprites.update()

    # Проверка столкновения с монетками
    if pygame.sprite.spritecollide(player, coins, False):
        coin_score += 1
        coin.reset() # Просто перемещаем ту же монетку наверх

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.music.stop()
        crash_sound.play()
        time.sleep(0.5)
        
        # Экран Game Over
        screen.fill(RED)
        rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, rect)
        pygame.display.flip()
        
        time.sleep(2)
        running = False

    # 3. Отрисовка
    screen.blit(bg, (0, 0))
    
    # Рисуем все спрайты
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # Отображение счета
    score_text = font_small.render(f"Coins: {coin_score}", True, BLACK)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()