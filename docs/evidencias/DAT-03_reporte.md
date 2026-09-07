# DAT-03 - Reporte de limpieza y normalización

## Estado

DAT-03 implementa una capa separada de transformación reproducible. Parte de ZIP/TXT mediante lectura de solo lectura, valida la longitud con los esquemas existentes y escribe JSONL en `data/work/normalized/`. No modifica `data/raw/` ni `data/work/extracted/`.

## Reglas

Los tres esquemas actuales no tienen campos configurados (`fields: []`) y los movimientos no están configurados. Por ello:

- Regla activa: validación estructural y conservación de registros válidos como objetos JSON sin campos semánticos.
- Fechas internas: `BLOQUEADA_POR_DOCUMENTACION`.
- Categorías y códigos: `BLOQUEADA_POR_DOCUMENTACION`.
- Unidades: `BLOQUEADA_POR_DOCUMENTACION`.
- Nombres y tipos semánticos: `NO_CONFIGURADA`.

No se inventan columnas ni posiciones. No se convierten códigos a enteros y no se eliminan ceros iniciales.

## Ejecución

Comando:

```powershell
python -m tfg_demografia normalize --source <ZIP-o-TXT> --dataset <dataset> --dry-run
```

Sin `--dry-run`, la salida se escribe en `data/work/normalized/<dataset>/<dataset>.jsonl` y la bitácora en `data/manifests/transformation_log.csv`.

La bitácora registra `run_id`, hashes SHA-256 de fuente, miembro, reglas y salida, conteos evaluados/normalizados/fallidos, excepciones, estado y timestamp. No registra líneas, nombres, cédulas ni valores RAW.

## Ceros, nulos y excepciones

Los campos declarados como texto conservan su representación, incluidos ceros iniciales. No se convierten automáticamente `""`, `"0"`, `"0000"` o `"999"` en nulos. Las operaciones de fecha, catálogo y tipo solo se ejecutan cuando están declaradas; sus errores se cuentan sin escribir el valor problemático.

## Limitaciones

La salida actual no es un dataset semántico utilizable porque falta el diccionario oficial TSE. Es una estructura normalizada vacía y trazable, deliberadamente limitada. DAT-03 no implementa anonimización final, reconstrucción de movimientos, agregación mensual, series, modelado ni web.

## Tecnologías

Python y biblioteca estándar: lectura, transformación declarativa, JSONL, CSV, hashes y CLI. `pytest`: pruebas sintéticas y regresión. SHA-256: trazabilidad de entrada, reglas y salida. Git/GitHub: versionado de código, configuración y evidencia.

## Relación con Producto 2

DAT-03 constituye la primera capa reproducible del dataset procesado. Producto 2 todavía requiere resolver documentación semántica y aplicar posteriormente las tareas de anonimización y reconstrucción que no pertenecen a DAT-03.
