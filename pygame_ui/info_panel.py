"""Panel de información del turno."""
import pygame
from core.ColorFicha import ColorFicha

# Constantes
WIDTH = 1200
HEIGHT = 800
COLOR_FICHA_BLANCA = (255, 255, 255)
COLOR_FICHA_NEGRA = (50, 50, 50)


class InfoPanel:
    """Clase responsable de mostrar información del turno."""
    
    def __init__(self, screen, game):
        """Inicializar el panel de información.
        
        Args:
            screen: Superficie de pygame donde dibujar
            game: Instancia de BackgammonGame
        """
        self.__screen = screen
        self.__game = game
        self.__font_titulo = pygame.font.SysFont('Arial', 20, bold=True)
        self.__font_normal = pygame.font.SysFont('Arial', 18)
    
    def dibujar_info_turno(self):
        """Dibuja la información del turno actual."""
        # Panel de información (lado derecho)
        panel_x = WIDTH - 250
        panel_y = HEIGHT // 2 - 150
        panel_width = 230
        panel_height = 300
        
        # Fondo del panel
        pygame.draw.rect(self.__screen, (80, 50, 20), 
                        (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.__screen, (100, 60, 30), 
                        (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Título
        texto_titulo = self.__font_titulo.render("TURNO ACTUAL", True, (255, 255, 255))
        self.__screen.blit(texto_titulo, (panel_x + 40, panel_y + 20))
        
        # Nombre del jugador
        jugador = self.__game.current_player.nombre
        texto_jugador = self.__font_normal.render(f"Jugador:", True, (255, 255, 255))
        self.__screen.blit(texto_jugador, (panel_x + 20, panel_y + 60))
        texto_nombre = self.__font_normal.render(jugador, True, (255, 255, 0))
        self.__screen.blit(texto_nombre, (panel_x + 20, panel_y + 85))
        
        # Color de fichas
        color_texto = "Blancas" if self.__game.current_player.color == ColorFicha.BLANCA else "Negras"
        texto_color = self.__font_normal.render(f"Color: {color_texto}", True, (255, 255, 255))
        self.__screen.blit(texto_color, (panel_x + 20, panel_y + 115))
        
        # Dibujar ficha de ejemplo
        ficha_y = panel_y + 150
        if self.__game.current_player.color == ColorFicha.BLANCA:
            pygame.draw.circle(self.__screen, COLOR_FICHA_BLANCA, 
                             (panel_x + 115, ficha_y), 20)
        else:
            pygame.draw.circle(self.__screen, COLOR_FICHA_NEGRA, 
                             (panel_x + 115, ficha_y), 20)
        pygame.draw.circle(self.__screen, (0, 0, 0), 
                         (panel_x + 115, ficha_y), 20, 2)
        
        # Estado del turno
        if self.__game.dice.last_roll:
            estado = "Puede mover"
            movimientos = self.__game.dice.get_moves_remaining()
            texto_estado = self.__font_normal.render(estado, True, (0, 255, 0))
            texto_movs = self.__font_normal.render(
                f"Movimientos: {movimientos}", True, (255, 255, 255))
            self.__screen.blit(texto_movs, (panel_x + 20, panel_y + 210))
        else:
            estado = "Lanzar dados"
            texto_estado = self.__font_normal.render(estado, True, (255, 200, 0))
        
        self.__screen.blit(texto_estado, (panel_x + 20, panel_y + 185))
        
        # Instrucciones
        inst_font = pygame.font.SysFont('Arial', 14)
        texto_inst = inst_font.render("ESPACIO: Dados", True, (200, 200, 200))
        self.__screen.blit(texto_inst, (panel_x + 20, panel_y + 250))