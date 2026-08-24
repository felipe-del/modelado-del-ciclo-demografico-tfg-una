# Estándar de mensajes de commit

Este proyecto utiliza una convención basada en **Conventional Commits**, adaptada al idioma español y al contexto del TFG. Este estándar se aplica a todos los commits futuros del repositorio. El objetivo es que cada commit explique con claridad qué cambió, por qué cambió y cómo fue validado, para facilitar el historial del proyecto y permitir identificar rápidamente el alcance de cada modificación.

## Formato general

```text
<tipo>(<alcance>): <resumen breve>

<explicación detallada del cambio>

<referencias o notas adicionales>
```

Ejemplo:

```text
feat(dat-01): implementar lector seguro de movimientos TSE

Agrega lectura directa de archivos ZIP y TXT, validación de registros
con ancho fijo y persistencia del resumen técnico en SQLite.

La implementación no almacena líneas RAW ni datos personales.
```

## Reglas obligatorias

1. Escribir el mensaje en español.
2. Usar el formato `tipo(alcance): resumen`.
3. Escribir el resumen en una sola línea.
4. Mantener el resumen preferiblemente por debajo de 72 caracteres.
5. Usar verbos en infinitivo en el resumen: `agregar`, `corregir`, `documentar`, `actualizar`, `refactorizar`.
6. Explicar en el cuerpo qué se modificó, cuál fue el motivo y cuál es el efecto esperado.
7. Mencionar pruebas ejecutadas cuando el cambio incluya código.
8. Mencionar limitaciones o decisiones metodológicas relevantes.
9. No incluir nombres, cédulas, líneas RAW, secretos, tokens ni datos personales.
10. No usar mensajes genéricos como `cambios`, `arreglos`, `update` o `final`.
11. No mezclar cambios no relacionados en un mismo commit cuando puedan separarse razonablemente.
12. No incluir información que no pueda comprobarse en el repositorio.

## Tipos permitidos

### `feat`

Nueva funcionalidad visible o capacidad nueva del sistema.

```text
feat(dat-01): agregar lectura directa de archivos ZIP del TSE
```

### `fix`

Corrección de un comportamiento incorrecto o un error.

```text
fix(validator): corregir validación de registros truncados
```

### `docs`

Cambios únicamente en documentación.

```text
docs(dat-01): documentar ejecución y evidencias de SQLite
```

### `test`

Agregar, modificar o corregir pruebas sin cambiar la funcionalidad principal.

```text
test(ingestion): cubrir ZIP sin archivo TXT
```

### `refactor`

Reorganización interna sin cambiar el comportamiento esperado.

```text
refactor(persistence): separar conexión y guardado de resúmenes
```

### `perf`

Mejora de rendimiento que conserva el comportamiento.

```text
perf(archive-reader): reducir copias de contenido durante la lectura
```

### `build`

Cambios en empaquetado, dependencias o configuración de construcción.

```text
build(project): configurar instalación editable con pyproject.toml
```

### `ci`

Cambios en integración continua, automatizaciones o validaciones del repositorio.

```text
ci(tests): ejecutar pytest en cada cambio del proyecto
```

### `chore`

Tareas de mantenimiento que no modifican directamente la funcionalidad.

```text
chore(repo): actualizar reglas de archivos ignorados
```

### `revert`

Revertir un commit anterior. Debe indicar qué commit se revierte y el motivo.

```text
revert(dat-01): revertir cambio incompatible en esquemas
```

## Alcances recomendados

El alcance debe indicar el módulo, área o tarea afectada. Usar minúsculas y guiones cuando sea necesario.

- `dat-01`: lector inicial y validación del TSE.
- `archive-reader`: lectura de ZIP y TXT.
- `schema`: esquemas JSON y configuración de campos.
- `validator`: validación estructural y de campos.
- `movement`: clasificación de movimientos registrales.
- `processor`: coordinación del procesamiento.
- `persistence`: SQLite, historial e incidencias.
- `cli`: comandos de terminal y salida.
- `tests`: pruebas automatizadas.
- `docs`: documentación y evidencias.
- `repo`: configuración general del repositorio.

