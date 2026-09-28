# Criterios de aceptación DAT-03

| Criterio | Estado | Evidencia | Resultado |
|---|---|---|---|
| Parte de RAW inmutable | CUMPLIDO | `normalization.py`; pruebas ZIP/TXT | Entrada de solo lectura y salida separada |
| Campos y posiciones | CUMPLIDO | Diccionarios DOCX TSE y schemas NAC/MAT/DEF-S01 | Layout documentado por dataset |
| Tipos documentados | CUMPLIDO CON LIMITACIÓN | DOCX y schemas | Numérico/alfanumérico representados conservadoramente |
| Fechas AAAAMMDD | CUMPLIDO | Schemas y `date_ymd` | Nacimientos y matrimonios |
| Fecha DDMMYYYY | CUMPLIDO | Schema y `date_dmy` | Defunciones |
| Tipo de Movimiento | CUMPLIDO CON LIMITACIÓN | DOCX, enum y movement config | 1 exclusión, 2 cambio, 3 inclusión |
| Catálogos explícitos | CUMPLIDO CON LIMITACIÓN | Enums de schemas | Nacionalidad, defunción y tipo de suceso |
| Reglas registradas | CUMPLIDO | `config/transformations/` | Reglas versionadas por schema |
| Ceros iniciales | CUMPLIDO | `tests/test_dat03.py` | Códigos e identificadores permanecen texto |
| Excepciones registradas | CUMPLIDO | `NormalizationResult` y bitácora | Conteos sin valores RAW |
| Dry-run sin escritura | CUMPLIDO | Pruebas existentes | No crea salida ni bitácora |
| Idempotencia | CUMPLIDO | Pruebas existentes | Hash estable para entrada y reglas iguales |
| Privacidad final | PENDIENTE DAT-04 | `matriz_privacidad_campos.md` | Requiere minimización/anónimo final |
| Reconstrucción histórica | PENDIENTE DAT-05 | Evidencia FUE-03 | Requiere maestro inicial y reglas operativas |

## Dictamen

**IMPLEMENTADO CON LIMITACIONES.** La normalización semántica inicial está habilitada por documentación primaria TSE; no constituye todavía el dataset procesado y anonimizado final.
