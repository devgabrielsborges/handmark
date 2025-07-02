from dataclasses import dataclass
from .base import BaseFormat


@dataclass
class YamlConfig(BaseFormat):
    """Dataclass for YAML output format."""

    default_flow_style: bool = False
    allow_unicode: bool = True


def get_yaml_config() -> YamlConfig:
    """Returns the configuration for the YAML output format."""
    return YamlConfig(
        system_message_content="You are a helpful assistant that extracts structured data from handwritten images and formats it as YAML.",
        user_message_content="Extract the text from this handwritten image and structure it as YAML. Include a 'title' field for the main topic, 'content' field for the main text, and 'sections' list if there are multiple topics or bullet points. Return only valid YAML, no explanations.",
        file_extension=".yaml",
        content_type="application/x-yaml",
        default_flow_style=False,
        allow_unicode=True,
    )
