from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class WorkoutSourceDTO(BaseModel):
    provider: str
    source_format: str
    file_name: str


class ActiveSegmentDTO(BaseModel):
    index: int
    type: Literal["active"] = "active"

    start_time: datetime

    distance_meters: float
    timer_time: float
    elapsed_time: float

    strokes: int
    stroke_type: str
    avg_speed: float


class RestSegmentDTO(BaseModel):
    index: int
    type: Literal["rest"] = "rest"

    start_time: datetime

    timer_time: float
    elapsed_time: float


SegmentDTO = ActiveSegmentDTO | RestSegmentDTO


class LapDTO(BaseModel):
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

    segments: list[SegmentDTO]


class WorkoutSummaryDTO(BaseModel):
    distance_meters: float

    timer_time: float
    elapsed_time: float

    avg_hr: int
    max_hr: int

    calories: int
    pool_length_meters: float


class WorkoutDTO(BaseModel):
    source: WorkoutSourceDTO

    started_at: datetime
    sport: str
    sub_sport: str

    summary: WorkoutSummaryDTO
    laps: list[LapDTO]
