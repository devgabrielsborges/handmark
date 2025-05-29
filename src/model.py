from dataclasses import dataclass
from typing import List, Optional
import json
from pathlib import Path

@dataclass
class Model:
    name: str
    provider: str
    rate_limit: str

    def __str__(self):
        return f"{self.name} | {self.provider} | {self.rate_limit}"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "provider": self.provider,
            "rate_limit": self.rate_limit
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Model":
        return cls(
            name=data["name"],
            provider=data["provider"],
            rate_limit=data["rate_limit"]
        )


def get_available_models() -> List[Model]:
    """Get list of available models"""
    return [
        Model("Phi-4-multimodal-instruct", "Microsoft", "150 requests/day"),
        Model("gpt-4.1-mini", "OpenAI", "150 requests/day"),
        Model("gpt-4.1-nano", "OpenAI", "150 requests/day"),
        Model("Phi-3.5-vision-instruct", "Microsoft", "150 requests/day"),
        Model("Llama-4-Maverick-17B-128E-Instruct-FP8", "Meta", "50 requests/day"),
        Model("Llama-4-Scout-17B-16E-Instruct", "Meta", "50 requests/day"),
    ]


def save_selected_model(model: Model) -> bool:
    """Save selected model to config file"""
    try:
        config_dir = Path.home() / ".config" / "handmark"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"
        
        config = {"selected_model": model.to_dict()}
        
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception:
        return False


def load_selected_model() -> Optional[Model]:
    """Load selected model from config file"""
    try:
        config_dir = Path.home() / ".config" / "handmark"
        config_file = config_dir / "config.json"

        if not config_file.exists():
            return None
 
        with open(config_file, "r") as f:
            config = json.load(f)
  
        if "selected_model" in config:
            return Model.from_dict(config["selected_model"])
   
        return None
    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError):
        return None


def get_default_model() -> Model:
    """Get default model if none is configured"""
    return Model("gpt-4o", "OpenAI", "500 requests/day")
