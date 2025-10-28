"""Pantalla de entrada de nombres de jugadores."""
import pygame
import sys

# Constantes
WIDTH = 1200
HEIGHT = 800
COLOR_FONDO = (139, 90, 43)
COLOR_PANEL = (80, 50, 20)
COLOR_BORDE = (100, 60, 30)
COLOR_INPUT_ACTIVO = (255, 255, 255)
COLOR_INPUT_INACTIVO = (200, 200, 200)
COLOR_TEXTO = (255, 255, 255)


class InputBox:
    """Caja de input para texto."""
    
    def __init__(self, x, y, w, h, placeholder=''):
        """Inicializar caja de input.
        
        Args:
            x (int): Posición x
            y (int): Posición y
            w (int): Ancho
            h (int): Alto
            placeholder (str): Texto de ejemplo
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INPUT_INACTIVO
        self.text = ''
        self.placeholder = placeholder
        self.font = pygame.font.SysFont('Arial', 24)
        self.active = False
        self.max_length = 20
    
    def handle_event(self, event):
        """Manejar eventos del input.
        
        Args:
            event: Evento de pygame
            
        Returns:
            bool: True si se presionó Enter con texto válido
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle activo/inactivo al hacer click
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = COLOR_INPUT_ACTIVO
            else:
                self.active = False
                self.color = COLOR_INPUT_INACTIVO
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if self.text.strip():  # Solo si hay texto válido
                    return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Añadir caracter si no excede el límite
                if len(self.text) < self.max_length:
                    self.text += event.unicode
        
        return False
    
    def draw(self, screen):
        """Dibujar el input box."""
        # Dibujar rectángulo
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 3)
        
        # Dibujar texto o placeholder
        if self.text:
            txt_surface = self.font.render(self.text, True, (0, 0, 0))
        else:
            txt_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        
        # Centrar texto verticalmente
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + (self.rect.h - txt_surface.get_height()) // 2))


class PantallaInicio:
    """Pantalla para pedir nombres de jugadores."""
    
    def __init__(self, screen):
        """Inicializar pantalla de inicio.
        
        Args:
            screen: Superficie de pygame
        """
        self.screen = screen
        self.font_titulo = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_subtitulo = pygame.font.SysFont('Arial', 24)
        self.font_instruccion = pygame.font.SysFont('Arial', 18)
        
        # Crear inputs
        center_x = WIDTH // 2
        self.input_jugador1 = InputBox(center_x - 200, 300, 400, 50, 'Jugador 1')
        self.input_jugador2 = InputBox(center_x - 200, 400, 400, 50, 'Jugador 2')
        
        # Botón de inicio
        self.boton_rect = pygame.Rect(center_x - 100, 500, 200, 60)
        
        # Estado
        self.jugador1_listo = False
    
    def ejecutar(self):
        """Ejecutar la pantalla de inicio y retornar nombres.
        
        Returns:
            tuple: (nombre_jugador1, nombre_jugador2)
        """
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Manejar inputs
                if self.input_jugador1.handle_event(event):
                    self.jugador1_listo = True
                    self.input_jugador1.active = False
                    self.input_jugador2.active = True
                    self.input_jugador2.color = COLOR_INPUT_ACTIVO
                
                if self.input_jugador2.handle_event(event):
                    # Si ambos tienen nombres, continuar
                    if self.input_jugador1.text.strip():
                        return self._validar_y_retornar()
                
                # Click en botón
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_rect.collidepoint(event.pos):
                        resultado = self._validar_y_retornar()
                        if resultado:
                            return resultado
            
            # Renderizar
            self._dibujar()
            pygame.display.flip()
            clock.tick(60)
    
    def _validar_y_retornar(self):
        """Validar nombres y retornarlos si son válidos.
        
        Returns:
            tuple o None: (nombre1, nombre2) si son válidos, None si no
        """
        nombre1 = self.input_jugador1.text.strip()
        nombre2 = self.input_jugador2.text.strip()
        
        if nombre1 and nombre2:
            return (nombre1, nombre2)
        return None
    
    def _dibujar(self):
        """Dibujar la pantalla de inicio."""
        # Fondo
        self.screen.fill(COLOR_FONDO)
        
        # Panel principal
        panel_rect = pygame.Rect(WIDTH//2 - 350, 100, 700, 550)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_BORDE, panel_rect, 4, border_radius=10)
        
        # Título
        titulo = self.font_titulo.render("BACKGAMMON", True, COLOR_TEXTO)
        titulo_rect = titulo.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(titulo, titulo_rect)
        
        # Subtítulo jugador 1
        subtitulo1 = self.font_subtitulo.render("Jugador 1 (Blancas):", True, COLOR_TEXTO)
        subtitulo1_rect = subtitulo1.get_rect(center=(WIDTH//2, 270))
        self.screen.blit(subtitulo1, subtitulo1_rect)
        
        # Input jugador 1
        self.input_jugador1.draw(self.screen)
        
        # Subtítulo jugador 2
        subtitulo2 = self.font_subtitulo.render("Jugador 2 (Negras):", True, COLOR_TEXTO)
        subtitulo2_rect = subtitulo2.get_rect(center=(WIDTH//2, 370))
        self.screen.blit(subtitulo2, subtitulo2_rect)
        
        # Input jugador 2
        self.input_jugador2.draw(self.screen)
        
        # Botón de inicio
        mouse_pos = pygame.mouse.get_pos()
        boton_hover = self.boton_rect.collidepoint(mouse_pos)
        
        # Verificar si se puede iniciar
        puede_iniciar = self.input_jugador1.text.strip() and self.input_jugador2.text.strip()
        
        if puede_iniciar:
            boton_color = (100, 200, 100) if boton_hover else (50, 150, 50)
        else:
            boton_color = (100, 100, 100)
        
        pygame.draw.rect(self.screen, boton_color, self.boton_rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 200, 200), self.boton_rect, 3, border_radius=8)
        
        boton_texto = self.font_subtitulo.render("JUGAR", True, COLOR_TEXTO)
        boton_texto_rect = boton_texto.get_rect(center=self.boton_rect.center)
        self.screen.blit(boton_texto, boton_texto_rect)
        
        # Instrucciones
        instruccion = self.font_instruccion.render(
            "Escribe los nombres y presiona ENTER o click en JUGAR", 
            True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(center=(WIDTH//2, 600))
        self.screen.blit(instruccion, instruccion_rect)