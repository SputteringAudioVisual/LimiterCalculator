# Limiter Calculator

Aplicación de escritorio para calcular los ajustes de limitador RMS y pico de un
sistema de altavoces a partir de las características del amplificador, el
transductor y el procesador.

![Limiter Calculator](GUI/resources/imageFF.png)

## Funciones actuales

- Cálculo de umbrales RMS y pico en dBu.
- Cálculo de tiempos de ataque y relajación a partir del filtro pasa-altos.
- Introducción manual de amplificador y altavoz.
- Base de datos editable en JSON para amplificadores y transductores.
- Modos de operación, impedancias y posiciones de ganancia/MLS dependientes de
  cada amplificador.
- Tabla para guardar y comparar configuraciones durante la sesión.
- Generación de un ejecutable para Windows con PyInstaller.

> [!IMPORTANT]
> Los resultados son una ayuda para configurar un sistema. Deben contrastarse
> con los manuales del fabricante, la topología real del sistema y mediciones
> realizadas por personal cualificado.

## Requisitos

- Windows 10/11
- Python 3.10 o posterior
- PyCharm es opcional; cualquier entorno de Python compatible funciona.

## Instalación

```powershell
git clone https://github.com/SputteringAudioVisual/LimiterCalculator.git
cd LimiterCalculator
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src\main.py
```

En PyCharm, abre la raíz del repositorio y selecciona `.venv` como intérprete.
La configuración de ejecución debe apuntar a `src/main.py` y usar la raíz del
proyecto como directorio de trabajo.

## Uso básico

1. Introduce manualmente los datos o carga un amplificador y un transductor
   desde sus botones correspondientes.
2. Selecciona modo de operación, impedancia y sensibilidad/ganancia.
3. Introduce la frecuencia del filtro pasa-altos y el margen de protección.
4. Revisa los umbrales RMS y pico, ataque y relajación.
5. Usa **Store parameters** para añadir la configuración a la tabla.

La base de datos se encuentra en `dataBase/`. Los formatos admitidos y el modo
de añadir equipos están descritos en [docs/DATABASES.md](docs/DATABASES.md).
Las fórmulas y supuestos se detallan en
[docs/CALCULATIONS.md](docs/CALCULATIONS.md).

## Pruebas

Las pruebas no necesitan PyQt5 porque comprueban de forma aislada los cálculos
y la integridad de los JSON:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Crear el ejecutable

```powershell
python -m pip install -r requirements-build.txt
pyinstaller "Build files/main.spec"
```

El resultado se genera en `dist/`. La carpeta `dataBase/` se copia junto al
ejecutable para que pueda ampliarse sin recompilar.

## Estructura

```text
LimiterCalculator/
├── amplifiers/       Modelo de amplificador
├── Speakers/         Modelo de transductor
├── src/API/          Lógica de cálculo
├── GUI/              Interfaz Qt y recursos
├── dataBase/         Equipos en formato JSON
├── tests/            Pruebas de cálculos y datos
├── docs/             Documentación técnica
└── Build files/      Configuración de PyInstaller
```

## Estado del proyecto

El proyecto ha retomado su desarrollo después de una primera versión
experimental. La prioridad actual es validar los datos de fabricantes,
fortalecer las pruebas y separar progresivamente la lógica de dominio de la
interfaz para facilitar nuevas subaplicaciones.

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) antes de proponer cambios.
