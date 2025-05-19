import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
from main import main, handle_conf


@pytest.fixture(autouse=True)
def universal_mocks(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test_token_main")
    monkeypatch.setattr(
        "azure.ai.inference.ChatCompletionsClient.complete", MagicMock()
    )
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_dir, ".env")
    if os.path.exists(env_path):
        os.remove(env_path)
    yield
    if os.path.exists(env_path):
        os.remove(env_path)


@patch("builtins.input", return_value="test_github_token_123")
@patch("builtins.open", new_callable=mock_open)
@patch("builtins.print")
def test_handle_conf_success(mock_print, mock_file_open, mock_input):
    handle_conf()

    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_dir, ".env")

    mock_input.assert_called_once_with("Please enter your GitHub token: ")
    mock_file_open.assert_called_once_with(env_path, "w")

    mock_file_open().write.assert_called_once_with(
        "GITHUB_TOKEN=test_github_token_123\n"  # Real newline, not \\n
    )
    mock_print.assert_any_call(f"Token stored in {env_path}.")
    mock_print.assert_any_call("Configuration complete.")


@patch("builtins.input", return_value="")
@patch("builtins.print")
def test_handle_conf_no_token_provided(mock_print, mock_input):
    handle_conf()
    mock_input.assert_called_once_with("Please enter your GitHub token: ")
    mock_print.assert_any_call("No token provided. Configuration cancelled.")


@patch("builtins.input", return_value="test_token")
@patch("builtins.open", side_effect=OSError("Disk full"))
@patch("builtins.print")
def test_handle_conf_os_error(mock_print, mock_file_open_os_error, mock_input):
    handle_conf()
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_dir, ".env")
    mock_print.assert_any_call(f"Error writing file at {env_path}: Disk full")


@patch("argparse.ArgumentParser.parse_args")
@patch("main.handle_conf")
@patch("sys.exit", side_effect=SystemExit)
def test_main_conf_command(mock_sys_exit, mock_handle_conf, mock_parse_args):
    mock_parse_args.return_value = MagicMock(command="conf", image_path=None)
    with pytest.raises(SystemExit):
        main()
    mock_handle_conf.assert_called_once()
    mock_sys_exit.assert_called_once_with(0)


@patch("argparse.ArgumentParser.parse_args")
@patch("argparse.ArgumentParser.print_help")
@patch("builtins.print")
@patch("sys.exit", side_effect=SystemExit)
def test_main_unknown_command(
    mock_sys_exit, mock_print, mock_print_help, mock_parse_args
):
    mock_parse_args.return_value = MagicMock(command="unknown", image_path=None)
    with pytest.raises(SystemExit):
        main()
    mock_print_help.assert_called_once()
    mock_print.assert_any_call("\nError: Unknown command 'unknown'.")
    mock_sys_exit.assert_called_once_with(1)


@patch("argparse.ArgumentParser.parse_args")
@patch("argparse.ArgumentParser.print_help")
@patch("builtins.print")
@patch("sys.exit", side_effect=SystemExit)
def test_main_no_image_or_command(
    mock_sys_exit, mock_print, mock_print_help, mock_parse_args
):
    mock_parse_args.return_value = MagicMock(command=None, image_path=None)
    with pytest.raises(SystemExit):
        main()
    mock_print_help.assert_called_once()
    error_msg = (
        "\nError: You must provide an image path using --image <path> "
        "or specify a subcommand (e.g., 'conf')."
    )
    mock_print.assert_any_call(error_msg)
    mock_sys_exit.assert_called_once_with(1)


@patch("argparse.ArgumentParser.parse_args")
@patch("os.getenv", return_value=None)  # No env var
@patch("os.path.exists", return_value=False)  # No .env file
@patch("builtins.print")
@patch("sys.exit", side_effect=SystemExit)
def test_main_no_github_token_anywhere(
    mock_sys_exit, mock_print, mock_path_exists, mock_getenv, mock_parse_args
):
    mock_parse_args.return_value = MagicMock(
        command=None, image_path="some_image.png", output="./", filename="out.md"
    )
    with pytest.raises(SystemExit):
        main()

    project_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(os.path.join(__file__, "..", "..", "src", "main.py"))
        )
    )
    dotenv_path = os.path.join(project_dir, ".env")

    error_message = (
        "Error: GITHUB_TOKEN environment variable not set and not found "
        "in project directory."
    )
    guidance_message = (
        f"Please set it, use 'handmark conf', or ensure {dotenv_path} "
        "exists and is readable."
    )
    mock_print.assert_any_call(error_message)
    mock_print.assert_any_call(guidance_message)
    mock_sys_exit.assert_called_once_with(1)


