"""Módulo de interfaz gráfica usando Pygame."""
import pygame
import sys
from core.BackgammonGame import BackgammonGame
from pygame_ui.tablero_renderer import TableroRenderer
from pygame_ui.dados_renderer import DadosRenderer

# constantes
WIDTH = 1200
HEIGHT = 800
FPS = 60


def main():
    """Función principal del juego."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Backgammon")
    clock = pygame.time.Clock()
    
    # Crear juego
    game = BackgammonGame("Jugador 1", "Jugador 2")
    game.start_game()
    
    # Crear renderizadores (aplicando SRP)
    tablero_renderer = TableroRenderer(screen, game)
    dados_renderer = DadosRenderer(screen, game)
    
    punto_seleccionado = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    punto = tablero_renderer.obtener_punto_clickeado(event.pos)
                    if punto is not None:
                        punto_seleccionado = punto
                        print(f"Clickeaste el punto {punto + 1}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Barra espaciadora para lanzar dados
                    if not game.dice.last_roll:
                        game.roll_dice()
                        print(f"Dados: {game.dice.last_roll}")
        
        # Renderizar (delegando responsabilidades)
        tablero_renderer.dibujar_tablero_completo()
        dados_renderer.dibujar_dados()
        
        # Resaltar punto seleccionado
        if punto_seleccionado is not None:
            tablero_renderer.resaltar_punto(punto_seleccionado)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()