# Perfil de datos TSE - FUE-04

Este perfil se genera desde el manifiesto DAT-02 y los esquemas técnicos. No contiene líneas RAW, valores individuales ni identificadores.

## Criterio de interpretación

La cobertura descrita es de publicación de movimientos, no de ocurrencia del acontecimiento. No hay posiciones de fechas internas documentadas oficialmente en el workspace; por tanto, fecha del suceso, fecha marginal y fecha de aplicación se declaran `NO DOCUMENTADO EN LA FUENTE CONSULTADA`.

| Característica | Nacimientos | Matrimonios | Defunciones |
|---|---|---|---|
| Longitud esperada | 281 | 328 | 191 |
| Archivos analizados | 31 | 31 | 31 |
| Filas | 47705 | 20546 | 18719 |
| Filas con longitud válida | 47705 | 20546 | 18719 |
| Filas cortas | 0 | 0 | 0 |
| Filas largas | 0 | 0 | 0 |
| Filas vacías | 0 | 0 | 0 |
| Cobertura publicación mínima | 2026-02-01 | 2026-02-01 | 2026-02-01 |
| Cobertura publicación máxima | 2026-08-06 | 2026-08-06 | 2026-08-06 |
| Huecos aparentes (días) | 0 | 0 | 0 |
| Nivel territorial | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO |
| Identificadores potenciales | NO DOCUMENTADO EN LA FUENTE CONSULTADA | NO DOCUMENTADO EN LA FUENTE CONSULTADA | NO DOCUMENTADO EN LA FUENTE CONSULTADA |
| Faltantes por campo | NO DETERMINADO: no hay campos con posiciones oficialmente documentadas o configuradas. | NO DETERMINADO: no hay campos con posiciones oficialmente documentadas o configuradas. | NO DETERMINADO: no hay campos con posiciones oficialmente documentadas o configuradas. |

## NACIMIENTOS

- Archivo TXT: `MOVWEBNAC.txt`.
- Patrón ZIP: `nac_*.zip`.
- Codificación observada: latin-1, utf-8.
- Periodicidad: semanal por bloques de fechas; no se presupone que cada bloque tenga siete días.
- Movimientos: NO CONFIGURADOS por ausencia de diccionario oficial.
- Privacidad: ALTO: los TXT registrales pueden contener datos identificables; el perfil no conserva valores ni lineas.

### Campos y variables

| Campo | Posición | Longitud | Tipo | Obligatorio | Fuente de definición | Estado |
|---|---:|---:|---|---|---|---|
| NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | Sin diccionario oficial en el workspace | NO DETERMINADO |

### Fechas

| Nombre lógico | Significado | Fuente | Formato | Presente en esquema | Uso correcto | Riesgo |
|---|---|---|---|---|---|---|
| Fecha del suceso | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |
| Fecha marginal | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |
| Fecha de aplicación | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |

La fecha contenida en el nombre del ZIP se utiliza únicamente como período de publicación del movimiento; no identifica por sí misma ninguna de las fechas internas anteriores.

## MATRIMONIOS

- Archivo TXT: `MOVWEBMAT.txt`.
- Patrón ZIP: `mat_*.zip`.
- Codificación observada: latin-1, utf-8.
- Periodicidad: semanal por bloques de fechas; no se presupone que cada bloque tenga siete días.
- Movimientos: NO CONFIGURADOS por ausencia de diccionario oficial.
- Privacidad: ALTO: los TXT registrales pueden contener datos identificables; el perfil no conserva valores ni lineas.

### Campos y variables

| Campo | Posición | Longitud | Tipo | Obligatorio | Fuente de definición | Estado |
|---|---:|---:|---|---|---|---|
| NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | Sin diccionario oficial en el workspace | NO DETERMINADO |

### Fechas

| Nombre lógico | Significado | Fuente | Formato | Presente en esquema | Uso correcto | Riesgo |
|---|---|---|---|---|---|---|
| Fecha del suceso | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |
| Fecha marginal | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |
| Fecha de aplicación | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |

La fecha contenida en el nombre del ZIP se utiliza únicamente como período de publicación del movimiento; no identifica por sí misma ninguna de las fechas internas anteriores.

## DEFUNCIONES

- Archivo TXT: `MOVWEBDEF.txt`.
- Patrón ZIP: `def_*.zip`.
- Codificación observada: latin-1.
- Periodicidad: semanal por bloques de fechas; no se presupone que cada bloque tenga siete días.
- Movimientos: NO CONFIGURADOS por ausencia de diccionario oficial.
- Privacidad: ALTO: los TXT registrales pueden contener datos identificables; el perfil no conserva valores ni lineas.

### Campos y variables

| Campo | Posición | Longitud | Tipo | Obligatorio | Fuente de definición | Estado |
|---|---:|---:|---|---|---|---|
| NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | NO DETERMINADO | Sin diccionario oficial en el workspace | NO DETERMINADO |

### Fechas

| Nombre lógico | Significado | Fuente | Formato | Presente en esquema | Uso correcto | Riesgo |
|---|---|---|---|---|---|---|
| Fecha del suceso | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |
| Fecha marginal | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |
| Fecha de aplicación | NO DOCUMENTADO EN LA FUENTE CONSULTADA | Sin diccionario oficial | NO DETERMINADO | No | No inferir desde el nombre ZIP | Confundir periodo de publicación con fecha del acontecimiento |

La fecha contenida en el nombre del ZIP se utiliza únicamente como período de publicación del movimiento; no identifica por sí misma ninguna de las fechas internas anteriores.