@patch("argparse.ArgumentParser.parse_args")
@patch("os.getenv")
@patch("os.path.exists", return_value=True)
@patch("dotenv.load_dotenv")
@patch("main.ImageDissector")
@patch("builtins.print")
def test_main_token_from_dotenv(
    mock_print,
    mock_image_dissector,
    mock_load_dotenv,
    mock_path_exists,
    mock_getenv,
    mock_parse_args,
):
    # Simulate GITHUB_TOKEN is None initially, then set by load_dotenv
    mock_getenv.side_effect = [None, "token_from_dotenv"]
    mock_parse_args.return_value = MagicMock(
        command=None, image_path="image.jpg", output="out/", filename="file.md"
    )

    mock_dissector_instance = mock_image_dissector.return_value
    mock_dissector_instance.write_response.return_value = "out/file.md"

    # Create a dummy image file to avoid FileNotFoundError
    with open("image.jpg", "w") as f:
        f.write("dummy")

    main()

    mock_load_dotenv.assert_called_once()
    mock_image_dissector.assert_called_once_with(image_path="image.jpg")
    mock_dissector_instance.write_response.assert_called_once_with(
        dest_path=os.path.abspath("out/"), fallback_filename="file.md"
    )
    mock_print.assert_any_call("Response written to out/file.md for image: image.jpg")

    if os.path.exists("image.jpg"):
        os.remove("image.jpg")


@patch("argparse.ArgumentParser.parse_args")
@patch("os.getenv", return_value="env_token_exists")
@patch("main.ImageDissector")
@patch("builtins.print")
def test_main_token_from_env_var_success(
    mock_print, mock_image_dissector, mock_getenv, mock_parse_args
):
    mock_parse_args.return_value = MagicMock(
        command=None, image_path="another.png", output="./", filename="default.md"
    )

    mock_dissector_instance = mock_image_dissector.return_value
    mock_dissector_instance.write_response.return_value = os.path.abspath(
        "./default.md"
    )

    with open("another.png", "w") as f:
        f.write("dummy")

    main()

    mock_image_dissector.assert_called_once_with(image_path="another.png")
    mock_dissector_instance.write_response.assert_called_once_with(
        dest_path=os.path.abspath("./"), fallback_filename="default.md"
    )
    mock_print.assert_any_call(
        f"Response written to {os.path.abspath('./default.md')} for image: another.png"
    )

    if os.path.exists("another.png"):
        os.remove("another.png")


@patch("argparse.ArgumentParser.parse_args")
@patch("os.getenv", return_value="env_token_exists")
@patch("main.ImageDissector")
@patch("builtins.print")
@patch("sys.exit", side_effect=SystemExit)
def test_main_image_not_found(
    mock_sys_exit, mock_print, mock_image_dissector, mock_getenv, mock_parse_args
):
    mock_parse_args.return_value = MagicMock(
        command=None,
        image_path="non_existent_image.jpg",
        output="./",
        filename="out.md",
    )
    mock_image_dissector.side_effect = FileNotFoundError("Image not found")

    with pytest.raises(SystemExit):
        main()

    mock_print.assert_any_call("Error: Image file not found at non_existent_image.jpg")
    mock_sys_exit.assert_called_once_with(1)


@patch("argparse.ArgumentParser.parse_args")
@patch("os.getenv", return_value="env_token_exists")
@patch("main.ImageDissector")
@patch("builtins.print")
@patch("sys.exit", side_effect=SystemExit)
def test_main_general_exception_in_processing(
    mock_sys_exit, mock_print, mock_image_dissector, mock_getenv, mock_parse_args
):
    mock_parse_args.return_value = MagicMock(
        command=None, image_path="image.png", output="./", filename="out.md"
    )
    mock_dissector_instance = mock_image_dissector.return_value
    mock_dissector_instance.write_response.side_effect = Exception(
        "Something went wrong"
    )

    with open("image.png", "w") as f:
        f.write("dummy")

    with pytest.raises(SystemExit):
        main()

    mock_print.assert_any_call("An error occurred: Something went wrong")
    mock_sys_exit.assert_called_once_with(1)

    if os.path.exists("image.png"):
        os.remove("image.png")
