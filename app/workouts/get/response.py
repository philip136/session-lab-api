from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    index: int
    type: str

    start_time: datetime

    timer_time: float
    elapsed_time: float

    distance_meters: float | None
    strokes: int | None
    stroke_type: str | None
    avg_speed: float | None


class LapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    index: int
    start_time: datetime

    distance_meters: float
    timer_time: float
    elapsed_time: float

    avg_hr: int
    max_hr: int

    total_strokes: int

    lengths_no: int
    active_lengths_no: int

    segments: list[SegmentResponse]


class WorkoutGetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    provider: str
    source_format: str
    file_name: str

    started_at: datetime

    sport: str
    sub_sport: str

    distance_meters: float
    timer_time: float
    elapsed_time: float

    avg_hr: int
    max_hr: int

    calories: int
    pool_length_meters: float

    laps: list[LapResponse]
