import pygame
import random
from pygame.constants import QUIT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

COLOR_PLAYER = (255, 255, 255)
SIZE_PLAYER = (20, 20)
COLOR_BG = (0,0,0)

main_display = pygame.display.set_mode((WIDTH,HEIGHT))

player = pygame.Surface(SIZE_PLAYER)
player.fill(COLOR_PLAYER)
player_rect = player.get_rect()
player_speed = [1, 1] # [speed_x, speed_y]

playing = True


while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
    main_display.fill(COLOR_BG)


    # X
    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_speed[0] = player_speed[0]*-1
    # Y
    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        player_speed[1] = player_speed[1]*-1

    # print("x = ", player_rect.centerx, "y = ", player_rect.centery)

    main_display.blit(player, player_rect)

    player_rect = player_rect.move(player_speed)

    pygame.display.flip()