# DOC-03 - Resumen del informe de analisis de fuentes

## Producto

**Producto 1: Informe de analisis de fuentes demograficas.**

El informe responde al Objetivo Especifico 1 mediante la integracion documental de FUE-02, FUE-03, FUE-04, FUE-05, DAT-01 y DAT-02. FUE-01 y el Documento 18 completo no fueron localizados como artefactos independientes en el repositorio y se registran como limitaciones de trazabilidad.

## Resultado principal

El TSE queda definido como fuente primaria RAW para movimientos de nacimientos, matrimonios y defunciones. Los tres acontecimientos se seleccionan **CON LIMITACION** porque comparten fuente, cobertura de publicacion comun, continuidad aparente y calidad estructural verificable.

La **COBERTURA DE PUBLICACION COMUN VERIFICADA** es 2026-02-01 a 2026-08-06. No se interpreta como periodo historico de ocurrencia. El alcance inicial es nacional agregado. La frecuencia analitica mensual es una propuesta condicionada a una futura capa canonica; no se ha construido una serie mensual en DOC-03.

## Resultados tecnicos

- Nacimientos: 31 archivos, 47.705 filas, longitud 281.
- Matrimonios: 31 archivos, 20.546 filas, longitud 328.
- Defunciones: 31 archivos, 18.719 filas, longitud 191.
- Cero filas cortas, largas o vacias en los tres acontecimientos.
- 0 huecos aparentes dentro de los bloques disponibles; existen bloques parciales.
- Codificacion observada: nacimientos y matrimonios `latin-1`/`utf-8`; defunciones `latin-1`.

## Comparacion TSE-INEC

Los movimientos del TSE son el insumo registral primario del proyecto. El INEC no forma parte del RAW ni se utiliza para completar faltantes; sus publicaciones agregadas se consideran solamente referencia contextual y eventual contraste estadistico. No se afirma que el dataset combine TSE e INEC.

## Limitaciones decisivas

- Los DOCX internos de los 93 ZIP documentan campos, posiciones, tipos, códigos de movimiento y fechas; la calidad semántica completa, faltantes por variable y territorialidad permanecen limitadas.
- Los movimientos no demuestran historia completa desde un estado vacio; FUE-03 establece `REQUIERE_MAESTRO_INICIAL`.
- No se localizo archivo maestro TSE en el repositorio.
- FUE-03 queda como **GESTIÓN DOCUMENTADA / EVIDENCIA PRIMARIA PENDIENTE**: no existe PDF, captura, export de correo ni otro artefacto verificable del envío.

## Artefactos

- `docs/productos/producto1_informe_analisis_fuentes.md`
- `docs/evidencias/DOC-03_resumen.md`
- `docs/evidencias/criterios_aceptacion_doc03.md`

## Estado del Producto 1

**CERRADO.** El informe y la evidencia estructural TSE están consolidados como análisis académico de fuentes. La ausencia de comprobante primario del envío FUE-03, de un artefacto separado de obtención inicial y del Documento 18 completo queda declarada como limitación institucional/documental, no como bloqueo del Producto 1.

## Estado DOC-03

DOC-03 queda documentalmente cumplida con limitaciones: procedencia, estructura, cobertura, calidad, privacidad, seleccion, comparacion TSE-INEC, referencias y trazabilidad estan incorporadas. La calificacion propuesta es **95/100**.

La sincronizacion posterior con Documento 18 deberá incluir objetivo, procedimiento, tablas de fuentes y caracterización, cobertura, comparación TSE-INEC, selección, exclusiones, limitaciones y decisión de alcance. No se editó Documento 18.
