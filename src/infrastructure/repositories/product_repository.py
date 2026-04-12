from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities import Product as ProductEntity
from src.domain.repositories import IProductRepository
from src.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """Repositorio de productos basado en SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ProductEntity]:
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_id(self, product_id: int) -> Optional[ProductEntity]:
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[ProductEntity]:
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_category(self, category: str) -> List[ProductEntity]:
        models = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(model) for model in models]

    def save(self, product: ProductEntity) -> ProductEntity:
        if product.id is None:
            model = self._entity_to_model(product)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)

        existing = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
        if existing is None:
            model = self._entity_to_model(product)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return self._model_to_entity(model)

        existing.name = product.name
        existing.brand = product.brand
        existing.category = product.category
        existing.size = product.size
        existing.color = product.color
        existing.price = product.price
        existing.stock = product.stock
        existing.description = product.description

        self.db.commit()
        self.db.refresh(existing)
        return self._model_to_entity(existing)

    def delete(self, product_id: int) -> bool:
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> ProductEntity:
        return ProductEntity(
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

    def _entity_to_model(self, entity: ProductEntity) -> ProductModel:
        model = ProductModel(
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )
        if entity.id is not None:
            model.id = entity.id
        return model
