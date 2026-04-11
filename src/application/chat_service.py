from typing import List, Optional, Dict, Any
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
        self.chat_repository = chat_repository