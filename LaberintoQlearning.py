import sys
import pygame
import numpy as np
import random

# Definir las constantes del juego que se usara para iterar el bucle y crear el laberinto
LABERINTO = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                 ])


# Definir las constantes de colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

#Tamaño de cada bloque en píxeles del laberinto.
BLOQUE_TAM = 40
#Tamaño de la pantalla que se usará para visualizar el laberinto y cualquier solución encontrada
SCREEN_WIDTH = LABERINTO.shape[1] * BLOQUE_TAM
SCREEN_HEIGHT = LABERINTO.shape[0] * BLOQUE_TAM
#Coordenada para la posicion inicial
INICIAL_POS = (1, 1)
#Coordenada para la posicion final (meta)
FINAL_POS = (18, 18)
#Número de episodios para entrenar el modelo
NUM_EPISODIOS = 5000
#Factor de Aprendizaje
FACTOR_APRENDIZAJE = 0.8
#Factor de descuento para las recompensas en futuras acciones
FACTOR_DESCUENTO = 0.95

# Definir una función para dibujar el laberinto en la pantalla
def dibujar_laberinto(screen):
    for i in range(LABERINTO.shape[0]):
        for j in range(LABERINTO.shape[1]):
            if LABERINTO[i][j] == 1:
                pygame.draw.rect(screen, BLACK, (j * BLOQUE_TAM, i * BLOQUE_TAM, BLOQUE_TAM, BLOQUE_TAM))
            elif LABERINTO[i][j] == 0:
                pygame.draw.rect(screen, WHITE, (j * BLOQUE_TAM, i * BLOQUE_TAM, BLOQUE_TAM, BLOQUE_TAM))
    pygame.display.update()


# Definir una función para dibujar el bloque en la pantalla
def dibujar_bloque(screen, pos):
    pygame.draw.rect(screen, BLUE, (pos[1] * BLOQUE_TAM, pos[0] * BLOQUE_TAM, BLOQUE_TAM, BLOQUE_TAM))
    pygame.display.update()


# Definir una función para dibujar la meta en la pantalla
def dibujar_meta(screen, pos):
    pygame.draw.rect(screen, RED, (pos[1] * BLOQUE_TAM, pos[0] * BLOQUE_TAM, BLOQUE_TAM, BLOQUE_TAM))
    pygame.display.update()


# Definir una función para mover el bloque en el laberinto
def movimiento_bloque(pos, action):
    new_pos = list(pos)
    if action == 0: # mover arriba
        new_pos[0] -= 1
    elif action == 1: # mover abajo
        new_pos[0] += 1
    elif action == 2: # mover izquierda
        new_pos[1] -= 1
    elif action == 3: # mover derecha
        new_pos[1] += 1
    # Comprobar si la nueva posición es válida
    if LABERINTO[new_pos[0]][new_pos[1]] == 0:
        return tuple(new_pos)
    else:
        return pos


# Definir una matriz Q para almacenar los valores de Q para cada estado y acción
Q = np.zeros((LABERINTO.shape[0], LABERINTO.shape[1], 4))


# Inicializar pygame y la ventana de juego
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Laberinto Q-Learning')


# Dibujar el laberinto, el bloque y la meta en la pantalla
dibujar_laberinto(screen)
dibujar_bloque(screen, INICIAL_POS)
dibujar_meta(screen, FINAL_POS)


# Ejecutar el ciclo principal del juego
for episode in range(NUM_EPISODIOS):
    # Reiniciar el bloque en su posición inicial
    block_pos = INICIAL_POS

    # Ejecutar un episodio
    while True:
        # Elegir una acción para el bloque (exploración vs. explotación)
        if random.uniform(0, 1) < 0.1:
            action = random.randint(0, 3) # exploración aleatoria
        else:
            action = np.argmax(Q[block_pos[0], block_pos[1]]) # explotación de la matriz Q

        # Mover el bloque según la acción elegida
        new_pos = movimiento_bloque(block_pos, action)

        # Calcular la recompensa por mover el bloque a la nueva posición
        if new_pos == FINAL_POS:
            reward = 100
            done = True
        else:
            reward = -1
            done = False

        # Actualizar la matriz Q con el nuevo valor de Q
        old_value = Q[block_pos[0], block_pos[1], action]
        next_max = np.max(Q[new_pos[0], new_pos[1]])
        new_value = (1 - FACTOR_APRENDIZAJE) * old_value + FACTOR_APRENDIZAJE * (reward + FACTOR_DESCUENTO * next_max)
        Q[block_pos[0], block_pos[1], action] = new_value

        # Dibujar el laberinto, el bloque y la meta en la pantalla
        screen.fill(WHITE)
        dibujar_laberinto(screen)
        dibujar_bloque(screen, block_pos)
        dibujar_meta(screen, FINAL_POS)

        # Actualizar la pantalla
        pygame.display.update()

        # Esperar un momento antes de continuar
        pygame.time.wait(20)

        # Si se alcanza la meta, terminar el episodio
        if done:
            # Definir las dimensiones de la pantalla
            width = 800
            height = 600

            # Crear una nueva ventana de Pygame
            screen = pygame.display.set_mode((width, height))

            # Definir el tamaño de fuente y tipo de letra para el texto
            font_size = 32
            font = pygame.font.SysFont('Arial', font_size) 
             
            popup_surface = pygame.Surface((400, 200))
            popup_surface.fill((255, 255, 255))

            # Dibujar el mensaje en la superficie emergente
            message = "LABERINTO RESUELTO :)"
            text = font.render(message, True, (0, 0, 0))
            text_rect = text.get_rect(center=popup_surface.get_rect().center)
            popup_surface.blit(text, text_rect)

            # Dibujar la ventana emergente en la pantalla
            popup_rect = popup_surface.get_rect(center=screen.get_rect().center)
            screen.blit(popup_surface, popup_rect)

            # Actualizar la pantalla para mostrar la ventana emergente
            pygame.display.flip()
        
            print("Matriz Q:")
            print(Q)
            # Esperar 5 segundos antes de cerrar el programa
            pygame.time.wait(4000)
            pygame.quit()
            sys.exit()
            break

        # Actualizar la posición del bloque
        block_pos = new_pos

    

