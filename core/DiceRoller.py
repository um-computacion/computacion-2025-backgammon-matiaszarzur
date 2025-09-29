"""Módulo para generar números aleatorios de dados."""
import random


class DiceRoller:
    """Responsable únicamente de generar números aleatorios de dados."""
    
    @staticmethod
    def roll_two_dice():
        """Lanza dos dados de 6 caras.
        
        Returns:
            tuple: Tupla con los valores de los dos dados (1-6)
        """
        return (random.randint(1, 6), random.randint(1, 6))