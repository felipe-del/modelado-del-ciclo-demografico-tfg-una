# Matriz de aceptación DAT-01

| Criterio Jira | Estado | Implementación | Evidencia |
|---|---|---|---|
| Abrir ZIP | CUMPLIDO | `archive_reader.open_source` abre ZIP sin extracción permanente | Tres ZIP reales procesados por `verify-dat01` |
| Localizar TXT | CUMPLIDO | Selecciona automáticamente miembros `.txt` e ignora auxiliares | `MOVWEBNAC.txt`, `MOVWEBMAT.txt`, `MOVWEBDEF.txt` |
| Verificar longitud | CUMPLIDO | Validación contra el esquema JSON | 281, 328 y 191 caracteres |
| Reportar filas | CUMPLIDO | `ImportSummary` y salida CLI | Evidencias JSON y SQLite |
| Reportar inclusiones | CUMPLIDO CON LIMITACIÓN | Campo y códigos documentados en DOCX TSE; configuración de schema actualizada | `TSE_schema_audit.md`; `NO CONFIGURADO` histórico |
| Reportar cambios | CUMPLIDO CON LIMITACIÓN | Campo y códigos documentados en DOCX TSE; configuración de schema actualizada | `TSE_schema_audit.md`; `NO CONFIGURADO` histórico |
| Reportar exclusiones | CUMPLIDO CON LIMITACIÓN | Campo y códigos documentados en DOCX TSE; configuración de schema actualizada | `TSE_schema_audit.md`; `NO CONFIGURADO` histórico |
| Reportar errores | CUMPLIDO | Validación de longitud, estructura y campos | `import_issues` y contadores de error |
| No guardar nombres | CUMPLIDO | SQLite solo define metadatos técnicos | Prueba de privacidad y `schema.sql` |
| No guardar cédulas | CUMPLIDO | No existen columnas ni valores RAW | Prueba de privacidad |
| SQLite | CUMPLIDO | `import_runs` e `import_issues` | `data/db/imports.sqlite` |
| Pruebas | CUMPLIDO | Suite pytest | `python -m pytest -q` |
| Ejecución real | CUMPLIDO | Orquestador procesa muestras conocidas | `python -m tfg_demografia verify-dat01` |

## Dictamen

DAT-01 conserva su alcance de validación técnica y privacidad. La evidencia DOCX permite configurar el movimiento en una futura ejecución real; no se amplía DAT-01 a reconstrucción histórica ni almacenamiento de registros.
