import pygame
import math

pygame.init()
WIDTH = 800
HEIGHT = 600
display = pygame.display.set_mode((WIDTH, HEIGHT))
asteroid = pygame.image.load('asteroid.png')
blueship = pygame.image.load('ship.png')
big_ast = pygame.transform.scale(asteroid, (105, 100))
med_ast = pygame.transform.scale(asteroid, (53, 50))
small_ast = pygame.transform.scale(asteroid, (26, 25))
ship = pygame.transform.scale(blueship, (30, 20))
bullet = pygame.transform.scale(pygame.image.load('bullet.png'), (5, 5))

ship_x = 400
ship_y = 300
angle = 90
bullet_angle = 0
bullet_x = ship_x - bullet.get_width()/2 + 13 * math.cos(math.pi*angle/180)
bullet_y = ship_y - bullet.get_height()/2 -  13 * math.sin(math.pi*angle/180)
vel_x = 0
vel_y = 0
bullet_vel = 0
VEL_ANG = 0.5
ACCEL = 0.01
FRICTION = 0.05

running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(30)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle += VEL_ANG * dt
    if keys[pygame.K_RIGHT]:
        angle -= VEL_ANG * dt
    if keys[pygame.K_UP]:
        vel_x += ACCEL * math.cos(math.pi*angle/180) * dt
        vel_y += ACCEL * math.sin(math.pi*angle/180) * dt
#    if keys[pygame.K_DOWN]:
    if vel_x > 0:
        vel_x = max(0, vel_x - FRICTION)
    if vel_x < 0:
        vel_x = min(0, vel_x + FRICTION)
    if vel_y > 0:
        vel_y = max(0, vel_y - FRICTION)
    if vel_y < 0:
        vel_y = min(0, vel_y + FRICTION)
    vel_x = min(vel_x, 0.5*dt)
    vel_x = max(vel_x, -0.5*dt)
    vel_y = min(vel_y, 0.5*dt)
    vel_y = max(vel_y, -0.5*dt)

    ship_x = (ship_x + vel_x) % WIDTH
    ship_y = (ship_y - vel_y) % HEIGHT
    bullet_x = (bullet_x + bullet_vel * math.cos(math.pi*bullet_angle/180)) % WIDTH
    bullet_y = (bullet_y - bullet_vel * math.sin(math.pi*bullet_angle/180)) % HEIGHT  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = ship_x - bullet.get_width()/2 + 15 * math.cos(math.pi*angle/180)
                bullet_y = ship_y - bullet.get_height()/2 -  15 * math.sin(math.pi*angle/180)
                bullet_vel = 0.3 * dt
                bullet_angle = angle
    if running == False:
        break


    rot_ship = pygame.transform.rotate(ship, angle)
    dw = rot_ship.get_width() - ship.get_width()
    dh = rot_ship.get_height() - ship.get_height()
    display.fill((0, 0, 0))
    display.blit(bullet, (bullet_x, bullet_y))
    display.blit(rot_ship, (ship_x-dw/2 - ship.get_width()/2, ship_y-dh/2 - ship.get_height()/2))
    display.blit(big_ast, (0, 0))
    display.blit(med_ast, (105, 0))
    display.blit(small_ast, (158, 0))
    pygame.display.flip()
