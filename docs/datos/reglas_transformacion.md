# DAT-03 - Reglas de transformación

Las reglas son declarativas y versionadas en `config/transformations/`. Su fuente estructural es el DOCX incluido en cada ZIP TSE. Las firmas estables son `NAC-S01`, `MAT-S01` y `DEF-S01`.

| Regla | Estado | Fuente | Aplicación |
|---|---|---|---|
| Layout fixed-width | ACTIVA | Diccionarios DOCX TSE | Posiciones 1-based calculadas y validadas |
| Texto | ACTIVA | Tipo Alfanumérico/identificadores DOCX | `strip`, conservando representación y ceros |
| Códigos | ACTIVA CON LIMITACIÓN | DOCX TSE | Se conservan como texto; enums validan dominios explícitos |
| Tipo de Movimiento | ACTIVA | DOCX TSE | 1 exclusión, 2 cambio, 3 inclusión |
| Fecha AAAAMMDD | ACTIVA | DOCX TSE | `date_ymd` en nacimientos y matrimonios |
| Fecha DDMMYYYY | ACTIVA | DOCX TSE | `date_dmy` en defunciones |
| Vacíos | NO AUTOMÁTICA | No hay regla TSE explícita | No se aplica `empty_to_null` |
| Unidades | BLOQUEADA | No documentadas | No convertir |
| Territorialidad | BLOQUEADA | No documentada | No interpretar |
| Anonimización | FUERA DE DAT-03 | DAT-04 | No eliminar ni publicar PII en este incremento |
| Reconstrucción | FUERA DE DAT-03 | DAT-05 | No aplicar movimientos a un maestro |

## Política

- `data/raw/` permanece inmutable.
- La salida se escribe en `data/work/normalized/`.
- La bitácora contiene hashes, conteos, excepciones y estados, nunca valores de registros.
- Los campos PII se reconocen técnicamente, pero su uso analítico queda sujeto a DAT-04.
