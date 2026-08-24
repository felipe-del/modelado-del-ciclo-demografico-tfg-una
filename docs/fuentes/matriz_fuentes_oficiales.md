# Inventario de fuentes oficiales del TSE

## TSE

### 1) Movimiento de nacimientos

- Institución: TSE
- Enlace oficial: https://www.tse.go.cr/descarga_movimientos.html
- Formato: ZIP con archivos TXT de ancho fijo; verificado localmente mediante DAT-01
- Cobertura: NO DETERMINADO
- Periodicidad oficial: Semanal por bloques de fechas; la página informa actualización semanal y recomienda solicitar mensualmente los archivos maestros si no se actualizan semanalmente
- Granularidad: Registro individual por movimiento y bloque de fechas
- Mecanismo de acceso: Descarga directa desde la página oficial del TSE
- Rol dentro del TFG: PRIMARIA_RAW
- Observaciones: La página oficial del TSE documenta la descarga de movimientos para nacimientos, matrimonios y defunciones. Evidencia técnica local: DAT-01 verificó `MOVWEBNAC.txt` con longitud 281.

### 2) Movimiento de matrimonios

- Institución: TSE
- Enlace oficial: https://www.tse.go.cr/descarga_movimientos.html
- Formato: ZIP con archivos TXT de ancho fijo; verificado localmente mediante DAT-01
- Cobertura: NO DETERMINADO
- Periodicidad oficial: Semanal por bloques de fechas; la página informa actualización semanal y recomienda solicitar mensualmente los archivos maestros si no se actualizan semanalmente
- Granularidad: Registro individual por movimiento y bloque de fechas
- Mecanismo de acceso: Descarga directa desde la página oficial del TSE
- Rol dentro del TFG: PRIMARIA_RAW
- Observaciones: La página oficial del TSE documenta la descarga de movimientos para nacimientos, matrimonios y defunciones. Evidencia técnica local: DAT-01 verificó `MOVWEBMAT.txt` con longitud 328.

### 3) Movimiento de defunciones

- Institución: TSE
- Enlace oficial: https://www.tse.go.cr/descarga_movimientos.html
- Formato: ZIP con archivos TXT de ancho fijo; verificado localmente mediante DAT-01
- Cobertura: NO DETERMINADO
- Periodicidad oficial: Semanal por bloques de fechas; la página informa actualización semanal y recomienda solicitar mensualmente los archivos maestros si no se actualizan semanalmente
- Granularidad: Registro individual por movimiento y bloque de fechas
- Mecanismo de acceso: Descarga directa desde la página oficial del TSE
- Rol dentro del TFG: PRIMARIA_RAW
- Observaciones: La página oficial del TSE documenta la descarga de movimientos para nacimientos, matrimonios y defunciones. Evidencia técnica local: DAT-01 verificó `MOVWEBDEF.txt` con longitud 191.

### 4) Archivo maestro de nacimientos (potencial)

- Institución: TSE
- Enlace oficial: https://www.tse.go.cr/descarga_movimientos.html
- Formato: NO DOCUMENTADO EN LA FUENTE CONSULTADA
- Cobertura: NO DETERMINADO
- Periodicidad oficial: La página informa que si no se realizan actualizaciones semanales, se recomienda solicitar mensualmente al correo institucional los archivos maestros
- Granularidad: NO DETERMINADO
- Mecanismo de acceso: Solicitud institucional por correo; la página menciona `secretariadtic@tse.go.cr`
- Rol dentro del TFG: PRIMARIA_POTENCIAL
- Observaciones: La página del TSE documenta la solicitud de archivos maestros, pero no se dispone físicamente del archivo maestro en el repositorio ni de su formato exacto publicado públicamente.

### 5) Archivo maestro de matrimonios (potencial)

