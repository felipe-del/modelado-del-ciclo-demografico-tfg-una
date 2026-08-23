from dataclasses import dataclass
from datetime import datetime

from ..models import Schema
from .fixed_width_reader import extract_field


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    field_name: str | None
    message: str


def validate(line: str, schema: Schema) -> list[ValidationIssue]:
    if not line:
        return [ValidationIssue("EMPTY_RECORD", None, "El registro esta vacio.")]
    if len(line) != schema.expected_record_length:
        return [ValidationIssue("INVALID_RECORD_LENGTH", None, "La longitud no coincide con la longitud esperada.")]
    issues = []
    for field in schema.fields:
        value = extract_field(line, field)
        if field.required and not value.strip():
            issues.append(ValidationIssue("REQUIRED_FIELD", field.name, "Falta un campo obligatorio."))
        if field.type == "integer" and value.strip():
            try:
                int(value.strip())
            except ValueError:
                issues.append(ValidationIssue("INVALID_FIELD_TYPE", field.name, "El campo no tiene el tipo esperado."))
        if field.type == "date" and value.strip():
            try:
                datetime.strptime(value.strip(), "%d%m%Y")
            except ValueError:
                issues.append(ValidationIssue("INVALID_DATE", field.name, "La fecha no tiene el formato esperado."))
        if field.enum is not None and value.strip() not in field.enum:
            issues.append(ValidationIssue("INVALID_ENUM", field.name, "El valor no pertenece al dominio configurado."))
    return issues