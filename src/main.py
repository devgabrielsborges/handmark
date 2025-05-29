from pathlib import Path
import typer
from rich.panel import Panel
from rich.text import Text
from dissector import ImageDissector
from model import (
    get_available_models,
    save_selected_model,
    load_selected_model,
    get_default_model,
)
from utils import (
    console,
    save_github_token,
    validate_image_path,
    validate_github_token,
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


@app.command("conf")
def configure_model():
    """Configure the AI model to use for processing images."""
    console.print(Panel("Model Configuration", style="blue"))

    models = get_available_models()
    current_model = load_selected_model()

    if current_model:
        console.print(f"[blue]Current model:[/blue] {current_model}")
        console.print()

    console.print("[bold]Available models:[/bold]")
    for i, model in enumerate(models, 1):
        console.print(f"  {i}. {model}")

    try:
        selection = typer.prompt("\nSelect a model (enter number)")

        try:
            model_index = int(selection) - 1
            if 0 <= model_index < len(models):
                selected_model = models[model_index]

                if save_selected_model(selected_model):
                    console.print(f"\n[green]✓ Model configured successfully![/green]")
                    console.print(f"[bold]Selected:[/bold] {selected_model}")
                else:
                    console.print(f"[red]✗ Failed to save model configuration.[/red]")
            else:
                console.print(
                    f"[red]Invalid selection. Please choose a number between 1 and {len(models)}.[/red]"
                )

        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Configuration cancelled.[/yellow]")


@app.command("digest")
def digest(
    image_path: Path = typer.Argument(
        ..., help="Path to the image file to process.", show_default=False
    ),
    output: Path = typer.Option(
        "./",
        "-o",
        "--output",
        help="Directory to save the Markdown file (default: current directory).",
    ),
    filename: str = typer.Option(
        "response.md",
        "--filename",
        help="Name of the output Markdown file (default: response.md).",
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

    selected_model = load_selected_model()
    if not selected_model:
        selected_model = get_default_model()
        console.print(
            f"[yellow]No model configured. Using default: {selected_model.name}[/yellow]"
        )
    else:
        console.print(
            f"[blue]Using model: {selected_model.name} ({selected_model.provider})[/blue]"
        )

    with console.status("[bold green]Processing image...[/bold green]"):
        try:
            sample = ImageDissector(image_path=str(image_path), model=selected_model.name)
            output_dir = output.absolute()

            actual_output_path = sample.write_response(
                dest_path=str(output_dir),
                fallback_filename=filename,
            )

            console.print(f"[green]✓ Image processed successfully![/green]")
            console.print(f"[bold]Markdown file saved to:[/bold] {actual_output_path}")
        except Exception as e:
            console.print(f"[red]✗ Error processing image: {str(e)}[/red]")
            raise typer.Exit(code=1)


def main():
    """Entry point that calls the app"""
    app()
    return 0


if __name__ == "__main__":
    main()
