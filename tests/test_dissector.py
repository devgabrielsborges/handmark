# tests/test_dissector.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
from pathlib import Path

from src.dissector import ImageDissector
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
    TextContentItem,
    ImageContentItem,
)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_token_dissector")


@pytest.fixture
def dummy_image_path():
    image_file = Path("dummy_image_for_dissector.png")
    image_file.write_text("dummy image data")
    yield image_file
    if image_file.exists():
        os.remove(image_file)


@pytest.fixture
def mock_config():
    return {
        "output_formats": {
            "markdown": {
                "system_message_content": "System message for markdown",
                "user_message_content": "User message for markdown",
                "file_extension": ".md",
                "content_type": "text/markdown",
            },
            "json": {
                "system_message_content": "System message for JSON",
                "user_message_content": "User message for JSON",
                "file_extension": ".json",
                "content_type": "application/json",
                "pretty_print": True,
                "ensure_ascii": False,
            },
            "yaml": {
                "system_message_content": "System message for YAML",
                "user_message_content": "User message for YAML",
                "file_extension": ".yaml",
                "content_type": "application/x-yaml",
                "default_flow_style": False,
                "allow_unicode": True,
            },
            "xml": {
                "system_message_content": "System message for XML",
                "user_message_content": "User message for XML",
                "file_extension": ".xml",
                "content_type": "application/xml",
                "encoding": "utf-8",
                "pretty_print": True,
            },
        },
        "default_format": "markdown",
    }


@pytest.fixture
def dissector_instance(dummy_image_path, mock_config):
    with patch("src.dissector.ChatCompletionsClient") as MockClient:
        mock_azure_client_instance = MagicMock()
        MockClient.return_value = mock_azure_client_instance

        with patch("builtins.open", mock_open()):
            with patch("json.load", return_value=mock_config):
                instance = ImageDissector(
                    image_path=str(dummy_image_path), output_format="markdown"
                )
                yield instance


def test_image_dissector_initialization(dissector_instance, dummy_image_path):
    """Test basic initialization of ImageDissector."""
    assert dissector_instance.image_path == str(dummy_image_path)
    assert dissector_instance.image_format == "png"
    assert dissector_instance._token == "test_token_dissector"
    assert dissector_instance.output_format == "markdown"
    assert hasattr(dissector_instance, "_client")
    assert isinstance(dissector_instance._client, MagicMock)


def test_image_dissector_initialization_with_custom_format(
    dummy_image_path, mock_config
):
    """Test initialization with different output formats."""
    formats_to_test = ["json", "yaml", "xml", "markdown"]

    for format_name in formats_to_test:
        with patch("src.dissector.ChatCompletionsClient"):
            with patch("builtins.open", mock_open()):
                with patch("json.load", return_value=mock_config):
                    instance = ImageDissector(
                        image_path=str(dummy_image_path), output_format=format_name
                    )
                    assert instance.output_format == format_name


def test_image_dissector_initialization_invalid_format(dummy_image_path, mock_config):
    """Test initialization with invalid format raises error."""
    with patch("src.dissector.ChatCompletionsClient"):
        with patch("builtins.open", mock_open()):
            with patch("json.load", return_value=mock_config):
                with pytest.raises(ValueError, match="Unknown output format"):
                    ImageDissector(
                        image_path=str(dummy_image_path), output_format="invalid_format"
                    )


def test_image_dissector_initialization_no_token(monkeypatch, dummy_image_path):
    """Test initialization fails without GitHub token."""
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(ValueError, match="GITHUB_TOKEN was not found"):
        ImageDissector(image_path=str(dummy_image_path))


def test_get_file_extension(dissector_instance, mock_config):
    """Test file extension retrieval for different formats."""
    format_extensions = {
        "markdown": ".md",
        "json": ".json",
        "yaml": ".yaml",
        "xml": ".xml",
    }

    for format_name, expected_ext in format_extensions.items():
        dissector_instance.output_format = format_name
        assert dissector_instance._get_file_extension() == expected_ext


def test_sanitize_filename_basic_cases(dissector_instance):
    """Test filename sanitization with basic cases."""
    assert dissector_instance._sanitize_filename("") == ""
    assert dissector_instance._sanitize_filename("   ") == ""
    assert dissector_instance._sanitize_filename("My Test File") == "my_test_file.md"
    assert dissector_instance._sanitize_filename("Another Title!") == "another_title.md"


