# Handmark

**Handmark** is a Python CLI tool that converts handwritten notes from images into Markdown files. It uses AI to process the images and extract the text.

---

## Features

* Converts images of handwritten notes to Markdown.
* Simple CLI interface.
* Uses Azure AI for image processing.

---

## Installation

```bash
pip install .
```

---

## Usage

To use Handmark, run the following command in your terminal:

```bash
handmark <image_path>
```

Replace `<image_path>` with the path to the image file you want to convert. The output will be saved as `response.md` in the current directory.

### Configure GitHub Token

You can configure the GitHub token using the `conf` subcommand:

```bash
handmark conf
```

This will prompt you to enter your GitHub token, which will be stored for future use.

---

## Example

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


[Link to prova-response.md](prova-response.md)

---

## Development

This project uses `uv` for package management.

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/handmark.git
   cd handmark
   ```

2. Install dependencies:

   ```bash
   uv pip install -e .
   ```

   or

   ```bash
   pip install -e .
   ```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the **MIT License**.

---
