from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infra.database.base import Base
from backend.infra.database.entities.workout.common import (
    DistanceMixin,
    HeartRateMixin,
    IndexedMixin,
    TimingMixin,
)

if TYPE_CHECKING:
    from backend.infra.database.entities.workout.segment import SegmentEntity
    from backend.infra.database.entities.workout.workout import WorkoutEntity


class LapEntity(
    IndexedMixin,
    TimingMixin,
    DistanceMixin,
    HeartRateMixin,
    Base
):
    __tablename__ = "laps"
    __table_args__ = (UniqueConstraint("workout_id", "index"),)

    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    stroke_count: Mapped[int]
    length_count: Mapped[int]
    active_length_count: Mapped[int]

    workout: Mapped["WorkoutEntity"] = relationship(back_populates="laps")
    segments: Mapped[list["SegmentEntity"]] = relationship(
        back_populates="lap",
        cascade="all, delete-orphan",
        order_by="SegmentEntity.index"
    )