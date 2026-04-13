from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./data/ecommerce_chat.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency de FastAPI para obtener una sesión de base de datos.

    Usa yield para proporcionar la sesión y asegurar su cierre en finally.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa la base de datos creando las tablas ORM.

    Llama a Base.metadata.create_all() para crear las tablas definidas
    en los modelos importados.
    """
    Base.metadata.create_all(bind=engine)
