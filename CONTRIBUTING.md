# Contribuir

## Preparación

1. Crea una rama desde `main`.
2. Configura un entorno virtual.
3. Instala `requirements.txt`.
4. Mantén fuera del repositorio `.venv/`, `.idea/`, `build/`, `dist/` y
   `__pycache__/`.

## Cambios de código

- Separa los cambios funcionales de las incorporaciones masivas de datos.
- Añade o actualiza pruebas cuando cambies una fórmula.
- Evita introducir dependencias en la lógica de cálculo que obliguen a cargar
  la interfaz gráfica durante las pruebas.
- Usa UTF-8 y finales de línea LF.

## Datos de fabricantes

Sigue el esquema de [docs/DATABASES.md](docs/DATABASES.md). En el mensaje del
commit o la PR, incluye fabricante, modelo, documento de referencia y página.

## Antes de abrir una PR

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Describe qué cambia, por qué, cómo se ha verificado y qué limitaciones quedan.
