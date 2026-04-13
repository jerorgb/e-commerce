"""
Configuración y fixtures compartidas para tests.
Proporciona mocks y fixtures que se utilizan en múltiples tests.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock
from src.domain.entities import Product, ChatMessage, ChatContext
from src.application.dtos import ProductDTO, ChatMessageRequestDTO


@pytest.fixture
def sample_product():
    """
    Fixture que proporciona un objeto Product válido para testing.
    """
    return Product(
        id=1,
        name="Nike Air Zoom Pegasus",
        brand="Nike",
        category="Running",
        size="42",
        color="Black",
        price=120.0,
        stock=50,
        description="Zapatilla de running de alta performance"
    )


@pytest.fixture
def sample_product_unavailable():
    """
    Fixture que proporciona un producto sin stock.
    """
    return Product(
        id=2,
        name="Adidas Ultraboost",
        brand="Adidas",
        category="Running",
        size="43",
        color="White",
        price=180.0,
        stock=0,
        description="Zapatilla de running premium"
    )


@pytest.fixture
def sample_product_dto():
    """
    Fixture que proporciona un ProductDTO válido.
    """
    return ProductDTO(
        id=None,
        name="Puma Future Z",
        brand="Puma",
        category="Football",
        size="42",
        color="Red",
        price=150.0,
        stock=30,
        description="Botín de fútbol profesional"
    )


@pytest.fixture
def sample_chat_message():
    """
    Fixture que proporciona un ChatMessage válido.
    """
    return ChatMessage(
        id=1,
        session_id="session_123",
        role="user",
        message="¿Tienes zapatillas running en talla 42?",
        timestamp=datetime.now()
    )


@pytest.fixture
def sample_chat_message_assistant():
    """
    Fixture que proporciona una respuesta del asistente.
    """
    return ChatMessage(
        id=2,
        session_id="session_123",
        role="assistant",
        message="Sí, tenemos varias opciones disponibles.",
        timestamp=datetime.now()
    )


@pytest.fixture
def sample_chat_context(sample_chat_message, sample_chat_message_assistant):
    """
    Fixture que proporciona un ChatContext con histórico.
    """
    messages = [sample_chat_message, sample_chat_message_assistant]
    return ChatContext(messages=messages)


@pytest.fixture
def mock_product_repository():
    """
    Fixture que proporciona un mock del repositorio de productos.
    """
    mock = Mock()
    mock.get_all = Mock(return_value=[])
    mock.get_by_id = Mock(return_value=None)
    mock.get_by_brand = Mock(return_value=[])
    mock.get_by_category = Mock(return_value=[])
    mock.save = Mock(return_value=None)
    mock.delete = Mock(return_value=None)
    return mock


@pytest.fixture
def mock_chat_repository():
    """
    Fixture que proporciona un mock del repositorio de chat.
    """
    mock = Mock()
    mock.save_message = Mock(return_value=None)
    mock.get_session_history = Mock(return_value=[])
    mock.delete_session_history = Mock(return_value=None)
    mock.get_recent_messages = Mock(return_value=[])
    return mock


@pytest.fixture
def mock_gemini_service():
    """
    Fixture que proporciona un mock del servicio Gemini.
    """
    mock = AsyncMock()
    mock.generate_response = AsyncMock(return_value="Respuesta del asistente")
    mock.format_products_info = Mock(return_value="Información formateada de productos")
    return mock
