"""Ollama provider implementation."""

import base64
from typing import List
from .base import BaseProvider
from model import Model


class OllamaProvider(BaseProvider):
    """Ollama provider for local image processing."""

    def __init__(self):
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Ollama client."""
        try:
            import ollama
            self._client = ollama.Client()
        except ImportError:
            self._client = None

    def get_response(
        self,
        image_path: str,
        system_message: str,
        user_message: str,
        model_name: str
    ) -> str:
        """Get AI response using Ollama service."""
        if not self._client:
            raise ValueError(
                "Ollama client not available. Please install ollama package."
            )

        if not self.is_service_available():
            raise ConnectionError(
                "Ollama service is not running. Please start Ollama service first."
            )

        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        try:
            response = self._client.chat(
                model=model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': system_message
                    },
                    {
                        'role': 'user',
                        'content': user_message,
                        'images': [image_data]
                    }
                ]
            )

            return response['message']['content']

        except Exception as e:
            if "model not found" in str(e).lower():
                raise ValueError(
                    f"Model '{model_name}' not found. Please pull the model first: "
                    f"ollama pull {model_name}"
                ) from e
            else:
                raise RuntimeError(f"Ollama request failed: {str(e)}") from e

    def validate_configuration(self) -> bool:
        """Validate Ollama provider configuration."""
        return self._client is not None and self.is_service_available()

    def list_available_models(self) -> List[Model]:
        """List available Ollama models."""
        ollama_models = [
            Model(
                name="llama3.2-vision:latest",
                pretty_name="Llama 3.2 Vision",
                provider="Ollama",
                rate_limit="Unlimited (Local)",
                provider_type="ollama",
                ollama_model_name="llama3.2-vision:latest",
            ),
            Model(
                name="llava:13b",
                pretty_name="LLaVA 13B",
                provider="Ollama",
                rate_limit="Unlimited (Local)",
                provider_type="ollama",
                ollama_model_name="llava:13b",
            ),
            Model(
                name="llava:7b",
                pretty_name="LLaVA 7B",
                provider="Ollama",
                rate_limit="Unlimited (Local)",
                provider_type="ollama",
                ollama_model_name="llava:7b",
            ),
        ]

        # Filter to only return models that are actually pulled locally
        if self._client and self.is_service_available():
            try:
                local_models = self._client.list()
                local_model_names = {
                    model['name'] for model in local_models.get('models', [])
                }
                return [
                    model for model in ollama_models
                    if model.name in local_model_names
                ]
            except Exception:
                # If we can't check local models, return the full list
                pass

        return ollama_models

    def is_service_available(self) -> bool:
        """Check if Ollama service is available."""
        if not self._client:
            return False

        try:
            # Try to list models to check if service is running
            self._client.list()
            return True
        except Exception:
            return False

    def get_installed_models(self) -> List[str]:
        """Get list of locally installed Ollama models."""
        if not self._client or not self.is_service_available():
            return []

        try:
            response = self._client.list()
            # Handle both old dict format and new Model object format
            models = []
            for model in response.get('models', []):
                if hasattr(model, 'model'):
                    models.append(model.model)
                elif isinstance(model, dict) and 'name' in model:
                    models.append(model['name'])
            return models
        except Exception:
            return []
