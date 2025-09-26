"""Tests para la clase Board."""

import unittest
from core.Board import Board
from core.Checker import Checker
from core.ColorFicha import ColorFicha

class TestBoard(unittest.TestCase):

    def setUp(self):
        """Configurar objetos antes de cada prueba."""
        self.tablero = Board()
        self.ficha_blanca = Checker(ColorFicha.BLANCA)
        self.ficha_negra = Checker(ColorFicha.NEGRA)

    def test_crear_tablero_vacio(self):
        self.assertEqual(len(self.tablero.puntos), 24)
        self.assertTrue(self.tablero.tablero_esta_vacio())

    def test_agregar_ficha_punto(self):
        self.tablero.agregar_ficha(0, self.ficha_blanca)
        self.assertEqual(self.tablero.contar_fichas(0), 1)
        self.assertFalse(self.tablero.tablero_esta_vacio())

    def test_obtener_fichas_punto(self):
        self.tablero.agregar_ficha(5, self.ficha_blanca)
        fichas = self.tablero.obtener_fichas(5)
        self.assertEqual(len(fichas), 1)
        self.assertEqual(fichas[0].color, ColorFicha.BLANCA)

    def test_contar_fichas_punto_vacio(self):
        self.assertEqual(self.tablero.contar_fichas(10), 0)

    def test_punto_esta_vacio(self):
        self.assertTrue(self.tablero.punto_esta_vacio(0))
        self.tablero.agregar_ficha(0, self.ficha_blanca)
        self.assertFalse(self.tablero.punto_esta_vacio(0))

    def test_quitar_ficha(self):
        self.tablero.agregar_ficha(3, self.ficha_negra)
        ficha_quitada = self.tablero.quitar_ficha(3)
        self.assertEqual(ficha_quitada.color, ColorFicha.NEGRA)
        self.assertEqual(self.tablero.contar_fichas(3), 0)

    def test_obtener_color_punto(self):
        self.tablero.agregar_ficha(7, self.ficha_blanca)
        color = self.tablero.obtener_color_punto(7)
        self.assertEqual(color, ColorFicha.BLANCA)

    def test_obtener_color_punto_vacio(self):
        self.assertIsNone(self.tablero.obtener_color_punto(5))

    def test_agregar_ficha_contenedor(self):
        self.tablero.agregar_ficha_contenedor(self.ficha_blanca)
        self.assertEqual(self.tablero.contar_fichas_contenedor(ColorFicha.BLANCA), 1)
        self.assertFalse(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))

    def test_quitar_ficha_contenedor(self):
        self.tablero.agregar_ficha_contenedor(self.ficha_negra)
        ficha_quitada = self.tablero.quitar_ficha_contenedor(ColorFicha.NEGRA)
        self.assertEqual(ficha_quitada.color, ColorFicha.NEGRA)
        self.assertEqual(self.tablero.contar_fichas_contenedor(ColorFicha.NEGRA), 0)

    def test_quitar_ficha_contenedor_vacio(self):
        result = self.tablero.quitar_ficha_contenedor(ColorFicha.NEGRA)
        self.assertIsNone(result)

    def test_contenedor_esta_vacio(self):
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))

    # Tests para casos de puntos fuera de rango
    def test_obtener_fichas_punto_invalido(self):
        self.assertEqual(self.tablero.obtener_fichas(30), [])
        self.assertEqual(self.tablero.obtener_fichas(-5), [])

    def test_contar_fichas_punto_invalido(self):
        self.assertEqual(self.tablero.contar_fichas(-5), 0)
        self.assertEqual(self.tablero.contar_fichas(25), 0)

    def test_quitar_ficha_punto_invalido(self):
        self.assertIsNone(self.tablero.quitar_ficha(-1))
        self.assertIsNone(self.tablero.quitar_ficha(24))
        self.assertIsNone(self.tablero.quitar_ficha(50))

    def test_punto_esta_vacio_invalido(self):
        self.assertTrue(self.tablero.punto_esta_vacio(99))
        self.assertTrue(self.tablero.punto_esta_vacio(-1))

    def test_agregar_ficha_punto_invalido(self):
        ficha = Checker(ColorFicha.BLANCA)
        self.tablero.agregar_ficha(-1, ficha)
        self.tablero.agregar_ficha(24, ficha)
        self.assertTrue(self.tablero.tablero_esta_vacio())

    def test_setter_puntos_valido(self):
        nuevos_puntos = [[] for _ in range(24)]
        nuevos_puntos[0].append(self.ficha_blanca)
        self.tablero.puntos = nuevos_puntos
        self.assertEqual(len(self.tablero.puntos), 24)
        self.assertEqual(self.tablero.puntos[0][0].color, ColorFicha.BLANCA)
        self.assertEqual(len(self.tablero.puntos[0]), 1)
    
    def test_setter_puntos_lista_invalida_longitud(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.puntos = [[] for _ in range(23)]
        self.assertEqual(str(context.exception), "Los nuevos puntos deben ser una lista de 24 elementos.")
        
    def test_setter_puntos_no_es_lista(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.puntos = "no es una lista"
        self.assertEqual(str(context.exception), "Los nuevos puntos deben ser una lista de 24 elementos.")
        
    def test_setter_contenedor_blancas_valido(self):
        nuevo_contenedor = [self.ficha_blanca]
        self.tablero.contenedor_blancas = nuevo_contenedor
        self.assertEqual(self.tablero.contenedor_blancas, nuevo_contenedor)
    
    def test_setter_contenedor_negras_valido(self):
        nuevas_fichas = [self.ficha_negra]
        self.tablero.contenedor_negras = nuevas_fichas
        self.assertEqual(len(self.tablero.contenedor_negras), 1)
        self.assertEqual(self.tablero.contenedor_negras[0].color, ColorFicha.NEGRA)
        
        
    def test_resetear_tablero(self):
        self.tablero.agregar_ficha(0, self.ficha_blanca)
        self.tablero.agregar_ficha(5, self.ficha_negra)
        self.tablero.agregar_ficha_contenedor(self.ficha_blanca)
        self.tablero.agregar_ficha_contenedor(self.ficha_negra)
        #verifica que hayan fichas
        self.assertFalse(self.tablero.tablero_esta_vacio())
        self.assertFalse(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))
        self.assertFalse(self.tablero.contenedor_esta_vacio(ColorFicha.NEGRA))
        #resetea
        self.tablero.resetear_tablero()
        self.assertTrue(self.tablero.tablero_esta_vacio())
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.NEGRA))

    def test_limpiar_contenedores(self):
        self.tablero.agregar_ficha_contenedor(self.ficha_blanca)
        self.tablero.agregar_ficha_contenedor(self.ficha_negra)
        self.tablero.agregar_ficha_contenedor(Checker(ColorFicha.BLANCA))
        
        self.assertFalse(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))
        self.assertFalse(self.tablero.contenedor_esta_vacio(ColorFicha.NEGRA))
        self.tablero.limpiar_contenedores()
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.BLANCA))
        self.assertTrue(self.tablero.contenedor_esta_vacio(ColorFicha.NEGRA))
    #Tests adicionales para coverage
    def test_contar_fichas_contenedor_color_invalido(self):
        self.assertEqual(self.tablero.contar_fichas_contenedor("no es un color"), 0)
        self.assertEqual(self.tablero.contar_fichas_contenedor(None), 0)
        
    def test_quitar_ficha_contenedor_vacio_ambos_colores(self):
        self.assertIsNone(self.tablero.quitar_ficha_contenedor(ColorFicha.BLANCA))
        self.assertIsNone(self.tablero.quitar_ficha_contenedor(ColorFicha.NEGRA))
        
    def test_obtener_color_punto_despues_de_quitar_ficha(self):
        self.tablero.agregar_ficha(10, self.ficha_blanca)
        color = self.tablero.obtener_color_punto(10)
        self.assertEqual(color, ColorFicha.BLANCA)
        
        self.tablero.quitar_ficha(10)
        color_despues = self.tablero.obtener_color_punto(10)
        self.assertIsNone(color_despues)
    
    def test_setter_puntos_tipo_incorrecto(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.puntos = "esto no es una lista"
        self.assertEqual(str(context.exception), "Los nuevos puntos deben ser una lista de 24 elementos.")
    
    def test_setter_contenedor_blancas_tipo_incorrecto(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.contenedor_blancas = "esto no es una lista"
        self.assertEqual(str(context.exception), "El nuevo contenedor debe ser una lista.")
        
    def test_setter_contenedor_negras_tipo_incorrecto(self):
        with self.assertRaises(ValueError) as context:
            self.tablero.contenedor_negras = 12345
        self.assertEqual(str(context.exception), "El nuevo contenedor debe ser una lista.")