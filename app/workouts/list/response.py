from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkoutListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: datetime

    sport: str
    sub_sport: str

    distance_meters: float
    timer_time: float
    elapsed_time: float

    avg_hr: int
    max_hr: int

    pool_length_meters: float


class WorkoutListResponse(BaseModel):
    items: list[WorkoutListItemResponse]
    limit: int
    offset: int