Si el cambio afecta varias áreas estrechamente relacionadas, usar el alcance de mayor nivel, por ejemplo `dat-01` o `project`.

## Cómo escribir el resumen

El resumen debe expresar la acción principal y su objeto.

Usar:

```text
feat(cli): agregar salida JSON para evidencias
fix(schema): validar rangos fuera de la longitud del registro
docs(dat-01): actualizar resultados de las muestras reales
test(sqlite): comprobar ausencia de columnas personales
```

Evitar:

```text
cambios varios
arreglo
update
se hicieron pruebas
final
```

## Cómo escribir el cuerpo

El cuerpo debe responder, de forma breve, estas preguntas:

- ¿Qué se cambió?
- ¿Por qué era necesario?
- ¿Qué comportamiento queda disponible?
- ¿Qué decisión o limitación debe conocer quien revise el commit?

Ejemplo:

```text
feat(movement): preparar clasificación configurable de movimientos

Permite configurar el campo y los códigos de inclusión, cambio y exclusión
mediante JSON. Mantiene UNKNOWN para códigos no reconocidos y
NOT_CONFIGURED cuando no existe evidencia oficial.

No se infieren códigos a partir de registros reales.

Pruebas: 7 passed.
```

## Pruebas en el commit

Cuando se cambie código, agregar al cuerpo una línea con las validaciones realizadas:

```text
Pruebas: python -m compileall -q src tests
Pruebas: python -m pytest -v (7 passed)
```

Si no fue posible ejecutar una prueba, indicarlo claramente:

```text
Pruebas: no ejecutadas; el cambio corresponde únicamente a documentación.
```

No afirmar que una prueba pasó si no fue ejecutada.

## Referencias a Jira

Cuando el commit corresponda a una tarea Jira, incluir la clave en el alcance o en el cuerpo. La clave debe conservar su formato oficial.

```text
feat(dat-01): agregar resumen técnico de importaciones TSE

Implementa la persistencia del resumen requerido por DAT-01.

Jira: DAT-01
```

Si el equipo utiliza una automatización que cierra tareas, usarla únicamente cuando exista autorización y el flujo del equipo lo requiera. Para este proyecto se recomienda referenciar la tarea sin cerrarla automáticamente desde el mensaje.

## Cambios incompatibles

Si un cambio rompe una interfaz, formato o comportamiento que otros componentes utilizan, agregar `!` después del alcance y explicar el impacto:

```text
refactor(schema)!: cambiar estructura de configuración de movimientos

La configuración anterior deja de ser válida y debe migrarse al nuevo formato.
```

## Commits pequeños y enfocados

Un commit debe representar una unidad lógica revisable. Ejemplos:

- código y sus pruebas relacionadas;
- documentación de una funcionalidad ya implementada;
- configuración del proyecto;
- corrección específica de validación.

Evitar incluir en el mismo commit una nueva funcionalidad, una reorganización masiva, cambios de formato y archivos no relacionados.

## Plantilla recomendada

```text
<tipo>(<alcance>): <acción concreta>

Qué se modificó:
- ...

Por qué se modificó:
- ...

Consideraciones o limitaciones:
- ...

Pruebas:
- ...

Jira: <CLAVE>
```

## Ejemplo completo para DAT-01

```text
feat(dat-01): implementar lector seguro de movimientos TSE

Agrega lectura directa de ZIP y TXT, validación de registros de ancho fijo,
generación de hashes SHA-256 y persistencia del resumen técnico en SQLite.

Incluye soporte para nacimientos, matrimonios y defunciones con longitudes
esperadas de 281, 328 y 191 caracteres. No almacena nombres, cédulas,
identificaciones ni líneas RAW.

La clasificación de inclusiones, cambios y exclusiones permanece no
configurada porque no existe un diccionario oficial en el repositorio.

Pruebas: python -m pytest -v (7 passed).
Pruebas reales: tres ZIP del TSE procesados correctamente.

Jira: DAT-01
```
