from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base

if TYPE_CHECKING:
    from app.dto.workout import LapDTO, SegmentDTO, WorkoutDTO


class WorkoutDBO(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)

    provider: Mapped[str]
    source_format: Mapped[str]
    file_name: Mapped[str]
    raw_file_path: Mapped[str]

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    sport: Mapped[str]
    sub_sport: Mapped[str]

    distance_meters: Mapped[float]
    timer_time: Mapped[float]
    elapsed_time: Mapped[float]

    avg_hr: Mapped[int]
    max_hr: Mapped[int]

    calories: Mapped[int]
    pool_length_meters: Mapped[float]

    laps: Mapped[list[LapDBO]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan",
        order_by="LapDBO.index",
    )

    @classmethod
    def from_dto(
        cls,
        dto: WorkoutDTO,
        raw_file_path: str,
    ) -> WorkoutDBO:
        workout = cls(
            **dto.source.model_dump(),
            **dto.summary.model_dump(),
            raw_file_path=raw_file_path,
            started_at=dto.started_at,
            sport=dto.sport,
            sub_sport=dto.sub_sport,
        )

        workout.laps = [LapDBO.from_dto(lap) for lap in dto.laps]
        return workout


class LapDBO(Base):
    __tablename__ = "laps"

    __table_args__ = (
        UniqueConstraint("workout_id", "lap_index"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"))

    index: Mapped[int] = mapped_column("lap_index")

    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    distance_meters: Mapped[float]
    timer_time: Mapped[float]
    elapsed_time: Mapped[float]

    avg_hr: Mapped[int]
    max_hr: Mapped[int]

    total_strokes: Mapped[int]

    lengths_no: Mapped[int]
    active_lengths_no: Mapped[int]

    workout: Mapped[WorkoutDBO] = relationship(back_populates="laps")

    segments: Mapped[list[SegmentDBO]] = relationship(
        back_populates="lap",
        cascade="all, delete-orphan",
        order_by="SegmentDBO.index",
    )

    @classmethod
    def from_dto(cls, dto: LapDTO) -> LapDBO:
        lap = cls(**dto.model_dump(exclude={"segments"}))
        lap.segments = [SegmentDBO.from_dto(segment) for segment in dto.segments]
        return lap


class SegmentDBO(Base):
    __tablename__ = "segments"

    __table_args__ = (
        UniqueConstraint("lap_id", "segment_index"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lap_id: Mapped[int] = mapped_column(ForeignKey("laps.id"))

    index: Mapped[int] = mapped_column("segment_index")

    type: Mapped[str]
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    timer_time: Mapped[float]
    elapsed_time: Mapped[float]

    distance_meters: Mapped[float | None]
    strokes: Mapped[int | None]
    stroke_type: Mapped[str | None]
    avg_speed: Mapped[float | None]

    lap: Mapped[LapDBO] = relationship(back_populates="segments")

    @classmethod
    def from_dto(cls, dto: SegmentDTO) -> SegmentDBO:
        return cls(**dto.model_dump())
