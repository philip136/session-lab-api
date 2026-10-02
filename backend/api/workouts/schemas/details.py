from datetime import datetime

from pydantic import Field, computed_field

from backend.api.schema import ApiSchema
from backend.api.workouts.schemas.common import (
    DistanceResponse,
    HeartRateResponse,
    SwimTimingResponse,
)
from backend.api.workouts.schemas.laps import LapResponse


class WorkoutDetailsRequest(ApiSchema):
    workout_id: int


class WorkoutDetailsResponse(ApiSchema):
    id: int
    started_at: datetime
    sport: str
    sub_sport: str
    duration_seconds: float = Field(exclude=True)
    elapsed_seconds: float = Field(exclude=True)
    meters: float = Field(exclude=True)
    avg_hr: int = Field(exclude=True)
    max_hr: int = Field(exclude=True)
    calories: int
    pool_length_meters: float
    laps: list[LapResponse]

    @computed_field
    @property
    def name(self) -> str:
        if self.sub_sport == "lap_swimming":
            return "Pool Swim"

        return self.sport.replace("_", " ").title()

    @computed_field
    @property
    def timing(self) -> SwimTimingResponse:
        swim_seconds = sum(lap.timing.swim_seconds for lap in self.laps)
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
        pace = swim_seconds / self.meters * 100
        avg_speed_mps = self.meters / swim_seconds
        return DistanceResponse(
            meters=self.meters,
            pace_seconds=pace,
            avg_speed_mps=avg_speed_mps
        )

    @computed_field
    @property
    def heart_rate(self) -> HeartRateResponse:
        return HeartRateResponse(avg=self.avg_hr, max=self.max_hr)
