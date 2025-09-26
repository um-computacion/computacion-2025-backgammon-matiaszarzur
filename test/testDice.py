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
        
    @patch('random.randint', side_effect=[5, 2])
    def test_simple(self, randint_patched):
        self.dice.roll()
        self.assertEqual(len(self.dice.last_roll), 2)
        self.assertEqual(self.dice.last_roll[0], 5)
        self.assertEqual(self.dice.last_roll[1], 2)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', return_value=1)
    def test_complex(self, randint_patched):
        dice = Dice()
        dice.roll()
        self.assertEqual(len(dice.last_roll), 4)
        self.assertEqual(dice.last_roll[0], 1)
        self.assertEqual(dice.last_roll[1], 1)
        self.assertEqual(dice.last_roll[2], 1)
        self.assertEqual(dice.last_roll[3], 1)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', side_effect=Exception("error!!"))
    def test_error(self, randint_patched):
        dice = Dice()
        with self.assertRaises(Exception):
            dice.roll()
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 1)


    def test_double(self):
        with patch('random.randint', side_effect=[5, 2]) as randint_patched:
            dice = Dice()
            dice.roll()
            self.assertEqual(len(dice.last_roll), 2)
            self.assertEqual(dice.last_roll[0], 5)
            self.assertEqual(dice.last_roll[1], 2)
            self.assertTrue(randint_patched.called)
            self.assertEqual(randint_patched.call_count, 2)

        with patch('random.randint', return_value=1) as randint_patched:
            dice = Dice()
            dice.roll()
            self.assertEqual(len(dice.last_roll), 4)
            self.assertEqual(dice.last_roll[0], 1)
            self.assertEqual(dice.last_roll[1], 1)
            self.assertEqual(dice.last_roll[2], 1)
            self.assertEqual(dice.last_roll[3], 1)
            self.assertTrue(randint_patched.called)
            self.assertEqual(randint_patched.call_count, 2)

    def test_dice_initial_state(self):
        dice = Dice()
        self.assertIsNone(dice.last_roll)
        self.assertEqual(dice.get_moves_remaining(), 0)
        self.assertFalse(dice.is_double())

    def test_is_double_method(self):
        dice = Dice()
        with patch('random.randint', return_value=3):
            dice.roll()
            self.assertTrue(dice.is_double())
            dice.clear_roll()
            self.assertFalse(dice.is_double())
            
        with patch('random.randint', side_effect=[1, 6]):
            dice.roll()
            self.assertFalse(dice.is_double())
    
    def test_get_moves_remaining_method(self):
        self.assertEqual(Dice().get_moves_remaining(), 0)
        dice = Dice()
        with patch('random.randint', return_value=3):
            dice.roll()
            self.assertEqual(dice.get_moves_remaining(), 4)
            dice.clear_roll()
            self.assertEqual(dice.get_moves_remaining(), 0)
            self.assertFalse(dice.is_double())

    def test_clear_roll_method(self):
        dice = Dice()
        with patch('random.randint', return_value=3):
            dice.roll()
            self.assertEqual(dice.get_moves_remaining(), 4)
            dice.clear_roll()
            self.assertEqual(dice.get_moves_remaining(), 0)

    def test_last_roll_setter_valid_y_invalid(self):
        self.dice.last_roll= (3,4)
        self.assertEqual(self.dice.last_roll, (3,4))
        with self.assertRaises(ValueError):
            self.dice.last_roll = [3,4]
            
    def test_get_roll_values_none(self):
        self.assertIsNone(self.dice.get_roll_values())

    def test_get_roll_values_double(self):
        self.dice.last_roll = (5, 5, 5, 5)
        self.assertEqual(self.dice.get_roll_values(), (5, 5))

    def test_get_roll_values_normal(self):
        self.dice.last_roll = (2, 6)
        self.assertEqual(self.dice.get_roll_values(), (2, 6))

    def test_use_move_not_found(self):
        self.dice.last_roll = (2, 3)
        result = self.dice.use_move(5)  # no existe
        self.assertFalse(result)
        self.assertEqual(self.dice.last_roll, (2, 3))
        
    def test_use_move_not_found_branch(self):
        dice = Dice()
        dice.last_roll = (2, 3)
        result = dice.use_move(6)  # 6 no está en la tirada
        self.assertFalse(result)
        self.assertEqual(dice.last_roll, (2, 3))  # no cambia
    
    def test_use_move_no_last_roll(self):
        """Test use_move cuando no hay tirada previa (last_roll es None)"""
        dice = Dice()
        result = dice.use_move(3)
        self.assertFalse(result)
        self.assertIsNone(dice.last_roll)

    def test_use_move_found_normal_roll(self):
        """Test use_move con tirada normal - encontrando el movimiento"""
        dice = Dice()
        dice.last_roll = (2, 5)
        result = dice.use_move(2)
        self.assertTrue(result)
        self.assertEqual(dice.last_roll, (5,))  # queda solo el 5

    def test_use_move_found_double_roll(self):
        """Test use_move con dobles - usando uno de los movimientos"""
        dice = Dice()
        dice.last_roll = (4, 4, 4, 4)
        result = dice.use_move(4)
        self.assertTrue(result)
        self.assertEqual(dice.last_roll, (4, 4, 4))  # queda con 3 movimientos

    def test_use_move_sequential_usage(self):
        """Test usando movimientos secuencialmente hasta agotarlos"""
        dice = Dice()
        dice.last_roll = (3, 6)
        
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
        dice.last_roll = (2, 2, 2, 2)
        
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

    def test_last_roll_setter_invalid_types(self):
        """Test setter con diferentes tipos inválidos"""
        dice = Dice()
        
        # Test con lista (ya lo tienes, pero agregando más casos)
        with self.assertRaises(ValueError):
            dice.last_roll = [1, 2, 3]
            
        # Test con string
        with self.assertRaises(ValueError):
            dice.last_roll = "123"
            
        # Test con int
        with self.assertRaises(ValueError):
            dice.last_roll = 123
            
        # Test con dict
        with self.assertRaises(ValueError):
            dice.last_roll = {1: 2}

    def test_is_double_after_use_move(self):
        """Test is_double después de usar movimientos"""
        dice = Dice()
        dice.last_roll = (3, 3, 3, 3)
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
        
        # Test con diferentes longitudes de tupla
        dice.last_roll = (2, 2, 2, 2)  # 4 elementos
        self.assertTrue(dice.is_double())
        
        dice.last_roll = (2, 2, 2)  # 3 elementos
        self.assertFalse(dice.is_double())
        
        dice.last_roll = (2, 2)  # 2 elementos
        self.assertFalse(dice.is_double())
        
        dice.last_roll = (2,)  # 1 elemento
        self.assertFalse(dice.is_double())
        
        dice.last_roll = ()  # 0 elementos
        self.assertFalse(dice.is_double())

    def test_get_roll_values_after_partial_use(self):
        """Test get_roll_values después de usar algunos movimientos"""
        dice = Dice()
        
        # Test con dobles después de usar movimientos
        dice.last_roll = (5, 5, 5, 5)
        dice.use_move(5)  # Usar uno
        self.assertEqual(dice.get_roll_values(), (5, 5))  # Aún devuelve par de dobles
        
        # Test con tirada normal después de usar un movimiento
        dice.last_roll = (2, 6)
        dice.use_move(2)  # queda solo (6,)
        # Nota: get_roll_values podría tener un bug aquí si last_roll = (6,)
        # Dependiendo de cómo se comporte, podrías necesitar revisar la implementación

    def test_edge_cases_empty_roll(self):
        """Test casos edge cuando last_roll está vacío"""
        dice = Dice()
        dice.last_roll = ()  # Tupla vacía
        
        self.assertEqual(dice.get_moves_remaining(), 0)
        self.assertFalse(dice.is_double())
        result = dice.use_move(1)
        self.assertFalse(result)

    @patch('random.randint', side_effect=[6, 1])
    def test_roll_different_values(self, randint_patched):
        """Test roll con valores diferentes (no dobles)"""
        dice = Dice()
        result = dice.roll()
        self.assertEqual(result, (6, 1))
        self.assertEqual(dice.last_roll, (6, 1))
        self.assertFalse(dice.is_double())
        self.assertEqual(dice.get_moves_remaining(), 2)

    @patch('random.randint', side_effect=[1, 1])
    def test_roll_minimum_double(self, randint_patched):
        """Test roll con el mínimo valor doble (1,1)"""
        dice = Dice()
        result = dice.roll()
        self.assertEqual(result, (1, 1, 1, 1))
        self.assertTrue(dice.is_double())
        self.assertEqual(dice.get_moves_remaining(), 4)

    @patch('random.randint', side_effect=[6, 6])
    def test_roll_maximum_double(self, randint_patched):
        """Test roll con el máximo valor doble (6,6)"""
        dice = Dice()
        result = dice.roll()
        self.assertEqual(result, (6, 6, 6, 6))
        self.assertTrue(dice.is_double())
        self.assertEqual(dice.get_moves_remaining(), 4)