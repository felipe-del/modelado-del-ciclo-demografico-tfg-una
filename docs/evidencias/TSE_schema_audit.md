# Auditor?a t?cnica de schemas TSE

- ZIP inspeccionados: **93**.
- Distribuci?n: **31 nacimientos, 31 matrimonios, 31 defunciones**.
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

Los DOCX documentan campos, longitudes, tipos, rellenos, identificadores, fechas y cat?logos. El Tipo de Movimiento aparece como `1 = Exclusi?n`, `2 = Cambio`, `3 = Inclusi?n` en los tres datasets.

Fechas documentadas: nacimientos (suceso, marginal, naturalizaci?n, aplicaci?n en AAAAMMDD), matrimonios (suceso en AAAAMMDD) y defunciones (campo Fecha en DDMMYYYY).

PII directa identificada documentalmente: c?dulas, identificaciones, nombres y apellidos. PII indirecta: citas registrales, procedencia, hospital y combinaciones de fechas/c?digos.

## Qu? bloqueos se resolvieron

- Campos y posiciones fixed-width.
- Tipos declarados por el TSE.
- C?digos y posici?n de Tipo de Movimiento.
- Formatos de fechas documentados.
- Cat?logos expl?citos de nacionalidad, marca de defunci?n y tipo de suceso.

## Qu? bloqueos siguen pendientes

- Archivo maestro o estado inicial.
- Reglas completas para aplicar cambios y exclusiones.
- Cobertura hist?rica anterior a febrero de 2026.
- Anonimizaci?n final y minimizaci?n DAT-04.
- Definici?n metodol?gica definitiva de la serie temporal.
- Territorialidad y unidades no documentadas.
