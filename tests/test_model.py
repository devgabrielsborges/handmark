import json
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import pytest

from model import (
    Model,
    get_available_models,
    save_selected_model,
    load_selected_model,
    get_default_model,
)

@pytest.fixture
def mock_config_home(monkeypatch):
    # Mocks Path.home() to return a MagicMock representing the home directory
    mock_home_path = MagicMock(spec=Path)
    monkeypatch.setattr(Path, "home", lambda: mock_home_path)

    mock_config_dir_path = MagicMock(spec=Path)
    mock_handmark_dir_path = MagicMock(spec=Path)
    mock_config_file_path = MagicMock(spec=Path)

    mock_home_path.__truediv__.return_value = mock_config_dir_path
    mock_config_dir_path.__truediv__.return_value = mock_handmark_dir_path
    mock_handmark_dir_path.__truediv__.return_value = mock_config_file_path

    return mock_handmark_dir_path, mock_config_file_path


def test_model_creation():
    model = Model("test-model", "TestProvider", "100 req/day")
    assert model.name == "test-model"
    assert model.provider == "TestProvider"
    assert model.rate_limit == "100 req/day"
    assert str(model) == "test-model | TestProvider | 100 req/day"


def test_model_to_dict():
    model = Model("test-model", "TestProvider", "100 req/day")
    assert model.to_dict() == {
        "name": "test-model",
        "provider": "TestProvider",
        "rate_limit": "100 req/day",
    }


def test_model_from_dict():
    data = {
        "name": "test-model",
        "provider": "TestProvider",
        "rate_limit": "100 req/day",
    }
    model = Model.from_dict(data)
    assert model.name == "test-model"
    assert model.provider == "TestProvider"
    assert model.rate_limit == "100 req/day"


def test_get_available_models():
    models = get_available_models()
    assert isinstance(models, list)
    assert len(models) > 0 # Should have at least one model
    for model in models:
        assert isinstance(model, Model)
    # Check for a known model (example, adjust if default list changes)
    assert any(m.name == "Phi-4-multimodal-instruct" for m in models)


def test_get_default_model():
    model = get_default_model()
    assert isinstance(model, Model)
    assert model.name == "gpt-4o" # As per src/model.py
    assert model.provider == "OpenAI"
    assert model.rate_limit == "500 requests/day"


@patch("json.dump")
@patch("builtins.open", new_callable=mock_open)
def test_save_selected_model_success(mock_file_open, mock_json_dump, mock_config_home):
    mock_handmark_dir, mock_config_file = mock_config_home

    model_to_save = Model("gpt-4.1-mini", "OpenAI", "150 requests/day")
    success = save_selected_model(model_to_save)

    assert success is True
    mock_handmark_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_file_open.assert_called_once_with(mock_config_file, "w")
    mock_json_dump.assert_called_once_with(
        {"selected_model": model_to_save.to_dict()}, mock_file_open(), indent=2
    )


@patch("builtins.open", side_effect=OSError("Cannot write"))
def test_save_selected_model_failure(mock_file_open_failure, mock_config_home):
    # This test ensures that if 'open' fails, save_selected_model returns False
    model_to_save = Model("gpt-4.1-mini", "OpenAI", "150 requests/day")
    success = save_selected_model(model_to_save)
    assert success is False


@patch("json.load")
@patch("builtins.open", new_callable=mock_open)
def test_load_selected_model_success(mock_file_open, mock_json_load, mock_config_home):
    mock_handmark_dir, mock_config_file = mock_config_home
    mock_config_file.exists.return_value = True

    expected_model_data = {"name": "gpt-4.1-mini", "provider": "OpenAI", "rate_limit": "150 requests/day"}
    mock_json_load.return_value = {"selected_model": expected_model_data}

    model = load_selected_model()

    assert model is not None
    assert model.name == "gpt-4.1-mini"
    mock_file_open.assert_called_once_with(mock_config_file, "r")
    mock_json_load.assert_called_once()


def test_load_selected_model_file_not_exists(mock_config_home):
    mock_handmark_dir, mock_config_file = mock_config_home
    mock_config_file.exists.return_value = False

    model = load_selected_model()
    assert model is None

@patch("builtins.open", new_callable=mock_open) # Mock open to simulate file existence
def test_load_selected_model_json_error(mock_file_open, mock_config_home):
    mock_handmark_dir, mock_config_file = mock_config_home
    mock_config_file.exists.return_value = True
    # Make the context manager for 'open' raise a JSONDecodeError when json.load is called
    # This requires json.load to be called within the 'with open(...)' block
    with patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)):
        model = load_selected_model()
        assert model is None
    
@patch("json.load")
@patch("builtins.open", new_callable=mock_open)
def test_load_selected_model_key_error(mock_file_open, mock_json_load, mock_config_home):
    mock_handmark_dir, mock_config_file = mock_config_home
    mock_config_file.exists.return_value = True
    mock_json_load.return_value = {"wrong_key": {}} # Missing "selected_model"

    model = load_selected_model()
    assert model is None

@patch("builtins.open", new_callable=mock_open)
def test_load_selected_model_os_error(mock_file_open, mock_config_home):
    mock_handmark_dir, mock_config_file = mock_config_home
    mock_config_file.exists.return_value = True
    mock_file_open.side_effect = OSError("Cannot read file")

    model = load_selected_model()
    assert model is None
