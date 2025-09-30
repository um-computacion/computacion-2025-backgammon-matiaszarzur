"""Clase Player"""
from core.ColorFicha import ColorFicha

class Player:
    """Clase que representa a un jugador en el backgammon."""
    def __init__ (self, name: str, color: ColorFicha):
        #verificar que nombre no este vacio
        """Inicializar jugador con nombre y color de ficha."""
        self.__name = name
        self.__color = color
        
    #property para name
    #property para color
    #representacion en string
    #comparacion de igualdad
    #metodo str