import pygame
import random

pygame.init()

WIDTH = 700
HEIGHT = 500

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('mogank')

WHITE = (225, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

hero = pygame.image.load('hero.png')
hero = pygame.transform.scale(hero,  (50, 50))

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

enemy_size = 50
enemy_pos = [random.randint(0, 750,), 0]
enemy_list = [enemy_pos]


SPEED = 10

font = pygame.font.SysFont('monospace', 75)

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, 600)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(WIN, RED,(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True

def show_game_over_screen():
    WIN.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    WIN.blit(game_over_text,
             (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        show_game_over_screen()
        game_over = False
        player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
        enemy_list = [enemy_pos]
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= SPEED
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += SPEED
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= SPEED
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += SPEED

    WIN.fill(BLACK)

    drop_enemies(enemy_list)
    update_enemy_positions(enemy_list)


    if collision_check(enemy_list, player_pos):
        game_over = True

    draw_enemies(enemy_list)
    #pygame.draw.rect(WIN, WHITE, (player_pos[0], player_pos[1], player_size, player_size))
    WIN.blit(hero, (player_pos[0], player_pos[1]))
    clock.tick(30)
    pygame.display.update()


pygame.quit()
