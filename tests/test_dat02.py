import csv
import json
import zipfile
from pathlib import Path

import pytest

from tfg_demografia.errors import ArchiveError
from tfg_demografia.ingestion.tse_sync import (
    discover_links,
    detect_encoding as detect_sync_encoding,
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
    assert detect_sync_encoding(b"texto", "latin-1") == ("utf-8", "UTF8_STRICT")
    assert detect_sync_encoding(b"\xe1", "latin-1") == ("latin-1", "SCHEMA_FALLBACK_AFTER_UTF8_FAILURE")
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


def test_report_uses_period_start_for_minimum_and_period_end_for_maximum(tmp_path):
    raw = tmp_path / "raw"
    first = raw / "nacimientos" / "nac_febrero2026_27_28.zip"
    last = raw / "nacimientos" / "nac_agosto2026_01_06.zip"
    first.parent.mkdir(parents=True)
    create_zip(first, "MOVWEBNAC.txt", b"abcd\n")
    create_zip(last, "MOVWEBNAC.txt", b"abcd\n")
    manifest, report = tmp_path / "manifest.csv", tmp_path / "report.md"

    sync_tse(raw, tmp_path / "work", manifest, report, schema_root(tmp_path), local_only=True)

    report_text = report.read_text(encoding="utf-8")
    assert "Periodo minimo detectado: 2026-02-27" in report_text
    assert "Periodo maximo detectado: 2026-08-06" in report_text


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

from tfg_demografia.ingestion.dat02 import (
    Dat02Result,
    detect_encoding as detect_batch_encoding,
    process_batch,
    process_zip,
    validate_zip_members,
    write_manifest,
)


def make_record(length: int, value: str = "A") -> str:
    return (value * length)[:length]


def make_zip(path: Path, name: str, data: bytes) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(name, data)


def test_detects_latin1_and_expected_lengths():
    payload = (make_record(281, "A") + "\n").encode("latin-1")
    assert detect_batch_encoding(payload) == "latin-1"
    assert len(payload.strip()) == 281


def test_process_zip_extracts_to_own_folder_and_keeps_raw_immutable(tmp_path):
    zip_path = tmp_path / "nac_agosto2026_01_06.zip"
    payload = (make_record(281, "A") + "\n").encode("latin-1")
    make_zip(zip_path, "MOVWEBNAC.txt", payload)
    original_hash = __import__("hashlib").sha256(zip_path.read_bytes()).hexdigest()

    result = process_zip(zip_path, tmp_path / "extracted")

    assert isinstance(result, Dat02Result)
    assert result.status in {"PROCESADO", "YA_PROCESADO"}
    assert result.sha256_zip == original_hash
    assert result.file_txt.endswith("MOVWEBNAC.txt")
    assert result.extraction_dir.exists()
    assert result.extraction_dir != zip_path.parent
    assert zip_path.read_bytes() == result.raw_bytes


def test_process_zip_rejects_zip_slip(tmp_path):
    zip_path = tmp_path / "bad.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("../evil.txt", b"bad")

    with pytest.raises(ValueError):
        validate_zip_members(zip_path)


def test_process_zip_is_idempotent_and_detects_existing_manifest(tmp_path):
    zip_path = tmp_path / "mat_agosto2026_01_06.zip"
    payload = (make_record(328, "B") + "\n").encode("latin-1")
    make_zip(zip_path, "MOVWEBMAT.txt", payload)

    first = process_zip(zip_path, tmp_path / "extracted")
    second = process_zip(zip_path, tmp_path / "extracted")

    assert first.status == "PROCESADO"
    assert second.status in {"YA_PROCESADO", "PROCESADO"}
    assert second.sha256_zip == first.sha256_zip


def test_batch_processes_multiple_zips_and_continues_after_error(tmp_path):
    good = tmp_path / "good.zip"
    bad = tmp_path / "bad.zip"
    make_zip(good, "MOVWEBDEF.txt", (make_record(191, "C") + "\n").encode("latin-1"))
    bad.write_bytes(b"not zip")

    results = process_batch(tmp_path, tmp_path / "extracted")
    assert len(results) >= 1
    assert any(result.status == "PROCESADO" for result in results)
    assert any(result.status in {"ERROR", "ZIP_INVALIDO"} for result in results)


def test_manifest_and_report_are_generated_without_pii(tmp_path):
    zip_path = tmp_path / "def_agosto2026_01_06.zip"
    payload = (make_record(191, "D") + "\n").encode("latin-1")
    make_zip(zip_path, "MOVWEBDEF.txt", payload)

    manifest_path = tmp_path / "manifest.jsonl"
    report_path = tmp_path / "report.md"
    result = process_zip(zip_path, tmp_path / "extracted")
    write_manifest([result], manifest_path)

    assert manifest_path.exists()
    text = manifest_path.read_text(encoding="utf-8")
    assert "PII" not in text.upper()
    assert "sha256_zip" in text
    assert report_path.parent == tmp_path


def test_verify_dat02_criteria_and_cli_are_available(tmp_path):
    zip_path = tmp_path / "nac_agosto2026_01_06.zip"
    payload = (make_record(281, "A") + "\n").encode("latin-1")
    make_zip(zip_path, "MOVWEBNAC.txt", payload)
    result = process_zip(zip_path, tmp_path / "extracted")
    manifest_path = tmp_path / "manifest.jsonl"
    write_manifest([result], manifest_path)
    assert result.sha256_txt
    assert result.encoding == "latin-1"
    assert result.rows_total >= 1
    assert manifest_path.exists()


def test_invalid_zip_and_missing_txt_are_marked(tmp_path):
    bad = tmp_path / "broken.zip"
    bad.write_bytes(b"nope")
    with pytest.raises(ValueError):
        validate_zip_members(bad)

    good = tmp_path / "sample.zip"
    with zipfile.ZipFile(good, "w") as archive:
        archive.writestr("notes.txt", b"x")
    result = process_zip(good, tmp_path / "out")
    assert result.status in {"ERROR", "TXT_NO_ENCONTRADO", "MULTIPLES_TXT"}


def test_reprocessing_uses_manifest_metrics_and_semantic_period(tmp_path):
    zip_path = tmp_path / "mat_febrero2026_27_28.zip"
    payload = (make_record(328, "B") + "\n").encode("latin-1")
    make_zip(zip_path, "MOVWEBMAT.txt", payload)
    manifest_path = tmp_path / "manifest.jsonl"

    first = process_zip(zip_path, tmp_path / "extracted", manifest_path)
    write_manifest([first], manifest_path)
    second = process_zip(zip_path, tmp_path / "extracted", manifest_path)

    assert first.estado == "PROCESADO"
    assert second.estado == "YA_PROCESADO"
    assert second.filas_totales == first.filas_totales == 1
    assert second.longitud_minima == first.longitud_minima == 328
    assert second.longitud_maxima == first.longitud_maxima == 328
    assert second.encoding == first.encoding == "latin-1"
    assert second.sha256_zip == first.sha256_zip
    assert second.sha256_txt == first.sha256_txt
    assert second.periodo_anio == "2026"
    assert second.periodo_mes == "02"
    assert second.periodo_desde == "2026-02-27"
    assert second.periodo_hasta == "2026-02-28"
    assert second.periodo_original == "febrero2026_27_28"
    assert second.ruta_zip == str(zip_path)
    assert second.periodo_original != second.ruta_zip
    assert "C:/" not in second.periodo_original


def test_manifest_remains_idempotent_for_reprocessed_zip(tmp_path):
    zip_path = tmp_path / "def_febrero2026_27_28.zip"
    payload = (make_record(191, "C") + "\n").encode("latin-1")
    make_zip(zip_path, "MOVWEBDEF.txt", payload)
    manifest_path = tmp_path / "manifest.jsonl"

    first = process_zip(zip_path, tmp_path / "extracted", manifest_path)
    write_manifest([first], manifest_path)
    second = process_zip(zip_path, tmp_path / "extracted", manifest_path)
    write_manifest([second], manifest_path)

    lines = [line for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    payloads = [json.loads(line) for line in lines]
    assert len(payloads) == 1
    assert payloads[0]["sha256_zip"] == first.sha256_zip
    assert payloads[0]["estado"] == "PROCESADO"
    assert payloads[0]["periodo_original"] == "febrero2026_27_28"
    assert payloads[0]["ruta_zip"] == str(zip_path)
