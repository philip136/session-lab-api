from typing import Annotated, Literal

from pydantic import Field, computed_field

from backend.api.workouts.schemas.common import (
    DistanceResponse,
    IndexedResponse,
    SegmentStrokeResponse,
    TimingResponse,
)


class BaseSegmentResponse(IndexedResponse):
    duration_seconds: float = Field(exclude=True)
    elapsed_seconds: float = Field(exclude=True)

    @computed_field
    @property
    def timing(self) -> TimingResponse:
        return TimingResponse(
            duration_seconds=self.duration_seconds,
            elapsed_seconds=self.elapsed_seconds
        )


class ActiveSegmentResponse(BaseSegmentResponse):
    type: Literal["active"]
    meters: float = Field(exclude=True)
    stroke_count: int = Field(exclude=True)
    stroke_type: Literal["freestyle", "backstroke", "breaststroke", "butterfly"] = Field(
        exclude=True
    )

    @computed_field
    @property
    def distance(self) -> DistanceResponse:
        pace = self.duration_seconds / self.meters * 100
        avg_speed = self.meters / self.duration_seconds
        return DistanceResponse(
            meters=self.meters,
            pace_seconds=pace,
            avg_speed_mps=avg_speed
        )

    @computed_field
    @property
    def stroke(self) -> SegmentStrokeResponse:
        rate_per_min = self.stroke_count / self.duration_seconds * 60
        distance_per_stroke_meters = self.meters / self.stroke_count
        return SegmentStrokeResponse(
            count=self.stroke_count,
            type=self.stroke_type,
            rate_per_min=rate_per_min,
            distance_per_stroke_meters=distance_per_stroke_meters
        )


class RestSegmentResponse(BaseSegmentResponse):
    type: Literal["rest"]


SegmentResponse = Annotated[
    ActiveSegmentResponse | RestSegmentResponse,
    Field(discriminator="type")
]