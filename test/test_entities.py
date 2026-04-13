"""
Tests unitarios para las entidades del dominio.
Prueba validaciones, métodos de negocio y comportamientos de las entidades.
"""

import pytest
from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext


class TestProduct:
    """Tests para la entidad Product."""
    
    def test_product_creation_valid(self, sample_product):
        """Test: Crear un producto válido."""
        assert sample_product.id == 1
        assert sample_product.name == "Nike Air Zoom Pegasus"
        assert sample_product.brand == "Nike"
        assert sample_product.price == 120.0
        assert sample_product.stock == 50
    
    
    def test_product_creation_negative_price(self):
        """Test: No se permite crear producto con precio negativo."""
        with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
            Product(
                id=1,
                name="Zapatilla",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=-50.0,
                stock=10,
                description="Descripción"
            )
    
    
    def test_product_creation_zero_price(self):
        """Test: No se permite crear producto con precio cero."""
        with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
            Product(
                id=1,
                name="Zapatilla",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=0.0,
                stock=10,
                description="Descripción"
            )
    
    
    def test_product_creation_negative_stock(self):
        """Test: No se permite crear producto con stock negativo."""
        with pytest.raises(ValueError, match="El stock no puede ser negativo"):
            Product(
                id=1,
                name="Zapatilla",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=100.0,
                stock=-5,
                description="Descripción"
            )
    
    
    def test_product_creation_empty_name(self):
        """Test: No se permite crear producto sin nombre."""
        with pytest.raises(ValueError, match="El nombre del producto no puede estar vacío"):
            Product(
                id=1,
                name="",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=100.0,
                stock=10,
                description="Descripción"
            )
    
    
    def test_is_available_with_stock(self, sample_product):
        """Test: Producto con stock está disponible."""
        assert sample_product.is_available() is True
    
    
    def test_is_available_without_stock(self, sample_product_unavailable):
        """Test: Producto sin stock no está disponible."""
        assert sample_product_unavailable.is_available() is False
    
    
    def test_reduce_stock_valid(self, sample_product):
        """Test: Reducir stock válido."""
        initial_stock = sample_product.stock
        sample_product.reduce_stock(10)
        assert sample_product.stock == initial_stock - 10
    
    
    def test_reduce_stock_exact_amount(self, sample_product):
        """Test: Reducir exactamente todo el stock."""
        sample_product.reduce_stock(sample_product.stock)
        assert sample_product.stock == 0
    
    
    def test_reduce_stock_negative_quantity(self, sample_product):
        """Test: No se permite reducir stock con cantidad negativa."""
        with pytest.raises(ValueError, match="La cantidad a reducir debe ser positiva"):
            sample_product.reduce_stock(-5)
    
    
    def test_reduce_stock_insufficient(self, sample_product):
        """Test: No se permite reducir más stock del disponible."""
        with pytest.raises(ValueError, match="No hay suficiente stock disponible"):
            sample_product.reduce_stock(sample_product.stock + 1)
    
    
    def test_increase_stock_valid(self, sample_product):
        """Test: Aumentar stock válido."""
        initial_stock = sample_product.stock
        sample_product.increase_stock(20)
        assert sample_product.stock == initial_stock + 20
    
    
    def test_increase_stock_negative_quantity(self, sample_product):
        """Test: No se permite aumentar stock con cantidad negativa."""
        with pytest.raises(ValueError, match="La cantidad a incrementar debe ser positiva"):
            sample_product.increase_stock(-10)
    
    
    def test_increase_stock_zero(self, sample_product):
        """Test: Se permite aumentar stock en 0 (sin cambios)."""
        initial_stock = sample_product.stock
        # No debería lanzar excepción, pero el stock no cambia
        # Nota: Si la validación es estricta, puede fallar
        sample_product.increase_stock(0)
        assert sample_product.stock == initial_stock


