"""
Excepciones específicas del dominio para el sistema de e-commerce.

Este módulo define excepciones personalizadas que representan errores de negocio,
no errores técnicos. Estas excepciones ayudan a manejar situaciones específicas
del dominio como productos no encontrados o datos inválidos.
"""

class ProductNotFoundError(Exception):
    """
    Excepción lanzada cuando se busca un producto que no existe.

    Esta excepción se usa en los repositorios y servicios cuando
    no se puede encontrar un producto con el ID especificado.

    Args:
        product_id (int, optional): ID del producto que no se encontró.
                                   Si se proporciona, se incluye en el mensaje.
    """

    def __init__(self, product_id: int = None):
        if product_id is not None:
            super().__init__(f"Producto con ID {product_id} no encontrado")
        else:
            super().__init__("Producto no encontrado")



class InvalidProductDataError(Exception):
    """
    Excepción lanzada cuando los datos de un producto son inválidos.

    Esta excepción se usa cuando se intenta crear o actualizar un producto
    con datos que no cumplen las reglas de negocio.

    Args:
        message (str): Mensaje descriptivo del error de validación.
                      Por defecto: "Datos de producto inválidos".
    """

    def __init__(self, message: str = "Datos de producto inválidos"):
        super().__init__(message)


class ChatServiceError(Exception):
    """
    Excepción lanzada cuando hay un error en el servicio de chat.

    Esta excepción se usa para manejar errores relacionados con el procesamiento
    de mensajes de chat, integración con IA o problemas de contexto.

    Args:
        message (str): Mensaje descriptivo del error en el servicio de chat.
                      Por defecto: "Error en el servicio de chat".
    """

    def __init__(self, message: str = "Error en el servicio de chat"):
        super().__init__(message)
