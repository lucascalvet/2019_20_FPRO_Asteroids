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


VEL_ANG = 0.3
ACCEL = 0.007
MAX_VEL = 0.4
FRICTION = 0.05
AST_VEL = 0.1
BULLET_VEL = 0.3
ship_x = 400
ship_y = 300
vel_x = 0
vel_y = 0
angle = 90
bullets = []
bullet_max = 500
asteroids = [{'x': rand_x(), 'y': rand_y(), 'ang': rand_ang(), 'type': big_ast} for i in range(4)]
running = True
ship_vis = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(30)
    pygame.display.set_caption('FPS: ' + str(clock.get_fps()))
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        angle += VEL_ANG * dt
    if keys[pygame.K_RIGHT]:
        angle -= VEL_ANG * dt
    if keys[pygame.K_UP]:
        vel_x += ACCEL * math.cos(PI*angle/180) * dt
        vel_y += ACCEL * math.sin(PI*angle/180) * dt
        ship = f_ship
    else:
        ship = n_ship
#    if keys[pygame.K_DOWN]:
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

    ship_x = (ship_x + vel_x) % (WIDTH + SHIP_WIDTH)
    ship_y = (ship_y - vel_y) % (HEIGHT + SHIP_HEIGHT)
    bull_index = -1
    ast_index = -1
    color = (0, 255, 0)
    ship_rect = rot_ship.get_rect(center=(ship_x-SHIP_WIDTH/2, ship_y-SHIP_HEIGHT/2))
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
                else:
                    new_type = small_ast
                asteroids.append({'x': ast['x'], 'y': ast['y'],
                                  'ang': rand_ang(amp=(ast['ang']-0.75, ast['ang']+0.75)),
                                  'type': new_type})
                asteroids.append({'x': ast['x'], 'y': ast['y'],
                                  'ang': rand_ang(amp=(ast['ang']-0.75, ast['ang']+0.75)),
                                  'type': new_type})
            del asteroids[ast_index]
            del bullets[bull_coll]
        if ship_coll:
            color = (255, 0, 0)
#            running = False

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
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            ship_vis = True
            ship_x, ship_y = rand_x(), rand_y()
            vel_x, vel_y = 0, 0
            pygame.time.set_timer(pygame.USEREVENT, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(bullets) < 4:
                    x = ship_x - SHIP_WIDTH/2 - bullet.get_width()/2 + SHIP_HEIGHT*math.cos(PI*angle/180)
                    y = ship_y - SHIP_HEIGHT/2 - bullet.get_height()/2 - SHIP_HEIGHT*math.sin(PI*angle/180)
                    bullets.append({'x': x, 'y': y, 'ang': angle, 'd': 0,
                                    'rect': bullet.get_rect(topleft=(x, y))})
            if event.key == pygame.K_DOWN:
                ship_vis = False
                pygame.time.set_timer(pygame.USEREVENT, 1000)
    if len(asteroids) == 0:
        running = False
    rot_ship = pygame.transform.rotate(ship, angle)
    dw = rot_ship.get_width() - SHIP_WIDTH
    dh = rot_ship.get_height() - SHIP_HEIGHT
    display.fill((0, 0, 0))
    for bull in bullets:
        display.blit(bullet, (bull['x'], bull['y']))
#        pygame.draw.rect(display, (0, 255, 0), bull['rect'], 1)
    if ship_vis:
        display.blit(rot_ship, (ship_x-dw/2 - SHIP_WIDTH, ship_y-dh/2 - SHIP_HEIGHT))
    pygame.draw.circle(display, (0, 255, 0), (int(ship_x-SHIP_WIDTH/2), int(ship_y-SHIP_HEIGHT/2)), 2)
    for ast in asteroids:
        display.blit(ast['type'], (ast['x'] - ast['type'].get_width(), ast['y'] - ast['type'].get_height()))
    pygame.draw.rect(display, color, ship_rect, 3)
#        pygame.draw.rect(display, (0, 255, 0), ast['rect'], 3)
#    display.blit(big_ast, (0, 0))
#    display.blit(med_ast, (105, 0))
#    display.blit(small_ast, (158, 0))
    pygame.display.flip()
pygame.quit()