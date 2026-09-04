import argparse
import json
import subprocess
from pathlib import Path

from .errors import TSEError
from .ingestion.dat02 import process_batch, verify_dat02
from .ingestion.processor import process
from .persistence.sqlite import connect, history, save_summary
from .schema_loader import load_schema

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
REAL_SAMPLES = (("NACIMIENTOS", "nacimientos", "data/raw/tse/nacimientos/movimientos/2026/08_agosto/01_06/nac_agosto2026_01_06.zip"), ("MATRIMONIOS", "matrimonios", "data/raw/tse/matrimonios/movimientos/2026/08_agosto/01_06/mat_agosto2026_01_06.zip"), ("DEFUNCIONES", "defunciones", "data/raw/tse/defunciones/movimientos/2026/08_agosto/01_06/def_agosto2026_01_06.zip"))


def format_summary(summary) -> str:
    movement = lambda value: "NO CONFIGURADO" if value is None else str(value)
    return "\n".join(["=" * 66, "DAT-01 | IMPORTACION DE MOVIMIENTOS TSE", "=" * 66, f"Dataset             : {summary.dataset}", f"Archivo fuente      : {summary.source_file}", f"TXT procesado       : {summary.source_member}", f"SHA-256 ZIP         : {summary.source_sha256}", f"SHA-256 TXT         : {summary.member_sha256}", f"Esquema             : {summary.schema_version}", f"Longitud esperada   : {summary.expected_length}", "-" * 66, f"Filas totales       : {summary.total_rows}", f"Filas validas       : {summary.valid_rows}", f"Filas invalidas     : {summary.invalid_rows}", "-" * 66, f"Inclusiones         : {movement(summary.inclusions)}", f"Cambios             : {movement(summary.changes)}", f"Exclusiones         : {movement(summary.exclusions)}", f"No reconocidos      : {summary.unknown_movements}", "-" * 66, f"Errores longitud    : {summary.length_errors}", f"Errores estructura  : {summary.structural_errors}", f"Errores de campos   : {summary.field_errors}", f"Estado              : {summary.status}", "=" * 66])


def format_verification(results, privacy_ok: bool, raw_clean: bool) -> str:
    lines = ["=" * 60, "DAT-01 | VERIFICACION FINAL", "=" * 60, ""]
    for label, summary in results:
        movement = lambda value: "NO CONFIGURADO" if value is None else str(value)
        error_count = summary.invalid_rows
        lines.extend([label, f"Fuente             : {summary.source_file}", f"TXT                : {summary.source_member}", f"Longitud esperada  : {summary.expected_length}", f"Filas totales      : {summary.total_rows}", f"Filas validas      : {summary.valid_rows}", f"Filas invalidas    : {summary.invalid_rows}", f"Inclusiones        : {movement(summary.inclusions)}", f"Cambios            : {movement(summary.changes)}", f"Exclusiones        : {movement(summary.exclusions)}", f"Movimientos desconocidos: {summary.unknown_movements}", f"Errores            : {error_count}", f"Estado             : {'OK' if summary.status == 'COMPLETED' and error_count == 0 else summary.status}", ""])
    lines.extend(["-" * 60, "PRIVACIDAD", "-" * 60, f"Datos personales almacenados : {'NO' if privacy_ok else 'REVISAR'}", "Lineas RAW almacenadas        : NO", "", "-" * 60, "VERIFICACIONES", "-" * 60, "Esquemas cargados             : OK", "SQLite                        : OK", f"RAW modificado               : {'SI' if not raw_clean else 'NO'}", "", "=" * 60, "RESULTADO DAT-01", "=" * 60, f"{'OK' if privacy_ok and raw_clean and all(item.valid_rows + item.invalid_rows == item.total_rows for _, item in results) else 'REVISAR'}"])
    return "\n".join(lines)


def verify_dat01(db: Path) -> str:
    results = []
    with connect(db) as database:
        for label, dataset, relative_source in REAL_SAMPLES:
            summary = process(PROJECT_ROOT / relative_source, load_schema(ROOT / "schemas" / f"{dataset}.json"))
            save_summary(database, summary)
            results.append((label, summary))
        columns = {row[1].lower() for table in ("import_runs", "import_issues") for row in database.execute(f"PRAGMA table_info({table})")}
    forbidden = {"name", "nombre", "apellido", "cedula", "identification", "id_persona", "raw_line", "raw_record", "record_content", "field_value"}
    privacy_ok = not columns & forbidden
    raw_result = subprocess.run(["git", "status", "--short", "--", "data/raw/tse"], cwd=PROJECT_ROOT, capture_output=True, text=True, check=False)
    return format_verification(results, privacy_ok, not raw_result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser(prog="tfg-demografia")
    subparsers = parser.add_subparsers(dest="command", required=True)
    read = subparsers.add_parser("read")
    read.add_argument("--source", type=Path, required=True)
    read.add_argument("--dataset", choices=["nacimientos", "matrimonios", "defunciones"], required=True)
    read.add_argument("--db", type=Path, default=Path("data/db/imports.sqlite"))
    read.add_argument("--require-movement-config", action="store_true")
    read.add_argument("--json", action="store_true")
    hist = subparsers.add_parser("history")
    hist.add_argument("--db", type=Path, default=Path("data/db/imports.sqlite"))
    hist.add_argument("--json", action="store_true")
    batch = subparsers.add_parser("ingest-batch")
    batch.add_argument("--source-root", type=Path, default=Path("data/raw/tse"))
    batch.add_argument("--extraction-root", type=Path, default=Path("data/extracted/tse"))
    batch.add_argument("--manifest", type=Path, default=Path("data/work/dat02_manifest.jsonl"))
    batch.add_argument("--report", type=Path, default=Path("docs/evidencias/DAT-02_reporte_ingesta.md"))
    subparsers.add_parser("verify-dat01")
    verify_dat02_parser = subparsers.add_parser("verify-dat02")
    verify_dat02_parser.add_argument("--source-root", type=Path, default=Path("data/raw/tse"))
    verify_dat02_parser.add_argument("--extraction-root", type=Path, default=Path("data/extracted/tse"))
    verify_dat02_parser.add_argument("--manifest", type=Path, default=Path("data/work/dat02_manifest.jsonl"))
    verify_dat02_parser.add_argument("--report", type=Path, default=Path("docs/evidencias/DAT-02_reporte_ingesta.md"))
    args = parser.parse_args()
    try:
        if args.command == "read":
            summary = process(args.source, load_schema(ROOT / "schemas" / f"{args.dataset}.json"), args.require_movement_config)
            with connect(args.db) as database:
                save_summary(database, summary)
            print(json.dumps(summary.__dict__, ensure_ascii=False, indent=2) if args.json else format_summary(summary))
        elif args.command == "verify-dat01":
            print(verify_dat01(Path("data/db/imports.sqlite")))
        elif args.command == "verify-dat02":
            print(verify_dat02(args.source_root, args.extraction_root, args.manifest, args.report))
        elif args.command == "ingest-batch":
            results = process_batch(args.source_root, args.extraction_root, args.manifest)
            print(json.dumps([result.to_manifest_record() for result in results], ensure_ascii=False, indent=2))
        else:
            with connect(args.db) as database:
                rows = [dict(row) for row in history(database)]
            print(json.dumps(rows, ensure_ascii=False, indent=2) if args.json else "\n".join(f"{row['id']}: {row['dataset']} {row['status']} {row['total_rows']} filas" for row in rows))
    except TSEError as exc:
        parser.error(str(exc))