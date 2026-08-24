import json
import sqlite3
import zipfile
from pathlib import Path

import pytest

from tfg_demografia.errors import ArchiveError, SchemaError
from tfg_demografia.ingestion.archive_reader import open_source
from tfg_demografia.ingestion.fixed_width_reader import extract_field
from tfg_demografia.ingestion.movement_classifier import classify
from tfg_demografia.ingestion.processor import process
from tfg_demografia.models import FieldSpec, Movement, Schema
from tfg_demografia.persistence.sqlite import connect, history, save_summary
from tfg_demografia.schema_loader import load_schema


def schema(length=10, configured=False):
    return Schema("sintetico", "1.0", length, "utf-8", {"configured": configured, "field": "movement", "inclusion": ["I"], "change": ["C"], "exclusion": ["E"]}, (FieldSpec("movement", 1, 1),))


def test_txt_zip_subfolder_and_hashes(tmp_path):
    path = tmp_path / "sample.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("folder/MOVWEB.txt", "I         \n")
    content = open_source(path)
    assert content.member_name == "folder/MOVWEB.txt"
    assert len(content.source_sha256) == 64


def test_archive_errors(tmp_path):
    with pytest.raises(ArchiveError):
        open_source(tmp_path / "missing.zip")
    invalid = tmp_path / "bad.zip"
    invalid.write_bytes(b"not zip")
    with pytest.raises(ArchiveError):
        open_source(invalid)
    empty = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty, "w") as archive:
        archive.writestr("readme.docx", b"x")
    with pytest.raises(ArchiveError):
        open_source(empty)


def test_fixed_width_preserves_spaces_and_validation(tmp_path):
    source = tmp_path / "records.txt"
    source.write_text("I         \nshort\n" + "E         \n", encoding="utf-8")
    summary = process(source, schema(10, True))
    assert summary.total_rows == 3
    assert summary.valid_rows == 2
    assert summary.invalid_rows == 1
    assert summary.length_errors == 1
    assert summary.inclusions == 1
    assert summary.exclusions == 1
    assert "short" not in json.dumps(summary.issues)
    assert extract_field("  I       ", FieldSpec("x", 1, 3)) == "  I"


def test_movement_states():
    configured = schema(10, True)
    assert classify("I         ", configured) == Movement.INCLUSION
    assert classify("C         ", configured) == Movement.CHANGE
    assert classify("E         ", configured) == Movement.EXCLUSION
    assert classify("X         ", configured) == Movement.UNKNOWN
    assert classify("I         ", schema()) == Movement.NOT_CONFIGURED


def test_strict_mode_and_documented_movement_shape(tmp_path):
    source = tmp_path / "records.txt"
    source.write_text("I         \n", encoding="utf-8")
    configured_path = tmp_path / "configured.json"
    configured_path.write_text(json.dumps({"dataset": "sintetico", "schema_version": "1.0", "expected_record_length": 10, "encoding": "utf-8", "movement": {"configured": True, "field": {"name": "movement", "start": 1, "end": 1}, "codes": {"inclusion_codes": ["I"], "change_codes": ["C"], "exclusion_codes": ["E"]}}, "fields": []}), encoding="utf-8")
    configured = load_schema(configured_path)
    assert classify("I         ", configured) == Movement.INCLUSION
    strict = process(source, Schema("sintetico", "1.0", 10, "utf-8", {"configured": False}, ()), require_movement_config=True)
    assert strict.status == "INCOMPLETE_CONFIG"
    assert strict.inclusions is None
    assert strict.changes is None
    assert strict.exclusions is None


def test_schema_validation_and_real_lengths():
    root = Path(__file__).parents[1] / "src/tfg_demografia/schemas"
    assert load_schema(root / "nacimientos.json").expected_record_length == 281
    assert load_schema(root / "matrimonios.json").expected_record_length == 328
    assert load_schema(root / "defunciones.json").expected_record_length == 191
    bad = root.parent / "bad-schema.json"
    bad.write_text(json.dumps({"expected_record_length": 2}), encoding="utf-8")
    try:
        with pytest.raises(SchemaError):
            load_schema(bad)
    finally:
        bad.unlink()


def test_sqlite_has_summary_only_and_history(tmp_path):
    database_path = tmp_path / "imports.sqlite"
    summary = process(tmp_path / "record.txt", schema()) if False else None
    connection = connect(database_path)
    from datetime import datetime, timezone
    from tfg_demografia.models import ImportSummary
    summary = ImportSummary("sintetico", "1.0", "sample.zip", "MOVWEB.txt", "a" * 64, "b" * 64, datetime.now(timezone.utc).isoformat(), 10, total_rows=1)
    save_summary(connection, summary)
    assert len(history(connection)) == 1
    columns = {row[1] for row in connection.execute("PRAGMA table_info(import_runs)")}
    columns |= {row[1] for row in connection.execute("PRAGMA table_info(import_issues)")}
    forbidden = {"nombre", "apellido", "cedula", "identificacion", "raw_line", "raw_value"}
    assert not columns & forbidden
    connection.close()