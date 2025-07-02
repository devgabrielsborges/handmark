import os
from pathlib import Path
from typing import Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

console = Console()


def load_github_token() -> Optional[str]:
    """Load GitHub token from environment or .env file"""
    github_token_env = os.getenv("GITHUB_TOKEN")

    if not github_token_env:
        project_dir = Path(__file__).parent.parent
        dotenv_path = project_dir / ".env"

        if dotenv_path.exists():
            load_dotenv(dotenv_path)
            github_token_env = os.getenv("GITHUB_TOKEN")

    return github_token_env


def save_github_token(token: str) -> Tuple[bool, str]:
    """Save GitHub token to .env file

    Returns:
        Tuple[bool, str]: Success status and message
    """
    if not token:
        return False, "No token provided"

    cleaned_token = token.strip()
    project_dir = Path(__file__).parent.parent
    env_path = project_dir / ".env"

    try:
        with open(env_path, "w") as f:
            f.write(f"GITHUB_TOKEN={cleaned_token}\n")
        return True, str(env_path)
    except OSError as e:
        return False, f"Error writing file at {env_path}: {e}"


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
            "Please set it, use 'handmark conf', or ensure .env file "
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
