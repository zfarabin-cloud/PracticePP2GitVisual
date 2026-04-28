# racer
import pygame
import random
import time
from itertools import chain

# --- КОНСТАНТЫ И НАСТРОЙКИ ---
WIDTH, HEIGHT = 400, 600
FPS = 60
PLAYER_SPEED = 5
INITIAL_ENEMY_SPEED = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font.render("Game Over", True, BLACK)

# Загрузка ресурсов
background = pygame.image.load("Practice11/images/AnimatedStreet.png")
player_img = pygame.image.load('Practice11/images/Player.png')
enemy_img = pygame.image.load('Practice11/images/Enemy.png')
coin_img = pygame.image.load('Practice11/images/coin.png')

# Звуки
pygame.mixer.music.load('Practice11/sounds/background.wav')
pygame.mixer.music.play(-1)
crash_sound = pygame.mixer.Sound('Practice11/sounds/crash.wav')

# --- КЛАССЫ ОБЪЕКТОВ ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - self.rect.height // 2)
    
    def move(self):
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
    
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.reset()
    
    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        # Настройка внешнего вида и веса монеты
        self.image = pygame.transform.scale(coin_img, (40, 40))
        self.rect = self.image.get_rect()
        self.weight = random.randint(1, 3) 
        self.score_value = self.weight * 10
        self.reset(enemy)
    
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.kill() # Удаляем старую монету, если улетела

    def reset(self, enemy):
        # Логика появления, чтобы не перекрывать врага
        x_range = list(chain(
            range(20, max(21, enemy.rect.left - 40)), 
            range(min(WIDTH - 60, enemy.rect.right + 20), WIDTH - 40)
        ))
        self.rect.x = random.choice(x_range) if x_range else random.randint(0, WIDTH - 40)
        self.rect.y = -self.rect.height

# --- ГРУППЫ СПРАЙТОВ ---
player = Player()
enemy = Enemy()

enemies = pygame.sprite.Group(enemy)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player, enemy)

# --- ИГРОВЫЕ ПЕРЕМЕННЫЕ ---
coin_score = 0
enemy_speed = INITIAL_ENEMY_SPEED
running = True

# --- ОСНОВНОЙ ЦИКЛ ---
while running:
    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 2. Логика движения
    player.move()
    enemy.move(enemy_speed)
    
    # Создание монет, если их нет на экране
    if len(coins) == 0:
        new_coin = Coin(enemy)
        coins.add(new_coin)
        all_sprites.add(new_coin)

    for coin in coins:
        coin.move(enemy_speed)

    # 3. Проверка столкновений (Монеты)
    collected = pygame.sprite.spritecollide(player, coins, True)
    for c in collected:
        coin_score += c.score_value
        # Ускоряем игру каждые 50 очков
        if coin_score % 50 == 0:
            enemy_speed += 1

    # 4. Проверка столкновений (Враги)
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.music.stop()
        crash_sound.play()
        time.sleep(0.5)
        
        screen.fill(RED)
        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()
        
        time.sleep(2)
        running = False

    # 5. Отрисовка
    screen.blit(background, (0, 0))
    
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    # Отображение счета
    score_surf = font_small.render(f"Score: {coin_score}", True, BLACK)
    screen.blit(score_surf, (WIDTH - score_surf.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()