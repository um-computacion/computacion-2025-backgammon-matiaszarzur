"""Tests para la clase CLI."""
import unittest
from unittest.mock import patch
from cli.Cli import CLI
from core.BackgammonGame import BackgammonGame


class TestCLI(unittest.TestCase):
    """Tests para la clase CLI del juego de Backgammon."""

    def setUp(self):
        """Configurar objetos antes de cada prueba."""
        self.cli = CLI()

    def test_inicializacion_cli(self):
        """Test que el CLI se inicializa correctamente."""
        # pylint: disable=protected-access
        self.assertIsNone(self.cli._CLI__game)
        self.assertIsNotNone(self.cli._CLI__move_executor)
        self.assertTrue(self.cli._CLI__running)

    def test_cli_tiene_metodo_limpiar_pantalla(self):
        """Test que CLI tiene método limpiar_pantalla."""
        self.assertTrue(hasattr(self.cli, 'limpiar_pantalla'))
        self.assertTrue(callable(self.cli.limpiar_pantalla))

    def test_cli_tiene_metodo_mostrar_menu_principal(self):
        """Test que CLI tiene método mostrar_menu_principal."""
        self.assertTrue(hasattr(self.cli, 'mostrar_menu_principal'))
        self.assertTrue(callable(self.cli.mostrar_menu_principal))

    def test_cli_tiene_metodo_ejecutar_menu_principal(self):
        """Test que CLI tiene método ejecutar_menu_principal."""
        self.assertTrue(hasattr(self.cli, 'ejecutar_menu_principal'))
        self.assertTrue(callable(self.cli.ejecutar_menu_principal))

    def test_cli_tiene_metodo_mostrar_reglas(self):
        """Test que CLI tiene método mostrar_reglas."""
        self.assertTrue(hasattr(self.cli, 'mostrar_reglas'))
        self.assertTrue(callable(self.cli.mostrar_reglas))

    def test_cli_tiene_metodo_mostrar_menu_partida(self):
        """Test que CLI tiene método mostrar_menu_partida."""
        self.assertTrue(hasattr(self.cli, 'mostrar_menu_partida'))
        self.assertTrue(callable(self.cli.mostrar_menu_partida))

    def test_cli_tiene_metodo_ejecutar_menu_partida(self):
        """Test que CLI tiene método ejecutar_menu_partida."""
        self.assertTrue(hasattr(self.cli, 'ejecutar_menu_partida'))
        self.assertTrue(callable(self.cli.ejecutar_menu_partida))

    def test_cli_tiene_metodo_nueva_partida(self):
        """Test que CLI tiene método nueva_partida."""
        self.assertTrue(hasattr(self.cli, 'nueva_partida'))
        self.assertTrue(callable(self.cli.nueva_partida))

    def test_cli_tiene_metodo_ver_tablero(self):
        """Test que CLI tiene método ver_tablero."""
        self.assertTrue(hasattr(self.cli, 'ver_tablero'))
        self.assertTrue(callable(self.cli.ver_tablero))

    def test_cli_tiene_metodo_lanzar_dados(self):
        """Test que CLI tiene método lanzar_dados."""
        self.assertTrue(hasattr(self.cli, 'lanzar_dados'))
        self.assertTrue(callable(self.cli.lanzar_dados))

    def test_cli_tiene_metodo_mover_ficha(self):
        """Test que CLI tiene método mover_ficha."""
        self.assertTrue(hasattr(self.cli, 'mover_ficha'))
        self.assertTrue(callable(self.cli.mover_ficha))

    def test_cli_tiene_metodo_finalizar_turno(self):
        """Test que CLI tiene método finalizar_turno."""
        self.assertTrue(hasattr(self.cli, 'finalizar_turno'))
        self.assertTrue(callable(self.cli.finalizar_turno))

    def test_cli_tiene_metodo_rendirse(self):
        """Test que CLI tiene método rendirse."""
        self.assertTrue(hasattr(self.cli, 'rendirse'))
        self.assertTrue(callable(self.cli.rendirse))

    def test_cli_tiene_metodo_volver_menu_principal(self):
        """Test que CLI tiene método volver_menu_principal."""
        self.assertTrue(hasattr(self.cli, 'volver_menu_principal'))
        self.assertTrue(callable(self.cli.volver_menu_principal))

    def test_cli_tiene_metodo_mostrar_ganador(self):
        """Test que CLI tiene método mostrar_ganador."""
        self.assertTrue(hasattr(self.cli, 'mostrar_ganador'))
        self.assertTrue(callable(self.cli.mostrar_ganador))

    def test_cli_tiene_metodo_ejecutar(self):
        """Test que CLI tiene método ejecutar."""
        self.assertTrue(hasattr(self.cli, 'ejecutar'))
        self.assertTrue(callable(self.cli.ejecutar))

    @patch('os.system')
    def test_limpiar_pantalla(self, mock_system):
        """Test limpiar pantalla."""
        self.cli.limpiar_pantalla()
        mock_system.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_mostrar_reglas(self, mock_limpiar, _mock_input, _mock_print):
        """Test mostrar reglas."""
        self.cli.mostrar_reglas()
        mock_limpiar.assert_called_once()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['Juan', 'Maria', ''])
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_nueva_partida(self, mock_limpiar, _mock_input, _mock_print):
        """Test crear nueva partida."""
        # pylint: disable=protected-access
        self.cli.nueva_partida()
        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.current_player.nombre, "Juan")
        mock_limpiar.assert_called()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['', 'Juan', 'Maria', ''])
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_nueva_partida_nombre_vacio(self, _mock_limpiar, _mock_input, _mock_print):
        """Test nueva partida con nombre vacío primero."""
        # pylint: disable=protected-access
        self.cli.nueva_partida()
        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.current_player.nombre, "Juan")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['Juan', '', 'Maria', ''])
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_nueva_partida_segundo_nombre_vacio(self, _mock_limpiar, _mock_input, _mock_print):
        """Test nueva partida con segundo nombre vacío."""
        # pylint: disable=protected-access
        self.cli.nueva_partida()
        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.other_player.nombre, "Maria")

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    def test_ver_tablero(self, _mock_input, _mock_print):
        """Test ver tablero con juego iniciado."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.ver_tablero()

    @patch('builtins.print')
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', return_value='')
    def test_lanzar_dados_exitoso(self, _mock_input, _mock_roll, _mock_print):
        """Test lanzar dados exitosamente."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.lanzar_dados()
        self.assertEqual(self.cli._CLI__game.dice.last_raw_roll, (3, 5))

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    def test_lanzar_dados_sin_juego(self, _mock_input, _mock_print):
        """Test lanzar dados sin juego iniciado."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli.lanzar_dados()

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    def test_mover_ficha_sin_dados(self, _mock_input, _mock_print):
        """Test mover ficha sin haber lanzado dados."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.mover_ficha()

    @patch('builtins.print')
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['23', '3', ''])
    def test_mover_ficha_exitoso(self, _mock_input, _mock_roll, _mock_print):
        """Test mover ficha exitosamente."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()
        self.cli.mover_ficha()

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    def test_mover_ficha_sin_movimientos_disponibles(self, _mock_input, _mock_print):
        """Test mover ficha cuando no quedan movimientos."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()
        while self.cli._CLI__game.dice.get_moves_remaining() > 0:
            self.cli._CLI__game.dice.use_move(self.cli._CLI__game.dice.last_roll[0])
        self.cli.mover_ficha()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['abc', '3', ''])
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_mover_ficha_input_invalido(self, _mock_roll, _mock_input, _mock_print):
        """Test mover ficha con input inválido."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()
        self.cli.mover_ficha()

    @patch('builtins.print')
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['10', '7', ''])
    def test_mover_ficha_error_valor(self, _mock_input, _mock_roll, _mock_print):
        """Test mover ficha con ValueError."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()
        self.cli.mover_ficha()

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    def test_finalizar_turno_sin_movimientos(self, _mock_input, _mock_print):
        """Test finalizar turno sin movimientos disponibles."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        jugador_inicial = self.cli._CLI__game.current_player
        self.cli.finalizar_turno()
        jugador_despues = self.cli._CLI__game.current_player
        self.assertNotEqual(jugador_inicial, jugador_despues)

    @patch('builtins.print')
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['n', ''])
    def test_finalizar_turno_con_movimientos_cancelar(self, _mock_input, _mock_roll, _mock_print):
        """Test finalizar turno con movimientos disponibles cancelando."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()
        jugador_inicial = self.cli._CLI__game.current_player
        self.cli.finalizar_turno()
        self.assertEqual(self.cli._CLI__game.current_player, jugador_inicial)

    @patch('builtins.print')
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['s', ''])
    def test_finalizar_turno_con_movimientos_confirmar(self, _mock_input, _mock_roll, _mock_print):
        """Test finalizar turno con movimientos disponibles confirmando."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()
        jugador_inicial = self.cli._CLI__game.current_player
        self.cli.finalizar_turno()
        self.assertNotEqual(self.cli._CLI__game.current_player, jugador_inicial)

    @patch('builtins.print')
    @patch('builtins.input', return_value='s')
    def test_rendirse_confirmar(self, _mock_input, _mock_print):
        """Test rendirse confirmando."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.rendirse()
        self.assertIsNone(self.cli._CLI__game)

    @patch('builtins.print')
    @patch('builtins.input', return_value='n')
    def test_rendirse_cancelar(self, _mock_input, _mock_print):
        """Test rendirse cancelando."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.rendirse()
        self.assertIsNotNone(self.cli._CLI__game)

    @patch('builtins.print')
    @patch('builtins.input', return_value='s')
    def test_volver_menu_principal_confirmar(self, _mock_input, _mock_print):
        """Test volver al menú principal confirmando."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.volver_menu_principal()
        self.assertIsNone(self.cli._CLI__game)

    @patch('builtins.print')
    @patch('builtins.input', return_value='n')
    def test_volver_menu_principal_cancelar(self, _mock_input, _mock_print):
        """Test volver al menú principal cancelando."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.volver_menu_principal()
        self.assertIsNotNone(self.cli._CLI__game)

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_mostrar_ganador(self, _mock_limpiar, _mock_input, _mock_print):
        """Test mostrar ganador."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.set_winner(self.cli._CLI__game.current_player)
        self.cli.mostrar_ganador()
        self.assertIsNone(self.cli._CLI__game)

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['1'])
    @patch('cli.Cli.CLI.nueva_partida')
    def test_ejecutar_menu_principal_opcion_1(self, mock_nueva, _mock_input, _mock_menu, _mock_print):
        """Test ejecutar menú principal opción 1."""
        self.cli.ejecutar_menu_principal()
        mock_nueva.assert_called_once()

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['2'])
    @patch('cli.Cli.CLI.mostrar_reglas')
    def test_ejecutar_menu_principal_opcion_2(self, mock_reglas, _mock_input, _mock_menu, _mock_print):
        """Test ejecutar menú principal opción 2."""
        self.cli.ejecutar_menu_principal()
        mock_reglas.assert_called_once()

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['3'])
    def test_ejecutar_menu_principal_opcion_3(self, _mock_input, _mock_menu, _mock_print):
        """Test ejecutar menú principal opción 3 (salir)."""
        # pylint: disable=protected-access
        self.cli.ejecutar_menu_principal()
        self.assertFalse(self.cli._CLI__running)

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['9', ''])
    def test_ejecutar_menu_principal_opcion_invalida(self, _mock_input, _mock_menu, _mock_print):
        """Test ejecutar menú principal con opción inválida."""
        # pylint: disable=protected-access
        self.cli.ejecutar_menu_principal()
        self.assertTrue(self.cli._CLI__running)

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_menu_partida')
    @patch('builtins.input', side_effect=['1'])
    @patch('cli.Cli.CLI.ver_tablero')
    def test_ejecutar_menu_partida_opcion_1(self, mock_ver, _mock_input, _mock_menu, _mock_print):
        """Test ejecutar menú partida opción 1."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.ejecutar_menu_partida()
        mock_ver.assert_called_once()

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_menu_partida')
    @patch('builtins.input', side_effect=['2'])
    @patch('cli.Cli.CLI.lanzar_dados')
    def test_ejecutar_menu_partida_opcion_2(self, mock_lanzar, _mock_input, _mock_menu, _mock_print):
        """Test ejecutar menú partida opción 2."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.ejecutar_menu_partida()
        mock_lanzar.assert_called_once()

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_menu_partida')
    @patch('builtins.input', side_effect=['9', ''])
    def test_ejecutar_menu_partida_opcion_invalida(self, _mock_input, _mock_menu, _mock_print):
        """Test ejecutar menú partida opción inválida."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli.ejecutar_menu_partida()

    @patch('builtins.print')
    @patch('cli.Cli.CLI.mostrar_ganador')
    @patch('cli.Cli.CLI.mostrar_menu_partida')
    def test_ejecutar_menu_partida_juego_terminado(self, _mock_menu, mock_ganador, _mock_print):
        """Test ejecutar menú partida cuando juego terminó."""
        # pylint: disable=protected-access
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.set_winner(self.cli._CLI__game.current_player)
        self.cli.ejecutar_menu_partida()
        mock_ganador.assert_called_once()

    def test_estado_inicial_running(self):
        """Test que el CLI inicia en estado running."""
        # pylint: disable=protected-access
        self.assertTrue(self.cli._CLI__running)

    def test_estado_inicial_sin_juego(self):
        """Test que el CLI inicia sin juego activo."""
        # pylint: disable=protected-access
        self.assertIsNone(self.cli._CLI__game)

    def test_move_executor_inicializado(self):
        """Test que move_executor está inicializado."""
        # pylint: disable=protected-access
        self.assertIsNotNone(self.cli._CLI__move_executor)

    def test_cli_puede_crear_juego(self):
        """Test que CLI puede crear un juego."""
        # pylint: disable=protected-access
        game = BackgammonGame("Jugador1", "Jugador2")
        self.cli._CLI__game = game
        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.current_player.nombre, "Jugador1")


if __name__ == '__main__':
    unittest.main()
