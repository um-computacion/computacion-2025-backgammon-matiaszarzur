"""Manejador de entrada del usuario para el juego de Backgammon."""
from core.ColorFicha import ColorFicha


class InputHandler:
    """Gestiona la interacción del usuario con el tablero y las fichas."""
    
    def __init__(self, game, tablero_renderer):
        """Inicializa el manejador con la lógica del juego y el renderizador del tablero."""
        self.__game = game
        self.__tablero_renderer = tablero_renderer
        self.__punto_origen = None
    
    @property
    def punto_origen(self):
        """Devuelve el punto de origen actualmente seleccionado."""
        return self.__punto_origen
    
    def manejar_click(self, pos_mouse):
        """Procesa un clic del usuario sobre el tablero."""
        punto = self.__tablero_renderer.obtener_punto_clickeado(pos_mouse)
        if punto is None:
            return None
        
        # No se puede mover si los dados no fueron lanzados
        if not self.__game.dice.last_raw_roll:
            return "Debes lanzar los dados primero"
        
        # No hay movimientos disponibles
        if self.__game.dice.get_moves_remaining() == 0:
            return "No hay movimientos disponibles"
        
        # Primer clic: se selecciona el punto de origen
        if self.__punto_origen is None:
            fichas = self.__game.board.obtener_fichas(punto)
            if not fichas:
                return "No hay fichas en ese punto"
            
            # Se verifica que las fichas pertenezcan al jugador actual
            if not all(ficha.color == self.__game.current_player.color for ficha in fichas):
                return "Esas no son tus fichas"
            
            self.__punto_origen = punto
            return f"Ficha seleccionada en punto {punto + 1}"
        
        # Segundo clic: se intenta realizar el movimiento
        else:
            punto_destino = punto
            resultado = self.__intentar_movimiento(self.__punto_origen, punto_destino)
            self.__punto_origen = None
            return resultado
    
    def __intentar_movimiento(self, origen, destino):
        """Valida y ejecuta un intento de movimiento."""
        color = self.__game.current_player.color
        
        # Determina la dirección del movimiento según el color
        if color == ColorFicha.BLANCA:
            if destino >= origen:
                return "Las blancas se mueven hacia números menores"
            distancia = origen - destino
        else:
            if destino <= origen:
                return "Las negras se mueven hacia números mayores"
            distancia = destino - origen
        
        # Comprueba que la distancia esté en los dados disponibles
        movimientos = list(self.__game.dice.last_roll)
        if distancia not in movimientos:
            return f"Movimiento inválido. Dados disponibles: {movimientos}"
        
        # Verifica que haya fichas en el punto de origen
        fichas_origen = self.__game.board.obtener_fichas(origen)
        if not fichas_origen:
            return "No hay fichas en el origen"
        
        fichas_destino = self.__game.board.obtener_fichas(destino)
        
        # Controla posibles capturas o bloqueos
        if fichas_destino:
            if fichas_destino[0].color != color:
                if len(fichas_destino) == 1:
                    return self.__ejecutar_movimiento_con_captura(origen, destino, distancia)
                else:
                    return "El punto destino está bloqueado por el oponente"
        
        # Movimiento normal (sin captura)
        return self.__ejecutar_movimiento_normal(origen, destino, distancia)
    
    def __ejecutar_movimiento_normal(self, origen, destino, distancia):
        """Realiza un movimiento sin captura."""
        try:
            ficha = self.__game.board.quitar_ficha(origen)
            if ficha is None:
                return "Error: no se pudo quitar la ficha"
            
            self.__game.board.agregar_ficha(destino, ficha)
            self.__game.dice.use_move(distancia)
            return f"Ficha movida de {origen + 1} a {destino + 1}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def __ejecutar_movimiento_con_captura(self, origen, destino, distancia):
        """Realiza un movimiento en el que se captura una ficha del oponente."""
        try:
            ficha_propia = self.__game.board.quitar_ficha(origen)
            if ficha_propia is None:
                return "Error: no se pudo quitar la ficha"
            
            ficha_enemiga = self.__game.board.quitar_ficha(destino)
            if ficha_enemiga is None:
                # Reversión: se devuelve la ficha propia al origen
                self.__game.board.agregar_ficha(origen, ficha_propia)
                return "Error: no se pudo capturar la ficha enemiga"
            
            # Envía la ficha capturada al contenedor (barra)
            self.__game.board.agregar_ficha_contenedor(ficha_enemiga)
            self.__game.board.agregar_ficha(destino, ficha_propia)
            self.__game.dice.use_move(distancia)
            
            return f"¡Captura! Ficha movida de {origen + 1} a {destino + 1}"
        except Exception as e:
            return f"Error en captura: {str(e)}"
    
    def verificar_fin_turno(self):
        """Verifica si el turno debe finalizar automáticamente."""
        if self.__game.dice.last_raw_roll and self.__game.dice.get_moves_remaining() == 0:
            jugador_anterior = self.__game.current_player.nombre
            self.__game.end_turn()
            return f"Fin del turno de {jugador_anterior}. Turno de {self.__game.current_player.nombre}"
        return None
    
    def cancelar_seleccion(self):
        """Cancela el punto seleccionado actualmente."""
        self.__punto_origen = None
    
    def lanzar_dados(self):
        """Lanza los dados si todavía no fueron lanzados en el turno actual."""
        if self.__game.dice.last_raw_roll:
            return "Ya hay dados lanzados"
        
        self.__game.roll_dice()
        return f"Dados: {self.__game.dice.last_raw_roll}"
