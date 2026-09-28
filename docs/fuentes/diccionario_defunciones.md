# Diccionario TSE - Defunciones

- ZIP analizados: 31
- Periodo cubierto: febrero-agosto de 2026, con bloques publicados del 01 de febrero al 06 de agosto.
- Cada ZIP contiene exactamente un TXT y un DOCX de definici?n.
- M?todo: lectura de `word/document.xml` dentro del DOCX sin modificar ni extraer permanentemente RAW.
- Firma estructural: `18a8912c3b4fa233`
- Schema drift: ausente; firma equivalente en los 31 ZIP.

| orden | campo | longitud | inicio | fin | tipo | formato | cat?logo/observaciones |
|---:|---|---:|---:|---:|---|---|---|
| 1 | Relleno | 1 | 1 | 1 | NUMÉRICO |  |  |
| 2 | Tipo de Movimiento | 1 | 2 | 2 | NUMÉRICO |  | 1 = Exclusión2 = Cambio3 = Inclusión |
| 3 | Cita de Defunción | 12 | 3 | 14 | NUMÉRICO | FormatoPTTTTFFFAAAAP = ProvinciaT = TomoF = FolioA = Asiento | FormatoPTTTTFFFAAAAP = ProvinciaT = TomoF = FolioA = Asiento |
| 4 | Cédula | 20 | 15 | 34 | alfaNUMÉRICO |  |  |
| 5 | Relleno | 1 | 35 | 35 | NUMÉRICO |  |  |
| 6 | Fecha | 8 | 36 | 43 | NUMÉRICO | fORMATODDMMAAAA | fORMATODDMMAAAA |
| 7 | Nombre | 50 | 44 | 93 | ALFANUMÉRICO |  |  |
| 8 | Primer Apellido | 26 | 94 | 119 | ALFANUMÉRICO |  |  |
| 9 | Segundo Apellido | 26 | 120 | 145 | ALFANUMÉRICO |  |  |
| 10 | Nombre (Conocido como) | 20 | 146 | 165 | ALFANUMÉRICO |  |  |
| 11 | Primer apellido (conocido como) | 13 | 166 | 178 | ALFANUMÉRICO |  |  |
| 12 | Segundo apellido (Conocido como) | 13 | 179 | 191 | alfanumérico |  |  |

- Suma total documentada: **191**.
- Longitud observada del TXT asociado: **[191]** en los 31 ZIP.
- Conclusi?n: la suma documentada coincide exactamente con la longitud observada y no se detecta drift estructural.
