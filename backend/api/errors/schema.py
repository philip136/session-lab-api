from backend.api.schema import ApiSchema


class ErrorDetails(ApiSchema):
    code: str
    message: str


class ErrorResponse(ApiSchema):
    error: ErrorDetails