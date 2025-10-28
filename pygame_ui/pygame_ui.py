"""Módulo de interfaz gráfica usando Pygame."""
import pygame
import sys
from core.BackgammonGame import BackgammonGame
from pygame_ui.tablero_renderer import TableroRenderer
from pygame_ui.dados_renderer import DadosRenderer
from pygame_ui.info_panel import InfoPanel
from pygame_ui.input_handler import InputHandler
from pygame_ui.pantalla_inicio import PantallaInicio

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
    
    # ========== PANTALLA DE INICIO ==========
    pantalla_inicio = PantallaInicio(screen)
    nombre_jugador1, nombre_jugador2 = pantalla_inicio.ejecutar()
    
    # Crear juego con los nombres ingresados
    game = BackgammonGame(nombre_jugador1, nombre_jugador2)
    game.start_game()
    
    # Crear renderizadores (aplicando SRP)
    tablero_renderer = TableroRenderer(screen, game)
    dados_renderer = DadosRenderer(screen, game)
    info_panel = InfoPanel(screen, game)
    input_handler = InputHandler(game, tablero_renderer)
    
    mensaje = None
    font_mensaje = pygame.font.SysFont('Arial', 18)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    mensaje = input_handler.manejar_click(event.pos)
                    if mensaje:
                        print(mensaje)
                        # Verificar fin de turno automático
                        if "Ficha movida" in mensaje:
                            fin_turno = input_handler.verificar_fin_turno()
                            if fin_turno:
                                mensaje = fin_turno
                                print(fin_turno)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Lanzar dados
                    mensaje = input_handler.lanzar_dados()
                    print(mensaje)
                elif event.key == pygame.K_ESCAPE:  # Cancelar selección
                    input_handler.cancelar_seleccion()
                    mensaje = "Selección cancelada"
                    print(mensaje)
        
        # Renderizar (delegando responsabilidades)
        tablero_renderer.dibujar_tablero_completo()
        dados_renderer.dibujar_dados()
        info_panel.dibujar_info_turno()
        
        # Resaltar punto seleccionado
        if input_handler.punto_origen is not None:
            tablero_renderer.resaltar_punto(input_handler.punto_origen)
        
        # Mostrar mensaje en pantalla
        if mensaje:
            # Determinar color del mensaje
            if "Error" in mensaje or "invalido" in mensaje or "bloqueado" in mensaje:
                color_msg = (255, 100, 100)  # Rojo para errores
            elif "Turno de" in mensaje or "Dados:" in mensaje:
                color_msg = (100, 255, 100)  # Verde para cambios de estado
            else:
                color_msg = (255, 255, 255)  # Blanco para info general
            
            # Fondo del mensaje
            pygame.draw.rect(screen, (40, 40, 40), (WIDTH//2 - 250, 30, 500, 40), border_radius=5)
            pygame.draw.rect(screen, (100, 100, 100), (WIDTH//2 - 250, 30, 500, 40), 2, border_radius=5)
            
            # Texto del mensaje
            texto_msg = font_mensaje.render(mensaje, True, color_msg)
            texto_rect = texto_msg.get_rect(center=(WIDTH//2, 50))
            screen.blit(texto_msg, texto_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()