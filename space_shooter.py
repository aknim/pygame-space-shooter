import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)

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
enemy_padding = 10
enemy_speed = 3
enemies = []
enemy_direction = 1
enemy_bullets = []
enemy_bullet_speed = 5

score = 0
level = 1
lives = 3

# Create enemies
def create_enemies(rows, cols, speed):
    global enemies, enemy_speed
    start_x = 50
    start_y = 50
    enemies = []
    enemy_speed = speed
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (enemy_width + enemy_padding)
            y = start_y + row * (enemy_height + enemy_padding)
            enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

# End screen
def display_end_screen(message):
    while True:
        screen.fill(BLACK)
        text = large_font.render(message, True, GREEN)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Restart
                    main_game()
                if event.key == pygame.K_q: # Quit
                    pygame.quit()
                    sys.exit()

def main_game():
    global player_x, bullets, enemies, enemy_bullets, score, level, lives, enemy_direction

    player_x = (WIDTH - player_width) // 2
    bullets = []
    enemy_bullets = []
    score = 0
    level = 1
    lives = 3
    enemy_direction = 1
    create_enemies(3, 8, enemy_speed)

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
                    score +=10
                    break

        # Check if all enemies are destroyed
        if not enemies:
            level += 1
            if level > 2: # End game at level 2
                display_end_screen("Victory!")
            create_enemies(3 + level, 8, enemy_speed + level // 2) # More rows, greater speeds

        # Enemy shooting
        if random.randint(0, 100) < 2: # Small chance per frame
            shooting_enemy = random.choice(enemies)
            enemy_bullet_x = shooting_enemy.x + enemy_width // 2 - bullet_width // 2
            enemy_bullet_y = shooting_enemy.y + enemy_height
            enemy_bullets.append(pygame.Rect(enemy_bullet_x, enemy_bullet_y, bullet_width, bullet_height))

        # Update enemy bullet positions
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.y += enemy_bullet_speed
            if enemy_bullet.y > HEIGHT:
                enemy_bullets.remove(enemy_bullet)
            elif enemy_bullet.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                enemy_bullets.remove(enemy_bullet)
                lives -= 1 
                if lives == 0:
                    display_end_screen("Game Over")

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Draw enemy bullets
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(screen, YELLOW, enemy_bullet)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

        # Display score
        score_text = font.render(f"Score: {score} Level: {level} Lives: {lives}", True, GREEN)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS

main_game()