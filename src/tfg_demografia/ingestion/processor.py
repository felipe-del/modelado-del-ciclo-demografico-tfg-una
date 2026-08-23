from datetime import datetime, timezone
from pathlib import Path

from ..models import ImportSummary, Movement, Schema
from .archive_reader import open_source
from .movement_classifier import classify
from .validator import validate


def process(source: Path, schema: Schema, require_movement_config: bool = False, issue_limit: int = 100) -> ImportSummary:
    content = open_source(source)
    configured = bool(schema.movement.get("configured", False))
    summary = ImportSummary(schema.dataset, schema.schema_version, source.name, content.member_name, content.source_sha256, content.member_sha256, datetime.now(timezone.utc).isoformat(), schema.expected_record_length, movement_classification_configured=configured)
    counts = {Movement.INCLUSION: 0, Movement.CHANGE: 0, Movement.EXCLUSION: 0, Movement.UNKNOWN: 0}
    if require_movement_config and not configured:
        summary.status = "INCOMPLETE_CONFIG"
        summary.notes = "Falta evidencia oficial de posicion y codigos de movimiento."
    for line_number, line in enumerate(content.lines(schema.encoding), 1):
        summary.total_rows += 1
        issues = validate(line, schema)
        if issues:
            summary.invalid_rows += 1
            if any(item.code == "INVALID_RECORD_LENGTH" for item in issues):
                summary.length_errors += 1
            else:
                summary.structural_errors += 1
            if any(item.field_name for item in issues):
                summary.field_errors += 1
            for issue in issues:
                if len(summary.issues) < issue_limit:
                    summary.issues.append({"line_number": line_number, "error_code": issue.code, "field_name": issue.field_name, "message": issue.message})
            continue
        summary.valid_rows += 1
        movement = classify(line, schema)
        if movement in counts:
            counts[movement] += 1
    if configured:
        summary.inclusions = counts[Movement.INCLUSION]
        summary.changes = counts[Movement.CHANGE]
        summary.exclusions = counts[Movement.EXCLUSION]
        summary.unknown_movements = counts[Movement.UNKNOWN]
    else:
        summary.notes = summary.notes or "Clasificacion de movimientos no configurada por falta de diccionario oficial."
    return summary