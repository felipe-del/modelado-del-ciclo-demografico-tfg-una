# Producto 1 - Informe de análisis de fuentes de datos demográficos

## 1. Propósito

Este producto responde al Objetivo Específico 1 del TFG: investigar y caracterizar fuentes oficiales para el análisis del ciclo demográfico mediante registros de nacimientos, matrimonios y defunciones.

El resultado es un informe documental y técnico. No contiene valores individuales TXT, no transforma RAW y no afirma reconstrucción histórica.

## 2. Alcance y procedencia

La fuente primaria del alcance es el Tribunal Supremo de Elecciones (TSE), mediante su página oficial de descarga de movimientos: <https://www.tse.go.cr/descarga_movimientos.html>. El INEC se conserva únicamente como referencia contextual; no forma parte del RAW ni se usa para rellenar faltantes.

Se evaluaron movimientos de nacimientos, matrimonios y defunciones. Los archivos maestros TSE se consideran fuentes potenciales, pero no están disponibles físicamente ni documentados en formato completo dentro del repositorio.

## 3. Metodología y trazabilidad

La caracterización combina:

1. Inventario institucional de fuentes y mecanismos de acceso.
2. Inspección agregada de `tse_manifest.csv`.
3. Inspección directa de los 93 ZIP RAW.
4. Lectura de cada DOCX desde `word/document.xml`.
5. Cálculo de hashes ZIP, TXT y DOCX.
6. Normalización de tablas de campos y cálculo de posiciones 1-based.
7. Comparación de firmas estructurales entre períodos.
8. Evaluación separada de estructura, privacidad, cobertura y limitaciones metodológicas.

Los artefactos de trazabilidad son [TSE_schema_audit.md](../evidencias/TSE_schema_audit.md), [tse_schema_registry.csv](../../data/manifests/tse_schema_registry.csv), los tres diccionarios TSE y [tse_manifest.csv](../../data/manifests/tse_manifest.csv).

## 4. Metodología e implementación técnica

El flujo reproducible utilizado para analizar las fuentes fue:

```text
TSE
	-> ZIP RAW
	-> inventario de archivos
	-> SHA-256 de ZIP, TXT y DOCX
	-> TXT + DOCX asociados
	-> word/document.xml
	-> diccionario de campos
	-> posiciones fixed-width 1-based
	-> validación de suma y longitud
	-> schema fingerprint
	-> comparación de schema drift
	-> caracterización agregada
	-> selección y alcance metodológico
```

La inspección de los DOCX se realizó leyendo Office Open XML, específicamente `word/document.xml`, dentro de cada ZIP. Las tablas se normalizaron conservando el orden de campos, longitudes, tipos, formatos y observaciones documentadas. Las posiciones se calcularon acumulando longitudes desde la posición 1; la suma se contrastó contra la longitud observada del TXT asociado.

La firma estructural se calculó a partir de campo, longitud, tipo y observaciones/catálogos normalizados. Los hashes SHA-256 se conservaron para la identidad de cada ZIP, TXT y DOCX; el registro por período está en `tse_schema_registry.csv`.

Tecnologías realmente utilizadas: Python y biblioteca estándar, ZIP, Office Open XML, SHA-256, JSON, CSV, Markdown, pytest y Git/GitHub. No se utilizaron valores individuales del TXT en las evidencias ni en las conclusiones del Producto 1.

## 5. Inventario y cobertura

Se inspeccionaron 93 ZIP: 31 por acontecimiento. Cada ZIP contiene un TXT de movimientos y un DOCX de definición de campos. La cobertura común publicada verificada es 2026-02-01 a 2026-08-06, en bloques de fechas. Esto no equivale al período de ocurrencia de los acontecimientos.

| Dataset | ZIP | TXT | DOCX | Filas | Longitud |
|---|---:|---|---:|---:|---:|
| Nacimientos | 31 | MOVWEBNAC.txt | 31 | 47.705 | 281 |
| Matrimonios | 31 | MOVWEBMAT.txt | 31 | 20.546 | 328 |
| Defunciones | 31 | MOVWEBDEF.txt | 31 | 18.719 | 191 |

## 6. Estructura documentada

| Dataset | Versión | Campos | Longitud | Tipo de Movimiento | Fechas |
|---|---|---:|---:|---|---|
| Nacimientos | NAC-S01 | 26 | 281 | Posición 247, longitud 1; 1 exclusión, 2 cambio, 3 inclusión | Suceso, marginal, naturalización y aplicación; AAAAMMDD |
| Matrimonios | MAT-S01 | 16 | 328 | Posición 1-2, longitud 2; 1 exclusión, 2 cambio, 3 inclusión | Suceso; AAAAMMDD |
| Defunciones | DEF-S01 | 12 | 191 | Posición 2, longitud 1; 1 exclusión, 2 cambio, 3 inclusión | Campo Fecha; DDMMYYYY |

Las tablas completas y posiciones están en [diccionario_nacimientos.md](../fuentes/diccionario_nacimientos.md), [diccionario_matrimonios.md](../fuentes/diccionario_matrimonios.md) y [diccionario_defunciones.md](../fuentes/diccionario_defunciones.md).

Las sumas documentadas coinciden con las longitudes observadas: 281, 328 y 191, diferencia cero en los tres datasets.

## 7. Schema drift

Cada dataset tiene una firma estructural única y estable en sus 31 ZIP. Los hashes DOCX cambian entre archivos, pero las tablas normalizadas son equivalentes. No se detectaron campos agregados o eliminados, cambios de longitud, tipo, orden, catálogos, códigos de movimiento ni fechas documentadas.

## 8. Calidad

### Calidad estructural

