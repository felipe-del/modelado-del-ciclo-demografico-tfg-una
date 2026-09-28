# FUE-04 - Caracterización de fuentes seleccionadas

## Estado real

**CUMPLIDA CON LIMITACIONES.** FUE-04 caracteriza la publicación TSE y documenta su estructura interna sin exponer registros. La estructura está documentada; la calidad semántica completa y la validación de valores continúan pendientes.

## Resultado verificable

- 93 ZIP inspeccionados: 31 de nacimientos, 31 de matrimonios y 31 de defunciones.
- Cada ZIP contiene un TXT de movimientos y un DOCX de definición de campos.
- Los DOCX se leyeron desde `word/document.xml`.
- Cobertura de publicación común: 2026-02-01 a 2026-08-06.
- Nacimientos: 47.705 filas, longitud 281, 26 campos, `NAC-S01`.
- Matrimonios: 20.546 filas, longitud 328, 16 campos, `MAT-S01`.
- Defunciones: 18.719 filas, longitud 191, 12 campos, `DEF-S01`.
- Cero filas cortas, largas o vacías en los 93 ZIP.
- No se detectó schema drift; las firmas estructurales son estables por dataset.

## Estructura documentada

| Dataset | Tipo de Movimiento | Fechas documentadas | Tipos y reglas |
|---|---|---|---|
| Nacimientos | Posición 247, longitud 1; 1 exclusión, 2 cambio, 3 inclusión | Suceso, marginal, naturalización y aplicación; `AAAAMMDD` | 26 campos; tipos Numérico/Alfanumérico; catálogos de nacionalidad y marca de defunción |
| Matrimonios | Posición 1, longitud 2; 1 exclusión, 2 cambio, 3 inclusión | Suceso; `AAAAMMDD` | 16 campos; tipo de suceso documentado |
| Defunciones | Posición 2, longitud 1; 1 exclusión, 2 cambio, 3 inclusión | Campo Fecha; `DDMMYYYY` | 12 campos; identificadores y nombres documentados |

Detalle completo: [diccionario_nacimientos.md](../fuentes/diccionario_nacimientos.md), [diccionario_matrimonios.md](../fuentes/diccionario_matrimonios.md), [diccionario_defunciones.md](../fuentes/diccionario_defunciones.md), [TSE_schema_audit.md](TSE_schema_audit.md) y [tse_schema_registry.csv](../../data/manifests/tse_schema_registry.csv).

## Calidad estructural vs calidad semántica

La calidad estructural evaluada incluye longitud, codificación, hashes, conteos, extracción, períodos y drift. La calidad semántica completamente validada no se declara: aún faltan validación de dominios completos, faltantes por campo, consistencia de valores, reglas maestro/movimientos y territorialidad.

## Privacidad

Los DOCX identifican campos de PII directa e indirecta, incluyendo cédulas, identificaciones, nombres, apellidos, citas registrales y procedencia. Los artefactos FUE-04 contienen únicamente metadatos, conteos, hashes y definiciones; no contienen valores TXT.

## Artefactos

- `data/profiles/fue04_profile.json`
- `docs/fuentes/caracterizacion_acontecimientos.csv`
- `docs/fuentes/perfil_datos_tse.md`
- `docs/evidencias/TSE_schema_audit.md`
- `docs/evidencias/criterios_aceptacion_fue04.md`
