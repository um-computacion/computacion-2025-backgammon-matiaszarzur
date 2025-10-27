"""Renderizador del tablero de backgammon."""
import pygame
from core.ColorFicha import ColorFicha

# Constantes (copiadas para este módulo)
WIDTH = 1200
HEIGHT = 800
TRIANGLE_WIDTH = 80
TRIANGLE_HEIGHT = 250
BAR_WIDTH = 40

COLOR_FONDO = (139, 90, 43)
COLOR_MARCO_OSCURO = (50, 30, 10)
COLOR_MARCO_CLARO = (100, 60, 30)
COLOR_BAR = (60, 40, 15)
COLOR_TRIANGULO_CLARO = (200, 200, 200)
COLOR_TRIANGULO_OSCURO = (100, 50, 30)
COLOR_FICHA_BLANCA = (255, 255, 255)
COLOR_FICHA_NEGRA = (50, 50, 50)


class TableroRenderer:
    """Clase responsable de renderizar el tablero de backgammon."""
    
    def __init__(self, screen, game):
        """Inicializar el renderizador del tablero."""
        self.__screen = screen
        self.__game = game
        self.__font = pygame.font.SysFont('Arial', 16)
    
    def obtener_posicion_triangulo(self, punto_index):
        """Obtiene la posición base de un triángulo específico."""
        margen = 30

        if punto_index < 12:
            # Puntos superiores (0-11)
            if punto_index < 6:
                columna = 5 - punto_index
                x = WIDTH // 2 + BAR_WIDTH // 2 + margen + columna * TRIANGLE_WIDTH
            else:
                columna = 11 - punto_index
                x = margen + columna * TRIANGLE_WIDTH
            y = margen
        else:
            # Puntos inferiores (12-23)
            if punto_index < 18:
                columna = punto_index - 12
                x = margen + columna * TRIANGLE_WIDTH
            else:
                columna = punto_index - 18
                x = WIDTH // 2 + BAR_WIDTH // 2 + margen + columna * TRIANGLE_WIDTH
            y = HEIGHT - margen

        return (x, y)

    def dibujar_triangulo(self, punto_index, es_superior):
        """Dibuja un triángulo en una posición específica."""
        x, y = self.obtener_posicion_triangulo(punto_index)

        if punto_index % 2 == 0:
            color = COLOR_TRIANGULO_CLARO
        else:
            color = COLOR_TRIANGULO_OSCURO

        if es_superior:
            punto1 = (x, y)
            punto2 = (x + TRIANGLE_WIDTH, y)
            punto3 = (x + TRIANGLE_WIDTH // 2, y + TRIANGLE_HEIGHT)
        else:
            punto1 = (x, y)
            punto2 = (x + TRIANGLE_WIDTH, y)
            punto3 = (x + TRIANGLE_WIDTH // 2, y - TRIANGLE_HEIGHT)

        pygame.draw.polygon(self.__screen, color, [punto1, punto2, punto3])
        pygame.draw.polygon(self.__screen, (0, 0, 0), [punto1, punto2, punto3], 2)
    
    def dibujar_numero_punto(self, punto_index):
        """Dibuja el número del punto en el triángulo."""
        numero = punto_index + 1
        x_base, y_base = self.obtener_posicion_triangulo(punto_index)
        x_centro = x_base + TRIANGLE_WIDTH // 2
        
        texto = self.__font.render(str(numero), True, (0, 0, 0))
        texto_rect = texto.get_rect()
        
        if punto_index < 12:
            texto_rect.center = (x_centro, y_base + 10)
        else:
            texto_rect.center = (x_centro, y_base - 10)
        
        self.__screen.blit(texto, texto_rect)
    
    def dibujar_marco(self):
        """Dibuja el marco del tablero."""
        pygame.draw.rect(self.__screen, COLOR_MARCO_OSCURO, (0, 0, WIDTH, HEIGHT), 15)
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

        x_base, y_base = self.obtener_posicion_triangulo(punto_index)
        x_centro = x_base + TRIANGLE_WIDTH // 2
        radio = 15
        es_superior = punto_index < 12

        for i, ficha in enumerate(fichas):
            if ficha.color == ColorFicha.BLANCA:
                color = COLOR_FICHA_BLANCA
            else:
                color = COLOR_FICHA_NEGRA

            if es_superior:
                y_ficha = y_base + 20 + i * (radio * 2 + 2)
            else:
                y_ficha = y_base - 20 - i * (radio * 2 + 2)

            pygame.draw.circle(self.__screen, color, (x_centro, y_ficha), radio)
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
        
        pygame.draw.polygon(self.__screen, (255, 255, 0), [punto1, punto2, punto3], 4)
    
    def dibujar_tablero_completo(self):
        """Dibuja el tablero completo con todos sus elementos."""
        self.__screen.fill(COLOR_FONDO)
        self.dibujar_marco()
        self.dibujar_bar()
        
        for i in range(24):
            es_superior = i < 12
            self.dibujar_triangulo(i, es_superior)
            self.dibujar_numero_punto(i)
        
        for i in range(24):
            self.dibujar_fichas(i)
