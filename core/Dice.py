"""Clase que representa los dados del Backgammon."""
import random

class Dice:
    """Clase que representa los dados del Backgammon."""
    def __init__(self):
        """Inicializar dados sin valor."""
        self.__last_roll = None

    @property
    def last_roll(self):
        """Obtener el último lanzamiento de dados."""
        return self.__last_roll

    @last_roll.setter
    def last_roll(self, value):
        """Establecer el último lanzamiento de dados."""
        if isinstance(value, tuple):
            self.__last_roll = value
        else:
            raise ValueError("last_roll debe ser una tupla")

    def roll(self):
        """Lanzar los dados y obtener el resultado."""
        dice_0 = random.randint(1, 6)
        dice_1 = random.randint(1, 6)
        if dice_0 == dice_1:
            # Dobles: 4 movimientos del mismo valor
            self.__last_roll = (dice_0, dice_0, dice_0, dice_0)
        else:
            self.__last_roll = (dice_0, dice_1)
        return self.__last_roll

    def is_double(self):
        """Verificar si el último lanzamiento fue un doble."""
        return self.__last_roll is not None and len(self.__last_roll) == 4

    def get_moves_remaining(self):
        """Obtener los movimientos restantes basados en el último lanzamiento."""
        return len(self.__last_roll) if self.__last_roll else 0

    def clear_roll(self):
        """Limpiar el último lanzamiento."""
        self.__last_roll = None

    def get_roll_values(self):
        """Obtener los valores del último lanzamiento."""
        if not self.__last_roll:
            return None
        if self.is_double():
            return (self.__last_roll[0], self.__last_roll[0])
        return (self.__last_roll[0], self.__last_roll[1])

    def use_move(self, move):
        """Usar un movimiento basado en el último lanzamiento."""
        if not self.__last_roll:
            return False
        if move in self.__last_roll:
            last_roll_list = list(self.__last_roll)
            last_roll_list.remove(move)  # elimina solo la primera ocurrencia
            self.__last_roll = tuple(last_roll_list)
            return True
        return False
