from dataclasses import dataclass
from .base import BaseFormat


@dataclass
class JsonConfig(BaseFormat):
    """Dataclass for JSON output format."""

    pretty_print: bool = True
    ensure_ascii: bool = False


def get_json_config() -> JsonConfig:
    """Returns the configuration for the JSON output format."""
    return JsonConfig(
        system_message_content="You are a helpful assistant that extracts structured data from handwritten images and formats it as JSON.",
        user_message_content="Extract the text from this handwritten image and structure it as JSON. Include a 'title' field for the main topic, 'content' field for the main text, and 'sections' array if there are multiple topics or bullet points. Return only valid JSON, no explanations.",
        file_extension=".json",
        content_type="application/json",
        pretty_print=True,
        ensure_ascii=False,
    )
