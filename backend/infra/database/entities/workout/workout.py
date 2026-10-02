from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infra.database.base import Base
from backend.infra.database.entities.workout.common import (
    DistanceMixin,
    HeartRateMixin,
    IdentityMixin,
    TimingMixin,
)

if TYPE_CHECKING:
    from backend.infra.database.entities.workout.lap import LapEntity


class WorkoutEntity(
    IdentityMixin,
    TimingMixin,
    DistanceMixin,
    HeartRateMixin,
    Base
):
    __tablename__ = "workouts"

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    sport: Mapped[str]
    sub_sport: Mapped[str]
    calories: Mapped[int]
    pool_length_meters: Mapped[float]
    laps: Mapped[list["LapEntity"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan",
        order_by="LapEntity.index"
    )