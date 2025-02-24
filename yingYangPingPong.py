import sys
import pygame
import random
import math

# --- Procesamiento de argumentos ---
# Por defecto se asume modo protector (/s)
mode = 's'
if len(sys.argv) > 1:
    arg = sys.argv[1].lower()
    if arg.startswith('/c'):
        # Modo configuración: se muestra una ventana sencilla y se sale
        pygame.init()
        config_screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Configuración del Protector de Pantallas")
        font = pygame.font.SysFont(None, 24)
        text = font.render("No hay opciones de configuración.", True, (255, 255, 255))
        config_screen.fill((0, 0, 0))
        config_screen.blit(text, (50, 130))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()
    elif arg.startswith('/p'):
        mode = 'p'
    # Si es /s o cualquier otro parámetro, se usa el modo protector

# Inicializar Pygame (se vuelve a inicializar para el modo que corresponda)
pygame.init()

# --- Configuración de la pantalla según el modo ---
def setup_screen(mode):
    if mode == 'p':
        # Modo vista previa: ventana pequeña
        screen = pygame.display.set_mode((300, 200))
    else:
        # Modo protector: pantalla completa
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return screen

screen = setup_screen(mode)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Protector de Pantallas Ying Yang Ping Pong")

# --- Definiciones y configuraciones del juego ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRICK_SIZE = 40
RADIUS = 20

# Configuración inicial de los círculos
circulo_negro = {
    "pos": [WIDTH // 4, HEIGHT // 2],
    "vel": [random.choice([-4, 4]), random.choice([-4, 4])],
    "color": BLACK
}

circulo_blanco = {
    "pos": [3 * WIDTH // 4, HEIGHT // 2],
    "vel": [random.choice([-4, 4]), random.choice([-4, 4])],
    "color": WHITE
}

# Creación del fondo de ladrillos: ladrillos blancos en la mitad izquierda, negros en la derecha.
bricks = []
for x in range(0, WIDTH, BRICK_SIZE):
    column = []
    for y in range(0, HEIGHT, BRICK_SIZE):
        color = WHITE if x < WIDTH // 2 else BLACK
        column.append({"rect": pygame.Rect(x, y, BRICK_SIZE, BRICK_SIZE), "color": color})
    bricks.append(column)

clock = pygame.time.Clock()
small_font = pygame.font.SysFont(None, 20)

# --- Funciones de colisión y lógica del juego ---
def check_ball_collision(c1, c2):
    dist = math.hypot(c1["pos"][0] - c2["pos"][0], c1["pos"][1] - c2["pos"][1])
    return dist < 2 * RADIUS

def check_collision_with_bricks(circle, skip_color_change=False):
    for column in bricks:
        for brick in column:
            if brick["color"] == circle["color"]:
                if brick["rect"].collidepoint(circle["pos"]):
                    # Invertir velocidad según el lado de colisión
                    if brick["rect"].left < circle["pos"][0] < brick["rect"].right:
                        circle["vel"][1] *= -1
                    if brick["rect"].top < circle["pos"][1] < brick["rect"].bottom:
                        circle["vel"][0] *= -1
                    # Cambiar el color del ladrillo (si no están chocando ambas pelotas)
                    if not skip_color_change:
                        brick["color"] = WHITE if circle["color"] == BLACK else BLACK

def calculate_color_percentages():
    total_bricks = sum(len(column) for column in bricks)
    black_count = sum(1 for column in bricks for brick in column if brick["color"] == BLACK)
    white_count = total_bricks - black_count
    black_percentage = (black_count / total_bricks) * 100
    white_percentage = (white_count / total_bricks) * 100
    return black_percentage, white_percentage

# --- Bucle principal del protector de pantallas ---
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

    # Verificar colisión entre las pelotas
    pelotas_chocan = check_ball_collision(circulo_negro, circulo_blanco)

    # Actualizar posición de cada círculo y gestionar rebotes
    for circulo in [circulo_negro, circulo_blanco]:
        circulo["pos"][0] += circulo["vel"][0]
        circulo["pos"][1] += circulo["vel"][1]

        if circulo["pos"][0] - RADIUS < 0 or circulo["pos"][0] + RADIUS > WIDTH:
            circulo["vel"][0] *= -1
        if circulo["pos"][1] - RADIUS < 0 or circulo["pos"][1] + RADIUS > HEIGHT:
            circulo["vel"][1] *= -1

        check_collision_with_bricks(circulo, skip_color_change=pelotas_chocan)

    # Calcular porcentajes de ladrillos
    black_percentage, white_percentage = calculate_color_percentages()

    # Dibujar fondo (ladrillos)
    for column in bricks:
        for brick in column:
            pygame.draw.rect(screen, brick["color"], brick["rect"])

    # Dibujar círculos
    pygame.draw.circle(screen, circulo_negro["color"], circulo_negro["pos"], RADIUS)
    pygame.draw.circle(screen, circulo_blanco["color"], circulo_blanco["pos"], RADIUS)

    # Mostrar porcentajes en cada círculo (el negro muestra el porcentaje de blancos y viceversa)
    black_text = small_font.render(f"{white_percentage:.2f}", True, WHITE)
    white_text = small_font.render(f"{black_percentage:.2f}", True, BLACK)
    black_text_rect = black_text.get_rect(center=circulo_negro["pos"])
    white_text_rect = white_text.get_rect(center=circulo_blanco["pos"])
    screen.blit(black_text, black_text_rect)
    screen.blit(white_text, white_text_rect)

    pygame.display.flip()
    clock.tick(30)
