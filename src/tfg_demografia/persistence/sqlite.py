import sqlite3
from pathlib import Path

from ..models import ImportSummary


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(Path(__file__).with_name("schema.sql").read_text(encoding="utf-8"))
    return connection


def save_summary(connection: sqlite3.Connection, summary: ImportSummary) -> int:
    values = (summary.dataset, summary.schema_version, summary.source_file, summary.source_member, summary.source_sha256, summary.member_sha256, summary.processed_at_utc, summary.expected_length, summary.total_rows, summary.valid_rows, summary.invalid_rows, summary.inclusions, summary.changes, summary.exclusions, summary.unknown_movements, summary.length_errors, summary.structural_errors, summary.field_errors, int(summary.movement_classification_configured), summary.status, summary.notes)
    cursor = connection.execute("INSERT INTO import_runs (dataset,schema_version,source_file,source_member,source_sha256,member_sha256,processed_at_utc,expected_length,total_rows,valid_rows,invalid_rows,inclusions,changes,exclusions,unknown_movements,length_errors,structural_errors,field_errors,movement_classification_configured,status,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", values)
    run_id = cursor.lastrowid
    connection.executemany("INSERT INTO import_issues (import_run_id,line_number,error_code,field_name,message) VALUES (?,?,?,?,?)", [(run_id, item["line_number"], item["error_code"], item["field_name"], item["message"]) for item in summary.issues])
    connection.commit()
    return run_id


def history(connection: sqlite3.Connection):
    connection.row_factory = sqlite3.Row
    return connection.execute("SELECT * FROM import_runs ORDER BY id DESC").fetchall()