# Matriz de aceptación FUE-04

| Criterio Jira | Estado | Evidencia | Resultado |
|---|---|---|---|
| Nacimientos caracterizados | CUMPLIDO | Perfil FUE-04 y tabla CSV | 31 archivos, 47.705 filas, longitud 281 |
| Matrimonios caracterizados | CUMPLIDO | Perfil FUE-04 y tabla CSV | 31 archivos, 20.546 filas, longitud 328 |
| Defunciones caracterizadas | CUMPLIDO | Perfil FUE-04 y tabla CSV | 31 archivos, 18.719 filas, longitud 191 |
| Fechas diferenciadas | CUMPLIDO CON LIMITACIÓN | Perfil FUE-04 | El período ZIP es publicación; suceso, marginal y aplicación no están documentadas |
| Faltantes cuantificados | CUMPLIDO CON LIMITACIÓN | Perfil FUE-04 | No cuantificables por campo: no existen posiciones oficialmente documentadas o configuradas |
| Inconsistencias cuantificadas | CUMPLIDO | Perfil FUE-04 | 0 filas cortas, largas o vacías en 93 ZIP inspeccionados |
| Riesgos de privacidad documentados | CUMPLIDO | Perfil FUE-04 | Riesgo alto de TXT registrales; perfil sin valores ni líneas RAW |
| Perfil generado | CUMPLIDO | `data/profiles/fue04_profile.json` | Perfil técnico agregado reproducible |
| Tabla de caracterización generada | CUMPLIDO | `docs/fuentes/caracterizacion_acontecimientos.csv` | Comparación de los tres acontecimientos |

## Dictamen

FUE-04 caracteriza la evidencia disponible sin inferir campos, códigos ni fechas internas. Las limitaciones de diccionario oficial se documentan como resultado de la caracterización y preparan, pero no sustituyen, etapas posteriores de transformación.