from dissector import ImageDissector
import sys
import argparse
import os


def handle_conf():
    """Handles the configuration for the GitHub token."""
    print("Configuring GitHub token...")
    raw_token_input = input("Please enter your GitHub token: ")
    if raw_token_input:
        cleaned_token = raw_token_input.strip()

        env_dir = os.path.join(os.path.expanduser("~"), ".config", "handmark")
        env_path = os.path.join(env_dir, ".env")

        try:
            os.makedirs(env_dir, exist_ok=True)
            with open(env_path, "w") as f:
                f.write(f"GITHUB_TOKEN={cleaned_token}\\n")
            print(f"Token stored in {env_path}.")
            print("Please ensure this file is loaded by your shell or application.")
            print("You might need to restart your shell or source the .env file.")
        except OSError as e:
            print(f"Error creating directory or writing file at {env_path}: {e}")
            return
    else:
        print("No token provided. Configuration cancelled.")


def main():
    parser = argparse.ArgumentParser(
        description="Transforms handwritten images into Markdown files.", add_help=True
    )

    parser.add_argument(
        "--image",
        dest="image_path",
        metavar="<image_path>",
        help="Path to the image file to process.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="./",
        help="Directory to save the Markdown file (default: current directory).",
    )
    parser.add_argument(
        "--filename",
        default="response.md",
        help="Name of the output Markdown file (default: response.md).",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="Available Subcommands",
        help="For more help on a subcommand, run `handmark <subcommand> --help`",
        required=False,
        metavar="<command>",
    )

    _ = subparsers.add_parser(
        "conf", help="Configure GitHub token for the application."
    )

    args = parser.parse_args()

    if args.command == "conf":
        handle_conf()
        sys.exit(0)
    elif args.command:
        parser.print_help()
        print(f"\\nError: Unknown command '{args.command}'.")
        sys.exit(1)
    elif args.image_path:
        pass
    else:
        parser.print_help()
        error_msg = (
            "\\nError: You must provide an image path using --image <path> "
            "or specify a subcommand (e.g., 'conf')."
        )
        print(error_msg)
        sys.exit(1)

    github_token_env = os.getenv("GITHUB_TOKEN")
    dotenv_path = os.path.join(os.path.expanduser("~"), ".config", "handmark", ".env")

    if not github_token_env:
        if os.path.exists(dotenv_path):
            from dotenv import load_dotenv

            load_dotenv(dotenv_path)
            github_token_env = os.getenv("GITHUB_TOKEN")

        if not github_token_env:
            error_message = (
                "Error: GITHUB_TOKEN environment variable not set and not found "
                "in default path."
            )
            guidance_message = (
                f"Please set it, use 'handmark conf', or ensure {dotenv_path} "
                "exists and is readable."
            )
            print(error_message)
            print(guidance_message)
            sys.exit(1)

    try:
        sample = ImageDissector(image_path=args.image_path)
        output_dir = os.path.abspath(args.output)

        sample.write_response(dest_path=output_dir, filename=args.filename)

        print(
            f"Response written to {os.path.join(output_dir, args.filename)} "
            f"for image: {args.image_path}"
        )
    except FileNotFoundError:
        print(f"Error: Image file not found at {args.image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
