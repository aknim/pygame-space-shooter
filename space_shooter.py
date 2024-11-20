import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()

player_width, player_height = 50, 20
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - 60
player_speed = 5

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    pygame.display.flip()
    clock.tick(60) # Limit to 60 FPS

pygame.quit()
sys.exit()