"""
Entidades del dominio para el sistema de e-commerce con chat IA.

Este módulo define las entidades principales del negocio: Product, ChatMessage y ChatContext.
Estas clases encapsulan la lógica de negocio y validaciones relacionadas con productos
y conversaciones de chat.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime



@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.

    Esta clase encapsula la lógica de negocio relacionada con productos,
    incluyendo validaciones de precio, stock y disponibilidad.

    Attributes:
        id (Optional[int]): Identificador único del producto
        name (str): Nombre del producto
        brand (str): Marca del producto
        category (str): Categoría del producto
        size (str): Talla del producto
        color (str): Color del producto
        price (float): Precio en dólares, debe ser mayor a 0
        stock (int): Cantidad disponible en inventario
        description (str): Descripción detallada del producto
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str
    
    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.

        Realiza validaciones de negocio para asegurar la integridad de los datos:
        - El precio debe ser mayor a 0
        - El stock no puede ser negativo
        - El nombre no puede estar vacío

        Raises:
            ValueError: Si alguna validación falla.
        """
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if not self.name:
            raise ValueError("El nombre del producto no puede estar vacío")        
        
    
    
    def is_available(self) -> bool:
        """
        Verifica si el producto está disponible para venta.

        Un producto se considera disponible si tiene stock mayor a cero.

        Returns:
            bool: True si el producto tiene stock disponible, False en caso contrario.
        """
        if self.stock == 0:
            return False
        return True
    


    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto en la cantidad especificada.

        Este método valida que haya suficiente stock antes de reducir.
        Se usa típicamente cuando se realiza una venta.

        Args:
            quantity (int): Cantidad a reducir del stock. Debe ser positivo.

        Raises:
            ValueError: Si quantity es negativo o mayor al stock disponible.
        """
        if quantity < 0:
            raise ValueError("La cantidad a reducir debe ser positiva")
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible")
        self.stock -= quantity
        message = f"Stock reducido en {quantity}. Stock disponible: {self.stock}"
        print(message)
        
        

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto en la cantidad especificada.

        Este método valida que la cantidad sea positiva antes de incrementar.
        Se usa típicamente cuando se recibe nuevo inventario.

        Args:
            quantity (int): Cantidad a incrementar del stock. Debe ser positivo.

        Raises:
            ValueError: Si quantity es negativo.
        """
        self.stock += quantity
        message = f"Stock incrementado en {quantity}. Stock disponible: {self.stock}"
        print(message)





@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.

    Esta clase encapsula la información de un mensaje intercambiado
    entre el usuario y el asistente de IA.

    Attributes:
        id (Optional[int]): Identificador único del mensaje
        session_id (str): Identificador de la sesión de chat
        role (str): Rol del emisor ('user' o 'assistant')
        message (str): Contenido del mensaje
        timestamp (datetime): Fecha y hora del mensaje
    """
    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime
    
    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.

        Realiza validaciones de negocio para asegurar la integridad de los datos:
        - El rol debe ser 'user' o 'assistant'
        - El mensaje no puede estar vacío
        - El session_id no puede estar vacío

        Raises:
            ValueError: Si alguna validación falla.
        """
        if self.role not in ['user', 'assistant']:
            raise ValueError("Acceso no autorizado. Rol incorrecto.")
        if not self.message:
            raise ValueError("Mensaje invalido, mensaje vacío")
        if not self.session_id:
            raise ValueError("ID de sesión invalido, ID vacío")
    
    
    
    def is_from_user(self) -> bool:
        """
        Verifica si el mensaje proviene del usuario.

        Returns:
            bool: True si el rol es 'user', False en caso contrario.
        """
        if self.role == 'user':
            return True
        return False



    def is_from_assistant(self) -> bool:
        """
        Verifica si el mensaje proviene del asistente.

        Returns:
            bool: True si el rol es 'assistant', False en caso contrario.
        """
        if self.role == 'assistant':
            return True
        return False





@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.

    Mantiene los mensajes recientes para dar coherencia al chat con IA.
    Limita el número de mensajes para evitar prompts demasiado largos.

    Attributes:
        messages (list[ChatMessage]): Lista de mensajes de la conversación
        max_messages (int): Número máximo de mensajes a mantener (por defecto 6)
    """
    messages: list[ChatMessage]
    max_messages: int = 6
    
    def get_recent_messages(self) -> list[ChatMessage]:
        """
        Obtiene los mensajes más recientes de la conversación.

        Retorna los últimos N mensajes según max_messages para mantener
        el contexto sin sobrecargar el prompt de IA.

        Returns:
            list[ChatMessage]: Lista con los mensajes más recientes.
        """
        return self.messages[-self.max_messages:]
    
    
    
    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes recientes para incluirlos en el prompt de IA.

        Convierte los mensajes en un formato legible para el modelo de IA,
        diferenciando entre mensajes del usuario y del asistente.

        Returns:
            str: String formateado con los mensajes recientes.

        Example:
            >>> context = ChatContext([...])
            >>> print(context.format_for_prompt())
            Usuario: ¿Qué productos tienes?
            Asistente: Tengo varios productos disponibles...
        """
        formatted_messages = []
        for msg in self.get_recent_messages():
            role = "Usuario" if msg.is_from_user() else "Asistente"
            formatted_messages.append(f"{role}: {msg.message}")
        return "\n".join(formatted_messages)

