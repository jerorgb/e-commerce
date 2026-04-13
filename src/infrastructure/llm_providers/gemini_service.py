"""
Servicio de integración con Google Gemini AI.

Este módulo proporciona una interfaz para interactuar con el modelo de IA
Google Gemini, específicamente configurado para generar respuestas de chat
en un contexto de e-commerce de zapatos.
"""

import os
from typing import List

import google.generativeai as genai

from src.domain.entities import Product, ChatContext


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

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Inicializa el servicio de Gemini con configuración por defecto.

        Args:
            model_name (str): Nombre del modelo Gemini a utilizar.
                             Por defecto "gemini-2.5-flash".

        Raises:
            EnvironmentError: Si la variable GEMINI_API_KEY no está configurada.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "tu_api_key_aqui":
            print("⚠️  WARNING: GEMINI_API_KEY no está configurada o es placeholder.")
            print("   Para usar el chat con IA, configura una API key válida de Google Gemini.")
            print("   Obtén tu API key en: https://makersuite.google.com/app/apikey")
            print("   Luego actualiza el archivo .env con: GEMINI_API_KEY=tu_clave_real")
            self.model = None
            self.api_configured = False
        else:
            genai.configure(api_key=api_key)
            self.model_name = model_name
            self.model = genai.GenerativeModel(self.model_name)
            self.api_configured = True

    async def generate_response(
        self, user_message: str, products: List[Product], context: ChatContext
    ) -> str:
        """
        Genera una respuesta de asistente basada en el prompt, productos y contexto.

        Realiza el flujo completo: formatea productos, construye prompt con contexto,
        llama a Gemini y retorna la respuesta generada.

        Args:
            user_message (str): Mensaje actual del usuario.
            products (List[Product]): Lista de productos disponibles.
            context (ChatContext): Contexto conversacional con historial.

        Returns:
            str: Respuesta generada por el modelo Gemini.

        Raises:
            RuntimeError: Si hay error al comunicarse con Gemini.
        """
        if not self.api_configured or self.model is None:
            return "Lo siento, el servicio de IA no está configurado. Por favor configura GEMINI_API_KEY en el archivo .env para usar el chat inteligente."

        try:
            product_text = self.format_products_info(products)
            context_text = context.format_for_prompt() if context else ""

            prompt = self._build_prompt(product_text, context_text, user_message)

            response = await self.model.generate_content_async(prompt)

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            return "Lo siento, no pude generar una respuesta en este momento."

        except Exception as exc:
            raise RuntimeError(f"Error al generar respuesta con Gemini: {exc}") from exc

    def format_products_info(self, products: List[Product]) -> str:
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
                f"- {product.name} | {product.brand} | ${product.price:.2f} | "
                f"Talla: {product.size} | Color: {product.color} | Stock: {product.stock}"
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
            "- Si no tienes información, sé honesto\n"
            "- Responde en español\n\n"
            f"{context_text}\n"
            f"Usuario: {user_message}\n\n"
            "Asistente:"
        )
