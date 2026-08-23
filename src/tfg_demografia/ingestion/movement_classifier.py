from ..models import Movement, Schema


def classify(line: str, schema: Schema) -> Movement:
    config = schema.movement
    if not config.get("configured", False):
        return Movement.NOT_CONFIGURED
    field = next((item for item in schema.fields if item.name == config.get("field")), None)
    if field is None:
        return Movement.NOT_CONFIGURED
    code = line[field.start - 1:field.end].strip()
    for movement, key in ((Movement.INCLUSION, "inclusion"), (Movement.CHANGE, "change"), (Movement.EXCLUSION, "exclusion")):
        if code in {str(value) for value in config.get(key, [])}:
            return movement
    return Movement.UNKNOWN