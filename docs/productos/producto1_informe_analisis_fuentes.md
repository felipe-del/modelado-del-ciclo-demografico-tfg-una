# Producto 1 - Informe de analisis de fuentes demograficas

## 1. Introduccion

Este informe presenta el analisis de las fuentes demograficas consideradas para el Trabajo Final de Graduacion **Modelado del ciclo demografico de la poblacion utilizando tecnicas de analitica de datos aplicadas a registros de nacimientos, matrimonios y defunciones**.

El informe responde al Objetivo Especifico 1:

> Investigar las fuentes de datos demograficos disponibles en registros oficiales del TSE, identificando variables relevantes y caracteristicas de los datos necesarios para el estudio del ciclo demografico.

El producto documenta procedencia, estructura, cobertura, calidad, privacidad, comparabilidad, seleccion y limitaciones. No transforma registros, no interpreta posiciones desconocidas y no incorpora lineas RAW.

## 2. Objetivo y alcance

El objetivo es establecer una base documental verificable para seleccionar las fuentes que podran alimentar las etapas posteriores del TFG. El alcance institucional actual utiliza al **Tribunal Supremo de Elecciones (TSE) como unica fuente primaria RAW**.

Las publicaciones del Instituto Nacional de Estadistica y Censos (INEC) se consideran un posible referente contextual o estadistico agregado, pero **no forman parte del RAW, del manifiesto DAT-02 ni de la ingesta del proyecto**. Por tanto, el informe no afirma que el dataset combine TSE e INEC.

El resultado describe la evidencia disponible al corte documentado en el repositorio. La fecha del nombre de un ZIP identifica un bloque de publicacion observado; no prueba la fecha de ocurrencia de un acontecimiento.

## 3. Procedimiento metodologico

El Producto 1 se construyo mediante revision documental y caracterizacion agregada:

| Etapa | Entrada utilizada | Procedimiento y herramienta | Resultado | Limitacion | Evidencia |
|---|---|---|---|---|---|
| FUE-01 | Evidencia inicial del proyecto | Inventario y organizacion inicial | No se localizo un artefacto independiente de FUE-01 en este repositorio | La trazabilidad de FUE-01 depende de documentos posteriores | Estado del repositorio: FUE-01 no localizada |
| FUE-02 | Pagina oficial TSE y matriz de fuentes | Revision documental y clasificacion de movimientos, maestros y documentacion | Inventario institucional TSE | No hay diccionario ni maestro publico disponible | `docs/evidencias/FUE-02_resumen.md`; `docs/fuentes/matriz_fuentes_oficiales.md` |
| FUE-03 | Pagina oficial TSE y consulta documentada | Evaluacion de cobertura historica y relacion maestro/movimientos | Se establece `REQUIERE_MAESTRO_INICIAL` | La evidencia de envio institucional no esta verificable en el repositorio | `docs/evidencias/FUE-03_resumen.md`; `docs/evidencias/FUE-03_aporte_documento18.md` |
| FUE-04 | Manifiesto DAT-02 y esquemas | Perfilado agregado con Python, CSV y Markdown, sin leer valores en el informe | Conteos, longitudes, codificacion, cobertura y riesgos | Semantica de campos y territorialidad no determinada | `docs/evidencias/FUE-04_resumen.md`; `docs/fuentes/perfil_datos_tse.md` |
| FUE-05 | Manifiesto, FUE-04 y matrices | Evaluacion de cobertura, continuidad, calidad y comparabilidad | Seleccion de los tres acontecimientos con limitacion | Frecuencia mensual y ampliacion historica dependen de etapas posteriores | `docs/evidencias/FUE-05_decision_alcance.md`; `docs/fuentes/matriz_seleccion_fue05.md` |
| DAT-01/DAT-02 | ZIP/TXT TSE y metadatos derivados | Validacion de ancho fijo, hashes, codificacion, estados e inspeccion por lote | Evidencia tecnica de integridad estructural y trazabilidad | No demuestra semantica ni historia completa | `docs/evidencias/criterios_aceptacion_dat01.md`; `docs/evidencias/DAT-02_reporte.md` |

