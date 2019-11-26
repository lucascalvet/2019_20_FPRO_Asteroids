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
vel = 0
angle = 90
VEL_ANG = 0.5
ACCEL = 0.0002
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
        vel += ACCEL * dt
    if keys[pygame.K_DOWN]:
        vel -= ACCEL * dt

    if vel > 0:
        vel = max(0, vel - FRICTION)
    if vel < 0:
        vel = min(0, vel + FRICTION)
    print(vel/dt)
    vel = min(vel, 0.007*dt)
    vel = max(vel, -0.007*dt)

    x = (x + vel * math.cos(math.pi*angle/180) * dt) % WIDTH
    y = (y - vel * math.sin(math.pi*angle/180) * dt) % HEIGHT

    rot_ship = pygame.transform.rotate(ship, angle)
    dw = rot_ship.get_width() - ship.get_width()
    dh = rot_ship.get_height() - ship.get_height()

    display.fill((0, 0, 0))

    display.blit(big_ast, (0, 0))
    display.blit(med_ast, (105, 0))
    display.blit(small_ast, (158, 0))
    display.blit(rot_ship, (x-dw/2, y-dh/2))
    pygame.display.flip()
