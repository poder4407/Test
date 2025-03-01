import pygame
import sys
import random
import math

# Inicialización de Pygame
pygame.init()

# Configurar pantalla completa y obtener dimensiones reales
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Juego en Pantalla Completa con Ladrillos")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tamaño de los ladrillos
BRICK_SIZE = 40

# Datos de los círculos
RADIUS = 20

# Definir propiedades de los círculos, cada uno empieza en el fondo de color contrario
# Ahora los ladrillos blancos estarán en la mitad izquierda (igual que el rectángulo blanco del ejemplo previo)
circulo_negro = {
    "pos": [WIDTH // 4, HEIGHT // 2],  # En la mitad izquierda (fondo blanco)
    "vel": [random.choice([-4, 4]), random.choice([-4, 4])],
    "color": BLACK
}

circulo_blanco = {
    "pos": [3 * WIDTH // 4, HEIGHT // 2],  # En la mitad derecha (fondo negro)
    "vel": [random.choice([-4, 4]), random.choice([-4, 4])],
    "color": WHITE
}

# Crear el fondo de ladrillos:
# Se asignan ladrillos blancos en la mitad izquierda y negros en la mitad derecha,
# de forma que el área ocupada por los ladrillos blancos sea igual al rectángulo blanco del ejemplo anterior.
bricks = []
for x in range(0, WIDTH, BRICK_SIZE):
    column = []
    for y in range(0, HEIGHT, BRICK_SIZE):
        color = WHITE if x < WIDTH // 2 else BLACK
        column.append({"rect": pygame.Rect(x, y, BRICK_SIZE, BRICK_SIZE), "color": color})
    bricks.append(column)

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Fuente pequeña para el texto dentro de los círculos
small_font = pygame.font.SysFont(None, 20)

# Función para verificar colisión entre las pelotas
def check_ball_collision(c1, c2):
    dist = math.hypot(c1["pos"][0] - c2["pos"][0], c1["pos"][1] - c2["pos"][1])
    return dist < 2 * RADIUS  # Chocan si la distancia es menor al diámetro

# Función para manejar el rebote y el cambio de color de los ladrillos
def check_collision_with_bricks(circle, skip_color_change=False):
    for column in bricks:
        for brick in column:
            if brick["color"] == circle["color"]:  # Solo se verifica colisión con ladrillos del mismo color
                if brick["rect"].collidepoint(circle["pos"]):
                    # Rebote: se invierte la dirección en el eje correspondiente
                    if brick["rect"].left < circle["pos"][0] < brick["rect"].right:
                        circle["vel"][1] *= -1
                    if brick["rect"].top < circle["pos"][1] < brick["rect"].bottom:
                        circle["vel"][0] *= -1
                    # Cambiar el color del ladrillo (si no están chocando ambas pelotas)
                    if not skip_color_change:
                        brick["color"] = WHITE if circle["color"] == BLACK else BLACK

# Función para calcular los porcentajes de ladrillos de cada color
def calculate_color_percentages():
    total_bricks = sum(len(column) for column in bricks)
    black_count = sum(1 for column in bricks for brick in column if brick["color"] == BLACK)
    white_count = total_bricks - black_count
    black_percentage = (black_count / total_bricks) * 100
    white_percentage = (white_count / total_bricks) * 100
    return black_percentage, white_percentage

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Permitir salir presionando Escape
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Verificar colisión entre pelotas
    pelotas_chocan = check_ball_collision(circulo_negro, circulo_blanco)

    # Mover las pelotas y manejar rebotes
    for circulo in [circulo_negro, circulo_blanco]:
        circulo["pos"][0] += circulo["vel"][0]
        circulo["pos"][1] += circulo["vel"][1]

        if circulo["pos"][0] - RADIUS < 0 or circulo["pos"][0] + RADIUS > WIDTH:
            circulo["vel"][0] *= -1
        if circulo["pos"][1] - RADIUS < 0 or circulo["pos"][1] + RADIUS > HEIGHT:
            circulo["vel"][1] *= -1

        # Revisar colisiones con los ladrillos
        check_collision_with_bricks(circulo, skip_color_change=pelotas_chocan)

    # Calcular los porcentajes de ladrillos negros y blancos
    black_percentage, white_percentage = calculate_color_percentages()

    # Dibujar el fondo: se dibujan todos los ladrillos
    for column in bricks:
        for brick in column:
            pygame.draw.rect(screen, brick["color"], brick["rect"])

    # Dibujar los círculos
    pygame.draw.circle(screen, circulo_negro["color"], circulo_negro["pos"], RADIUS)
    pygame.draw.circle(screen, circulo_blanco["color"], circulo_blanco["pos"], RADIUS)

    # Mostrar el porcentaje de ladrillos de color contrario en cada círculo
    # El círculo negro muestra el porcentaje de blancos y viceversa.
    black_text = small_font.render(f"{white_percentage:.2f}", True, WHITE)
    white_text = small_font.render(f"{black_percentage:.2f}", True, BLACK)
    black_text_rect = black_text.get_rect(center=circulo_negro["pos"])
    white_text_rect = white_text.get_rect(center=circulo_blanco["pos"])
    screen.blit(black_text, black_text_rect)
    screen.blit(white_text, white_text_rect)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(30)
