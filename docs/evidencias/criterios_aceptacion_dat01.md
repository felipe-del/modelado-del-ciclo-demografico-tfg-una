# Matriz de aceptación DAT-01

| Criterio Jira | Estado | Implementación | Evidencia |
|---|---|---|---|
| Abrir ZIP | CUMPLIDO | `archive_reader.open_source` abre ZIP sin extracción permanente | Tres ZIP reales procesados por `verify-dat01` |
| Localizar TXT | CUMPLIDO | Selecciona automáticamente miembros `.txt` e ignora auxiliares | `MOVWEBNAC.txt`, `MOVWEBMAT.txt`, `MOVWEBDEF.txt` |
| Verificar longitud | CUMPLIDO | Validación contra el esquema JSON | 281, 328 y 191 caracteres |
| Reportar filas | CUMPLIDO | `ImportSummary` y salida CLI | Evidencias JSON y SQLite |
| Reportar inclusiones | BLOQUEADO POR DICCIONARIO | Clasificador y campo configurables; códigos reales no disponibles | `NO CONFIGURADO`, valor SQLite `NULL` |
| Reportar cambios | BLOQUEADO POR DICCIONARIO | Clasificador y códigos configurables | `NO CONFIGURADO`, valor SQLite `NULL` |
| Reportar exclusiones | BLOQUEADO POR DICCIONARIO | Clasificador y códigos configurables | `NO CONFIGURADO`, valor SQLite `NULL` |
| Reportar errores | CUMPLIDO | Validación de longitud, estructura y campos | `import_issues` y contadores de error |
| No guardar nombres | CUMPLIDO | SQLite solo define metadatos técnicos | Prueba de privacidad y `schema.sql` |
| No guardar cédulas | CUMPLIDO | No existen columnas ni valores RAW | Prueba de privacidad |
| SQLite | CUMPLIDO | `import_runs` e `import_issues` con consultas parametrizadas | `data/db/imports.sqlite` |
| README | CUMPLIDO | Documenta alcance, uso, privacidad y limitaciones | `README.md` |
| Pruebas | CUMPLIDO | Suite sintética de pytest | `python -m pytest -v` |
| Ejecución real | CUMPLIDO | Orquestador procesa las tres muestras conocidas | `python -m tfg_demografia verify-dat01` |

## Dictamen

DAT-01 está técnicamente implementada. El conteo real de inclusiones, cambios y exclusiones permanece bloqueado hasta disponer de documentación oficial del TSE que defina posición y códigos. No se infieren valores desde registros reales.


# [SECURITY] Auditar privilegios de Keycloak y relacionarlos con endpoints del backend

## Descripción

Realizar una revisión completa de los privilegios, roles y permisos configurados actualmente en **Keycloak**, con el objetivo de identificar qué funcionalidad habilita cada uno dentro del backend y establecer una relación clara entre cada permiso y los endpoints protegidos por este.

Actualmente es necesario contar con una trazabilidad precisa entre:

**Permiso / privilegio en Keycloak → Endpoint(s) del backend → Acción que permite realizar**

Como parte de esta revisión, también se deberán identificar los permisos existentes en Keycloak que no cuenten con una descripción clara y agregar una descripción funcional que permita entender fácilmente qué acceso otorgan.

## Objetivo

Contar con un inventario actualizado y documentado de todos los permisos utilizados por la aplicación, evitando permisos ambiguos, duplicados, sin uso o sin una relación claramente identificada con el backend.

## Alcance

- Revisar todos los privilegios, permisos y roles configurados en Keycloak relacionados con el sistema.
- Identificar en el backend todos los endpoints que requieren permisos de Keycloak.
- Determinar qué permiso o privilegio habilita el acceso a cada endpoint.
- Identificar endpoints protegidos que no tengan una relación clara con un permiso.
- Identificar permisos existentes en Keycloak que actualmente no sean utilizados por ningún endpoint.
- Identificar posibles permisos duplicados, obsoletos o inconsistentes.
- Revisar la nomenclatura utilizada para los permisos.
- Agregar descripción en Keycloak a todos los permisos que actualmente no tengan una descripción.
- Validar que la descripción explique claramente la acción o funcionalidad habilitada.
- Generar una matriz de relación entre permisos y endpoints.

