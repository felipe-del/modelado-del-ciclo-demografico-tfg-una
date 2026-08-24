# FUE-02 — Inventario de fuentes oficiales del TSE

## Objetivo

Inventariar únicamente las fuentes oficiales del Tribunal Supremo de Elecciones (TSE) relacionadas con nacimientos, matrimonios y defunciones, con diferenciación clara entre:

- movimientos del TSE;
- archivos maestros del TSE;
- documentación oficial pertinente del TSE.

## Fecha de la investigación

Fecha de verificación y documentación: 2026-08-23.

## Fuente oficial principal utilizada

La fuente principal de movimientos es:

https://www.tse.go.cr/descarga_movimientos.html

Esta página oficial del TSE documenta la descarga de movimientos de nacimientos, matrimonios y defunciones, así como la actualización de los archivos maestros y la solicitud institucional de archivos maestros por correo electrónico.

## Criterios para considerar una fuente oficial

Se consideró oficial toda fuente publicada en un dominio institucional del TSE y vinculada directamente a la administración o actualización de los archivos registrales.

## Dominios consultados

- https://www.tse.go.cr/
- https://www.tse.go.cr/descarga_movimientos.html

Se excluyeron blogs, copias no institucionales, Wikipedia, GitHub de terceros y fuentes sin procedencia oficial.

## Criterios de clasificación

Se utilizó la siguiente taxonomía:

- ARCHIVO_MAESTRO: base administrativa del Registro Civil.
- MOVIMIENTO: archivo de actualización para el proceso de registro.
- DOCUMENTACION: página oficial institucional que orienta la descarga y el uso de los archivos.

También se definió el rol dentro del TFG:

- PRIMARIA_RAW: entrada potencial del pipeline RAW.
- PRIMARIA_POTENCIAL: fuente administrativa relevante pero no disponible físicamente en el repositorio.
- DOCUMENTACION: fuente institucional para contextualizar acceso y mecanismo de actualización.

## Diferencia entre fuente primaria y documento institucional

En este proyecto, la fuente primaria es la que puede alimentar el pipeline RAW. Para el TFG, los tres movimientos del TSE son la entrada RAW seleccionada, porque la página oficial documenta que se publican como archivos de descarga y porque DAT-01 verificó localmente muestras reales.

Los archivos maestros del TSE se mantienen como fuente administrativa potencial, porque la institución informa que pueden solicitarse por correo institucional, pero no se dispone de archivos físicos en el repositorio del proyecto.

## Diferencia entre archivo maestro y movimiento

- Archivo maestro: base institucional administrativa del Registro Civil.
- Movimiento: archivo de actualización por bloque temporal para facilitar la incorporación de cambios.

La página oficial del TSE distingue claramente la descarga de movimientos de los archivos maestros y la solicitud periódica de los archivos maestros para actualización.

## Tratamiento de información no determinada

Cuando una propiedad no está explicitada en la fuente oficial, este inventario usa:

- NO DETERMINADO
- NO DOCUMENTADO EN LA FUENTE CONSULTADA

Esto aplica especialmente a cobertura histórica completa, formato exacto del archivo maestro y posiciones de campos no publicadas oficialmente.

## Limitaciones de la investigación

- La página oficial del TSE documenta la descarga de movimientos y la solicitud de archivos maestros, pero no publica el diccionario completo de campos ni los códigos oficiales de movimiento en la página consultada.
- No se localizó diccionario oficial del TSE para ancho fijo ni de códigos de movimiento dentro del repositorio del proyecto ni en la fuente institucional consultada.
- Los archivos maestros no se encontraron físicamente en el repositorio; se documentan como potenciales y no como fuentes accesibles por descarga directa.
- La evidencia técnica local corresponde a DAT-01 y no debe atribuirse a una documentación oficial del TSE si la fuente no lo estipula.

## Relación con DAT-01

DAT-01 verificó localmente la existencia de archivos reales del TSE en el repositorio, concretamente `MOVWEBNAC.txt`, `MOVWEBMAT.txt` y `MOVWEBDEF.txt`, con longitudes comprobadas de 281, 328 y 191 caracteres. Esa evidencia técnica valida el formato y la estructura de la muestra local, pero no sustituye la documentación oficial del TSE.

FUE-02 no modifica DAT-01 ni procesa los archivos RAW. La tarea se limita a documentar la fuente oficial y su rol dentro del TFG.

## Relación con el objetivo específico 1 del TFG

El objetivo específico 1 del TFG prioriza la investigación de fuentes demográficas disponibles en registros oficiales del TSE. La clasificación aquí mantenida se ajusta a ese alcance real: el TSE es la fuente principal y los movimientos del TSE son la entrada RAW seleccionada. No se incorpora INEC porque el proyecto no la utiliza como fuente primaria ni secundaria.

## Evidencia base

La evidencia disponible se conserva en:

- data/raw/tse/
- README.md
- ESTADO_ACTUAL_DAT01.txt
- docs/evidencias/

La matriz principal se guarda en:

- docs/fuentes/matriz_fuentes_oficiales.csv
- docs/fuentes/matriz_fuentes_oficiales.md
