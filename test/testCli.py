"""Tests para la clase CLI."""
import unittest
from cli.Cli import CLI
from core.BackgammonGame import BackgammonGame
from unittest.mock import patch, MagicMock
from io import StringIO
from core.BackgammonGame import BackgammonGame


class TestCLI(unittest.TestCase):

    def setUp(self):
        """Configurar objetos antes de cada prueba."""
        self.cli = CLI()

    def test_inicializacion_cli(self):
        """Test que el CLI se inicializa correctamente."""
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

    def test_estado_inicial_running(self):
        """Test que el CLI inicia en estado running."""
        self.assertTrue(self.cli._CLI__running)

    def test_estado_inicial_sin_juego(self):
        """Test que el CLI inicia sin juego activo."""
        self.assertIsNone(self.cli._CLI__game)

    def test_move_executor_inicializado(self):
        """Test que move_executor está inicializado."""
        self.assertIsNotNone(self.cli._CLI__move_executor)

    def test_cli_puede_crear_juego(self):
        """Test que CLI puede crear un juego."""
        game = BackgammonGame("Jugador1", "Jugador2")
        self.cli._CLI__game = game
        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.current_player.nombre, "Jugador1")

    @patch('os.system')
    def test_limpiar_pantalla(self, mock_system):
        """Test limpiar pantalla."""
        self.cli.limpiar_pantalla()
        mock_system.assert_called_once()

    @patch('builtins.input', return_value='')
    @patch('cli.Cli.CLI.limpiar_pantalla')
    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_reglas(self, mock_stdout, mock_limpiar, mock_input):
        """Test mostrar reglas."""
        self.cli.mostrar_reglas()

        output = mock_stdout.getvalue()
        self.assertIn("REGLAS", output)
        self.assertIn("15 fichas", output)
        mock_limpiar.assert_called_once()

    @patch('builtins.input', side_effect=['Juan', 'Maria', ''])
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_nueva_partida(self, mock_limpiar, mock_input):
        """Test crear nueva partida."""
        self.cli.nueva_partida()

        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.current_player.nombre, "Juan")

    @patch('builtins.input', return_value='')
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_ver_tablero(self, mock_limpiar, mock_input):
        """Test ver tablero con juego iniciado."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.ver_tablero()
        mock_limpiar.assert_called()

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', return_value='')
    def test_lanzar_dados_exitoso(self, mock_input, mock_roll):
        """Test lanzar dados exitosamente."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.lanzar_dados()
        self.assertEqual(self.cli._CLI__game.dice.last_raw_roll, (3, 5))

    @patch('builtins.input', return_value='')
    def test_lanzar_dados_sin_juego(self, mock_input):
        """Test lanzar dados sin juego iniciado."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli.lanzar_dados()

    @patch('builtins.input', return_value='')
    def test_mover_ficha_sin_dados(self, mock_input):
        """Test mover ficha sin haber lanzado dados."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.mover_ficha()


    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['23', '3', ''])
    def test_mover_ficha_exitoso(self, mock_input, mock_roll):
        """Test mover ficha exitosamente."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()

        self.cli.mover_ficha()


    @patch('builtins.input', return_value='')
    def test_finalizar_turno_sin_movimientos(self, mock_input):
        """Test finalizar turno sin movimientos disponibles."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        jugador_inicial = self.cli._CLI__game.current_player
        self.cli.finalizar_turno()
        jugador_despues = self.cli._CLI__game.current_player

        self.assertNotEqual(jugador_inicial, jugador_despues)

    @patch('builtins.input', return_value='s')
    def test_rendirse_confirmar(self, mock_input):
        """Test rendirse confirmando."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.rendirse()

        self.assertIsNone(self.cli._CLI__game)

    @patch('builtins.input', return_value='n')
    def test_rendirse_cancelar(self, mock_input):
        """Test rendirse cancelando."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.rendirse()

        self.assertIsNotNone(self.cli._CLI__game)

    @patch('builtins.input', return_value='s')
    def test_volver_menu_principal_confirmar(self, mock_input):
        """Test volver al menú principal confirmando."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.volver_menu_principal()

        self.assertIsNone(self.cli._CLI__game)

    @patch('builtins.input', return_value='')
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_mostrar_ganador(self, mock_limpiar, mock_input):
        """Test mostrar ganador."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.set_winner(self.cli._CLI__game.current_player)

        self.cli.mostrar_ganador()

        self.assertIsNone(self.cli._CLI__game)
    @patch('builtins.input', side_effect=['', 'Juan', 'Maria', ''])

    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_nueva_partida_nombre_vacio(self, mock_limpiar, mock_input):
        """Test nueva partida con nombre vacío primero."""
        self.cli.nueva_partida()
        
        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.current_player.nombre, "Juan")

    @patch('builtins.input', side_effect=['Juan', '', 'Maria', ''])
    @patch('cli.Cli.CLI.limpiar_pantalla')
    def test_nueva_partida_segundo_nombre_vacio(self, mock_limpiar, mock_input):
        """Test nueva partida con segundo nombre vacío."""
        self.cli.nueva_partida()
        
        self.assertIsNotNone(self.cli._CLI__game)
        self.assertEqual(self.cli._CLI__game.other_player.nombre, "Maria")

    @patch('builtins.input', return_value='')
    def test_mover_ficha_sin_movimientos_disponibles(self, mock_input):
        """Test mover ficha cuando no quedan movimientos."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()
        # Usar todos los movimientos
        while self.cli._CLI__game.dice.get_moves_remaining() > 0:
            self.cli._CLI__game.dice.use_move(self.cli._CLI__game.dice.last_roll[0])

        self.cli.mover_ficha()

    @patch('builtins.input', side_effect=['abc', '3', ''])
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    def test_mover_ficha_input_invalido(self, mock_roll, mock_input):
        """Test mover ficha con input inválido."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()

        self.cli.mover_ficha()

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['10', '7', ''])
    def test_mover_ficha_error_valor(self, mock_input, mock_roll):
        """Test mover ficha con ValueError."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()

        self.cli.mover_ficha()

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['n', ''])
    def test_finalizar_turno_con_movimientos_cancelar(self, mock_input, mock_roll):
        """Test finalizar turno con movimientos disponibles cancelando."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()

        jugador_inicial = self.cli._CLI__game.current_player
        self.cli.finalizar_turno()


        self.assertEqual(self.cli._CLI__game.current_player, jugador_inicial)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5))
    @patch('builtins.input', side_effect=['s', ''])
    def test_finalizar_turno_con_movimientos_confirmar(self, mock_input, mock_roll):
        """Test finalizar turno con movimientos disponibles confirmando."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.roll_dice()

        jugador_inicial = self.cli._CLI__game.current_player
        self.cli.finalizar_turno()


        self.assertNotEqual(self.cli._CLI__game.current_player, jugador_inicial)

    @patch('builtins.input', return_value='n')
    def test_volver_menu_principal_cancelar(self, mock_input):
        """Test volver al menú principal cancelando."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.volver_menu_principal()

        self.assertIsNotNone(self.cli._CLI__game)

    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['1'])
    @patch('cli.Cli.CLI.nueva_partida')
    def test_ejecutar_menu_principal_opcion_1(self, mock_nueva, mock_input, mock_menu):
        """Test ejecutar menú principal opción 1."""
        self.cli.ejecutar_menu_principal()
        mock_nueva.assert_called_once()

    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['2'])
    @patch('cli.Cli.CLI.mostrar_reglas')
    def test_ejecutar_menu_principal_opcion_2(self, mock_reglas, mock_input, mock_menu):
        """Test ejecutar menú principal opción 2."""
        self.cli.ejecutar_menu_principal()
        mock_reglas.assert_called_once()

    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['3'])
    def test_ejecutar_menu_principal_opcion_3(self, mock_input, mock_menu):
        """Test ejecutar menú principal opción 3 (salir)."""
        self.cli.ejecutar_menu_principal()
        self.assertFalse(self.cli._CLI__running)

    @patch('cli.Cli.CLI.mostrar_menu_principal')
    @patch('builtins.input', side_effect=['9', ''])
    def test_ejecutar_menu_principal_opcion_invalida(self, mock_input, mock_menu):
        """Test ejecutar menú principal con opción inválida."""
        self.cli.ejecutar_menu_principal()
        self.assertTrue(self.cli._CLI__running)

    @patch('cli.Cli.CLI.mostrar_menu_partida')
    @patch('builtins.input', side_effect=['1'])
    @patch('cli.Cli.CLI.ver_tablero')
    def test_ejecutar_menu_partida_opcion_1(self, mock_ver, mock_input, mock_menu):
        """Test ejecutar menú partida opción 1."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.ejecutar_menu_partida()
        mock_ver.assert_called_once()

    @patch('cli.Cli.CLI.mostrar_menu_partida')
    @patch('builtins.input', side_effect=['2'])
    @patch('cli.Cli.CLI.lanzar_dados')
    def test_ejecutar_menu_partida_opcion_2(self, mock_lanzar, mock_input, mock_menu):
        """Test ejecutar menú partida opción 2."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        
        self.cli.ejecutar_menu_partida()
        mock_lanzar.assert_called_once()

    @patch('cli.Cli.CLI.mostrar_menu_partida')
    @patch('builtins.input', side_effect=['9', ''])
    def test_ejecutar_menu_partida_opcion_invalida(self, mock_input, mock_menu):
        """Test ejecutar menú partida opción inválida."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()

        self.cli.ejecutar_menu_partida()

    @patch('cli.Cli.CLI.mostrar_ganador')
    @patch('cli.Cli.CLI.mostrar_menu_partida')
    def test_ejecutar_menu_partida_juego_terminado(self, mock_menu, mock_ganador):
        """Test ejecutar menú partida cuando juego terminó."""
        self.cli._CLI__game = BackgammonGame("Juan", "Maria")
        self.cli._CLI__game.start_game()
        self.cli._CLI__game.set_winner(self.cli._CLI__game.current_player)

        self.cli.ejecutar_menu_partida()
        mock_ganador.assert_called_once()

if __name__ == '__main__':
    unittest.main()
