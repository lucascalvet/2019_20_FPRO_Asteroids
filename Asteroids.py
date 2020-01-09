import pygame
import math
import random
PI = math.pi


def rand_x():  # returns a random x coordinate within the game display
    return random.randrange(WIDTH + 1)


def rand_y():  # returns a random y coordinate within the game display
    return random.randrange(HEIGHT + 1)


def rand_ang(amp=(0, 2*PI)):  # returns a random angle (amplitude can be set)
    return random.randrange(int(1000*amp[0]), int(1000*amp[1]))/1000


def set_level(level):  # generates a new level and returns the asteroids list
    asteroids = []
    for _ in range(level + 3):
        x, y = rand_x(), rand_y()
        rect = pygame.Rect(0, 0, 0, 0)
        rect.size = (80, 80)
        rect.center = big_ast.get_rect(bottomright=(x, y)).center
        asteroids.append({'x': x, 'y': y, 'ang': rand_ang(), 'type': big_ast,
                          'rect': rect})
    return asteroids


def break_ast(asteroids, ast_del, score):
    # 'break' the asteroids from ast_del and return the new
    # asteroids list and the new score
    new_ast = []
    for ast in ast_del[::-1]:
        new_ast.append(asteroids[ast])
        del asteroids[ast]
    for ast in new_ast:
        if ast['type'] != small_ast:
            if ast['type'] == big_ast:
                new_type = med_ast
                score += 20
            else:
                new_type = small_ast
                score += 50
            asteroids.append({'x': ast['x'], 'y': ast['y'],
                              'ang': rand_ang(amp=(ast['ang']-1.3, ast['ang']+1.3)),
                              'type': new_type,
                              'rect': new_type.get_rect(bottomright=(ast['x'], ast['y']))})
            asteroids.append({'x': ast['x'], 'y': ast['y'],
                              'ang': rand_ang(amp=(ast['ang']-1.3, ast['ang']+1.3)),
                              'type': new_type,
                              'rect': new_type.get_rect(bottomright=(ast['x'], ast['y']))})
        else:
            score += 100
    return asteroids, score


