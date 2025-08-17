from dataclasses import dataclass
from typing import Dict, Any
from .base import BaseFormat


@dataclass
class MarkdownConfig(BaseFormat):
    """Dataclass for Markdown output format."""

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "MarkdownConfig":
        """Create MarkdownConfig from configuration dictionary"""
        return cls(
            system_message_content=config.get("system_message_content", ""),
            user_message_content=config.get("user_message_content", ""),
            file_extension=config.get("file_extension", ".md"),
            content_type=config.get("content_type", "text/markdown"),
        )


def get_markdown_config() -> MarkdownConfig:
    """Returns the configuration for the Markdown output format."""
    from config import get_format_config

    config = get_format_config("markdown")

    if config:
        return MarkdownConfig.from_config(config)

    return MarkdownConfig(
        system_message_content=(
            "You are a helpful assistant that transforms handwritten images "
            "into well-structured Markdown files."
        ),
        user_message_content=(
            "Convert the handwritten text in this image to Markdown format. "
            "Add a descriptive title as the first line (starting with #). "
            "Structure the content with appropriate headers, lists, and formatting. "
            "Only return the Markdown content, do not describe the image."
        ),
        file_extension=".md",
        content_type="text/markdown",
    )
