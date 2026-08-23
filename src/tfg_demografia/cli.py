import argparse
import json
from pathlib import Path

from .errors import TSEError
from .ingestion.processor import process
from .persistence.sqlite import connect, history, save_summary
from .schema_loader import load_schema

ROOT = Path(__file__).resolve().parent


def format_summary(summary) -> str:
    movement = lambda value: "NO CONFIGURADO" if value is None else str(value)
    return "\n".join(["=" * 66, "DAT-01 | IMPORTACION DE MOVIMIENTOS TSE", "=" * 66, f"Dataset             : {summary.dataset}", f"Archivo fuente      : {summary.source_file}", f"TXT procesado       : {summary.source_member}", f"SHA-256 ZIP         : {summary.source_sha256}", f"SHA-256 TXT         : {summary.member_sha256}", f"Esquema             : {summary.schema_version}", f"Longitud esperada   : {summary.expected_length}", "-" * 66, f"Filas totales       : {summary.total_rows}", f"Filas validas       : {summary.valid_rows}", f"Filas invalidas     : {summary.invalid_rows}", "-" * 66, f"Inclusiones         : {movement(summary.inclusions)}", f"Cambios             : {movement(summary.changes)}", f"Exclusiones         : {movement(summary.exclusions)}", f"No reconocidos      : {summary.unknown_movements}", "-" * 66, f"Errores longitud    : {summary.length_errors}", f"Errores estructura  : {summary.structural_errors}", f"Errores de campos   : {summary.field_errors}", f"Estado              : {summary.status}", "=" * 66])


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
    args = parser.parse_args()
    try:
        if args.command == "read":
            summary = process(args.source, load_schema(ROOT / "schemas" / f"{args.dataset}.json"), args.require_movement_config)
            with connect(args.db) as database:
                save_summary(database, summary)
            print(json.dumps(summary.__dict__, ensure_ascii=False, indent=2) if args.json else format_summary(summary))
        else:
            with connect(args.db) as database:
                rows = [dict(row) for row in history(database)]
            print(json.dumps(rows, ensure_ascii=False, indent=2) if args.json else "\n".join(f"{row['id']}: {row['dataset']} {row['status']} {row['total_rows']} filas" for row in rows))
    except TSEError as exc:
        parser.error(str(exc))