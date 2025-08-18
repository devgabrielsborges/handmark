from pathlib import Path
from typing import Optional, Tuple, List

from rich.console import Console
from rich.panel import Panel

console = Console()


def load_github_token() -> Optional[str]:
    """Load GitHub token from environment or configuration file (legacy function)"""
    from config import get_github_token

    return get_github_token()


def save_github_token(token: str) -> Tuple[bool, str]:
    """Save GitHub token to configuration file

    Returns:
        Tuple[bool, str]: Success status and message
    """
    if not token:
        return False, "No token provided"

    from config import save_github_token as config_save_token

    success = config_save_token(token)

    if success:
        return True, "Token saved to configuration"
    else:
        return False, "Error saving token to configuration"


def validate_image_path(image_path: Optional[Path]) -> Tuple[bool, Optional[str]]:
    """Validate that image path exists and is accessible

    Returns:
        Tuple[bool, Optional[str]]: Success status and error message if any
    """
    if not image_path:
        return False, "You must provide an image path using --image <path>"

    if not image_path.exists():
        return False, f"Image file not found at {image_path}"

    return True, None


def check_ollama_service() -> bool:
    """Check if Ollama service is available.
    
    Returns:
        bool: True if Ollama service is running
    """
    try:
        import ollama
        client = ollama.Client()
        client.list()
        return True
    except Exception:
        return False


def list_ollama_models() -> List[str]:
    """Get list of locally installed Ollama models.
    
    Returns:
        List[str]: List of available model names
    """
    try:
        import ollama
        client = ollama.Client()
        response = client.list()
        models = []
        for model in response.get('models', []):
            if hasattr(model, 'model'):
                models.append(model.model)
            elif isinstance(model, dict) and 'name' in model:
                models.append(model['name'])
        return models
    except Exception:
        return []


def validate_ollama_model(model_name: str) -> bool:
    """Validate that an Ollama model is available locally.
    
    Args:
        model_name: Name of the model to validate
        
    Returns:
        bool: True if model is available
    """
    return model_name in list_ollama_models()


def validate_github_token() -> Tuple[bool, Optional[str], Optional[str]]:
    """Validate GitHub token exists

    Returns:
        Tuple[bool, Optional[str], Optional[str]]: Success status,
        error message, guidance message
    """
    github_token = load_github_token()
    if not github_token:
        error = (
            "Error: GITHUB_TOKEN environment variable not set and "
            "not found in project directory."
        )
        guidance = (
            "Please set it, use 'handmark auth', or ensure .env file "
            "exists and is readable."
        )
        return False, error, guidance

    return True, None, None


def format_success_message(output_path: str, image_path: Path) -> Panel:
    """Format success message panel"""
    return Panel(
        f"Response written to [bold]{output_path}[/bold] for image: "
        f"[italic]{image_path}[/italic]",
        title="Success",
        border_style="green",
    )
