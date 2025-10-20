"""Tests para la clase Player."""
import unittest
from core.Player import Player
from core.ColorFicha import ColorFicha


class TestPlayer(unittest.TestCase):

    def test_crear_player_valido(self):
        """Test crear jugador con datos válidos."""
        player = Player("Juan", ColorFicha.BLANCA)

        self.assertEqual(player.nombre, "Juan")
        self.assertEqual(player.color, ColorFicha.BLANCA)

    def test_crear_player_color_negro(self):
        """Test crear jugador con color negro."""
        player = Player("Maria", ColorFicha.NEGRA)

        self.assertEqual(player.nombre, "Maria")
        self.assertEqual(player.color, ColorFicha.NEGRA)

    def test_nombre_se_limpia_espacios(self):
        """Test que el nombre elimina espacios en blanco al inicio y final."""
        player = Player("  Pedro  ", ColorFicha.BLANCA)

        self.assertEqual(player.nombre, "Pedro")

    def test_nombre_vacio_lanza_error(self):
        """Test que nombre vacío lanza ValueError."""
        with self.assertRaises(ValueError) as context:
            Player("", ColorFicha.BLANCA)

        self.assertEqual(str(context.exception), "El nombre del jugador no puede estar vacío")

    def test_nombre_solo_espacios_lanza_error(self):
        """Test que nombre con solo espacios lanza ValueError."""
        with self.assertRaises(ValueError) as context:
            Player("   ", ColorFicha.BLANCA)

        self.assertEqual(str(context.exception), "El nombre del jugador no puede estar vacío")

    def test_nombre_none_lanza_error(self):
        """Test que nombre None lanza error."""
        with self.assertRaises(ValueError):
            Player(None, ColorFicha.BLANCA)

    def test_color_invalido_lanza_error(self):
        """Test que color inválido lanza TypeError."""
        with self.assertRaises(TypeError):
            Player("Juan", "blanco")

    def test_color_none_lanza_error(self):
        """Test que color None lanza TypeError."""
        with self.assertRaises(TypeError):
            Player("Juan", None)

    def test_color_numero_lanza_error(self):
        """Test que color como número lanza TypeError."""
        with self.assertRaises(TypeError):
            Player("Juan", 1)

    def test_str_representation(self):
        """Test del método __str__."""
        player_blanco = Player("Ana", ColorFicha.BLANCA)
        player_negro = Player("Luis", ColorFicha.NEGRA)

        self.assertEqual(str(player_blanco), "Player(Ana, BLANCA)")
        self.assertEqual(str(player_negro), "Player(Luis, NEGRA)")

    def test_repr_representation(self):
        """Test del método __repr__."""
        player = Player("Carlos", ColorFicha.BLANCA)

        repr_str = repr(player)
        self.assertIn("Player", repr_str)
        self.assertIn("Carlos", repr_str)
        self.assertIn("ColorFicha.BLANCA", repr_str)

    def test_igualdad_players_iguales(self):
        """Test comparación de igualdad entre jugadores iguales."""
        player1 = Player("Juan", ColorFicha.BLANCA)
        player2 = Player("Juan", ColorFicha.BLANCA)

        self.assertEqual(player1, player2)

    def test_igualdad_players_diferente_nombre(self):
        """Test comparación entre jugadores con diferente nombre."""
        player1 = Player("Juan", ColorFicha.BLANCA)
        player2 = Player("Maria", ColorFicha.BLANCA)

        self.assertNotEqual(player1, player2)

    def test_igualdad_players_diferente_color(self):
        """Test comparación entre jugadores con diferente color."""
        player1 = Player("Juan", ColorFicha.BLANCA)
        player2 = Player("Juan", ColorFicha.NEGRA)

        self.assertNotEqual(player1, player2)

    def test_igualdad_con_no_player(self):
        """Test comparación con objeto que no es Player."""
        player = Player("Juan", ColorFicha.BLANCA)

        self.assertNotEqual(player, "Juan")
        self.assertNotEqual(player, None)
        self.assertNotEqual(player, 123)
        self.assertNotEqual(player, [])

    def test_properties_son_readonly(self):
        """Test que las properties no tienen setter."""
        player = Player("Juan", ColorFicha.BLANCA)

        with self.assertRaises(AttributeError):
            player.nombre = "Pedro"

        with self.assertRaises(AttributeError):
            player.color = ColorFicha.NEGRA


if __name__ == '__main__':
    unittest.main()