## Matriz esperada

La revisión debe dejar documentada, como mínimo, la siguiente información:

| Permiso Keycloak | Descripción | Microservicio | Método HTTP | Endpoint | Acción habilitada | Estado |
|---|---|---|---|---|---|---|
| `ejemplo_read` | Permite consultar información de ejemplo | `msvc-ejemplo` | GET | `/api/ejemplo` | Consultar registros | En uso |
| `ejemplo_create` | Permite crear registros de ejemplo | `msvc-ejemplo` | POST | `/api/ejemplo` | Crear registros | En uso |
| `ejemplo_old` | Permiso legado sin referencias actuales | N/A | N/A | N/A | N/A | Sin uso |

## Validaciones a realizar

Durante la revisión se deberá validar especialmente:

- Que cada endpoint protegido tenga identificado su permiso correspondiente.
- Que los permisos utilizados en anotaciones, filtros o configuraciones del backend existan realmente en Keycloak.
- Que no existan diferencias de nombres entre backend y Keycloak.
- Que los permisos tengan una descripción comprensible.
- Que los permisos no utilizados sean identificados antes de considerar su eliminación.
- Que no existan endpoints sensibles sin protección de permisos cuando deberían tenerla.
- Que permisos demasiado generales sean identificados para revisión.
- Que los métodos HTTP asociados al mismo recurso tengan los permisos correctos según la operación realizada.

## Ejemplo de descripción de permisos

En caso de encontrar permisos sin descripción, agregar una descripción siguiendo una estructura uniforme.

Ejemplos:

- `documento_read`: Permite consultar documentos registrados en el sistema.
- `documento_create`: Permite registrar nuevos documentos.
- `documento_update`: Permite modificar documentos existentes.
- `documento_delete`: Permite eliminar documentos.
- `inventory_read`: Permite consultar información del inventario.
- `maintenance_manage`: Permite administrar procesos de mantenimiento.

Las descripciones deben indicar claramente **qué acción permite realizar el privilegio**, evitando textos genéricos como:

- "Permiso de documentos"
- "Acceso a módulo"
- "Permiso general"

## Entregables

- [ ] Inventario completo de permisos existentes en Keycloak.
- [ ] Relación de cada permiso con su(s) endpoint(s) correspondiente(s).
- [ ] Identificación del microservicio al que pertenece cada endpoint.
- [ ] Método HTTP asociado a cada endpoint.
- [ ] Descripción funcional de cada permiso.
- [ ] Descripciones agregadas en Keycloak para permisos que actualmente no tengan.
- [ ] Listado de permisos sin uso identificado.
- [ ] Listado de endpoints sin permiso identificado, si existen.
- [ ] Listado de inconsistencias encontradas entre Keycloak y backend.
- [ ] Matriz final de permisos vs endpoints documentada.

## Criterios de aceptación

- [ ] Se revisaron todos los permisos y privilegios configurados en Keycloak relacionados con el sistema.
- [ ] Todos los endpoints protegidos del backend fueron revisados.
- [ ] Cada endpoint protegido tiene identificado el permiso que controla su acceso.
- [ ] Cada permiso utilizado tiene identificado al menos un endpoint, salvo aquellos marcados explícitamente como "sin uso".
- [ ] Los permisos sin descripción fueron actualizados en Keycloak.
- [ ] Las descripciones agregadas indican claramente la funcionalidad habilitada.
- [ ] Se identificaron y documentaron permisos sin uso.
- [ ] Se identificaron y documentaron endpoints sin una protección o permiso claramente definido.
- [ ] Se documentaron inconsistencias de nomenclatura entre Keycloak y backend.
- [ ] Se generó una matriz final de trazabilidad entre permisos y endpoints.
- [ ] La revisión no modifica permisos o accesos existentes sin antes validar su impacto.

## Consideraciones

Este issue tiene inicialmente un alcance de **auditoría, documentación y normalización de descripciones**.

La eliminación, modificación o consolidación de permisos existentes deberá realizarse únicamente después de verificar que dichos cambios no afecten usuarios, roles, clientes o integraciones actualmente activas.

Cualquier permiso identificado como obsoleto, duplicado o sin uso deberá quedar documentado para su posterior evaluación.