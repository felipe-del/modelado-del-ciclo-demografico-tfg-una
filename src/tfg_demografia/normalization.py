import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .errors import TSEError
from .ingestion.archive_reader import open_source
from .ingestion.fixed_width_reader import extract_field
from .ingestion.validator import validate
from .models import Schema


@dataclass(frozen=True)
class NormalizationResult:
    run_id: str
    dataset: str
    source_file: str
    source_member: str
    source_sha256: str
    member_sha256: str
    rules_sha256: str
    output_file: str | None
    output_sha256: str | None
    rows_evaluated: int
    rows_normalized: int
    rows_failed: int
    exception_count: int
    status: str


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_rules(path: Path, dataset: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TSEError(f"No se pudo cargar la configuracion de transformacion: {path}") from exc
    if not isinstance(data, dict) or data.get("dataset") != dataset or not isinstance(data.get("fields", []), list):
        raise TSEError("La configuracion de transformacion no coincide con el dataset")
    return data


def _normalize_value(value: str, rule: dict[str, Any]) -> Any:
    result: Any = value
    for operation in rule.get("operations", []):
        if operation == "strip":
            result = result.strip()
        elif operation == "empty_to_null":
            result = None if result == "" else result
        elif operation == "upper":
            result = result.upper()
        elif operation == "lower":
            result = result.lower()
        elif operation == "integer":
            result = int(result) if result != "" else None
        elif operation == "date_dmy":
            result = datetime.strptime(result, "%d%m%Y").date().isoformat() if result else None
        elif operation == "map":
            catalog = rule.get("catalog")
            if not isinstance(catalog, dict) or result not in catalog:
                raise ValueError("VALUE_NOT_IN_CATALOG")
            result = catalog[result]
        else:
            raise ValueError("UNKNOWN_OPERATION")
    return result


def transform_record(line: str, schema: Schema, rules: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    rules_by_name = {str(rule["name"]): rule for rule in rules.get("fields", []) if isinstance(rule, dict) and "name" in rule}
    for field in schema.fields:
        rule = rules_by_name.get(field.name)
        if rule is None:
            continue
        normalized_name = str(rule.get("normalized_name", field.name))
        normalized[normalized_name] = _normalize_value(extract_field(line, field), rule)
    return normalized


def normalize_source(source: Path, schema: Schema, rules: dict[str, Any], output: Path | None = None, dry_run: bool = False) -> NormalizationResult:
    content = open_source(source)
    rules_bytes = json.dumps(rules, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    rules_sha256 = _sha256_bytes(rules_bytes)
    run_id = _sha256_bytes(f"{content.source_sha256}:{content.member_sha256}:{rules_sha256}".encode("ascii"))[:16]
    rows_evaluated = rows_normalized = rows_failed = exception_count = 0
    rendered: list[bytes] = []
    for line in content.lines(schema.encoding):
        rows_evaluated += 1
        issues = validate(line, schema)
        if issues:
            rows_failed += 1
            continue
        try:
            rendered.append((json.dumps(transform_record(line, schema, rules), ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
            rows_normalized += 1
        except (TypeError, ValueError, OverflowError):
            rows_failed += 1
            exception_count += 1
    payload = b"".join(rendered)
    output_sha256 = _sha256_bytes(payload)
    output_file = None if output is None else str(output)
    if not dry_run and output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
    return NormalizationResult(run_id, schema.dataset, str(content.source_file), content.member_name, content.source_sha256, content.member_sha256, rules_sha256, output_file, output_sha256, rows_evaluated, rows_normalized, rows_failed, exception_count, "DRY_RUN" if dry_run else "COMPLETED")


def append_log(result: NormalizationResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(result.__dataclass_fields__)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields + ["timestamp_utc"])
        if not exists:
            writer.writeheader()
        row = {field: getattr(result, field) for field in fields}
        row["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
        writer.writerow(row)