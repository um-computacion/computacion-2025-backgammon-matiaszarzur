## [23-08-2025] V 0.0.0
# Agregado:
Carpetas para las clases
Archivos de test para cada clase
# Cambiado o eliminado:
Se cambio los archivos creados anteriormente a las carpetas de sus respectivas clases para que queden junto a sus archivos de test
cambio en el nombre del archivo de cli: main.py --> cli.py

## [24-08-2025] V 0.0.1
# Agregado:
Archivos y lineas de comandos necesarias para la implementacion de CircleCi

## [25-08-2025] V 0.0.2
# Cambiado: 
Se arreglo la localizacion de los archivos test, se movieron a la carpeta test.
Se añadio la clase color_ficha utilizando enums (enumeraciones), que son un conjunto fijo y definido de constantes con nombres, en este caso se utilizan para el color de la ficha en la clase checker. 

## [25-08-2025] V 0.0.3
Se agrego el archivo .coveragerc y se configuro de acuerdo al proyecto.

## [30-08-2025] V 0.0.4
Se corrigieron los nombres de las clases. Se continuo trabajando sobre la clase Board, se agregaron metodos, verificaciones y setters. Ademas se añadieron test para una mayor covertura de codigo (tambien debido a la creacion de nuevos metodos se añadieron tests).
Se deja el coverage en un 92% comparado al 89% que se tenian antes de los arreglos.

## [30-08-2025] V 0.0.5
Se agrega la clase dice segun lo visto en clase, ademas se agregan algunos metodos para una mejor funcionalidad.
Se crean test para la clase dice.
Se corrigio la clase para utilizar getters y setter, ademas tambien se corrigio la encapsulacion. Tambien se cambio la logica de dobles porque era un poco confusa.

## [11-09-2025] V 0.0.6
Se comenzo con la clase BackGammon Game.Se agregaron atributos principales:board, dice, jugador_actual,estado_juego, ganador, barras de fichas capturadas y tiradas iniciales. Se implementaron getters y setter con validaciones para cada atributo.Se definieron los métodos principales del flujo de juego como placeholders (configuración, tiradas, movimientos, validaciones, cambio de turno, verificación de ganador, etc)
Estructura preparada para avanzar con la lógica del juego en versiones futuras.

## [14-09-2025] V 0.0.7
Se corrige la clase board con un metodo adicional, tambien se agregan test necesarios para una mayor cobertura del codigo. Se elimina lo realizado en la clase Backgammon game porque se retomara despues de haber corregido algunas clases y haber añadido la clase player.
## [14-09-2025] V 0.0.8
Se elimina la carpeta CircleCI debido a que no se trabajara segun lo visto en la clase virtual. 
Se agregan las librerias necesarias
Se añaden los archivos y configuraciones necesarias para su funcionamiento

## [15-09-2025] V 0.0.9
Se cambia el codigo dentro de /.github/workflows/ci.yml para una mejora en el aspecto de los tests, analisis de los directorios, mejor debugging y demas.
## [15-09-2025] V 0.1.0
Se agregan budgets en el README.md para que se muestre la informacion tipica del proyecto.
Se corrigio varias veces el ci.yml para que actulice automaticamente los budges del README

## [16-09-2025] V 0.1.1
Se corrigen y se pulen algunos puntos flojos del codigo para mejorar su valoracion, intentando que no afecte al coverage ni a la logica.
Se agregaron los docstrings solicitados por el ci.yml

## [26-09-2025] V 0.1.2
Se corrige la clase Board con los principios SOLID vistos en clase. Se creo una nueva clase "BoardInitilizer".
    -Responsabilidad única: Solo maneja la estructura y operaciones del tablero (Board)
    -Se eliminó inicializar_tablero() que era responsabilidad de configuración (Ahora en BoardInitilizer)
Se crearon los tests para la nueva clase y se eliminaron los de la clase board que no se usan.
## [28-09-2025] V 0.1.3
Se corrige la clase Dice con los principios SOLID vistos en clase. Se creó una nueva clase "DiceRoller".
    - Responsabilidad única: Solo maneja dados y movimientos de backgammon (Dice)
    - Se separó la generación aleatoria en DiceRoller que es responsabilidad de generar números
    - Se eliminó el setter público de last_roll mejorando el encapsulamiento
    - Se extrajeron las reglas como métodos estáticos dentro de Dice (_process_roll, _is_double_roll)
    - Se agregó last_raw_roll para mantener los valores originales del lanzamiento
