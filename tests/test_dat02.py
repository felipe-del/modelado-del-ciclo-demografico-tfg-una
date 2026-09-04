import json
import zipfile
from pathlib import Path

import pytest

from tfg_demografia.ingestion.dat02 import (
    Dat02Result,
    detect_encoding,
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
    assert detect_encoding(payload) == "latin-1"
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
