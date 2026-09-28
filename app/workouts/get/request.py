from pydantic import BaseModel


class WorkoutGetRequest(BaseModel):
    workout_id: int