Se crearon los tests para la nueva estructura y se actualizaron todos los mocks para usar DiceRoller.
Se crearon los test para la clase DiceRoller.
## [05-10-2025] V 0.1.4
Se crea la clase Backgammon con sus respectivos metodos.
## [06-10-2025] V 0.1.5
Se crean los test necesarios para la clase Backgammon.
## [11-10-2025] V 0.1.6
Se implementa la clase MoveExecutor aplicando principios SOLID.
    - Responsabilidad única: Ejecutar movimientos de fichas en el tablero
    - Separación de coordinación: Extrae lógica de movimientos de BackgammonGame
## [13-10-2025] V 0.1.7
Se implemento la estructura basica del CLI con menus.

-iniciazion del CLI 
-menu principal
-menu de partida
-Reglas del juego
-Limpieza de pantalla

Tambien se agragaron algunos test para el CLI.
## [14-10-2025] V 0.1.8
Se implemento la estructura faltante del CLI.
    - Nueva partida con validacion de nombres
    - Visualizacion del tablero en consola
    - Lanzar dados con deteccion de dobles
    - Mover fichas usando MoveExecutor
    - Finalizar turno y cambiar jugador
    - Rendirse y declarar ganador
    - Mostrar ganador con emoji (con ayuda de IA, prompt de ayer)

se crearon los test y se modificaron algunos de Cli.
Se modificaron algunas clases para mejorar la valoracion del codigo.
## [20-10-2025] V 0.1.9
Se realizaron cambios en el requirements.txt para la instalacion de Pygame. V 2.6.1
## [23-10-2025] V 0.2.0
Se implemento la estructura del tableroUI, luego se implementaron las funciones necesarias para el funcionamiento.
- Crea clase TableroUI aplicando principio de responsabilidad unica
- Renderiza tablero completo: marco, barra, 24 triangulos, fichas
## [25-10-2025] V 0.2.1
Se implementaron las siguientes funciones en el pygame:
- Agrega numeracion de puntos (1-24) para mejor usabilidad
- Implementa deteccion de clicks en triangulos
- Agrega sistema de resaltado visual de puntos seleccionados
## [27-10-2025] V 0.2.2
Se refactorizaron los archivos de pygame_ui para cumplir con los principios SOLID
Se implementaron las siguientes funciones en el pygame:
- Crea TableroRenderer: responsable solo del renderizado del tablero
- Crea DadosRenderer: responsable solo del renderizado de dados
- pygame_ui.py ahora coordina y delega responsabilidades
- Reduce acoplamiento entre componentes
- Agrega funcionalidad de lanzar dados con tecla ESPACIO
## [28-10-2025] V 0.2.3
Agrego panel de informacion del turno en Pygame.
Se implementaron las siguientes funciones en el pygame:
    - Clase InfoPanel para mostrar estado del juego
    - Muestra jugador actual, color y movimientos disponibles
    - Instrucciones de controles en pantalla
    - Panel lateral derecho integrado al tablero
Correcciones de bugs:
    - Bug de cambio de turno: Corregido usando last_raw_roll en lugar de last_roll
    - Bug de verificación de fichas: Actualizado para comprobar el color de todas las fichas del punto
    - Bug de capturas: Implementada lógica completa para capturar fichas enemigas (blots) y envío a la barra

Mejoras implementadas:
    - Visualización de la barra central con fichas capturadas
    - Contador de fichas apiladas cuando hay más de 5 en un punto
    - Pantalla inicial para ingresar nombres de jugadores (PantallaInicio)
    - Sistema de mensajes en pantalla con colores según tipo (error/info/estado)
    - Renderizado mejorado del tablero con soporte para barra

  ## [28-10-2025] V 0.2.4

  Se modificaron los test del CLI con lo visto en la clase del 28/10

  Se corrigieron ciertos aspectos para el correcto funcionamiento del programa:
  CORE (BackgammonGame.py):
- puede_hacer_bear_off() para validar reglas
- bear_off_ficha() con detección automática de victoria
- tiene_fichas_en_barra() para validaciones
- contadores fichas_fuera_blancas y fichas_fuera_negras

INTERFAZ (pygame_ui/):
- input_handler.py para usar métodos del CORE
- tablero_renderer.py para consultar datos del CORE
- pygame_ui.py para verificar victoria desde el CORE
- pantalla_victoria.py para fin de juego
- Correccion re-entry
- Correccion superposición de triángulos con barra y bear off