from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Model:
    name: str
    pretty_name: str
    provider: str
    rate_limit: str
    provider_type: str = "azure"  # "azure" or "ollama"
    ollama_model_name: Optional[str] = None

    def __str__(self):
        return f"{self.pretty_name} | {self.provider} | {self.rate_limit}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "pretty_name": self.pretty_name,
            "provider": self.provider,
            "rate_limit": self.rate_limit,
            "provider_type": self.provider_type,
            "ollama_model_name": self.ollama_model_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Model":
        return cls(
            name=data["name"],
            # fallback to name if pretty_name missing
            pretty_name=data.get("pretty_name", data["name"]),
            provider=data["provider"],
            rate_limit=data["rate_limit"],
            provider_type=data.get("provider_type", "azure"),
            ollama_model_name=data.get("ollama_model_name"),
        )


def get_available_models() -> List[Model]:
    """Get list of available models from configuration"""
    from config import get_available_models_from_config

    models_config = get_available_models_from_config()
    models = []

    for model_data in models_config:
        models.append(
            Model(
                name=model_data["name"],
                pretty_name=model_data["pretty_name"],
                provider=model_data["provider"],
                rate_limit=model_data["rate_limit"],
                provider_type=model_data.get("provider_type", "azure"),
                ollama_model_name=model_data.get("ollama_model_name"),
            )
        )

    if not models:
        models = [
            Model(
                "microsoft/Phi-4-multimodal-instruct",
                "Phi-4-multimodal-instruct",
                "Microsoft",
                "150 requests/day",
            ),
            Model("openai/gpt-4.1-nano", "GPT-4.1 Nano", "OpenAI", "150 requests/day"),
            Model("openai/gpt-4.1-mini", "GPT-4.1 Mini", "OpenAI", "150 requests/day"),
            Model(
                "microsoft/Phi-3.5-vision-instruct",
                "Phi-3.5-vision-instruct",
                "Microsoft",
                "150 requests/day",
            ),
            Model(
                "meta/Llama-4-Maverick-17B-128E-Instruct-FP8",
                "Llama-4-Maverick-17B-128E-Instruct-FP8",
                "Meta",
                "50 requests/day",
            ),
            Model(
                "meta/Llama-4-Scout-17B-16E-Instruct",
                "Llama-4-Scout-17B-16E-Instruct",
                "Meta",
                "50 requests/day",
            ),
        ]

    return models


def save_selected_model(model: Model) -> bool:
    from config import save_selected_model as config_save_model

    return config_save_model(model)


def load_selected_model() -> Optional[Model]:
    from config import get_selected_model

    return get_selected_model()


def get_default_model() -> Model:
    from config import get_default_model_from_config

    default_config = get_default_model_from_config()
    return Model(
        name=default_config["name"],
        pretty_name=default_config["pretty_name"],
        provider=default_config["provider"],
        rate_limit=default_config["rate_limit"],
        provider_type=default_config.get("provider_type", "azure"),
        ollama_model_name=default_config.get("ollama_model_name"),
    )