El procedimiento evita abrir o imprimir valores RAW con PII. Las conclusiones de este informe se basan en documentos, esquemas y metadatos agregados.

## 4. Tecnologias y herramientas utilizadas

| Herramienta | Uso real en Producto 1 y sus evidencias |
|---|---|
| Sitio oficial TSE | Consulta de la pagina de descarga de movimientos y de la documentacion institucional disponible |
| Python y biblioteca estandar | Lectura segura, validacion, hashes, procesamiento agregado y generacion de perfiles |
| CSV | Manifiestos, matrices de fuentes, caracterizacion y matriz de seleccion |
| Markdown | Informe, reportes, criterios y evidencia versionable |
| SQLite | Almacenamiento de metadatos tecnicos de DAT-01; no almacena lineas RAW en el esquema descrito |
| pytest | Pruebas automatizadas de ingestion, validacion, perfilado y privacidad |
| Git/GitHub | Control de versiones y trazabilidad de documentos y codigo; los TXT RAW estan excluidos |
| Jira | Organizacion de tareas y criterios; los archivos del repositorio son la evidencia principal |

No se presentan como utilizadas en Producto 1 FastAPI, React, PostgreSQL, Pandas, Statsmodels ni otras tecnologias futuras.

## 5. Instituciones y fuentes consideradas

### 5.1 TSE como fuente primaria

La fuente institucional principal es el Tribunal Supremo de Elecciones, mediante su pagina oficial de descarga:

- URL: https://www.tse.go.cr/descarga_movimientos.html
- Mecanismo: descarga directa de ZIP con TXT de ancho fijo.
- Acontecimientos: nacimientos, matrimonios y defunciones.
- Tipo: movimientos de actualizacion publicados por bloques de fechas.
- Rol: fuente primaria RAW del pipeline.

La documentacion revisada diferencia los movimientos de los archivos maestros. La pagina institucional indica que los movimientos se relacionan con la actualizacion de archivos maestros y que los maestros pueden solicitarse institucionalmente si no se realizan actualizaciones semanales.

### 5.2 Archivos maestros potenciales

Se identifican tres fuentes potenciales: archivo maestro de nacimientos, archivo maestro de matrimonios y archivo maestro de defunciones. No se dispone de ellos fisicamente en el repositorio y no se localizo formato, cobertura ni diccionario publico completo. Por eso no se presentan como fuentes disponibles ni se usan para completar el estudio.

### 5.3 INEC como referencia contextual

El INEC puede aportar estadisticas vitales agregadas y contexto institucional, pero no es fuente RAW de este proyecto. No se integro ningun archivo INEC al manifiesto ni al pipeline. La comparacion TSE-INEC se utiliza para delimitar funciones y evitar mezclar registros administrativos con estadisticas agregadas.

Referencia institucional contextual: https://www.inec.cr/

### 5.4 Documento 18 y FUE-01

El Documento 18 completo no fue localizado en el repositorio. Solo se localizo `docs/evidencias/FUE-03_aporte_documento18.md`, que es un aporte documental. Tampoco se localizo un artefacto independiente de FUE-01. Estas ausencias se registran como limitaciones de trazabilidad, no se rellenan con suposiciones.

## 6. Caracterizacion tecnica de las fuentes TSE

### Tabla 1. Fuentes oficiales identificadas

| Fuente | Tipo | Disponibilidad actual | Uso en el TFG |
|---|---|---|---|
| Movimientos de nacimientos TSE | Movimiento registral | Disponible en el lote local verificado | Fuente primaria RAW seleccionada con limitacion |
| Movimientos de matrimonios TSE | Movimiento registral | Disponible en el lote local verificado | Fuente primaria RAW seleccionada con limitacion |
| Movimientos de defunciones TSE | Movimiento registral | Disponible en el lote local verificado | Fuente primaria RAW seleccionada con limitacion |
| Maestros TSE de los tres acontecimientos | Archivo maestro potencial | No disponible fisicamente ni documentado como descarga publica | Excluido del corte; posible incorporacion posterior |
| Pagina oficial de descarga TSE | Documentacion institucional | Disponible | Referencia de procedencia y mecanismo de acceso |
| INEC | Estadistica agregada/contexto | No integrado al pipeline | Contraste contextual eventual; no RAW |

