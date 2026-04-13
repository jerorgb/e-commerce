from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage



class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.
    Las implementaciones concretas estarán en la capa de infraestructura.
    """
    
    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        TODO: Define el método para obtener todos los productos
        No implementes nada, solo la firma del método
        """
        pass
    
    
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        TODO: Define el método para obtener un producto por ID
        Retorna None si no existe
        
        sol:
        obtiene todos los productos con get_all(), despues itera la lista, si no encuentra un match con el ID
        reporta con print y retorna None 
        """
        pass
        all = self.get_all()
        for product in all:
            if product.id == product_id:
                return product
            else:
                print("ID de producto no encontrado")
                return None
    
    
    
    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """TODO: Obtiene productos de una marca específica
        
        sol:
        obtiene todos los productos con get_all(), despues itera la lista, si no encuentra un match con la marca/brand
        reporta con print y retorna None 
        """
        pass
        all = self.get_all()
        for product in all:
            if product.brand == brand:
                return product
            else:
                print("Marca de producto no encontrada")
                return None
    
    


class IChatRepository(ABC):
    """
    Interface para gestionar el historial de conversaciones.
    """
    
    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        TODO: Guarda un mensaje en el historial
        Retorna el mensaje guardado con su ID
        
        sol:
        recolecta el mensaje y le incorpora un id para guardarlo, despues reporta con print el ID del mensaje guardado
        """
        pass
        message.id = message.id ### check on future where does new id gonna come from, user interface maybe?
        print(f"Mensaje guardado con ID: {message.id}")
    
    
    
    @abstractmethod
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        TODO: Obtiene el historial completo de una sesión
        Si limit está definido, retorna solo los últimos N mensajes
        Los mensajes deben estar en orden cronológico (más antiguos primero)
        
        sol:
        obtiene los mensajes de un usuario, y los selecciona/filtra por session_id,
        si el limit no es None, se detiene despues de obtener N mensajes,
        y los retorna en orden cronologico
        """
        pass
        out = []
        stopper = limit if limit is not None else float('inf')
        for msg in self.get_all_messages():
            if msg.session_id == session_id:
                out.append(msg)
                if len(out) >= stopper:
                    break
        return out



    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        TODO: Elimina todo el historial de una sesión
        Retorna la cantidad de mensajes eliminados
        
        sol:
        obtiene los mensajes de un usuario, y los selecciona/filtra por session_id,
        los elimina de su historial y reporta la cantidad eliminada
        """
        pass
        out = []
        for msg in self.get_all_messages():
            if msg.session_id == session_id:
                out.append(msg)
                self.delete_message(msg.id) ### check on future where does delete_message come from, user interface maybe?
        return len(out)



    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        TODO: Obtiene los últimos N mensajes de una sesión
        Crucial para mantener el contexto conversacional
        Retorna en orden cronológico
        
        sol:
        obtiene los mensajes del usuario, y los selecciona/filtra por session_id,
        los ordena por fecha y hora, y retorna los últimos N mensajes
        """
        pass
        select = []
        out = []
        for msg in self.get_all_messages():
            if msg.session_id == session_id:
                select.append(msg)
        
        for msg in select[-count:]:
            out.append(msg)
        return out
