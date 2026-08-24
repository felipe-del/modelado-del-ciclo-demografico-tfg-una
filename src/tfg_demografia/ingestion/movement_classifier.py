from ..models import Movement, Schema


def classify(line: str, schema: Schema) -> Movement:
    config = schema.movement
    if not config.get("configured", False):
        return Movement.NOT_CONFIGURED
    configured_field = config.get("field")
    field_name = configured_field.get("name") if isinstance(configured_field, dict) else configured_field
    field = next((item for item in schema.fields if item.name == field_name), None)
    if field is None:
        return Movement.NOT_CONFIGURED
    code = line[field.start - 1:field.end].strip()
    code_config = config.get("codes", config)
    code_names = {Movement.INCLUSION: "inclusion_codes", Movement.CHANGE: "change_codes", Movement.EXCLUSION: "exclusion_codes"}
    for movement, key in code_names.items():
        values = code_config.get(key, code_config.get(movement.value.lower(), []))
        if code in {str(value) for value in values}:
            return movement
    return Movement.UNKNOWN