### Tabla 2. Caracterizacion tecnica por acontecimiento

| Acontecimiento | TXT | Patron ZIP | Longitud | Codificacion observada | Archivos | Filas | Filas validas | Cortas | Largas | Vacias |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| Nacimientos | MOVWEBNAC.txt | nac_*.zip | 281 | latin-1; utf-8 | 31 | 47.705 | 47.705 | 0 | 0 | 0 |
| Matrimonios | MOVWEBMAT.txt | mat_*.zip | 328 | latin-1; utf-8 | 31 | 20.546 | 20.546 | 0 | 0 | 0 |
| Defunciones | MOVWEBDEF.txt | def_*.zip | 191 | latin-1 | 31 | 18.719 | 18.719 | 0 | 0 | 0 |

Los archivos se publican como ZIP que contienen TXT de ancho fijo. La longitud observada y la codificacion son propiedades tecnicas verificadas por DAT-01, DAT-02 y FUE-04. No se atribuyen nombres o significados a campos que no esten documentados oficialmente.

## 7. Variables y semantica

Actualmente no estan determinadas de forma verificable:

- fecha del suceso;
- fecha marginal;
- fecha de aplicacion;
- posiciones y nombres de variables territoriales;
- identificadores por campo;
- faltantes por variable;
- codigos de inclusion, cambio y exclusion;
- reglas de aplicacion de movimientos al maestro.

Esta ausencia es una limitacion documentada de la fuente disponible, no un error del perfilado. DAT-01 y FUE-04 validan estructura y metadatos, pero no autorizan inferir semantica observando registros RAW.

## 8. Cobertura y continuidad

La interseccion de los tres acontecimientos es:

**COBERTURA DE PUBLICACION COMUN VERIFICADA: 2026-02-01 a 2026-08-06.**

No debe denominarse periodo historico de los acontecimientos.

### Tabla 3. Cobertura y continuidad

| Acontecimiento | Inicio de publicacion | Fin de publicacion | Bloques | Continuidad | Interpretacion |
|---|---|---|---:|---|---|
| Nacimientos | 2026-02-01 | 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | Publicacion de movimientos, no ocurrencia |
| Matrimonios | 2026-02-01 | 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | Publicacion de movimientos, no ocurrencia |
| Defunciones | 2026-02-01 | 2026-08-06 | 31 | 0 huecos aparentes; bloques parciales | Publicacion de movimientos, no ocurrencia |

La continuidad es aparente dentro del conjunto de bloques disponibles. Fuera del intervalo se registra **SIN ARCHIVO**, no cero acontecimientos. Los bloques parciales se conservan tal como fueron publicados; no se convierten artificialmente en semanas completas.

La cobertura anterior a febrero de 2026 y posterior al corte no se declara porque no esta verificada en el manifiesto utilizado. FUE-03 establece ademas que los movimientos no bastan para afirmar una reconstruccion historica completa desde un estado vacio.

## 9. Calidad de los datos

### 9.1 Calidad estructural evaluada

La calidad estructural demostrada comprende:

- longitud esperada y observada;
- cantidad de archivos y filas;
- filas cortas, largas y vacias;
- codificacion detectada;
- lectura de ZIP/TXT;
- hashes y conflictos;
- continuidad aparente de bloques;
- estados de procesamiento e inspeccion.

En los 93 ZIP revisados no se reportan errores de longitud: los tres acontecimientos presentan cero filas cortas, largas o vacias. DAT-02 registro 93 ZIP, 93 inspecciones, cero conflictos y hashes calculados.

### 9.2 Calidad semantica no evaluada completamente

No se puede evaluar completamente la calidad semantica, faltantes por variable, validez de codigos, duplicidad de personas, consistencia de fechas o validez territorial porque falta el diccionario oficial y la relacion documentada maestro/movimientos. Esta limitacion impide presentar el perfil como validacion sustantiva del Registro Civil.

## 10. Privacidad y riesgos

Los TXT registrales pueden contener informacion identificable. El riesgo pertenece a la fuente RAW y exige minimizar su exposicion. Los perfiles, matrices y reportes utilizados en este producto contienen conteos, hashes, estados, longitudes, fechas de bloques y categorias agregadas; no deben contener lineas RAW ni valores individuales.

