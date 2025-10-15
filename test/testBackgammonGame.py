"""Tests para la clase BackgammonGame."""
import unittest
from unittest.mock import patch
from core.BackgammonGame import BackgammonGame
from core.Player import Player
from core.ColorFicha import ColorFicha
from core.Board import Board
from core.Dice import Dice


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


if __name__ == '__main__':
    unittest.main()
