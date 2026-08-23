from ..models import FieldSpec


def remove_line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return line[:-2]
    if line.endswith(("\r", "\n")):
        return line[:-1]
    return line


def extract_field(line: str, field: FieldSpec) -> str:
    return line[field.start - 1:field.end]