La ausencia de PII se afirma aqui solo para los artefactos agregados revisados y no como una certificacion general de todo el historial de GitHub. El informe no publica registros. Los TXT RAW y extraidos permanecen excluidos del control de versiones mediante las reglas del repositorio.

La PII no es necesaria para definir el alcance nacional agregado ni para las decisiones metodologicas de Producto 1. Para fases posteriores se requeriran minimizacion, anonimización y controles de acceso, fuera del alcance de este informe.

## 11. Comparabilidad entre acontecimientos

Los tres acontecimientos son comparables para el alcance inicial porque comparten institución, mecanismo de acceso, intervalo de publicacion, numero de bloques y nivel agregado. La comparabilidad semantica completa queda limitada hasta conocer campos, codigos y fechas internas.

La seleccion no se basa en que los conteos sean iguales. Las diferencias de volumen se conservan como una caracteristica observada y no justifican excluir un acontecimiento relevante para el ciclo demografico.

## 12. Comparacion institucional TSE-INEC

### Tabla 4. Comparacion TSE-INEC

| Criterio | TSE | INEC | Funcion en el TFG |
|---|---|---|---|
| Funcion institucional | Administra y actualiza registros electorales/civiles segun la fuente consultada | Produce estadisticas oficiales y publicaciones estadisticas | Se distingue fuente administrativa de estadistica agregada |
| Tipo de informacion considerada | Movimientos registrales de nacimientos, matrimonios y defunciones | Estadisticas vitales y otros productos agregados publicados | TSE alimenta RAW; INEC puede contextualizar |
| Nivel de agregacion | Registros o movimientos individuales en TXT de ancho fijo | Tablas y publicaciones agregadas, segun producto | No se mezclan niveles sin una decision metodologica adicional |
| Publicacion | ZIP/TXT por bloques de fechas en la pagina oficial TSE | Publicaciones y bases estadisticas institucionales | Solo el mecanismo TSE esta integrado al pipeline actual |
| Uso actual | Fuente primaria RAW seleccionada | No integrado como RAW ni como relleno | Contraste contextual eventual, no combinacion de datasets |
| Valor metodologico | Trazabilidad hacia movimientos registrales y estudio del flujo de actualizaciones | Contexto y contraste de magnitudes agregadas | Funciones complementarias, no competencia |
| Limitacion | Falta diccionario completo, maestro inicial y semantica verificable | No representa el mismo nivel ni necesariamente la misma definicion operativa | No usar INEC para completar faltantes TSE |

La comparacion no pretende establecer superioridad entre instituciones. TSE e INEC cumplen funciones diferentes. Los movimientos del TSE constituyen el insumo registral primario del proyecto, mientras que las publicaciones agregadas del INEC se consideran referencia contextual y eventual contraste estadistico.

## 13. Frecuencia analitica

Se separan tres frecuencias:

1. **Frecuencia de publicacion:** el TSE publica movimientos por bloques periodicos, descritos en la documentacion revisada como actualizacion semanal por bloques de fechas.
2. **Frecuencia de procesamiento:** depende de cada ejecucion del pipeline DAT-02 sobre los archivos disponibles.
3. **Frecuencia analitica:** mensual, como propuesta condicionada para una futura capa canonica valida.

La frecuencia mensual no es una serie ya construida y este informe no agrega registros. Se propone porque proporciona una unidad comun entre acontecimientos, reduce la irregularidad de los bloques y puede servir para estudiar estacionalidad y pronostico. La decision debe revisarse cuando se conozcan fechas internas, reglas de movimiento y cobertura historica.

## 14. Nivel territorial

El alcance inicial es **nacional agregado**. Esta es una decision metodologica conservadora y reproducible: permite trabajar con el total de cada acontecimiento sin inventar posiciones, nombres o codigos territoriales.

Provincia, canton y distrito quedan pendientes del diccionario oficial, la identificacion verificable de las variables y la evaluacion de la estabilidad de sus codigos. No se presentan como ausencias del fenomeno, sino como dimensiones no interpretables con la evidencia actual.

