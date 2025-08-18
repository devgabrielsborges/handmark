from pathlib import Path
import typer
from rich.panel import Panel
from rich.text import Text
from dissector import ImageDissector
from model import (
    get_available_models,
    get_default_model,
)
from config import (
    initialize_config,
    get_selected_model,
    save_selected_model,
    save_github_token,
)
from utils import (
    console,
    validate_image_path,
    validate_github_token,
)


def version_callback(value: bool):
    if value:
        console.print("handmark version 0.4.0")
        raise typer.Exit()


app = typer.Typer(
    help="Transform handwritten images into structured documents (MD, JSON, YAML, XML).",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """Main callback for the application."""
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit()


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


@app.command("set-model")
def configure_model():
    """Configure the AI model to use for processing images."""
    from utils import check_ollama_service

    console.print(Panel("Model Configuration", style="blue"))

    models = get_available_models()
    current_model = get_selected_model()

    if current_model:
        console.print(f"[blue]Current model:[/blue] {current_model}")
        console.print()

    azure_models = [m for m in models if m.provider_type == "azure"]
    ollama_models = [m for m in models if m.provider_type == "ollama"]

    console.print("[bold]Available models:[/bold]")
    model_list = []
    counter = 1

    if azure_models:
        console.print("\n[bold cyan]Azure AI Models (Remote):[/bold cyan]")
        for model in azure_models:
            status = "[green]✓[/green]"
            console.print(
                f"  {counter}. {model.pretty_name} | {model.provider} | {status}"
            )
            model_list.append(model)
            counter += 1

    if ollama_models:
        console.print("\n[bold magenta]Ollama Models (Local):[/bold magenta]")
        ollama_available = check_ollama_service()

        for model in ollama_models:
            if ollama_available:
                from utils import validate_ollama_model

                model_name = model.ollama_model_name or model.name
                if validate_ollama_model(model_name):
                    status = "[green]✓ Available[/green]"
                else:
                    status = "[yellow]⚠ Not installed[/yellow]"
            else:
                status = "[red]✗ Service not running[/red]"

            console.print(
                f"  {counter}. {model.pretty_name} | {model.provider} | {status}"
            )
            model_list.append(model)
            counter += 1

    try:
        selection = typer.prompt("\nSelect a model (enter number)")

        try:
            model_index = int(selection) - 1
            if 0 <= model_index < len(model_list):
                selected_model = model_list[model_index]

                if selected_model.provider_type == "ollama":
                    if not check_ollama_service():
                        console.print("[red]✗ Ollama service is not running![/red]")
                        console.print(
                            "[yellow]Please start Ollama service first.[/yellow]"
                        )
                        return

                    model_name = selected_model.ollama_model_name or selected_model.name
                    from utils import validate_ollama_model

                    if not validate_ollama_model(model_name):
                        console.print(
                            f"[red]✗ Model '{model_name}' is not installed![/red]"
                        )
                        console.print(
                            f"[yellow]Install with: ollama pull {model_name}[/yellow]"
                        )
                        return

                if save_selected_model(selected_model):
                    console.print("\n[green]✓ Model configured successfully![/green]")
                    console.print(f"[bold]Selected:[/bold] {selected_model}")
                else:
                    console.print("[red]✗ Failed to save model configuration.[/red]")
            else:
                console.print(
                    f"[red]Invalid selection. Please choose a number between 1 "
                    f"and {len(model_list)}.[/red]"
                )

        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Configuration cancelled.[/yellow]")


@app.command("test-connection")
def test_connection():
    """Test connection to the AI service."""
    from config import get_github_token, get_selected_model
    from model import get_default_model

    console.print(Panel("Testing AI Service Connection", style="blue"))

    token = get_github_token()
    if not token:
        console.print("[red]✗ No GitHub token found[/red]")
        console.print("[yellow]Run 'handmark auth' to configure your token[/yellow]")
        raise typer.Exit(code=1)

    console.print("[green]✓ GitHub token found[/green]")

    selected_model = get_selected_model()
    if not selected_model:
        selected_model = get_default_model()
        console.print(f"[yellow]Using default model: {selected_model.name}[/yellow]")
    else:
        console.print(f"[blue]Using selected model: {selected_model.name}[/blue]")

    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.inference.models import (
            SystemMessage,
            UserMessage,
            TextContentItem,
        )

        client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(token),
        )

        console.print("[yellow]Testing connection to AI service...[/yellow]")

        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(
                    content=[TextContentItem(text="Hello, respond with just 'OK'")]
                ),
            ],
            model=selected_model.name,
        )

        if response and response.choices:
            console.print("[green]✓ Connection successful![/green]")
            console.print(f"[green]✓ Model {selected_model.name} is responding[/green]")
            return
        else:
            console.print("[red]✗ Empty response from service[/red]")
            raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[red]✗ Connection failed: {str(e)}[/red]")
        if "timeout" in str(e).lower():
            console.print(
                "[yellow]💡 Network timeout - check your connection and try again[/yellow]"
            )
        elif "unauthorized" in str(e).lower():
            console.print(
                "[yellow]💡 Authentication failed - check your GitHub token[/yellow]"
            )
        else:
            console.print(
                "[yellow]💡 Service might be temporarily unavailable[/yellow]"
            )
        raise typer.Exit(code=1)


