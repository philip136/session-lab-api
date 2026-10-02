import asyncio

from garmin_fit_sdk import Decoder, Stream

from backend.infra.database.entities.workout import LapEntity, SegmentEntity, WorkoutEntity
from backend.infra.fit.errors import FitParseError


class FitParser:
    @classmethod
    async def parse(cls, content: bytes) -> WorkoutEntity:
        def _sync_parse(content) -> WorkoutEntity:
            msgs = cls._decode(content)
            session = msgs["session_mesgs"][0]
            pool_length = float(session["pool_length"])
            return WorkoutEntity(
                started_at=session["start_time"],
                sport=session["sport"],
                sub_sport=session["sub_sport"],
                meters=session["total_distance"],
                duration_seconds=session["total_timer_time"],
                elapsed_seconds=session["total_elapsed_time"],
                avg_hr=session["avg_heart_rate"],
                max_hr=session["max_heart_rate"],
                calories=session["total_calories"],
                pool_length_meters=pool_length,
                laps=cls._read_laps(
                    records=msgs["lap_mesgs"],
                    pool_length=pool_length,
                    lengths_by_index={
                        rec["message_index"]: rec for rec in msgs["length_mesgs"]
                    }
                )
            )
        return await asyncio.to_thread(_sync_parse, content)

    @staticmethod
    def _decode(content: bytes):
        stream = Stream.from_byte_array(bytearray(content))
        messages, errors = Decoder(stream).read(enable_crc_check=True)

        if errors:
            raise FitParseError(f"Couldn't decode FIT file: {errors}")
        return messages

    @staticmethod
    def _read_laps(
        records: list[dict],
        lengths_by_index: dict[int, dict],
        pool_length: float
    ) -> list[LapEntity]:
        laps = []

        for rec in records:
            laps.append(
                LapEntity(
                    index=rec["message_index"],
                    started_at=rec["start_time"],
                    meters=rec["total_distance"],
                    duration_seconds=rec["total_timer_time"],
                    elapsed_seconds=rec["total_elapsed_time"],
                    avg_hr=rec["avg_heart_rate"],
                    max_hr=rec["max_heart_rate"],
                    stroke_count=rec["total_strokes"],
                    length_count=rec["num_lengths"],
                    active_length_count=rec["num_active_lengths"],
                    segments=FitParser._read_segments(
                        start_index=rec["first_length_index"],
                        count=rec["num_lengths"],
                        lengths_by_index=lengths_by_index,
                        pool_length=pool_length
                    )
                )
            )
        return laps

    @staticmethod
    def _read_segments(
        start_index: int,
        count: int,
        lengths_by_index: dict[int, dict],
        pool_length: float,
    ) -> list[SegmentEntity]:
        segments = []

        for index in range(start_index, start_index + count):
            rec = lengths_by_index[index]
            data = {
                "index": rec["message_index"],
                "started_at": rec["start_time"],
                "duration_seconds": rec["total_timer_time"],
                "elapsed_seconds": rec["total_elapsed_time"]
            }

            match rec["length_type"]:
                case "active":
                    segment = SegmentEntity(
                        type="active",
                        meters=pool_length,
                        stroke_count=rec["total_strokes"],
                        stroke_type=rec["swim_stroke"],
                        **data
                    )
                case "idle":
                    segment = SegmentEntity(type="rest", **data)

            segments.append(segment)
        return segments
