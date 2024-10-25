import pygame

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 200, 200)
AZUL = (100, 150, 255)
VERDE = (100, 255, 100)
GRIS = (200, 200, 200)
GRIS_CLARO = (230, 230, 230)

def puzzle_drawing(screen, state, size, cell_width, next_state=None):
    screen.fill(BLANCO)
    font = pygame.font.SysFont(None, 60, bold=True)

    # Encontrar la posición actual y futura del '0' (si hay un next_state)
    future_position = None
    if next_state is not None:
        for i in range(size):
            for j in range(size):
                # Buscar dónde está el '0' en el siguiente state
                if next_state[i][j] == 0:
                    future_position = (i, j)  # Guardar la futura posición del '0'
                    break

    for i in range(size):
        for j in range(size):
            value = state[i][j]
            rect = pygame.Rect(j * cell_width, i * cell_width, cell_width, cell_width)

            # Establecer color de fondo de cada celda
            if value == 0:
                color_font = BLANCO  # Color para el bloque vacío actual
            else:
                color_font = ROJO  # Color para los bloques con números

            # Pintar en verde la futura posición del '0'
            if future_position == (i, j):
                color_font = VERDE

            pygame.draw.rect(screen, color_font, rect)

            if value != 0:
                # Dibujar número en cada bloque
                text = font.render(str(value), True, NEGRO)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
                pygame.draw.rect(screen, NEGRO, rect, 3)  # Bordear las celdas
            else:
                #text = font.render('0', True, NEGRO)
                #text_rect = text.get_rect(center=rect.center)
                #screen.blit(text, text_rect)
                pygame.draw.rect(screen, NEGRO, rect, 3)



def boton_drawing(screen, window_width, cell_width, mouse_hover):
    # Dibuja un botón sobre el puzzle para reiniciar la animación
    font_boton = pygame.font.SysFont(None, 50, bold=True)
    boton_rect = pygame.Rect(window_width // 4, window_width // 2 - cell_width // 2, window_width // 2, cell_width)

    # Cambia el color del botón si el cursor está encima
    color_boton = GRIS_CLARO if not mouse_hover else GRIS
    pygame.draw.rect(screen, color_boton, boton_rect, border_radius=10)
    pygame.draw.rect(screen, NEGRO, boton_rect, 3)

    text_boton = font_boton.render("Reiniciar", True, NEGRO)
    text_rect_boton = text_boton.get_rect(center=boton_rect.center)
    screen.blit(text_boton, text_rect_boton)

    return boton_rect

def visualizer_solution(path, size):
    # Inicializar pygame
    pygame.init()

    window_width = 500
    cell_width = window_width // size
    screen = pygame.display.set_mode((window_width, window_width))
    pygame.display.set_caption('N-Puzzle Visualizer')

    clock = pygame.time.Clock()
    index = 0  # Índice para recorrer los states del puzzle
    end_animation = False
    boton_rect = None

    while True:
        mouse_hover = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and end_animation:
                x, y = event.pos
                if boton_rect.collidepoint(x, y):
                    index = 0  # Reiniciar la animación
                    end_animation = False

        if end_animation:
            x, y = pygame.mouse.get_pos()
            if boton_rect and boton_rect.collidepoint(x, y):
                mouse_hover = True

        if not end_animation:
            state = path[index]
            next_state = path[index + 1] if index + 1 < len(path) else None
            puzzle_drawing(screen, state, size, cell_width, next_state)
            index += 1

            clock.tick(0.5)

            if index >= len(path):
                end_animation = True
        else:
            boton_rect = boton_drawing(screen, window_width, cell_width, mouse_hover)

        pygame.display.flip()
