import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Target Shooting with Placeholders")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SKY = (135, 206, 235)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
gunsound=pygame.mixer.Sound("gunshot.mp3")
gunsound.set_volume(0.5)

# Placeholder gun: blue rectangle
gun_img = pygame.image.load("sniper.png")
gun_img=pygame.transform.scale(gun_img,(100,100))
screen.blit(gun_img,(100,100))
# Placeholder target: red square
target_img = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.rect(target_img, RED, target_img.get_rect())

# Player gun position (fixed at bottom center)
gun_pos = (WIDTH // 2, HEIGHT - 60)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.original_image = pygame.Surface((10, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, WHITE, (0, 0, 10, 4))
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle_rad = math.radians(angle)
        self.speed = 15

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle_rad)
        self.rect.y -= self.speed * math.sin(self.angle_rad)
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()

# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = target_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)
        self.speed = random.uniform(1.5, 3.5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()

# Spawn initial targets
for _ in range(7):
    t = Target()
    all_sprites.add(t)
    targets.add(t)

# Score and lives
score = 0
lives = 3
font = pygame.font.SysFont(None, 36)
cloud_x=0
# Game loop
running = True
while running:
    clock.tick(20)  # 60 FPS
    
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - gun_pos[0]
            dy = gun_pos[1] - mouse_y
            angle = math.degrees(math.atan2(dy, dx))
            bullet = Bullet(gun_pos[0], gun_pos[1], angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
            gunsound.play()

    # Update sprites
    all_sprites.update()

    # Spawn new targets occasionally to keep 7 on screen max
    if len(targets) < 7 and random.random() < 0.02:
        t = Target()
        all_sprites.add(t)
        targets.add(t)

    # Check collisions: bullets hitting targets
    hits = pygame.sprite.groupcollide(targets, bullets, True, True)
    for hit in hits:
        score += 10
        # Spawn a new target for every one destroyed
        t = Target()
        all_sprites.add(t)
        targets.add(t)

    # Check if targets reach bottom (lose life)
    for target in targets:
        if target.rect.bottom >= HEIGHT - 50:
            lives -= 1
            target.kill()
            if lives <= 0:
                print(f"Game Over! Final Score: {score}")
                running = False

    

    # Rotate gun to point at mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - gun_pos[0]
    dy = gun_pos[1] - mouse_y
    angle = math.degrees(math.atan2(dy, dx))
    rotated_gun = pygame.transform.rotate(gun_img, angle)
    gun_rect = rotated_gun.get_rect(center=gun_pos)
    screen.blit(rotated_gun, gun_rect)

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.flip()
    screen.fill(SKY)

    # Sun
    pygame.draw.circle(screen, YELLOW, (70, 70), 30)

    # Static cloud
    pygame.draw.circle(screen, WHITE, (170, 80), 20)
    pygame.draw.circle(screen, WHITE, (140, 70), 25)
    pygame.draw.circle(screen, WHITE, (160, 80), 20)

    # Moving cloud
    pygame.draw.circle(screen, WHITE, (cloud_x + 300, 120), 20)
    pygame.draw.circle(screen, WHITE, (cloud_x + 320, 110), 25)
    pygame.draw.circle(screen, WHITE, (cloud_x + 340, 120), 20)

    cloud_x += 1
    if cloud_x > 600:
        cloud_x = 0

    # Ground
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 50, WIDTH, 50))
pygame.quit()
sys.exit()