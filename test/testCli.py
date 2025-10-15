"""Tests para la clase CLI."""
import unittest
from cli.Cli import CLI
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


if __name__ == '__main__':
    unittest.main()