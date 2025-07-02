from dataclasses import dataclass


@dataclass
class BaseFormat:
    """Base dataclass for output formats."""

    system_message_content: str
    user_message_content: str
    file_extension: str
    content_type: str
