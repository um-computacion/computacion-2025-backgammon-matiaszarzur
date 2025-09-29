"""Clase para manejo de dados en backgammon."""
from core.DiceRoller import DiceRoller


class Dice:
    """Maneja dados y movimientos disponibles en backgammon."""
    
    def __init__(self):
        """Inicializar dados sin lanzamiento."""
        self.__available_moves = []
        self.__last_raw_roll = None
    
    @property
    def last_roll(self):
        """Obtener los movimientos disponibles del último lanzamiento."""
        return tuple(self.__available_moves)
    
    @property
    def last_raw_roll(self):
        """Obtener los valores originales del último lanzamiento."""
        return self.__last_raw_roll
    
    @staticmethod
    def _process_roll(dice_values):
        """Aplicar reglas de backgammon a un lanzamiento.
        
        Args:
            dice_values (tuple): Valores de los dos dados
            
        Returns:
            tuple: Movimientos disponibles según reglas de backgammon
        """
        dice_0, dice_1 = dice_values
        if dice_0 == dice_1:
            # Dobles: 4 movimientos del mismo valor
            return (dice_0, dice_0, dice_0, dice_0)
        return (dice_0, dice_1)
    
    @staticmethod
    def _is_double_roll(moves):
        """Verificar si los movimientos corresponden a un doble.
        
        Args:
            moves (tuple): Movimientos disponibles
            
        Returns:
            bool: True si es doble, False si no
        """
        return len(moves) == 4 and len(set(moves)) == 1
    
    def roll(self):
        """Lanzar dados y configurar movimientos disponibles.
        
        Returns:
            tuple: Valores originales de los dados
        """
        # Generar números aleatorios
        self.__last_raw_roll = DiceRoller.roll_two_dice()
        
        # Aplicar reglas de backgammon
        moves = self._process_roll(self.__last_raw_roll)
        
        # Configurar movimientos disponibles
        self.__available_moves = list(moves)
        
        return self.__last_raw_roll
    
    def is_double(self):
        """Verificar si el último lanzamiento fue un doble."""
        return self._is_double_roll(tuple(self.__available_moves))
    
    def get_moves_remaining(self):
        """Obtener cantidad de movimientos restantes."""
        return len(self.__available_moves)
    
    def use_move(self, move):
        """Usar un movimiento si está disponible.
        
        Args:
            move (int): Valor del movimiento a usar
            
        Returns:
            bool: True si se pudo usar, False si no
        """
        if move in self.__available_moves:
            self.__available_moves.remove(move)
            return True
        return False
    
    def clear_roll(self):
        """Limpiar el lanzamiento actual."""
        self.__available_moves = []
        self.__last_raw_roll = None
    
    def get_roll_values(self):
        """Obtener los valores únicos del último lanzamiento."""
        return self.__last_raw_roll
    
    def has_moves_available(self):
        """Verificar si quedan movimientos disponibles."""
        return len(self.__available_moves) > 0