class TestChatMessage:
    """Tests para la entidad ChatMessage."""
    
    def test_chat_message_creation_valid(self, sample_chat_message):
        """Test: Crear un ChatMessage válido."""
        assert sample_chat_message.id == 1
        assert sample_chat_message.session_id == "session_123"
        assert sample_chat_message.role == "user"
        assert sample_chat_message.message == "¿Tienes zapatillas running en talla 42?"
    
    
    def test_chat_message_invalid_role(self):
        """Test: No se permite rol inválido."""
        with pytest.raises(ValueError, match="Acceso no autorizado. Rol incorrecto"):
            ChatMessage(
                id=1,
                session_id="session_123",
                role="invalid_role",
                message="Test message",
                timestamp=datetime.now()
            )
    
    
    def test_chat_message_empty_content(self):
        """Test: No se permite mensaje vacío."""
        with pytest.raises(ValueError, match="Mensaje invalido, mensaje vacío"):
            ChatMessage(
                id=1,
                session_id="session_123",
                role="user",
                message="",
                timestamp=datetime.now()
            )
    
    
    def test_chat_message_empty_session_id(self):
        """Test: No se permite session_id vacío."""
        with pytest.raises(ValueError, match="ID de sesión invalido, ID vacío"):
            ChatMessage(
                id=1,
                session_id="",
                role="user",
                message="Test message",
                timestamp=datetime.now()
            )
    
    
    def test_is_from_user_true(self, sample_chat_message):
        """Test: Identificar mensaje del usuario."""
        assert sample_chat_message.is_from_user() is True
    
    
    def test_is_from_user_false(self, sample_chat_message_assistant):
        """Test: Mensaje del asistente no es del usuario."""
        assert sample_chat_message_assistant.is_from_user() is False
    
    
    def test_is_from_assistant_true(self, sample_chat_message_assistant):
        """Test: Identificar respuesta del asistente."""
        assert sample_chat_message_assistant.is_from_assistant() is True
    
    
    def test_is_from_assistant_false(self, sample_chat_message):
        """Test: Mensaje del usuario no es del asistente."""
        assert sample_chat_message.is_from_assistant() is False
    
    
    def test_valid_roles(self):
        """Test: Ambos roles válidos funcionan correctamente."""
        user_msg = ChatMessage(
            id=1,
            session_id="session_123",
            role="user",
            message="Mensaje del usuario",
            timestamp=datetime.now()
        )
        assert user_msg.role == "user"
        
        assistant_msg = ChatMessage(
            id=2,
            session_id="session_123",
            role="assistant",
            message="Respuesta del asistente",
            timestamp=datetime.now()
        )
        assert assistant_msg.role == "assistant"


class TestChatContext:
    """Tests para el Value Object ChatContext."""
    
    def test_chat_context_creation(self, sample_chat_context):
        """Test: Crear un ChatContext válido."""
        assert len(sample_chat_context.messages) == 2
        assert sample_chat_context.max_messages == 6
    
    
    def test_chat_context_with_custom_max_messages(self, sample_chat_message):
        """Test: ChatContext con max_messages personalizado."""
        messages = [sample_chat_message]
        context = ChatContext(messages=messages, max_messages=3)
        assert context.max_messages == 3
    
    
    def test_get_recent_messages_less_than_max(self, sample_chat_context):
        """Test: Obtener mensajes recientes (menos que el máximo)."""
        recent = sample_chat_context.get_recent_messages()
        assert len(recent) == 2  # Tenemos 2 mensajes, max es 6
    
    
    def test_get_recent_messages_more_than_max(self, sample_chat_message):
        """Test: Obtener últimos N mensajes cuando hay más que el máximo."""
        messages = [
            ChatMessage(
                id=i,
                session_id="session_123",
                role="user" if i % 2 == 0 else "assistant",
                message=f"Mensaje {i}",
                timestamp=datetime.now()
            )
            for i in range(1, 11)  # 10 mensajes
        ]
        context = ChatContext(messages=messages, max_messages=3)
        recent = context.get_recent_messages()
        assert len(recent) == 3
        # Últimos 3 mensajes son los IDs 8, 9, 10
        assert recent[0].id == 8
        assert recent[1].id == 9
        assert recent[2].id == 10
    
    
    def test_format_for_prompt(self, sample_chat_context):
        """Test: Formatear mensajes para el prompt."""
        formatted = sample_chat_context.format_for_prompt()
        assert "Usuario:" in formatted or "user" in formatted.lower()
        assert "Asistente:" in formatted or "assistant" in formatted.lower()
    
    
    def test_format_for_prompt_includes_messages(self, sample_chat_message, sample_chat_message_assistant):
        """Test: El formato incluye los contenidos de los mensajes."""
        context = ChatContext(messages=[sample_chat_message, sample_chat_message_assistant])
        formatted = context.format_for_prompt()
        assert sample_chat_message.message in formatted
        assert sample_chat_message_assistant.message in formatted
    
    
    def test_empty_chat_context(self):
        """Test: ChatContext vacío."""
        context = ChatContext(messages=[])
        recent = context.get_recent_messages()
        assert len(recent) == 0


@pytest.mark.unit
class TestProductValidations:
    """Tests para validaciones comprehensivas de Product."""
    
    def test_product_all_attributes(self):
        """Test: Verificar que se asignen correctamente todos los atributos."""
        product = Product(
            id=99,
            name="Test Product",
            brand="Test Brand",
            category="Test Category",
            size="40",
            color="Blue",
            price=99.99,
            stock=5,
            description="Test Description"
        )
        assert product.id == 99
        assert product.name == "Test Product"
        assert product.brand == "Test Brand"
        assert product.category == "Test Category"
        assert product.size == "40"
        assert product.color == "Blue"
        assert product.price == 99.99
        assert product.stock == 5
        assert product.description == "Test Description"
    
    
    def test_product_stock_operations_sequence(self):
        """Test: Operaciones secuenciales de stock."""
        product = Product(
            id=1,
            name="Test",
            brand="Test",
            category="Test",
            size="42",
            color="Black",
            price=100.0,
            stock=100,
            description="Test"
        )
        
        # Reducir 30
        product.reduce_stock(30)
        assert product.stock == 70
        
        # Aumentar 20
        product.increase_stock(20)
        assert product.stock == 90
        
        # Reducir 90 (toda la cantidad)
        product.reduce_stock(90)
        assert product.stock == 0
        assert not product.is_available()
