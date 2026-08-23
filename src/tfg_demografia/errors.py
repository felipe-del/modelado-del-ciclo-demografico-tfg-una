class TSEError(Exception):
    """Error controlado del lector TSE."""


class ArchiveError(TSEError):
    pass


class SchemaError(TSEError):
    pass