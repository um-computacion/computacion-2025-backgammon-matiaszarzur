"""Tests para la clase BackgammonGame."""
import unittest
from unittest.mock import patch
from core.BackgammonGame import BackgammonGame
from core.Player import Player
from core.ColorFicha import ColorFicha
from core.Board import Board
from core.Dice import Dice
from core.Checker import Checker


class TestBackgammonGame(unittest.TestCase):

    def setUp(self):
        """Configurar objetos antes de cada prueba."""
        self.game = BackgammonGame("Juan", "Maria")

    def test_inicializar_juego(self):
        """Test que el juego se inicializa correctamente."""
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.dice)
        self.assertIsInstance(self.game.board, Board)
        self.assertIsInstance(self.game.dice, Dice)

    def test_jugadores_creados_correctamente(self):
        """Test que los jugadores se crean con nombres y colores correctos."""
        self.assertEqual(self.game.current_player.nombre, "Juan")
        self.assertEqual(self.game.current_player.color, ColorFicha.BLANCA)
        self.assertEqual(self.game.other_player.nombre, "Maria")
        self.assertEqual(self.game.other_player.color, ColorFicha.NEGRA)

    def test_estado_inicial_juego(self):
        """Test que el estado inicial del juego es correcto."""
        self.assertFalse(self.game.is_game_over)
        self.assertIsNone(self.game.winner)

    def test_start_game_inicializa_tablero(self):
        """Test que start_game inicializa el tablero correctamente."""
        self.game.start_game()
        # Verificar que hay fichas en el tablero
        self.assertFalse(self.game.board.tablero_esta_vacio())
        # Verificar algunas posiciones específicas del setup estándar
        self.assertEqual(self.game.board.contar_fichas(0), 2)
        self.assertEqual(self.game.board.contar_fichas(23), 2)

    def test_start_game_resetea_estado(self):
        """Test que start_game resetea el estado del juego."""
        self.game.start_game()
        self.assertFalse(self.game.is_game_over)
        self.assertIsNone(self.game.winner)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_roll_dice_success(self, mock_roll):
        """Test lanzar dados exitosamente."""
        self.game.start_game()
        result = self.game.roll_dice()
        self.assertEqual(result, (3, 5))
        self.assertEqual(self.game.dice.last_raw_roll, (3, 5))

    def test_roll_dice_sin_iniciar_juego(self):
        """Test que lanzar dados sin iniciar el juego lanza error."""
        with self.assertRaises(RuntimeError) as context:
            self.game.roll_dice()
        self.assertEqual(str(context.exception), "El juego no ha comenzado")

    def test_roll_dice_juego_terminado(self):
        """Test que lanzar dados en juego terminado lanza error."""
        self.game.start_game()
        self.game.set_winner(self.game.current_player)

        with self.assertRaises(RuntimeError) as context:
            self.game.roll_dice()

        self.assertEqual(str(context.exception), "El juego ya ha terminado")

    def test_end_turn_cambia_jugador(self):
        """Test que end_turn cambia al jugador actual."""
        self.game.start_game()

        jugador_inicial = self.game.current_player
        self.game.end_turn()
        jugador_despues = self.game.current_player

        self.assertNotEqual(jugador_inicial, jugador_despues)
        self.assertEqual(self.game.current_player.nombre, "Maria")

    def test_end_turn_limpia_dados(self):
        """Test que end_turn limpia el lanzamiento de dados."""
        self.game.start_game()
        
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 4)):
            self.game.roll_dice()
            self.assertIsNotNone(self.game.dice.last_raw_roll)

            self.game.end_turn()
            self.assertIsNone(self.game.dice.last_raw_roll)

    def test_end_turn_sin_iniciar_juego(self):
        """Test que end_turn sin iniciar el juego lanza error."""
        with self.assertRaises(RuntimeError) as context:
            self.game.end_turn()

        self.assertEqual(str(context.exception), "El juego no ha comenzado")

    def test_end_turn_juego_terminado(self):
        """Test que end_turn en juego terminado lanza error."""
        self.game.start_game()
        self.game.set_winner(self.game.current_player)

        with self.assertRaises(RuntimeError) as context:
            self.game.end_turn()

        self.assertEqual(str(context.exception), "El juego ya ha terminado")

    def test_set_winner_jugador_valido(self):
        """Test establecer ganador con jugador válido."""
        self.game.start_game()
        jugador = self.game.current_player

        self.game.set_winner(jugador)

        self.assertTrue(self.game.is_game_over)
        self.assertEqual(self.game.winner, jugador)

    def test_set_winner_jugador_invalido(self):
        """Test establecer ganador con jugador que no pertenece al juego."""
        jugador_externo = Player("Pedro", ColorFicha.BLANCA)

        with self.assertRaises(ValueError) as context:
            self.game.set_winner(jugador_externo)

        self.assertEqual(str(context.exception), "El jugador no pertenece a esta partida")

    def test_reset_game_reinicia_estado(self):
        """Test que reset_game reinicia el juego correctamente."""
        self.game.start_game()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(1, 1)):
            self.game.roll_dice()
        self.game.set_winner(self.game.current_player)
        # Resetear
        self.game.reset_game()
        # Verificar estado inicial
        self.assertFalse(self.game.is_game_over)
        self.assertIsNone(self.game.winner)
        self.assertIsNone(self.game.dice.last_raw_roll)

    def test_reset_game_limpia_tablero(self):
        """Test que reset_game crea nuevas instancias de Board y Dice."""
        self.game.start_game()
        board_original = self.game.board
        dice_original = self.game.dice
        self.game.reset_game()
        # Verificar que son nuevas instancias
        self.assertIsNot(self.game.board, board_original)
        self.assertIsNot(self.game.dice, dice_original)

    def test_current_player_alterna_correctamente(self):
        """Test que current_player alterna entre jugadores."""
        self.game.start_game()
        
        player1 = self.game.current_player
        self.game.end_turn()
        player2 = self.game.current_player
        self.game.end_turn()
        player3 = self.game.current_player
        
        self.assertEqual(player1, player3)
        self.assertNotEqual(player1, player2)

    def test_other_player_retorna_jugador_opuesto(self):
        """Test que other_player siempre retorna el jugador contrario."""
        self.game.start_game()
        current = self.game.current_player
        other = self.game.other_player
        self.assertNotEqual(current, other)
        self.game.end_turn()
        # Ahora el "other" debería ser el "current" anterior
        self.assertEqual(self.game.current_player, other)

    def test_multiple_end_turns(self):
        """Test múltiples cambios de turno."""
        self.game.start_game()
        jugadores = []
        for _ in range(6):
            jugadores.append(self.game.current_player.nombre)
            self.game.end_turn()
        # Debe alternar: Juan, Maria, Juan, Maria, Juan, Maria
        self.assertEqual(jugadores, ["Juan", "Maria", "Juan", "Maria", "Juan", "Maria"])

    # ==================== NUEVOS TESTS PARA MEJORAR COVERAGE ====================

    def test_fichas_fuera_blancas_inicial(self):
        """Test que fichas_fuera_blancas se inicializa en 0."""
        self.game.start_game()
        self.assertEqual(self.game.fichas_fuera_blancas, 0)

    def test_fichas_fuera_negras_inicial(self):
        """Test que fichas_fuera_negras se inicializa en 0."""
        self.game.start_game()
        self.assertEqual(self.game.fichas_fuera_negras, 0)

    def test_puede_hacer_bear_off_sin_fichas_en_home_blancas(self):
        """Test que blancas no pueden hacer bear off si tienen fichas fuera del home."""
        self.game.start_game()
        # En el tablero estándar, las blancas tienen fichas en varios puntos (no todas en 0-5)
        resultado = self.game.puede_hacer_bear_off(ColorFicha.BLANCA)
        self.assertFalse(resultado)

    def test_puede_hacer_bear_off_sin_fichas_en_home_negras(self):
        """Test que negras no pueden hacer bear off si tienen fichas fuera del home."""
        self.game.start_game()
        # En el tablero estándar, las negras tienen fichas en varios puntos (no todas en 18-23)
        resultado = self.game.puede_hacer_bear_off(ColorFicha.NEGRA)
        self.assertFalse(resultado)

    def test_puede_hacer_bear_off_con_fichas_en_barra_blancas(self):
        """Test que blancas no pueden hacer bear off si tienen fichas en la barra."""
        self.game.start_game()
        # Limpiar el tablero manualmente removiendo todas las fichas
        for punto in range(24):
            while self.game.board.contar_fichas(punto) > 0:
                self.game.board.quitar_ficha(punto)
        
        # Poner fichas blancas solo en home
        for i in range(5):
            self.game.board.agregar_ficha(i, Checker(ColorFicha.BLANCA))
        
        # Agregar una ficha blanca a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.BLANCA))
        
        resultado = self.game.puede_hacer_bear_off(ColorFicha.BLANCA)
        self.assertFalse(resultado)

    def test_puede_hacer_bear_off_con_fichas_en_barra_negras(self):
        """Test que negras no pueden hacer bear off si tienen fichas en la barra."""
        self.game.start_game()
        # Limpiar el tablero manualmente
        for punto in range(24):
            while self.game.board.contar_fichas(punto) > 0:
                self.game.board.quitar_ficha(punto)
        
        # Poner fichas negras solo en home
        for i in range(18, 23):
            self.game.board.agregar_ficha(i, Checker(ColorFicha.NEGRA))
        
        # Agregar una ficha negra a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.NEGRA))
        
        resultado = self.game.puede_hacer_bear_off(ColorFicha.NEGRA)
        self.assertFalse(resultado)

    def test_puede_hacer_bear_off_todas_fichas_en_home_blancas(self):
        """Test que blancas pueden hacer bear off cuando todas las fichas están en home."""
        self.game.start_game()
        # Limpiar el tablero manualmente
        for punto in range(24):
            while self.game.board.contar_fichas(punto) > 0:
                self.game.board.quitar_ficha(punto)
        
        # Poner fichas blancas solo en home (0-5)
        for i in range(6):
            self.game.board.agregar_ficha(i, Checker(ColorFicha.BLANCA))
        
        resultado = self.game.puede_hacer_bear_off(ColorFicha.BLANCA)
        self.assertTrue(resultado)

    def test_puede_hacer_bear_off_todas_fichas_en_home_negras(self):
        """Test que negras pueden hacer bear off cuando todas las fichas están en home."""
        self.game.start_game()
        # Limpiar el tablero manualmente
        for punto in range(24):
            while self.game.board.contar_fichas(punto) > 0:
                self.game.board.quitar_ficha(punto)
        
        # Poner fichas negras solo en home (18-23)
        for i in range(18, 24):
            self.game.board.agregar_ficha(i, Checker(ColorFicha.NEGRA))
        
        resultado = self.game.puede_hacer_bear_off(ColorFicha.NEGRA)
        self.assertTrue(resultado)

    def test_bear_off_ficha_blanca_incrementa_contador(self):
        """Test que bear_off_ficha incrementa el contador de fichas blancas fuera."""
        self.game.start_game()
        self.assertEqual(self.game.fichas_fuera_blancas, 0)
        
        victoria = self.game.bear_off_ficha(ColorFicha.BLANCA)
        
        self.assertEqual(self.game.fichas_fuera_blancas, 1)
        self.assertFalse(victoria)

    def test_bear_off_ficha_negra_incrementa_contador(self):
        """Test que bear_off_ficha incrementa el contador de fichas negras fuera."""
        self.game.start_game()
        self.assertEqual(self.game.fichas_fuera_negras, 0)
        
        victoria = self.game.bear_off_ficha(ColorFicha.NEGRA)
        
        self.assertEqual(self.game.fichas_fuera_negras, 1)
        self.assertFalse(victoria)

    def test_bear_off_ficha_blanca_victoria_al_sacar_15(self):
        """Test que blancas ganan al sacar la ficha número 15."""
        self.game.start_game()
        # Sacar 14 fichas blancas
        for _ in range(14):
            victoria = self.game.bear_off_ficha(ColorFicha.BLANCA)
            self.assertFalse(victoria)
        
        # Sacar la ficha 15
        victoria = self.game.bear_off_ficha(ColorFicha.BLANCA)
        
        self.assertTrue(victoria)
        self.assertEqual(self.game.fichas_fuera_blancas, 15)
        self.assertTrue(self.game.is_game_over)
        self.assertEqual(self.game.winner, self.game.current_player)

    def test_bear_off_ficha_negra_victoria_al_sacar_15(self):
        """Test que negras ganan al sacar la ficha número 15."""
        self.game.start_game()
        # Cambiar al jugador negro
        self.game.end_turn()
        
        # Sacar 14 fichas negras
        for _ in range(14):
            victoria = self.game.bear_off_ficha(ColorFicha.NEGRA)
            self.assertFalse(victoria)
        
        # Sacar la ficha 15
        victoria = self.game.bear_off_ficha(ColorFicha.NEGRA)
        
        self.assertTrue(victoria)
        self.assertEqual(self.game.fichas_fuera_negras, 15)
        self.assertTrue(self.game.is_game_over)
        self.assertEqual(self.game.winner, self.game.current_player)

    def test_tiene_fichas_en_barra_blancas_false(self):
        """Test que tiene_fichas_en_barra devuelve False cuando no hay fichas blancas en barra."""
        self.game.start_game()
        resultado = self.game.tiene_fichas_en_barra(ColorFicha.BLANCA)
        self.assertFalse(resultado)

    def test_tiene_fichas_en_barra_blancas_true(self):
        """Test que tiene_fichas_en_barra devuelve True cuando hay fichas blancas en barra."""
        self.game.start_game()
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.BLANCA))
        
        resultado = self.game.tiene_fichas_en_barra(ColorFicha.BLANCA)
        self.assertTrue(resultado)

    def test_tiene_fichas_en_barra_negras_false(self):
        """Test que tiene_fichas_en_barra devuelve False cuando no hay fichas negras en barra."""
        self.game.start_game()
        resultado = self.game.tiene_fichas_en_barra(ColorFicha.NEGRA)
        self.assertFalse(resultado)

    def test_tiene_fichas_en_barra_negras_true(self):
        """Test que tiene_fichas_en_barra devuelve True cuando hay fichas negras en barra."""
        self.game.start_game()
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.NEGRA))
        
        resultado = self.game.tiene_fichas_en_barra(ColorFicha.NEGRA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_hay_reentry_posible_sin_fichas_en_barra(self, mock_roll):
        """Test que hay_reentry_posible devuelve True si no hay fichas en barra."""
        self.game.start_game()
        self.game.roll_dice()
        
        resultado = self.game.hay_reentry_posible(ColorFicha.BLANCA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_hay_reentry_posible_blancas_punto_vacio(self, mock_roll):
        """Test que blancas pueden hacer reentry cuando el punto está vacío."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha blanca a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.BLANCA))
        # Limpiar puntos de entrada para blancas (24-3=21, 24-5=19)
        self.game.board.limpiar_punto(21)
        self.game.board.limpiar_punto(19)
        
        resultado = self.game.hay_reentry_posible(ColorFicha.BLANCA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_hay_reentry_posible_blancas_punto_propio(self, mock_roll):
        """Test que blancas pueden hacer reentry cuando el punto tiene fichas propias."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha blanca a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.BLANCA))
        # Limpiar y poner fichas blancas en punto de entrada (24-3=21)
        self.game.board.limpiar_punto(21)
        self.game.board.agregar_ficha(21, Checker(ColorFicha.BLANCA))
        
        resultado = self.game.hay_reentry_posible(ColorFicha.BLANCA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_hay_reentry_posible_blancas_una_ficha_enemiga(self, mock_roll):
        """Test que blancas pueden hacer reentry cuando hay una sola ficha enemiga."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha blanca a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.BLANCA))
        # Limpiar y poner una ficha negra en punto de entrada (24-3=21)
        self.game.board.limpiar_punto(21)
        self.game.board.agregar_ficha(21, Checker(ColorFicha.NEGRA))
        
        resultado = self.game.hay_reentry_posible(ColorFicha.BLANCA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_hay_reentry_posible_blancas_bloqueado(self, mock_roll):
        """Test que blancas no pueden hacer reentry cuando todos los puntos están bloqueados."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha blanca a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.BLANCA))
        # Bloquear puntos de entrada (24-3=21, 24-5=19) con 2+ fichas negras
        self.game.board.limpiar_punto(21)
        self.game.board.limpiar_punto(19)
        self.game.board.agregar_ficha(21, Checker(ColorFicha.NEGRA))
        self.game.board.agregar_ficha(21, Checker(ColorFicha.NEGRA))
        self.game.board.agregar_ficha(19, Checker(ColorFicha.NEGRA))
        self.game.board.agregar_ficha(19, Checker(ColorFicha.NEGRA))
        
        resultado = self.game.hay_reentry_posible(ColorFicha.BLANCA)
        self.assertFalse(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 4))
    def test_hay_reentry_posible_negras_punto_vacio(self, mock_roll):
        """Test que negras pueden hacer reentry cuando el punto está vacío."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha negra a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.NEGRA))
        # Limpiar puntos de entrada para negras (2-1=1, 4-1=3)
        self.game.board.limpiar_punto(1)
        self.game.board.limpiar_punto(3)
        
        resultado = self.game.hay_reentry_posible(ColorFicha.NEGRA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 4))
    def test_hay_reentry_posible_negras_punto_propio(self, mock_roll):
        """Test que negras pueden hacer reentry cuando el punto tiene fichas propias."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha negra a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.NEGRA))
        # Limpiar y poner fichas negras en punto de entrada (2-1=1)
        self.game.board.limpiar_punto(1)
        self.game.board.agregar_ficha(1, Checker(ColorFicha.NEGRA))
        
        resultado = self.game.hay_reentry_posible(ColorFicha.NEGRA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 4))
    def test_hay_reentry_posible_negras_una_ficha_enemiga(self, mock_roll):
        """Test que negras pueden hacer reentry cuando hay una sola ficha enemiga."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha negra a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.NEGRA))
        # Limpiar y poner una ficha blanca en punto de entrada (2-1=1)
        self.game.board.limpiar_punto(1)
        self.game.board.agregar_ficha(1, Checker(ColorFicha.BLANCA))
        
        resultado = self.game.hay_reentry_posible(ColorFicha.NEGRA)
        self.assertTrue(resultado)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 4))
    def test_hay_reentry_posible_negras_bloqueado(self, mock_roll):
        """Test que negras no pueden hacer reentry cuando todos los puntos están bloqueados."""
        self.game.start_game()
        self.game.roll_dice()
        
        # Agregar ficha negra a la barra
        self.game.board.agregar_ficha_contenedor(Checker(ColorFicha.NEGRA))
        # Bloquear puntos de entrada (2-1=1, 4-1=3) con 2+ fichas blancas
        self.game.board.limpiar_punto(1)
        self.game.board.limpiar_punto(3)
        self.game.board.agregar_ficha(1, Checker(ColorFicha.BLANCA))
        self.game.board.agregar_ficha(1, Checker(ColorFicha.BLANCA))
        self.game.board.agregar_ficha(3, Checker(ColorFicha.BLANCA))
        self.game.board.agregar_ficha(3, Checker(ColorFicha.BLANCA))
        
        resultado = self.game.hay_reentry_posible(ColorFicha.NEGRA)
        self.assertFalse(resultado)


if __name__ == '__main__':
    unittest.main()
