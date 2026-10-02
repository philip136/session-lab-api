from datetime import datetime
from typing import Literal

from backend.api.schema import ApiSchema


class IndexedResponse(ApiSchema):
    id: int
    index: int
    started_at: datetime


class TimingResponse(ApiSchema):
    duration_seconds: float
    elapsed_seconds: float


class SwimTimingResponse(TimingResponse):
    swim_seconds: float
    rest_seconds: float


class DistanceResponse(ApiSchema):
    meters: float
    pace_seconds: float | None
    avg_speed_mps: float | None


class HeartRateResponse(ApiSchema):
    avg: int
    max: int


class StrokeSummaryResponse(ApiSchema):
    count: int
    rate_per_min: float | None
    distance_per_stroke_meters: float | None


class SegmentStrokeResponse(StrokeSummaryResponse):
    type: Literal["freestyle", "backstroke", "breaststroke", "butterfly"]


class LengthsResponse(ApiSchema):
    total: int
    active: int