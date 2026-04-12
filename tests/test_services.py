import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime

from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import ProductDTO, ChatMessageRequestDTO
from src.domain.entities import Product, ChatMessage
from src.domain.exceptions import ProductNotFoundError, ChatServiceError


@pytest.fixture
def product_repo_mock():
    return Mock()


@pytest.fixture
def chat_repo_mock():
    return Mock()


@pytest.fixture
def ai_service_mock():
    service = Mock()
    service.generate_response = AsyncMock()
    return service


@pytest.fixture
def product_service(product_repo_mock):
    return ProductService(product_repo_mock)


@pytest.fixture
def chat_service(product_repo_mock, chat_repo_mock, ai_service_mock):
    return ChatService(product_repo_mock, chat_repo_mock, ai_service_mock)


def test_product_service_get_all_products(product_service, product_repo_mock):
    product_repo_mock.get_all.return_value = [
        Product(id=1, name="Zapato", brand="Nike", category="Running", size="10", color="White", price=120.0, stock=5, description="Cómodo"),
        Product(id=2, name="Zapatilla", brand="Adidas", category="Casual", size="9", color="Black", price=90.0, stock=0, description="Estilo urbano"),
    ]

    results = product_service.get_all_products()

    assert len(results) == 2
    assert results[0].id == 1
    assert results[0].name == "Zapato"
    product_repo_mock.get_all.assert_called_once()


def test_product_service_get_product_by_id_not_found(product_service, product_repo_mock):
    product_repo_mock.get_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        product_service.get_product_by_id(999)


def test_product_service_create_product_calls_save(product_service, product_repo_mock):
    dto = ProductDTO(
        id=None,
        name="Zapato",
        brand="Nike",
        category="Running",
        size="10",
        color="White",
        price=120.0,
        stock=10,
        description="Cómodo",
    )
    saved_entity = Product(
        id=1,
        name=dto.name,
        brand=dto.brand,
        category=dto.category,
        size=dto.size,
        color=dto.color,
        price=dto.price,
        stock=dto.stock,
        description=dto.description,
    )
    product_repo_mock.save.return_value = saved_entity

    result = product_service.create_product(dto)

    assert result.id == 1
    assert result.name == dto.name
    product_repo_mock.save.assert_called_once()


def test_product_service_update_product_not_found(product_service, product_repo_mock):
    product_repo_mock.get_by_id.return_value = None
    dto = ProductDTO(
        id=None,
        name="Zapato",
        brand="Nike",
        category="Running",
        size="10",
        color="White",
        price=120.0,
        stock=10,
        description="Cómodo",
    )

    with pytest.raises(ProductNotFoundError):
        product_service.update_product(999, dto)


def test_product_service_delete_product_not_found(product_service, product_repo_mock):
    product_repo_mock.get_by_id.return_value = None

    with pytest.raises(ProductNotFoundError):
        product_service.delete_product(999)


def test_product_service_get_available_products(product_service, product_repo_mock):
    product_repo_mock.get_all.return_value = [
        Product(id=1, name="Disponible", brand="Nike", category="Running", size="10", color="White", price=120.0, stock=3, description="Ok"),
        Product(id=2, name="Agotado", brand="Adidas", category="Casual", size="9", color="Black", price=95.0, stock=0, description="Agotado"),
    ]

    result = product_service.get_available_products()

    assert len(result) == 1
    assert result[0].id == 1


@pytest.mark.asyncio
async def test_chat_service_process_message_saves_messages(
    chat_service, product_repo_mock, chat_repo_mock, ai_service_mock
):
    product_repo_mock.get_all.return_value = [
        Product(id=1, name="Zapato", brand="Nike", category="Running", size="10", color="White", price=120.0, stock=5, description="Cómodo"),
    ]
    chat_repo_mock.get_recent_messages.return_value = []
    ai_service_mock.generate_response.return_value = "Hola, te recomiendo el Zapato Nike"

    request = ChatMessageRequestDTO(session_id="sess1", message="Quiero zapatillas")
    response = await chat_service.process_message(request)

    assert response.session_id == "sess1"
    assert response.assistant_message == "Hola, te recomiendo el Zapato Nike"
    assert response.user_message == "Quiero zapatillas"
    assert chat_repo_mock.get_recent_messages.called
    assert chat_repo_mock.save_message.call_count == 2
    saved_user, saved_assistant = chat_repo_mock.save_message.call_args_list
    assert saved_user.args[0].role == "user"
    assert saved_assistant.args[0].role == "assistant"


@pytest.mark.asyncio
async def test_chat_service_process_message_raises_chat_service_error(
    chat_service, chat_repo_mock, ai_service_mock
):
    chat_repo_mock.get_recent_messages.return_value = []
    ai_service_mock.generate_response.side_effect = RuntimeError("API falló")

    request = ChatMessageRequestDTO(session_id="sess1", message="Hola")

    with pytest.raises(ChatServiceError):
        await chat_service.process_message(request)


def test_chat_service_history_and_clear(chat_service, chat_repo_mock):
    chat_repo_mock.get_session_history.return_value = [
        ChatMessage(id=1, session_id="sess1", role="user", message="Hola", timestamp=datetime.utcnow())
    ]
    chat_repo_mock.delete_session_history.return_value = 3

    history = chat_service.get_session_history("sess1", limit=5)
    assert len(history) == 1
    assert history[0].role == "user"

    deleted = chat_service.clear_session_history("sess1")
    assert deleted == 3
