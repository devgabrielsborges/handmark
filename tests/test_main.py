# tests/test_main.py
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner
from rich.text import Text

from src.main import app
from src.model import Model


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_token_main_scope")


@patch("src.main.typer.prompt", return_value="test_token_auth_success")
@patch("src.main.save_github_token", return_value=(True, "/path/to/.env"))
@patch("src.main.console.print")
def test_auth_success(mock_console_print, mock_save_token, mock_prompt, runner):
    result = runner.invoke(app, ["auth"])
    assert result.exit_code == 0
    mock_prompt.assert_called_once_with(
        "Please enter your GitHub token", hide_input=True
    )
    mock_save_token.assert_called_once_with("test_token_auth_success")
    mock_console_print.assert_any_call("[green]Token stored in /path/to/.env[/green]")
    mock_console_print.assert_any_call("[green]Configuration complete.[/green]")


@patch("src.main.typer.prompt", return_value="")
@patch("src.main.save_github_token")
@patch("src.main.console.print")
def test_auth_empty_token(mock_console_print, mock_save_token, mock_prompt, runner):
    result = runner.invoke(app, ["auth"])
    assert result.exit_code == 0
    mock_prompt.assert_called_once_with(
        "Please enter your GitHub token", hide_input=True
    )
    mock_save_token.assert_not_called()
    mock_console_print.assert_called_with(
        "[yellow]No token provided. Configuration cancelled.[/yellow]"
    )


@patch("src.main.typer.prompt", return_value="test_token_auth_fail")
@patch("src.main.save_github_token", return_value=(False, "Mocked save error"))
@patch("src.main.console.print")
def test_auth_save_failure(mock_console_print, mock_save_token, mock_prompt, runner):
    result = runner.invoke(app, ["auth"])
    assert result.exit_code == 0
    mock_prompt.assert_called_once_with(
        "Please enter your GitHub token", hide_input=True
    )
    mock_save_token.assert_called_once_with("test_token_auth_fail")
    mock_console_print.assert_called_with("[red]Mocked save error[/red]")


@patch("src.main.get_available_models")
@patch("src.main.load_selected_model")
@patch("src.main.save_selected_model")
@patch("src.main.typer.prompt")
@patch("src.main.console.print")
def test_configure_model_success(
    mock_console_print,
    mock_prompt,
    mock_save_model,
    mock_load_model,
    mock_get_models,
    runner,
):
    mock_models_list = [
        Model("model1", "Model 1", "providerA", "100/day"),
        Model("model2", "Model 2", "providerB", "200/day"),
    ]
    mock_get_models.return_value = mock_models_list
    mock_load_model.return_value = None
    mock_prompt.return_value = "1"
    mock_save_model.return_value = True

    result = runner.invoke(app, ["conf"])

    assert result.exit_code == 0
    mock_get_models.assert_called_once()
    mock_save_model.assert_called_once_with(mock_models_list[0])


@patch("src.main.get_available_models")
@patch("src.main.load_selected_model")
@patch("src.main.save_selected_model")
@patch("src.main.typer.prompt")
@patch("src.main.console.print")
def test_configure_model_invalid_selection_number(
    mock_console_print,
    mock_prompt,
    mock_save_model,
    mock_load_model,
    mock_get_models,
    runner,
):
    mock_models_list = [Model("model1", "Model 1", "providerA", "100/day")]
    mock_get_models.return_value = mock_models_list
    current_model_mock = Model("current_model", "Current Model", "providerC", "50/day")
    mock_load_model.return_value = current_model_mock
    mock_prompt.return_value = "999"  # Out of range selection

    result = runner.invoke(app, ["conf"])

    assert result.exit_code == 0
    # Should print invalid selection message
    error_calls = [
        call
        for call in mock_console_print.call_args_list
        if "Invalid selection" in str(call)
    ]
    assert len(error_calls) > 0


