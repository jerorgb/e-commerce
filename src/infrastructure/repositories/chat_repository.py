from typing import List

from sqlalchemy.orm import Session

from src.domain.entities import ChatMessage as ChatMessageEntity
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """Repositorio de chat basado en SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def save_message(self, message: ChatMessageEntity) -> ChatMessageEntity:
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: int = None) -> List[ChatMessageEntity]:
        query = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).order_by(ChatMemoryModel.timestamp.desc())
        if limit is not None:
            query = query.limit(limit)
        models = query.all()
        models.reverse()
        return [self._model_to_entity(model) for model in models]

    def delete_session_history(self, session_id: str) -> int:
        models = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).all()
        deleted_count = len(models)
        for model in models:
            self.db.delete(model)
        self.db.commit()
        return deleted_count

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessageEntity]:
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )
        models.reverse()
        return [self._model_to_entity(model) for model in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessageEntity:
        return ChatMessageEntity(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessageEntity) -> ChatMemoryModel:
        model = ChatMemoryModel(
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )
        if entity.id is not None:
            model.id = entity.id
        return model
