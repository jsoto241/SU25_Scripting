# Jose Soto
# GAME 2341 - Summer
# Final Project Game

''' This is a simple shoot'em up where you use the arrow keys to make left and right and space to shoot. '''


import pygame
import random
import sys
import math


# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Insert Cool Name Later")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
FONT = pygame.font.SysFont("Arial", 32)

# Load images
PLAYER_IMG = pygame.image.load("player.png")
ENEMY_IMG = pygame.image.load("enemyM.png")
BULLET_IMG = pygame.image.load("playerProj.png")
ENEMY_BULLET_IMG = pygame.image.load("enemyProj.png")

# Game constants
FPS = 60
MAX_SHOOT_DELAY = 10000  # milliseconds

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ENEMY_BULLET_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.last_shot = pygame.time.get_ticks()
        self.next_shot_delay = random.randint(3000, MAX_SHOOT_DELAY)

    def update(self):
        now = pygame.time.get_ticks()
        # Shoot randomly but at least every 15 seconds
        if now - self.last_shot >= self.next_shot_delay or now - self.last_shot >= 15000:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            enemy_bullets.add(bullet)
            all_sprites.add(bullet)
            self.last_shot = now
            self.next_shot_delay = random.randint(3000, MAX_SHOOT_DELAY)

# Game loop
def main_game():
    global all_sprites, enemy_bullets
    clock = pygame.time.Clock()
    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    score = 0

    level = 1

    patterns = {
        "T": [(0, -40), (-40, -40), (40, -40), (0, 0), (0, 40)],
        "H": [(-40, -40), (-40, 0), (-40, 40), (40, -40), (40, 0), (40, 40), (0, 0)],
        "box": [(-40, -40), (0, -40), (40, -40), (-40, 0), (40, 0), (-40, 40), (0, 40), (40, 40)],
        "triangle": [(0, -40), (-30, 0), (30, 0), (-60, 40), (0, 40), (60, 40)],
        "circle": [(math.cos(a) * 50, math.sin(a) * 50) for a in [i * math.pi / 4 for i in range(8)]],
        "rhombus": [(0, -40), (-30, -20), (30, -20), (-60, 0), (0, 0), (60, 0), (-30, 20), (30, 20), (0, 40)]
    }

    def spawn_single_pattern(enemies_group, all_sprites_group, center_x):
        cy = HEIGHT // 3
        pattern_name = random.choice(list(patterns.keys()))
        pattern = patterns[pattern_name]
        spawned = 0
        for dx, dy in pattern:
            x = int(center_x + dx)
            y = int(cy + dy)
            if 40 <= x <= WIDTH - 40 and 20 <= y <= HEIGHT // 2:
                new_enemy = Enemy()
                new_enemy.rect.center = (x, y)
                if not pygame.sprite.spritecollideany(new_enemy, enemies_group):
                    enemies_group.add(new_enemy)
                    all_sprites_group.add(new_enemy)
                    spawned += 1
        return spawned

    def spawn_patterns(count):
        total_spawned = 0
        spacing = WIDTH // (count + 1)
        centers = [spacing * (i + 1) for i in range(count)]
        for cx in centers:
            total_spawned += spawn_single_pattern(enemies, all_sprites, cx)
        return total_spawned

    enemies_spawned = spawn_patterns(1)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()
        enemies.update()
        enemy_bullets.update()

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            if hits:
                bullet.kill()
                score += 10

        if pygame.sprite.spritecollide(player, enemy_bullets, False) or pygame.sprite.spritecollide(player, enemies, False):
            running = False

        if not enemies:
            level += 1
            if level > 10:
                enemies_spawned = spawn_patterns(3)
            elif level > 5:
                enemies_spawned = spawn_patterns(2)
            else:
                enemies_spawned = spawn_patterns(1)

        WIN.fill(BLACK)
        all_sprites.draw(WIN)

        score_text = FONT.render(f"Score: {score}", True, WHITE)
        level_text = FONT.render(f"Level: {level}", True, WHITE)
        WIN.blit(score_text, (10, 10))
        WIN.blit(level_text, (10, 50))

        pygame.display.update()

    return score

def main_menu():
    while True:
        WIN.fill(BLACK)
        title = FONT.render("Insert Cool Name Later", True, WHITE)
        play_text = FONT.render("[P] Play", True, WHITE)
        exit_text = FONT.render("[ESC] Exit", True, WHITE)

        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        WIN.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    score = main_game()
                    game_over(score)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_over(score):
    while True:
        WIN.fill(BLACK)
        over_text = FONT.render("Game Over", True, WHITE)
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        restart_text = FONT.render("[R] Restart", True, WHITE)
        exit_text = FONT.render("[ESC] Exit", True, WHITE)

        WIN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 40))
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Start the game
main_menu()
