import os
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest
from rich.panel import Panel

from utils import (
    console,
    load_github_token,
    save_github_token,
    validate_image_path,
    validate_github_token,
    format_success_message,
)


@pytest.fixture(autouse=True)
def clear_env_vars(monkeypatch):
    # Clear environment variables before each test
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)


def test_load_github_token_from_env(monkeypatch):
    # Test loading token from environment variable
    monkeypatch.setenv("GITHUB_TOKEN", "test_token_env")
    assert load_github_token() == "test_token_env"


@patch("utils.load_dotenv")
@patch("pathlib.Path.exists", return_value=True)
@patch("os.getenv")
def test_load_github_token_from_dotenv(mock_getenv, mock_path_exists, mock_load_dotenv):
    # Test loading token from .env file when not in environment
    mock_getenv.side_effect = [None, "test_token_dotenv"]
    
    token = load_github_token()
    
    mock_path_exists.assert_called_once()
    mock_load_dotenv.assert_called_once()
    assert token == "test_token_dotenv"


@patch("pathlib.Path.exists", return_value=False)
def test_load_github_token_not_found(mock_path_exists):
    # Test what happens when token is not found
    token = load_github_token()
    mock_path_exists.assert_called_once()
    assert token is None


@patch("builtins.open", new_callable=mock_open)
def test_save_github_token_success(mock_file_open):
    # Test successfully saving a token
    success, message = save_github_token("test_token")
    
    assert success is True
    assert ".env" in message
    mock_file_open.assert_called_once()
    mock_file_open().write.assert_called_once_with("GITHUB_TOKEN=test_token\n")


@patch("builtins.open", side_effect=OSError("Permission denied"))
def test_save_github_token_failure(mock_file_open):
    # Test failure when saving token
    success, message = save_github_token("test_token")
    
    assert success is False
    assert "Error writing file" in message
    assert "Permission denied" in message


def test_save_github_token_empty():
    # Test saving an empty token
    success, message = save_github_token("")
    
    assert success is False
    assert message == "No token provided"


def test_validate_image_path_none():
    # Test validation when no path is provided
    valid, error = validate_image_path(None)
    
    assert valid is False
    assert "You must provide an image path" in error


@patch("pathlib.Path.exists", return_value=False)
def test_validate_image_path_not_found(mock_exists):
    # Test validation when image doesn't exist
    path = Path("non_existent.jpg")
    valid, error = validate_image_path(path)
    
    assert valid is False
    assert "not found" in error
    mock_exists.assert_called_once()


@patch("pathlib.Path.exists", return_value=True)
def test_validate_image_path_success(mock_exists):
    # Test successful validation
    path = Path("exists.jpg")
    valid, error = validate_image_path(path)
    
    assert valid is True
    assert error is None
    mock_exists.assert_called_once()


@patch("utils.load_github_token", return_value=None)
def test_validate_github_token_missing(mock_load_token):
    # Test validation when token is missing
    valid, error, guidance = validate_github_token()
    
    assert valid is False
    assert "GITHUB_TOKEN environment variable not set" in error
    assert "handmark conf" in guidance
    mock_load_token.assert_called_once()


@patch("utils.load_github_token", return_value="valid_token")
def test_validate_github_token_success(mock_load_token):
    # Test successful token validation
    valid, error, guidance = validate_github_token()
    
    assert valid is True
    assert error is None
    assert guidance is None
    mock_load_token.assert_called_once()


def test_format_success_message():
    # Test formatting of success message
    output_path = "/path/to/output.md"
    image_path = Path("input.jpg")
    
    panel = format_success_message(output_path, image_path)
    
    assert isinstance(panel, Panel)
    assert panel.title == "Success"
    assert panel.border_style == "green"
    assert "output.md" in panel.renderable
    assert "input.jpg" in panel.renderable


def test_format_success_message_long_paths():
    output_path = "/very/long/path/to/some/directory/with/output_file_with_long_name.md"
    image_path = Path("very/long/path/to/input/file/with/long_name_image_file.jpg")

    panel = format_success_message(output_path, image_path)

    assert isinstance(panel, Panel)
    assert output_path in panel.renderable
    assert str(image_path) in panel.renderable


def test_format_success_message_special_chars():
    output_path = "/path/with-special_chars!/output.md"
    image_path = Path("input-with_special~chars!.jpg")

    panel = format_success_message(output_path, image_path)

    assert isinstance(panel, Panel)
    assert output_path in panel.renderable
    assert str(image_path) in panel.renderable
