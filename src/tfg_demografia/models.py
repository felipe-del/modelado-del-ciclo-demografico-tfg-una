from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Movement(StrEnum):
    INCLUSION = "INCLUSION"
    CHANGE = "CHANGE"
    EXCLUSION = "EXCLUSION"
    UNKNOWN = "UNKNOWN"
    NOT_CONFIGURED = "NOT_CONFIGURED"


@dataclass(frozen=True)
class FieldSpec:
    name: str
    start: int
    end: int
    required: bool = False
    type: str | None = None
    enum: list[str] | None = None


@dataclass(frozen=True)
class Schema:
    dataset: str
    schema_version: str
    expected_record_length: int
    encoding: str
    movement: dict[str, Any]
    fields: tuple[FieldSpec, ...]


@dataclass
class ImportSummary:
    dataset: str
    schema_version: str
    source_file: str
    source_member: str
    source_sha256: str
    member_sha256: str
    processed_at_utc: str
    expected_length: int
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0
    inclusions: int | None = None
    changes: int | None = None
    exclusions: int | None = None
    unknown_movements: int = 0
    length_errors: int = 0
    structural_errors: int = 0
    field_errors: int = 0
    movement_classification_configured: bool = False
    status: str = "COMPLETED"
    notes: str = ""
    issues: list[dict[str, Any]] = field(default_factory=list)