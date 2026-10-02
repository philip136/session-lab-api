from pydantic import Field, computed_field

from backend.api.workouts.schemas.common import (
    DistanceResponse,
    HeartRateResponse,
    IndexedResponse,
    LengthsResponse,
    StrokeSummaryResponse,
    SwimTimingResponse,
)
from backend.api.workouts.schemas.segments import SegmentResponse


class LapResponse(IndexedResponse):
    duration_seconds: float = Field(exclude=True)
    elapsed_seconds: float = Field(exclude=True)
    meters: float = Field(exclude=True)
    avg_hr: int = Field(exclude=True)
    max_hr: int = Field(exclude=True)
    stroke_count: int = Field(exclude=True)
    length_count: int = Field(exclude=True)
    active_length_count: int = Field(exclude=True)

    segments: list[SegmentResponse]

    @computed_field
    @property
    def timing(self) -> SwimTimingResponse:
        swim_seconds = sum(
            seg.duration_seconds for seg in self.segments
            if seg.type == "active"
        )
        rest_seconds = max(self.duration_seconds - swim_seconds, 0)
        return SwimTimingResponse(
            duration_seconds=self.duration_seconds,
            elapsed_seconds=self.elapsed_seconds,
            swim_seconds=swim_seconds,
            rest_seconds=rest_seconds
        )

    @computed_field
    @property
    def distance(self) -> DistanceResponse:
        swim_seconds = self.timing.swim_seconds
        # Rest-only lap has no pace or speed.
        if swim_seconds == 0:
            return DistanceResponse(
                meters=self.meters,
                pace_seconds=None,
                avg_speed_mps=None
            )

        pace = swim_seconds / self.meters * 100
        avg_speed_mps = self.meters / swim_seconds
        return DistanceResponse(
            meters=self.meters,
            pace_seconds=pace,
            avg_speed_mps=avg_speed_mps
        )

    @computed_field
    @property
    def stroke(self) -> StrokeSummaryResponse:
        swim_seconds = self.timing.swim_seconds

        if swim_seconds == 0 or self.stroke_count == 0:
            return StrokeSummaryResponse(
                count=self.stroke_count,
                rate_per_min=None,
                distance_per_stroke_meters=None
            )

        rate_per_min = self.stroke_count / swim_seconds * 60
        distance_per_stroke_meters = self.meters / self.stroke_count
        return StrokeSummaryResponse(
            count=self.stroke_count,
            rate_per_min=rate_per_min,
            distance_per_stroke_meters=distance_per_stroke_meters
        )

    @computed_field
    @property
    def lengths(self) -> LengthsResponse:
        return LengthsResponse(total=self.length_count, active=self.active_length_count)

    @computed_field
    @property
    def heart_rate(self) -> HeartRateResponse:
        return HeartRateResponse(avg=self.avg_hr, max=self.max_hr)