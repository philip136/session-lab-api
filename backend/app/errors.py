class AppError(Exception):
    code: str = "APPLICATION_ERROR"
    message: str = "Application error."


class NotFoundError(AppError):
    pass


class InvalidDataError(AppError):
    pass