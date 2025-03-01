import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Screensaver")

# Colores iniciales y posición del rectángulo
player = pygame.Rect((random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50))
numero1 = random.randint(0, 255)
numero2 = random.randint(0, 255)
numero3 = random.randint(0, 255)

# Tiempo inicial
last_change_time = pygame.time.get_ticks()
last_move_time = pygame.time.get_ticks()

# Variables de control de movimiento
speed_x = random.choice([-3, 3])
speed_y = random.choice([-3, 3])

run = True
while run:
    # Verificar el tiempo actual
    current_time = pygame.time.get_ticks()

    # Cambiar color cada segundo
    if current_time - last_change_time >= 1000:
        numero1 = random.randint(0, 255)
        numero2 = random.randint(0, 255)
        numero3 = random.randint(0, 255)
        last_change_time = current_time

    # Mover el rectángulo
    if current_time - last_move_time >= 20:  # Mover cada 20 ms para suavidad
        player.x += speed_x
        player.y += speed_y

        # Rebotar en los bordes
        if player.left <= 0 or player.right >= SCREEN_WIDTH:
            speed_x = -speed_x
        if player.top <= 0 or player.bottom >= SCREEN_HEIGHT:
            speed_y = -speed_y

        last_move_time = current_time

    # Dibujar pantalla
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (numero1, numero2, numero3), player)
    pygame.display.update()

    # Detectar movimiento del mouse o teclas presionadas para cerrar el protector de pantalla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
            pygame.quit()
            sys.exit()

pygame.quit()
