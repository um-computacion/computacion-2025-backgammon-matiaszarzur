"""Módulo del juego principal de Backgammon."""
from core.Board import Board
from core.BoardInitializer import BoardInitializer
from core.Dice import Dice
from core.Player import Player
from core.ColorFicha import ColorFicha


class BackgammonGame:
    """Coordina el flujo del juego de backgammon."""
    def __init__(self, player1_name: str, player2_name: str):
        """Inicializar juego con dos jugadores.
        
        Args:
            player1_name (str): Nombre del jugador 1 (fichas blancas)
            player2_name (str): Nombre del jugador 2 (fichas negras)
        """
        self.__board = Board()
        self.__dice = Dice()
        # Crear jugadores
        self.__players = [
            Player(player1_name, ColorFicha.BLANCA),
            Player(player2_name, ColorFicha.NEGRA)
        ]
        self.__current_player_index = 0
        self.__game_started = False
        self.__game_over = False
        self.__winner = None
        # Contadores de bear off
        self.__fichas_fuera_blancas = 0
        self.__fichas_fuera_negras = 0

    @property
    def board(self):
        """Obtener el tablero del juego."""
        return self.__board

    @property
    def dice(self):
        """Obtener los dados del juego."""
        return self.__dice

    @property
    def current_player(self):
        """Obtener el jugador actual."""
        return self.__players[self.__current_player_index]

    @property
    def other_player(self):
        """Obtener el otro jugador."""
        return self.__players[1 - self.__current_player_index]

    @property
    def is_game_over(self):
        """Verificar si el juego ha terminado."""
        return self.__game_over

    @property
    def winner(self):
        """Obtener el ganador del juego."""
        return self.__winner

    @property
    def fichas_fuera_blancas(self):
        """Obtener cantidad de fichas blancas sacadas del tablero."""
        return self.__fichas_fuera_blancas

    @property
    def fichas_fuera_negras(self):
        """Obtener cantidad de fichas negras sacadas del tablero."""
        return self.__fichas_fuera_negras

    def start_game(self):
        """Iniciar el juego configurando el tablero."""
        BoardInitializer.inicializar_estandar(self.__board)
        self.__game_started = True
        self.__game_over = False
        self.__winner = None
        self.__current_player_index = 0
        self.__fichas_fuera_blancas = 0
        self.__fichas_fuera_negras = 0

    def roll_dice(self):
        """Lanzar los dados para el turno actual.
        
        Returns:
            tuple: Valores de los dados lanzados
            
        Raises:
            RuntimeError: Si el juego no ha comenzado
        """
        if not self.__game_started:
            raise RuntimeError("El juego no ha comenzado")
        if self.__game_over:
            raise RuntimeError("El juego ya ha terminado")

        return self.__dice.roll()

    def end_turn(self):
        """Finalizar el turno del jugador actual y pasar al siguiente.
        
        Raises:
            RuntimeError: Si el juego no ha comenzado
        """
        if not self.__game_started:
            raise RuntimeError("El juego no ha comenzado")
        if self.__game_over:
            raise RuntimeError("El juego ya ha terminado")

        self.__dice.clear_roll()
        self.__current_player_index = 1 - self.__current_player_index
    def set_winner(self, player):
        """Establecer el ganador y finalizar el juego.
        
        Args:
            player (Player): El jugador ganador
        """
        if player not in self.__players:
            raise ValueError("El jugador no pertenece a esta partida")
        self.__winner = player
        self.__game_over = True
    def reset_game(self):
        """Reiniciar el juego a su estado inicial."""
        self.__board = Board()
        self.__dice = Dice()
        self.__current_player_index = 0
        self.__game_started = False
        self.__game_over = False
        self.__winner = None
        self.__fichas_fuera_blancas = 0
        self.__fichas_fuera_negras = 0
    def puede_hacer_bear_off(self, color):
        """Verificar si un jugador puede hacer bear off (sacar fichas).
        
        Solo se puede hacer bear off cuando TODAS las fichas están en el home.
        - Blancas: home = puntos 0-5
        - Negras: home = puntos 18-23
        
        Args:
            color (ColorFicha): Color del jugador
            
        Returns:
            bool: True si puede hacer bear off
        """
        # No puede hacer bear off si tiene fichas en la barra
        if self.__board.contar_fichas_contenedor(color) > 0:
            return False
        if color == ColorFicha.BLANCA:
            home_range = range(0, 6)
            outside_home_range = range(6, 24)
        else:
            home_range = range(18, 24)
            outside_home_range = range(0, 18)
        # Verificar que NO hay fichas fuera del home
        for punto in outside_home_range:
            fichas = self.__board.obtener_fichas(punto)
            if fichas and fichas[0].color == color:
                return False
        return True

    def bear_off_ficha(self, color):
        """Sacar una ficha del tablero (bear off).
        
        Args:
            color (ColorFicha): Color de la ficha a sacar
            
        Returns:
            bool: True si esta acción causó una victoria
        """
        if color == ColorFicha.BLANCA:
            self.__fichas_fuera_blancas += 1
            if self.__fichas_fuera_blancas == 15:
                self.set_winner(self.current_player)
                return True
        else:
            self.__fichas_fuera_negras += 1
            if self.__fichas_fuera_negras == 15:
                self.set_winner(self.current_player)
                return True

        return False

    def tiene_fichas_en_barra(self, color):
        """Verificar si un jugador tiene fichas en la barra.
        
        Args:
            color (ColorFicha): Color del jugador
            
        Returns:
            bool: True si tiene fichas en la barra
        """
        return self.__board.contar_fichas_contenedor(color) > 0

    def hay_reentry_posible(self, color):
        """Verificar si hay al menos un punto de entrada posible desde la barra."""
        if not self.tiene_fichas_en_barra(color):
            return True  # No hay fichas en barra, no aplica
        dados = list(self.__dice.last_roll)
        if color == ColorFicha.BLANCA:
            # Blancas entran por 18-23
            for dado in dados:
                punto_entrada = 24 - dado
                if 18 <= punto_entrada <= 23:
                    fichas = self.__board.obtener_fichas(punto_entrada)
                    # Puede entrar si: vacío, propias, o 1 enemiga
                    if not fichas:
                        return True
                    if fichas[0].color == color:
                        return True
                    if len(fichas) == 1:
                        return True
        else:
            # Negras entran por 0-5
            for dado in dados:
                punto_entrada = dado - 1
                if 0 <= punto_entrada <= 5:
                    fichas = self.__board.obtener_fichas(punto_entrada)
                    # Puede entrar si: vacío, propias, o 1 enemiga
                    if not fichas:
                        return True
                    if fichas[0].color == color:
                        return True
                    if len(fichas) == 1:
                        return True
        return False
