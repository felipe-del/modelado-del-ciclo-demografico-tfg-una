# Perfil de datos TSE - FUE-04

Este perfil resume metadatos de los 93 ZIP y sus DOCX internos. No contiene líneas RAW ni valores individuales.

## Interpretación

La cobertura indicada es de publicación de movimientos, no de ocurrencia. Los campos, posiciones, tipos, formatos y códigos se documentan en los DOCX internos leídos desde `word/document.xml`. La elección de una fecha definitiva para una serie temporal y la calidad semántica completa requieren decisiones posteriores.

| Característica | Nacimientos | Matrimonios | Defunciones |
|---|---:|---:|---:|
| ZIP analizados | 31 | 31 | 31 |
| Campos documentados | 26 | 16 | 12 |
| Longitud esperada | 281 | 328 | 191 |
| Filas | 47705 | 20546 | 18719 |
| Filas con longitud válida | 47705 | 20546 | 18719 |
| Filas cortas/largas/vacías | 0/0/0 | 0/0/0 | 0/0/0 |
| Cobertura de publicación | 2026-02-01 a 2026-08-06 | 2026-02-01 a 2026-08-06 | 2026-02-01 a 2026-08-06 |
| Schema | NAC-S01 | MAT-S01 | DEF-S01 |
| Schema drift | AUSENTE | AUSENTE | AUSENTE |
| Tipo de Movimiento | Posición 247; 1/2/3 | Posición 1-2; 1/2/3 | Posición 2; 1/2/3 |

## Fechas documentadas

- Nacimientos: Fecha del Suceso, Fecha de Marginal, Fecha de Naturalización y Fecha de Aplicación, formato `AAAAMMDD`.
- Matrimonios: Fecha del Suceso, formato `AAAAMMDD`.
- Defunciones: campo Fecha, formato `DDMMYYYY`.

Estas definiciones no convierten automáticamente el período del nombre ZIP en fecha de ocurrencia ni resuelven por sí solas la fecha de la serie temporal.

## Privacidad y limitaciones

Los DOCX identifican campos de PII directa e indirecta: cédulas, identificaciones, nombres, apellidos, citas registrales y procedencia. Los valores no se reproducen. Faltantes por campo, dominios completos, territorialidad, maestro inicial, reglas de reconstrucción y anonimización final permanecen pendientes.

## Artefactos

- `data/profiles/fue04_profile.json`
- `docs/fuentes/caracterizacion_acontecimientos.csv`
- `docs/fuentes/diccionario_nacimientos.md`
- `docs/fuentes/diccionario_matrimonios.md`
- `docs/fuentes/diccionario_defunciones.md`
- `data/manifests/tse_schema_registry.csv`
- `docs/evidencias/TSE_schema_audit.md`
