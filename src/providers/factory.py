"""Provider factory for AI services."""

from .base import BaseProvider
from .azure_provider import AzureProvider
from .ollama_provider import OllamaProvider
from model import Model


def create_provider(model: Model) -> BaseProvider:
    """Create appropriate provider based on model.

    Args:
        model: The model to use for processing

    Returns:
        BaseProvider: Configured provider instance

    Raises:
        ValueError: If provider type is not supported
    """
    # Use the provider_type field from the model
    if model.provider_type == "ollama":
        return OllamaProvider()
    elif model.provider_type == "azure":
        return AzureProvider()
    else:
        raise ValueError(f"Unsupported provider type: {model.provider_type}")


def get_best_available_provider(preferred_model: Model = None) -> BaseProvider:
    """Get the best available provider.

    Args:
        preferred_model: Preferred model to use

    Returns:
        BaseProvider: Best available provider
    """
    if preferred_model and preferred_model.provider_type == "ollama":
        ollama_provider = OllamaProvider()
        if ollama_provider.is_service_available():
            return ollama_provider
        else:
            # Fallback to Azure if Ollama is not available
            return AzureProvider()
    
    # Default to Azure provider
    return AzureProvider()

