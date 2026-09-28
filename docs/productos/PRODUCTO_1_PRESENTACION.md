# Producto 1 - Guía profesional de presentación

## 1. Qué es el Producto 1

Es el informe académico que identifica, evalúa y selecciona fuentes oficiales para el estudio del ciclo demográfico de nacimientos, matrimonios y defunciones. Su resultado es una caracterización documental y técnica verificable, no un dataset analítico final.

## 2. Problema que resuelve

Establece qué fuente puede sostener el TFG, qué cobertura existe, cómo están estructurados los archivos, qué calidad estructural presentan, qué riesgos de privacidad contienen y qué límites deben respetarse antes de procesar o modelar.

## 3. Fuente utilizada

La fuente primaria es el Tribunal Supremo de Elecciones mediante sus movimientos publicados en ZIP. Se analizaron 93 ZIP: 31 de nacimientos, 31 de matrimonios y 31 de defunciones. INEC se conserva como referencia contextual, no como fuente RAW ni como relleno.

## 4. Metodología

El flujo fue:

```text
TSE -> ZIP RAW -> inventario -> hashes -> TXT + DOCX
    -> word/document.xml -> diccionario -> fixed-width
    -> validación -> schema fingerprint -> schema drift
    -> caracterización -> selección
```

Cada ZIP contiene un TXT y un DOCX. El DOCX se leyó como Office Open XML desde `word/document.xml`. Las longitudes se acumularon para calcular posiciones 1-based y se verificaron contra el TXT asociado. Las estructuras se agruparon mediante firmas normalizadas.

## 5. Tecnologías

- Python y biblioteca estándar.
- ZIP.
- Office Open XML y `word/document.xml`.
- SHA-256.
- JSON y CSV.
- Markdown.
- pytest.
- Git/GitHub.

## 6. Implementación

Los documentos DOCX aportaron la estructura de 26 campos de nacimientos, 16 de matrimonios y 12 de defunciones. Las longitudes son 281, 328 y 191. Se documentaron Tipo de Movimiento y sus códigos: 1 exclusión, 2 cambio y 3 inclusión. También se documentaron fechas y formatos.

La firma estructural resultó estable en los 31 ZIP de cada dataset. No se detectó schema drift en el corte febrero-agosto de 2026. Los hashes de ZIP, TXT y DOCX se registraron por período.

## 7. Resultados

- Cobertura común de publicación: 2026-02-01 a 2026-08-06.
- 31 ZIP por dataset.
- Cero filas cortas, largas o vacías en el lote inspeccionado.
- Tres schemas estructurales estables: `NAC-S01`, `MAT-S01`, `DEF-S01`.
- PII directa e indirecta identificada sin reproducir valores.
- Selección de los tres acontecimientos con alcance inicial nacional agregado.
- Frecuencia mensual propuesta para etapas posteriores, no construida en este producto.

## 8. Evidencias

- [Informe principal](producto1_informe_analisis_fuentes.md): conclusión académica.
- [Auditoría TSE](../evidencias/TSE_schema_audit.md): inspección de 93 ZIP y drift.
- [Registry de schemas](../../data/manifests/tse_schema_registry.csv): hashes y versiones por ZIP.
- [Diccionario de nacimientos](../fuentes/diccionario_nacimientos.md): layout completo.
- [Diccionario de matrimonios](../fuentes/diccionario_matrimonios.md): layout completo.
- [Diccionario de defunciones](../fuentes/diccionario_defunciones.md): layout completo.
- [Manifiesto TSE](../../data/manifests/tse_manifest.csv): inventario y calidad estructural.
- [Perfil de datos](../fuentes/perfil_datos_tse.md): caracterización agregada y privacidad.
- [Matriz de cierre](PRODUCTO_1_CIERRE.md): criterios y estado final.

## 9. Limitaciones

El análisis no demuestra cobertura histórica completa, no incluye un maestro inicial, no define la regla operativa para aplicar cambios y exclusiones, no construye una serie temporal ni ejecuta anonimización final. Esas son dependencias de etapas posteriores, principalmente Producto 2 y tareas posteriores.

No existe en el repositorio evidencia primaria verificable del envío de la consulta al TSE ni el Documento 18 completo. Estas ausencias se declaran, pero no invalidan la caracterización de fuentes realizada.

## 10. Conclusión

El TSE es una fuente primaria técnicamente caracterizada para el alcance del TFG. Los 93 ZIP y sus DOCX internos permiten verificar procedencia, estructura, cobertura, calidad estructural, privacidad, selección y límites metodológicos. Producto 1 queda cerrado como informe de análisis de fuentes.

## Demostración sugerida

1. Abrir [producto1_informe_analisis_fuentes.md](producto1_informe_analisis_fuentes.md) y mostrar propósito, alcance y conclusión.
2. Abrir [TSE_schema_audit.md](../evidencias/TSE_schema_audit.md) para demostrar los 93 ZIP, las firmas y la ausencia de drift.
3. Abrir un diccionario TSE para mostrar campos, longitudes y posiciones fixed-width.
4. Abrir [tse_schema_registry.csv](../../data/manifests/tse_schema_registry.csv) y mostrar hashes y versiones por período.
5. Abrir [tse_manifest.csv](../../data/manifests/tse_manifest.csv) para mostrar cobertura, filas y calidad estructural.
6. Mostrar [perfil_datos_tse.md](../fuentes/perfil_datos_tse.md) para explicar privacidad y límites semánticos.
7. Mostrar [PRODUCTO_1_CIERRE.md](PRODUCTO_1_CIERRE.md) y explicar que las dependencias de maestro, reconstrucción y anonimización pertenecen a etapas posteriores.
8. Como comprobación técnica opcional, ejecutar `python -m pytest -q` y mostrar la evidencia reproducible disponible, sin imprimir líneas RAW.