def test_sanitize_filename_special_characters(dissector_instance):
    """Test filename sanitization with special characters."""
    assert dissector_instance._sanitize_filename("A!@#$%^&*()B") == "a_b.md"
    assert (
        dissector_instance._sanitize_filename(" leading and trailing_ ")
        == "leading_and_trailing.md"
    )


def test_sanitize_filename_multiple_underscores(dissector_instance):
    """Test filename sanitization removes multiple underscores."""
    assert dissector_instance._sanitize_filename("test___name") == "test_name.md"
    assert dissector_instance._sanitize_filename("_test_name_") == "test_name.md"


def test_strip_code_blocks(dissector_instance):
    """Test code block stripping functionality."""
    # Test YAML code block stripping
    yaml_with_blocks = "```yaml\ntitle: Test\ncontent: data\n```"
    yaml_clean = dissector_instance._strip_code_blocks(yaml_with_blocks, "yaml")
    assert yaml_clean == "title: Test\ncontent: data"

    # Test JSON code block stripping
    json_with_blocks = '```json\n{"title": "Test"}\n```'
    json_clean = dissector_instance._strip_code_blocks(json_with_blocks, "json")
    assert json_clean == '{"title": "Test"}'

    # Test content without code blocks
    plain_content = "title: Test\ncontent: data"
    plain_result = dissector_instance._strip_code_blocks(plain_content, "yaml")
    assert plain_result == plain_content


def test_get_response_success(dissector_instance):
    """Test successful response from AI model."""
    mock_response_obj = MagicMock()
    mock_message_obj = MagicMock()
    mock_message_obj.content = "# Test Title\nTest content"
    mock_response_obj.choices = [MagicMock(message=mock_message_obj)]

    dissector_instance._client.complete.return_value = mock_response_obj

    response_content = dissector_instance.get_response()
    assert response_content == "# Test Title\nTest content"

    dissector_instance._client.complete.assert_called_once()


@patch("src.dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_markdown_with_title(
    mock_os_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    """Test writing response with markdown title extraction."""
    mock_get_response.return_value = "# My Awesome Title\nThis is the content."

    expected_filename = "my_awesome_title.md"
    expected_dest_path = "/custom/output_path"
    expected_full_path = os.path.join(expected_dest_path, expected_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename="fallback.md"
    )

    assert actual_path == expected_full_path
    mock_os_makedirs.assert_called_once_with(expected_dest_path, exist_ok=True)
    mock_file_open.assert_called_once_with(expected_full_path, "w", encoding="utf-8")


@patch("src.dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_json_with_title(
    mock_os_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    """Test writing response with JSON title extraction."""
    dissector_instance.output_format = "json"
    mock_get_response.return_value = '{"title": "Test Document", "content": "test"}'

    expected_filename = "test_document.json"
    expected_dest_path = "/test/path"
    expected_full_path = os.path.join(expected_dest_path, expected_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename="fallback.json"
    )

    assert actual_path == expected_full_path


@patch("src.dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_yaml_with_title(
    mock_os_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    """Test writing response with YAML title extraction."""
    dissector_instance.output_format = "yaml"
    mock_get_response.return_value = "title: Test Document\ncontent: test data"

    expected_filename = "test_document.yaml"
    expected_dest_path = "/test/path"
    expected_full_path = os.path.join(expected_dest_path, expected_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename="fallback.yaml"
    )

    assert actual_path == expected_full_path


@patch("src.dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_xml_with_title(
    mock_os_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    """Test writing response with XML title extraction."""
    dissector_instance.output_format = "xml"
    xml_content = (
        "<document><title>Test Document</title><content>test</content></document>"
    )
    mock_get_response.return_value = xml_content

    expected_filename = "test_document.xml"
    expected_dest_path = "/test/path"
    expected_full_path = os.path.join(expected_dest_path, expected_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename="fallback.xml"
    )

    assert actual_path == expected_full_path


@patch("src.dissector.ImageDissector.get_response")
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_write_response_fallback_filename(
    mock_os_makedirs, mock_file_open, mock_get_response, dissector_instance
):
    """Test writing response uses fallback when no title found."""
    mock_get_response.return_value = "Content without title"

    fallback_filename = "fallback.md"
    expected_dest_path = "./output"
    expected_full_path = os.path.join(expected_dest_path, fallback_filename)

    actual_path = dissector_instance.write_response(
        dest_path=expected_dest_path, fallback_filename=fallback_filename
    )

    assert actual_path == expected_full_path
