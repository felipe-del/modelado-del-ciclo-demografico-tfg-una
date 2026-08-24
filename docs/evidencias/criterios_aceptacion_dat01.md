# Matriz de aceptación DAT-01

| Criterio Jira | Estado | Implementación | Evidencia |
|---|---|---|---|
| Abrir ZIP | CUMPLIDO | `archive_reader.open_source` abre ZIP sin extracción permanente | Tres ZIP reales procesados por `verify-dat01` |
| Localizar TXT | CUMPLIDO | Selecciona automáticamente miembros `.txt` e ignora auxiliares | `MOVWEBNAC.txt`, `MOVWEBMAT.txt`, `MOVWEBDEF.txt` |
| Verificar longitud | CUMPLIDO | Validación contra el esquema JSON | 281, 328 y 191 caracteres |
| Reportar filas | CUMPLIDO | `ImportSummary` y salida CLI | Evidencias JSON y SQLite |
| Reportar inclusiones | BLOQUEADO POR DICCIONARIO | Clasificador y campo configurables; códigos reales no disponibles | `NO CONFIGURADO`, valor SQLite `NULL` |
| Reportar cambios | BLOQUEADO POR DICCIONARIO | Clasificador y códigos configurables | `NO CONFIGURADO`, valor SQLite `NULL` |
| Reportar exclusiones | BLOQUEADO POR DICCIONARIO | Clasificador y códigos configurables | `NO CONFIGURADO`, valor SQLite `NULL` |
| Reportar errores | CUMPLIDO | Validación de longitud, estructura y campos | `import_issues` y contadores de error |
| No guardar nombres | CUMPLIDO | SQLite solo define metadatos técnicos | Prueba de privacidad y `schema.sql` |
| No guardar cédulas | CUMPLIDO | No existen columnas ni valores RAW | Prueba de privacidad |
| SQLite | CUMPLIDO | `import_runs` e `import_issues` con consultas parametrizadas | `data/db/imports.sqlite` |
| README | CUMPLIDO | Documenta alcance, uso, privacidad y limitaciones | `README.md` |
| Pruebas | CUMPLIDO | Suite sintética de pytest | `python -m pytest -v` |
| Ejecución real | CUMPLIDO | Orquestador procesa las tres muestras conocidas | `python -m tfg_demografia verify-dat01` |

## Dictamen

DAT-01 está técnicamente implementada. El conteo real de inclusiones, cambios y exclusiones permanece bloqueado hasta disponer de documentación oficial del TSE que defina posición y códigos. No se infieren valores desde registros reales.