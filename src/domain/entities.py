from dataclasses import dataclass
from typing import Optional
from datetime import datetime



@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    Contiene la lógica de negocio relacionada con productos.
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
        TODO: Implementar validaciones:
        - price debe ser mayor a 0
        - stock no puede ser negativo
        - name no puede estar vacío
        Lanza ValueError si alguna validación falla
        
        sol:
        compara el atributo price con 0, si es menor, arroja error
        compara el atributo stock con 0, si es menor, arroja error
        si la longitud del nombre es 0, arroja error
        
        de lo contrario, el producto es válido y se puede postear/usar en el sistema
        """
        pass  # Implementa aquí las validaciones
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if not self.name:
            raise ValueError("El nombre del producto no puede estar vacío")        
        
    
    
    def is_available(self) -> bool:
        """
        TODO: Retorna True si el producto tiene stock disponible
        
        sol:
        compara el stock del producto y si este es = a 0 lanza falso,
        de lo contrario retorna verdadero
        """
        pass
        if self.stock == 0:
            return False
        return True
    


    def reduce_stock(self, quantity: int) -> None:
        """
        TODO: Reduce el stock del producto
        - Valida que quantity sea positivo
        - Valida que haya suficiente stock
        - Lanza ValueError si no se puede reducir
        
        sol:
        compara el atributo quantity con 0, si es menor, arroja error
        averigua si quantity es mayor a stock del producto, si es mayor, arroja error
        
        si no cumple ningun condicional, la operacion es valida y reduce el stock y reporta
        
        """
        pass
        if quantity < 0:
            raise ValueError("La cantidad a reducir debe ser positiva")
        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible")
        self.stock -= quantity
        message = f"Stock reducido en {quantity}. Stock disponible: {self.stock}"
        print(message)
        
        

    def increase_stock(self, quantity: int) -> None:
        """
        TODO: Aumenta el stock del producto
        - Valida que quantity sea positivo
        
        sol:
        compara el atributo quantity con 0, si es menor, arroja error
        
        sino, incrementa y reporta
        """
        pass
        if quantity < 0:
                raise ValueError("La cantidad a incrementar debe ser positiva")
        self.stock += quantity
        message = f"Stock incrementado en {quantity}. Stock disponible: {self.stock}"
        print(message)





@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.
    """
    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime
    
    def __post_init__(self):
        """
        TODO: Implementar validaciones:
        - role debe ser 'user' o 'assistant'
        - message no puede estar vacío
        - session_id no puede estar vacío
        
        sol:
        compara el atributo role con 'user' y 'assistant', si no es ninguno de los dos, arroja error
        si la longitud del mensaje es 0, arroja error
        si la longitud del session_id es 0, arroja error
        """
        pass
        if self.role not in ['user', 'assistant']:
            raise ValueError("Acceso no autorizado. Rol incorrecto.")
        if not self.message:
            raise ValueError("Mensaje invalido, mensaje vacío")
        if not self.session_id:
            raise ValueError("ID de sesión invalido, ID vacío")
    
    
    
    def is_from_user(self) -> bool:
        """
        TODO: Retorna True si el mensaje es del usuario
        
        sol:
        valida si el rol del usuario es "user", si no, retorna False
        """
        pass
        if self.role == 'user':
            return True
        return False



    def is_from_assistant(self) -> bool:
        """
        TODO: Retorna True si el mensaje es del asistente
        
        sol:
        si el rol es asistente, retorna verdadero, de lo contrario, retorna False
        """
        pass
        if self.role == 'assistant':
            return True
        return False





@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    Mantiene los mensajes recientes para dar coherencia al chat.
    """
    messages: list[ChatMessage]
    max_messages: int = 6
    
    def get_recent_messages(self) -> list[ChatMessage]:
        """
        TODO: Retorna los últimos N mensajes (max_messages)
        Pista: Usa slicing de Python messages[-self.max_messages:]
        
        sol:
        recorre la lista de mensajes en reversa, y retorna los max_messages
        """
        pass
        return self.messages[-self.max_messages:]
    
    
    
    def format_for_prompt(self) -> str:
        """
        TODO: Formatea los mensajes para incluirlos en el prompt de IA
        Formato esperado:
        "Usuario: mensaje del usuario
        Asistente: respuesta del asistente
        Usuario: otro mensaje
        ..."
        
        Pista: Itera sobre get_recent_messages() y construye el string
        
        sol:
        usando la funcion anterior (is_from_user()) se detecta el origen "verbal" del mensaje y se utiliza
        para formatear el mensaje, contruyendo el string 
        """
        pass
        formatted_messages = []
        for msg in self.get_recent_messages():
            role = "Usuario" if msg.is_from_user() else "Asistente"
            formatted_messages.append(f"{role}: {msg.message}")
        return "\n".join(formatted_messages)

