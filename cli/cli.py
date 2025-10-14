"""Módulo de interfaz de línea de comandos para Backgammon."""
import os
from core.BackgammonGame import BackgammonGame
from core.MoveExecutor import MoveExecutor
from core.ColorFicha import ColorFicha


class CLI:
    """Interfaz de línea de comandos para el juego de Backgammon."""

    def __init__(self):
        """Inicializar CLI."""
        self.__game = None
        self.__move_executor = MoveExecutor()
        self.__running = True

    def limpiar_pantalla(self):
        """Limpiar la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu_principal(self):
        """Mostrar menú principal."""
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("           BACKGAMMON GAME")
        print("="*50)
        print("1. Nueva partida")
        print("2. Reglas del juego")
        print("3. Salir")
        print("="*50)

    def ejecutar_menu_principal(self):
        """Ejecutar lógica del menú principal."""
        self.mostrar_menu_principal()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            self.nueva_partida()
        elif opcion == "2":
            self.mostrar_reglas()
        elif opcion == "3":
            print("\n¡Gracias por jugar! Hasta pronto.")
            self.__running = False
        else:
            print("\nOpción inválida. Presione Enter para continuar...")
            input()

    def mostrar_reglas(self):
        """Mostrar las reglas del juego."""
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("           REGLAS DEL BACKGAMMON")
        print("="*50)
        print("\n1. Cada jugador tiene 15 fichas")
        print("2. El objetivo es mover todas tus fichas al home board")
        print("   y luego sacarlas del tablero")
        print("3. Las fichas blancas se mueven en sentido antihorario (23→0)")
        print("4. Las fichas negras se mueven en sentido horario (0→23)")
        print("5. Debes lanzar los dados en cada turno")
        print("6. Si sacas dobles, juegas ese número 4 veces")
        print("7. Si capturas una ficha rival, va al bar")
        print("8. Gana quien saque todas sus fichas primero")
        print("\n" + "="*50)
        input("\nPresione Enter para volver al menú...")

    def mostrar_menu_partida(self):
        """Mostrar menú durante la partida."""
        self.limpiar_pantalla()
        jugador = self.__game.current_player
        color = "Blancas" if jugador.color == ColorFicha.BLANCA else "Negras"

        print("\n" + "="*50)
        print(f" Turno de: {jugador.nombre} ({color})")
        print("="*50)
        print("1. Ver tablero")
        print("2. Lanzar dados")
        print("3. Mover ficha")
        print("4. Finalizar turno")
        print("5. Rendirse")
        print("6. Volver al menú principal")
        print("="*50)

        # Mostrar dados si están lanzados
        if self.__game.dice.last_raw_roll:
            dados = self.__game.dice.last_raw_roll
            movimientos = self.__game.dice.last_roll
            print(f"\nDados lanzados: {dados[0]}, {dados[1]}")
            print(f"Movimientos disponibles: {movimientos}")
            print("="*50)
