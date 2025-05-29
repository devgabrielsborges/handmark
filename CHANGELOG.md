# Changelog

## [Unreleased]

### Added

- Future improvements will be added here.

## [0.3.3] - 2025-05-29

### Added

- **Model Configuration System**: New `conf` command to configure and select AI models from multiple providers
- **Model Selection Interface**: Interactive model selection with support for Microsoft, OpenAI, and Meta models
- **Persistent Model Configuration**: Model preferences are saved in user configuration directory (`~/.config/handmark/config.json`)
- **Enhanced Model Management**: Support for multiple models including Phi-4-multimodal-instruct, GPT-4.1 variants, Phi-3.5-vision-instruct, and Llama-4 models
- **Version Command**: Added `--version` flag to display current application version
- **Improved Help System**: Enhanced CLI help display with better command documentation
- **Pretty Model Names**: User-friendly model names with provider information and rate limits

### Changed

- **Enhanced CLI Structure**: Improved command organization with clearer help text and better user experience
- **Model Data Structure**: Upgraded Model class to include pretty names, provider information, and rate limits
- **Configuration Management**: Better error handling and validation for model configuration
- **Default Model Fallback**: Automatic fallback to default model (GPT-4o) when no model is configured

### Fixed

- **Entry Point Configuration**: Fixed application entry point in pyproject.toml for proper installation
- **CLI Callback Handling**: Improved main callback function to show help when no command is provided

## [0.3.0] - 2025-05-20

### Added

- Complete CLI interface with `digest` and `auth` commands
- Azure AI integration for image processing via GitHub token authentication
- Automatic title extraction from content for smart file naming
- Markdown formatting for output files
- Smart error handling and user feedback with rich console output
- Detailed documentation and usage examples

### Changed

- Improved project structure with separate modules for image processing, utilities, and CLI
- Enhanced environment variable management with dotenv support
- Better error messages and user guidance for authentication issues

## [0.1.0] - 2025-05-18

### Added

- Added `prova-response.md` for demonstration purposes. (b3b74da)
- Added sample images (`example.png`, `olamundo.jpeg`, `prova.jpeg`) for testing and demonstration. (1feb8ed)
- Initial implementation of `ImageDissector` in `src/dissector.py` and main script `src/main.py` for image processing. (fd4a255)

### Changed

- Updated `.gitignore` to include `.env` and `*.lock` files. (1d0619e)
- Added `.gitignore` to exclude Python-generated files and virtual environments like `__pycache__/`, `*.pyc`, `*.egg-info/`, `build/`, `dist/`, `*.so`, `.env`, `*.lock`, and `venv/`. (4144d24)
