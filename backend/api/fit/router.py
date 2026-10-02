from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from backend.api.fit.schemas.fit import ImportFitRequest, ImportFitResponse
from backend.app.fit.service import ImportFitService

router = APIRouter(prefix="/fit", tags=["Fit"])

@router.post(
    "/import",
    response_model=ImportFitResponse,
    status_code=status.HTTP_201_CREATED
)
async def import_fit(
    file: Annotated[UploadFile, File()],
    service: Annotated[ImportFitService, Depends()]
) -> ImportFitResponse:
    request = ImportFitRequest(content=await file.read())
    return await service.import_fit(request)


