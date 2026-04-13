"""
API REST principal del sistema de e-commerce con chat IA.

Este módulo define la aplicación FastAPI con todos los endpoints para
gestionar productos y chat conversacional. Incluye configuración de CORS,
inyección de dependencias y manejo de errores.
"""

from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.application.chat_service import ChatService
from src.application.dtos import (
    ProductDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO,
)
from src.application.product_service import ProductService
from src.domain.exceptions import ProductNotFoundError, ChatServiceError
from src.infrastructure.db.database import get_db, init_db
from src.infrastructure.db.init_data import load_initial_data
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.repositories.product_repository import SQLProductRepository


app = FastAPI(
    title="E-Commerce Chat API",
    description="API para gestionar productos y chat conversacional con IA.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_product_service(db: Session) -> ProductService:
    """
    Crea una instancia del servicio de productos con inyección de dependencias.

    Args:
        db (Session): Sesión de base de datos SQLAlchemy.

    Returns:
        ProductService: Instancia configurada del servicio de productos.
    """
    return ProductService(SQLProductRepository(db))


def get_chat_service(db: Session, ai_service: GeminiService) -> ChatService:
    """
    Crea una instancia del servicio de chat con inyección de dependencias.

    Args:
        db (Session): Sesión de base de datos SQLAlchemy.
        ai_service (GeminiService): Servicio de IA de Google Gemini.

    Returns:
        ChatService: Instancia configurada del servicio de chat.
    """
    return ChatService(SQLProductRepository(db), SQLChatRepository(db), ai_service)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Evento de inicio de la aplicación.

    Inicializa la base de datos, carga datos iniciales y configura
    el servicio de IA. Se ejecuta automáticamente al iniciar la app.
    """
    init_db()
    try:
        load_initial_data()
    except Exception:
        pass
    app.state.ai_service = GeminiService()


@app.get("/", summary="Información de la API")
def read_root() -> dict:
    """
    Retorna información básica de la API y los endpoints disponibles.

    Returns:
        dict: Información de la API incluyendo nombre, versión y lista de endpoints.
    """
    return {
        "name": app.title,
        "version": app.version,
        "description": app.description,
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Información de la API"},
            {"path": "/products", "method": "GET", "description": "Lista todos los productos"},
            {
                "path": "/products/{product_id}",
                "method": "GET",
                "description": "Obtiene un producto por ID",
            },
            {
                "path": "/chat",
                "method": "POST",
                "description": "Procesa un mensaje de chat con IA",
            },
            {
                "path": "/chat/history/{session_id}",
                "method": "GET",
                "description": "Obtiene el historial de una sesión",
            },
            {
                "path": "/chat/history/{session_id}",
                "method": "DELETE",
                "description": "Elimina el historial de una sesión",
            },
            {"path": "/health", "method": "GET", "description": "Health check"},
        ],
    }


@app.get("/products", response_model=List[ProductDTO], summary="Lista todos los productos")
def list_products(db: Session = Depends(get_db)) -> List[ProductDTO]:
    """
    Obtiene la lista completa de productos disponibles.

    Este endpoint retorna todos los productos registrados en la base de datos,
    incluyendo aquellos sin stock.

    Args:
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ProductDTO]: Lista de productos con toda su información.
    """
    service = get_product_service(db)
    return service.get_all_products()


@app.get(
    "/products/{product_id}",
    response_model=ProductDTO,
    summary="Obtiene un producto por su ID",
)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductDTO:
    """
    Obtiene un producto específico por su identificador único.

    Args:
        product_id (int): Identificador único del producto.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ProductDTO: Información completa del producto solicitado.

    Raises:
        HTTPException: 404 si el producto no existe.
    """
    service = get_product_service(db)
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.post(
    "/chat",
    response_model=ChatMessageResponseDTO,
    summary="Procesa un mensaje de chat con IA",
)
async def process_chat(
    request: ChatMessageRequestDTO,
    db: Session = Depends(get_db),
) -> ChatMessageResponseDTO:
    """
    Procesa un mensaje del usuario y genera una respuesta con IA.

    Recibe un mensaje de chat, lo procesa con el servicio de IA considerando
    el contexto de la conversación y el catálogo de productos, y retorna
    la respuesta generada.

    Args:
        request (ChatMessageRequestDTO): Mensaje del usuario con session_id.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ChatMessageResponseDTO: Respuesta generada por la IA con timestamp.

    Raises:
        HTTPException: 500 si hay error procesando el mensaje o con IA.
    """
    ai_service: GeminiService = app.state.ai_service
    service = get_chat_service(db, ai_service)
    try:
        return await service.process_message(request)
    except ChatServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get(
    "/chat/history/{session_id}",
    response_model=List[ChatHistoryDTO],
    summary="Obtiene el historial de una sesión de chat",
)
def get_chat_history(
    session_id: str,
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
) -> List[ChatHistoryDTO]:
    """
    Obtiene el historial de mensajes de una sesión de chat específica.

    Args:
        session_id (str): Identificador único de la sesión de chat.
        limit (int): Número máximo de mensajes a retornar (mínimo 1).
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ChatHistoryDTO]: Lista de mensajes del historial en orden cronológico.
    """
    service = get_chat_service(db, app.state.ai_service)
    return service.get_session_history(session_id, limit)


@app.delete(
    "/chat/history/{session_id}",
    summary="Elimina el historial de una sesión de chat",
)
def delete_chat_history(session_id: str, db: Session = Depends(get_db)) -> dict:
    """
    Elimina todo el historial de mensajes de una sesión de chat.

    Args:
        session_id (str): Identificador único de la sesión a eliminar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        dict: Diccionario con la cantidad de mensajes eliminados.
    """
    service = get_chat_service(db, app.state.ai_service)
    deleted_count = service.clear_session_history(session_id)
    return {"deleted": deleted_count}


@app.get("/health", summary="Verificación de salud de la API")
def health_check() -> dict:
    """
    Verifica el estado de salud de la API.

    Endpoint simple para monitoreo que indica si el servicio está funcionando
    correctamente.

    Returns:
        dict: Estado de salud con timestamp en formato ISO 8601.
    """
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}
