from dataclasses import dataclass
from typing import Dict, Any
from .base import BaseFormat


@dataclass
class JsonConfig(BaseFormat):
    """Dataclass for JSON output format."""

    pretty_print: bool = True
    ensure_ascii: bool = False

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "JsonConfig":
        """Create JsonConfig from configuration dictionary"""
        return cls(
            system_message_content=config.get("system_message_content", ""),
            user_message_content=config.get("user_message_content", ""),
            file_extension=config.get("file_extension", ".json"),
            content_type=config.get("content_type", "application/json"),
            pretty_print=config.get("pretty_print", True),
            ensure_ascii=config.get("ensure_ascii", False),
        )


def get_json_config() -> JsonConfig:
    """Returns the configuration for the JSON output format."""
    from config import get_format_config

    config = get_format_config("json")

    if config:
        return JsonConfig.from_config(config)

    return JsonConfig(
        system_message_content=(
            "You are a helpful assistant that extracts structured data "
            "from handwritten images and formats it as JSON."
        ),
        user_message_content=(
            "Extract the text from this handwritten image and structure it as JSON. "
            "Include a 'title' field for the main topic, 'content' field for the "
            "main text, and 'sections' array if there are multiple topics or "
            "bullet points. Return only valid JSON, no explanations."
        ),
        file_extension=".json",
        content_type="application/json",
        pretty_print=True,
        ensure_ascii=False,
    )
