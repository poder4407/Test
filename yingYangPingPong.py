import pygame
import sys
import random
import math

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla completa usando la resolución actual
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption("Ventana con Ladrillos de Colores y Rebote de Pelotas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tamaño de los ladrillos
BRICK_SIZE = 40

# Datos de los círculos
RADIUS = 20

# Definir propiedades de los círculos, cada uno empieza en el fondo de color contrario
circulo_negro = {
    "pos": [3 * WIDTH // 4, HEIGHT // 2],  # Posición inicial en el fondo blanco
    "vel": [random.choice([-4, 4]), random.choice([-4, 4])],
    "color": BLACK
}

circulo_blanco = {
    "pos": [WIDTH // 4, HEIGHT // 2],  # Posición inicial en el fondo negro
    "vel": [random.choice([-4, 4]), random.choice([-4, 4])],
    "color": WHITE
}

# Crear el fondo de ladrillos
bricks = []
for x in range(0, WIDTH, BRICK_SIZE):
    column = []
    for y in range(0, HEIGHT, BRICK_SIZE):
        # Colocar ladrillos blancos en el lado derecho y negros en el izquierdo
        color = BLACK if x < WIDTH // 2 else WHITE
        column.append({"rect": pygame.Rect(x, y, BRICK_SIZE, BRICK_SIZE), "color": color})
    bricks.append(column)

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Fuente pequeña para el texto dentro de los círculos
small_font = pygame.font.SysFont(None, 20)

# Función para verificar colisión entre las pelotas
def check_ball_collision(c1, c2):
    dist = math.hypot(c1["pos"][0] - c2["pos"][0], c1["pos"][1] - c2["pos"][1])
    return dist < 2 * RADIUS  # Las pelotas chocan si la distancia es menor al diámetro

# Función para manejar el rebote y el cambio de color de los ladrillos
def check_collision_with_bricks(circle, skip_color_change=False):
    for column in bricks:
        for brick in column:
            if brick["color"] == circle["color"]:  # Solo verificar colisiones con ladrillos del mismo color
                if brick["rect"].collidepoint(circle["pos"]):
                    # Rebote al tocar un ladrillo del mismo color
                    if brick["rect"].left < circle["pos"][0] < brick["rect"].right:
                        circle["vel"][1] *= -1
                    if brick["rect"].top < circle["pos"][1] < brick["rect"].bottom:
                        circle["vel"][0] *= -1

                    # Cambiar el color del ladrillo solo si no se está en un choque entre pelotas
                    if not skip_color_change:
                        brick["color"] = WHITE if circle["color"] == BLACK else BLACK

# Función para calcular los porcentajes de color
def calculate_color_percentages():
    total_bricks = sum(len(column) for column in bricks)
    black_count = sum(1 for column in bricks for brick in column if brick["color"] == BLACK)
    white_count = total_bricks - black_count
    black_percentage = (black_count / total_bricks) * 100
    white_percentage = (white_count / total_bricks) * 100
    return black_percentage, white_percentage

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Verificar colisión entre pelotas
    pelotas_chocan = check_ball_collision(circulo_negro, circulo_blanco)

    # Mover los círculos
    for circulo in [circulo_negro, circulo_blanco]:
        # Actualizar posición
        circulo["pos"][0] += circulo["vel"][0]
        circulo["pos"][1] += circulo["vel"][1]

        # Rebote en los bordes de la ventana
        if circulo["pos"][0] - RADIUS < 0 or circulo["pos"][0] + RADIUS > WIDTH:
            circulo["vel"][0] *= -1
        if circulo["pos"][1] - RADIUS < 0 or circulo["pos"][1] + RADIUS > HEIGHT:
            circulo["vel"][1] *= -1

        ''' Comprobar colisiones con los ladrillos, pero no cambiar color si las pelotas 
        están chocando'''
        
        check_collision_with_bricks(circulo, skip_color_change=pelotas_chocan)

    # Calcular los porcentajes de ladrillos negros y blancos
    black_percentage, white_percentage = calculate_color_percentages()

    # Dibujar los ladrillos
    for column in bricks:
        for brick in column:
            pygame.draw.rect(screen, brick["color"], brick["rect"])

    # Dibujar los círculos
    pygame.draw.circle(screen, circulo_negro["color"], circulo_negro["pos"], RADIUS)
    pygame.draw.circle(screen, circulo_blanco["color"], circulo_blanco["pos"], RADIUS)

    # Texto de porcentaje dentro de cada círculo (porcentaje de ladrillos blancos en el círculo negro y viceversa)
    black_text = small_font.render(f"{white_percentage:.2f}", True, WHITE)  # Porcentaje de blancos en círculo negro
    white_text = small_font.render(f"{black_percentage:.2f}", True, BLACK)  # Porcentaje de negros en círculo blanco
    black_text_rect = black_text.get_rect(center=circulo_negro["pos"])
    white_text_rect = white_text.get_rect(center=circulo_blanco["pos"])
    screen.blit(black_text, black_text_rect)
    screen.blit(white_text, white_text_rect)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(30)
