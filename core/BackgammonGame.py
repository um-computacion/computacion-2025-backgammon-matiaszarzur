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
    def start_game(self):
        """Iniciar el juego configurando el tablero."""
        BoardInitializer.inicializar_estandar(self.__board)
        self.__game_started = True
        self.__game_over = False
        self.__winner = None
        self.__current_player_index = 0
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
