# Matriz de aceptación DAT-02

| Criterio Jira | Estado | Implementación | Evidencia |
|---|---|---|---|
| Procesa nacimientos, matrimonios y defunciones | CUMPLIDO | `sync_tse` y esquemas existentes | 93 ZIP locales: 31 por dataset |
| Descarga automática | CUMPLIDO POR PRUEBA SINTÉTICA | Descubrimiento HTML, descarga y contraste hash con biblioteca estándar | `test_dat02.py`; la fuente oficial respondió en `--dry-run` |
| Conserva ZIP originales y evita sobrescritura | CUMPLIDO | Estados `ALREADY_PRESENT` y `HASH_CONFLICT` | pruebas DAT-02 y verificación Git |
| Extrae ZIP en carpeta propia | CUMPLIDO | `data/work/extracted/tse/<dataset>/<zip>` | pruebas DAT-02 |
| Extracción segura | CUMPLIDO | Rechazo de rutas absolutas y traversal | prueba Zip Slip sintética |
| Detecta codificación | CUMPLIDO | BOM, UTF-8 estricto y respaldo del esquema | `latin-1` y `utf-8` registrados sin PII |
| Verifica longitud, hash, período, filas y estado | CUMPLIDO | Inspección y parser de nombre oficial | 93 ZIP; períodos 2026-02-01 a 2026-08-01; cero errores de longitud |
| Manifiesto idempotente | CUMPLIDO | Identidad dataset + nombre ZIP + SHA-256 | prueba de segunda ejecución |
| Reporte automático | CUMPLIDO | Generado desde manifiesto | `DAT-02_reporte.md` |
| No expone datos personales | CUMPLIDO | Solo metadatos, contadores y estados | pruebas y revisión de reporte |

## Dictamen

DAT-02 cumple los criterios técnicos mediante ejecución local, pruebas sintéticas y consulta real de la fuente oficial. No se descargó un ZIP nuevo durante la validación porque los 93 ZIP locales ya estaban presentes; la descarga y el conflicto remoto se demuestran con pruebas aisladas sin red.