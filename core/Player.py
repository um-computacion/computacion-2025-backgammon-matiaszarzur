"""Modulo que representa un jugador de Backgammon."""
from core.ColorFicha import ColorFicha


class Player:
    """Representa un jugador en el juego de Backgammon."""
    def __init__(self, nombre: str, color: ColorFicha):
        """Inicializar jugador con nombre y color"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del jugador no puede estar vacío")
        if not isinstance(color, ColorFicha):
            raise TypeError("El color debe ser Blanca o Negra")
            
        self.__nombre = nombre.strip()
        self.__color = color

    @property
    def nombre(self) -> str:
        """Obtener el nombre del jugador."""
        return self.__nombre

    @property
    def color(self) -> ColorFicha:
        """Obtener el color del jugador."""
        return self.__color

    def __str__(self) -> str:
        """Representación en string del jugador."""
        return f"Player({self.__nombre}, {self.__color.name})"

    def __eq__(self, other) -> bool:
        """Comparar igualdad entre jugadores."""
        if isinstance(other, Player):
            return self.__nombre == other.nombre and self.__color == other.color
        return False

    def __repr__(self) -> str:
        """Representación para debugging."""
        return f"Player(nombre='{self.__nombre}', color=ColorFicha.{self.__color.name})"
