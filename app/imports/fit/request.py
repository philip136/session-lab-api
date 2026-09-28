from pydantic import BaseModel


class ImportFitRequest(BaseModel):
    file_name: str
    content: bytes
