from sqlalchemy.orm import Session

from app.database.db import Base


class Repository[ModelT: Base]:
    def __init__(self, session: Session, model: type[ModelT]):
        self._session = session
        self._model = model

    def save(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        return entity

    def get(self, entity_id: int) -> ModelT | None:
        return self._session.get(self._model, entity_id)

    def delete(self, entity: ModelT) -> None:
        self._session.delete(entity)
