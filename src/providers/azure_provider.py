"""Azure AI provider implementation."""

import time
from typing import List
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
    TextContentItem,
    ImageContentItem,
    ImageUrl,
    ImageDetailLevel,
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import (
    HttpResponseError,
    ServiceRequestTimeoutError,
    ServiceResponseError,
)
from .base import BaseProvider
from model import Model


class AzureProvider(BaseProvider):
    """Azure AI provider for image processing."""

    def __init__(self):
        self._token = None
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Azure AI client."""
        from config import get_github_token

        self._token = get_github_token()
        if self._token:
            self._client = ChatCompletionsClient(
                endpoint="https://models.github.ai/inference",
                credential=AzureKeyCredential(self._token),
            )

    def get_response(
        self, image_path: str, system_message: str, user_message: str, model_name: str
    ) -> str:
        """Get AI response using Azure AI service."""
        if not self._client:
            raise ValueError(
                "GITHUB_TOKEN was not found in environment or configuration."
            )

        image_format = image_path.split(".")[-1]
        max_retries = 3
        base_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                response = self._client.complete(
                    messages=[
                        SystemMessage(content=system_message),
                        UserMessage(
                            content=[
                                TextContentItem(text=user_message),
                                ImageContentItem(
                                    image_url=ImageUrl.load(
                                        image_file=image_path,
                                        image_format=image_format,
                                        detail=ImageDetailLevel.LOW,
                                    )
                                ),
                            ],
                        ),
                    ],
                    model=model_name,
                )

                return response.choices[0].message.content

            except (
                HttpResponseError,
                ServiceRequestTimeoutError,
                ServiceResponseError,
            ) as e:
                if attempt == max_retries - 1:  # Last attempt
                    if "Read timed out" in str(e) or "timeout" in str(e).lower():
                        raise TimeoutError(
                            f"Request timed out after {max_retries} attempts. "
                            "The API might be experiencing high load. "
                            "Please try again later."
                        ) from e
                    elif "Unauthorized" in str(e):
                        raise ValueError(
                            "Authentication failed. Please check your GitHub token "
                            "with 'handmark auth'."
                        ) from e
                    else:
                        raise RuntimeError(f"API request failed: {str(e)}") from e

                delay = base_delay * (2**attempt)
                time.sleep(delay)

            except Exception as e:
                # For any other unexpected errors
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Unexpected error occurred: {str(e)}") from e

                delay = base_delay * (2**attempt)
                time.sleep(delay)

        # This should never be reached, but added for safety
        raise RuntimeError("Maximum retries exceeded")

    def validate_configuration(self) -> bool:
        """Validate Azure provider configuration."""
        return self._token is not None

    def list_available_models(self) -> List[Model]:
        """List available Azure AI models."""
        from config import get_available_models_from_config

        models_config = get_available_models_from_config()
        azure_models = []

        for model_data in models_config:
            # Filter for Azure/remote models (non-Ollama)
            if model_data.get("provider_type", "azure") == "azure":
                azure_models.append(
                    Model(
                        name=model_data["name"],
                        pretty_name=model_data["pretty_name"],
                        provider=model_data["provider"],
                        rate_limit=model_data["rate_limit"],
                        provider_type=model_data.get("provider_type", "azure"),
                        ollama_model_name=model_data.get("ollama_model_name"),
                    )
                )

        return azure_models

    def is_service_available(self) -> bool:
        """Check if Azure AI service is available."""
        if not self._client:
            return False

        try:
            # Simple test request to check connectivity
            response = self._client.complete(
                messages=[
                    SystemMessage(content="You are a helpful assistant."),
                    UserMessage(
                        content=[TextContentItem(text="Hello, respond with just 'OK'")]
                    ),
                ],
                model="microsoft/Phi-3.5-vision-instruct",  # Use a known model
            )
            return response and response.choices
        except Exception:
            return False
