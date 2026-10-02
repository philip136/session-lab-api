from collections.abc import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from backend.api.errors.schema import ErrorDetails, ErrorResponse
from backend.app.errors import AppError, InvalidDataError, NotFoundError


def create_handler(status_code: int) -> Callable:
    async def handler(_: Request, error: AppError) -> JSONResponse:
        response = ErrorResponse(
            error=ErrorDetails(
                code=error.code,
                message=error.message
            )
        )
        return JSONResponse(
            status_code=status_code,
            content=response.model_dump(
                mode="json",
                by_alias=True
            )
        )
    return handler


ERROR_HANDLERS = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    InvalidDataError: status.HTTP_422_UNPROCESSABLE_CONTENT,
}


def register_exception_handlers(app: FastAPI):
    for error_type, status_code in ERROR_HANDLERS.items():
        app.add_exception_handler(
            error_type,
            create_handler(status_code),
        )