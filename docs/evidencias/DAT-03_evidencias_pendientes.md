# DAT-03 - Evidencias visuales pendientes

Las capturas deben mostrar únicamente metadatos y fixtures sintéticos, nunca registros RAW.

- [EVIDENCIA DAT03-01] Ejecución de `python -m tfg_demografia normalize --source <fixture> --dataset nacimientos --dry-run`, mostrando conteos, hashes y estado DRY_RUN.
- [EVIDENCIA DAT03-02] Ejecución de `python -m pytest -q tests/test_dat03.py`, mostrando las pruebas de ceros iniciales, excepciones, ZIP y dry-run.
- [EVIDENCIA DAT03-03] Tabla `docs/datos/reglas_transformacion.md` con reglas activas y bloqueadas.
- [EVIDENCIA DAT03-04] Bitácora `data/manifests/transformation_log.csv` mostrando solo hashes, conteos y estados.
- [EVIDENCIA DAT03-05] Comparación agregada de entrada/salida: filas evaluadas, normalizadas, fallidas y hash de salida; no mostrar contenido de filas.