## 15. Criterios de seleccion y decision de alcance

### Tabla 5. Matriz de seleccion final

| Acontecimiento | Decision | Disponibilidad | Calidad estructural | Continuidad | Comparabilidad | Relevancia |
|---|---|---|---|---|---|---|
| Nacimientos | SELECCIONADO CON LIMITACION | 31 ZIP disponibles | 281; 47.705 filas validas; cero errores | 0 huecos aparentes; bloques parciales | Comun con los otros dos en fuente, intervalo y nivel agregado | Componente fundamental del ciclo demografico |
| Matrimonios | SELECCIONADO CON LIMITACION | 31 ZIP disponibles | 328; 20.546 filas validas; cero errores | 0 huecos aparentes; bloques parciales | Comun con los otros dos en fuente, intervalo y nivel agregado | Componente demografico relevante |
| Defunciones | SELECCIONADO CON LIMITACION | 31 ZIP disponibles | 191; 18.719 filas validas; cero errores | 0 huecos aparentes; bloques parciales | Comun con los otros dos en fuente, intervalo y nivel agregado | Componente fundamental del ciclo demografico |

La decision definitiva de FUE-05 es seleccionar los tres movimientos TSE con las limitaciones indicadas. El alcance temporal comun se limita a la **COBERTURA DE PUBLICACION COMUN VERIFICADA** de 2026-02-01 a 2026-08-06. El alcance nacional agregado es inicial y no autoriza analisis subnacional.

## 16. Exclusiones y no ampliacion artificial

| Elemento excluido | Motivo | Consecuencia metodologica |
|---|---|---|
| Periodos anteriores a 2026-02-01 | No verificados en el manifiesto actual | No se afirma historia anterior |
| Periodos posteriores a 2026-08-06 | Fuera del corte documentado | No se anticipa cobertura futura |
| Archivos maestros | No disponibles fisicamente ni documentados en formato completo | No se reconstruye un estado registral completo |
| Variables y codigos no documentados | No hay posiciones ni diccionario oficial verificable | No se infieren semantica, fechas ni territorialidad |
| Provincia, canton y distrito | Nivel no determinable | Se mantiene alcance nacional agregado |
| PII innecesaria | No es necesaria para el Producto 1 | No se publican valores ni identificadores |
| INEC como relleno | No pertenece al pipeline RAW y tiene otro nivel de agregacion | No se completan movimientos faltantes |
| Observaciones sinteticas | No representan evidencia observada | No se crean fechas, ceros ni duplicados |

El proyecto no rellena periodos faltantes con cero, no extrapola el historico, no usa INEC para completar movimientos, no duplica archivos, no crea observaciones sinteticas y no interpreta ausencia de archivo como ausencia de eventos. Esta regla protege la validez del estudio y evita ampliar artificialmente las series.

## 17. Limitaciones

1. La cobertura disponible es de publicacion de movimientos, no de ocurrencia.
2. Los movimientos no demuestran una historia completa desde un estado vacio.
3. Falta archivo maestro o estado inicial verificable.
4. Falta diccionario oficial de campos, posiciones y codigos.
5. Fechas internas, identificadores, faltantes por variable y territorialidad no estan determinados.
6. La calidad semantica no puede evaluarse completamente.
7. FUE-03 tiene una inconsistencia documental sobre el supuesto envio del correo al TSE; no existe en este repositorio evidencia primaria verificable del envio. Por rigor, el informe la trata como **NO VERIFICADA / PENDIENTE**.
8. No se localizo el Documento 18 completo ni un artefacto independiente de FUE-01.
9. La fecha de procesamiento que aparece en algunos reportes DAT-02 es posterior a la fecha de contexto indicada para esta ejecucion; se conserva como dato del reporte y no se interpreta como fecha de publicacion.
10. La comparacion TSE-INEC es funcional e institucional, no una validacion cuantitativa entre series compatibles.

## 18. Implicaciones para Producto 2 y Producto 3

### Producto 2

El dataset procesado y anonimizado debera mantener el alcance TSE, separar metadatos de registros, documentar la incertidumbre semantica, no incorporar PII innecesaria y no completar ausencias con estadisticas INEC. La construccion de una capa canonica requiere resolver primero la documentacion de campos y la regla maestro/movimientos.

