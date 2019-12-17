import pygame
import math
import random
PI = math.pi


def rand_x():
    return random.randrange(WIDTH + 1)


def rand_y():
    return random.randrange(HEIGHT + 1)


def rand_ang(amp=(0, 2*PI)):
    return random.randrange(int(1000*amp[0]), int(1000*amp[1]))/1000


def set_level(level):
    asteroids = []
    for _ in range(level + 3):
        x, y = rand_x(), rand_y()
        asteroids.append({'x': x, 'y': y, 'ang': rand_ang(), 'type': big_ast,
                          'rect': big_ast.get_rect(bottomright=(x, y))})
    return asteroids


def start_screen():
    start_message = large_font.render('ASTEROIDS', True, (255, 255, 255))
    info_message = font.render('Press s to start.', True, (255, 255, 255))
    display.blit(start_message, start_message.get_rect(center=(WIDTH/2, HEIGHT/2 - 40)))
    display.blit(info_message, info_message.get_rect(center=(WIDTH/2, HEIGHT/2 + 40)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True

def game_over():
    over_message = large_font.render('GAME OVER', True, (255, 255, 255))
    info_message = font.render('Press q to quit or r to restart.', True, (255, 255, 255))
    display.blit(over_message, over_message.get_rect(center=(WIDTH/2, HEIGHT/2 - 40)))
    display.blit(info_message, info_message.get_rect(center=(WIDTH/2, HEIGHT/2 + 40)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_r:
                    return True

pygame.init()
WIDTH = 800
HEIGHT = 600
SHIP_WIDTH = 30
SHIP_HEIGHT = 20
display = pygame.display.set_mode((WIDTH, HEIGHT))
asteroid = pygame.image.load('asteroid.png')
n_ship = pygame.transform.scale(pygame.image.load('ship.png'), (SHIP_WIDTH, SHIP_HEIGHT))
f_ship = pygame.transform.scale(pygame.image.load('ship_firing.png'), (SHIP_WIDTH, SHIP_HEIGHT))
big_ast = pygame.transform.scale(asteroid, (105, 100))
med_ast = pygame.transform.scale(asteroid, (53, 50))
small_ast = pygame.transform.scale(asteroid, (26, 25))
ship = n_ship
rot_ship = ship
bullet = pygame.transform.scale(pygame.image.load('bullet.png'), (5, 5))
pygame.display.set_icon(small_ast)

'''
class Jogador:
    vel_x = 0
    vel_y = 0
    lives = 2

    def f(self):
        self.vel_x
        return

jogador1 = Jogador()
jogador1.f()
jogadores = [jogador1, jogador2]
'''

HYPERSPACE = 24
NEW_LEVEL = 25
NEW_TRY = 26
GAME_OVER = 27
ANG_VEL = 0.3
ACCEL = 0.008
MAX_VEL = 0.4
FRICTION = 0.05
AST_VEL = 0.1
BULLET_VEL = 0.3
ship_x, ship_y = WIDTH/2, HEIGHT/2
vel_x, vel_y = 0, 0
angle = 90
bullets = []
bullet_max = 350
level = 1
score = 0
lives = 3
asteroids = set_level(level)
changing = False
ship_vis = True
clock = pygame.time.Clock()
font_list = 'Corbel, Courier 10 Pitc, FreeMono, Garuda'
font = pygame.font.SysFont(font_list, 30, bold=True, italic=False)
large_font = pygame.font.SysFont(font_list, 60, bold=True, italic=False)
running = start_screen()

while running:
    dt = clock.tick(30)
    pygame.display.set_caption('FPS: ' + str(clock.get_fps()))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        angle += ANG_VEL * dt
    if keys[pygame.K_RIGHT]:
        angle -= ANG_VEL * dt
    if keys[pygame.K_UP]:
        vel_x += ACCEL * math.cos(PI*angle/180) * dt
        vel_y += ACCEL * math.sin(PI*angle/180) * dt
        ship = f_ship
    else:
        ship = n_ship


    if vel_x > 0:
        vel_x = max(0, vel_x - FRICTION)
    if vel_x < 0:
        vel_x = min(0, vel_x + FRICTION)
    if vel_y > 0:
        vel_y = max(0, vel_y - FRICTION)
    if vel_y < 0:
        vel_y = min(0, vel_y + FRICTION)
    vel_x = min(vel_x, MAX_VEL*dt)
    vel_x = max(vel_x, -MAX_VEL*dt)
    vel_y = min(vel_y, MAX_VEL*dt)
    vel_y = max(vel_y, -MAX_VEL*dt)
#    if vel_x != 0:
#        vel_ang = math.atan(vel_y/vel_x)
#    elif vel_y > 0:
#        vel_ang = PI/2
#    elif vel_y < 0:
#        vel_ang = -PI/2
#    vel_x = min(vel_x, MAX_VEL*dt * math.cos(vel_ang))
#    vel_x = max(vel_x, -MAX_VEL*dt * math.cos(vel_ang))
#    vel_y = min(vel_y, MAX_VEL*dt * math.sin(vel_ang))
#    vel_y = max(vel_y, -MAX_VEL*dt * math.sin(vel_ang))

    ship_x = (ship_x + vel_x) % (WIDTH + SHIP_WIDTH)
    ship_y = (ship_y - vel_y) % (HEIGHT + SHIP_HEIGHT)
    bull_index = -1
    ast_index = -1
    color = (0, 255, 0)
    ship_rect = rot_ship.get_rect(center=(ship_x-SHIP_WIDTH/2, ship_y-SHIP_HEIGHT/2))

    for bull in bullets:
        bull_index += 1
        if bull['d'] > bullet_max:
            del bullets[bull_index]
            break
        bull['x'] = (bull['x'] + BULLET_VEL*dt * math.cos(PI*bull['ang']/180)) % WIDTH
        bull['y'] = (bull['y'] - BULLET_VEL*dt * math.sin(PI*bull['ang']/180)) % HEIGHT
        bull['d'] += BULLET_VEL*dt
        bull['rect'] = bullet.get_rect(topleft=(bull['x'], bull['y']))

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == HYPERSPACE:
            ship_vis = True
            ship_x, ship_y = rand_x(), rand_y()
            vel_x, vel_y = 0, 0
            pygame.time.set_timer(HYPERSPACE, 0)
        if event.type == NEW_LEVEL:
            changing = False
            asteroids = set_level(level)
            pygame.time.set_timer(NEW_LEVEL, 0)
        if event.type == NEW_TRY:
            changing = False
            ship_vis = True
            ship_x, ship_y = WIDTH/2, HEIGHT/2
            vel_x, vel_y = 0, 0
            angle = 90
            pygame.time.set_timer(NEW_TRY, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(bullets) < 4 and ship_vis:
                    x = ship_x - SHIP_WIDTH/2 - bullet.get_width()/2 + SHIP_HEIGHT*math.cos(PI*angle/180)
                    y = ship_y - SHIP_HEIGHT/2 - bullet.get_height()/2 - SHIP_HEIGHT*math.sin(PI*angle/180)
                    bullets.append({'x': x, 'y': y, 'ang': angle, 'd': 0,
                                    'rect': bullet.get_rect(topleft=(x, y))})
            if event.key == pygame.K_DOWN:
                if ship_vis:
                    ship_vis = False
                    pygame.time.set_timer(HYPERSPACE, 1000)

    for ast in asteroids:
        ast_index += 1
        ast['x'] = (ast['x'] + AST_VEL*dt * math.cos(ast['ang'])) % (WIDTH + ast['type'].get_width())
        ast['y'] = (ast['y'] - AST_VEL*dt * math.sin(ast['ang'])) % (HEIGHT + ast['type'].get_height())
        ast['rect'] = ast['type'].get_rect(bottomright=(ast['x'], ast['y']))
        bull_coll = ast['rect'].collidelist([bull['rect'] for bull in bullets])
        ship_coll = ast['rect'].colliderect(ship_rect)
        if bull_coll > -1:
            if ast['type'] != small_ast:
                if ast['type'] == big_ast:
                    new_type = med_ast
                    score += 20
                else:
                    new_type = small_ast
                    score += 50
                asteroids.append({'x': ast['x'], 'y': ast['y'],
                                  'ang': rand_ang(amp=(ast['ang']-0.75, ast['ang']+0.75)),
                                  'type': new_type,
                                  'rect': new_type.get_rect(bottomright=(ast['x'], ast['y']))})
                asteroids.append({'x': ast['x'], 'y': ast['y'],
                                  'ang': rand_ang(amp=(ast['ang']-0.75, ast['ang']+0.75)),
                                  'type': new_type,
                                  'rect': new_type.get_rect(bottomright=(ast['x'], ast['y']))})
            else:
                score += 100
            del asteroids[ast_index]
            del bullets[bull_coll]
        if ship_coll and not changing and ship_vis:
            color = (255, 0, 0)
            lives -= 1
            if lives > 0:
                changing = True
                ship_vis = False
                pygame.time.set_timer(NEW_TRY, 2000)

    if len(asteroids) == 0 and not changing:
        changing = True
        level += 1
        pygame.time.set_timer(NEW_LEVEL, 2000)

    rot_ship = pygame.transform.rotate(ship, angle)
    dw = rot_ship.get_width() - SHIP_WIDTH
    dh = rot_ship.get_height() - SHIP_HEIGHT
    display.fill((0, 0, 0))
    for bull in bullets:
        display.blit(bullet, (bull['x'], bull['y']))
#        pygame.draw.rect(display, (0, 255, 0), bull['rect'], 1)
    for ast in asteroids:
        display.blit(ast['type'], (ast['x'] - ast['type'].get_width(), ast['y'] - ast['type'].get_height()))
#        pygame.draw.rect(display, (0, 255, 0), ast['rect'], 3)
    if ship_vis:
        display.blit(rot_ship, (ship_x-dw/2 - SHIP_WIDTH, ship_y-dh/2 - SHIP_HEIGHT))
#    pygame.draw.circle(display, (0, 255, 0), (int(ship_x-SHIP_WIDTH/2), int(ship_y-SHIP_HEIGHT/2)), 2)
#    pygame.draw.rect(display, color, ship_rect, 3)

#    display.blit(big_ast, (0, 0))
#    display.blit(med_ast, (105, 0))
#    display.blit(small_ast, (158, 0))
    display.blit(font.render('Level: ' + str(level), True, (255, 255, 255)), (10, 10))
    display.blit(font.render('Score: ' + str(score), True, (255, 255, 255)), (10, 40))
    display.blit(font.render('Lives: ' + str(lives), True, (255, 255, 255)), (10, 70))
    if lives == 0:
        running = game_over()
        score = 0
        lives = 3
        level = 1
        ship_x, ship_y = WIDTH/2, HEIGHT/2
        vel_x, vel_y = 0, 0
        angle = 90
        asteroids = set_level(level)
    pygame.display.flip()
pygame.quit()