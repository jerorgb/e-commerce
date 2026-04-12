from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models import ProductModel


def load_initial_data() -> None:
    """Carga productos iniciales si la tabla aún está vacía."""
    session = SessionLocal()
    try:
        product_count = session.query(ProductModel).count()
        if product_count > 0:
            return

        products = [
            ProductModel(
                name="Nike Air Zoom Pegasus 39",
                brand="Nike",
                category="Running",
                size="10",
                color="White",
                price=130.0,
                stock=25,
                description="Zapatillas running con amortiguación reactiva y ajuste transpirable.",
            ),
            ProductModel(
                name="Adidas Ultraboost 22",
                brand="Adidas",
                category="Running",
                size="10",
                color="Core Black",
                price=180.0,
                stock=18,
                description="Calzado de alto rendimiento con energía de retorno y comodidad total.",
            ),
            ProductModel(
                name="Puma Smash v2",
                brand="Puma",
                category="Casual",
                size="9",
                color="Navy",
                price=65.0,
                stock=40,
                description="Zapatillas casuales clásicas con diseño limpio y suela duradera.",
            ),
            ProductModel(
                name="Nike Court Royale",
                brand="Nike",
                category="Casual",
                size="9",
                color="White",
                price=75.0,
                stock=35,
                description="Estilo retro y cómodo para uso diario con detalles de cuero.",
            ),
            ProductModel(
                name="Adidas Gazelle",
                brand="Adidas",
                category="Casual",
                size="10",
                color="Green",
                price=95.0,
                stock=28,
                description="Icónicas zapatillas de estilo retro con exterior en gamuza.",
            ),
            ProductModel(
                name="Puma Future Rider",
                brand="Puma",
                category="Casual",
                size="11",
                color="Grey",
                price=85.0,
                stock=22,
                description="Zapatillas de estilo vintage con amortiguación suave y look urbano.",
            ),
            ProductModel(
                name="Nike Blazer Mid 77",
                brand="Nike",
                category="Streetwear",
                size="9",
                color="Sail",
                price=110.0,
                stock=20,
                description="Estilo retro de baloncesto con acabado premium y versatilidad urbana.",
            ),
            ProductModel(
                name="Adidas Stan Smith",
                brand="Adidas",
                category="Formal",
                size="10",
                color="White",
                price=100.0,
                stock=30,
                description="Clásicas zapatillas blancas para un look limpio y formal casual.",
            ),
            ProductModel(
                name="Puma Legacy Court",
                brand="Puma",
                category="Formal",
                size="11",
                color="Black",
                price=120.0,
                stock=14,
                description="Zapatillas formales con líneas elegantes y suela resistente.",
            ),
            ProductModel(
                name="Nike Revolution 6",
                brand="Nike",
                category="Running",
                size="8",
                color="Rush Blue",
                price=60.0,
                stock=50,
                description="Zapatillas running accesibles con soporte ligero y comodidad diaria.",
            ),
        ]

        session.add_all(products)
        session.commit()
    finally:
        session.close()
