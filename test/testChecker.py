import unittest
from core.Checker import Checker
from core.ColorFicha import ColorFicha
from test.testTipoFicha import ColorFicha

class TestChecker(unittest.TestCase):

    def setUp(self):
        self.checker = Checker(ColorFicha.BLANCA)

    def test_color(self):
        self.assertEqual(self.checker.color, ColorFicha.BLANCA)

    def test_color_negro(self):
        self.checker = Checker(ColorFicha.NEGRA)
        self.assertEqual(self.checker.color, ColorFicha.NEGRA)
        
    def test_color_blanca_nombre(self):
        """Test que BLANCA tenga el nombre correcto."""
        self.assertEqual(ColorFicha.BLANCA.name, 'BLANCA')

    def test_color_negra_nombre(self):
        """Test que NEGRA tenga el nombre correcto."""
        self.assertEqual(ColorFicha.NEGRA.name, 'NEGRA')

    def test_colores_son_diferentes(self):
        """Test que BLANCA y NEGRA sean diferentes."""
        self.assertNotEqual(ColorFicha.BLANCA, ColorFicha.NEGRA)    
