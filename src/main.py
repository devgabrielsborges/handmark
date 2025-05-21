from pathlib import Path
import typer
from rich.panel import Panel
from rich.text import Text
from dissector import ImageDissector
from utils import (
    console,
    save_github_token,
    validate_image_path,
    validate_github_token,
    format_success_message,
)

app = typer.Typer(
    help="Transforms handwritten images into Markdown files.",
    add_completion=False,
)


@app.command("auth")
def handle_auth():
    """Configure GitHub token for the application."""
    console.print(Panel("Configuring GitHub token...", style="blue"))

    raw_token_input = typer.prompt("Please enter your GitHub token", hide_input=True)

    if raw_token_input:
        success, message = save_github_token(raw_token_input)
        if success:
            console.print(f"[green]Token stored in {message}[/green]")
            console.print("[green]Configuration complete.[/green]")
        else:
            console.print(f"[red]{message}[/red]")
    else:
        console.print("[yellow]No token provided. Configuration cancelled.[/yellow]")


@app.command("digest")
def digest(
    image_path: Path = typer.Argument(
        ..., help="Path to the image file to process.", show_default=False
    ),
    output: Path = typer.Option(
        "./", "-o", "--output", help="Directory to save the Markdown file (default: current directory)."
    ),
    filename: str = typer.Option(
        "response.md", "--filename", help="Name of the output Markdown file (default: response.md)."
    ),
):
    """Process a handwritten image and convert it to Markdown."""
    valid_path, error_msg = validate_image_path(image_path)
    if not valid_path:
        console.print(f"[red]Error: {error_msg}[/red]")
        raise typer.Exit(code=1)

    token_valid, error_msg, guidance_msg = validate_github_token()
    if not token_valid:
        console.print(Text(error_msg, style="red"))
        console.print(Text(guidance_msg, style="yellow"))
        raise typer.Exit(code=1)

    # Process image
    with console.status("[bold green]Processing image...[/bold green]"):
        try:
            sample = ImageDissector(image_path=str(image_path))
            output_dir = output.absolute()

            actual_output_path = sample.write_response(
                dest_path=str(output_dir), fallback_filename=filename
            )

            console.print(format_success_message(actual_output_path, image_path))
        except FileNotFoundError as e:
            console.print(f"[red]File not found: {e}[/red]")
            raise typer.Exit(code=1)
        except PermissionError as e:
            console.print(f"[red]Permission error: {e}[/red]")
            raise typer.Exit(code=1)
        except ValueError as e:
            console.print(f"[red]Value error: {e}[/red]")
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[red]An unexpected error occurred: {e}[/red]")
            raise typer.Exit(code=1)


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
):
    """Handmark - Transform handwritten notes into Markdown.
    
    A simple CLI tool to convert handwritten images to Markdown text using AI.
    Run 'handmark digest <image_path>' to process an image or 'handmark auth' to set up your GitHub token.
    """
    if version:
        from importlib.metadata import version as get_version
        try:
            app_version = get_version("handmark")
            console.print(f"[bold blue]Handmark[/bold blue] version: [green]{app_version}[/green]")
        except:
            console.print("[bold blue]Handmark[/bold blue] [yellow]development version[/yellow]")
        raise typer.Exit()
    
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit()


def main():
    """Entry point function that calls the app."""
    app()
    return 0
    

if __name__ == "__main__":
    app()
