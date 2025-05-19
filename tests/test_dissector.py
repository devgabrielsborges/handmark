# Tests for dissector.py will go here

import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
from dissector import ImageDissector

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_token")


@pytest.fixture
def dissector_instance():
    # Create a dummy image file for testing
    with open("dummy_image.png", "w") as f:
        f.write("dummy image data")
    instance = ImageDissector(image_path="dummy_image.png")
    instance._client.complete = MagicMock()
    yield instance
    os.remove("dummy_image.png")  # Clean up dummy image


def test_image_dissector_initialization(dissector_instance):
    assert dissector_instance.image_path == "dummy_image.png"
    assert dissector_instance.image_format == "png"
    assert dissector_instance._token == "test_token"
    assert dissector_instance._model_name == "openai/gpt-4o"
    assert dissector_instance._client is not None


def test_image_dissector_initialization_no_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(ValueError, match="GITHUB_TOKEN was not found in environment."):
        ImageDissector(image_path="dummy_image.png")


def test_sanitize_filename_empty_and_whitespace():
    # Need an instance to call _sanitize_filename, or make it static
    dissector = ImageDissector(image_path="dummy.png")
    assert dissector._sanitize_filename("") == ""
    assert dissector._sanitize_filename("   ") == ""


def test_sanitize_filename_simple_cases(dissector_instance):
    assert dissector_instance._sanitize_filename("My Test File") == "my_test_file.md"
    assert dissector_instance._sanitize_filename("Another Title!") == "another_title.md"
    assert (
        dissector_instance._sanitize_filename("file_with_numbers_123")
        == "file_with_numbers_123.md"
    )


def test_sanitize_filename_special_characters(dissector_instance):
    assert (
        dissector_instance._sanitize_filename("A!@#$%^&*()_+{}[]|\\\\:;'\\\",.<>?/B")
        == "a_b.md"
    )
    assert (
        dissector_instance._sanitize_filename(" leading and trailing_ ")
        == "leading_and_trailing.md"
    )


def test_sanitize_filename_multiple_underscores(dissector_instance):
    assert dissector_instance._sanitize_filename("test___name") == "test_name.md"
    assert dissector_instance._sanitize_filename("_test_name_") == "test_name.md"


@patch("dissector.ChatCompletionsClient")
def test_get_response_success(mock_chat_client, dissector_instance):
    mock_client = mock_chat_client.return_value
    dissector_instance._client = mock_client

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "# Test Title\nTest content"
    mock_client.complete.return_value = mock_response

    response_content = dissector_instance.get_response()
    assert response_content == "# Test Title\nTest content"
    mock_client.complete.assert_called_once()
    call_args = mock_client.complete.call_args
    assert call_args[1]["model"] == "openai/gpt-4o"
    messages = call_args[1]["messages"]

    expected_system_message = (
        "You are a helpful assistant that transforms "
        "handwritten images in Markdown files."
    )
    assert messages[0].content == expected_system_message

    expected_user_message = (
        "Give to me a Markdown of this text on the image and only this."
        "Add a title for it, that must be the first line of the response ."
        "Do not describe the image."
    )
    assert messages[1].content[0].text == expected_user_message

    # Verify that image content was passed correctly
    # Check that the structure exists without assuming specific attribute names
    assert len(messages[1].content) >= 2  # At least text and image items
    assert hasattr(messages[1].content[1], "image_url")  # Has image_url property


@patch("dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_with_derived_filename(
    mock_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    mock_get_response.return_value = "# My Awesome Title\nThis is the content."

    title_from_first_line = "My Awesome Title"
    expected_filename = dissector_instance._sanitize_filename(title_from_first_line)
    expected_dest_path = "/custom/output"
    expected_full_path = os.path.join(expected_dest_path, expected_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename="fallback.md"
    )

    assert actual_path == expected_full_path
    mock_makedirs.assert_called_once_with(expected_dest_path, exist_ok=True)
    mock_file_open.assert_called_once_with(expected_full_path, "w")
    mock_file_open().write.assert_called_once_with(
        "# My Awesome Title\nThis is the content."
    )


@patch("dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_with_fallback_filename(
    mock_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    mock_get_response.return_value = ""

    fallback_filename = "response.md"
    expected_dest_path = "./output_dir"
    expected_full_path = os.path.join(expected_dest_path, fallback_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename=fallback_filename
    )

    assert actual_path == expected_full_path
    mock_makedirs.assert_called_once_with(expected_dest_path, exist_ok=True)
    mock_file_open.assert_called_once_with(expected_full_path, "w")
    mock_file_open().write.assert_called_once_with("")


@patch("dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_no_content_uses_fallback(
    mock_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    mock_get_response.return_value = None  # Simulate no content

    fallback_filename = "fallback_name.md"
    expected_dest_path = "test_output"
    expected_full_path = os.path.join(expected_dest_path, fallback_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename=fallback_filename
    )

    assert actual_path == expected_full_path
    mock_makedirs.assert_called_once_with(expected_dest_path, exist_ok=True)
    mock_file_open.assert_called_once_with(expected_full_path, "w")
    mock_file_open().write.assert_called_once_with("")


@patch("dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_title_with_only_special_chars_uses_fallback(
    mock_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    mock_get_response.return_value = "# !@#\nContent"

    original_sanitize = dissector_instance._sanitize_filename

    def patched_sanitize(name):
        if name.strip() == "!@#":
            return ""
        return original_sanitize(name)

    with patch.object(
        dissector_instance, "_sanitize_filename", side_effect=patched_sanitize
    ):
        fallback_filename = "special_fallback.md"
        expected_dest_path = "output"
        expected_full_path = os.path.join(expected_dest_path, fallback_filename)

        actual_path = dissector_instance.write_response(
            dest_path=expected_dest_path, fallback_filename=fallback_filename
        )

        assert actual_path == expected_full_path
        mock_makedirs.assert_called_once_with(expected_dest_path, exist_ok=True)
        mock_file_open.assert_called_once_with(expected_full_path, "w")
        mock_file_open().write.assert_called_once_with("# !@#\nContent")
