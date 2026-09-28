# Auditoría técnica de schemas TSE

- ZIP inspeccionados: **93**.
- Distribución: **31 nacimientos, 31 matrimonios, 31 defunciones**.
- Cada ZIP contiene un TXT y un DOCX; los DOCX se leyeron desde `word/document.xml`.
- Los valores de registros TXT no fueron incluidos.

## Firmas y drift

| dataset | firma | ZIP | hashes DOCX | drift |
|---|---|---:|---:|---|
| nacimientos | `445ae4c469e6ba2b` | 31 | 31 | AUSENTE |
| matrimonios | `092fe259301b271e` | 31 | 31 | AUSENTE |
| defunciones | `18a8912c3b4fa233` | 31 | 31 | AUSENTE |

## Consistencia de longitud

| dataset | suma DOCX | longitud TXT | diferencia |
|---|---:|---:|---:|
| nacimientos | 281 | 281 | 0 |
| matrimonios | 328 | 328 | 0 |
| defunciones | 191 | 191 | 0 |

## Hallazgos

Los DOCX documentan campos, longitudes, tipos, rellenos, identificadores, fechas y catálogos. El Tipo de Movimiento aparece como `1 = Exclusión`, `2 = Cambio`, `3 = Inclusión` en los tres datasets.

Fechas documentadas: nacimientos (suceso, marginal, naturalización, aplicación en AAAAMMDD), matrimonios (suceso en AAAAMMDD) y defunciones (campo Fecha en DDMMYYYY).

PII directa identificada documentalmente: cédulas, identificaciones, nombres y apellidos. PII indirecta: citas registrales, procedencia, hospital y combinaciones de fechas/códigos.

## Qué bloqueos se resolvieron

- Campos y posiciones fixed-width.
- Tipos declarados por el TSE.
- Códigos y posición de Tipo de Movimiento.
- Formatos de fechas documentados.
- Catálogos explícitos de nacionalidad, marca de defunción y tipo de suceso.

## Qué bloqueos siguen pendientes

- Archivo maestro o estado inicial.
- Reglas completas para aplicar cambios y exclusiones.
- Cobertura histórica anterior a febrero de 2026.
- Anonimización final y minimización DAT-04.
- Definición metodológica definitiva de la serie temporal.
- Territorialidad y unidades no documentadas.
