from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BaseFormat:
    """Base dataclass for output formats."""

    system_message_content: str
    user_message_content: str
    file_extension: str
    content_type: str

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "BaseFormat":
        """Create BaseFormat from configuration dictionary"""
        return cls(
            system_message_content=config.get("system_message_content", ""),
            user_message_content=config.get("user_message_content", ""),
            file_extension=config.get("file_extension", ""),
            content_type=config.get("content_type", ""),
        )
