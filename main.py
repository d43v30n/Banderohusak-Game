import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_LEFT, K_UP, K_RIGHT, K_ESCAPE

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Arial', 20)

COLOR_PLAYER = (255, 255, 255)
COLOR_ENEMY = (255, 0, 0)
COLOR_BONUS = (0, 255, 0)
SIZE_PLAYER = (20, 20)
SIZE_ENEMY = (60, 30)
SIZE_BONUS = (40,100)
COLOR_BG = (0,0,0)

main_display = pygame.display.set_mode((WIDTH,HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), 
                            (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

player = pygame.image.load('player.png').convert_alpha() #pygame.Surface(SIZE_PLAYER)
player_rect = player.get_rect()

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_move_right = [4, 0]


class EnemyClass:
    def init(self):
        self.event = pygame.USEREVENT +1
        pygame.time.set_timer(self.event, 1500)
        self.count = []
        pass

    def create_enemy(self):
        fenemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (SIZE_ENEMY))
        fenemy_rect = pygame.Rect(WIDTH, random.randint((HEIGHT / 4), (3*HEIGHT/4)), *SIZE_ENEMY)
        fenemy_move = [random.randint(-8, -4), 0]
        return [fenemy, fenemy_rect, fenemy_move]

class BonusClass:
    def init(self):
        self.event = pygame.USEREVENT +2
        pygame.time.set_timer(self.event, 3000)
        self.count = []
        pass
        
    def create_bonus(self):
        bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (SIZE_BONUS))
        bonus_rect = pygame.Rect(random.randint((WIDTH / 4), (3*WIDTH/4)), 0, *SIZE_BONUS)
        bonus_move = [0, random.randint(4, 8)]
        return [bonus, bonus_rect, bonus_move]
    
score = 0

playing = True

freshenemy = EnemyClass()
freshbonus = BonusClass()

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT: playing = False
        if event.type == freshenemy.event: 
            freshenemy.count.append(freshenemy.create_enemy())
        if event.type == freshbonus.event: 
            freshbonus.count.append(freshbonus.create_bonus())

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom <= HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > -1:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left > -1:
        player_rect = player_rect.move(player_move_left)
    if keys[K_RIGHT] and player_rect.right <= WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()
    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    for enemy in freshenemy.count:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]): playing = False

    for bonus in freshbonus.count:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        if player_rect.colliderect(bonus[1]): 
            score += 1
            freshbonus.count.pop(freshbonus.count.index(bonus))

    main_display.blit(player, player_rect)
    main_display.blit(FONT.render(str(score), True, COLOR_PLAYER), (WIDTH-50, 20))

    for penemy in freshenemy.count:
        if penemy[1].left < 0:
            freshenemy.count.pop(freshenemy.count.index(penemy))
    for pbonus in freshbonus.count:
        if pbonus[1].bottom > HEIGHT:
            freshbonus.count.pop(freshbonus.count.index(pbonus))

    if keys[K_ESCAPE]: break
    pygame.display.flip()