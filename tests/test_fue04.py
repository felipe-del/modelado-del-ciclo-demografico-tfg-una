import csv
import json

import pytest

from tfg_demografia.errors import TSEError
from tfg_demografia.ingestion.source_profile import build_profile, write_profile


def write_schema(root, dataset="nacimientos"):
    (root / f"{dataset}.json").write_text(json.dumps({"dataset": dataset, "schema_version": "1.0", "expected_record_length": 4, "encoding": "latin-1", "movement": {"configured": False}, "fields": []}), encoding="utf-8")


def write_manifest(path):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["dataset", "year", "month", "period_start", "period_end", "encoding_detected", "total_rows", "valid_length_rows", "short_rows", "long_rows", "empty_rows", "txt_filename"])
        writer.writeheader()
        writer.writerows([{"dataset": "nacimientos", "year": 2026, "month": 2, "period_start": 27, "period_end": 28, "encoding_detected": "latin-1", "total_rows": 4, "valid_length_rows": 3, "short_rows": 1, "long_rows": 0, "empty_rows": 0, "txt_filename": "MOVWEBNAC.txt"}, {"dataset": "nacimientos", "year": 2026, "month": 3, "period_start": 2, "period_end": 5, "encoding_detected": "utf-8", "total_rows": 6, "valid_length_rows": 5, "short_rows": 0, "long_rows": 1, "empty_rows": 0, "txt_filename": "MOVWEBNAC.txt"}])


def test_profile_aggregates_coverage_quality_and_no_field_missingness(tmp_path):
    schemas = tmp_path / "schemas"
    schemas.mkdir()
    write_schema(schemas)
    manifest = tmp_path / "manifest.csv"
    write_manifest(manifest)
    profile = build_profile(manifest, schemas, ("nacimientos",))
    item = profile["profiles"][0]
    assert item["publication_period_start"] == "2026-02-27"
    assert item["publication_period_end"] == "2026-03-05"
    assert item["apparent_gap_days"] == 1
    assert item["total_rows"] == 10
    assert item["short_rows"] == 1
    assert item["long_rows"] == 1
    assert item["field_missingness"].startswith("NO DETERMINADO")
    assert item["event_date"].startswith("NO DOCUMENTADO")


def test_profile_outputs_contain_aggregates_without_raw_values(tmp_path):
    schemas = tmp_path / "schemas"
    schemas.mkdir()
    write_schema(schemas)
    manifest = tmp_path / "manifest.csv"
    write_manifest(manifest)
    profile = build_profile(manifest, schemas, ("nacimientos",))
    json_path, table_path, report_path = tmp_path / "profile.json", tmp_path / "table.csv", tmp_path / "report.md"
    write_profile(profile, json_path, table_path, report_path)
    assert json_path.exists() and table_path.exists() and report_path.exists()
    assert "MOVWEBNAC.txt" in table_path.read_text(encoding="utf-8")
    assert "fecha marginal" in report_path.read_text(encoding="utf-8").lower()


def test_profile_rejects_missing_manifest_and_unknown_dataset_schema(tmp_path):
    schemas = tmp_path / "schemas"
    schemas.mkdir()
    with pytest.raises(TSEError):
        build_profile(tmp_path / "missing.csv", schemas, ("nacimientos",))
    manifest = tmp_path / "manifest.csv"
    write_manifest(manifest)
    with pytest.raises(TSEError):
        build_profile(manifest, schemas, ("desconocido",))