La evidencia cubre longitud, codificación, conteos, filas cortas/largas/vacías, hashes, conflictos, extracción, período de publicación y schema drift. Los 93 ZIP presentan cero filas cortas, largas o vacías.

### Calidad semántica

La estructura, tipos declarados, formatos y algunos catálogos están documentados. La calidad semántica completamente validada sigue pendiente: no se han validado todos los dominios, faltantes por campo, duplicidad, consistencia de valores, territorialidad ni reglas de actualización del maestro.

## 9. Privacidad

Los DOCX documentan PII directa: cédulas, identificaciones, nombres y apellidos. También documentan PII indirecta o potencial: citas registrales, procedencia, hospital y combinaciones de fechas/códigos.

Los artefactos del Producto 1 contienen metadatos, definiciones, hashes y conteos. No incluyen valores TXT ni líneas RAW. La minimización y anonimización final pertenecen a DAT-04.

## 10. Selección y alcance

Se seleccionan los tres acontecimientos porque comparten fuente, cobertura publicada, procesamiento y relevancia para el ciclo demográfico. El alcance inicial es nacional agregado. La frecuencia analítica mensual es una propuesta futura, no una serie ya construida.

No se rellenan ausencias con cero, no se extrapolan períodos, no se duplican bloques y no se usa INEC como sustituto de movimientos TSE.

## 11. Limitaciones y dependencias posteriores

- No existe archivo maestro TSE disponible físicamente en el repositorio.
- No están documentadas las reglas completas para aplicar cambios y exclusiones al maestro.
- No está confirmada la cobertura histórica anterior a febrero de 2026.
- La fecha documentada no determina por sí sola la fecha definitiva para una serie temporal.
- La territorialidad y sus dominios no están suficientemente documentados.
- La anonimización final no pertenece a este producto.
- El Documento 18 completo no está disponible.
- FUE-01 no tiene un artefacto independiente de obtención inicial; el inventario y la organización efectiva del corte sí quedan demostrados por manifiestos, RAW, registry y auditoría.
- FUE-03 conserva gestión documentada sin comprobante primario del envío; esta ausencia no impide verificar el análisis de fuentes del Producto 1.

Estas limitaciones son dependencias para etapas posteriores o trazabilidad institucional complementaria. No invalidan el análisis de procedencia, cobertura, estructura, calidad, privacidad, selección y alcance presentado en este producto.

## 12. Estado de FUE-01 a FUE-05 y DOC-03

| Tarea | Estado real | Evidencia principal |
|---|---|---|
| FUE-01 | Cumplida para el alcance analítico del Producto 1; trazabilidad primaria de la obtención inicial no disponible | Manifiestos, inventario RAW, registry y auditoría |
| FUE-02 | Cumplida con limitaciones | [FUE-02_resumen.md](../evidencias/FUE-02_resumen.md), matrices oficiales |
| FUE-03 | Cumplida para el análisis de cobertura y maestro/movimientos; comprobante primario del envío institucional pendiente | [FUE-03_resumen.md](../evidencias/FUE-03_resumen.md), consulta y aporte documental |
| FUE-04 | Cumplida con limitaciones | [FUE-04_resumen.md](../evidencias/FUE-04_resumen.md), perfiles y diccionarios |
| FUE-05 | Documentada con limitaciones | [FUE-05_decision_alcance.md](../evidencias/FUE-05_decision_alcance.md), matrices |
| DOC-03 | Consolidado con limitaciones | Este informe, criterios DOC-03 y evidencia del Producto 1 |

## 13. Criterio formal de cierre

Producto 1 se declara cerrado cuando el análisis académico de fuentes tiene objetivo, procedencia, metodología, inventario, cobertura, estructura, calidad, privacidad, selección, alcance, limitaciones y trazabilidad verificables. Las dependencias de maestro, reconstrucción, anonimización y datasets posteriores no forman parte del criterio de cierre de este producto.

## 14. Conclusión

El Producto 1 dispone de una caracterización técnica verificable de 93 ZIP TSE y sus 93 DOCX internos, con diccionarios, posiciones, tipos, fechas, códigos de movimiento, hashes y ausencia de schema drift. La selección de nacimientos, matrimonios y defunciones y el alcance nacional agregado son defendibles para el corte documentado.

El Producto 1 queda **CERRADO** como informe de análisis de fuentes. La ausencia del comprobante primario del correo TSE, del Documento 18 completo y de un artefacto independiente de obtención inicial se conserva como limitación de trazabilidad institucional, no como bloqueo del análisis académico presentado.

## 15. Evidencias del Producto 1

- [TSE_schema_audit.md](../evidencias/TSE_schema_audit.md): demuestra la inspección de 93 ZIP, DOCX, firmas, sumas, códigos, fechas y ausencia de drift.
- [tse_schema_registry.csv](../../data/manifests/tse_schema_registry.csv): registra hashes y versión estructural por ZIP.
- [diccionario_nacimientos.md](../fuentes/diccionario_nacimientos.md): demuestra el layout de nacimientos.
- [diccionario_matrimonios.md](../fuentes/diccionario_matrimonios.md): demuestra el layout de matrimonios.
- [diccionario_defunciones.md](../fuentes/diccionario_defunciones.md): demuestra el layout de defunciones.
- [tse_manifest.csv](../../data/manifests/tse_manifest.csv): demuestra inventario, períodos, conteos y calidad estructural del lote.
- [perfil_datos_tse.md](../fuentes/perfil_datos_tse.md): resume campos, cobertura, privacidad y límites semánticos.
- [PRODUCTO_1_EVIDENCIAS.md](PRODUCTO_1_EVIDENCIAS.md): relaciona requisitos con evidencias.
- [PRODUCTO_1_CIERRE.md](PRODUCTO_1_CIERRE.md): contiene la matriz formal y el dictamen de cierre.
