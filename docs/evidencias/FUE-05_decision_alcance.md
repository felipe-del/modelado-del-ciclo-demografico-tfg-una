# FUE-05 - Decision metodologica de alcance

## Decision

El estudio selecciona como fuente primaria RAW los movimientos oficiales del Tribunal Supremo de Elecciones (TSE) para **nacimientos, matrimonios y defunciones**. Los tres conjuntos quedan **SELECCIONADOS CON LIMITACION**: tienen cobertura publicada comun verificable, continuidad aparente y calidad estructural demostrada, pero aun no cuentan con diccionario oficial de campos, codigos de movimiento ni fechas internas interpretables.

La cobertura comun actual es **2026-02-01 a 2026-08-06**. Esta expresion significa **COBERTURA DE PUBLICACION COMUN VERIFICADA** de archivos de movimientos. No significa periodo historico de ocurrencia de nacimientos, matrimonios o defunciones.

La fuente RAW del alcance es el TSE y no se incorpora INEC. La frecuencia de ingesta sigue la publicacion semanal por bloques del TSE; la frecuencia de procesamiento depende de la ejecucion del pipeline. La frecuencia analitica **propuesta** es mensual, condicionada a una capa canonica posterior y fuera del alcance de FUE-05. El alcance territorial inicial es nacional agregado, sin interpretar campos territoriales desconocidos. Provincia, canton y distrito quedan pendientes.

## Matriz de evidencia

| Acontecimiento | Inicio | Fin | Bloques | Continuidad | Estado |
|---|---|---|---:|---|---|
| Nacimientos | 2026-02-01 | 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | SELECCIONADO CON LIMITACION |
| Matrimonios | 2026-02-01 | 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | SELECCIONADO CON LIMITACION |
| Defunciones | 2026-02-01 | 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | SELECCIONADO CON LIMITACION |

Calidad estructural observada:

- Nacimientos: 47.705 filas, longitud 281, 0 cortas, 0 largas y 0 vacias.
- Matrimonios: 20.546 filas, longitud 328, 0 cortas, 0 largas y 0 vacias.
- Defunciones: 18.719 filas, longitud 191, 0 cortas, 0 largas y 0 vacias.

La calidad semantica permanece **NO EVALUADA**: no se han documentado oficialmente posiciones de campos, fechas internas, codigos de movimiento, identificadores o territorios.

## Justificacion

La cobertura, continuidad y comparabilidad favorecen conservar los tres acontecimientos juntos: comparten fuente institucional, periodo publicado, periodicidad observada y estructura de procesamiento. La cantidad de filas no se usa como criterio de exclusion.

La propuesta mensual es metodologicamente preferible para las futuras series porque permite comparar los tres acontecimientos con una unidad comun, reduce la irregularidad de bloques semanales y deja suficientes observaciones para estudiar estacionalidad y pronosticar. No se ejecuta la agregacion en FUE-05.

## Exclusiones justificadas

| Elemento excluido | Motivo | Impacto | Puede incorporarse despues |
|---|---|---|---|
| Periodos anteriores a 2026-02-01 | No estan verificados en el manifiesto actual | No se declara historia anterior | Si se obtienen fuentes oficiales verificables o un maestro inicial |
| Periodos posteriores a 2026-08-06 | No forman parte del corte documentado | El alcance queda limitado al corte actual | Si se descargan e inspeccionan con el mismo procedimiento |
| Archivos maestros TSE | Son potenciales, pero no estan disponibles ni documentados en formato y cobertura | No se puede reconstruir un estado registral completo | Si existe respuesta institucional y evidencia verificable |
| Provincia, canton y distrito | No hay diccionario ni posiciones territoriales verificables | No se realizan comparaciones subnacionales | Si el TSE documenta variables y codigos estables |
| Campos identificadores sin uso analitico | No son necesarios para el alcance agregado y elevan el riesgo de privacidad | No se publican ni se usan como variables del estudio | Solo con justificacion, minimizacion y autorizacion metodologica |
| INEC como fuente de relleno | No pertenece al pipeline RAW definido y no debe completar faltantes TSE | No se mezclan fuentes ni coberturas | Solo mediante una decision de alcance independiente |

## Regla de no ampliacion artificial

El proyecto no rellena periodos anteriores o posteriores con cero, no extrapola historia, no duplica bloques, no interpreta ausencia de archivo como ausencia de acontecimientos, no usa estadisticas externas para completar RAW faltante y no crea observaciones sinteticas. Un intervalo sin archivo se registra como **SIN ARCHIVO**.

## Estado de las decisiones

### Definitivas

- TSE como fuente primaria RAW.
- Seleccion de nacimientos, matrimonios y defunciones con la limitacion documentada.
- Cobertura comun publicada verificable: 2026-02-01 a 2026-08-06.
- Exclusiones de INEC como relleno y de variables territoriales no verificables.
- Alcance inicial nacional agregado, sin interpretar campos desconocidos.

### Condicionales

- Frecuencia analitica mensual, pendiente de la capa canonica.
- Ampliacion del periodo mediante nuevos archivos TSE verificados.
- Uso de archivos maestros para reconstruccion historica.

### Pendientes

- Diccionario oficial de campos y codigos de movimiento.
- Significado y posicion de fechas internas.
- Variables y codigos territoriales.
- Estado inicial o archivo maestro para afirmar cobertura historica completa.
- Evidencia institucional adicional sobre cobertura y formato de maestros.

## Relacion con el TFG

FUE-05 entrega al Producto 1 el criterio de seleccion, la delimitacion temporal, la frecuencia y el alcance territorial. Para el Producto 2 fija restricciones: no incluir PII innecesaria, no mezclar fuentes y no rellenar faltantes. Para el Producto 3 establece una frecuencia mensual propuesta, pero condicionada a la construccion posterior de una capa canonica valida.

## Evidencia generada

- `docs/fuentes/matriz_seleccion_fue05.csv`
- `docs/fuentes/matriz_seleccion_fue05.md`
- `docs/evidencias/criterios_aceptacion_fue05.md`
- `data/manifests/tse_manifest.csv`
- `docs/fuentes/caracterizacion_acontecimientos.csv`
- `docs/evidencias/FUE-04_resumen.md`

No se modifican ni se incluyen registros RAW.
