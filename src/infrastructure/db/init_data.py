from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models import ProductModel


def load_initial_data() -> None:
    """
    Carga datos iniciales en la base de datos si no existen productos.

    Comprueba si ya hay productos registrados y, de no haberlos,
    inserta un conjunto de productos de ejemplo variados.
    """
    session = SessionLocal()
    try:
        existing_count = session.query(ProductModel).count()
        if existing_count > 0:
            return

        products = [
            ProductModel(
                name="Nike Air Zoom Pegasus 41",
                brand="Nike",
                category="Running",
                size="9",
                color="Blanco",
                price=120.0,
                stock=15,
                description="Zapatillas de running cómodas y versátiles para entrenamientos diarios.",
            ),
            ProductModel(
                name="Adidas Ultraboost 22",
                brand="Adidas",
                category="Running",
                size="10",
                color="Negro",
                price=180.0,
                stock=10,
                description="Calzado con amortiguación superior para corredores que buscan confort y retorno de energía.",
            ),
            ProductModel(
                name="Puma RS-X³",
                brand="Puma",
                category="Casual",
                size="9.5",
                color="Gris",
                price=110.0,
                stock=20,
                description="Zapatillas urbanas de estilo retro con diseño moderno y gran comodidad.",
            ),
            ProductModel(
                name="Nike Court Vision Low",
                brand="Nike",
                category="Casual",
                size="8",
                color="Blanco",
                price=75.0,
                stock=25,
                description="Modelo clásico inspirado en el baloncesto ideal para uso diario.",
            ),
            ProductModel(
                name="Adidas Stan Smith",
                brand="Adidas",
                category="Casual",
                size="11",
                color="Blanco/Verde",
                price=90.0,
                stock=18,
                description="Icono del estilo casual con diseño limpio y materiales duraderos.",
            ),
            ProductModel(
                name="Puma Suede Classic",
                brand="Puma",
                category="Casual",
                size="10.5",
                color="Azul Marino",
                price=85.0,
                stock=12,
                description="Zapato de gamuza con estilo clásico y excelente ajuste para la ciudad.",
            ),
            ProductModel(
                name="Nike Air Force 1",
                brand="Nike",
                category="Formal",
                size="10",
                color="Blanco",
                price=95.0,
                stock=14,
                description="Zapatilla urbana icónica que combina estilo formal y confortable.",
            ),
            ProductModel(
                name="Adidas Gazelle",
                brand="Adidas",
                category="Casual",
                size="9",
                color="Verde",
                price=80.0,
                stock=22,
                description="Modelo retro de Adidas con perfil bajo y estilo atemporal.",
            ),
            ProductModel(
                name="Puma Clyde",
                brand="Puma",
                category="Formal",
                size="11.5",
                color="Negro",
                price=100.0,
                stock=8,
                description="Zapato de corte elegante inspirado en el baloncesto clásico.",
            ),
            ProductModel(
                name="Nike React Infinity Run",
                brand="Nike",
                category="Running",
                size="10",
                color="Gris Claro",
                price=150.0,
                stock=9,
                description="Calzado de running diseñado para reducir lesiones con gran amortiguación.",
            ),
        ]

        session.add_all(products)
        session.commit()
    finally:
        session.close()