@app.command("digest")
def digest(
    image_path: Path = typer.Argument(
        ..., help="Path to the image file to process.", show_default=False
    ),
    output: Path = typer.Option(
        "./",
        "-o",
        "--output",
        help="Directory to save the output file (default: current directory).",
    ),
    filename: str = typer.Option(
        None,
        "--filename",
        help="Name of the output file (default: auto-generated based on content).",
    ),
    format: str = typer.Option(
        "markdown",
        "-f",
        "--format",
        help="Output format: markdown, json, yaml, or xml (default: markdown).",
    ),
):
    """Process a handwritten image and convert it to the specified format."""
    valid_formats = ["markdown", "json", "yaml", "xml"]
    if format.lower() not in valid_formats:
        formats_str = ", ".join(valid_formats)
        error_msg = f"[red]Error: Invalid format '{format}'. Valid formats: "
        error_msg += f"{formats_str}[/red]"
        console.print(error_msg)
        raise typer.Exit(code=1)

    valid_path, error_msg = validate_image_path(image_path)
    if not valid_path:
        console.print(f"[red]Error: {error_msg}[/red]")
        raise typer.Exit(code=1)

    token_valid, error_msg, guidance_msg = validate_github_token()
    if not token_valid:
        console.print(Text(error_msg, style="red"))
        console.print(Text(guidance_msg, style="yellow"))
        raise typer.Exit(code=1)

    selected_model = get_selected_model()
    if not selected_model:
        selected_model = get_default_model()
        console.print(
            f"[yellow]No model configured. Using default: {selected_model.name}[/yellow]"
        )
    else:
        console.print(
            f"[blue]Using model: {selected_model.name} ({selected_model.provider})[/blue]"
        )

    console.print(f"[blue]Output format: {format.upper()}[/blue]")

    format_upper = format.upper()
    status_msg = f"[bold green]Processing image to {format_upper}...[/bold green]"
    with console.status(status_msg):
        try:
            sample = ImageDissector(
                image_path=str(image_path),
                model=selected_model,
                output_format=format.lower(),
            )
            output_dir = output.absolute()

            actual_output_path = sample.write_response(
                dest_path=str(output_dir),
                fallback_filename=filename,
            )

            console.print("[green]✓ Image processed successfully![/green]")
            console.print(f"[bold]Output file saved to:[/bold] {actual_output_path}")
        except TimeoutError as e:
            console.print(f"[red]✗ Timeout Error:[/red] {str(e)}")
            console.print(
                "[yellow]💡 Try again in a few minutes or use a different model "
                "with 'handmark set-model'[/yellow]"
            )
            raise typer.Exit(code=1)
        except ValueError as e:
            if "token" in str(e).lower() or "auth" in str(e).lower():
                console.print(f"[red]✗ Authentication Error:[/red] {str(e)}")
                console.print(
                    "[yellow]💡 Run 'handmark auth' to configure your "
                    "GitHub token[/yellow]"
                )
            else:
                console.print(f"[red]✗ Configuration Error:[/red] {str(e)}")
            raise typer.Exit(code=1)
        except RuntimeError as e:
            console.print(f"[red]✗ API Error:[/red] {str(e)}")
            console.print(
                "[yellow]💡 The API service might be temporarily unavailable. "
                "Please try again later.[/yellow]"
            )
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[red]✗ Unexpected Error:[/red] {str(e)}")
            console.print(
                "[yellow]💡 If this persists, please check your image file "
                "and try again.[/yellow]"
            )
            raise typer.Exit(code=1)


