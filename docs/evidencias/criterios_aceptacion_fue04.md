# Matriz de aceptación FUE-04

| Criterio Jira | Estado | Evidencia | Resultado |
|---|---|---|---|
| Nacimientos caracterizados | CUMPLIDO | Perfil FUE-04 y tabla CSV | 31 archivos, 47.705 filas, longitud 281 |
| Matrimonios caracterizados | CUMPLIDO | Perfil FUE-04 y tabla CSV | 31 archivos, 20.546 filas, longitud 328 |
| Defunciones caracterizadas | CUMPLIDO | Perfil FUE-04 y tabla CSV | 31 archivos, 18.719 filas, longitud 191 |
| Fechas diferenciadas | CUMPLIDO CON LIMITACIÓN | DOCX internos y diccionarios TSE | Las fechas y formatos están documentados; su uso como fecha definitiva de serie sigue pendiente |
| Faltantes cuantificados | PENDIENTE | Perfil FUE-04 y schemas | La estructura está documentada, pero faltantes por campo requieren validación semántica |
| Inconsistencias cuantificadas | CUMPLIDO | Perfil FUE-04 | 0 filas cortas, largas o vacías en 93 ZIP inspeccionados |
| Riesgos de privacidad documentados | CUMPLIDO | Perfil FUE-04 | Riesgo alto de TXT registrales; perfil sin valores ni líneas RAW |
| Perfil generado | CUMPLIDO | `data/profiles/fue04_profile.json` | Perfil técnico agregado reproducible |
| Tabla de caracterización generada | CUMPLIDO | `docs/fuentes/caracterizacion_acontecimientos.csv` | Comparación de los tres acontecimientos |

## Dictamen

FUE-04 caracteriza la evidencia disponible usando los DOCX internos de los 93 ZIP. Documenta campos, posiciones, tipos, códigos y fechas sin inferir valores; la validación semántica completa y la reconstrucción permanecen fuera de la tarea.