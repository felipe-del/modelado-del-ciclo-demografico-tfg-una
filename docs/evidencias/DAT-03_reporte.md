# DAT-03 - Reporte de limpieza y normalización

## Estado

DAT-03 mantiene una capa declarativa, reproducible y separada de RAW. Con la evidencia de los 93 DOCX internos del TSE, la normalización semántica inicial queda habilitada para los tres layouts estables `NAC-S01`, `MAT-S01` y `DEF-S01`.

La salida JSONL se genera desde ZIP/TXT en modo lectura y no modifica `data/raw/tse/`. Los identificadores, nombres, apellidos y otros campos personales están configurados para trazabilidad técnica, pero quedan sujetos a exclusión/minimización posterior en DAT-04.

## Evidencia estructural

- 93 ZIP inspeccionados: 31 por dataset.
- Cada ZIP contiene un TXT y un DOCX.
- El DOCX se leyó desde `word/document.xml`.
- Firmas: nacimientos `445ae4c469e6ba2b`, matrimonios `092fe259301b271e`, defunciones `18a8912c3b4fa233`.
- No se detectó schema drift.
- Sumas documentadas y longitudes TXT: 281, 328 y 191, con diferencia cero.

Evidencia detallada: [TSE_schema_audit.md](TSE_schema_audit.md), [diccionario_nacimientos.md](../fuentes/diccionario_nacimientos.md), [diccionario_matrimonios.md](../fuentes/diccionario_matrimonios.md), [diccionario_defunciones.md](../fuentes/diccionario_defunciones.md).

## Reglas activas

- Campos, posiciones y tipos respaldados por DOCX TSE.
- Códigos de movimiento conservados como texto.
- Tipo de Movimiento: `1` exclusión, `2` cambio, `3` inclusión.
- Fechas de nacimientos y matrimonios: `AAAAMMDD`.
- Fecha de defunciones: `DDMMAAAA`.
- Catálogos documentados se validan mediante `enum`; no se inventan catálogos territoriales, hospitalarios o de país.
- No se aplica `empty_to_null` automáticamente.
- Los ceros iniciales se conservan.

## Limitaciones

DAT-03 no implementa anonimización final, maestro inicial, reconstrucción de cambios/exclusiones, agregación temporal, series, modelado ni web. El significado operativo completo de fechas y la regla de aplicación al maestro siguen pendientes de validación institucional.

## Ejecución

```powershell
python -m tfg_demografia normalize --source <ZIP-o-TXT> --dataset <dataset> --dry-run
```

La bitácora conserva hashes, conteos, estado y timestamp; nunca valores de registros.

## Dictamen

**DAT-03 = IMPLEMENTADO CON LIMITACIONES.** La capa estructural previa y la capa semántica documentada están implementadas y probadas. La privacidad final y la reconstrucción permanecen fuera de este incremento.
