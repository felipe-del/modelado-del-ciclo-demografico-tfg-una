import json
from pathlib import Path

from .errors import SchemaError
from .models import FieldSpec, Schema

REQUIRED_KEYS = {"dataset", "schema_version", "expected_record_length", "encoding", "movement", "fields"}


def load_schema(path: Path) -> Schema:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaError(f"No se pudo cargar el esquema: {path.name}") from exc
    if not isinstance(data, dict) or not REQUIRED_KEYS <= data.keys():
        raise SchemaError("El esquema no contiene la estructura requerida")
    length = data["expected_record_length"]
    if not isinstance(length, int) or length <= 0:
        raise SchemaError("expected_record_length debe ser un entero positivo")
    movement = data["movement"]
    if not isinstance(movement, dict):
        raise SchemaError("movement debe ser un objeto")
    configured = movement.get("configured", False)
    if not isinstance(configured, bool):
        raise SchemaError("movement.configured debe ser booleano")
    code_config = movement.get("codes", movement)
    if not isinstance(code_config, dict):
        raise SchemaError("movement.codes debe ser un objeto")
    code_names = {"inclusion": "inclusion_codes", "change": "change_codes", "exclusion": "exclusion_codes"}
    codes = {key: code_config.get(code_names[key], code_config.get(key, [])) for key in code_names}
    if any(not isinstance(value, list) for value in codes.values()):
        raise SchemaError("Los codigos de movimiento deben ser listas")
    code_sets = [set(map(str, value)) for value in codes.values()]
    if code_sets[0] & code_sets[1] or code_sets[0] & code_sets[2] or code_sets[1] & code_sets[2]:
        raise SchemaError("Un codigo de movimiento aparece en mas de una categoria")
    fields = []
    if not isinstance(data["fields"], list):
        raise SchemaError("fields debe ser una lista")
    for raw in data["fields"]:
        if not isinstance(raw, dict) or not {"name", "start", "end"} <= raw.keys():
            raise SchemaError("Campo sin nombre o rango completo")
        start, end = raw["start"], raw["end"]
        if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start or end > length:
            raise SchemaError("Rango de campo fuera del registro")
        fields.append(FieldSpec(raw["name"], start, end, bool(raw.get("required", False)), raw.get("type"), raw.get("enum")))
    movement_field = movement.get("field")
    if configured:
        if isinstance(movement_field, dict):
            if not {"name", "start", "end"} <= movement_field.keys():
                raise SchemaError("El campo de movimiento requiere nombre y rango")
            start, end = movement_field["start"], movement_field["end"]
            if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start or end > length:
                raise SchemaError("Rango del campo de movimiento fuera del registro")
            fields.append(FieldSpec(movement_field["name"], start, end, bool(movement_field.get("required", False)), movement_field.get("type"), movement_field.get("enum")))
        elif not isinstance(movement_field, str):
            raise SchemaError("Un movimiento configurado requiere el campo de clasificacion")
    return Schema(data["dataset"], str(data["schema_version"]), length, data["encoding"], movement, tuple(fields))