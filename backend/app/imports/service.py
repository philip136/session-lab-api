from typing import Annotated

from fastapi import Depends

from backend.api.fit.schemas.fit import ImportFitRequest, ImportFitResponse
from backend.app.imports.errors import InvalidFitFileError
from backend.infra.database.repos.workout import WorkoutRepo
from backend.infra.fit.errors import FitParseError
from backend.infra.fit.parser import FitParser


class ImportFitService:
    def __init__(self, repo: Annotated[WorkoutRepo, Depends()]):
        self._repo = repo

    async def import_fit(self, req: ImportFitRequest) -> ImportFitResponse:
        try:
            workout = await FitParser.parse(req.content)
        except FitParseError as exc:
            raise InvalidFitFileError() from exc

        await self._repo.save(workout)
        return ImportFitResponse(workout_id=workout.id)
