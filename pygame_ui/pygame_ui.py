"""Módulo de interfaz gráfica usando Pygame."""
import pygame
import sys
from core.BackgammonGame import BackgammonGame
from core.ColorFicha import ColorFicha

# constantes
WIDTH = 1200
HEIGHT = 800
FPS = 60

# Dimensiones del tablero
BOARD_MARGIN = 50
BAR_WIDTH = 40
TRIANGLE_WIDTH = 80
TRIANGLE_HEIGHT = 250

# colores
COLOR_FONDO = (139, 90, 43)
COLOR_MARCO_OSCURO = (50, 30, 10)
COLOR_MARCO_CLARO = (100, 60, 30)
COLOR_BAR = (60, 40, 15)
COLOR_TRIANGULO_CLARO = (200, 200, 200)
COLOR_TRIANGULO_OSCURO = (100, 50, 30)
COLOR_FICHA_BLANCA = (255, 255, 255)
COLOR_FICHA_NEGRA = (50, 50, 50)



class TableroUI:
    """Clase para renderizar el tablero de backgammon."""
    
    def __init__(self, screen, game):
        """Inicializar el tablero UI."""
        self.__screen = screen
        self.__game = game
        self.__font = pygame.font.SysFont('Arial', 16)
    
    @property
    def screen(self):
        """Obtener la superficie de dibujo."""
        return self.__screen
    
    @property
    def game(self):
        """Obtener la instancia del juego."""
        return self.__game
    
    def obtener_posicion_triangulo(self, punto_index):
        """Obtiene la posición base de un triángulo específico."""
        # Margen desde el borde
        margen = 30

        # Calcular si está en la mitad izquierda o derecha
        if punto_index < 12:
            # Puntos superiores (0-11)
            if punto_index < 6:
                # Lado derecho superior (puntos 0-5)
                columna = 5 - punto_index
                x = WIDTH // 2 + BAR_WIDTH // 2 + margen + columna * TRIANGLE_WIDTH
            else:
                # Lado izquierdo superior (puntos 6-11)
                columna = 11 - punto_index
                x = margen + columna * TRIANGLE_WIDTH
            y = margen
        else:
            # Puntos inferiores (12-23)
            if punto_index < 18:
                # Lado izquierdo inferior (puntos 12-17)
                columna = punto_index - 12
                x = margen + columna * TRIANGLE_WIDTH
            else:
                # Lado derecho inferior (puntos 18-23)
                columna = punto_index - 18
                x = WIDTH // 2 + BAR_WIDTH // 2 + margen + columna * TRIANGLE_WIDTH
            y = HEIGHT - margen

        return (x, y)

    def dibujar_triangulo(self, punto_index, es_superior):
        """Dibuja un triángulo en una posición específica."""
        # Obtener posición base
        x, y = self.obtener_posicion_triangulo(punto_index)

        # Determinar color (alternado)
        if punto_index % 2 == 0:
            color = COLOR_TRIANGULO_CLARO
        else:
            color = COLOR_TRIANGULO_OSCURO

        # Calcular los 3 vértices del triángulo
        if es_superior:
            # Triángulo apuntando hacia abajo (▼)
            punto1 = (x, y)
            punto2 = (x + TRIANGLE_WIDTH, y)
            punto3 = (x + TRIANGLE_WIDTH // 2, y + TRIANGLE_HEIGHT)
        else:
            # Triángulo apuntando hacia arriba (▲)
            punto1 = (x, y)
            punto2 = (x + TRIANGLE_WIDTH, y)
            punto3 = (x + TRIANGLE_WIDTH // 2, y - TRIANGLE_HEIGHT)

        # Dibujar el triángulo
        pygame.draw.polygon(self.__screen, color, [punto1, punto2, punto3])
        # Dibujar borde del triángulo
        pygame.draw.polygon(self.__screen, (0, 0, 0), [punto1, punto2, punto3], 2)
    
    def dibujar_numero_punto(self, punto_index):
        """Dibuja el número del punto en el triángulo."""
        # Convertir índice interno (0-23) a número visual (1-24)
        numero = punto_index + 1
        
        # Obtener posición del triángulo
        x_base, y_base = self.obtener_posicion_triangulo(punto_index)
        x_centro = x_base + TRIANGLE_WIDTH // 2
        
        # Renderizar texto
        texto = self.__font.render(str(numero), True, (0, 0, 0))
        texto_rect = texto.get_rect()
        
        # Posicionar según si es superior o inferior
        if punto_index < 12:
            # Superior - número arriba
            texto_rect.center = (x_centro, y_base + 10)
        else:
            # Inferior - número abajo
            texto_rect.center = (x_centro, y_base - 10)
        
        self.__screen.blit(texto, texto_rect)
    
    def dibujar_marco(self):
        """Dibuja el marco del tablero."""
        # Marco exterior
        pygame.draw.rect(self.__screen, COLOR_MARCO_OSCURO, (0, 0, WIDTH, HEIGHT), 15)
        # Marco interior
        pygame.draw.rect(self.__screen, COLOR_MARCO_CLARO, (10, 10, WIDTH-20, HEIGHT-20), 8)
    
    def dibujar_bar(self):
        """Dibuja la barra central del tablero."""
        bar_x = WIDTH // 2 - BAR_WIDTH // 2
        pygame.draw.rect(self.__screen, COLOR_BAR, (bar_x-5, 10, BAR_WIDTH+10, HEIGHT-20))
        pygame.draw.rect(self.__screen, COLOR_MARCO_CLARO, (bar_x, 10, BAR_WIDTH, HEIGHT-20))
    
    def dibujar_fichas(self, punto_index):
        """Dibuja las fichas en un punto específico."""
        fichas = self.__game.board.obtener_fichas(punto_index)

        if not fichas:
            return

        # Obtener posición del triángulo
        x_base, y_base = self.obtener_posicion_triangulo(punto_index)

        # Centro del triángulo en X
        x_centro = x_base + TRIANGLE_WIDTH // 2

        # Radio de las fichas
        radio = 15

        # Determinar dirección de apilamiento
        es_superior = punto_index < 12

        for i, ficha in enumerate(fichas):
            # Determinar color de la ficha
            if ficha.color == ColorFicha.BLANCA:
                color = COLOR_FICHA_BLANCA
            else:
                color = COLOR_FICHA_NEGRA

            # Calcular posición Y según si es superior o inferior
            if es_superior:
                y_ficha = y_base + 20 + i * (radio * 2 + 2)
            else:
                y_ficha = y_base - 20 - i * (radio * 2 + 2)

            # Dibujar ficha
            pygame.draw.circle(self.__screen, color, (x_centro, y_ficha), radio)
            # Borde de la ficha
            pygame.draw.circle(self.__screen, (0, 0, 0), (x_centro, y_ficha), radio, 2)
    
    def obtener_punto_clickeado(self, pos_mouse):
        """Detecta en qué punto se hizo click."""
        mouse_x, mouse_y = pos_mouse
        
        # Verificar cada triángulo
        for i in range(24):
            x_base, y_base = self.obtener_posicion_triangulo(i)
            es_superior = i < 12
            
            # Verificar si el click está dentro del rectángulo del triángulo
            if x_base <= mouse_x <= x_base + TRIANGLE_WIDTH:
                if es_superior:
                    # Triángulo superior
                    if y_base <= mouse_y <= y_base + TRIANGLE_HEIGHT:
                        return i
                else:
                    # Triángulo inferior
                    if y_base - TRIANGLE_HEIGHT <= mouse_y <= y_base:
                        return i
        
        return None
    
    def resaltar_punto(self, punto_index):
        """Resalta un punto con un borde más grueso."""
        x, y = self.obtener_posicion_triangulo(punto_index)
        es_superior = punto_index < 12
        
        if es_superior:
            punto1 = (x, y)
            punto2 = (x + TRIANGLE_WIDTH, y)
            punto3 = (x + TRIANGLE_WIDTH // 2, y + TRIANGLE_HEIGHT)
        else:
            punto1 = (x, y)
            punto2 = (x + TRIANGLE_WIDTH, y)
            punto3 = (x + TRIANGLE_WIDTH // 2, y - TRIANGLE_HEIGHT)
        
        # Dibujar borde amarillo grueso
        pygame.draw.polygon(self.__screen, (255, 255, 0), [punto1, punto2, punto3], 4)
    
    def dibujar_tablero_completo(self):
        """Dibuja el tablero completo con todos sus elementos."""
        self.__screen.fill(COLOR_FONDO)
        self.dibujar_marco()
        self.dibujar_bar()
        # Dibujar los 24 triángulos
        for i in range(24):
            es_superior = i < 12
            self.dibujar_triangulo(i, es_superior)
            self.dibujar_numero_punto(i)
        # Dibujar todas las fichas
        for i in range(24):
            self.dibujar_fichas(i)


# main loop del juego
def main():
    """Función principal del juego."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Backgammon")
    clock = pygame.time.Clock()
    # Crear juego
    game = BackgammonGame("Jugador 1", "Jugador 2")
    game.start_game()
    # Crear tablero UI
    tablero_ui = TableroUI(screen, game)
    
    punto_seleccionado = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    punto = tablero_ui.obtener_punto_clickeado(event.pos)
                    if punto is not None:
                        punto_seleccionado = punto
                        print(f"Clickeaste el punto {punto + 1}")
        
        # Renderizar
        tablero_ui.dibujar_tablero_completo()
        
        # Resaltar punto seleccionado
        if punto_seleccionado is not None:
            tablero_ui.resaltar_punto(punto_seleccionado)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()