# Diccionario TSE - Nacimientos

- ZIP analizados: 31
- Periodo cubierto: febrero-agosto de 2026, con bloques publicados del 01 de febrero al 06 de agosto.
- Cada ZIP contiene exactamente un TXT y un DOCX de definici?n.
- M?todo: lectura de `word/document.xml` dentro del DOCX sin modificar ni extraer permanentemente RAW.
- Firma estructural: `445ae4c469e6ba2b`
- Schema drift: ausente; firma equivalente en los 31 ZIP.

| orden | campo | longitud | inicio | fin | tipo | formato | cat?logo/observaciones |
|---:|---|---:|---:|---:|---|---|---|
| 1 | Cita de Nacimiento | 12 | 1 | 12 | Numérico | Formato PTTTTFFFAAAAP = Provincia T = Tomo F = FolioA = Asiento | Formato PTTTTFFFAAAAP = Provincia T = Tomo F = FolioA = Asiento |
| 2 | Cédula del Progenitor/a 1 | 9 | 13 | 21 | Numérico |  |  |
| 3 | Cédula del Progenitor/a 2 | 9 | 22 | 30 | Numérico |  |  |
| 4 | Código de Hospital | 3 | 31 | 33 | Numérico |  |  |
| 5 | Hora del Suceso | 4 | 34 | 37 | Numérico |  |  |
| 6 | Fecha del Suceso | 8 | 38 | 45 | Numérico | Formato AAAAMMDD | Formato AAAAMMDD |
| 7 | Relleno | 1 | 46 | 46 | Numérico |  |  |
| 8 | Relleno | 2 | 47 | 48 | Numérico |  |  |
| 9 | Nacionalidad del Hijo | 1 | 49 | 49 | Numérico |  | 0 = Costarricense1 = Por Opción2 = Naturalizado3 = No indica nacionalidad4 = Conserva nacionalidad extranjera 5 = Conserva nacionalidad costarricense |
| 10 | Marca de Defunción | 1 | 50 | 50 | Numérico |  | 0 = No tiene defunción1 = Tiene Defunción |
| 11 | País del Progenitor/a 1 | 3 | 51 | 53 | Numérico |  |  |
| 12 | País del Progenitor/a 2 | 3 | 54 | 56 | Numérico |  |  |
| 13 | Indicador de Advertencia | 1 | 57 | 57 | Numérico |  |  |
| 14 | Primer Apellido | 26 | 58 | 83 | Alfanumérico |  |  |
| 15 | Segundo Apellido | 26 | 84 | 109 | Alfanumérico |  |  |
| 16 | Nombre | 50 | 110 | 159 | Alfanumérico |  |  |
| 17 | Nombre del Progenitor/a 1 | 29 | 160 | 188 | Alfanumérico |  |  |
| 18 | Nombre del Progenitor/a 2 | 29 | 189 | 217 | Alfanumérico |  |  |
| 19 | Lugar de Nacimiento | 29 | 218 | 246 | Alfanumérico |  |  |
| 20 | Tipo de Movimiento | 1 | 247 | 247 | Numérico |  | 1 = Exclusión2 = Cambio3 = Inclusión |
| 21 | Fecha de Marginal | 8 | 248 | 255 | Numérico | Formato AAAAMMDD | Formato AAAAMMDD |
| 22 | Hora de Marginal | 6 | 256 | 261 | Numérico |  |  |
| 23 | Fecha de Naturalización | 8 | 262 | 269 | Numérico | Formato AAAAMMDD | Formato AAAAMMDD |
| 24 | Indicador de extensión | 1 | 270 | 270 | Numérico |  |  |
| 25 | Provincia y Cantón de Procedencia del Progenitor/a 2 | 3 | 271 | 273 | Numérico |  |  |
| 26 | Fecha de Aplicación | 8 | 274 | 281 | NUMERICO | Formato AAAAMMDD | Formato AAAAMMDD |

- Suma total documentada: **281**.
- Longitud observada del TXT asociado: **[281]** en los 31 ZIP.
- Conclusi?n: la suma documentada coincide exactamente con la longitud observada y no se detecta drift estructural.
