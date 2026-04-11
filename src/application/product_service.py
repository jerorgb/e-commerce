from typing import List, Optional, Dict, Any
from src.domain.repositories import IProductRepository
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError, InvalidProductDataError
from src.application.dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para gestionar productos.
    Coordina las operaciones de productos entre la capa de presentación y la de data.
    """
    
    def __init__(self, product_repository: IProductRepository):
        """
        Constructor con inyección de dependencias.
        
        Args:
            product_repository: Implementación del repositorio de productos
        """
        self.product_repository = product_repository
    
    
    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos disponibles.
        
        Returns:
            Lista de ProductDTOs con todos los productos registrados
        """
        products = self.product_repository.get_all()
        return [self._to_dto(product) for product in products]
    
    
    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Busca un producto por su ID.
        
        Args:
            product_id: ID del producto a buscar
            
        Returns:
            ProductDTO del producto encontrado
            
        Raises:
            ProductNotFoundError: Si el producto no existe
        """
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return self._to_dto(product)
    
    
    def search_products(self, filters: Dict[str, Any]) -> List[ProductDTO]:
        """
        Filtra productos según criterios específicos.
        
        Args:
            filters: Diccionario con criterios de filtrado
                     Puede contener: 'brand', 'category', 'min_price', 'max_price', 'color', etc.
        
        Returns:
            Lista de ProductDTOs que coinciden con los filtros
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
        Crea un nuevo producto a partir de un DTO.
        
        Args:
            product_dto: DTO con los datos del producto a crear
            
        Returns:
            ProductDTO del producto creado (con ID asignado)
            
        Raises:
            InvalidProductDataError: Si los datos del producto son inválidos
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
        Actualiza un producto existente.
        
        Args:
            product_id: ID del producto a actualizar
            product_dto: DTO con los nuevos datos del producto
            
        Returns:
            ProductDTO del producto actualizado
            
        Raises:
            ProductNotFoundError: Si el producto no existe
            InvalidProductDataError: Si los datos del producto son inválidos
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
        Elimina un producto del sistema.
        
        Args:
            product_id: ID del producto a eliminar
            
        Raises:
            ProductNotFoundError: Si el producto no existe
        """
        # Verificar que el producto existe antes de eliminarlo
        existing_product = self.product_repository.get_by_id(product_id)
        if existing_product is None:
            raise ProductNotFoundError(product_id)
        
        self.product_repository.delete(product_id)
    
    
    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene los productos que tienen stock disponible.
        
        Returns:
            Lista de ProductDTOs de productos con stock > 0
        """
        all_products = self.product_repository.get_all()
        available_products = [p for p in all_products if p.is_available()]
        return [self._to_dto(product) for product in available_products]
    
    
    # Métodos auxiliares privados
    
    def _to_entity(self, product_dto: ProductDTO) -> Product:
        """
        Convierte un ProductDTO a una entidad Product.
        
        Args:
            product_dto: DTO a convertir
            
        Returns:
            Entidad Product
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
        Convierte una entidad Product a un ProductDTO.
        
        Args:
            product_entity: Entidad a convertir
            
        Returns:
            DTO ProductDTO
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
