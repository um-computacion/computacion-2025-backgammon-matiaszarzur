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
            
    def ejecutar_menu_partida(self):
        """Ejecutar lógica del menú de partida."""
        if self.__game.is_game_over:
            self.mostrar_ganador()
            return

        self.mostrar_menu_partida()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            self.ver_tablero()
        elif opcion == "2":
            self.lanzar_dados()
        elif opcion == "3":
            self.mover_ficha()
        elif opcion == "4":
            self.finalizar_turno()
        elif opcion == "5":
            self.rendirse()
        elif opcion == "6":
            self.volver_menu_principal()
        else:
            print("\nOpción inválida. Presione Enter para continuar...")
            input()

    def nueva_partida(self):
        """Iniciar nueva partida."""
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("           NUEVA PARTIDA")
        print("="*50)

        nombre1 = input("\nNombre del Jugador 1 (Blancas): ").strip()
        while not nombre1:
            print("El nombre no puede estar vacío.")
            nombre1 = input("Nombre del Jugador 1 (Blancas): ").strip()

        nombre2 = input("Nombre del Jugador 2 (Negras): ").strip()
        while not nombre2:
            print("El nombre no puede estar vacío.")
            nombre2 = input("Nombre del Jugador 2 (Negras): ").strip()

        self.__game = BackgammonGame(nombre1, nombre2)
        self.__game.start_game()

        print(f"\n¡Partida iniciada!")
        print(f"{nombre1} (Blancas) vs {nombre2} (Negras)")
        input("\nPresione Enter para comenzar...")

    def ver_tablero(self):
        """Mostrar el tablero en consola."""
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("           TABLERO DE JUEGO")
        print("="*50)

        board = self.__game.board

        # Mostrar puntos 12-23 (arriba)
        print("\n Puntos 12-23:")
        print(" " + "-"*48)
        for i in range(12, 24):
            fichas = board.obtener_fichas(i)
            if fichas:
                color = "B" if fichas[0].color == ColorFicha.BLANCA else "N"
                print(f" [{i:2d}]: {color}x{len(fichas)}", end="  ")
            else:
                print(f" [{i:2d}]: ---", end="  ")
            if (i - 11) % 6 == 0:
                print()

        print("\n " + "-"*48)

        # Mostrar contenedores
        print(f"\n Bar Blancas: {board.contar_fichas_contenedor(ColorFicha.BLANCA)}")
        print(f" Bar Negras:  {board.contar_fichas_contenedor(ColorFicha.NEGRA)}")

        print("\n " + "-"*48)

        # Mostrar puntos 0-11 (abajo)
        print("\n Puntos 0-11:")
        print(" " + "-"*48)
        for i in range(0, 12):
            fichas = board.obtener_fichas(i)
            if fichas:
                color = "B" if fichas[0].color == ColorFicha.BLANCA else "N"
                print(f" [{i:2d}]: {color}x{len(fichas)}", end="  ")
            else:
                print(f" [{i:2d}]: ---", end="  ")
            if (i + 1) % 6 == 0:
                print()

        print("\n" + "="*50)
        input("\nPresione Enter para continuar...")

    def lanzar_dados(self):
        """Lanzar dados del turno actual."""
        try:
            dados = self.__game.roll_dice()
            print(f"\n¡Dados lanzados! Obtuviste: {dados[0]} y {dados[1]}")

            if self.__game.dice.is_double():
                print(f"¡DOBLES! Puedes mover 4 veces el valor {dados[0]}")

            input("\nPresione Enter para continuar...")
        except RuntimeError as e:
            print(f"\nError: {e}")
            input("\nPresione Enter para continuar...")

    def mover_ficha(self):
        """Mover una ficha."""
        if not self.__game.dice.last_raw_roll:
            print("\n¡Debes lanzar los dados primero!")
            input("\nPresione Enter para continuar...")
            return

        if self.__game.dice.get_moves_remaining() == 0:
            print("\n¡No quedan movimientos disponibles!")
            input("\nPresione Enter para continuar...")
            return

        print("\n" + "="*50)
        print("           MOVER FICHA")
        print("="*50)
        print(f"Movimientos disponibles: {self.__game.dice.last_roll}")

        try:
            from_point = int(input("\nPunto de origen (0-23): ").strip())
            dice_value = int(input("Valor del dado a usar: ").strip())

            self.__move_executor.execute_move(
                self.__game.board,
                self.__game.dice,
                self.__game.current_player,
                from_point,
                dice_value
            )

            print(f"\n¡Ficha movida exitosamente!")
            print(f"Movimientos restantes: {self.__game.dice.get_moves_remaining()}")

        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")

        input("\nPresione Enter para continuar...")

    def finalizar_turno(self):
        """Finalizar el turno actual."""
        if self.__game.dice.has_moves_available():
            confirmar = input("\n¿Seguro que deseas finalizar el turno? "
                            "Aún tienes movimientos (s/n): ").strip().lower()
            if confirmar != 's':
                return

        self.__game.end_turn()
        print(f"\nTurno finalizado. Ahora juega {self.__game.current_player.nombre}")
        input("\nPresione Enter para continuar...")

    def rendirse(self):
        """Rendirse y terminar la partida."""
        confirmar = input("\n¿Estás seguro de que quieres rendirte? (s/n): ").strip().lower()

        if confirmar == 's':
            ganador = self.__game.other_player
            self.__game.set_winner(ganador)
            print(f"\n{self.__game.current_player.nombre} se ha rendido.")
            print(f"¡{ganador.nombre} gana la partida!")
            input("\nPresione Enter para volver al menú principal...")
            self.__game = None

    def volver_menu_principal(self):
        """Volver al menú principal abandonando la partida."""
        confirmar = input("\n¿Seguro que deseas abandonar la partida? (s/n): ").strip().lower()

        if confirmar == 's':
            self.__game = None
            print("\nPartida abandonada.")
            input("\nPresione Enter para continuar...")

    def mostrar_ganador(self):
        """Mostrar al ganador de la partida."""
        self.limpiar_pantalla()
        print("\n" + "="*50)
        print("           ¡PARTIDA TERMINADA!")
        print("="*50)
        print(f"\n🏆 ¡Felicidades {self.__game.winner.nombre}! 🏆")
        print(f"\n¡Has ganado la partida!")
        print("\n" + "="*50)
        input("\nPresione Enter para volver al menú principal...")
        self.__game = None

    def ejecutar(self):
        """Ejecutar el CLI principal."""
        while self.__running:
            if self.__game is None:
                self.ejecutar_menu_principal()
            else:
                self.ejecutar_menu_partida()


# Punto de entrada del programa
if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()