@app.command("config")
def show_config():
    """Show current configuration settings."""
    from config import load_config, load_project_config

    console.print(Panel("Current Configuration", style="blue"))

    # Show user config
    user_config = load_config()
    console.print("\n[bold]User Configuration:[/bold]")
    console.print(f"  [cyan]Selected Model:[/cyan] {user_config.selected_model}")

    token_status = "Set" if user_config.github_token else "Not Set"
    console.print(f"  [cyan]GitHub Token:[/cyan] {token_status}")

    console.print(
        f"  [cyan]Default Output Format:[/cyan] {user_config.default_output_format}"
    )
    console.print(
        f"  [cyan]Default Output Directory:[/cyan] {user_config.default_output_directory}"
    )

    # Show project config
    project_config = load_project_config()
    if project_config:
        console.print("\n[bold]Project Configuration:[/bold]")

        formats = ", ".join(project_config.get("formats", {}).keys())
        console.print(f"  [cyan]Available Formats:[/cyan] {formats}")

        models = project_config.get("available_models", [])
        console.print(
            f"  [cyan]Available Models:[/cyan] {len(models)} models configured"
        )
    else:
        console.print(
            "\n[yellow]Project configuration (config.yaml) not found.[/yellow]"
        )


@app.command("status")
def status():
    """Check provider availability and configuration status."""
    from providers.azure_provider import AzureProvider
    from utils import check_ollama_service, list_ollama_models

    console.print(Panel("Provider Status", style="blue"))

    # Check Azure provider
    console.print("[bold]Azure AI Provider:[/bold]")
    azure_provider = AzureProvider()
    if azure_provider.validate_configuration():
        console.print("  [green]✓ GitHub token configured[/green]")
        if azure_provider.is_service_available():
            console.print("  [green]✓ Service available[/green]")
        else:
            console.print("  [yellow]⚠ Service connectivity issues[/yellow]")
    else:
        console.print("  [red]✗ GitHub token not configured[/red]")
        console.print("  [yellow]  Run 'handmark auth' to configure[/yellow]")

    console.print()

    # Check Ollama provider
    console.print("[bold]Ollama Provider:[/bold]")
    if check_ollama_service():
        console.print("  [green]✓ Ollama service running[/green]")
        local_models = list_ollama_models()
        if local_models:
            console.print(
                f"  [green]✓ {len(local_models)} models available locally[/green]"
            )
            vision_models = [
                m
                for m in local_models
                if any(pattern in m.lower() for pattern in ["llava", "llama3.2-vision"])
            ]
            if vision_models:
                console.print("  [green]✓ Vision models available[/green]")
                for model in vision_models:
                    console.print(f"    • {model}")
            else:
                console.print("  [yellow]⚠ No vision models found[/yellow]")
                console.print("    Install with: ollama pull llama3.2-vision")
        else:
            console.print("  [yellow]⚠ No models installed[/yellow]")
    else:
        console.print("  [red]✗ Ollama service not running[/red]")
        console.print(
            "  [yellow]  Install and start Ollama from: https://ollama.com[/yellow]"
        )

    console.print()

    selected_model = get_selected_model()
    if selected_model:
        console.print(f"[bold]Current Model:[/bold] {selected_model.pretty_name}")
        console.print(f"[bold]Provider Type:[/bold] {selected_model.provider_type}")
    else:
        console.print("[yellow]No model configured. Run 'handmark set-model'[/yellow]")


def main():
    """Entry point that calls the app"""
    # Initialize configuration system
    initialize_config()
    app()
    return 0


if __name__ == "__main__":
    main()
