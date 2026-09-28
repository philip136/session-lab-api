from pathlib import Path

from garmin_fit_sdk import Decoder, Stream

from app.dto.workout import (
    ActiveSegmentDTO,
    LapDTO,
    RestSegmentDTO,
    SegmentDTO,
    WorkoutDTO,
    WorkoutSourceDTO,
    WorkoutSummaryDTO,
)


class FitParseError(Exception):
    pass


class FitParser:
    def __init__(self, path: str | Path, source_name: str | None = None):
        self._path = Path(path)
        self._source_name = source_name or self._path.name
        self._msgs = self._decode()

        self._lengths_by_index = {
            record["message_index"]: record
            for record in self._msgs["length_mesgs"]
        }

    def _decode(self) -> dict:
        stream = Stream.from_file(str(self._path))
        messages, errors = Decoder(stream).read(enable_crc_check=True)

        if errors:
            raise FitParseError(
                f"Couldn't decode FIT file '{self._source_name}': {errors}"
            )

        return messages

    def _read_segments(
        self,
        start_index: int,
        count: int,
        pool_length: float,
    ) -> list[SegmentDTO]:
        segments: list[SegmentDTO] = []

        for index in range(start_index, start_index + count):
            record = self._lengths_by_index[index]
            length_type = record["length_type"]

            if length_type == "active":
                segment = ActiveSegmentDTO(
                    index=record["message_index"],
                    start_time=record["start_time"],
                    distance_meters=pool_length,
                    timer_time=record["total_timer_time"],
                    elapsed_time=record["total_elapsed_time"],
                    strokes=record["total_strokes"],
                    stroke_type=record["swim_stroke"],
                    avg_speed=record["avg_speed"],
                )
            elif length_type == "idle":
                segment = RestSegmentDTO(
                    index=record["message_index"],
                    start_time=record["start_time"],
                    timer_time=record["total_timer_time"],
                    elapsed_time=record["total_elapsed_time"],
                )
            else:
                raise FitParseError(f"Unsupported length type: {length_type}")

            segments.append(segment)

        return segments

    def _read_laps(self, pool_length: float) -> list[LapDTO]:
        laps: list[LapDTO] = []

        for record in self._msgs["lap_mesgs"]:
            segments = self._read_segments(
                start_index=record["first_length_index"],
                count=record["num_lengths"],
                pool_length=pool_length,
            )

            laps.append(
                LapDTO(
                    index=record["message_index"],
                    start_time=record["start_time"],
                    distance_meters=record["total_distance"],
                    timer_time=record["total_timer_time"],
                    elapsed_time=record["total_elapsed_time"],
                    avg_hr=record["avg_heart_rate"],
                    max_hr=record["max_heart_rate"],
                    total_strokes=record["total_strokes"],
                    lengths_no=record["num_lengths"],
                    active_lengths_no=record["num_active_lengths"],
                    segments=segments,
                )
            )

        return laps

    def read_activity(self) -> WorkoutDTO:
        sessions = self._msgs["session_mesgs"]

        if len(sessions) != 1:
            raise FitParseError(
                f"Expected exactly one session, found {len(sessions)}"
            )

        session = sessions[0]
        pool_length = float(session["pool_length"])

        return WorkoutDTO(
            source=WorkoutSourceDTO(
                provider="COROS",
                source_format="FIT",
                file_name=self._source_name,
            ),
            started_at=session["start_time"],
            sport=session["sport"],
            sub_sport=session["sub_sport"],
            summary=WorkoutSummaryDTO(
                distance_meters=session["total_distance"],
                timer_time=session["total_timer_time"],
                elapsed_time=session["total_elapsed_time"],
                avg_hr=session["avg_heart_rate"],
                max_hr=session["max_heart_rate"],
                calories=session["total_calories"],
                pool_length_meters=pool_length,
            ),
            laps=self._read_laps(pool_length),
        )
