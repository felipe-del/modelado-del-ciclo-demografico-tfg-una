# Modelado del ciclo demográfico

Trabajo Final de Graduación de la Universidad Nacional de Costa Rica sobre nacimientos, matrimonios y defunciones de Costa Rica.

## DAT-01 — Estado de implementación

DAT-01 implementa la primera etapa RAW: abre ZIP del TSE directamente, localiza el TXT, calcula hashes SHA-256, valida registros de ancho fijo y guarda únicamente un resumen técnico en SQLite. No reconstruye la capa canónica ni interpreta acontecimientos individuales.

Las longitudes verificadas son nacimientos `281`, matrimonios `328` y defunciones `191`. La fecha del nombre del ZIP representa el periodo del movimiento, no necesariamente la fecha del acontecimiento.

## Arquitectura

`src/tfg_demografia/` separa modelos, carga de esquemas, lectura de archivos, validación, clasificación configurable, procesamiento y persistencia SQLite. Los tres JSON en `schemas/` contienen ahora los layouts documentados por los DOCX internos TSE, con versiones `NAC-S01`, `MAT-S01` y `DEF-S01`.

Los ZIP originales de `data/raw/tse/` permanecen intactos. `data/db/imports.sqlite` contiene `import_runs` e `import_issues`; no existen columnas para nombres, apellidos, cédulas, identificaciones, líneas RAW o valores RAW. Las incidencias se limitan a 100 por ejecución y no incluyen el valor problemático.

## Instalación en Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

Si PowerShell bloquea la activación, ejecute `Set-ExecutionPolicy -Scope Process Bypass` en esa terminal.

## Uso

```powershell
python -m tfg_demografia read --source "data/raw/tse/nacimientos/movimientos/2026/08_agosto/01_06/nac_agosto2026_01_06.zip" --dataset nacimientos --db data/db/imports.sqlite
python -m tfg_demografia read --source "data/raw/tse/matrimonios/movimientos/2026/08_agosto/01_06/mat_agosto2026_01_06.zip" --dataset matrimonios --db data/db/imports.sqlite
python -m tfg_demografia read --source "data/raw/tse/defunciones/movimientos/2026/08_agosto/01_06/def_agosto2026_01_06.zip" --dataset defunciones --db data/db/imports.sqlite
python -m tfg_demografia history --db data/db/imports.sqlite
python -m pytest -q
```

También se acepta un TXT directo para desarrollo y pruebas. Agregue `--json` para evidencia reproducible. `--require-movement-config` marca la ejecución como `INCOMPLETE_CONFIG` mientras no exista evidencia oficial de la posición y códigos de movimiento.

La verificación final de las tres muestras conocidas se ejecuta con:

```powershell
python -m tfg_demografia verify-dat01
```

Este comando orquesta la lectura existente, muestra conteos, comprueba el esquema SQLite y verifica que Git no reporte modificaciones bajo `data/raw/tse/`. La evidencia de aceptación está en `docs/evidencias/criterios_aceptacion_dat01.md`.

Cada ZIP TSE incluye un DOCX de definición leído desde `word/document.xml`. La evidencia versionada está en `docs/fuentes/diccionario_*.md` y `data/manifests/tse_schema_registry.csv`. Cada esquema configura `movement.field` y los códigos respaldados por esos DOCX.

## Clasificación de movimientos

Los DOCX internos documentan Tipo de Movimiento: `1 = Exclusión`, `2 = Cambio`, `3 = Inclusión`. El motor soporta `INCLUSION`, `CHANGE`, `EXCLUSION` y `UNKNOWN`; la configuración ya está materializada, aunque la verificación real mantiene incidencias de fechas no documentadas como relleno.

## DAT-02 — Descarga, extracción e inspección

DAT-02 amplía DAT-01 en la capa `FUENTE -> RAW -> INGESTA -> INSPECCIÓN`. El comando `sync-tse` descubre enlaces ZIP desde la página oficial del TSE mediante sus atributos `href`, filtrando los patrones `nac_*.zip`, `mat_*.zip` y `def_*.zip`. También permite procesar solo el inventario RAW local con `--local-only`.

Los ZIP originales se conservan bajo `data/raw/tse/`; los TXT se extraen exclusivamente en `data/work/extracted/tse/<dataset>/<nombre-del-zip>/`, directorio ignorado por Git. La extracción rechaza rutas absolutas y traversal. Un ZIP ya existente no se sobrescribe; si el mismo nombre aparece en el manifiesto con otro hash se registra `HASH_CONFLICT`.

La inspección detecta BOM, intenta UTF-8 estricto y usa la codificación del esquema como respaldo. Registra hashes, período derivado del nombre, estadísticas de longitud y estados, sin almacenar registros ni valores RAW. El manifiesto CSV idempotente se genera en `data/manifests/tse_manifest.csv` y el reporte derivado en `docs/evidencias/DAT-02_reporte.md`.

```powershell
python -m tfg_demografia sync-tse --dry-run
python -m tfg_demografia sync-tse --local-only
python -m tfg_demografia sync-tse --dataset nacimientos --local-only
```

DAT-02 no reconstruye registros, no interpreta códigos de movimiento y no genera un dataset analítico o anonimizado definitivo.

## FUE-04 — Caracterización de fuentes seleccionadas

`profile-sources` genera un perfil agregado desde el manifiesto DAT-02 y los esquemas técnicos, sin leer ni almacenar valores individuales. Documenta por acontecimiento la cobertura de publicación, periodicidad observada, codificación, longitudes, inconsistencias estructurales y riesgos de privacidad.

```powershell
python -m tfg_demografia profile-sources
python -m tfg_demografia profile-sources --dataset nacimientos
```

Genera `data/profiles/fue04_profile.json`, `docs/fuentes/caracterizacion_acontecimientos.csv` y `docs/fuentes/perfil_datos_tse.md`. Las posiciones, tipos, fechas y catálogos documentados por ZIP se encuentran en los diccionarios TSE; territorialidad, faltantes por campo y significado temporal definitivo siguen limitados.

## Alcance y privacidad

RAW conserva las fuentes originales. DAT-01 solo produce conteos, metadatos de trazabilidad, hashes, estados e incidencias técnicas seguras. La capa canónica, anonimización analítica, PostgreSQL, API, frontend y pronósticos pertenecen a etapas posteriores.

## Evidencia Jira

Para capturar la salida, ejecute `python -m tfg_demografia verify-dat01` en una terminal maximizada. La base SQLite se genera automáticamente. No copie registros ni contenido de los TXT a documentación o logs.

**Autor:** Isaac Felipe Brenes Calderón  
**Carrera:** Ingeniería en Sistemas de Información con énfasis en Sistemas Web  
**Universidad Nacional de Costa Rica**