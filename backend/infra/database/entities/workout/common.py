from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class TimingMixin:
    duration_seconds: Mapped[float]
    elapsed_seconds: Mapped[float]


class DistanceMixin:
    meters: Mapped[float]


class HeartRateMixin:
    avg_hr: Mapped[int]
    max_hr: Mapped[int]


class IdentityMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class IndexedMixin(IdentityMixin):
    index: Mapped[int]
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )