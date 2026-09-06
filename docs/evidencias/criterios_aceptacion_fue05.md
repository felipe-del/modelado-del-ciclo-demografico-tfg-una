# Criterios de aceptacion FUE-05

| Criterio Jira | Estado | Decision | Evidencia |
|---|---|---|---|
| Fuentes seleccionadas | CUMPLIDO | Se seleccionan movimientos TSE de nacimientos, matrimonios y defunciones con limitacion semantica | `matriz_seleccion_fue05.csv`; `FUE-05_decision_alcance.md` |
| Periodo comun definido | CUMPLIDO | 2026-02-01 a 2026-08-06 como cobertura de publicacion comun verificada | `tse_manifest.csv`; `caracterizacion_acontecimientos.csv` |
| Frecuencia definida | CUMPLIDO | Ingesta semanal por bloques; procesamiento por ejecucion; analitica mensual propuesta y condicional | `FUE-05_decision_alcance.md` |
| Nivel territorial definido | CUMPLIDO | Nacional agregado para el alcance inicial; subnacional pendiente | `FUE-05_decision_alcance.md`; `perfil_datos_tse.md` |
| Cobertura evaluada | CUMPLIDO | 31 bloques por acontecimiento; misma interseccion temporal | `FUE-04_resumen.md`; `tse_manifest.csv` |
| Calidad evaluada | CUMPLIDO | Cero filas cortas, largas y vacias; longitudes verificadas | `caracterizacion_acontecimientos.csv`; `criterios_aceptacion_dat02.md` |
| Continuidad evaluada | CUMPLIDO CON LIMITACION | 0 huecos aparentes; se conservan bloques parciales y se marca SIN ARCHIVO fuera del rango | `FUE-04_resumen.md`; `matriz_seleccion_fue05.md` |
| Comparabilidad evaluada | CUMPLIDO CON LIMITACION | Comparable en fuente, intervalo y nivel agregado; semantica no evaluada | `matriz_seleccion_fue05.md` |
| Exclusiones justificadas | CUMPLIDO | Se excluyen periodos no verificados, maestros no disponibles, territorios no documentados, INEC como relleno y PII innecesaria | `FUE-05_decision_alcance.md` |
| No ampliacion artificial demostrada | CUMPLIDO | No se rellenan ceros, extrapolan periodos, duplican bloques ni crean observaciones sinteticas | `FUE-05_decision_alcance.md` |
| Matriz generada | CUMPLIDO | CSV y version legible generados | `matriz_seleccion_fue05.csv`; `matriz_seleccion_fue05.md` |
| Decision de alcance generada | CUMPLIDO | Alcance, dependencias, limitaciones y estados formalizados | `FUE-05_decision_alcance.md` |

## Calificacion

**95/100.** FUE-05 queda documentalmente completa para el corte actual. Se reservan 5 puntos por dependencias externas no resueltas: diccionario oficial, semantica de fechas y movimientos, variables territoriales y archivo maestro o estado inicial para sostener una cobertura historica completa.

## Limitaciones de la calificacion

La calificacion no implica que los movimientos representen todos los acontecimientos ocurridos en Costa Rica ni que las fechas de los nombres ZIP sean fechas de ocurrencia. Solo evalua el cumplimiento documental y metodologico de la seleccion con la evidencia disponible.
