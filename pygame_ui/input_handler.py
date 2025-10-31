"""Manejador de entrada del usuario - SOLO PRESENTACIÓN, LÓGICA EN EL CORE."""
from core.ColorFicha import ColorFicha


class InputHandler:
    """Traduce interacciones del usuario en llamadas al CORE.
    
    Esta clase NO contiene lógica de negocio, solo:
    1. Detecta clicks
    2. Llama métodos del CORE
    3. Retorna mensajes para mostrar
    """
    
    def __init__(self, game, tablero_renderer):
        """Inicializar el manejador de input.
        
        Args:
            game (BackgammonGame): Instancia del juego del core
            tablero_renderer (TableroRenderer): Renderizador del tablero
        """
        self.__game = game
        self.__tablero_renderer = tablero_renderer
        self.__punto_origen = None
        self.__origen_es_barra = False
    
    @property
    def punto_origen(self):
        """Obtener el punto de origen seleccionado."""
        return self.__punto_origen
    
    def manejar_click(self, pos_mouse):
        """Maneja el click del mouse en el tablero."""
        # Detectar tipo de click
        click_en_barra = self.__tablero_renderer.obtener_click_barra(pos_mouse)
        if click_en_barra is not None:
            return self.__manejar_click_barra(click_en_barra)
        
        click_en_bear_off = self.__tablero_renderer.obtener_click_bear_off(pos_mouse)
        if click_en_bear_off is not None:
            return self.__manejar_click_bear_off(click_en_bear_off)
        
        punto = self.__tablero_renderer.obtener_punto_clickeado(pos_mouse)
        
        if punto is None:
            return None
        
        # Validaciones básicas
        if not self.__game.dice.last_raw_roll:
            return "Debes lanzar los dados primero"
        
        if self.__game.dice.get_moves_remaining() == 0:
            return "No hay movimientos disponibles"
        
        # LÓGICA DEL CORE: Verificar barra SOLO si no estamos en segundo click
        if self.__punto_origen is None:  # ← Solo validar en primer click
            if self.__game.tiene_fichas_en_barra(self.__game.current_player.color):
                return "Debes mover las fichas de la barra primero"
        
        # Primer click: seleccionar
        if self.__punto_origen is None:
            fichas = self.__game.board.obtener_fichas(punto)
            
            if not fichas:
                return "No hay fichas en ese punto"
            
            if not all(ficha.color == self.__game.current_player.color for ficha in fichas):
                return "Esas no son tus fichas"
            
            self.__punto_origen = punto
            self.__origen_es_barra = False
            return f"Ficha seleccionada en punto {punto + 1}"
        
        # Segundo click: mover
        else:
            punto_destino = punto
            if self.__origen_es_barra:
                resultado = self.__intentar_reentry(punto_destino)
            else:
                resultado = self.__intentar_movimiento(self.__punto_origen, punto_destino)
            
            self.__punto_origen = None
            self.__origen_es_barra = False
            return resultado
    
    def __manejar_click_barra(self, color_clickeado):
        """Maneja click en la barra."""
        if not self.__game.dice.last_raw_roll:
            return "Debes lanzar los dados primero"
        
        if self.__game.dice.get_moves_remaining() == 0:
            return "No hay movimientos disponibles"
        
        if color_clickeado != self.__game.current_player.color:
            return "Esas no son tus fichas"
        
        # LÓGICA DEL CORE: Verificar fichas en barra
        if not self.__game.tiene_fichas_en_barra(color_clickeado):
            return "No hay fichas tuyas en la barra"
        
        self.__punto_origen = -1
        self.__origen_es_barra = True
        return "Ficha de la barra seleccionada. Click en el punto de entrada."
    
    def __manejar_click_bear_off(self, color_clickeado):
        """Maneja click en zona de bear off."""
        if self.__punto_origen is None or self.__origen_es_barra:
            return None
        
        if color_clickeado != self.__game.current_player.color:
            return "No puedes sacar fichas ahí"
        
        return self.__intentar_bear_off(self.__punto_origen)
    
    def __intentar_reentry(self, punto_destino):
        """Intenta re-entrar una ficha desde la barra.
        
        REGLA: Las fichas capturadas re-entran por el HOME del OPONENTE:
        - Blancas → entran por puntos 18-23 (home de negras)
        - Negras → entran por puntos 0-5 (home de blancas)
        """
        color = self.__game.current_player.color
        
        # BLANCAS entran por HOME de NEGRAS (puntos 18-23)
        if color == ColorFicha.BLANCA:
            if not (18 <= punto_destino <= 23):
                return "Las blancas entran por los puntos 19-24"
            # Dado necesario: punto 23→dado 1, punto 22→dado 2, ..., punto 18→dado 6
            # Vienen del "punto 24 imaginario": dado = 24 - punto
            dado_necesario = 24 - punto_destino
        # NEGRAS entran por HOME de BLANCAS (puntos 0-5)
        else:
            if not (0 <= punto_destino <= 5):
                return "Las negras entran por los puntos 1-6"
            # Las negras avanzan: dado = punto + 1
            dado_necesario = punto_destino + 1
        
        # Verificar dado disponible
        movimientos = list(self.__game.dice.last_roll)
        if dado_necesario not in movimientos:
            return f"No tienes el dado {dado_necesario} disponible. Dados: {movimientos}"
        
        # Verificar destino
        fichas_destino = self.__game.board.obtener_fichas(punto_destino)
        if fichas_destino:
            if fichas_destino[0].color != color:
                if len(fichas_destino) == 1:
                    return self.__ejecutar_reentry_con_captura(punto_destino, dado_necesario)
                else:
                    return f"El punto {punto_destino + 1} está bloqueado"
        
        return self.__ejecutar_reentry_normal(punto_destino, dado_necesario)
    
    def __ejecutar_reentry_normal(self, punto_destino, dado_usado):
        """Ejecuta re-entry usando métodos del CORE."""
        try:
            # CORE: Quitar de contenedor
            ficha = self.__game.board.quitar_ficha_contenedor(self.__game.current_player.color)
            if ficha is None:
                return "Error: No hay fichas en la barra"
            
            # CORE: Agregar a tablero
            self.__game.board.agregar_ficha(punto_destino, ficha)
            # CORE: Usar dado
            self.__game.dice.use_move(dado_usado)
            
            return f"Ficha re-entrada en punto {punto_destino + 1}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def __ejecutar_reentry_con_captura(self, punto_destino, dado_usado):
        """Ejecuta re-entry con captura usando métodos del CORE."""
        try:
            # CORE: Quitar de contenedor
            ficha_propia = self.__game.board.quitar_ficha_contenedor(self.__game.current_player.color)
            if ficha_propia is None:
                return "Error: No hay fichas en la barra"
            
            # CORE: Capturar
            ficha_enemiga = self.__game.board.quitar_ficha(punto_destino)
            if ficha_enemiga is None:
                self.__game.board.agregar_ficha_contenedor(ficha_propia)
                return "Error: No se pudo capturar"
            
            # CORE: Mover fichas
            self.__game.board.agregar_ficha_contenedor(ficha_enemiga)
            self.__game.board.agregar_ficha(punto_destino, ficha_propia)
            # CORE: Usar dado
            self.__game.dice.use_move(dado_usado)
            
            return f"¡Re-entrada con captura en punto {punto_destino + 1}!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def __intentar_bear_off(self, punto_origen):
        """Intenta sacar una ficha del tablero."""
        color = self.__game.current_player.color
        
        # LÓGICA DEL CORE: Verificar si puede hacer bear off
        if not self.__game.puede_hacer_bear_off(color):
            return "No puedes sacar fichas aún. Todas deben estar en tu home."
        
        # Verificar que la ficha está en home
        if color == ColorFicha.BLANCA:
            if not (0 <= punto_origen <= 5):
                return "Solo puedes sacar fichas desde tu home (puntos 1-6)"
            distancia_necesaria = punto_origen + 1
        else:
            if not (18 <= punto_origen <= 23):
                return "Solo puedes sacar fichas desde tu home (puntos 19-24)"
            distancia_necesaria = 24 - punto_origen
        
        # Verificar dados
        movimientos = list(self.__game.dice.last_roll)
        dados_validos = [d for d in movimientos if d >= distancia_necesaria]
        
        if not dados_validos:
            return f"Necesitas un dado de al menos {distancia_necesaria}. Dados: {movimientos}"
        
        dado_a_usar = min(dados_validos)
        return self.__ejecutar_bear_off(punto_origen, dado_a_usar)
    
    def __ejecutar_bear_off(self, punto_origen, dado_usado):
        """Ejecuta el bear off usando métodos del CORE."""
        try:
            # CORE: Quitar ficha
            ficha = self.__game.board.quitar_ficha(punto_origen)
            if ficha is None:
                return "Error: No hay fichas en ese punto"
            
            # CORE: Usar dado
            self.__game.dice.use_move(dado_usado)
            # CORE: Registrar bear off (puede causar victoria)
            victoria = self.__game.bear_off_ficha(ficha.color)
            
            # Obtener contador del CORE
            fichas_fuera = (self.__game.fichas_fuera_blancas 
                          if ficha.color == ColorFicha.BLANCA 
                          else self.__game.fichas_fuera_negras)
            
            if victoria:
                return f"¡Ficha sacada! ({fichas_fuera}/15) - ¡VICTORIA!"
            
            return f"¡Ficha sacada! ({fichas_fuera}/15)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def __intentar_movimiento(self, origen, destino):
        """Intenta realizar un movimiento normal."""
        color = self.__game.current_player.color
        
        # Calcular distancia
        if color == ColorFicha.BLANCA:
            if destino >= origen:
                return "Las blancas se mueven hacia números menores"
            distancia = origen - destino
        else:
            if destino <= origen:
                return "Las negras se mueven hacia números mayores"
            distancia = destino - origen
        
        # Verificar dado
        movimientos = list(self.__game.dice.last_roll)
        if distancia not in movimientos:
            return f"Movimiento inválido. Dados disponibles: {movimientos}"
        
        # Verificar fichas
        fichas_origen = self.__game.board.obtener_fichas(origen)
        if not fichas_origen:
            return "No hay fichas en el origen"
        
        fichas_destino = self.__game.board.obtener_fichas(destino)
        
        if fichas_destino:
            if fichas_destino[0].color != color:
                if len(fichas_destino) == 1:
                    return self.__ejecutar_movimiento_con_captura(origen, destino, distancia)
                else:
                    return "El punto destino está bloqueado por el oponente"
        
        return self.__ejecutar_movimiento_normal(origen, destino, distancia)
    
    def __ejecutar_movimiento_normal(self, origen, destino, distancia):
        """Ejecuta un movimiento normal usando métodos del CORE."""
        try:
            # CORE: Mover ficha
            ficha = self.__game.board.quitar_ficha(origen)
            if ficha is None:
                return "Error: No se pudo quitar la ficha"
            
            self.__game.board.agregar_ficha(destino, ficha)
            # CORE: Usar dado
            self.__game.dice.use_move(distancia)
            
            return f"Ficha movida de {origen + 1} a {destino + 1}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def __ejecutar_movimiento_con_captura(self, origen, destino, distancia):
        """Ejecuta un movimiento con captura usando métodos del CORE."""
        try:
            # CORE: Mover ficha propia
            ficha_propia = self.__game.board.quitar_ficha(origen)
            if ficha_propia is None:
                return "Error: No se pudo quitar la ficha"
            
            # CORE: Capturar ficha enemiga
            ficha_enemiga = self.__game.board.quitar_ficha(destino)
            if ficha_enemiga is None:
                self.__game.board.agregar_ficha(origen, ficha_propia)
                return "Error: No se pudo capturar la ficha enemiga"
            
            # CORE: Mover fichas
            self.__game.board.agregar_ficha_contenedor(ficha_enemiga)
            self.__game.board.agregar_ficha(destino, ficha_propia)
            # CORE: Usar dado
            self.__game.dice.use_move(distancia)
            
            return f"¡Captura! Ficha movida de {origen + 1} a {destino + 1}"
        except Exception as e:
            return f"Error en captura: {str(e)}"
    
    def verificar_fin_turno(self):
        """Verifica si el turno debe terminar (llama al CORE).
        
        También verifica si no hay movimientos posibles desde la barra.
        """
        # CORE: Verificar si hay fichas en barra sin movimientos posibles
        if self.__game.tiene_fichas_en_barra(self.__game.current_player.color):
            if self.__game.dice.last_raw_roll:
                # CORE: Verificar si hay entrada posible
                if not self.__game.hay_reentry_posible(self.__game.current_player.color):
                    jugador_anterior = self.__game.current_player.nombre
                    # CORE: Terminar turno
                    self.__game.end_turn()
                    return f"❌ No hay entrada posible desde la barra. Turno perdido. Turno de {self.__game.current_player.nombre}"
        
        # Verificar fin normal de turno
        if self.__game.dice.last_raw_roll and self.__game.dice.get_moves_remaining() == 0:
            jugador_anterior = self.__game.current_player.nombre
            # CORE: Terminar turno
            self.__game.end_turn()
            return f"Fin del turno de {jugador_anterior}. Turno de {self.__game.current_player.nombre}"
        return None
    
    def cancelar_seleccion(self):
        """Cancela la selección actual."""
        self.__punto_origen = None
        self.__origen_es_barra = False
    
    def lanzar_dados(self):
        """Lanza los dados (llama al CORE)."""
        if self.__game.dice.last_raw_roll:
            return "Ya hay dados lanzados"
        
        # CORE: Lanzar dados
        self.__game.roll_dice()
        return f"Dados: {self.__game.dice.last_raw_roll}"