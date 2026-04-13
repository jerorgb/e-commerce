from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """
    Implementación SQL del repositorio de chat usando SQLAlchemy.

    Convierte entre modelos ORM (ChatMemoryModel) y entidades del dominio (ChatMessage).
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje de chat en la base de datos.

        Args:
            message (ChatMessage): Entidad de mensaje a guardar.

        Returns:
            ChatMessage: Entidad guardada con ID asignado.
        """
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)
        self.db.commit()
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        Obtiene el historial de mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión de chat.
            limit (Optional[int]): Límite de mensajes a retornar.

        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        query = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id)

        if limit:
            query = query.limit(limit)

        models = query.order_by(ChatMemoryModel.timestamp.desc()).all()
        entities = [self._model_to_entity(model) for model in models]

        # Invertir para obtener orden cronológico (más antiguos primero)
        entities.reverse()
        return entities

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión a eliminar.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        models = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).all()
        count = len(models)

        for model in models:
            self.db.delete(model)

        self.db.commit()
        return count

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los N mensajes más recientes de una sesión.

        Args:
            session_id (str): Identificador de la sesión de chat.
            count (int): Número de mensajes recientes a obtener.

        Returns:
            List[ChatMessage]: Lista con los mensajes más recientes en orden cronológico.
        """
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )

        entities = [self._model_to_entity(model) for model in models]

        # Invertir para obtener orden cronológico (más antiguos primero)
        entities.reverse()
        return entities

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un modelo ORM a entidad del dominio.

        Args:
            model (ChatMemoryModel): Modelo ORM a convertir.

        Returns:
            ChatMessage: Entidad del dominio.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """
        Convierte una entidad del dominio a modelo ORM.

        Args:
            entity (ChatMessage): Entidad del dominio a convertir.

        Returns:
            ChatMemoryModel: Modelo ORM.
        """
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )
