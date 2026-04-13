from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementación SQL del repositorio de productos usando SQLAlchemy.

    Convierte entre modelos ORM (ProductModel) y entidades del dominio (Product).
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy.
        """
        self.db = db

    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos de la base de datos.

        Returns:
            List[Product]: Lista completa de entidades de producto.
        """
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            Optional[Product]: Entidad de producto o None si no existe.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.

        Args:
            brand (str): Nombre de la marca a filtrar.

        Returns:
            List[Product]: Lista de productos de la marca.
        """
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene todos los productos de una categoría específica.

        Args:
            category (str): Nombre de la categoría a filtrar.

        Returns:
            List[Product]: Lista de productos de la categoría.
        """
        models = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(model) for model in models]

    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en la base de datos.

        Si el producto no tiene ID, lo crea. Si tiene ID, actualiza el existente.

        Args:
            product (Product): Entidad de producto a guardar.

        Returns:
            Product: Entidad actualizada con ID asignado.
        """
        model = self._entity_to_model(product)

        if product.id is None:
            self.db.add(model)
        else:
            self.db.merge(model)

        self.db.flush()
        self.db.refresh(model)
        self.db.commit()

        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto de la base de datos.

        Args:
            product_id (int): Identificador del producto a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return False

        self.db.delete(model)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM a entidad del dominio.

        Args:
            model (ProductModel): Modelo ORM a convertir.

        Returns:
            Product: Entidad del dominio.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    def _entity_to_model(self, entity: Product) -> ProductModel:
        """
        Convierte una entidad del dominio a modelo ORM.

        Args:
            entity (Product): Entidad del dominio a convertir.

        Returns:
            ProductModel: Modelo ORM.
        """
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )
