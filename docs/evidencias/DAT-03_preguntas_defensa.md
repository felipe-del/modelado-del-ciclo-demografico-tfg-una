# DAT-03 - Preguntas de defensa

| Pregunta | Respuesta | Evidencia |
|---|---|---|
| ¿Por qué no se modificó RAW? | RAW es la entrada inmutable para reproducibilidad y trazabilidad. | `normalization.py`; `reglas_transformacion.md` |
| ¿Cómo se preservan ceros iniciales? | Los valores se tratan como texto salvo regla explícita; la prueba sintética conserva `00045`. | `tests/test_dat03.py` |
| ¿Cómo se decide qué transformar? | Solo se ejecutan campos y operaciones declarados en JSON versionado. | `config/transformations/`; `normalization.py` |
| ¿Por qué no se normalizaron fechas internas? | No tienen definición ni formato oficial verificable. | FUE-04; reglas DAT-03 |
| ¿Cómo se registra una excepción? | Se acumula un contador agregado sin escribir el valor que falló. | `NormalizationResult`; bitácora |
| ¿Cómo se evitan correcciones manuales? | No existe edición fila por fila; cada cambio requiere una regla declarativa reproducible. | Reglas DAT-03 |
| ¿Cómo se sabe qué reglas se ejecutaron? | El hash de la configuración se guarda en la bitácora. | `transformation_log.csv` |
| ¿Qué diferencia hay entre limpieza y anonimización? | DAT-03 homogeneiza estructura; DAT-04 deberá minimizar o anonimizar datos. | Alcance DAT-03 |
| ¿Qué diferencia hay entre calidad estructural y semántica? | La primera valida longitud y formato; la segunda requiere diccionario y sigue bloqueada. | FUE-04; DAT-03 |
| ¿Cómo se reproduce una ejecución? | Con la misma entrada, esquema y configuración se obtiene el mismo hash de salida. | `tests/test_dat03.py` |
| ¿Qué ocurre con un código desconocido? | No se mapea sin catálogo; una regla `map` genera una excepción agregada. | `normalization.py` |
| ¿Cómo se comprueba que no cambió indebidamente? | Se comparan hashes de entrada, reglas y salida, además de conteos. | Bitácora |
| ¿Por qué reglas declarativas? | Permiten revisión, versionado y auditoría sin lógica oculta. | Configuración JSON |
| ¿Cómo se relaciona DAT-03 con DAT-04? | DAT-03 prepara transformación; DAT-04 queda fuera y deberá tratar privacidad. | Alcance DAT-03 |
| ¿Cómo se relaciona con Producto 2? | Es la primera capa reproducible del dataset procesado, aún sin reconstrucción ni series. | Evidencia DAT-03 |
