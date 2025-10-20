"""Tests para la clase MoveExecutor."""
import unittest
from core.MoveExecutor import MoveExecutor
from core.Board import Board
from core.BoardInitializer import BoardInitializer
from core.Dice import Dice
from core.Player import Player
from core.ColorFicha import ColorFicha
from core.Checker import Checker


class TestMoveExecutor(unittest.TestCase):

    def setUp(self):
        """Configurar objetos antes de cada prueba."""
        self.board = Board()
        self.dice = Dice()
        self.player_white = Player("Juan", ColorFicha.BLANCA)
        self.player_black = Player("Maria", ColorFicha.NEGRA)

    def test_calculate_destination_jugador_blanco(self):
        """Test calcular destino para jugador blanco (resta)."""
        result = MoveExecutor.calculate_destination(10, 3, ColorFicha.BLANCA)
        self.assertEqual(result, 7)

    def test_calculate_destination_jugador_negro(self):
        """Test calcular destino para jugador negro (suma)."""
        result = MoveExecutor.calculate_destination(5, 4, ColorFicha.NEGRA)
        self.assertEqual(result, 9)

    def test_calculate_destination_blanco_desde_inicio(self):
        """Test cálculo desde posición inicial blancas."""
        result = MoveExecutor.calculate_destination(23, 5, ColorFicha.BLANCA)
        self.assertEqual(result, 18)

    def test_calculate_destination_negro_desde_inicio(self):
        """Test cálculo desde posición inicial negras."""
        result = MoveExecutor.calculate_destination(0, 6, ColorFicha.NEGRA)
        self.assertEqual(result, 6)

    def test_execute_move_exitoso_blanco(self):
        """Test ejecutar movimiento exitoso con jugador blanco."""
        # Preparar tablero
        self.board.agregar_ficha(10, Checker(ColorFicha.BLANCA))
        self.dice._Dice__available_moves = [3]
        # Ejecutar movimiento
        MoveExecutor.execute_move(self.board, self.dice, self.player_white, 10, 3)
        # Verificar
        self.assertTrue(self.board.punto_esta_vacio(10))
        self.assertEqual(self.board.contar_fichas(7), 1)
        self.assertEqual(self.board.obtener_color_punto(7), ColorFicha.BLANCA)

    def test_execute_move_exitoso_negro(self):
        """Test ejecutar movimiento exitoso con jugador negro."""
        # Preparar tablero
        self.board.agregar_ficha(5, Checker(ColorFicha.NEGRA))
        self.dice._Dice__available_moves = [4]
        # Ejecutar movimiento
        MoveExecutor.execute_move(self.board, self.dice, self.player_black, 5, 4)
        # Verificar
        self.assertTrue(self.board.punto_esta_vacio(5))
        self.assertEqual(self.board.contar_fichas(9), 1)
        self.assertEqual(self.board.obtener_color_punto(9), ColorFicha.NEGRA)

    def test_execute_move_dado_no_disponible(self):
        """Test error cuando el valor del dado no está disponible."""
        self.board.agregar_ficha(10, Checker(ColorFicha.BLANCA))
        self.dice._Dice__available_moves = [2, 5]  # Solo 2 y 5 disponibles
        with self.assertRaises(ValueError) as context:
            MoveExecutor.execute_move(self.board, self.dice, self.player_white, 10, 3)
        self.assertEqual(str(context.exception), "El valor del dado no está disponible")

    def test_execute_move_punto_vacio(self):
        """Test error cuando no hay fichas en el punto de origen."""
        self.dice._Dice__available_moves = [3]
        with self.assertRaises(ValueError) as context:
            MoveExecutor.execute_move(self.board, self.dice, self.player_white, 10, 3)
        self.assertEqual(str(context.exception), "No hay fichas en el punto de origen")

    def test_execute_move_ficha_color_incorrecto(self):
        """Test error cuando la ficha no pertenece al jugador."""
        # Ficha negra en el tablero, intenta mover jugador blanco
        self.board.agregar_ficha(10, Checker(ColorFicha.NEGRA))
        self.dice._Dice__available_moves = [3]
        with self.assertRaises(ValueError) as context:
            MoveExecutor.execute_move(self.board, self.dice, self.player_white, 10, 3)
        self.assertEqual(str(context.exception), "La ficha no pertenece al jugador actual")

    def test_execute_move_destino_fuera_tablero_negativo(self):
        """Test error cuando el destino es negativo (jugador blanco)."""
        self.board.agregar_ficha(2, Checker(ColorFicha.BLANCA))
        self.dice._Dice__available_moves = [5]
        with self.assertRaises(ValueError) as context:
            MoveExecutor.execute_move(self.board, self.dice, self.player_white, 2, 5)
        self.assertEqual(str(context.exception), "El movimiento sale del tablero")

    def test_execute_move_destino_fuera_tablero_mayor_23(self):
        """Test error cuando el destino es mayor a 23 (jugador negro)."""
        self.board.agregar_ficha(20, Checker(ColorFicha.NEGRA))
        self.dice._Dice__available_moves = [6]
        with self.assertRaises(ValueError) as context:
            MoveExecutor.execute_move(self.board, self.dice, self.player_black, 20, 6)
        self.assertEqual(str(context.exception), "El movimiento sale del tablero")

    def test_execute_move_usa_dado_correctamente(self):
        """Test que el dado se consume después del movimiento."""
        self.board.agregar_ficha(10, Checker(ColorFicha.BLANCA))
        self.dice._Dice__available_moves = [3, 5]
        self.assertEqual(self.dice.get_moves_remaining(), 2)
        MoveExecutor.execute_move(self.board, self.dice, self.player_white, 10, 3)
        self.assertEqual(self.dice.get_moves_remaining(), 1)
        self.assertEqual(self.dice.last_roll, (5,))

    def test_execute_move_multiples_movimientos(self):
        """Test ejecutar múltiples movimientos secuenciales."""
        # Preparar tablero con 2 fichas blancas
        self.board.agregar_ficha(10, Checker(ColorFicha.BLANCA))
        self.board.agregar_ficha(8, Checker(ColorFicha.BLANCA))
        self.dice._Dice__available_moves = [3, 2]
        # Primer movimiento
        MoveExecutor.execute_move(self.board, self.dice, self.player_white, 10, 3)
        self.assertEqual(self.board.contar_fichas(7), 1)
        # Segundo movimiento
        MoveExecutor.execute_move(self.board, self.dice, self.player_white, 8, 2)
        self.assertEqual(self.board.contar_fichas(6), 1)
        # Dados agotados
        self.assertEqual(self.dice.get_moves_remaining(), 0)

    def test_execute_move_con_tablero_inicializado(self):
        """Test movimiento en tablero con configuración estándar."""
        BoardInitializer.inicializar_estandar(self.board)
        self.dice._Dice__available_moves = [3]
        # Mover ficha blanca desde punto 23
        MoveExecutor.execute_move(self.board, self.dice, self.player_white, 23, 3)
        # Verificar
        self.assertEqual(self.board.contar_fichas(23), 1)  # Quedó 1
        self.assertEqual(self.board.contar_fichas(20), 1)  # Se movió 1

    def test_calculate_destination_valores_extremos(self):
        """Test cálculo con valores extremos."""
        # Blanco desde 23 con 6
        self.assertEqual(
            MoveExecutor.calculate_destination(23, 6, ColorFicha.BLANCA), 
            17
        )
        # Negro desde 0 con 6
        self.assertEqual(
            MoveExecutor.calculate_destination(0, 6, ColorFicha.NEGRA), 
            6
        )

    def test_execute_move_mantiene_integridad_tablero(self):
        """Test que el movimiento mantiene la integridad del tablero."""
        self.board.agregar_ficha(15, Checker(ColorFicha.BLANCA))
        total_fichas_antes = sum(self.board.contar_fichas(i) for i in range(24))
        self.dice._Dice__available_moves = [4]
        MoveExecutor.execute_move(self.board, self.dice, self.player_white, 15, 4)
        total_fichas_despues = sum(self.board.contar_fichas(i) for i in range(24))
        # El total de fichas debe ser el mismo
        self.assertEqual(total_fichas_antes, total_fichas_despues)


if __name__ == '__main__':
    unittest.main()
