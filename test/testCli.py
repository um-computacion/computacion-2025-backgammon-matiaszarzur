"""Tests para la clase CLI."""
import unittest
from cli.Cli import CLI


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

    def test_estado_inicial_running(self):
        """Test que el CLI inicia en estado running."""
        self.assertTrue(self.cli._CLI__running)

    def test_estado_inicial_sin_juego(self):
        """Test que el CLI inicia sin juego activo."""
        self.assertIsNone(self.cli._CLI__game)


if __name__ == '__main__':
    unittest.main()