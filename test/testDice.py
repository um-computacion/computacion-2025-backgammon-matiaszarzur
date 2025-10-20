from core.Dice import Dice
from unittest import TestCase
from unittest.mock import patch

#Para la creacion de los test se presenta el problema de que genera numeros aleatorios, entonces cada vez que ejecutamos el test obtendriamos resultados diferentes. Para esto se utiliza el mocking
#El mocking es remplazar temporalmente una funcion por una version controlada de la misma, asi podemos predecir los resultados.

class TestDice(TestCase):

    # @patch.object(Clase, 'metodo', side_effect=[5, 2])
    # def test_method(self, randint_patched):
    #     ...
    def setUp(self):
        self.dice = Dice()
        
    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(5, 2))
    def test_simple(self, mock_roll):
        raw_roll = self.dice.roll()
        self.assertEqual(raw_roll, (5, 2))
        self.assertEqual(len(self.dice.last_roll), 2)
        self.assertEqual(self.dice.last_roll[0], 5)
        self.assertEqual(self.dice.last_roll[1], 2)
        self.assertTrue(mock_roll.called)
        self.assertEqual(mock_roll.call_count, 1)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(1, 1))
    def test_complex(self, mock_roll):
        dice = Dice()
        raw_roll = dice.roll()
        self.assertEqual(raw_roll, (1, 1))
        self.assertEqual(len(dice.last_roll), 4)
        self.assertEqual(dice.last_roll[0], 1)
        self.assertEqual(dice.last_roll[1], 1)
        self.assertEqual(dice.last_roll[2], 1)
        self.assertEqual(dice.last_roll[3], 1)
        self.assertTrue(mock_roll.called)
        self.assertEqual(mock_roll.call_count, 1)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', side_effect=Exception("error!!"))
    def test_error(self, mock_roll):
        dice = Dice()
        with self.assertRaises(Exception):
            dice.roll()
        self.assertTrue(mock_roll.called)
        self.assertEqual(mock_roll.call_count, 1)


    def test_double(self):
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(5, 2)) as mock_roll:
            dice = Dice()
            raw_roll = dice.roll()
            self.assertEqual(raw_roll, (5, 2))
            self.assertEqual(len(dice.last_roll), 2)
            self.assertEqual(dice.last_roll[0], 5)
            self.assertEqual(dice.last_roll[1], 2)
            self.assertTrue(mock_roll.called)
            self.assertEqual(mock_roll.call_count, 1)

        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(1, 1)) as mock_roll:
            dice = Dice()
            raw_roll = dice.roll()
            self.assertEqual(raw_roll, (1, 1))
            self.assertEqual(len(dice.last_roll), 4)
            self.assertEqual(dice.last_roll[0], 1)
            self.assertEqual(dice.last_roll[1], 1)
            self.assertEqual(dice.last_roll[2], 1)
            self.assertEqual(dice.last_roll[3], 1)
            self.assertTrue(mock_roll.called)
            self.assertEqual(mock_roll.call_count, 1)

    def test_dice_initial_state(self):
        dice = Dice()
        self.assertEqual(dice.last_roll, ())
        self.assertIsNone(dice.last_raw_roll)
        self.assertEqual(dice.get_moves_remaining(), 0)
        self.assertFalse(dice.is_double())

    def test_is_double_method(self):
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 3)):
            dice.roll()
            self.assertTrue(dice.is_double())
            dice.clear_roll()
            self.assertFalse(dice.is_double())

        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(1, 6)):
            dice.roll()
            self.assertFalse(dice.is_double())
    
    def test_get_moves_remaining_method(self):
        self.assertEqual(Dice().get_moves_remaining(), 0)
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 3)):
            dice.roll()
            self.assertEqual(dice.get_moves_remaining(), 4)
            dice.clear_roll()
            self.assertEqual(dice.get_moves_remaining(), 0)
            self.assertFalse(dice.is_double())

    def test_clear_roll_method(self):
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 3)):
            dice.roll()
            self.assertEqual(dice.get_moves_remaining(), 4)
            dice.clear_roll()
            self.assertEqual(dice.get_moves_remaining(), 0)

    def test_get_roll_values_none(self):
        self.assertIsNone(self.dice.get_roll_values())

    def test_get_roll_values_double(self):
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(5, 5)):
            self.dice.roll()
            self.assertEqual(self.dice.get_roll_values(), (5, 5))

    def test_get_roll_values_normal(self):
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 6)):
            self.dice.roll()
            self.assertEqual(self.dice.get_roll_values(), (2, 6))

    def test_use_move_not_found(self):
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 3)):
            self.dice.roll()
            result = self.dice.use_move(5)  # no existe
            self.assertFalse(result)
            self.assertEqual(self.dice.last_roll, (2, 3))

    def test_use_move_not_found_branch(self):
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 3)):
            dice.roll()
            result = dice.use_move(6)  # 6 no está en la tirada
            self.assertFalse(result)
            self.assertEqual(dice.last_roll, (2, 3))  # no cambia

    def test_use_move_no_last_roll(self):
        """Test use_move cuando no hay tirada previa (last_roll es None)"""
        dice = Dice()
        result = dice.use_move(3)
        self.assertFalse(result)
        self.assertEqual(dice.last_roll, ())

    def test_use_move_found_normal_roll(self):
        """Test use_move con tirada normal - encontrando el movimiento"""
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 5)):
            dice.roll()
            result = dice.use_move(2)
            self.assertTrue(result)
            self.assertEqual(dice.last_roll, (5,))  # queda solo el 5

    def test_use_move_found_double_roll(self):
        """Test use_move con dobles - usando uno de los movimientos"""
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(4, 4)):
            dice.roll()
            result = dice.use_move(4)
            self.assertTrue(result)
            self.assertEqual(dice.last_roll, (4, 4, 4))  # queda con 3 movimientos

    def test_use_move_sequential_usage(self):
        """Test usando movimientos secuencialmente hasta agotarlos"""
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 6)):
            dice.roll()

            # Usar primer movimiento
            result1 = dice.use_move(3)
            self.assertTrue(result1)
            self.assertEqual(dice.last_roll, (6,))
            self.assertEqual(dice.get_moves_remaining(), 1)

            # Usar segundo movimiento
            result2 = dice.use_move(6)
            self.assertTrue(result2)
            self.assertEqual(dice.last_roll, ())
            self.assertEqual(dice.get_moves_remaining(), 0)

            # Intentar usar movimiento cuando ya no hay
            result3 = dice.use_move(3)
            self.assertFalse(result3)

    def test_use_move_double_sequential(self):
        """Test usando dobles secuencialmente"""
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 2)):
            dice.roll()

            # Usar tres movimientos
            for i in range(3):
                result = dice.use_move(2)
                self.assertTrue(result)
                self.assertEqual(dice.get_moves_remaining(), 3-i)

            # El último movimiento
            result = dice.use_move(2)
            self.assertTrue(result)
            self.assertEqual(dice.get_moves_remaining(), 0)
            self.assertEqual(dice.last_roll, ())

    def test_is_double_after_use_move(self):
        """Test is_double después de usar movimientos"""
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 3)):
            dice.roll()
            self.assertTrue(dice.is_double())  # 4 elementos = doble

            # Usar un movimiento - ya no es considerado doble
            dice.use_move(3)
            self.assertFalse(dice.is_double())  # Solo 3 elementos, no es doble según la implementación

            # Confirmar que sigue siendo False con menos elementos
            dice.use_move(3)
            dice.use_move(3)
            self.assertFalse(dice.is_double())  # Solo queda 1 elemento

    def test_is_double_exact_behavior(self):
        """Test que is_double() solo es True con exactamente 4 elementos"""
        dice = Dice()
        # Test con diferentes longitudes usando roll real
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 2)):
            dice.roll()
            self.assertTrue(dice.is_double())  # 4 elementos después del roll

            dice.use_move(2)  # 3 elementos
            self.assertFalse(dice.is_double())

            dice.use_move(2)  # 2 elementos
            self.assertFalse(dice.is_double())

            dice.use_move(2)  # 1 elemento
            self.assertFalse(dice.is_double())

            dice.use_move(2)  # 0 elementos
            self.assertFalse(dice.is_double())

    def test_get_roll_values_after_partial_use(self):
        """Test get_roll_values después de usar algunos movimientos"""
        dice = Dice()
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(5, 5)):
            dice.roll()
            dice.use_move(5)  # Usar uno
            self.assertEqual(dice.get_roll_values(), (5, 5))  # Devuelve el raw_roll original

        # Test con tirada normal después de usar un movimiento
        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(2, 6)):
            dice.roll()
            dice.use_move(2)  # queda solo (6,)
            self.assertEqual(dice.get_roll_values(), (2, 6))  # Aún devuelve el raw_roll original

    def test_edge_cases_empty_roll(self):
        """Test casos edge cuando last_roll está vacío"""
        dice = Dice()
        # Sin necesidad de establecer last_roll manualmente, ya es () por defecto
        self.assertEqual(dice.get_moves_remaining(), 0)
        self.assertFalse(dice.is_double())
        result = dice.use_move(1)
        self.assertFalse(result)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(6, 1))
    def test_roll_different_values(self, mock_roll):
        """Test roll con valores diferentes (no dobles)"""
        dice = Dice()
        result = dice.roll()
        self.assertEqual(result, (6, 1))
        self.assertEqual(dice.last_roll, (6, 1))
        self.assertFalse(dice.is_double())
        self.assertEqual(dice.get_moves_remaining(), 2)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(1, 1))
    def test_roll_minimum_double(self, mock_roll):
        """Test roll con el mínimo valor doble (1,1)"""
        dice = Dice()
        result = dice.roll()
        self.assertEqual(result, (1, 1))
        self.assertEqual(dice.last_roll, (1, 1, 1, 1))
        self.assertTrue(dice.is_double())
        self.assertEqual(dice.get_moves_remaining(), 4)

    @patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(6, 6))
    def test_roll_maximum_double(self, mock_roll):
        """Test roll con el máximo valor doble (6,6)"""
        dice = Dice()
        result = dice.roll()
        self.assertEqual(result, (6, 6))
        self.assertEqual(dice.last_roll, (6, 6, 6, 6))
        self.assertTrue(dice.is_double())
        self.assertEqual(dice.get_moves_remaining(), 4)

    def test_has_moves_available(self):
        """Test has_moves_available method"""
        dice = Dice()
        self.assertFalse(dice.has_moves_available())  # Sin movimientos inicialmente

        with patch('core.DiceRoller.DiceRoller.roll_two_dice', return_value=(3, 5)):
            dice.roll()
            self.assertTrue(dice.has_moves_available())

            dice.use_move(3)
            self.assertTrue(dice.has_moves_available())  # Aún queda el 5

            dice.use_move(5)
            self.assertFalse(dice.has_moves_available())  # Ya no quedan movimientos
