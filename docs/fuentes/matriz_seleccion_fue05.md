# Matriz de seleccion FUE-05

## Dictamen resumido

| Acontecimiento | Decision | Cobertura de publicacion verificada | Bloques | Continuidad | Calidad estructural | Calidad semantica |
|---|---|---|---:|---|---|---|
| Nacimientos | SELECCIONADO CON LIMITACION | 2026-02-01 a 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | 47.705 filas validas; 0 cortas, largas o vacias | NO EVALUADA sin diccionario oficial |
| Matrimonios | SELECCIONADO CON LIMITACION | 2026-02-01 a 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | 20.546 filas validas; 0 cortas, largas o vacias | NO EVALUADA sin diccionario oficial |
| Defunciones | SELECCIONADO CON LIMITACION | 2026-02-01 a 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | 18.719 filas validas; 0 cortas, largas o vacias | NO EVALUADA sin diccionario oficial |

La matriz detallada, con la fuente, las longitudes, la frecuencia y las dependencias, esta en `matriz_seleccion_fue05.csv`.

## Criterio aplicado

Los tres acontecimientos se seleccionan porque existe una fuente oficial comun, los tres tienen el mismo intervalo publicado verificable, igual cantidad de bloques, continuidad aparente y calidad estructural completa. Se mantienen juntos para conservar comparabilidad. La seleccion es limitada porque el manifiesto y FUE-04 no permiten interpretar fechas internas, codigos de movimiento, identificadores ni variables territoriales.

No se excluye ningun acontecimiento por su cantidad de filas. Los volumenes diferentes son una propiedad observada de cada acontecimiento y no una razon suficiente para descartar una fuente.

## Alcance temporal y continuidad

- Cobertura publicada individual: 2026-02-01 a 2026-08-06 para cada acontecimiento.
- Interseccion comun: 2026-02-01 a 2026-08-06.
- Cobertura utilizable actualmente: el mismo intervalo, solo como cobertura de publicacion de movimientos y no como fechas de ocurrencia.
- Cada acontecimiento tiene 31 bloques. Hay bloques parciales y un bloque que no sigue estrictamente una semana de siete dias; esto no se corrige ni se rellena.
- No se observan huecos aparentes entre los bloques disponibles. Fuera del intervalo se registra SIN ARCHIVO, no cero acontecimientos.

## Frecuencias separadas

- **Frecuencia de ingesta:** la disponibilidad publicada por el TSE, semanal por bloques de fechas.
- **Frecuencia de procesamiento:** la que determine cada ejecucion del pipeline DAT-02 sobre los archivos disponibles.
- **Frecuencia analitica propuesta:** mensual, de forma condicional y solo despues de construir una capa canonica valida. La propuesta reduce la irregularidad de bloques, facilita la comparacion entre acontecimientos y ofrece una base razonable para estacionalidad y pronostico. FUE-05 no realiza esa agregacion.

## Nivel territorial

El alcance inicial se declara **nacional agregado**, siempre que la futura capa canonica use el total de cada acontecimiento sin interpretar posiciones desconocidas. No se declaran provincia, canton ni distrito. Cualquier analisis subnacional queda pendiente del diccionario oficial, la identificacion verificable de variables territoriales y la estabilidad de sus codigos.

## Evidencia base

- `data/manifests/tse_manifest.csv`
- `docs/fuentes/caracterizacion_acontecimientos.csv`
- `docs/fuentes/perfil_datos_tse.md`
- `docs/evidencias/FUE-04_resumen.md`
- `docs/evidencias/criterios_aceptacion_fue04.md`
- `docs/fuentes/matriz_fuentes_oficiales.md`
- `README.md`

La evidencia es agregada. No contiene lineas RAW ni valores individuales.
