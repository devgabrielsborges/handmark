# Handmark

**Handmark** is a Python CLI tool that converts handwritten notes from images into Markdown files. It uses Azure AI to process images and extract text, making it easy to digitize handwritten content.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3-blue)](https://github.com/devgabrielsborges/handmark)

---

## Features

* Converts images of handwritten notes to Markdown format
* Intelligent title extraction from content
* Easy-to-use CLI interface
* Uses Azure AI for accurate image processing
* Automatically formats output as valid Markdown

---

## Installation

```bash
pip install handmark
```

You can also install using `uv`:

```bash
uv pip install handmark
```

---

## Usage

Handmark provides a simple CLI with the following commands:

### Process an Image

```bash
handmark digest <image_path> [options]
```

Options:
- `-o, --output <directory>` - Specify output directory (default: current directory)
- `--filename <name>` - Custom output filename (default: response.md)

### Configure Authentication

```bash
handmark auth
```

This will prompt you to enter your GitHub token, which is required for Azure AI integration. The token is securely stored in a `.env` file in the project directory.

### Configure Model

```bash
handmark conf
```

This command lets you select and configure the AI model used for image processing. You can choose from available models, and your selection will be saved for future runs.

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

Leia atentamente todas as questões antes de começar a prova. As respostas obtidas somente terão validade se respondidas nas folhas entregues. Os cálculos podem ser escritos a lápis e em qualquer ordem. Evite usar material eletrônico durante a prova, não sendo permitido o uso de calculadora programável para validá-lo. Não é permitido o uso de celular em sala.

---

1. (2 pontos) Determine a equação do plano tangente à função f(x,y) = √(20 - x² - 7y²) em (2,1). Em seguida, calcule um valor aproximado para f(1.9, 1.1).

2. (2 pontos) Determine a derivada direcional de f(x,y) = (xy)^(1/2) em P(2,2), na direção de Q(5,4).

3. (2 pontos) Determine e classifique os extremos de f(x,y) = x⁴ + y⁴ - 4xy + 2.

4. (2 pontos) Usando integrais duplas, calcule o volume acima de onde z = 0 e abaixo da superfície z = x² + y² + 2.

5. (2 pontos) Sabendo que E é o volume do sólido delimitado pelo cilindro parabólico z = x² + y² e pelo plano z = 1, apresente um esboço deste volume e calcule o valor de E.
```

The output is saved as a Markdown file with a filename derived from the detected title.

[See the full example output](prova-response.md)

---

## Development

### Prerequisites

- Python 3.10 or higher
- A GitHub token for Azure AI integration

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/devgabrielsborges/handmark.git
   cd handmark
   ```

2. Install dependencies:

   ```bash
   pip install -e .
   ```

### Running Tests

```bash
pytest
```

### Project Structure

- `src/` - Source code
  - `main.py` - CLI interface
  - `dissector.py` - Image processing and API interaction
  - `utils.py` - Helper functions
- `samples/` - Sample images for testing
- `tests/` - Unit tests

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Gabriel Borges ([@devgabrielsborges](https://github.com/devgabrielsborges))

---

*Last updated: May 20, 2025*

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the **MIT License**.

---
