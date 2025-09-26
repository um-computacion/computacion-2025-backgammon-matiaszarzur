"""Clase que representa la ficha del Backgammon.Contiene la clase Checker que representa una ficha
del juego de backgammon con su color correspondiente."""
from core.ColorFicha import ColorFicha

class Checker:
    """Clase que representa una ficha del backgammon."""
    def __init__(self, color: ColorFicha):
        """Inicializar ficha con su color."""
        self.__color = color

    @property
    def color(self):
        """Obtener el color de la ficha."""
        return self.__color

    def __str__(self):
        """Representación en string de la ficha."""
        return f"Checker({self.__color.name})"

    def __eq__(self, other):
        """Comparar igualdad entre fichas."""
        if isinstance(other, Checker):
            return self.__color == other.color  # Usar property en lugar de atributo privado
        return False
