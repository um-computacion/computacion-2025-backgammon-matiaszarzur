"""Tests para la clase BoardInitializer."""

import unittest
from core.Board import Board
from core.BoardInitializer import BoardInitializer
from core.Checker import Checker
from core.ColorFicha import ColorFicha


class TestBoardInitializer(unittest.TestCase):

    def setUp(self):
        """Configurar objetos antes de cada prueba."""
        self.tablero = Board()

    def test_inicializar_estandar_correcta_config(self):
        """Verificar que inicializa con la configuración correcta."""
        BoardInitializer.inicializar_estandar(self.tablero)

        # Fichas negras
        self.assertEqual(self.tablero.contar_fichas(0), 2)
        self.assertEqual(self.tablero.contar_fichas(11), 5)
        self.assertEqual(self.tablero.contar_fichas(16), 3)
        self.assertEqual(self.tablero.contar_fichas(18), 5)
        
        # Fichas blancas
        self.assertEqual(self.tablero.contar_fichas(23), 2)
        self.assertEqual(self.tablero.contar_fichas(12), 5)
        self.assertEqual(self.tablero.contar_fichas(7), 3)
        self.assertEqual(self.tablero.contar_fichas(5), 5)

        # Verificar colores
        for punto in [0, 11, 16, 18]:
            for ficha in self.tablero.obtener_fichas(punto):
                self.assertEqual(ficha.color, ColorFicha.NEGRA)
        
        for punto in [23, 12, 7, 5]:
            for ficha in self.tablero.obtener_fichas(punto):
                self.assertEqual(ficha.color, ColorFicha.BLANCA)

    def test_inicializar_estandar_colores_correctos(self):
        """Verificar que los colores de las fichas son correctos."""
        BoardInitializer.inicializar_estandar(self.tablero)
        
        # Verificar las fichas blancas
        self.assertEqual(self.tablero.contar_fichas(23), 2)
        self.assertEqual(self.tablero.contar_fichas(12), 5)
        self.assertEqual(self.tablero.contar_fichas(7), 3)
        self.assertEqual(self.tablero.contar_fichas(5), 5)
        
        for punto in [23, 12, 7, 5]:
            for ficha in self.tablero.obtener_fichas(punto):
                self.assertEqual(ficha.color, ColorFicha.BLANCA)
        
        # Verificar las fichas negras
        self.assertEqual(self.tablero.contar_fichas(0), 2)
        self.assertEqual(self.tablero.contar_fichas(11), 5)
        self.assertEqual(self.tablero.contar_fichas(16), 3)
        self.assertEqual(self.tablero.contar_fichas(18), 5)
        
        for punto in [0, 11, 16, 18]:
            for ficha in self.tablero.obtener_fichas(punto):
                self.assertEqual(ficha.color, ColorFicha.NEGRA)

    def test_inicializar_estandar_total_fichas(self):
        """Verificar que se inicializan 15 fichas de cada color."""
        BoardInitializer.inicializar_estandar(self.tablero)
        
        total_fichas_blancas = sum(
            self.tablero.contar_fichas(punto) for punto in range(24) 
            if self.tablero.obtener_color_punto(punto) == ColorFicha.BLANCA
        )
        total_fichas_negras = sum(
            self.tablero.contar_fichas(punto) for punto in range(24) 
            if self.tablero.obtener_color_punto(punto) == ColorFicha.NEGRA
        )
        
        self.assertEqual(total_fichas_blancas, 15)
        self.assertEqual(total_fichas_negras, 15)

    def test_inicializar_estandar_puntos_vacios(self):
        """Verificar que solo los puntos correctos tienen fichas."""
        BoardInitializer.inicializar_estandar(self.tablero)
        
        puntos_ocupados = {0, 5, 7, 11, 12, 16, 18, 23}
        for punto in range(24):
            if punto not in puntos_ocupados:
                self.assertTrue(self.tablero.punto_esta_vacio(punto))

    def test_inicializar_estandar_contenedores_vacios(self):
        """Verificar que los contenedores están vacíos después de inicializar."""
        BoardInitializer.inicializar_estandar(self.tablero)
        
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.NEGRA))

    def test_inicializar_estandar_limpia_estado_anterior(self):
        """Verificar que inicializar limpia el estado anterior del tablero."""
        # Agregar fichas y contenedores antes de inicializar
        ficha_blanca = Checker(ColorFicha.BLANCA)
        ficha_negra = Checker(ColorFicha.NEGRA)
        
        self.tablero.agregar_ficha(0, ficha_blanca)
        self.tablero.agregar_ficha(5, ficha_negra)
        self.tablero.agregar_ficha_contenedor(ficha_blanca)
        self.tablero.agregar_ficha_contenedor(ficha_negra)
        
        # Inicializar tablero
        BoardInitializer.inicializar_estandar(self.tablero)
        
        # Verificar que se haya limpiado y configurado correctamente
        self.assertEqual(self.tablero.contar_fichas(0), 2)  # Config estándar
        self.assertEqual(self.tablero.contar_fichas(5), 5)  # Config estándar
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.NEGRA))

    def test_inicializar_estandar_multiples_llamadas(self):
        """Verificar que múltiples inicializaciones producen el mismo resultado."""
        BoardInitializer.inicializar_estandar(self.tablero)
        
        total_fichas_blancas_1 = sum(
            self.tablero.contar_fichas(punto) for punto in range(24) 
            if self.tablero.obtener_color_punto(punto) == ColorFicha.BLANCA
        )
        total_fichas_negras_1 = sum(
            self.tablero.contar_fichas(punto) for punto in range(24) 
            if self.tablero.obtener_color_punto(punto) == ColorFicha.NEGRA
        )
        
        self.assertEqual(total_fichas_blancas_1, 15)
        self.assertEqual(total_fichas_negras_1, 15)
        
        # Segunda inicialización
        BoardInitializer.inicializar_estandar(self.tablero)
        
        total_fichas_blancas_2 = sum(
            self.tablero.contar_fichas(punto) for punto in range(24) 
            if self.tablero.obtener_color_punto(punto) == ColorFicha.BLANCA
        )
        total_fichas_negras_2 = sum(
            self.tablero.contar_fichas(punto) for punto in range(24) 
            if self.tablero.obtener_color_punto(punto) == ColorFicha.NEGRA
        )
        
        self.assertEqual(total_fichas_blancas_2, 15)
        self.assertEqual(total_fichas_negras_2, 15)
        self.assertEqual(total_fichas_blancas_1, total_fichas_blancas_2)
        self.assertEqual(total_fichas_negras_1, total_fichas_negras_2)


if __name__ == '__main__':
    unittest.main()