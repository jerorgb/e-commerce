import pytest
from datetime import datetime

from src.domain.entities import Product, ChatMessage, ChatContext


def test_product_validations_raise_for_invalid_values():
    with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
        Product(id=None, name="Zapato", brand="Nike", category="Running", size="10", color="White", price=0, stock=10, description="Test")

    with pytest.raises(ValueError, match="El stock no puede ser negativo"):
        Product(id=None, name="Zapato", brand="Nike", category="Running", size="10", color="White", price=100.0, stock=-1, description="Test")

    with pytest.raises(ValueError, match="El nombre del producto no puede estar vacío"):
        Product(id=None, name="", brand="Nike", category="Running", size="10", color="White", price=100.0, stock=10, description="Test")


def test_product_is_available_and_reduce_stock():
    product = Product(id=1, name="Zapato", brand="Nike", category="Running", size="10", color="White", price=100.0, stock=5, description="Test")
    assert product.is_available() is True

    product.reduce_stock(2)
    assert product.stock == 3

    with pytest.raises(ValueError, match="La cantidad a reducir debe ser positiva"):
        product.reduce_stock(-1)

    with pytest.raises(ValueError, match="No hay suficiente stock disponible"):
        product.reduce_stock(10)


def test_chat_message_validations():
    with pytest.raises(ValueError, match="Acceso no autorizado. Rol incorrecto"):
        ChatMessage(id=None, session_id="s1", role="invalid", message="Hola", timestamp=datetime.utcnow())

    with pytest.raises(ValueError, match="Mensaje invalido, mensaje vacío"):
        ChatMessage(id=None, session_id="s1", role="user", message="", timestamp=datetime.utcnow())

    with pytest.raises(ValueError, match="ID de sesión invalido, ID vacío"):
        ChatMessage(id=None, session_id="", role="user", message="Hola", timestamp=datetime.utcnow())


def test_chat_context_format_for_prompt():
    messages = [
        ChatMessage(id=1, session_id="sess1", role="user", message="Hola", timestamp=datetime.utcnow()),
        ChatMessage(id=2, session_id="sess1", role="assistant", message="Hola, ¿en qué puedo ayudarte?", timestamp=datetime.utcnow()),
        ChatMessage(id=3, session_id="sess1", role="user", message="Busco zapatos para correr", timestamp=datetime.utcnow()),
    ]

    context = ChatContext(messages=messages)
    expected = (
        "Usuario: Hola\n"
        "Asistente: Hola, ¿en qué puedo ayudarte?\n"
        "Usuario: Busco zapatos para correr"
    )

    assert context.format_for_prompt() == expected
