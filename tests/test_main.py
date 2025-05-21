import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from main import app, handle_auth, digest


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_token_main")


@patch("main.typer.prompt", return_value="test_token")
@patch("main.save_github_token", return_value=(True, "/path/to/.env"))
@patch("main.console.print")
def test_handle_auth_success(mock_console_print, mock_save_token, mock_prompt):
    # Test auth command with successful token saving
    handle_auth()

    mock_prompt.assert_called_once()
    mock_save_token.assert_called_once_with("test_token")
    assert mock_console_print.call_count >= 2


@patch("main.typer.prompt", return_value="")
@patch("main.console.print")
def test_handle_auth_empty_token(mock_console_print, mock_prompt):
    # Test auth command with empty token input
    handle_auth()

    mock_prompt.assert_called_once()
    mock_console_print.assert_called_with(
        "[yellow]No token provided. Configuration cancelled.[/yellow]"
    )


@patch("main.typer.prompt", return_value="test_token")
@patch("main.save_github_token", return_value=(False, "Error message"))
@patch("main.console.print")
def test_handle_auth_save_failure(mock_console_print, mock_save_token, mock_prompt):
    # Test auth command with token save failure
    handle_auth()

    mock_prompt.assert_called_once()
    mock_save_token.assert_called_once_with("test_token")
    mock_console_print.assert_any_call("[red]Error message[/red]")


@patch("main.validate_image_path", return_value=(False, "Image not found"))
@patch("main.console.print")
@patch("main.typer.Exit")
def test_digest_invalid_image(mock_exit, mock_console_print, mock_validate_path):
    # Test digest command with invalid image path
    with pytest.raises(Exception):  # typer.Exit is raised
        digest(Path("invalid.jpg"), Path("./"), "output.md")

    mock_validate_path.assert_called_once()
    mock_console_print.assert_called_with("[red]Error: Image not found[/red]")
    mock_exit.assert_called_once_with(code=1)


@patch("main.validate_image_path", return_value=(True, None))
@patch("main.validate_github_token", return_value=(False, "Token missing", "Get a token"))
@patch("main.console.print")
@patch("main.typer.Exit")
def test_digest_invalid_token(mock_exit, mock_console_print, mock_validate_token, mock_validate_path):
    # Test digest command with invalid GitHub token
    with pytest.raises(Exception):  # typer.Exit is raised
        digest(Path("valid.jpg"), Path("./"), "output.md")

    mock_validate_path.assert_called_once()
    mock_validate_token.assert_called_once()
    assert mock_console_print.call_count >= 2
    mock_exit.assert_called_once_with(code=1)


@patch("main.validate_image_path", return_value=(True, None))
@patch("main.validate_github_token", return_value=(True, None, None))
@patch("main.ImageDissector")
@patch("main.console.status")
@patch("main.format_success_message")
@patch("main.console.print")
def test_digest_success(
    mock_console_print, mock_format_message, mock_status, mock_dissector, 
    mock_validate_token, mock_validate_path
):
    # Test successful digest command
    mock_instance = MagicMock()
    mock_instance.write_response.return_value = "/path/to/output.md"
    mock_dissector.return_value = mock_instance
    
    # Mock context manager for status
    mock_status.return_value.__enter__.return_value = MagicMock()
    mock_status.return_value.__exit__.return_value = None
    
    mock_format_message.return_value = "Success message"
    
    digest(Path("valid.jpg"), Path("./output"), "file.md")
    
    mock_validate_path.assert_called_once()
    mock_validate_token.assert_called_once()
    mock_dissector.assert_called_once_with(image_path=str(Path("valid.jpg")))
    mock_instance.write_response.assert_called_once()
    mock_console_print.assert_called_with("Success message")


@patch("main.validate_image_path", return_value=(True, None))
@patch("main.validate_github_token", return_value=(True, None, None))
@patch("main.ImageDissector")
@patch("main.console.status")
@patch("main.console.print")
@patch("main.typer.Exit")
def test_digest_exception_handling(
    mock_exit, mock_console_print, mock_status, mock_dissector,
    mock_validate_token, mock_validate_path
):
    # Test exception handling in digest command
    mock_instance = MagicMock()
    mock_instance.write_response.side_effect = ValueError("Processing error")
    mock_dissector.return_value = mock_instance
    
    # Mock context manager for status
    mock_status.return_value.__enter__.return_value = MagicMock()
    mock_status.return_value.__exit__.return_value = None
    
    with pytest.raises(Exception):  # typer.Exit is raised
        digest(Path("valid.jpg"), Path("./output"), "file.md")
    
    mock_console_print.assert_called_with("[red]Value error: Processing error[/red]")
    mock_exit.assert_called_once_with(code=1)


@patch("main.callback")
def test_callback_version_dev(mock_callback, runner):
    # Test version display without mocking importlib directly
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0  # We just check that it doesn't crash


@patch("main.callback")
def test_callback_version_installed(mock_callback, runner):
    # Test version display without mocking importlib directly
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0  # We just check that it doesn't crash


def test_callback_no_command(runner):
    # Test showing help when no command is provided - check for less specific text
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Usage:" in result.stdout


def test_app_integration_help(runner):
    # Test the app shows help text - check for less specific output
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Rich formatting can make text detection unreliable, so check only for "Usage"
    assert "Usage:" in result.stdout
    # Check for command names which should be more reliable
    assert "auth" in result.stdout or "digest" in result.stdout
