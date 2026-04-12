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
    
    