- Institución: TSE
- Enlace oficial: https://www.tse.go.cr/descarga_movimientos.html
- Formato: NO DOCUMENTADO EN LA FUENTE CONSULTADA
- Cobertura: NO DETERMINADO
- Periodicidad oficial: La página informa que si no se realizan actualizaciones semanales, se recomienda solicitar mensualmente al correo institucional los archivos maestros
- Granularidad: NO DETERMINADO
- Mecanismo de acceso: Solicitud institucional por correo; la página menciona `secretariadtic@tse.go.cr`
- Rol dentro del TFG: PRIMARIA_POTENCIAL
- Observaciones: La página del TSE documenta la solicitud de archivos maestros, pero no se dispone físicamente del archivo maestro en el repositorio ni de su formato exacto publicado públicamente.

### 6) Archivo maestro de defunciones (potencial)

- Institución: TSE
- Enlace oficial: https://www.tse.go.cr/descarga_movimientos.html
- Formato: NO DOCUMENTADO EN LA FUENTE CONSULTADA
- Cobertura: NO DETERMINADO
- Periodicidad oficial: La página informa que si no se realizan actualizaciones semanales, se recomienda solicitar mensualmente al correo institucional los archivos maestros
- Granularidad: NO DETERMINADO
- Mecanismo de acceso: Solicitud institucional por correo; la página menciona `secretariadtic@tse.go.cr`
- Rol dentro del TFG: PRIMARIA_POTENCIAL
- Observaciones: La página del TSE documenta la solicitud de archivos maestros, pero no se dispone físicamente del archivo maestro en el repositorio ni de su formato exacto publicado públicamente.

### 7) Página oficial de descarga de movimientos del TSE

- Institución: TSE
- Enlace oficial: https://www.tse.go.cr/descarga_movimientos.html
- Formato: Web institucional
- Cobertura: Institucional
- Periodicidad oficial: Semanal por bloques de fechas; recomendación de solicitud mensual de archivos maestros si no se actualiza semanalmente
- Granularidad: Documental y operativa
- Mecanismo de acceso: Navegación web institucional y descarga directa de movimientos
- Rol dentro del TFG: DOCUMENTACION
- Observaciones: La página oficial del TSE es la referencia institucional central para la descarga de movimientos y la actualización de archivos maestros. No sustituye la base registral ni la documentación técnica de ancho fijo.

## Evidencia oficial del TSE

- La página oficial https://www.tse.go.cr/descarga_movimientos.html documenta la descarga de movimientos de nacimientos, matrimonios y defunciones.
- La misma página informa que la actualización es semanal por bloques de fechas.
- La página recomienda solicitar mensualmente al correo institucional `secretariadtic@tse.go.cr` los archivos maestros si no se realizan actualizaciones semanales.
- La página oficial es, por tanto, la referencia institucional directa para acceso y actualización de movimientos.

## Evidencia técnica local de DAT-01

- `MOVWEBNAC.txt` verificado localmente con longitud 281.
- `MOVWEBMAT.txt` verificado localmente con longitud 328.
- `MOVWEBDEF.txt` verificado localmente con longitud 191.
- Los ZIP reales de movimientos del TSE fueron procesados en el repositorio sin modificar `data/raw/tse/`.

## Matriz de selección preliminar

| Fuente | Uso potencial en TFG | Selección preliminar | Justificación |
|---|---|---|---|
| TSE — movimientos de nacimientos | RAW / ingestión | SELECCIONADA | La fuente oficial documenta descarga de movimientos y DAT-01 verificó la muestra local. |
| TSE — movimientos de matrimonios | RAW / ingestión | SELECCIONADA | La fuente oficial documenta descarga de movimientos y DAT-01 verificó la muestra local. |
| TSE — movimientos de defunciones | RAW / ingestión | SELECCIONADA | La fuente oficial documenta descarga de movimientos y DAT-01 verificó la muestra local. |
| TSE — archivos maestros | Registro administrativo y contexto | PENDIENTE | La institución informa solicitud por correo, pero no se dispone físicamente de esos archivos en el repositorio. |
| TSE — página oficial de descarga | Documentación institucional | REFERENCIA | Sirve para documentar acceso, periodicidad y mecanismo de actualización. |

## Observación final

El alcance real del TFG utiliza únicamente fuentes oficiales del TSE. La documentación se mantiene en esa lógica y separa claramente la evidencia oficial institucional de la evidencia técnica local generada por DAT-01.
