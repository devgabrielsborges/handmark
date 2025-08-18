from dataclasses import dataclass
from typing import Dict, Any
from .base import BaseFormat


@dataclass
class XmlConfig(BaseFormat):
    """Dataclass for XML output format."""

    encoding: str = "utf-8"
    pretty_print: bool = True

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "XmlConfig":
        """Create XmlConfig from configuration dictionary"""
        return cls(
            system_message_content=config.get("system_message_content", ""),
            user_message_content=config.get("user_message_content", ""),
            file_extension=config.get("file_extension", ".xml"),
            content_type=config.get("content_type", "application/xml"),
            encoding=config.get("encoding", "utf-8"),
            pretty_print=config.get("pretty_print", True),
        )


def get_xml_config() -> XmlConfig:
    """Returns the configuration for the XML output format."""
    from config import get_format_config

    config = get_format_config("xml")

    if config:
        return XmlConfig.from_config(config)

    return XmlConfig(
        system_message_content=(
            "You are a helpful assistant that extracts structured data "
            "from handwritten images and formats it as XML."
        ),
        user_message_content=(
            "Extract the text from this handwritten image and structure it as XML. "
            "Use a root element called 'document' with child elements for 'title', "
            "'content', and 'sections' if applicable. ALWAYS include a 'title' element "
            "with a descriptive title for the content. Return only valid XML, "
            "no explanations."
        ),
        file_extension=".xml",
        content_type="application/xml",
        encoding="utf-8",
        pretty_print=True,
    )
