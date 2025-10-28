"""Renderizador del tablero de Backgammon."""

import pygame
from core.ColorFicha import ColorFicha

# Constantes de diseño del tablero
WIDTH = 1200
HEIGHT = 800
TRIANGLE_WIDTH = 80
TRIANGLE_HEIGHT = 250
BAR_WIDTH = 40

# Colores utilizados en el tablero
COLOR_FONDO = (139, 90, 43)
COLOR_MARCO_OSCURO = (50, 30, 10)
COLOR_MARCO_CLARO = (100, 60, 30)
COLOR_BAR = (60, 40, 15)
COLOR_TRIANGULO_CLARO = (200, 200, 200)
COLOR_TRIANGULO_OSCURO = (100, 50, 30)
COLOR_FICHA_BLANCA = (255, 255, 255)
COLOR_FICHA_NEGRA = (50, 50, 50)


class TableroRenderer:
    """Clase encargada de renderizar visualmente el tablero de Backgammon."""
    
    def __init__(self, screen, game):
        """Inicializa el renderizador con la superficie de Pygame y el estado del juego."""
        self.__screen = screen
        self.__game = game
        self.__font = pygame.font.SysFont('Arial', 16)
        self.__font_small = pygame.font.SysFont('Arial', 12, bold=True)
    
    def obtener_posicion_triangulo(self, punto_index):
        """Devuelve la posición (x, y) base de un triángulo dado su índice."""
        margen = 30

        if punto_index < 12:
            # Mitad superior del tablero
            if punto_index < 6:
                columna = 5 - punto_index
                x = WIDTH // 2 + BAR_WIDTH // 2 + margen + columna * TRIANGLE_WIDTH
            else:
                columna = 11 - punto_index
                x = margen + columna * TRIANGLE_WIDTH
            y = margen
        else:
            # Mitad inferior del tablero
            if punto_index < 18:
                columna = punto_index - 12
                x = margen + columna * TRIANGLE_WIDTH
            else:
                columna = punto_index - 18
                x = WIDTH // 2 + BAR_WIDTH // 2 + margen + columna * TRIANGLE_WIDTH
            y = HEIGHT - margen

        return (x, y)

    def dibujar_triangulo(self, punto_index, es_superior):
        """Dibuja un triángulo del tablero (claro u oscuro) en su posición correspondiente."""
        x, y = self.obtener_posicion_triangulo(punto_index)
        color = COLOR_TRIANGULO_CLARO if punto_index % 2 == 0 else COLOR_TRIANGULO_OSCURO

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
        """Dibuja el número identificador de un punto sobre el tablero."""
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
        """Dibuja el borde exterior y el marco interior del tablero."""
        pygame.draw.rect(self.__screen, COLOR_MARCO_OSCURO, (0, 0, WIDTH, HEIGHT), 15)
        pygame.draw.rect(self.__screen, COLOR_MARCO_CLARO, (10, 10, WIDTH - 20, HEIGHT - 20), 8)
    
    def dibujar_bar(self):
        """Dibuja la barra central (separador de los cuadrantes del tablero)."""
        bar_x = WIDTH // 2 - BAR_WIDTH // 2
        pygame.draw.rect(self.__screen, COLOR_BAR, (bar_x - 5, 10, BAR_WIDTH + 10, HEIGHT - 20))
        pygame.draw.rect(self.__screen, COLOR_MARCO_CLARO, (bar_x, 10, BAR_WIDTH, HEIGHT - 20))
    
    def dibujar_fichas_barra(self):
        """Dibuja las fichas capturadas (en la barra central)."""
        bar_x = WIDTH // 2
        radio = 15
        
        # Fichas blancas (parte superior)
        fichas_blancas = self.__game.board.contenedor_blancas
        if fichas_blancas:
            y_start = 100
            for i, ficha in enumerate(fichas_blancas[:6]):  # Muestra hasta 6 fichas apiladas
                y_pos = y_start + i * (radio * 2 + 2)
                pygame.draw.circle(self.__screen, COLOR_FICHA_BLANCA, (bar_x, y_pos), radio)
                pygame.draw.circle(self.__screen, (0, 0, 0), (bar_x, y_pos), radio, 2)
            
            # Contador si hay más de 6 fichas
            if len(fichas_blancas) > 6:
                texto = self.__font_small.render(f"+{len(fichas_blancas) - 6}", True, (255, 255, 255))
                texto_rect = texto.get_rect(center=(bar_x, y_start + 6 * (radio * 2 + 2) + 15))
                pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(8, 4))
                self.__screen.blit(texto, texto_rect)
        
        # Fichas negras (parte inferior)
        fichas_negras = self.__game.board.contenedor_negras
        if fichas_negras:
            y_start = HEIGHT - 100
            for i, ficha in enumerate(fichas_negras[:6]):
                y_pos = y_start - i * (radio * 2 + 2)
                pygame.draw.circle(self.__screen, COLOR_FICHA_NEGRA, (bar_x, y_pos), radio)
                pygame.draw.circle(self.__screen, (0, 0, 0), (bar_x, y_pos), radio, 2)
            
            if len(fichas_negras) > 6:
                texto = self.__font_small.render(f"+{len(fichas_negras) - 6}", True, (255, 255, 255))
                texto_rect = texto.get_rect(center=(bar_x, y_start - 6 * (radio * 2 + 2) - 15))
                pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(8, 4))
                self.__screen.blit(texto, texto_rect)
    
    def dibujar_fichas(self, punto_index):
        """Dibuja todas las fichas presentes en un punto del tablero."""
        fichas = self.__game.board.obtener_fichas(punto_index)
        if not fichas:
            return

        x_base, y_base = self.obtener_posicion_triangulo(punto_index)
        x_centro = x_base + TRIANGLE_WIDTH // 2
        radio = 15
        es_superior = punto_index < 12

        for i, ficha in enumerate(fichas[:5]):  # Muestra hasta 5 fichas apiladas
            color = COLOR_FICHA_BLANCA if ficha.color == ColorFicha.BLANCA else COLOR_FICHA_NEGRA
            y_ficha = y_base + 20 + i * (radio * 2 + 2) if es_superior else y_base - 20 - i * (radio * 2 + 2)
            pygame.draw.circle(self.__screen, color, (x_centro, y_ficha), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (x_centro, y_ficha), radio, 2)
        
        # Muestra un contador si hay más de 5 fichas
        if len(fichas) > 5:
            texto = self.__font_small.render(str(len(fichas)), True, (255, 255, 0))
            y_texto = (y_base + 20 + 4 * (radio * 2 + 2) + 5) if es_superior else (y_base - 20 - 4 * (radio * 2 + 2) - 5)
            texto_rect = texto.get_rect(center=(x_centro, y_texto))
            pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(6, 4))
            self.__screen.blit(texto, texto_rect)
    
    def obtener_punto_clickeado(self, pos_mouse):
        """Determina el índice del punto clickeado, o None si no se clickeó ninguno."""
        mouse_x, mouse_y = pos_mouse
        
        for i in range(24):
            x_base, y_base = self.obtener_posicion_triangulo(i)
            es_superior = i < 12
            
            if x_base <= mouse_x <= x_base + TRIANGLE_WIDTH:
                if es_superior and y_base <= mouse_y <= y_base + TRIANGLE_HEIGHT:
                    return i
                if not es_superior and y_base - TRIANGLE_HEIGHT <= mouse_y <= y_base:
                    return i
        
        return None
    
    def resaltar_punto(self, punto_index):
        """Dibuja un contorno resaltado alrededor de un punto del tablero."""
        x, y = self.obtener_posicion_triangulo(punto_index)
        es_superior = punto_index < 12
        
        if es_superior:
            puntos = [(x, y), (x + TRIANGLE_WIDTH, y), (x + TRIANGLE_WIDTH // 2, y + TRIANGLE_HEIGHT)]
        else:
            puntos = [(x, y), (x + TRIANGLE_WIDTH, y), (x + TRIANGLE_WIDTH // 2, y - TRIANGLE_HEIGHT)]
        
        pygame.draw.polygon(self.__screen, (255, 255, 0), puntos, 4)
    
    def dibujar_tablero_completo(self):
        """Redibuja el tablero completo con triángulos, fichas y barra central."""
        self.__screen.fill(COLOR_FONDO)
        self.dibujar_marco()
        self.dibujar_bar()
        
        # Dibuja triángulos y numeración
        for i in range(24):
            es_superior = i < 12
            self.dibujar_triangulo(i, es_superior)
            self.dibujar_numero_punto(i)
        
        # Dibuja las fichas sobre los puntos
        for i in range(24):
            self.dibujar_fichas(i)
        
        # Dibuja las fichas que están en la barra
        self.dibujar_fichas_barra()
