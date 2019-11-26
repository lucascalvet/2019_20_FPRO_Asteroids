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

x = 400
y = 300
vel_x = 0
vel_y = 0
angle = 90
vel_ang = 90
VEL_ANG = 0.5
ACCEL = 0.0003
FRICTION = 0.0025

running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle += VEL_ANG * dt
    if keys[pygame.K_RIGHT]:
        angle -= VEL_ANG * dt
    if keys[pygame.K_UP]:
        vel_x += ACCEL * math.cos(math.pi*angle/180) * dt
        vel_y += ACCEL * math.sin(math.pi*angle/180) * dt
#    if keys[pygame.K_DOWN]:
#        
#    vel = math.sqrt()
    if vel_x > 0:
        vel_x = max(0, vel_x - FRICTION)
    if vel_x < 0:
        vel_x = min(0, vel_x + FRICTION)
    if vel_y > 0:
        vel_y = max(0, vel_y - FRICTION)
    if vel_y < 0:
        vel_y = min(0, vel_y + FRICTION)
    vel_x = min(vel_x, 0.007*dt)
    vel_x = max(vel_x, -0.007*dt)
    vel_y = min(vel_y, 0.007*dt)
    vel_y = max(vel_y, -0.007*dt)

    x = (x + vel_x * dt) % WIDTH
    y = (y - vel_y * dt) % HEIGHT

    rot_ship = pygame.transform.rotate(ship, angle)
    dw = rot_ship.get_width() - ship.get_width()
    dh = rot_ship.get_height() - ship.get_height()

    display.fill((0, 0, 0))

    display.blit(big_ast, (0, 0))
    display.blit(med_ast, (105, 0))
    display.blit(small_ast, (158, 0))
    display.blit(rot_ship, (x-dw/2, y-dh/2))
    pygame.display.flip()
