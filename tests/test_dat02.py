import csv
import zipfile
from pathlib import Path

import pytest

from tfg_demografia.errors import ArchiveError
from tfg_demografia.ingestion.tse_sync import (
    discover_links,
    detect_encoding,
    generate_report,
    inspect_zip,
    parse_period,
    safe_extract_txt,
    sync_tse,
)


def create_zip(path: Path, name: str, payload: bytes) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(name, payload)


def schema_root(tmp_path: Path) -> Path:
    root = tmp_path / "schemas"
    root.mkdir()
    for dataset in ("nacimientos", "matrimonios", "defunciones"):
        (root / f"{dataset}.json").write_text('{"dataset":"' + dataset + '","schema_version":"1.0","expected_record_length":4,"encoding":"latin-1","movement":{"configured":false},"fields":[]}', encoding="utf-8")
    return root


def test_discovery_classification_and_period_parsing():
    html = '<a href="files/nac_enero2026_01_07.zip">N</a><a href="/mat_febrero2026_08_14.zip">M</a><a href="def_marzo2026_15_21.zip">D</a><a href="other.zip">X</a>'
    links = discover_links(html, "https://www.tse.go.cr/descarga_movimientos.html")
    assert [dataset for dataset, _ in links] == ["nacimientos", "matrimonios", "defunciones"]
    assert parse_period("nac_enero2026_01_07.zip") == {"year": 2026, "month": 1, "period_start": 1, "period_end": 7}
    assert parse_period("nac_invalido.zip")["year"] is None


def test_encoding_and_length_inspection(tmp_path):
    archive = tmp_path / "nac_abril2026_01_02.zip"
    create_zip(archive, "MOVWEBNAC.txt", b"abcd\nxy\n\nabcde\n")
    schema = schema_root(tmp_path) / "nacimientos.json"
    inspection = inspect_zip(archive, schema)
    assert detect_encoding(b"texto", "latin-1") == ("utf-8", "UTF8_STRICT")
    assert detect_encoding(b"\xe1", "latin-1") == ("latin-1", "SCHEMA_FALLBACK_AFTER_UTF8_FAILURE")
    assert (inspection.total_rows, inspection.valid_length_rows, inspection.short_rows, inspection.long_rows, inspection.empty_rows) == (4, 1, 1, 1, 1)
    assert (inspection.min_record_length, inspection.max_record_length) == (0, 5)


def test_safe_extraction_creates_own_folder_and_rejects_traversal(tmp_path):
    archive = tmp_path / "nac_mayo2026_01_07.zip"
    create_zip(archive, "folder/MOVWEBNAC.txt", b"abcd\n")
    destination = tmp_path / "extracted"
    name, target = safe_extract_txt(archive, destination, "a" * 64)
    assert name == "folder/MOVWEBNAC.txt"
    assert Path(target).is_file()
    assert (destination / ".dat02.json").is_file()
    unsafe = tmp_path / "nac_mayo2026_08_14.zip"
    create_zip(unsafe, "../outside.txt", b"abcd\n")
    with pytest.raises(ArchiveError):
        safe_extract_txt(unsafe, tmp_path / "unsafe", "b" * 64)


def test_local_sync_manifest_idempotency_conflict_and_report(tmp_path):
    raw = tmp_path / "raw"
    zip_path = raw / "nacimientos" / "nac_junio2026_01_07.zip"
    zip_path.parent.mkdir(parents=True)
    create_zip(zip_path, "MOVWEBNAC.txt", b"abcd\n")
    manifest, report, schemas = tmp_path / "manifest.csv", tmp_path / "report.md", schema_root(tmp_path)
    first = sync_tse(raw, tmp_path / "work", manifest, report, schemas, local_only=True)
    assert first[0]["download_status"] == "ALREADY_PRESENT"
    assert first[0]["extraction_status"] == "EXTRACTED"
    second = sync_tse(raw, tmp_path / "work", manifest, report, schemas, local_only=True)
    assert second[0]["extraction_status"] == "ALREADY_EXTRACTED"
    with manifest.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 1
    assert "abcd" not in report.read_text(encoding="utf-8")
    assert "Lineas RAW incluidas: NO" in report.read_text(encoding="utf-8")
    rows[0]["zip_sha256"] = "f" * 64
    with manifest.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    conflict = sync_tse(raw, tmp_path / "work", manifest, report, schemas, local_only=True)
    assert conflict[0]["download_status"] == "HASH_CONFLICT"


def test_dry_run_does_not_write_files(tmp_path):
    raw = tmp_path / "raw"
    zip_path = raw / "defunciones" / "def_julio2026_01_07.zip"
    zip_path.parent.mkdir(parents=True)
    create_zip(zip_path, "MOVWEBDEF.txt", b"abcd\n")
    manifest, report = tmp_path / "manifest.csv", tmp_path / "report.md"
    result = sync_tse(raw, tmp_path / "work", manifest, report, schema_root(tmp_path), dry_run=True, local_only=True)
    assert result[0]["download_status"] == "ALREADY_PRESENT"
    assert not manifest.exists()
    assert not report.exists()
    assert not (tmp_path / "work").exists()


def test_remote_download_and_hash_conflict_do_not_overwrite(tmp_path, monkeypatch):
    class Response:
        def __init__(self, data):
            self.data = data

        def read(self):
            return self.data

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    remote_zip = tmp_path / "remote.zip"
    create_zip(remote_zip, "MOVWEBNAC.txt", b"abcd\n")
    payload = remote_zip.read_bytes()
    page = b'<a href="nac_agosto2026_01_06.zip">archivo</a>'
    monkeypatch.setattr("tfg_demografia.ingestion.tse_sync.urlopen", lambda url, timeout: Response(page if str(url).endswith("html") else payload))
    raw, schemas = tmp_path / "raw", schema_root(tmp_path)
    manifest, report = tmp_path / "manifest.csv", tmp_path / "report.md"
    sync_tse(raw, tmp_path / "work", manifest, report, schemas)
    local = raw / "nacimientos" / "movimientos" / "downloaded" / "nac_agosto2026_01_06.zip"
    original = local.read_bytes()
    monkeypatch.setattr("tfg_demografia.ingestion.tse_sync.urlopen", lambda url, timeout: Response(page if str(url).endswith("html") else b"different"))
    result = sync_tse(raw, tmp_path / "work", manifest, report, schemas)
    assert result[0]["download_status"] == "HASH_CONFLICT"
    assert local.read_bytes() == original