### Producto 3

El modelado temporal podra considerar una frecuencia mensual, pero solo despues de validar la capa canonica y las fechas internas. El periodo inicial no debe presentarse como historia completa ni ampliarse con ceros o extrapolaciones. Los pronosticos deberan declarar el corte y las limitaciones de cobertura.

## 19. Evidencias y trazabilidad

### Tabla 6. Trazabilidad del Producto 1

| Tarea | Aporte | Evidencia | Resultado |
|---|---|---|---|
| FUE-01 | Obtencion y organizacion inicial | No localizado como artefacto independiente | Pendiente de trazabilidad especifica |
| FUE-02 | Inventario y procedencia institucional | `FUE-02_resumen.md`; `matriz_fuentes_oficiales.md/csv` | Movimientos, maestros potenciales y documentacion diferenciados |
| FUE-03 | Cobertura historica y relacion maestro/movimientos | `FUE-03_resumen.md`; `FUE-03_aporte_documento18.md`; consulta documentada | `REQUIERE_MAESTRO_INICIAL`; gestion institucional no verificable en el repositorio |
| FUE-04 | Caracterizacion tecnica agregada | `FUE-04_resumen.md`; perfil; caracterizacion CSV | 93 ZIP, conteos, longitudes, codificacion, continuidad y privacidad |
| FUE-05 | Seleccion y delimitacion metodologica | `FUE-05_decision_alcance.md`; matrices | Tres acontecimientos seleccionados con limitacion; cobertura comun y nivel nacional |
| DAT-01 | Validacion estructural y trazabilidad tecnica | criterios DAT-01; `verify-dat01` | Longitudes, hashes, estados e incidencias sin valores RAW |
| DAT-02 | Ingesta por lote y manifestado | criterios DAT-02; reportes; `tse_manifest.csv` | 93 ZIP inspeccionados y metadatos derivados |

Jira organiza el trabajo, pero la evidencia principal son los artefactos versionados y las verificaciones reproducibles del repositorio.

## 20. Referencias

1. Tribunal Supremo de Elecciones de Costa Rica. **Descarga de movimientos**. https://www.tse.go.cr/descarga_movimientos.html
2. Tribunal Supremo de Elecciones de Costa Rica. `docs/fuentes/matriz_fuentes_oficiales.md` y `docs/fuentes/matriz_fuentes_oficiales.csv`, repositorio del proyecto.
3. Proyecto TFG. `docs/evidencias/FUE-02_resumen.md`, inventario de fuentes oficiales.
4. Proyecto TFG. `docs/evidencias/FUE-03_resumen.md` y `docs/evidencias/FUE-03_aporte_documento18.md`, investigacion de disponibilidad historica.
5. Proyecto TFG. `docs/evidencias/FUE-04_resumen.md` y `docs/fuentes/perfil_datos_tse.md`, caracterizacion agregada.
6. Proyecto TFG. `docs/evidencias/FUE-05_decision_alcance.md` y `docs/fuentes/matriz_seleccion_fue05.md`, decision de seleccion.
7. Proyecto TFG. `data/manifests/tse_manifest.csv`, manifiesto DAT-02.
8. Instituto Nacional de Estadistica y Censos de Costa Rica. Portal institucional, utilizado solo como referencia contextual: https://www.inec.cr/

## 21. Preguntas de defensa

