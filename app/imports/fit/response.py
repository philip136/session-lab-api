from pydantic import BaseModel


class ImportFitResponse(BaseModel):
    workout_id: int
