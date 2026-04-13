"""
Servicio de integración con Google Gemini AI.

Este módulo proporciona una interfaz para interactuar con el modelo de IA
Google Gemini, específicamente configurado para generar respuestas de chat
en un contexto de e-commerce de zapatos.
"""

import os

import google.generativeai as genai



class GeminiService:
    """
    Servicio de IA que utiliza Google Gemini para generar respuestas de chat.

    Esta clase encapsula la integración con la API de Google Gemini,
    configurada específicamente para un asistente de ventas de zapatos.
    Maneja la autenticación, configuración del modelo y generación de respuestas.

    Attributes:
        model_name (str): Nombre del modelo Gemini a utilizar.
        model: Instancia del modelo Gemini configurado.
    """

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Inicializa el servicio de Gemini con configuración por defecto.

        Args:
            model_name (str): Nombre del modelo Gemini a utilizar.
                             Por defecto "gemini-2.5-flash".

        Raises:
            EnvironmentError: Si la variable GEMINI_API_KEY no está configurada.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY no está configurada en el entorno")

        genai.configure(api_key=api_key)
        self.model_name = model_name          # ← assign first
        self.model = genai.GenerativeModel(self.model_name)  # ← then use

    async def generate_response(self, user_message, products, context):
        """
        Genera una respuesta de asistente basada en mensaje, productos y contexto.

        Construye un prompt contextual con información de productos y conversación
        previa, luego utiliza Gemini para generar una respuesta natural y útil.

        Args:
            user_message (str): Mensaje del usuario actual.
            products (List[Product]): Lista de productos disponibles.
            context (ChatContext): Contexto de la conversación anterior.

        Returns:
            str: Respuesta generada por la IA.

        Raises:
            RuntimeError: Si hay error en la comunicación con Gemini.
        """
        try:
            product_text = self.format_products_info(products)
            context_text = context.format_for_prompt() if context is not None else ""
            prompt = self._build_prompt(product_text, context_text, user_message)

            response = await self.model.generate_content_async(prompt)  # ← fixed

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                return getattr(candidate, "text", "").strip()

            return "Lo siento, no pude generar una respuesta en este momento."

        except Exception as exc:
            raise RuntimeError(f"Error al generar respuesta con Gemini: {exc}") from exc

    def format_products_info(self, products) -> str:
        """
        Convierte la lista de productos en texto legible para el prompt.

        Args:
            products (List[Product]): Lista de productos a formatear.

        Returns:
            str: Texto formateado con información de productos.
        """
        lines = []
        for product in products:
            lines.append(
                f"- {product.name} | {product.brand} | ${product.price:.2f} | stock: {product.stock}"
            )
        return "\n".join(lines) if lines else "No hay productos disponibles."

    def _build_prompt(self, product_text: str, context_text: str, user_message: str) -> str:
        """
        Construye el prompt completo para enviar a Gemini.

        Args:
            product_text (str): Información formateada de productos.
            context_text (str): Historial de conversación formateado.
            user_message (str): Mensaje actual del usuario.

        Returns:
            str: Prompt completo para el modelo de IA.
        """
        return (
            "Eres un asistente virtual experto en ventas de zapatos para un e-commerce.\n"
            "Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.\n\n"
            "PRODUCTOS DISPONIBLES:\n"
            f"{product_text}\n\n"
            "INSTRUCCIONES:\n"
            "- Sé amigable y profesional\n"
            "- Usa el contexto de la conversación anterior\n"
            "- Recomienda productos específicos cuando sea apropiado\n"
            "- Menciona precios, tallas y disponibilidad\n"
            "- Si no tienes información, sé honesto\n\n"
            f"{context_text}\n"
            f"Usuario: {user_message}\n\n"
            "Asistente:"
        )
