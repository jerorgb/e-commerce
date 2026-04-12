"""
Servicios de aplicación para la gestión de productos.

Este módulo contiene la lógica de aplicación para operaciones relacionadas
con productos, incluyendo búsqueda, creación, actualización y eliminación.
Actúa como intermediario entre la capa de presentación y la capa de dominio.
"""

from typing import List, Optional, Dict, Any
from src.domain.repositories import IProductRepository
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError, InvalidProductDataError
from src.application.dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para gestionar productos.

    Este servicio coordina las operaciones CRUD de productos entre la capa
    de presentación y la capa de infraestructura. Implementa la lógica de
    negocio de aplicación como validaciones, conversiones DTO/entidad y
    manejo de errores.

    Attributes:
        product_repository (IProductRepository): Repositorio de productos
                                                 inyectado por dependencia.
    """
    
    def __init__(self, product_repository: IProductRepository):
        """
        Inicializa el servicio con sus dependencias.

        Args:
            product_repository (IProductRepository): Implementación del repositorio
                                                    de productos para acceso a datos.
        """
        self.product_repository = product_repository
    
    
    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos disponibles en el sistema.

        Returns:
            List[ProductDTO]: Lista completa de productos registrados,
                             convertidos a DTOs para la presentación.
        """
        products = self.product_repository.get_all()
        return [self._to_dto(product) for product in products]
    
    
    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Busca un producto específico por su identificador único.

        Args:
            product_id (int): Identificador único del producto a buscar.

        Returns:
            ProductDTO: DTO del producto encontrado.

        Raises:
            ProductNotFoundError: Si no existe un producto con el ID especificado.
        """
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return self._to_dto(product)
    
    
    def search_products(self, filters: Dict[str, Any]) -> List[ProductDTO]:
        """
        Filtra productos según múltiples criterios de búsqueda.

        Aplica filtros opcionales como marca, categoría, precio, color y texto
        de búsqueda. Los filtros se aplican de manera acumulativa.

        Args:
            filters (Dict[str, Any]): Diccionario con criterios de filtrado.
                Claves soportadas:
                - 'brand': str - Filtrar por marca
                - 'category': str - Filtrar por categoría
                - 'color': str - Filtrar por color
                - 'min_price': float - Precio mínimo
                - 'max_price': float - Precio máximo
                - 'search_text': str - Buscar en nombre y descripción

        Returns:
            List[ProductDTO]: Lista de productos que coinciden con los filtros aplicados.
        """
        all_products = self.product_repository.get_all()
        filtered_products = all_products
        
        # Filtro por marca
        if 'brand' in filters and filters['brand']:
            filtered_products = [p for p in filtered_products if p.brand.lower() == filters['brand'].lower()]
        
        # Filtro por categoría
        if 'category' in filters and filters['category']:
            filtered_products = [p for p in filtered_products if p.category.lower() == filters['category'].lower()]
        
        # Filtro por color
        if 'color' in filters and filters['color']:
            filtered_products = [p for p in filtered_products if p.color.lower() == filters['color'].lower()]
        
        # Filtro por rango de precio
        if 'min_price' in filters and filters['min_price'] is not None:
            filtered_products = [p for p in filtered_products if p.price >= filters['min_price']]
        
        if 'max_price' in filters and filters['max_price'] is not None:
            filtered_products = [p for p in filtered_products if p.price <= filters['max_price']]
        
        # Filtro por búsqueda de texto en nombre o descripción
        if 'search_text' in filters and filters['search_text']:
            search_term = filters['search_text'].lower()
            filtered_products = [p for p in filtered_products 
                               if search_term in p.name.lower() or search_term in p.description.lower()]
        
        return [self._to_dto(product) for product in filtered_products]
    
    
    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto en el sistema.

        Convierte el DTO a entidad de dominio, valida los datos y guarda
        el producto en el repositorio.

        Args:
            product_dto (ProductDTO): DTO con los datos del producto a crear.

        Returns:
            ProductDTO: DTO del producto creado con ID asignado.

        Raises:
            InvalidProductDataError: Si los datos del producto no cumplen
                                    las reglas de validación del dominio.
        """
        try:
            # Convertir DTO a entidad para validar los datos de dominio
            product_entity = self._to_entity(product_dto)
            
            # Guardar el producto en el repositorio
            created_product = self.product_repository.save(product_entity)
            
            return self._to_dto(created_product)
        except ValueError as e:
            raise InvalidProductDataError(str(e))
    
    
    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """
        Actualiza un producto existente con nuevos datos.

        Verifica que el producto exista, valida los nuevos datos y actualiza
        el producto en el repositorio.

        Args:
            product_id (int): Identificador del producto a actualizar.
            product_dto (ProductDTO): DTO con los nuevos datos del producto.

        Returns:
            ProductDTO: DTO del producto actualizado.

        Raises:
            ProductNotFoundError: Si no existe un producto con el ID especificado.
            InvalidProductDataError: Si los nuevos datos no cumplen las validaciones.
        """
        # Verificar que el producto existe
        existing_product = self.product_repository.get_by_id(product_id)
        if existing_product is None:
            raise ProductNotFoundError(product_id)
        
        try:
            # Crear la entidad actualizada manteniendo el ID
            product_dto.id = product_id
            updated_product_entity = self._to_entity(product_dto)
            
            # Guardar los cambios
            updated_product = self.product_repository.save(updated_product_entity)
            
            return self._to_dto(updated_product)
        except ValueError as e:
            raise InvalidProductDataError(str(e))
    
    
    def delete_product(self, product_id: int) -> None:
        """
        Elimina un producto del sistema permanentemente.

        Verifica que el producto exista antes de eliminarlo para asegurar
        integridad de datos.

        Args:
            product_id (int): Identificador del producto a eliminar.

        Raises:
            ProductNotFoundError: Si no existe un producto con el ID especificado.
        """
        # Verificar que el producto existe antes de eliminarlo
        existing_product = self.product_repository.get_by_id(product_id)
        if existing_product is None:
            raise ProductNotFoundError(product_id)
        
        self.product_repository.delete(product_id)
    
    
    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene únicamente los productos que tienen stock disponible.

        Filtra todos los productos para retornar solo aquellos con stock > 0.

        Returns:
            List[ProductDTO]: Lista de productos disponibles para venta.
        """
        all_products = self.product_repository.get_all()
        available_products = [p for p in all_products if p.is_available()]
        return [self._to_dto(product) for product in available_products]
    
    
    # Métodos auxiliares privados
    
    def _to_entity(self, product_dto: ProductDTO) -> Product:
        """
        Convierte un DTO de producto a entidad de dominio.

        Args:
            product_dto (ProductDTO): DTO a convertir.

        Returns:
            Product: Entidad de dominio con los datos del DTO.
        """
        return Product(
            id=product_dto.id,
            name=product_dto.name,
            brand=product_dto.brand,
            category=product_dto.category,
            size=product_dto.size,
            color=product_dto.color,
            price=product_dto.price,
            stock=product_dto.stock,
            description=product_dto.description
        )
    
    
    def _to_dto(self, product_entity: Product) -> ProductDTO:
        """
        Convierte una entidad de dominio a DTO de producto.

        Args:
            product_entity (Product): Entidad de dominio a convertir.

        Returns:
            ProductDTO: DTO con los datos de la entidad.
        """
        return ProductDTO(
            id=product_entity.id,
            name=product_entity.name,
            brand=product_entity.brand,
            category=product_entity.category,
            size=product_entity.size,
            color=product_entity.color,
            price=product_entity.price,
            stock=product_entity.stock,
            description=product_entity.description
        )
