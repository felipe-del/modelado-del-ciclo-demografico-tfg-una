# FUE-03 — Disponibilidad histórica oficial en el TSE

Fecha de actualización: 2026-08-29

## Objetivo

Analizar la disponibilidad histórica oficial del TSE para nacimientos, matrimonios y defunciones, y evaluar qué es necesario para reconstruir una base histórica utilizable sin asumir que los movimientos públicos son la historia completa desde un estado vacío.

## Alcance vigente

El proyecto utiliza exclusivamente fuentes del Tribunal Supremo de Elecciones (TSE). La presente investigación se limita a los registros y documentación oficiales del TSE.

## Metodología

1. Revisar la documentación oficial del TSE disponible en la página de descarga de movimientos.
2. Identificar los períodos públicos visibles para nacimientos, matrimonios y defunciones.
3. Evaluar la existencia y disponibilidad de archivos maestros.
4. Registrar el mecanismo institucional para solicitar archivos maestros.
5. Documentar la relación entre archivo maestro y movimientos sin afirmar más de lo que la fuente oficial permite comprobar.
6. Incorporar los DOCX internos de cada ZIP como evidencia estructural primaria del layout publicado.

## Evidencia pública del TSE revisada

Fuente oficial consultada:

- https://www.tse.go.cr/descarga_movimientos.html

### Documentación visible

La página oficial del TSE publica movimientos para nacimientos, matrimonios y defunciones, y describe estos archivos como movimientos utilizados para actualizar archivos maestros. Además, la misma página indica que, si no se realizan actualizaciones semanales, se recomienda solicitar mensualmente los archivos maestros al correo institucional secretariadtic@tse.go.cr.

## Períodos TSE identificados

| Dataset | Periodo público identificado | Estado |
|---|---|---|
| Nacimientos | 2026-02 a 2026-08, por bloques de fechas | documentado |
| Matrimonios | 2026-02 a 2026-08, por bloques de fechas | documentado |
| Defunciones | 2026-02 a 2026-08, por bloques de fechas | documentado |
| Archivo maestro público del TSE | no documentado como descarga pública | no documentado |
| Cobertura histórica previa no visible | no documentada en la fuente pública revisada | no documentada |

## Disponibilidad de archivos maestros

| Requisito | Estado |
|---|---|
| Archivo maestro de nacimientos | no documentado como descarga pública |
| Archivo maestro de matrimonios | no documentado como descarga pública |
| Archivo maestro de defunciones | no documentado como descarga pública |
| Procedimiento oficial de solicitud | documentado mediante correo institucional |
| Forma oficial del archivo maestro | no documentada en la fuente pública revisada |

## Relación maestro / movimientos

La documentación pública del TSE describe los archivos publicados como movimientos utilizados para actualizar archivos maestros. Con la cobertura pública actualmente identificada, la reconstrucción de un estado registral completo requiere disponer de un archivo maestro o estado inicial sobre el cual aplicar posteriormente los movimientos. No se presume que los movimientos públicos disponibles representen la totalidad de la historia registral desde un estado vacío.

## Conclusión de reconstrucción

CONCLUSION_RECONSTRUCCION = REQUIERE_MAESTRO_INICIAL

## Limitaciones pendientes

- No existe un archivo maestro público descargable en la página oficial revisada.
- Las posiciones, longitudes, tipos y códigos del layout de movimientos están documentados en los DOCX internos de los ZIP; las reglas de relación con archivos maestros siguen sin documentarse.
- No se ha verificado la cobertura histórica completa anterior a los bloques del 2026 mediante una fuente oficial pública accesible.
- La documentación pública no sustituye las reglas institucionales de relación maestro/movimientos; el layout de los movimientos sí está documentado en los DOCX internos.

## Gestión ante el TSE

ESTADO_CONSULTA_TSE = GESTIÓN DOCUMENTADA / EVIDENCIA PRIMARIA PENDIENTE

El repositorio conserva el texto de la consulta y el objetivo de la gestión, pero no contiene PDF, captura, export de correo ni otro artefacto verificable del envío. La respuesta institucional tampoco está disponible.

## Próximos pasos

1. Incorporar evidencia primaria del envío únicamente si se obtiene de forma verificable.
2. Incorporar la respuesta institucional recibida únicamente si se obtiene de manera verificable.
3. Mantener DAT-01 sin reinterpretar ni alterar su estado.
4. Conservar como dependencias el maestro inicial y las reglas operativas de reconstrucción.

## Matriz de cumplimiento

| Criterio Jira | Estado |
|---|---|
| Gestión ante TSE documentada | DOCUMENTADA; evidencia primaria pendiente |
| Períodos TSE disponibles identificados | CUMPLE |
| Disponibilidad de maestros investigada | CUMPLE |
| Necesidad maestro/movimientos evaluada | CUMPLE |
| Fuentes históricas TSE registradas | CUMPLE |
| Layout de movimientos | DOCUMENTADO en DOCX internos de los 93 ZIP |
| Maestro y reglas de reconstrucción | LIMITACIÓN DOCUMENTADA / PENDIENTE |

## Estado final

FUE-03 = GESTIÓN DOCUMENTADA / EVIDENCIA PRIMARIA PENDIENTE

El análisis de cobertura y la necesidad de un maestro inicial están documentados. No se declara enviado ni cerrada la gestión institucional porque falta evidencia primaria verificable.
