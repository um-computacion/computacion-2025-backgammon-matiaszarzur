"""Módulo para inicializar el tablero de backgammon.

Este módulo contiene la clase BoardInitializer que se encarga de
configurar diferentes disposiciones iniciales del tablero.
"""
from core.Checker import Checker
from core.ColorFicha import ColorFicha


class BoardInitializer:
    """Clase responsable de inicializar el tablero con diferentes configuraciones."""
    @staticmethod
    def inicializar_estandar(board):
        """Configurar el tablero con la disposición estándar de backgammon.
        
        Args:
            board (Board): El tablero a configurar
        """
        board.resetear_tablero()
        board.limpiar_contenedores()
        # Fichas negras
        for _ in range(2):
            board.agregar_ficha(0, Checker(ColorFicha.NEGRA))
        for _ in range(5):
            board.agregar_ficha(11, Checker(ColorFicha.NEGRA))
        for _ in range(3):
            board.agregar_ficha(16, Checker(ColorFicha.NEGRA))
        for _ in range(5):
            board.agregar_ficha(18, Checker(ColorFicha.NEGRA))
        # Fichas blancas
        for _ in range(2):
            board.agregar_ficha(23, Checker(ColorFicha.BLANCA))
        for _ in range(5):
            board.agregar_ficha(12, Checker(ColorFicha.BLANCA))
        for _ in range(3):
            board.agregar_ficha(7, Checker(ColorFicha.BLANCA))
        for _ in range(5):
            board.agregar_ficha(5, Checker(ColorFicha.BLANCA))
