import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()

# Player settings
player_width, player_height = 50, 20
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - 60
player_speed = 5

# Bullet settings
bullet_width, bullet_height = 5, 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width, enemy_height = 40, 30
enemy_rows = 3
enemy_cols = 8
enemy_padding = 10
enemy_speed = 3
enemies = []
enemy_direction = 1

# Create enemies
start_x = 50
start_y = 50
for row in range(enemy_rows):
    for col in range(enemy_cols):
        x = start_x + col * (enemy_width + enemy_padding)
        y = start_y + row * (enemy_height + enemy_padding)
        enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))


running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Update bullet positions
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Update enemy positions
    for enemy in enemies:
        enemy.x += enemy_speed * enemy_direction

    # Reverse direction and move enemies down if they hit screen edges
    if any(enemy.x + enemy_width >= WIDTH or enemy.x <= 0 for enemy in enemies):
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += enemy_height
    
    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()
sys.exit()