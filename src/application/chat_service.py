"""
Servicios de aplicación para la gestión del chat con IA.

Este módulo contiene la lógica de aplicación para el procesamiento de mensajes
de chat, integración con servicios de IA y gestión del historial de conversaciones.
Coordina entre repositorios de productos, chat y servicios de IA.
"""

from datetime import datetime
from typing import List

from src.application.dtos import ChatHistoryDTO, ChatMessageRequestDTO, ChatMessageResponseDTO
from src.domain.entities import ChatContext, ChatMessage, Product
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository


class ChatService:
    """
    Servicio de aplicación para gestionar el chat con IA.

    Este servicio orquesta la interacción entre el repositorio de productos,
    el repositorio de chat y el servicio de IA de Gemini para proporcionar
    respuestas contextuales a los usuarios sobre productos disponibles.

    Attributes:
        product_repository (IProductRepository): Repositorio para acceder a productos.
        chat_repository (IChatRepository): Repositorio para gestionar historial de chat.
        ai_service: Servicio de IA para generar respuestas (GeminiService).
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service,
    ):
        """
        Inicializa el servicio con sus dependencias.

        Args:
            product_repository (IProductRepository): Repositorio de productos.
            chat_repository (IChatRepository): Repositorio de mensajes de chat.
            ai_service: Servicio de IA para generar respuestas.
        """
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta con IA.

        Este método realiza el flujo completo de procesamiento de chat:
        1. Obtiene productos disponibles del repositorio
        2. Recupera historial reciente de la conversación
        3. Genera respuesta contextual usando IA con productos y contexto
        4. Guarda tanto el mensaje del usuario como la respuesta
        5. Retorna la respuesta formateada

        Args:
            request (ChatMessageRequestDTO): Mensaje del usuario con session_id.

        Returns:
            ChatMessageResponseDTO: Respuesta generada por la IA con timestamp.

        Raises:
            ChatServiceError: Si hay error al procesar el mensaje o comunicarse con IA.
        """
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
        """
        Obtiene el historial completo de mensajes de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión de chat.
            limit (int): Número máximo de mensajes a retornar. Por defecto 50.

        Returns:
            List[ChatHistoryDTO]: Lista de mensajes del historial en orden cronológico.
        """
        history = self.chat_repository.get_session_history(session_id, limit)
        return [self._to_history_dto(message) for message in history]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de mensajes de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión a limpiar.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        return self.chat_repository.delete_session_history(session_id)

    def _to_history_dto(self, message: ChatMessage) -> ChatHistoryDTO:
        """
        Convierte una entidad ChatMessage a DTO de historial.

        Args:
            message (ChatMessage): Entidad de mensaje a convertir.

        Returns:
            ChatHistoryDTO: DTO con los datos del mensaje para presentación.
        """
        return ChatHistoryDTO(
            id=message.id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp,
        )
