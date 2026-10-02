from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infra.database.base import Base
from backend.infra.database.entities.workout.common import IndexedMixin, TimingMixin

if TYPE_CHECKING:
    from backend.infra.database.entities.workout.lap import LapEntity


class SegmentEntity(
    IndexedMixin,
    TimingMixin,
    Base
):
    __tablename__ = "segments"
    __table_args__ = (UniqueConstraint("lap_id", "index"),)

    lap_id: Mapped[int] = mapped_column(ForeignKey("laps.id"))
    type: Mapped[str]
    meters: Mapped[float | None]
    stroke_count: Mapped[int | None]
    stroke_type: Mapped[str | None]
    lap: Mapped["LapEntity"] = relationship(back_populates="segments")