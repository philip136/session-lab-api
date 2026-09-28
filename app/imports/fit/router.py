from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.imports.errors import EmptyFitFileError
from app.imports.fit.request import ImportFitRequest
from app.imports.fit.response import ImportFitResponse
from app.imports.service import ImportServiceDep
from app.parsers.fit_parser import FitParseError

router = APIRouter()


@router.post(
    "/fit",
    response_model=ImportFitResponse,
    status_code=status.HTTP_201_CREATED,
)
async def import_fit(
    file: Annotated[UploadFile, File()],
    service: ImportServiceDep,
) -> ImportFitResponse:
    request = ImportFitRequest(
        file_name=file.filename,
        content=await file.read(),
    )

    try:
        return service.import_fit(request)
    except EmptyFitFileError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except FitParseError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
