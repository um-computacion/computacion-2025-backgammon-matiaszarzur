import unittest
from core.ColorFicha import ColorFicha

class TestColorFicha(unittest.TestCase):

    def test_enum_tiene_valores_correctos(self):
        self.assertEqual(ColorFicha.BLANCA.value, 1)
        self.assertEqual(ColorFicha.NEGRA.value, 2)

    def test_enum_tiene_nombres_correctos(self):
        self.assertEqual(ColorFicha.BLANCA.name, 'BLANCA')
        self.assertEqual(ColorFicha.NEGRA.name, 'NEGRA')

    def test_representacion_string(self):
        self.assertEqual(str(ColorFicha.BLANCA), 'ColorFicha.BLANCA')
        self.assertEqual(str(ColorFicha.NEGRA), 'ColorFicha.NEGRA')

    def test_comparacion_colores(self):
        self.assertEqual(ColorFicha.BLANCA, ColorFicha.BLANCA)
        self.assertEqual(ColorFicha.NEGRA, ColorFicha.NEGRA)
        self.assertNotEqual(ColorFicha.BLANCA, ColorFicha.NEGRA)

    def test_acceso_por_valor(self):
        self.assertEqual(ColorFicha(1), ColorFicha.BLANCA)
        self.assertEqual(ColorFicha(2), ColorFicha.NEGRA)

    def test_valor_invalido_genera_error(self):
        with self.assertRaises(ValueError):
            ColorFicha(3)
        
        with self.assertRaises(ValueError):
            ColorFicha(0)

    def test_enum_es_iterable(self):
        colores = list(ColorFicha)
        self.assertEqual(len(colores), 2)
        self.assertIn(ColorFicha.BLANCA, colores)
        self.assertIn(ColorFicha.NEGRA, colores)

    def test_tipo_de_instancia(self):
        self.assertIsInstance(ColorFicha.BLANCA, ColorFicha)
        self.assertIsInstance(ColorFicha.NEGRA, ColorFicha)

    def test_hash_consistente(self):
        colores_set = {ColorFicha.BLANCA, ColorFicha.NEGRA, ColorFicha.BLANCA}
        self.assertEqual(len(colores_set), 2) 

    def test_bool_conversion(self):
        self.assertTrue(ColorFicha.BLANCA)
        self.assertTrue(ColorFicha.NEGRA)
