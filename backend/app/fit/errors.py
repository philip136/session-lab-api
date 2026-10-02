from backend.app.errors import InvalidDataError


class InvalidFitFileError(InvalidDataError):
    code: str = "INVALID_FIT_FILE"
    message: str = "Unable to read FIT file."