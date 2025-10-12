"""Módulo para ejecutar movimientos de fichas en el tablero."""
from core.Board import Board
from core.Dice import Dice
from core.Player import Player
from core.ColorFicha import ColorFicha


class MoveExecutor:
    """Responsable de ejecutar movimientos de fichas en el tablero."""
    
    @staticmethod
    def calculate_destination(from_point: int, dice_value: int, player_color: ColorFicha) -> int:
        """Calcular el punto de destino según el color del jugador."""
        if player_color == ColorFicha.BLANCA:
            return from_point - dice_value
        else:  # ColorFicha.NEGRA
            return from_point + dice_value
    
    @staticmethod
    def execute_move(board: Board, dice: Dice, player: Player, from_point: int, dice_value: int):
        """Ejecutar un movimiento de ficha."""
        # Validar que el dado esté disponible
        if not dice.use_move(dice_value):
            raise ValueError("El valor del dado no está disponible")
        
        # Validar que hay ficha en el punto de origen
        if board.punto_esta_vacio(from_point):
            raise ValueError("No hay fichas en el punto de origen")
        
        # Validar que la ficha es del color del jugador
        ficha_color = board.obtener_color_punto(from_point)
        if ficha_color != player.color:
            raise ValueError("La ficha no pertenece al jugador actual")
        
        # Calcular destino
        to_point = MoveExecutor.calculate_destination(from_point, dice_value, player.color)
        
        # Validar que el destino está dentro del tablero
        if to_point < 0 or to_point > 23:
            raise ValueError("El movimiento sale del tablero")
        
        # Ejecutar movimiento
        ficha = board.quitar_ficha(from_point)
        board.agregar_ficha(to_point, ficha)