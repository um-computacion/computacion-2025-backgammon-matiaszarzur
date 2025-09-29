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
    
    def test_checker_str_representation(self):
        """Test del método __str__."""
        ficha_blanca = Checker(ColorFicha.BLANCA)
        ficha_negra = Checker(ColorFicha.NEGRA)
    
        self.assertEqual(str(ficha_blanca), "Checker(BLANCA)")
        self.assertEqual(str(ficha_negra), "Checker(NEGRA)")

    def test_checker_equality_with_non_checker(self):
        """Test comparación de igualdad con objeto que no es Checker."""
        ficha = Checker(ColorFicha.BLANCA)
    
        # Comparar con string
        self.assertFalse(ficha == "no es checker")
    
        # Comparar con None
        self.assertFalse(ficha == None)
    
        # Comparar con número
        self.assertFalse(ficha == 123)
    
        # Comparar con lista
        self.assertFalse(ficha == [])

    def test_checker_equality_different_colors(self):
        """Test comparación entre fichas de diferente color."""
        ficha_blanca = Checker(ColorFicha.BLANCA)
        ficha_negra = Checker(ColorFicha.NEGRA)

        self.assertFalse(ficha_blanca == ficha_negra)
        self.assertFalse(ficha_negra == ficha_blanca)
