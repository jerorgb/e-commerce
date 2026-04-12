"""
Objetos de Transferencia de Datos (DTOs) para la aplicación.

Este módulo define los DTOs utilizados para transferir datos entre capas
de la aplicación. Utiliza Pydantic para validación automática de tipos
y datos de entrada.
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime



class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos entre capas.

    Utilizado para operaciones CRUD de productos, validando automáticamente
    tipos de datos y reglas de negocio básicas.

    Attributes:
        id (Optional[int]): Identificador único del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio en dólares, debe ser mayor a 0.
        stock (int): Cantidad en inventario, no puede ser negativa.
        description (str): Descripción detallada del producto.
    """
    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str
    
    @validator('price')
    def price_must_be_positive(cls, v):
        """
        Valida que el precio sea mayor a cero.

        Args:
            v (float): Valor del precio a validar.

        Returns:
            float: El precio si es válido.

        Raises:
            ValueError: Si el precio es menor o igual a cero.
        """
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v
    
    
    
    @validator('stock')
    def stock_must_be_non_negative(cls, v):
        """
        Valida que el stock no sea negativo.

        Args:
            v (int): Valor del stock a validar.

        Returns:
            int: El stock si es válido.

        Raises:
            ValueError: Si el stock es negativo.
        """
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v
    
    
    
    class Config:
        from_attributes = True  # Permite crear desde objetos ORM





class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes de chat del usuario.

    Utilizado en el endpoint de chat para validar y estructurar
    los mensajes entrantes del usuario.

    Attributes:
        session_id (str): Identificador único de la sesión de chat.
        message (str): Contenido del mensaje del usuario.
    """
    session_id: str
    message: str
    
    @validator('message')
    def message_not_empty(cls, v):
        """
        Valida que el mensaje no esté vacío.

        Args:
            v (str): Mensaje a validar.

        Returns:
            str: El mensaje si es válido.

        Raises:
            ValueError: Si el mensaje está vacío o contiene solo espacios.
        """
        if not v.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return v
    
    
    
    @validator('session_id')
    def session_id_not_empty(cls, v):
        """
        Valida que el ID de sesión no esté vacío.

        Args:
            v (str): ID de sesión a validar.

        Returns:
            str: El ID de sesión si es válido.

        Raises:
            ValueError: Si el ID de sesión está vacío o contiene solo espacios.
        """
        if not v.strip():
            raise ValueError("El ID de sesión no puede estar vacío")
        return v
        
        
        
class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar respuestas del chat al usuario.

    Utilizado para estructurar las respuestas que incluyen tanto
    el mensaje original del usuario como la respuesta generada por IA.

    Attributes:
        session_id (str): Identificador de la sesión de chat.
        user_message (str): Mensaje original del usuario.
        assistant_message (str): Respuesta generada por la IA.
        timestamp (datetime): Fecha y hora de la respuesta.
    """
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime



class ChatHistoryDTO(BaseModel):
    """
    DTO para mostrar el historial de mensajes de chat.

    Utilizado para representar mensajes históricos en listados
    y consultas de historial de conversaciones.

    Attributes:
        id (int): Identificador único del mensaje.
        role (str): Rol del emisor ('user' o 'assistant').
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """
    id: int
    role: str
    message: str
    timestamp: datetime
    
    class Config:
        from_attributes = True




