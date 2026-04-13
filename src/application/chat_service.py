from typing import List, Optional, Dict, Any
from datetime import datetime
from src.domain.repositories import IChatRepository
from src.domain.entities import ChatContext, ChatMessage
from src.domain.exceptions import ChatServiceError
from src.application.dtos import ChatHistoryDTO, ChatMessageRequestDTO, ChatMessageResponseDTO

class ChatService:
    """
    Servicio de aplicación para gestionar chats.
    Coordina las operaciones de chats entre capas.
    """
    
    def __init__(self, chat_repository: IChatRepository):
        """
        Constructor con inyección de dependencias.
        
        Args:
            chat_repository: Implementación del repositorio de chat
        """
        self.chat_repository = chat_repository
    
    
    def save_message(self, session_id: str, role: str, message: str) -> ChatMessage:
        """
        Guarda un nuevo mensaje en el chat.
        
        Args:
            session_id: ID de la sesión de chat
            role: Rol del mensaje ('user' o 'assistant')
            message: Contenido del mensaje
            
        Returns:
            ChatMessage guardado
            
        Raises:
            ChatServiceError: Si hay error al guardar
        """
        try:
            chat_message = ChatMessage(
                id=None,
                session_id=session_id,
                role=role,
                message=message,
                timestamp=datetime.now()
            )
            return self.chat_repository.save_message(chat_message)
        except ValueError as e:
            raise ChatServiceError(f"Error al guardar mensaje: {str(e)}")
    
    
    def get_session_history(self, session_id: str, limit: int = 50) -> List[ChatMessage]:
        """
        Obtiene el histórico de mensajes de una sesión.
        
        Args:
            session_id: ID de la sesión
            limit: Número máximo de mensajes a retornar
            
        Returns:
            Lista de ChatMessages de la sesión
        """
        return self.chat_repository.get_session_history(session_id, limit=limit)
    
    
    def delete_session_history(self, session_id: str) -> None:
        """
        Elimina todo el histórico de una sesión.
        
        Args:
            session_id: ID de la sesión a eliminar
        """
        self.chat_repository.delete_session_history(session_id)
    
    
    def get_recent_messages(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión.
        
        Args:
            session_id: ID de la sesión
            limit: Número de mensajes recientes a obtener
            
        Returns:
            Lista de últimos mensajes
        """
        return self.chat_repository.get_recent_messages(session_id, limit=limit)