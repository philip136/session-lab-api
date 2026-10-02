from typing import Annotated

from pydantic import Field

from backend.api.schema import ApiSchema


class ImportFitRequest(ApiSchema):
    content: Annotated[bytes, Field(min_length=1)]


class ImportFitResponse(ApiSchema):
    workout_id: int