from dataclasses import dataclass
from typing import Dict, Any
from .base import BaseFormat


@dataclass
class YamlConfig(BaseFormat):
    """Dataclass for YAML output format."""

    default_flow_style: bool = False
    allow_unicode: bool = True

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "YamlConfig":
        """Create YamlConfig from configuration dictionary"""
        return cls(
            system_message_content=config.get("system_message_content", ""),
            user_message_content=config.get("user_message_content", ""),
            file_extension=config.get("file_extension", ".yaml"),
            content_type=config.get("content_type", "application/x-yaml"),
            default_flow_style=config.get("default_flow_style", False),
            allow_unicode=config.get("allow_unicode", True),
        )


def get_yaml_config() -> YamlConfig:
    """Returns the configuration for the YAML output format."""
    from config import get_format_config

    config = get_format_config("yaml")

    if config:
        return YamlConfig.from_config(config)

    return YamlConfig(
        system_message_content=(
            "You are a helpful assistant that extracts structured data "
            "from handwritten images and formats it as YAML."
        ),
        user_message_content=(
            "Extract the text from this handwritten image and structure it as YAML. "
            "Include a 'title' field for the main topic, 'content' field for the "
            "main text, and 'sections' list if there are multiple topics or "
            "bullet points. Return only valid YAML, no explanations."
        ),
        file_extension=".yaml",
        content_type="application/x-yaml",
        default_flow_style=False,
        allow_unicode=True,
    )
