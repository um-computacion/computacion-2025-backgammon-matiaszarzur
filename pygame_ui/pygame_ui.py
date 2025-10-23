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
        # Implementar cálculo de posición
        pass
    
    def dibujar_triangulo(self, punto_index, es_superior):
        """Dibuja un triángulo en una posición específica."""
        #Implementar dibujo de triángulo
        pass
    
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
        #Implementar dibujo de fichas
        pass
    
    def dibujar_tablero_completo(self):
        """Dibuja el tablero completo con todos sus elementos."""
        self.__screen.fill(COLOR_FONDO)
        self.dibujar_marco()
        self.dibujar_bar()
        
        # Dibujar los 24 triángulos
        for i in range(24):
            es_superior = i < 12
            self.dibujar_triangulo(i, es_superior)
        
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
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Renderizar
        tablero_ui.dibujar_tablero_completo()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()