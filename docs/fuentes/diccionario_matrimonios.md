# Diccionario TSE - Matrimonios

- ZIP analizados: 31
- Periodo cubierto: febrero-agosto de 2026, con bloques publicados del 01 de febrero al 06 de agosto.
- Cada ZIP contiene exactamente un TXT y un DOCX de definici?n.
- M?todo: lectura de `word/document.xml` dentro del DOCX sin modificar ni extraer permanentemente RAW.
- Firma estructural: `092fe259301b271e`
- Schema drift: ausente; firma equivalente en los 31 ZIP.

| orden | campo | longitud | inicio | fin | tipo | formato | cat?logo/observaciones |
|---:|---|---:|---:|---:|---|---|---|
| 1 | Tipo de Movimiento | 2 | 1 | 2 | NUMÉRICO |  | 1 = Exclusión2 = Cambio3 = Inclusión |
| 2 | Tipo de Suceso | 1 | 3 | 3 | NUMÉRICO |  | 1= Matrimonio Católico.2 = Matrimonio Civil.3 = Otros. |
| 3 | Cita de Matrimonio | 13 | 4 | 16 | ALFANUMÉRICO | Formato PTTTTFFFAAAARP = Provincia T = TomoF = FolioA = AsientoR = Tipo de Relación donde: 2 = Casado/a 3 = Separado/a 4 = Divorciado/a 5 = Viudo/a | Formato PTTTTFFFAAAARP = Provincia T = TomoF = FolioA = AsientoR = Tipo de Relación donde: 2 = Casado/a 3 = Separado/a 4 = Divorciado/a 5 = Viudo/a |
| 4 | Fecha del Suceso | 8 | 17 | 24 | NUMÉRICO | FormatoAAAAMMDD | FormatoAAAAMMDD |
| 5 | Identificación de la Persona Contrayente 1 | 20 | 25 | 44 | ALFANUMÉRICO |  |  |
| 6 | Relleno | 1 | 45 | 45 | NUMÉRICO |  |  |
| 7 | Identificación de la Persona Contrayente 2 | 20 | 46 | 65 | ALFANUMÉRICO |  |  |
| 8 | Relleno | 1 | 66 | 66 | NUMÉRICO |  |  |
| 9 | Nombre de la Persona Contrayente 1 | 50 | 67 | 116 | ALFANUMÉRICO |  |  |
| 10 | Primer Apellido de la Persona Contrayente 1 | 26 | 117 | 142 | ALFANUMÉRICO |  |  |
| 11 | Segundo Apellido de la Persona Contrayente 1 | 26 | 143 | 168 | ALFANUMÉRICO |  |  |
| 12 | Conocido como de la Persona Contrayente 1 | 29 | 169 | 197 | ALFANUMÉRICO |  |  |
| 13 | Nombre de la Persona Contrayente 2 | 50 | 198 | 247 | ALFANUMÉRICO |  |  |
| 14 | Primer Apellido de la Persona Contrayente 2 | 26 | 248 | 273 | ALFANUMÉRICO |  |  |
| 15 | Segundo Apellido de la Persona Contrayente 2 | 26 | 274 | 299 | ALFANUMÉRICO |  |  |
| 16 | Conocido como de la Persona Contrayente 2 | 29 | 300 | 328 | ALFANUMÉRICO |  |  |

- Suma total documentada: **328**.
- Longitud observada del TXT asociado: **[328]** en los 31 ZIP.
- Conclusi?n: la suma documentada coincide exactamente con la longitud observada y no se detecta drift estructural.
