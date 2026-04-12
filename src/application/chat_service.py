from datetime import datetime
from typing import List

from src.application.dtos import ChatHistoryDTO, ChatMessageRequestDTO, ChatMessageResponseDTO
from src.domain.entities import ChatContext, ChatMessage, Product
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository


class ChatService:
    """Servicio de aplicación para gestionar el chat con IA."""

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service,
    ):
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """Procesa un mensaje de usuario y retorna la respuesta del asistente."""
        try:
            # 1. Obtener todos los productos del repositorio
            products: List[Product] = self.product_repository.get_all()

            # 2. Obtener historial reciente (últimos 6 mensajes)
            recent_messages = self.chat_repository.get_recent_messages(request.session_id, 6)

            # 3. Crear ChatContext con el historial
            chat_context = ChatContext(messages=recent_messages)

            # 4. Llamar al servicio de IA para generar la respuesta
            assistant_text = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=chat_context,
            )

            # 5. Guardar mensaje del usuario en el repositorio
            now = datetime.utcnow()
            user_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=now,
            )
            self.chat_repository.save_message(user_message)

            # 6. Guardar respuesta del asistente en el repositorio
            assistant_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_text,
                timestamp=datetime.utcnow(),
            )
            self.chat_repository.save_message(assistant_message)

            # 7. Retornar la respuesta como DTO
            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_text,
                timestamp=assistant_message.timestamp,
            )

        except Exception as exc:
            raise ChatServiceError(f"Error al procesar el mensaje: {exc}") from exc

    def get_session_history(self, session_id: str, limit: int = 50) -> List[ChatHistoryDTO]:
        """Obtiene el historial de chat de una sesión."""
        history = self.chat_repository.get_session_history(session_id, limit)
        return [self._to_history_dto(message) for message in history]

    def clear_session_history(self, session_id: str) -> int:
        """Elimina el historial completo de una sesión."""
        return self.chat_repository.delete_session_history(session_id)

    def _to_history_dto(self, message: ChatMessage) -> ChatHistoryDTO:
        return ChatHistoryDTO(
            id=message.id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp,
        )
