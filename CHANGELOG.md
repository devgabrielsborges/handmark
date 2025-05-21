# Changelog

## [Unreleased]

### Added

- Future improvements will be added here.

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
