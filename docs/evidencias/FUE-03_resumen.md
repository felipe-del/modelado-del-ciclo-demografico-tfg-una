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
6. Mantener el diccionario de códigos y posiciones como limitación técnica documentada, sin convertirlo en un criterio de cierre automático de FUE-03.

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
- No se documenta un diccionario oficial del TSE para posiciones, longitudes, códigos y relaciones entre archivos maestros y movimientos.
- No se ha verificado la cobertura histórica completa anterior a los bloques del 2026 mediante una fuente oficial pública accesible.
- La falta de diccionario oficial no bloquea por sí sola FUE-03, pero sí debe dejarse documentada como dependencia técnica para tareas posteriores.

## Gestión ante el TSE

ESTADO_CONSULTA_TSE = ENVIADO

La gestión formal ante el TSE fue efectivamente realizada y queda documentada con evidencia de envío. La respuesta institucional sigue pendiente y no se declara recibida ni respondida.

## Próximos pasos

1. Mantener la evidencia del envío como trazabilidad formal.
2. Incorporar la respuesta institucional recibida únicamente si se obtenga de manera verificable.
3. Mantener DAT-01 sin reinterpretar ni alterar su estado.
4. Conservar la limitación técnica del diccionario oficial como dependencia para etapas posteriores.

## Matriz de cumplimiento

| Criterio Jira | Estado |
|---|---|
| Gestión ante TSE documentada | CUMPLE |
| Períodos TSE disponibles identificados | CUMPLE |
| Disponibilidad de maestros investigada | CUMPLE |
| Necesidad maestro/movimientos evaluada | CUMPLE |
| Fuentes históricas TSE registradas | CUMPLE |
| Diccionario oficial | LIMITACIÓN DOCUMENTADA / PENDIENTE PARA ETAPAS POSTERIORES |

## Estado final

FUE-03 = LISTA_PARA_CERRAR

La respuesta institucional del TSE continúa pendiente, pero la traza documental y la evidencia de gestión formal ya están cumplidas. La limitación del diccionario oficial permanece documentada para etapas posteriores y no invalida el cierre documental de FUE-03.
