"""Tests para la clase DiceRoller."""
import unittest
from unittest.mock import patch
from core.DiceRoller import DiceRoller


class TestDiceRoller(unittest.TestCase):

    @patch('random.randint', side_effect=[3, 5])
    def test_roll_two_dice_different_values(self, mock_randint):
        """Test que roll_two_dice devuelve dos valores diferentes."""
        result = DiceRoller.roll_two_dice()

        self.assertEqual(result, (3, 5))
        self.assertEqual(mock_randint.call_count, 2)
        mock_randint.assert_any_call(1, 6)

    @patch('random.randint', return_value=2)
    def test_roll_two_dice_same_values(self, mock_randint):
        """Test que roll_two_dice puede devolver valores iguales."""
        result = DiceRoller.roll_two_dice()

        self.assertEqual(result, (2, 2))
        self.assertEqual(mock_randint.call_count, 2)
        mock_randint.assert_any_call(1, 6)

    @patch('random.randint', side_effect=[1, 6])
    def test_roll_two_dice_min_max_values(self, mock_randint):
        """Test que roll_two_dice maneja valores mínimos y máximos."""
        result = DiceRoller.roll_two_dice()

        self.assertEqual(result, (1, 6))
        self.assertEqual(mock_randint.call_count, 2)

    @patch('random.randint', side_effect=[6, 1])
    def test_roll_two_dice_max_min_values(self, mock_randint):
        """Test que roll_two_dice maneja valores máximos y mínimos."""
        result = DiceRoller.roll_two_dice()

        self.assertEqual(result, (6, 1))
        self.assertEqual(mock_randint.call_count, 2)

    @patch('random.randint', side_effect=Exception("Random error"))
    def test_roll_two_dice_exception_handling(self, mock_randint):
        """Test que roll_two_dice propaga excepciones del generador."""
        with self.assertRaises(Exception) as context:
            DiceRoller.roll_two_dice()

        self.assertEqual(str(context.exception), "Random error")
        self.assertTrue(mock_randint.called)

    def test_roll_two_dice_returns_tuple(self):
        """Test que roll_two_dice siempre devuelve una tupla."""
        result = DiceRoller.roll_two_dice()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_roll_two_dice_values_in_range(self):
        """Test que roll_two_dice devuelve valores en el rango 1-6."""
        # Test sin mock para verificar el comportamiento real
        for _ in range(100):  # Múltiples iteraciones para mayor confianza
            result = DiceRoller.roll_two_dice()

            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)

            dice1, dice2 = result
            self.assertGreaterEqual(dice1, 1)
            self.assertLessEqual(dice1, 6)
            self.assertGreaterEqual(dice2, 1)
            self.assertLessEqual(dice2, 6)

    @patch('random.randint')
    def test_roll_two_dice_calls_randint_correctly(self, mock_randint):
        """Test que roll_two_dice llama a randint con los parámetros correctos."""
        mock_randint.side_effect = [4, 3]

        result = DiceRoller.roll_two_dice()


        expected_calls = [unittest.mock.call(1, 6), unittest.mock.call(1, 6)]
        mock_randint.assert_has_calls(expected_calls)
        self.assertEqual(result, (4, 3))

    def test_roll_two_dice_multiple_calls_independent(self):
        """Test que múltiples llamadas a roll_two_dice son independientes."""
        results = []


        for _ in range(10):
            result = DiceRoller.roll_two_dice()
            results.append(result)
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
        
        # Verificar que obtuvimos resultados (aunque podrían ser iguales por casualidad)
        self.assertEqual(len(results), 10)

    @patch('random.randint', side_effect=[1, 1])
    def test_roll_two_dice_minimum_double(self, mock_randint):
        """Test roll con el valor mínimo doble (1,1)."""
        result = DiceRoller.roll_two_dice()

        self.assertEqual(result, (1, 1))

    @patch('random.randint', side_effect=[6, 6])  
    def test_roll_two_dice_maximum_double(self, mock_randint):
        """Test roll con el valor máximo doble (6,6)."""
        result = DiceRoller.roll_two_dice()

        self.assertEqual(result, (6, 6))


if __name__ == '__main__':
    unittest.main()
