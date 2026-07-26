# Base de datos de equipos

Los datos están separados en:

- `dataBase/amplifierDataBase/`
- `dataBase/driverDataBase/`

Cada equipo ocupa un archivo JSON. Los nombres deben ser descriptivos y evitar
espacios cuando sea práctico.

## Transductores

Formato mínimo:

```json
{
  "Brand": "Fabricante",
  "Model": "Modelo",
  "Impedance": 8,
  "Power": 500
}
```

`Impedance` se expresa en ohmios y `Power` en vatios.

## Amplificadores

Un amplificador contiene metadatos, uno o más modos de operación y las opciones
de sensibilidad:

```json
{
  "Brand": "Fabricante",
  "Model": "Modelo",
  "Stereo": {
    "Impedance": [2, 4, 8],
    "Power": [2000, 1400, 800],
    "OutConections": ["1+ / 1-", "2+ / 2-"]
  },
  "Sensitivity": [
    {
      "label": "32 dB",
      "unit": "DB",
      "value": 32
    }
  ]
}
```

Las posiciones de `Impedance` y `Power` se corresponden por índice. Todos los
modos deben contener ambas listas con la misma longitud.

Unidades admitidas en `Sensitivity`:

- `V sens`: sensibilidad en voltios;
- `dBu sens`: sensibilidad en dBu;
- `X Factor`: ganancia lineal;
- `DB`: ganancia en decibelios.

La aplicación conserva compatibilidad con el formato antiguo de sensibilidad
basado en un objeto, pero los nuevos datos deben usar la lista mostrada arriba.

## Criterios para incorporar datos

1. Utiliza el manual o ficha técnica oficial del fabricante.
2. Conserva las unidades originales y convierte únicamente los campos exigidos
   por el esquema.
3. No inventes valores ausentes. Documenta cualquier estimación en el commit.
4. Comprueba el JSON y ejecuta las pruebas antes de enviarlo.
5. Indica en la PR la fuente y la página utilizada.

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```