def start_screen():  # displays a start screen and returns the 'running' value
    start_sound.play()
    start_message = pygame.font.SysFont(font_list, 100, bold=True, italic=False).render('ASTEROIDS', True, (255, 255, 255))
    info_message = font.render('Press s to start.', True, (255, 255, 255))  
    display.blit(start_message, start_message.get_rect(center=(WIDTH/2, HEIGHT/2 - 40)))
    display.blit(info_message, info_message.get_rect(center=(WIDTH/2, HEIGHT/2 + 40)))
    display.blit(instructions, instructions.get_rect(midbottom=(WIDTH/2, HEIGHT - 20)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_sound.stop()
                    return True


def pause():  # displays a pause screen and returns the 'running' value
    pygame.mixer.stop()
    pause_message = large_font.render('PAUSE', True, (255, 255, 255))
    info_message = font.render('Press q to quit or p to continue.', True, (255, 255, 255))
    display.blit(bg ,(0,0))
    display.blit(pause_message, pause_message.get_rect(center=(WIDTH/2, HEIGHT/2 - 40)))
    display.blit(info_message, info_message.get_rect(center=(WIDTH/2, HEIGHT/2 + 40)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_p:
                    return True


def game_over():  # displays a game over screen and returns the 'running' value
    pygame.mixer.stop()
    over_sound.play()
    over_message = large_font.render('GAME OVER', True, (255, 255, 255))
    info_message = font.render('Press q to quit or r to restart.', True, (255, 255, 255))
    display.blit(bg ,(0,0))
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
                    over_sound.stop()
                    return True

pygame.init()
WIDTH = 800
HEIGHT = 600
SHIP_WIDTH = 30
SHIP_HEIGHT = 20
# load assets
instructions = pygame.image.load('instructions.png')
asteroid = pygame.image.load('asteroid.png')
n_ship = pygame.transform.scale(pygame.image.load('ship.png'), (SHIP_WIDTH, SHIP_HEIGHT))
f_ship = pygame.transform.scale(pygame.image.load('ship_firing.png'), (SHIP_WIDTH, SHIP_HEIGHT))
big_ast = pygame.transform.scale(asteroid, (105, 100))
med_ast = pygame.transform.scale(asteroid, (53, 50))
small_ast = pygame.transform.scale(asteroid, (26, 25))
ship = n_ship
rot_ship = ship
bullet = pygame.transform.scale(pygame.image.load('bullet.png'), (6, 6))
bullet_sound = pygame.mixer.Sound('bullet.ogg')
exp1_sound = pygame.mixer.Sound('explosion1.ogg')
exp2_sound = pygame.mixer.Sound('explosion2.ogg')
over_sound = pygame.mixer.Sound('over.ogg')
start_sound = pygame.mixer.Sound('start.ogg')
thruster_sound = pygame.mixer.Sound('thruster.ogg')
start_lvl_sound = pygame.mixer.Sound('start_level.ogg')
new_life_sound = pygame.mixer.Sound('new_life.ogg')
font_list = 'Corbel, Courier 10 Pitc, FreeMono, Garuda'
font = pygame.font.SysFont(font_list, 30, bold=True, italic=False)
large_font = pygame.font.SysFont(font_list, 60, bold=True, italic=False)
# set USEREVENT codes
HYPERSPACE = 24
NEW_LEVEL = 25
NEW_TRY = 26
PROTECTION = 27
# set constants
ANG_VEL = 0.3
ACCEL = 0.008
MAX_VEL = 0.4
FRICTION = 0.05
AST_VEL = 0.1
BULLET_VEL = 0.3
# set inicial values
ship_x, ship_y = WIDTH/2, HEIGHT/2
vel_x, vel_y = 0, 0
angle = 90
bullets = []
bullet_max = 350
level = 1
score = 0
prev_score = 0
lives = 3
t_blink = 0
changing = True
ship_vis = True
protected = True
paused = False
stars = [(rand_x(), rand_y()) for _ in range(100)]
# window configuration
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(big_ast)
pygame.display.set_caption('Asteroids')
bg = pygame.Surface((WIDTH, HEIGHT))
bg.set_alpha(150)
bg.fill((0, 0, 0))

running = start_screen()  # show the start screen
clock = pygame.time.Clock()  # initialize the clock
pygame.event.post(pygame.event.Event(NEW_LEVEL))  # start the level

while running:
    dt = clock.tick(30)  # factor for adjusting the framerate
    if paused:
        dt = 30  # reset dt if the game was paused in the previous loop
        paused = False
    if not pygame.display.get_active():
        running = pause()
        paused = True
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == PROTECTION:
            ship_vis = not ship_vis
            t_blink += 1
            if t_blink == 6:
                pygame.time.set_timer(PROTECTION, 0)
                t_blink = 0
                changing = False
        if event.type == HYPERSPACE:
            ship_vis = True
            ship_x, ship_y = rand_x(), rand_y()
            vel_x, vel_y = 0, 0
            pygame.time.set_timer(HYPERSPACE, 0)
        if event.type == NEW_LEVEL:
            start_lvl_sound.play()
            ship_vis = True
            pygame.time.set_timer(PROTECTION, 300)
            asteroids = set_level(level)
            pygame.time.set_timer(NEW_LEVEL, 0)
        if event.type == NEW_TRY:
            if len(asteroids) == 0:
                start_lvl_sound.play()
                level += 1
                asteroids = set_level(level)
            pygame.time.set_timer(PROTECTION, 300)
            ship_vis = True
            ship_x, ship_y = WIDTH/2, HEIGHT/2
            vel_x, vel_y = 0, 0
            angle = 90
            pygame.time.set_timer(NEW_TRY, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # shoot bullet
                if len(bullets) < 4 and ship_vis and not changing:
                    bullet_sound.play()
                    x = ship_x - SHIP_WIDTH/2 - bullet.get_width()/2 + SHIP_HEIGHT*math.cos(PI*angle/180)
                    y = ship_y - SHIP_HEIGHT/2 - bullet.get_height()/2 - SHIP_HEIGHT*math.sin(PI*angle/180)
                    bullets.append({'x': x, 'y': y, 'ang': angle, 'd': 0,
                                    'rect': bullet.get_rect(topleft=(x, y))})
            if event.key == pygame.K_DOWN:  # spawn the ship in a random position
                if ship_vis and not changing:
                    ship_vis = False
                    pygame.time.set_timer(HYPERSPACE, 1000)
            if event.key == pygame.K_UP:
                thruster_sound.stop()
                thruster_sound.play()
            if event.key == pygame.K_q:  # quit the game
                running = False
            if event.key == pygame.K_p:  # pause the game
                running = pause()
                paused = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                thruster_sound.fadeout(500)    
        if event.type == pygame.ACTIVEEVENT:
            if event.state == 2 and event.gain == 0:
                running = pause()
                paused = True
#    pygame.display.set_caption('FPS: ' + str(clock.get_fps()))
    # monitor the left, right and up keys
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
    # apply friction to the ship
    if vel_x > 0:
        vel_x = max(0, vel_x - FRICTION)
    if vel_x < 0:
        vel_x = min(0, vel_x + FRICTION)
    if vel_y > 0:
        vel_y = max(0, vel_y - FRICTION)
    if vel_y < 0:
        vel_y = min(0, vel_y + FRICTION)
    # set a maximum velocity to the ship
    vel_x = min(vel_x, MAX_VEL*dt)
    vel_x = max(vel_x, -MAX_VEL*dt)
    vel_y = min(vel_y, MAX_VEL*dt)
    vel_y = max(vel_y, -MAX_VEL*dt)
    # update ship position
    ship_x = (ship_x + vel_x) % (WIDTH + SHIP_WIDTH)
    ship_y = (ship_y - vel_y) % (HEIGHT + SHIP_HEIGHT)
    # update bullets position and delete the ones that have reached the maximum distance
    bull_index = -1
    bull_del = []  # list of bullets indexes to be deleted
    for bull in bullets:
        bull_index += 1
        if bull['d'] > bullet_max:
            bull_del.append(bull_index)
        bull['x'] = (bull['x'] + BULLET_VEL*dt * math.cos(PI*bull['ang']/180)) % WIDTH
        bull['y'] = (bull['y'] - BULLET_VEL*dt * math.sin(PI*bull['ang']/180)) % HEIGHT
        bull['d'] += BULLET_VEL*dt
        bull['rect'] = bullet.get_rect(topleft=(bull['x'], bull['y']))
    for bull in bull_del[::-1]:
        del bullets[bull]
    # handle collisions with asteroids (from both bullets and the ship)
    ship_rect = rot_ship.get_rect(center=(ship_x-SHIP_WIDTH/2, ship_y-SHIP_HEIGHT/2))
    ast_index = -1
    ast_del = []  # list of asteroids indexes to be deleted
    for ast in asteroids:
        ast_index += 1
        ast['x'] = (ast['x'] + AST_VEL*dt * math.cos(ast['ang'])) % (WIDTH + ast['type'].get_width())
        ast['y'] = (ast['y'] - AST_VEL*dt * math.sin(ast['ang'])) % (HEIGHT + ast['type'].get_height())
        ast['rect'].center=(ast['x'] - ast['type'].get_width()/2, ast['y'] - ast['type'].get_height()/2)
        bull_coll = ast['rect'].collidelist([bull['rect'] for bull in bullets])
        ship_coll = ast['rect'].colliderect(ship_rect)
        if bull_coll > -1:
            exp1_sound.play()
            ast_del.append(ast_index)
            del bullets[bull_coll]
            break
        if ship_coll and not changing and ship_vis:
            exp2_sound.play()
            lives -= 1
            ast_del.append(ast_index)
            if lives > 0:
                changing = True
                ship_vis = False
                pygame.time.set_timer(NEW_TRY, 2000)
            break
    if len(ast_del) != 0:
        prev_score = score
        asteroids, score = break_ast(asteroids, ast_del, score)
        if prev_score//10000 != score//10000:
            new_life_sound.play()
            lives += 1
    # start a new level when there are no asteroids
    if len(asteroids) == 0 and not changing and lives > 0:
        changing = True
        level += 1
        pygame.time.set_timer(NEW_LEVEL, 2000)
    # render every thing on the screen
    rot_ship = pygame.transform.rotate(ship, angle)
    dw = rot_ship.get_width() - SHIP_WIDTH
    dh = rot_ship.get_height() - SHIP_HEIGHT
    display.fill((0, 0, 0))
    for star in stars:
        pygame.draw.circle(display, (180, 180, 180), (star[0], star[1]), 2)
    for bull in bullets:
        display.blit(bullet, (bull['x'], bull['y']))
    for ast in asteroids:
        display.blit(ast['type'], (ast['x'] - ast['type'].get_width(), ast['y'] - ast['type'].get_height()))
    if ship_vis:
        display.blit(rot_ship, (ship_x-dw/2 - SHIP_WIDTH, ship_y-dh/2 - SHIP_HEIGHT))
    display.blit(font.render('Level: ' + str(level), True, (255, 255, 255)), (10, 10))
    display.blit(font.render('Score: ' + str(score), True, (255, 255, 255)), (10, 40))
    display.blit(font.render('Lives: ' + str(lives), True, (255, 255, 255)), (10, 70))
    pygame.display.flip()
    # if there are no lives left, display the game over screen
    if lives == 0:
        running = game_over()
        score = 0
        lives = 3
        level = 1
        ship_x, ship_y = WIDTH/2, HEIGHT/2
        vel_x, vel_y = 0, 0
        angle = 90
        changing = True
        ship_vis = True
        pygame.event.post(pygame.event.Event(NEW_LEVEL))
pygame.quit()
