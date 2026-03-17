"""Pantalla de victoria del juego."""
import pygame
import sys

WIDTH = 1200
HEIGHT = 800
COLOR_FONDO = (139, 90, 43)
COLOR_PANEL = (80, 50, 20)
COLOR_BORDE = (100, 60, 30)


class PantallaVictoria:
    """Pantalla que se muestra cuando un jugador gana."""
    
    def __init__(self, screen, ganador_nombre):
        """Inicializar pantalla de victoria.
        
        Args:
            screen: Superficie de pygame
            ganador_nombre (str): Nombre del jugador ganador
        """
        self.__screen = screen
        self.__ganador = ganador_nombre
        self.__font_titulo = pygame.font.SysFont('Arial', 72, bold=True)
        self.__font_subtitulo = pygame.font.SysFont('Arial', 36)
        self.__font_boton = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Botones
        center_x = WIDTH // 2
        self.__boton_nueva = pygame.Rect(center_x - 250, 500, 220, 70)
        self.__boton_salir = pygame.Rect(center_x + 30, 500, 220, 70)
    
    def ejecutar(self):
        """Ejecutar la pantalla de victoria.
        
        Returns:
            str: 'nueva' para nueva partida, 'salir' para cerrar
        """
        clock = pygame.time.Clock()
        
        # Animación de entrada
        alpha = 0
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'salir'
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__boton_nueva.collidepoint(event.pos):
                        return 'nueva'
                    elif self.__boton_salir.collidepoint(event.pos):
                        return 'salir'
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return 'nueva'
                    elif event.key == pygame.K_ESCAPE:
                        return 'salir'
            
            # Dibujar pantalla
            self.__dibujar()
            
            # Efecto de fade-in (primeros 30 frames)
            if alpha < 255:
                alpha = min(255, alpha + 8)
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(255 - alpha)
                self.__screen.blit(fade_surface, (0, 0))
            
            pygame.display.flip()
            clock.tick(60)
    
    def __dibujar(self):
        """Dibujar la pantalla de victoria."""
        self.__screen.fill(COLOR_FONDO)
        
        # Panel principal
        panel_rect = pygame.Rect(WIDTH//2 - 400, 100, 800, 550)
        pygame.draw.rect(self.__screen, COLOR_PANEL, panel_rect, border_radius=15)
        pygame.draw.rect(self.__screen, COLOR_BORDE, panel_rect, 5, border_radius=15)
        
        # Título "¡VICTORIA!"
        titulo = self.__font_titulo.render("¡VICTORIA!", True, (255, 215, 0))
        titulo_rect = titulo.get_rect(center=(WIDTH//2, 180))
        # Sombra del título
        titulo_sombra = self.__font_titulo.render("¡VICTORIA!", True, (0, 0, 0))
        sombra_rect = titulo_sombra.get_rect(center=(WIDTH//2 + 3, 183))
        self.__screen.blit(titulo_sombra, sombra_rect)
        self.__screen.blit(titulo, titulo_rect)
        
        # Nombre del ganador
        texto_ganador = self.__font_subtitulo.render(f"Ganador: {self.__ganador}", True, (255, 255, 255))
        ganador_rect = texto_ganador.get_rect(center=(WIDTH//2, 280))
        self.__screen.blit(texto_ganador, ganador_rect)
        
        # Trofeo (emoji o texto)
        try:
            trofeo = self.__font_titulo.render("🏆", True, (255, 215, 0))
        except:
            # Fallback si no soporta emoji
            trofeo = self.__font_titulo.render("★", True, (255, 215, 0))
        trofeo_rect = trofeo.get_rect(center=(WIDTH//2, 360))
        self.__screen.blit(trofeo, trofeo_rect)
        
        # Mensaje de felicitaciones
        texto_felicidades = self.__font_subtitulo.render("¡Felicitaciones!", True, (255, 255, 255))
        felicidades_rect = texto_felicidades.get_rect(center=(WIDTH//2, 440))
        self.__screen.blit(texto_felicidades, felicidades_rect)
        
        # Botón Nueva Partida
        mouse_pos = pygame.mouse.get_pos()
        hover_nueva = self.__boton_nueva.collidepoint(mouse_pos)
        
        boton_nueva_color = (50, 150, 50) if not hover_nueva else (70, 200, 70)
        pygame.draw.rect(self.__screen, boton_nueva_color, self.__boton_nueva, border_radius=10)
        pygame.draw.rect(self.__screen, (200, 200, 200), self.__boton_nueva, 4, border_radius=10)
        
        texto_nueva = self.__font_boton.render("NUEVA PARTIDA", True, (255, 255, 255))
        nueva_rect = texto_nueva.get_rect(center=self.__boton_nueva.center)
        self.__screen.blit(texto_nueva, nueva_rect)
        
        # Botón Salir
        hover_salir = self.__boton_salir.collidepoint(mouse_pos)
        
        boton_salir_color = (150, 50, 50) if not hover_salir else (200, 70, 70)
        pygame.draw.rect(self.__screen, boton_salir_color, self.__boton_salir, border_radius=10)
        pygame.draw.rect(self.__screen, (200, 200, 200), self.__boton_salir, 4, border_radius=10)
        
        texto_salir = self.__font_boton.render("SALIR", True, (255, 255, 255))
        salir_rect = texto_salir.get_rect(center=self.__boton_salir.center)
        self.__screen.blit(texto_salir, salir_rect)
        
        # Instrucciones
        font_instruccion = pygame.font.SysFont('Arial', 16)
        instruccion = font_instruccion.render(
            "ENTER: Nueva partida  |  ESC: Salir", 
            True, (180, 180, 180)
        )
        instruccion_rect = instruccion.get_rect(center=(WIDTH//2, 620))
        self.__screen.blit(instruccion, instruccion_rect)