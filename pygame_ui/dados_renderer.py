"""Renderizador de dados."""
import pygame

WIDTH = 1200


class DadosRenderer:
    """Clase responsable de renderizar los dados."""
    
    def __init__(self, screen, game):
        """Inicializar el renderizador de dados."""
        self.__screen = screen
        self.__game = game
    
    def dibujar_dados(self):
        """Dibuja los dados si fueron lanzados."""
        if not self.__game.dice.last_roll:
            return
        
        dado_x = WIDTH // 2 - 80
        dado_y = 350
        
        dados = self.__game.dice.last_roll
        
        for i, valor in enumerate(dados):
            x = dado_x + i * 80
            
            pygame.draw.rect(self.__screen, (255, 255, 255), (x, dado_y, 60, 60), border_radius=8)
            pygame.draw.rect(self.__screen, (0, 0, 0), (x, dado_y, 60, 60), 3, border_radius=8)
            
            self.__dibujar_puntos_dado(x + 30, dado_y + 30, valor)

    def __dibujar_puntos_dado(self, centro_x, centro_y, valor):
        """Dibuja los puntos de un dado según su valor."""
        radio = 4
        offset = 12
        
        if valor == 1:
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x, centro_y), radio)
        elif valor == 2:
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y + offset), radio)
        elif valor == 3:
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x, centro_y), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y + offset), radio)
        elif valor == 4:
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y + offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y + offset), radio)
        elif valor == 5:
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x, centro_y), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y + offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y + offset), radio)
        elif valor == 6:
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y - offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x - offset, centro_y + offset), radio)
            pygame.draw.circle(self.__screen, (0, 0, 0), (centro_x + offset, centro_y + offset), radio)