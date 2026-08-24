# FUE-02 — Evidencia

Fecha: 2026-08-23

Objetivo: Inventariar únicamente fuentes oficiales del TSE relacionadas con nacimientos, matrimonios y defunciones, diferenciando movimientos, archivos maestros y documentación institucional, sin modificar DAT-01 ni los archivos RAW.

URL oficial principal utilizada: https://www.tse.go.cr/descarga_movimientos.html

Número de fuentes identificadas: 7

Fuentes TSE identificadas: 7

Fuentes INEC identificadas: 0

Cantidad por categoría:
- archivo maestro: 3
- movimiento: 3
- documentación: 1

Criterios Jira:

| Criterio | Estado | Evidencia |
|---|---|---|
| Institución | CUMPLE | Todas las fuentes registradas corresponden a TSE. |
| Enlace | CUMPLE | Todas las fuentes tienen URL oficial del TSE. |
| Formato | CUMPLE | Se documenta formato oficial o se indica `NO DOCUMENTADO EN LA FUENTE CONSULTADA`. |
| Cobertura | PARCIAL | La página oficial documenta el servicio de descarga, pero no la cobertura histórica completa. |
| Periodicidad | CUMPLE | La página oficial documenta actualización semanal por bloques de fechas; solicita archivos maestros mensualmente si no se actualiza semanalmente. |
| Granularidad | PARCIAL | Se documenta como “bloque de fechas” y “registro individual por movimiento”; no se ha documentado el detalle del archivo maestro. |
| Mecanismo de acceso | CUMPLE | Descarga directa desde la página oficial; solicitud de archivos maestros por correo institucional. |
| Observaciones | CUMPLE | Cada fuente incluye observación y rol dentro del TFG. |
| Archivo maestro diferenciado | CUMPLE | Se identifican 3 archivos maestros potenciales del TSE. |
| Movimiento diferenciado | CUMPLE | Se identifican 3 movimientos del TSE. |

Nota: El criterio de “estadística agregada” fue definido originalmente para un alcance TSE–INEC, pero el alcance vigente del TFG utiliza exclusivamente fuentes del TSE. Por ello, no se incorporó ninguna fuente del INEC.

Evidencia principal:
- docs/fuentes/matriz_fuentes_oficiales.csv
- docs/fuentes/matriz_fuentes_oficiales.md

Limitaciones:
- No se documentó un diccionario oficial completo del TSE para ancho fijo ni códigos de movimiento.
- Los archivos maestros no se encuentran físicamente en el repositorio y se mantienen como fuente administrativa potencial.
- La evidencia técnica local de DAT-01 se diferencia claramente de la documentación oficial del TSE.

Confirmación:
- DAT-01 no fue modificado.
- data/raw/tse no fue modificado por FUE-02.