@patch("src.main.get_available_models")
@patch("src.main.load_selected_model")
@patch("src.main.save_selected_model")
@patch("src.main.typer.prompt")
@patch("src.main.console.print")
def test_configure_model_invalid_input_str(
    mock_console_print,
    mock_prompt,
    mock_save_model,
    mock_load_model,
    mock_get_models,
    runner,
):
    mock_models_list = [Model("model1", "Model 1", "providerA", "100/day")]
    mock_get_models.return_value = mock_models_list
    mock_load_model.return_value = None
    mock_prompt.return_value = "invalid_string"

    result = runner.invoke(app, ["conf"])

    assert result.exit_code == 0
    # Should print invalid input message
    error_calls = [
        call
        for call in mock_console_print.call_args_list
        if "Invalid input" in str(call)
    ]
    assert len(error_calls) > 0


@patch("src.main.get_available_models")
@patch("src.main.load_selected_model")
@patch("src.main.save_selected_model")
@patch("src.main.typer.prompt", side_effect=KeyboardInterrupt)
@patch("src.main.console.print")
def test_configure_model_keyboard_interrupt(
    mock_console_print,
    mock_prompt,
    mock_save_model,
    mock_load_model,
    mock_get_models,
    runner,
):
    mock_models_list = [Model("model1", "Model 1", "providerA", "100/day")]
    mock_get_models.return_value = mock_models_list
    mock_load_model.return_value = None

    result = runner.invoke(app, ["conf"])

    assert result.exit_code == 0
    mock_console_print.assert_any_call("\n[yellow]Configuration cancelled.[/yellow]")


@patch("src.main.validate_image_path", return_value=(False, "Image not found"))
@patch("src.main.console.print")
def test_digest_invalid_image(mock_console_print, mock_validate_path, runner):
    result = runner.invoke(app, ["digest", "invalid.jpg"])

    assert result.exit_code == 1
    mock_validate_path.assert_called_once_with(Path("invalid.jpg"))
    mock_console_print.assert_any_call("[red]Error: Image not found[/red]")


@patch("src.main.validate_image_path", return_value=(True, None))
@patch(
    "src.main.validate_github_token",
    return_value=(
        False,
        "Token missing (mocked for test)",
        "Get a token (mocked for test)",
    ),
)
@patch("src.main.console.print")
def test_digest_invalid_token(
    mock_console_print, mock_validate_token, mock_validate_path, runner
):
    result = runner.invoke(app, ["digest", "valid.jpg"])

    assert result.exit_code == 1
    mock_validate_path.assert_called_once_with(Path("valid.jpg"))
    mock_validate_token.assert_called_once()


@patch("src.main.validate_image_path", return_value=(True, None))
@patch("src.main.validate_github_token", return_value=(True, None, None))
@patch("src.main.load_selected_model")
@patch("src.main.get_default_model")
@patch("src.main.ImageDissector")
@patch("src.main.console.status")
@patch("src.main.console.print")
def test_digest_success_with_format(
    mock_console_print,
    mock_console_status,
    mock_dissector,
    mock_get_default_model,
    mock_load_selected_model,
    mock_validate_token,
    mock_validate_path,
    runner,
):
    """Test digest command with different output formats."""
    mock_image_dissector_instance = MagicMock()
    mock_image_dissector_instance.write_response.return_value = "/path/to/output.json"
    mock_dissector.return_value = mock_image_dissector_instance

    mock_loaded_model = Model("test-model", "Test Model", "Test", "N/A")
    mock_load_selected_model.return_value = mock_loaded_model

    mock_console_status.return_value.__enter__.return_value = MagicMock()

    # Test with JSON format
    result = runner.invoke(app, ["digest", "test.jpg", "--format", "json"])

    assert result.exit_code == 0
    mock_dissector.assert_called_once_with(
        image_path=str(Path("test.jpg")),
        model=mock_loaded_model.name,
        output_format="json",
    )


def test_digest_invalid_format(runner):
    """Test digest command with invalid format."""
    result = runner.invoke(app, ["digest", "test.jpg", "--format", "invalid"])

    assert result.exit_code == 1
    assert "Invalid format" in result.stdout


def test_callback_version(runner):
    """Test version callback."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "handmark version 0.4.0" in result.stdout


def test_callback_no_command(runner):
    """Test main callback without command shows help."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout


def test_app_integration_help(runner):
    """Test that app help displays correctly."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Transform handwritten images" in result.stdout
    assert "digest" in result.stdout
    assert "auth" in result.stdout
    assert "conf" in result.stdout
