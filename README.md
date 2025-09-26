# Backgammon - Matías Zarzur

![CI Status](https://github.com/um-computacion/computacion-2025-backgammon-matiaszarzur/actions/workflows/ci.yml/badge.svg)

![Python](https://img.shields.io/badge/python-3.10-blue)

![Version](https://img.shields.io/badge/version-x.x.x-green) #actualizar version final

![Pylint](https://img.shields.io/badge/pylint-7.15%2F10-yellow)

![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)

## Información del Estudiante
- **Nombre:** Matías Zarzur
- **Ciclo Lectivo:** 2025
- **Carrera:** Ingeniería en Informática

## Descripción del Proyecto
Implementación completa del juego Backgammon desarrollado en Python como proyecto académico. El juego incluye todas las reglas tradicionales del Backgammon con interfaz de línea de comandos, sistema de colores, manejo de dados y validación completa de movimientos.

## Características
(- 🎲 Sistema completo de dados con lógica de dobles)EN PROGRESO 
(- 🎯 Validación completa de movimientos según reglas oficiales)EN PROGRESO 
(- 🎨 Interfaz colorida con sistema de colores personalizado)EN PROGRESO 
(- 👥 Sistema de jugadores con turnos alternados)EN PROGRESO 
(- 🏁 Detección automática de condiciones de victoria)EN PROGRESO 
(- ✅ Tests exhaustivos para todas las funcionalidades)EN PROGRESO 
(-📊 Análisis de cobertura de código superior al 90%)EN PROGRESO
🔍 Análisis estático con Pylint
🤖 CI/CD automatizado con GitHub Actions
📝 Reportes automatizados de calidad de código

## Estructura del Proyecto
```
├── .github/workflows/     # Configuración CI/CD
│   └── ci.yml            # Workflow de integración continua
├── core/                 # Código principal del juego
│   ├── BackgammonGame.py # Lógica principal del juego
│   ├── Board.py          # Manejo del tablero
│   ├── Checker.py        # Lógica de las fichas
│   ├── ColorFicha.py     # Sistema de colores
│   ├── Dice.py           # Sistema de dados
│   └── Player.py         # Lógica de jugadores
├── pygame_ui/            # Interfaz gráfica (Pygame)
│   └── Pygame.py         # Implementación con Pygame
├── test/                 # Tests unitarios completos
│   ├── testBackgammonGame.py
│   ├── testBoard.py
│   ├── testChecker.py
│   ├── testCli.py
│   ├── testDice.py
│   ├── testPlayer.py
│   └── testTipoFicha.py
├── assets/               # Recursos del juego
├── cli/                  # Interfaz de línea de comandos
├── venv/                 # Entorno virtual
├── CHANGELOG.md          # Historial de cambios
├── JUSTIFICACION.md      # Justificación 
├── README.md             # Este archivo
├── REPORTS.md            # Reportes automatizados
├── requirements.txt      # Dependencias Python
└── generate_reports.py   # Generador de reportes
```

## Instalación
```bash
# Clonar el repositorio
git clone https://github.com/um-computacion/computacion-2025-backgammon-matiaszarzur.git

# Navegar al directorio
cd computacion-2025-backgammon-matiaszarzur

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución del Juego
```bash
# Ejecutar el juego principal
xx
# O ejecutar la versión CLI
xx
```

## Ejecución de Tests
```bash
# Ejecutar tests y reporte coverage (Windows)
coverage run -m unittest; coverage report -m; coverage xml 
# Ejecutar tests y reporte coverage (Linux)
coverage run -m unittest && coverage report -m && coverage xml

```

## Reportes de Calidad
Los reportes automatizados se generan en cada push y se encuentran en:
- 📊 **Coverage Report**: `coverage_report.txt`
- 🔍 **Pylint Analysis**: `pylint_report.txt` 
- 📋 **Combined Report**: `REPORTS.md`

**Estado actual:**
- **Pylint Score**: 
- **Coverage**: 

Para ver los reportes más recientes, consulta el archivo `REPORTS.md` que se actualiza automáticamente con cada CI build.

## Estado del Proyecto
Este proyecto forma parte de las actividades académicas del ciclo lectivo 2025 para la carrera de Ingeniería en Informática, de la Universidad de Mendoza

---
*Última actualización: xx-xx-xx*