| Pregunta | Respuesta corta | Evidencia |
|---|---|---|
| Por que se eligio el TSE? | Es la fuente institucional primaria disponible para los movimientos registrales definidos en el alcance. | FUE-02; pagina oficial TSE |
| Por que no utilizar INEC como fuente primaria? | Sus publicaciones agregadas no cumplen la misma funcion ni nivel que los movimientos TSE y no estan integradas al RAW. | Seccion 12; README |
| Por que se eligieron los tres acontecimientos? | Son los tres componentes definidos del ciclo demografico y comparten cobertura, fuente y procesamiento verificables. | FUE-04; FUE-05 |
| Por que el periodo empieza en febrero? | Es el inicio comun observado en el manifiesto; no se amplia hacia atras sin evidencia. | `tse_manifest.csv` |
| Por que termina el 6 de agosto? | Es la fecha maxima de publicacion verificada en el corte. | DAT-02; FUE-04 |
| Eso significa que los eventos ocurrieron entre febrero y agosto? | No; solo demuestra cobertura de publicacion de movimientos. | FUE-05; perfil TSE |
| Por que trabajar inicialmente a nivel nacional? | Es el nivel que puede sostenerse sin interpretar campos territoriales desconocidos. | FUE-05 |
| Por que no usar provincia o canton? | No existe diccionario oficial verificable de posiciones y codigos territoriales. | Perfil TSE |
| Por que frecuencia mensual? | Es una propuesta para comparar y modelar posteriormente, no una serie ya agregada. | FUE-05; seccion 13 |
| Como se evaluo la calidad? | Se evaluo estructura, longitud, codificacion, filas, hashes y continuidad aparente; no semantica completa. | DAT-01; DAT-02; FUE-04 |
| Por que no calcular faltantes por variable? | Las posiciones y variables no estan documentadas oficialmente. | Perfil TSE |
| Como se trato la privacidad? | Se evitaron valores individuales y se conservaron metadatos agregados; la fuente RAW mantiene riesgo alto. | DAT-02; FUE-04 |
| Como se sabe que los archivos no fueron alterados? | Se calcularon hashes y se registraron conflictos y estados de integridad. | DAT-01; DAT-02 |
| Por que se necesita un archivo maestro? | La documentacion TSE describe los movimientos como actualizaciones; no se presume historia completa desde cero. | FUE-03 |
| Que limitacion tiene trabajar solo con movimientos? | No permite afirmar cobertura historica completa ni reconstruir sin un estado inicial verificable. | FUE-03 |
| Se recibio respuesta del TSE? | No hay respuesta institucional verificable en el repositorio. | FUE-03 y estado actual del proyecto |
| FUE-03 esta cerrada? | No debe declararse cerrada mientras no exista evidencia primaria verificable de la gestion y su estado sea coherente. | `FUE-03_consulta_TSE.md`; estado actual |
| Que ocurre fuera del intervalo? | Se marca SIN ARCHIVO; no se transforma en cero eventos. | FUE-05 |
| El volumen menor de matrimonios justifica excluirlo? | No; la cantidad de filas no es criterio suficiente para excluir un componente relevante. | FUE-05 |
| Que se sincronizara con Documento 18? | Objetivo, procedimiento, tablas de procedencia, caracterizacion, cobertura, seleccion, limitaciones y decision de alcance. | Este informe; Documento 18 no localizado |

## 22. Sincronizacion posterior con Documento 18

No se modifico Documento 18 porque no se localizo su archivo editable en el repositorio. Cuando exista acceso al documento, deben sincronizarse: el texto del Objetivo Especifico 1 y su respuesta, el procedimiento FUE-01 a FUE-05, las tablas 1 a 6, la distincion TSE-INEC, la cobertura comun como cobertura de publicacion, la decision de alcance nacional, las exclusiones, las limitaciones semanticas y el estado no verificado de FUE-03. La matriz CSV y las referencias deben conservarse como respaldo versionado.

## 23. Conclusiones del Producto 1

La investigación identifica al TSE como fuente primaria RAW para movimientos de nacimientos, matrimonios y defunciones. Los 93 ZIP verificados presentan calidad estructural completa en el corte: 31 por acontecimiento, sin errores de longitud y con cobertura de publicacion comun del 2026-02-01 al 2026-08-06.

La seleccion de los tres acontecimientos es metodologicamente defendible por disponibilidad, continuidad aparente, comparabilidad de fuente y relevancia para el ciclo demografico. Es una seleccion con limitacion: no se han demostrado la semantica de campos, la cobertura historica completa, el nivel territorial ni la suficiencia de los movimientos sin maestro inicial.

El Producto 1 puede considerarse **CASI COMPLETO**, no cerrado, porque el informe y sus matrices estan redactados, pero permanecen pendientes la evidencia primaria de FUE-03, el Documento 18 completo, FUE-01 como artefacto identificable y la documentacion institucional del maestro y del diccionario.
