# FUE-05 - Decisión metodológica de alcance

## Decisión

El estudio selecciona como fuente primaria RAW los movimientos oficiales del TSE para nacimientos, matrimonios y defunciones. Los tres conjuntos quedan **SELECCIONADOS CON LIMITACIÓN**.

La cobertura común publicada verificada es **2026-02-01 a 2026-08-06**. No representa el período histórico de ocurrencia. El alcance inicial es nacional agregado. La frecuencia de publicación y procesamiento es semanal/bajo demanda; la frecuencia analítica mensual es una propuesta condicionada a una capa canónica posterior.

## Evidencia estructural

La estructura de los movimientos está documentada en los DOCX internos de los 93 ZIP: 31 por dataset. Las versiones estables son `NAC-S01`, `MAT-S01` y `DEF-S01`; no se detectó schema drift.

| Dataset | Campos | Longitud | Tipo de Movimiento | Fechas documentadas |
|---|---:|---:|---|---|
| Nacimientos | 26 | 281 | Posición 247; 1 exclusión, 2 cambio, 3 inclusión | Suceso, marginal, naturalización, aplicación; `AAAAMMDD` |
| Matrimonios | 16 | 328 | Posición 1-2; 1 exclusión, 2 cambio, 3 inclusión | Suceso; `AAAAMMDD` |
| Defunciones | 12 | 191 | Posición 2; 1 exclusión, 2 cambio, 3 inclusión | Campo Fecha; `DDMMYYYY` |

La estructura documentada no equivale a calidad semántica completamente validada ni a reconstrucción histórica.

## Calidad y continuidad

- Nacimientos: 47.705 filas, 0 cortas, 0 largas, 0 vacías.
- Matrimonios: 20.546 filas, 0 cortas, 0 largas, 0 vacías.
- Defunciones: 18.719 filas, 0 cortas, 0 largas, 0 vacías.
- 31 bloques por acontecimiento.
- 0 huecos aparentes dentro de los bloques observados.
- Los bloques parciales se conservan tal como fueron publicados.

## Exclusiones y límites

| Elemento | Motivo | Consecuencia |
|---|---|---|
| Periodos anteriores a 2026-02-01 | No verificados en el manifiesto | No se afirma historia anterior |
| Periodos posteriores a 2026-08-06 | Fuera del corte | No se anticipa cobertura futura |
| Archivo maestro | No disponible físicamente ni documentado en formato completo | No se reconstruye el estado registral |
| Cambios y exclusiones | Falta regla institucional completa de aplicación al maestro | DAT-05 continúa pendiente |
| Provincia, cantón y distrito | Dominio territorial no documentado suficientemente | No hay análisis subnacional |
| PII innecesaria | Riesgo de privacidad | No se incorpora al análisis agregado |
| INEC como relleno | No pertenece al RAW TSE | No se completan faltantes |

El proyecto no rellena ausencias con cero, no extrapola, no duplica bloques y registra intervalos sin archivo como `SIN ARCHIVO`.

## Estado

FUE-05 queda **DOCUMENTADA CON LIMITACIONES**. La selección, cobertura, alcance, periodicidad propuesta y regla de no ampliación artificial están justificadas. Siguen pendientes el maestro inicial, la reconstrucción histórica, la definición final de la serie temporal y la validación semántica completa.

## Evidencia

- [matriz_seleccion_fue05.csv](../fuentes/matriz_seleccion_fue05.csv)
- [matriz_seleccion_fue05.md](../fuentes/matriz_seleccion_fue05.md)
- [TSE_schema_audit.md](TSE_schema_audit.md)
- [tse_schema_registry.csv](../../data/manifests/tse_schema_registry.csv)
