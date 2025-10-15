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