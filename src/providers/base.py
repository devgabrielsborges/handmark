"""Provider abstraction for AI services."""

from abc import ABC, abstractmethod
from typing import List
from model import Model


class BaseProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def get_response(
        self,
        image_path: str,
        system_message: str,
        user_message: str,
        model_name: str
    ) -> str:
        """Get AI response for image processing.

        Args:
            image_path: Path to the image file
            system_message: System message content
            user_message: User message content
            model_name: Name of the model to use

        Returns:
            str: AI response content
        """
        pass

    @abstractmethod
    def validate_configuration(self) -> bool:
        """Validate provider configuration.

        Returns:
            bool: True if configuration is valid
        """
        pass

    @abstractmethod
    def list_available_models(self) -> List[Model]:
        """List available models for this provider.

        Returns:
            List[Model]: Available models
        """
        pass

    @abstractmethod
    def is_service_available(self) -> bool:
        """Check if the provider service is available.

        Returns:
            bool: True if service is available
        """
        pass
