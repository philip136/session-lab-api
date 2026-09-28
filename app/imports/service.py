import logging
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database.deps import session_dep
from app.imports.errors import EmptyFitFileError
from app.imports.fit.request import ImportFitRequest
from app.imports.fit.response import ImportFitResponse
from app.parsers.fit_parser import FitParser
from app.storage.files import remove_file, save_bytes
from app.workouts.models import WorkoutDBO
from app.workouts.repository import WorkoutRepository

RAW_DIRECTORY = Path(settings.raw_data_dir)
logger = logging.getLogger(__name__)


class ImportService:
    def __init__(self, session: Session):
        self._session = session
        self._workouts = WorkoutRepository(session)

    def import_fit(self, request: ImportFitRequest) -> ImportFitResponse:
        logger.info("FIT import started: file=%s", request.file_name)
        if not request.content:
            raise EmptyFitFileError("Uploaded FIT file is empty")

        path = save_bytes(
            content=request.content,
            directory=RAW_DIRECTORY,
            suffix=".fit",
        )

        try:
            workout_dto = FitParser(
                path=path,
                source_name=request.file_name,
            ).read_activity()

            workout = WorkoutDBO.from_dto(
                dto=workout_dto,
                raw_file_path=str(path),
            )

            self._workouts.save(workout)
            self._session.commit()
            logger.info(
                "FIT import completed: file=%s workout_id=%s",
                request.file_name,
                workout.id,
            )
            return ImportFitResponse(workout_id=workout.id)
        except Exception:
            logger.exception(
                "FIT import failed: file=%s",
                request.file_name,
            )
            remove_file(path)
            raise


ImportServiceDep = Annotated[
    ImportService,
    Depends(session_dep(ImportService)),
]
