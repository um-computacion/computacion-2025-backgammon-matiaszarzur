"""Renderizador del tablero de backgammon - SOLO PRESENTACIÓN."""
import pygame
from core.ColorFicha import ColorFicha

# Constantes
WIDTH = 1200
HEIGHT = 800
TRIANGLE_WIDTH = 70  # ← Reducido de 80 a 70
TRIANGLE_HEIGHT = 250
BAR_WIDTH = 40
BEAR_OFF_WIDTH = 100

COLOR_FONDO = (139, 90, 43)
COLOR_MARCO_OSCURO = (50, 30, 10)
COLOR_MARCO_CLARO = (100, 60, 30)
COLOR_BAR = (60, 40, 15)
COLOR_TRIANGULO_CLARO = (200, 200, 200)
COLOR_TRIANGULO_OSCURO = (100, 50, 30)
COLOR_FICHA_BLANCA = (255, 255, 255)
COLOR_FICHA_NEGRA = (50, 50, 50)
COLOR_BEAR_OFF = (40, 60, 40)


class TableroRenderer:
    """Clase responsable de DIBUJAR el tablero. NO contiene lógica de negocio."""
    
    def __init__(self, screen, game):
        """Inicializar el renderizador.
        
        Args:
            screen: Superficie de pygame
            game (BackgammonGame): Instancia del juego del CORE
        """
        self.__screen = screen
        self.__game = game
        self.__font = pygame.font.SysFont('Arial', 16)
        self.__font_small = pygame.font.SysFont('Arial', 12, bold=True)
        self.__font_bear_off = pygame.font.SysFont('Arial', 24, bold=True)
    
    def obtener_posicion_triangulo(self, punto_index):
        """Obtiene la posición base de un triángulo."""
        margen = 30
        gap_barra = 15  # Espacio extra alrededor de la barra para evitar superposición

        if punto_index < 12:
            if punto_index < 6:
                columna = 5 - punto_index
                x = WIDTH // 2 + BAR_WIDTH // 2 + gap_barra + columna * TRIANGLE_WIDTH
            else:
                columna = 11 - punto_index
                x = margen + BEAR_OFF_WIDTH + columna * TRIANGLE_WIDTH
            y = margen
        else:
            if punto_index < 18:
                columna = punto_index - 12
                x = margen + BEAR_OFF_WIDTH + columna * TRIANGLE_WIDTH
            else:
                columna = punto_index - 18
                x = WIDTH // 2 + BAR_WIDTH // 2 + gap_barra + columna * TRIANGLE_WIDTH
            y = HEIGHT - margen

        return (x, y)

    def dibujar_triangulo(self, punto_index, es_superior):
        """Dibuja un triángulo."""
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
        """Dibuja el número del punto."""
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
        """Dibuja la barra central."""
        bar_x = WIDTH // 2 - BAR_WIDTH // 2
        # Solo el fondo de la barra, sin bordes extras
        pygame.draw.rect(self.__screen, COLOR_BAR, (bar_x, 30, BAR_WIDTH, HEIGHT-60))
    
    def dibujar_zonas_bear_off(self):
        """Dibuja las zonas de bear off."""
        margen = 30
        
        # Zona izquierda (negras)
        bear_off_izq_x = margen
        bear_off_izq_y = HEIGHT // 2 - 150
        pygame.draw.rect(self.__screen, COLOR_BEAR_OFF, 
                        (bear_off_izq_x, bear_off_izq_y, BEAR_OFF_WIDTH, 300))
        pygame.draw.rect(self.__screen, COLOR_MARCO_CLARO, 
                        (bear_off_izq_x, bear_off_izq_y, BEAR_OFF_WIDTH, 300), 3)
        
        texto_off = self.__font.render("BEAR", True, (200, 200, 200))
        texto_off2 = self.__font.render("OFF", True, (200, 200, 200))
        self.__screen.blit(texto_off, (bear_off_izq_x + 25, bear_off_izq_y + 130))
        self.__screen.blit(texto_off2, (bear_off_izq_x + 30, bear_off_izq_y + 150))
        
        # Zona derecha (blancas)
        bear_off_der_x = WIDTH - margen - BEAR_OFF_WIDTH
        bear_off_der_y = HEIGHT // 2 - 150
        pygame.draw.rect(self.__screen, COLOR_BEAR_OFF, 
                        (bear_off_der_x, bear_off_der_y, BEAR_OFF_WIDTH, 300))
        pygame.draw.rect(self.__screen, COLOR_MARCO_CLARO, 
                        (bear_off_der_x, bear_off_der_y, BEAR_OFF_WIDTH, 300), 3)
        
        self.__screen.blit(texto_off, (bear_off_der_x + 25, bear_off_der_y + 130))
        self.__screen.blit(texto_off2, (bear_off_der_x + 30, bear_off_der_y + 150))
        
        self.__dibujar_fichas_bear_off()
    
    def __dibujar_fichas_bear_off(self):
        """Dibuja las fichas sacadas (usa datos del CORE)."""
        margen = 30
        radio = 15
        
        # CORE: Obtener contadores
        fichas_blancas = self.__game.fichas_fuera_blancas
        if fichas_blancas > 0:
            bear_off_x = WIDTH - margen - BEAR_OFF_WIDTH // 2
            bear_off_y = HEIGHT // 2 - 100
            
            for i in range(min(fichas_blancas, 5)):
                y_pos = bear_off_y + i * (radio * 2 + 2)
                pygame.draw.circle(self.__screen, COLOR_FICHA_BLANCA, (bear_off_x, y_pos), radio)
                pygame.draw.circle(self.__screen, (0, 0, 0), (bear_off_x, y_pos), radio, 2)
            
            texto_count = self.__font_bear_off.render(f"{fichas_blancas}/15", True, (255, 255, 0))
            texto_rect = texto_count.get_rect(center=(bear_off_x, bear_off_y + 200))
            pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(10, 5))
            self.__screen.blit(texto_count, texto_rect)
        
        # CORE: Obtener contadores
        fichas_negras = self.__game.fichas_fuera_negras
        if fichas_negras > 0:
            bear_off_x = margen + BEAR_OFF_WIDTH // 2
            bear_off_y = HEIGHT // 2 + 100
            
            for i in range(min(fichas_negras, 5)):
                y_pos = bear_off_y - i * (radio * 2 + 2)
                pygame.draw.circle(self.__screen, COLOR_FICHA_NEGRA, (bear_off_x, y_pos), radio)
                pygame.draw.circle(self.__screen, (0, 0, 0), (bear_off_x, y_pos), radio, 2)
            
            texto_count = self.__font_bear_off.render(f"{fichas_negras}/15", True, (255, 255, 0))
            texto_rect = texto_count.get_rect(center=(bear_off_x, bear_off_y - 200))
            pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(10, 5))
            self.__screen.blit(texto_count, texto_rect)
    
    def dibujar_fichas_barra(self):
        """Dibuja las fichas en la barra (usa datos del CORE)."""
        bar_x = WIDTH // 2
        radio = 15
        
        # CORE: Obtener fichas blancas
        fichas_blancas = self.__game.board.contenedor_blancas
        if fichas_blancas:
            y_start = 100
            for i, ficha in enumerate(fichas_blancas[:6]):
                y_pos = y_start + i * (radio * 2 + 2)
                pygame.draw.circle(self.__screen, COLOR_FICHA_BLANCA, (bar_x, y_pos), radio)
                pygame.draw.circle(self.__screen, (0, 0, 0), (bar_x, y_pos), radio, 2)
            
            if len(fichas_blancas) > 6:
                texto = self.__font_small.render(f"+{len(fichas_blancas)-6}", True, (255, 255, 255))
                texto_rect = texto.get_rect(center=(bar_x, y_start + 6 * (radio * 2 + 2) + 15))
                pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(8, 4))
                self.__screen.blit(texto, texto_rect)
        
        # CORE: Obtener fichas negras
        fichas_negras = self.__game.board.contenedor_negras
        if fichas_negras:
            y_start = HEIGHT - 100
            for i, ficha in enumerate(fichas_negras[:6]):
                y_pos = y_start - i * (radio * 2 + 2)
                pygame.draw.circle(self.__screen, COLOR_FICHA_NEGRA, (bar_x, y_pos), radio)
                pygame.draw.circle(self.__screen, (0, 0, 0), (bar_x, y_pos), radio, 2)
            
            if len(fichas_negras) > 6:
                texto = self.__font_small.render(f"+{len(fichas_negras)-6}", True, (255, 255, 255))
                texto_rect = texto.get_rect(center=(bar_x, y_start - 6 * (radio * 2 + 2) - 15))
                pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(8, 4))
                self.__screen.blit(texto, texto_rect)
    
    def dibujar_fichas(self, punto_index):
        """Dibuja las fichas en un punto (usa datos del CORE)."""
        # CORE: Obtener fichas del punto
        fichas = self.__game.board.obtener_fichas(punto_index)

        if not fichas:
            return

        x_base, y_base = self.obtener_posicion_triangulo(punto_index)
        x_centro = x_base + TRIANGLE_WIDTH // 2
        radio = 15
        es_superior = punto_index < 12

        for i, ficha in enumerate(fichas[:5]):
            color = COLOR_FICHA_BLANCA if ficha.color == ColorFicha.BLANCA else COLOR_FICHA_NEGRA

            if es_superior:
                y_ficha = y_base + 20 + i * (radio * 2 + 2)
            else:
                y_ficha = y_base - 20 - i * (radio * 2 + 2)

            pygame.draw.circle(self.__screen, color, (x_centro, y_ficha), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (x_centro, y_ficha), radio, 2)
        
        if len(fichas) > 5:
            texto = self.__font_small.render(str(len(fichas)), True, (255, 255, 0))
            if es_superior:
                y_texto = y_base + 20 + 4 * (radio * 2 + 2) + 5
            else:
                y_texto = y_base - 20 - 4 * (radio * 2 + 2) - 5
            
            texto_rect = texto.get_rect(center=(x_centro, y_texto))
            pygame.draw.rect(self.__screen, (0, 0, 0), texto_rect.inflate(6, 4))
            self.__screen.blit(texto, texto_rect)
    
    def obtener_punto_clickeado(self, pos_mouse):
        """Detecta en qué punto se hizo click."""
        mouse_x, mouse_y = pos_mouse
        
        for i in range(24):
            x_base, y_base = self.obtener_posicion_triangulo(i)
            es_superior = i < 12
            
            if x_base <= mouse_x <= x_base + TRIANGLE_WIDTH:
                if es_superior:
                    if y_base <= mouse_y <= y_base + TRIANGLE_HEIGHT:
                        return i
                else:
                    if y_base - TRIANGLE_HEIGHT <= mouse_y <= y_base:
                        return i
        
        return None
    
    def obtener_click_barra(self, pos_mouse):
        """Detecta si se hizo click en la barra."""
        mouse_x, mouse_y = pos_mouse
        bar_x = WIDTH // 2 - BAR_WIDTH // 2
        
        if bar_x <= mouse_x <= bar_x + BAR_WIDTH:
            if mouse_y < HEIGHT // 2:
                return ColorFicha.BLANCA
            else:
                return ColorFicha.NEGRA
        
        return None
    
    def obtener_click_bear_off(self, pos_mouse):
        """Detecta si se hizo click en zona de bear off."""
        mouse_x, mouse_y = pos_mouse
        margen = 30
        bear_off_y = HEIGHT // 2 - 150
        
        # Zona izquierda (negras)
        if margen <= mouse_x <= margen + BEAR_OFF_WIDTH:
            if bear_off_y <= mouse_y <= bear_off_y + 300:
                return ColorFicha.NEGRA
        
        # Zona derecha (blancas)
        bear_off_der_x = WIDTH - margen - BEAR_OFF_WIDTH
        if bear_off_der_x <= mouse_x <= bear_off_der_x + BEAR_OFF_WIDTH:
            if bear_off_y <= mouse_y <= bear_off_y + 300:
                return ColorFicha.BLANCA
        
        return None
    
    def resaltar_punto(self, punto_index):
        """Resalta un punto seleccionado."""
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
        """Dibuja todo el tablero."""
        self.__screen.fill(COLOR_FONDO)
        self.dibujar_marco()
        self.dibujar_bar()  
        self.dibujar_zonas_bear_off()
        
        for i in range(24):
            es_superior = i < 12
            self.dibujar_triangulo(i, es_superior)  
            self.dibujar_numero_punto(i)
        
        for i in range(24):
            self.dibujar_fichas(i)
        
        self.dibujar_fichas_barra()