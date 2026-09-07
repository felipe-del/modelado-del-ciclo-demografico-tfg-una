# DAT-03 - Reglas de transformación

## Estado actual

Las reglas son declarativas, versionadas en `config/transformations/` y no ejecutan código dinámico. Los tres esquemas TSE actuales tienen `fields: []`; por eso no se inventan nombres, posiciones ni significados y la transformación semántica está `BLOQUEADA_POR_DOCUMENTACION`.

| Regla | Dataset | Campo | Transformación | Justificación | Estado |
|---|---|---|---|---|---|
| DAT03-STRUCT-001 | nacimientos, matrimonios, defunciones | Ninguno configurado | Validar longitud, conservar registros válidos como estructura JSON vacía y registrar conteos | No existe diccionario oficial de campos | ACTIVA |
| DAT03-TEXT-001 | Todos | Campos futuros documentados | Conservar texto y ceros iniciales; `strip` solo si se declara | Los códigos e identificadores no deben convertirse automáticamente a entero | NO_CONFIGURADA |
| DAT03-DATE-001 | Todos | Fechas internas | Convertir solo con formato y significado documentados | FUE-04 declara fechas internas no determinadas | BLOQUEADA_POR_DOCUMENTACION |
| DAT03-CODE-001 | Todos | Códigos/categorías | Conservar código y aplicar catálogo cerrado solo si existe | No hay catálogo oficial verificable | BLOQUEADA_POR_DOCUMENTACION |
| DAT03-NULL-001 | Todos | Campos futuros | Distinguir vacío, espacio y null solo con regla documentada | No se convierten `0`, `0000` o `999` automáticamente | BLOQUEADA_POR_DOCUMENTACION |
| DAT03-UNIT-001 | Todos | Unidades futuras | Sin conversiones | No hay unidades documentadas | BLOQUEADA_POR_DOCUMENTACION |

## Política

- `data/raw/` y `data/work/extracted/` son entradas inmutables.
- La salida se escribe en `data/work/normalized/`.
- La bitácora contiene hashes, conteos y códigos agregados; nunca valores de registros.
- Una excepción incrementa `exception_count` y no expone el valor que la causó.
- No hay correcciones manuales ocultas.
