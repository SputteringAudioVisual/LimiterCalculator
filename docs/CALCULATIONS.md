# Cálculos y supuestos

## Magnitudes eléctricas

Para una potencia `P` sobre una impedancia nominal `Z`:

```text
I_RMS = √(P / Z)
V_RMS = √(P × Z)
```

El amplificador utiliza `√2` como factor de pico. El modelo actual del
transductor utiliza un factor de pico de `2`, heredado del criterio de diseño
del proyecto.

## Conversión entre voltios y dBu

La referencia empleada es `0,7746 V`:

```text
V = 0,7746 × 10^(dBu / 20)
dBu = 20 × log10(V / 0,7746)
```

## Ganancia del amplificador

La ganancia lineal (`Xfactor`) puede obtenerse de cuatro formas:

- sensibilidad expresada en voltios;
- sensibilidad expresada en dBu;
- factor lineal introducido directamente;
- ganancia expresada en dB: `Xfactor = 10^(ganancia_dB / 20)`.

## Umbral RMS

```text
V_RMS_entrada = V_RMS_transductor / Xfactor
umbral_RMS = V_RMS_entrada × (1 - protección / 100)
```

El resultado se convierte después a dBu.

## Umbral de pico

```text
V_pico_entrada = V_pico_transductor / Xfactor
umbral_pico = V_pico_entrada × (1 - protección / 200)
```

El margen de protección aplicado al pico es la mitad del porcentaje aplicado
al umbral RMS, según el comportamiento histórico de la aplicación.

## Tiempos

Con la frecuencia del filtro pasa-altos (`HPF`) en hercios:

```text
ataque_ms = 1000 / HPF
relajación_ms = 15 × ataque_ms
```

## Limitaciones conocidas

- La impedancia se trata como un valor resistivo nominal; no se modela su curva
  compleja respecto a la frecuencia.
- La potencia declarada por el fabricante debe interpretarse según su estándar
  de medida.
- La conversión a dBFS usa actualmente una referencia fija de `+22 dBu`.
- LPF se almacena en la tabla, pero no interviene todavía en los cálculos.
- No se modelan tensión de red, limitación de corriente, factor de cresta del
  programa, compresión térmica ni respuesta dinámica del amplificador.

Estas limitaciones deben considerarse antes de utilizar los valores en un
sistema real.
