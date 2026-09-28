import json
import zipfile
from pathlib import Path

from tfg_demografia.models import FieldSpec, Schema
from tfg_demografia.normalization import append_log, normalize_source, transform_record
from tfg_demografia.schema_loader import load_schema
from tfg_demografia.ingestion.movement_classifier import classify
from tfg_demografia.models import Movement
from tfg_demografia.ingestion.validator import validate


def schema_with_code():
    return Schema("nacimientos", "test", 5, "latin-1", {"configured": False}, (FieldSpec("codigo", 1, 5, type="text"),))


def test_transform_preserves_leading_zero_and_normalizes_name():
    rules = {"dataset": "nacimientos", "fields": [{"name": "codigo", "normalized_name": "codigo_origen", "operations": ["strip"]}]}
    assert transform_record("00045", schema_with_code(), rules) == {"codigo_origen": "00045"}


def test_transform_supports_explicit_date_and_catalog_and_rejects_unknown_catalog():
    schema = Schema("nacimientos", "test", 8, "latin-1", {"configured": False}, (FieldSpec("fecha", 1, 8),))
    rules = {"dataset": "nacimientos", "fields": [{"name": "fecha", "operations": ["date_dmy"]}]}
    assert transform_record("01022026", schema, rules) == {"fecha": "2026-02-01"}
    bad = {"dataset": "nacimientos", "fields": [{"name": "fecha", "operations": ["map"], "catalog": {"A": "activo"}}]}
    try:
        transform_record("B       ", Schema("nacimientos", "test", 8, "latin-1", {}, (FieldSpec("fecha", 1, 8),)), bad)
    except ValueError as error:
        assert str(error) == "VALUE_NOT_IN_CATALOG"
    else:
        raise AssertionError("un codigo fuera del catalogo debe generar una excepcion controlada")


def test_real_schemas_have_documented_layouts_and_movement_codes():
    root = Path(__file__).parents[1] / "src/tfg_demografia/schemas"
    expected = {"nacimientos": (281, 247, 247), "matrimonios": (328, 1, 2), "defunciones": (191, 2, 2)}
    for dataset, (length, movement_start, movement_end) in expected.items():
        schema = load_schema(root / f"{dataset}.json")
        assert sum(field.end - field.start + 1 for field in schema.fields) == length
        movement = next(field for field in schema.fields if field.name == "Tipo de Movimiento")
        assert (movement.start, movement.end) == (movement_start, movement_end)
        def record(code):
            return " " * (movement_start - 1) + code.ljust(movement_end - movement_start + 1) + " " * (length - movement_end)
        assert classify(record("3"), schema) == Movement.INCLUSION
        assert classify(record("2"), schema) == Movement.CHANGE
        assert classify(record("1"), schema) == Movement.EXCLUSION


def test_documented_date_formats_are_supported():
    ymd = Schema("nacimientos", "test", 8, "latin-1", {}, (FieldSpec("fecha", 1, 8, type="date", format="AAAAMMDD"),))
    dmy = Schema("defunciones", "test", 8, "latin-1", {}, (FieldSpec("fecha", 1, 8, type="date", format="DDMMAAAA"),))
    assert transform_record("20260201", ymd, {"fields": [{"name": "fecha", "operations": ["date_ymd"]}]}) == {"fecha": "2026-02-01"}
    assert transform_record("01022026", dmy, {"fields": [{"name": "fecha", "operations": ["date_dmy"]}]}) == {"fecha": "2026-02-01"}


def test_real_schema_catalogs_accept_documented_values_and_reject_unknown_values():
    schema = load_schema(Path(__file__).parents[1] / "src/tfg_demografia/schemas/nacimientos.json")
    valid = [" "] * schema.expected_record_length
    valid[48] = "0"
    valid[49] = "1"
    valid[246] = "3"
    assert validate("".join(valid), schema) == []
    invalid = valid.copy()
    invalid[48] = "9"
    assert any(issue.code == "INVALID_ENUM" for issue in validate("".join(invalid), schema))


def test_semantic_jsonl_uses_documented_fields_and_keeps_codes_as_text(tmp_path):
    source = tmp_path / "birth.txt"
    source.write_text("2026-02-01".replace("-", "") + "\n", encoding="latin-1")
    schema = Schema("nacimientos", "test", 8, "latin-1", {}, (FieldSpec("fecha", 1, 8, type="date", format="AAAAMMDD"),))
    rules = {"dataset": "nacimientos", "fields": [{"name": "fecha", "normalized_name": "fecha_suceso", "operations": ["date_ymd"]}]}
    output = tmp_path / "normalized.jsonl"
    result = normalize_source(source, schema, rules, output)
    assert result.rows_normalized == 1
    assert output.read_text(encoding="utf-8") == '{"fecha_suceso":"2026-02-01"}\n'


def test_normalization_is_idempotent_and_dry_run_writes_nothing(tmp_path):
    source = tmp_path / "nacimientos.txt"
    source.write_text("00045\n", encoding="latin-1")
    rules = {"dataset": "nacimientos", "version": "1.0", "fields": [{"name": "codigo", "operations": ["strip"]}]}
    output = tmp_path / "processed" / "normalized.jsonl"
    first = normalize_source(source, schema_with_code(), rules, output)
    second = normalize_source(source, schema_with_code(), rules, tmp_path / "other.jsonl", dry_run=True)
    assert first.output_sha256 == second.output_sha256
    assert output.read_text(encoding="utf-8") == '{"codigo":"00045"}\n'
    assert not (tmp_path / "other.jsonl").exists()
    log = tmp_path / "log.csv"
    append_log(first, log)
    assert "00045" not in log.read_text(encoding="utf-8")


def test_invalid_date_is_counted_without_writing_raw_value(tmp_path):
    source = tmp_path / "nacimientos.txt"
    source.write_text("32132026\n", encoding="latin-1")
    schema = Schema("nacimientos", "test", 8, "latin-1", {}, (FieldSpec("fecha", 1, 8, type="date"),))
    rules = {"dataset": "nacimientos", "fields": [{"name": "fecha", "operations": ["date_dmy"]}]}
    result = normalize_source(source, schema, rules, tmp_path / "out.jsonl")
    assert result.rows_failed == 1
    assert "32132026" not in (tmp_path / "out.jsonl").read_text(encoding="utf-8")


def test_zip_source_is_supported_without_extracting_to_raw(tmp_path):
    source = tmp_path / "nac_test.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("MOVWEBNAC.txt", "00045\n")
    result = normalize_source(source, schema_with_code(), {"dataset": "nacimientos", "fields": []}, tmp_path / "out.jsonl")
    assert result.rows_normalized == 1
    assert not (tmp_path / "MOVWEBNAC.txt").exists()
