"""Módulo de interfaz gráfica usando Pygame - SOLO PRESENTACIÓN, LÓGICA EN CORE."""
import pygame
import sys
from core.BackgammonGame import BackgammonGame
from pygame_ui.tablero_renderer import TableroRenderer
from pygame_ui.dados_renderer import DadosRenderer
from pygame_ui.info_panel import InfoPanel
from pygame_ui.input_handler import InputHandler
from pygame_ui.pantalla_inicio import PantallaInicio
from pygame_ui.pantalla_victoria import PantallaVictoria

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
    
    jugar_otra = True
    
    while jugar_otra:
        # ========== PANTALLA DE INICIO ==========
        pantalla_inicio = PantallaInicio(screen)
        nombre_jugador1, nombre_jugador2 = pantalla_inicio.ejecutar()
        
        # CORE: Crear juego
        game = BackgammonGame(nombre_jugador1, nombre_jugador2)
        game.start_game()
        
        # PRESENTACIÓN: Crear renderizadores
        tablero_renderer = TableroRenderer(screen, game)
        dados_renderer = DadosRenderer(screen, game)
        info_panel = InfoPanel(screen, game)
        input_handler = InputHandler(game, tablero_renderer)
        
        mensaje = None
        font_mensaje = pygame.font.SysFont('Arial', 18)
        
        running = True
        while running:
            # CORE: Verificar fin de juego
            if game.is_game_over:
                pantalla_victoria = PantallaVictoria(screen, game.winner.nombre)
                resultado = pantalla_victoria.ejecutar()
                
                if resultado == 'nueva':
                    break
                else:
                    jugar_otra = False
                    running = False
                    continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    jugar_otra = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mensaje = input_handler.manejar_click(event.pos)
                        if mensaje:
                            print(mensaje)
                            # Verificar fin de turno
                            if "movida" in mensaje.lower() or "captura" in mensaje.lower() or "sacada" in mensaje.lower() or "entrada" in mensaje.lower():
                                fin_turno = input_handler.verificar_fin_turno()
                                if fin_turno:
                                    mensaje = fin_turno
                                    print(fin_turno)
                                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        mensaje = input_handler.lanzar_dados()
                        print(mensaje)
                        # Verificar si hay fichas en barra sin entrada posible
                        fin_turno_barra = input_handler.verificar_fin_turno()
                        if fin_turno_barra and "turno perdido" in fin_turno_barra.lower():
                            mensaje = fin_turno_barra
                            print(fin_turno_barra)
                    elif event.key == pygame.K_ESCAPE:
                        input_handler.cancelar_seleccion()
                        mensaje = "Selección cancelada"
                        print(mensaje)
                    elif event.key == pygame.K_RETURN:
                        if game.dice.last_raw_roll and game.dice.get_moves_remaining() == 0:
                            jugador_anterior = game.current_player.nombre
                            # CORE: Terminar turno
                            game.end_turn()
                            mensaje = f"Turno pasado. Turno de {game.current_player.nombre}"
                            print(mensaje)
            
            # PRESENTACIÓN: Renderizar
            tablero_renderer.dibujar_tablero_completo()
            dados_renderer.dibujar_dados()
            info_panel.dibujar_info_turno()
            
            # PRESENTACIÓN: Resaltar punto seleccionado
            if input_handler.punto_origen is not None and input_handler.punto_origen >= 0:
                tablero_renderer.resaltar_punto(input_handler.punto_origen)
            
            # PRESENTACIÓN: Mostrar mensaje
            if mensaje:
                if "Error" in mensaje or "inválido" in mensaje or "bloqueado" in mensaje or "Debes" in mensaje:
                    color_msg = (255, 100, 100)
                elif "Turno de" in mensaje or "Dados:" in mensaje or "sacada" in mensaje or "Captura" in mensaje or "VICTORIA" in mensaje:
                    color_msg = (100, 255, 100)
                else:
                    color_msg = (255, 255, 255)
                
                pygame.draw.rect(screen, (40, 40, 40), (WIDTH//2 - 300, 30, 600, 40), border_radius=5)
                pygame.draw.rect(screen, (100, 100, 100), (WIDTH//2 - 300, 30, 600, 40), 2, border_radius=5)
                
                texto_msg = font_mensaje.render(mensaje, True, color_msg)
                texto_rect = texto_msg.get_rect(center=(WIDTH//2, 50))
                screen.blit(texto_msg, texto_rect)
            
            # PRESENTACIÓN: Advertencia de barra (usando CORE)
            if game.tiene_fichas_en_barra(game.current_player.color) and game.dice.last_raw_roll:
                font_advertencia = pygame.font.SysFont('Arial', 20, bold=True)
                texto_adv = font_advertencia.render("¡Debes mover fichas de la barra primero!", True, (255, 255, 0))
                rect_adv = texto_adv.get_rect(center=(WIDTH//2, 85))
                pygame.draw.rect(screen, (50, 50, 50), rect_adv.inflate(20, 10), border_radius=5)
                screen.blit(texto_adv, rect_adv)
            
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()