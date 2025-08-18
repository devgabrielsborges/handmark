import yaml
import os
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from model import Model


@dataclass
class AppConfig:
    """Application configuration structure"""

    selected_model: Optional[Dict[str, str]] = None
    github_token: Optional[str] = None
    default_output_format: str = "markdown"
    default_output_directory: str = "./"

    def to_dict(self) -> dict:
        """Convert config to dictionary for YAML serialization"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        """Create AppConfig from dictionary loaded from YAML"""
        return cls(
            selected_model=data.get("selected_model"),
            github_token=data.get("github_token"),
            default_output_format=data.get("default_output_format", "markdown"),
            default_output_directory=data.get("default_output_directory", "./"),
        )


def get_config_path() -> Path:
    """Get the path to the configuration file"""
    config_dir = Path.home() / ".config" / "handmark"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def get_project_config_path() -> Path:
    """Get the path to the project-wide configuration file"""
    return Path.cwd() / "config.yaml"


def load_project_config() -> dict:
    """Load the project-wide configuration from config.yaml"""
    config_path = get_project_config_path()

    if not config_path.exists():
        return {}

    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    except (yaml.YAMLError, OSError):
        return {}


def load_config() -> AppConfig:
    """Load configuration from YAML file"""
    config_path = get_config_path()

    if not config_path.exists():
        default_config = AppConfig()
        save_config(default_config)
        return default_config

    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}
        return AppConfig.from_dict(data)
    except (yaml.YAMLError, OSError):
        return AppConfig()


def save_config(config: AppConfig) -> bool:
    """Save configuration to YAML file"""
    config_path = get_config_path()

    try:
        with open(config_path, "w") as f:
            yaml.dump(config.to_dict(), f, default_flow_style=False, indent=2)
        return True
    except (yaml.YAMLError, OSError):
        return False


def get_selected_model() -> Optional[Model]:
    """Get the selected model from configuration"""
    config = load_config()

    if config.selected_model:
        try:
            return Model.from_dict(config.selected_model)
        except (KeyError, TypeError):
            pass

    return None


def save_selected_model(model: Model) -> bool:
    """Save selected model to configuration"""
    config = load_config()
    config.selected_model = model.to_dict()
    return save_config(config)


def get_github_token() -> Optional[str]:
    """Get GitHub token from configuration or environment"""
    # First check environment variable
    env_token = os.getenv("GITHUB_TOKEN")
    if env_token:
        return env_token

    config = load_config()
    return config.github_token


def save_github_token(token: str) -> bool:
    """Save GitHub token to configuration"""
    config = load_config()
    config.github_token = token.strip()
    return save_config(config)


def get_default_output_format() -> str:
    """Get default output format from configuration"""
    config = load_config()
    return config.default_output_format


def set_default_output_format(format_type: str) -> bool:
    """Set default output format in configuration"""
    config = load_config()
    config.default_output_format = format_type
    return save_config(config)


def get_default_output_directory() -> str:
    """Get default output directory from configuration"""
    config = load_config()
    return config.default_output_directory


def set_default_output_directory(directory: str) -> bool:
    """Set default output directory in configuration"""
    config = load_config()
    config.default_output_directory = directory
    return save_config(config)


def migrate_from_json_config() -> bool:
    """Migrate existing JSON configuration to YAML"""
    old_config_path = Path.home() / ".config" / "handmark" / "config.json"

    if not old_config_path.exists():
        return False

    try:
        import json

        with open(old_config_path, "r") as f:
            old_data = json.load(f)

        config = load_config()

        if "selected_model" in old_data:
            config.selected_model = old_data["selected_model"]

        success = save_config(config)

        if success:
            old_config_path.unlink()

        return success
    except (json.JSONDecodeError, OSError):
        return False


def migrate_from_env_file() -> bool:
    """Migrate GitHub token from .env file to YAML config"""
    project_dir = Path(__file__).parent.parent
    env_path = project_dir / ".env"

    if not env_path.exists():
        return False

    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
        token = os.getenv("GITHUB_TOKEN")

        if token:
            success = save_github_token(token)
            if success:
                env_path.unlink()
            return success
    except Exception:
        pass

    return False


def initialize_config() -> None:
    """Initialize configuration system and migrate old configurations"""
    # Migrate from old JSON config if it exists
    migrate_from_json_config()

    # Migrate from .env file if it exists
    migrate_from_env_file()

    # Ensure config file exists
    load_config()


def get_format_config(format_name: str) -> dict:
    """Get format configuration from project config file"""
    project_config = load_project_config()
    formats = project_config.get("formats", {})
    return formats.get(format_name, {})


def get_available_models_from_config() -> list:
    """Get available models from project configuration"""
    project_config = load_project_config()
    return project_config.get("available_models", [])


def get_default_model_from_config() -> dict:
    """Get default model from project configuration"""
    project_config = load_project_config()
    return project_config.get(
        "default_model",
        {
            "name": "openai/gpt-4o",
            "pretty_name": "GPT-4o",
            "provider": "OpenAI",
            "rate_limit": "500 requests/day",
        },
    )


def update_project_config(key_path: str, value) -> bool:
    """Update a value in the project configuration file

    Args:
        key_path: Dot-separated path to the config key (e.g., 'app.default_output_format')
        value: The new value to set

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config_path = get_project_config_path()

        if config_path.exists():
            with open(config_path, "r") as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}

        keys = key_path.split(".")
        current = config

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value

        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)

        return True
    except (yaml.YAMLError, OSError, KeyError):
        return False
