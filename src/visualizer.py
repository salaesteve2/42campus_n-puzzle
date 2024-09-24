import pygame

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 200, 200)
AZUL = (100, 150, 255)
VERDE = (100, 255, 100)
GRIS = (200, 200, 200)
GRIS_CLARO = (230, 230, 230)

def dibujar_puzzle(pantalla, estado, size, ancho_celda, proximo_estado=None):
    pantalla.fill(BLANCO)
    fuente = pygame.font.SysFont(None, 60, bold=True)

    # Encontrar la posición actual y futura del '0' (si hay un proximo_estado)
    futura_posicion = None
    if proximo_estado is not None:
        for i in range(size):
            for j in range(size):
                # Buscar dónde está el '0' en el siguiente estado
                if proximo_estado[i][j] == 0:
                    futura_posicion = (i, j)  # Guardar la futura posición del '0'
                    break

    for i in range(size):
        for j in range(size):
            valor = estado[i][j]
            rect = pygame.Rect(j * ancho_celda, i * ancho_celda, ancho_celda, ancho_celda)

            # Establecer color de fondo de cada celda
            if valor == 0:
                color_fondo = BLANCO  # Color para el bloque vacío actual
            else:
                color_fondo = ROJO  # Color para los bloques con números

            # Pintar en verde la futura posición del '0'
            if futura_posicion == (i, j):
                color_fondo = VERDE

            pygame.draw.rect(pantalla, color_fondo, rect)

            if valor != 0:
                # Dibujar número en cada bloque
                texto = fuente.render(str(valor), True, NEGRO)
                text_rect = texto.get_rect(center=rect.center)
                pantalla.blit(texto, text_rect)
                pygame.draw.rect(pantalla, NEGRO, rect, 3)  # Bordear las celdas
            else:
                #texto = fuente.render('0', True, NEGRO)
                #text_rect = texto.get_rect(center=rect.center)
                #pantalla.blit(texto, text_rect)
                pygame.draw.rect(pantalla, NEGRO, rect, 3)



def dibujar_boton(pantalla, ancho_ventana, ancho_celda, cursor_encima):
    # Dibuja un botón sobre el puzzle para reiniciar la animación
    fuente_boton = pygame.font.SysFont(None, 50, bold=True)
    boton_rect = pygame.Rect(ancho_ventana // 4, ancho_ventana // 2 - ancho_celda // 2, ancho_ventana // 2, ancho_celda)

    # Cambia el color del botón si el cursor está encima
    color_boton = GRIS_CLARO if not cursor_encima else GRIS
    pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=10)
    pygame.draw.rect(pantalla, NEGRO, boton_rect, 3)

    texto_boton = fuente_boton.render("Reiniciar", True, NEGRO)
    text_rect_boton = texto_boton.get_rect(center=boton_rect.center)
    pantalla.blit(texto_boton, text_rect_boton)

    return boton_rect

def visualizador_solucion(camino, size):
    # Inicializar pygame
    pygame.init()

    ancho_ventana = 500
    ancho_celda = ancho_ventana // size
    pantalla = pygame.display.set_mode((ancho_ventana, ancho_ventana))
    pygame.display.set_caption('N-Puzzle Visualizer')

    reloj = pygame.time.Clock()
    index = 0  # Índice para recorrer los estados del puzzle
    animacion_terminada = False
    boton_rect = None

    while True:
        cursor_encima = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and animacion_terminada:
                x, y = event.pos
                if boton_rect.collidepoint(x, y):
                    index = 0  # Reiniciar la animación
                    animacion_terminada = False

        if animacion_terminada:
            x, y = pygame.mouse.get_pos()
            if boton_rect and boton_rect.collidepoint(x, y):
                cursor_encima = True

        if not animacion_terminada:
            estado = camino[index]
            proximo_estado = camino[index + 1] if index + 1 < len(camino) else None
            dibujar_puzzle(pantalla, estado, size, ancho_celda, proximo_estado)
            index += 1

            reloj.tick(0.5)

            if index >= len(camino):
                animacion_terminada = True
        else:
            boton_rect = dibujar_boton(pantalla, ancho_ventana, ancho_celda, cursor_encima)

        pygame.display.flip()
