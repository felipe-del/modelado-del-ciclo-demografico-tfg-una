# FUE-04 - Caracterización de fuentes seleccionadas

FUE-04 genera un perfil técnico y semántico de los movimientos TSE seleccionados como fuente primaria RAW. Se reutiliza el manifiesto DAT-02 y los esquemas del proyecto; no se inspeccionan ni almacenan valores individuales.

## Resultado verificable

- Nacimientos: 31 ZIP, 47.705 filas, longitud esperada 281.
- Matrimonios: 31 ZIP, 20.546 filas, longitud esperada 328.
- Defunciones: 31 ZIP, 18.719 filas, longitud esperada 191.
- Cobertura de publicación: 2026-02-01 a 2026-08-06 en los tres acontecimientos.
- Periodicidad: semanal por bloques, con bloques parciales; huecos aparentes entre bloques: 0 días.
- Inconsistencias estructurales: 0 filas cortas, largas o vacías.
- Codificaciones observadas: nacimientos y matrimonios `latin-1`/`utf-8`; defunciones `latin-1`.

## Fechas, campos y privacidad

El nombre ZIP identifica únicamente el período de publicación del movimiento. Las fechas del suceso, marginal y de aplicación son `NO DOCUMENTADO EN LA FUENTE CONSULTADA`. Los esquemas actuales no configuran campos ni posiciones, por lo que faltantes por campo, identificadores potenciales y nivel territorial son `NO DETERMINADO` o `NO DOCUMENTADO EN LA FUENTE CONSULTADA`.

Los TXT registrales se clasifican con riesgo de privacidad alto. Los artefactos FUE-04 contienen solamente metadatos, conteos, porcentajes y categorías; no incluyen líneas RAW ni valores individuales.

## Artefactos

- `data/profiles/fue04_profile.json`
- `docs/fuentes/caracterizacion_acontecimientos.csv`
- `docs/fuentes/perfil_datos_tse.md`
- `docs/evidencias/criterios_aceptacion_fue04.md`