from dataclasses import dataclass
from .base import BaseFormat


@dataclass
class MarkdownConfig(BaseFormat):
    """Dataclass for Markdown output format."""

    pass


def get_markdown_config() -> MarkdownConfig:
    """Returns the configuration for the Markdown output format."""
    return MarkdownConfig(
        system_message_content="You are a helpful assistant that transforms handwritten images into well-structured Markdown files.",
        user_message_content="Convert the handwritten text in this image to Markdown format. Add a descriptive title as the first line (starting with #). Structure the content with appropriate headers, lists, and formatting. Only return the Markdown content, do not describe the image.",
        file_extension=".md",
        content_type="text/markdown",
    )
