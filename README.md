# Handmark

**Handmark** is a Python CLI tool that converts handwritten notes from images into Markdown files. It uses Azure AI to process images and extract text, making it easy to digitize handwritten content.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3.2.1-blue)](https://github.com/devgabrielsborges/handmark)

---

## Features

* 🖼️ **Image to Markdown Conversion** - Transform handwritten notes from images into clean, formatted Markdown
* 🧠 **Intelligent Title Extraction** - Automatically detects and extracts titles from content for smart file naming
* ⚡ **Easy CLI Interface** - Simple, intuitive commands with rich console output and error handling
* 🤖 **Azure AI Integration** - Leverages Azure AI models for accurate handwriting recognition
* 🔧 **Model Configuration** - Choose from multiple AI models and save your preferences
* 🔐 **Secure Authentication** - GitHub token-based authentication with secure local storage
* 📁 **Flexible Output** - Customize output directory and filename options

---

## Quick Start

1. **Install Handmark:**
   ```bash
   pip install handmark
   ```

2. **Configure authentication:**
   ```bash
   handmark auth
   ```

3. **Process your first image:**
   ```bash
   handmark digest path/to/your/image.jpg
   ```

That's it! Your handwritten notes will be converted to a Markdown file.

---

## Installation

### Requirements

- Python 3.10 or higher
- A GitHub token (for Azure AI access)

### Install from PyPI

```bash
pip install handmark
```

### Install with uv (recommended)

```bash
uv pip install handmark
```

### Install from source

```bash
git clone https://github.com/devgabrielsborges/handmark.git
cd handmark
pip install -e .
```

---

## Usage

### Getting Started

Before processing images, you need to configure authentication:

```bash
handmark auth
```

This will prompt you to enter your GitHub token, which provides access to Azure AI services.

### Commands Overview

| Command | Description |
|---------|-------------|
| `handmark digest <image>` | Convert handwritten image to Markdown |
| `handmark auth` | Configure GitHub token authentication |
| `handmark conf` | Select and configure AI model |
| `handmark --version` | Show version information |

### Process an Image

```bash
handmark digest <image_path> [options]
```

**Options:**
- `-o, --output <directory>` - Specify output directory (default: current directory)
- `--filename <name>` - Custom output filename (default: response.md)

**Examples:**
```bash
# Basic usage - process image and save to current directory
handmark digest samples/prova.jpeg

# Custom output directory
handmark digest samples/prova.jpeg -o ./notes

# Custom filename
handmark digest samples/prova.jpeg --filename lecture-notes.md

# Both custom directory and filename
handmark digest samples/prova.jpeg -o ./outputs --filename my-notes.md
```

#### Supported Image Formats

Handmark supports common image formats including:
* JPEG/JPG
* PNG
* And other formats supported by Azure AI Vision

### Configure Authentication

```bash
handmark auth
```

This will prompt you to enter your GitHub token, which is required for Azure AI integration. The token is securely stored in a `.env` file in the project directory.

### Configure Model

```bash
handmark conf
```

This command lets you select and configure the AI model used for image processing. You can choose from available Azure AI models, and your selection will be saved for future runs. If no model is configured, the system will use a default model.

### Check Version

```bash
handmark --version
```

---

## Example

Here's a real-world example of Handmark in action:

**Input image** (`samples/prova.jpeg`):

![Handwritten notes example](samples/prova.jpeg)

**Output** (`prova-response.md`):

```markdown
# Primeiro Exercício Escolar - 2025.1
Leia atentamente todas as questões antes de começar a prova. As respostas obtidas somente terão validade se respondidas nas folhas entregues. Os cálculos podem ser escritos à lápis e em qualquer ordem. Evite usar material diferente do que foi apresentado em sala ou justifique o material extra adequadamente para validá-lo. Não é permitido uso de celular ou calculadora.

1. (2 pontos) Determine a equação do plano tangente a função $f(x,y) = \sqrt{20 - x^2 - 7y^2}$ em (2,1). Em seguida, calcule um valor aproximado para $f(1,9 , 1,1)$.
2. (2 pontos) Determine a derivada direcional de $f(x,y) = (xy)^{1/2}$ em $P(2,8)$, na direção de $Q(5,4)$.
3. (2 pontos) Determine e classifique os extremos de $f(x,y) = x^4 + y^4 - 4xy + 2$
4. (2 pontos) Usando integrais duplas, calcule o volume acima do cone $z = (x^2 + y^2)^{1/2}$ e abaixo da esfera $x^2 + y^2 + z^2 = 1$
5. (2 pontos). Sabendo que $E$ é o volume delimitado pelo cilindro parabólico $z = 1 - y^2$, e pelos planos $z = 0$, $x = 1$, $x = -1$, apresente um esboço deste volume e calcule a integral tripla.
$$
\iiint_E x^2e^y dV
$$
```

The output is saved as a Markdown file with a filename derived from the detected title.

[See the full example output](prova-response.md)

---

## Troubleshooting

### Common Issues

**Authentication Error:**
```
Error: GitHub token not configured or invalid
```
**Solution:** Run `handmark auth` to configure your GitHub token.

**Image Format Error:**
```
Error: Unsupported image format
```
**Solution:** Ensure your image is in a supported format (JPEG, PNG, etc.).

**No Model Configured Warning:**
```
No model configured. Using default model
```
**Solution:** Run `handmark conf` to select your preferred AI model.

### Getting Help

- Check the [issues page](https://github.com/devgabrielsborges/handmark/issues) for known problems
- Create a new issue if you encounter a bug
- Use `handmark --help` for command-line help

---

## Development

### Prerequisites

- Python 3.10 or higher
- A GitHub token for Azure AI integration
- `uv` (recommended) or `pip` for package management

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/devgabrielsborges/handmark.git
   cd handmark
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv pip install -e .
   
   # Or using pip
   pip install -e .
   ```

3. **Configure for development:**
   ```bash
   handmark auth  # Configure your GitHub token
   handmark conf  # Select preferred AI model
   ```

### Project Structure

- `src/` - Source code
  - `main.py` - CLI interface and command handlers
  - `dissector.py` - Image processing and Azure AI API interaction
  - `model.py` - AI model management and configuration
  - `utils.py` - Helper functions and utilities
- `samples/` - Sample images for testing and demonstration
- `tests/` - Comprehensive unit tests
- `.github/` - GitHub workflows and project instructions

---

---

## Contributing

Contributions are welcome! Please feel free to:

* Open an issue for bug reports or feature requests
* Submit a pull request with improvements
* Help improve documentation
* Share examples of your handwritten notes processed with Handmark

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

* Gabriel Borges ([@devgabrielsborges](https://github.com/devgabrielsborges))

---

*Last updated: May 29, 2025*
