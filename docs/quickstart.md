---
icon: lucide/rocket
---

# Quick Start

Get started with Handmark in just a few minutes! This guide will walk you through the basic workflow of converting handwritten notes into digital documents.

## Prerequisites

Before starting, make sure you have:

- [x] Installed Handmark ([Installation Guide](installation.md))
- [ ] A GitHub token for Azure AI access
- [ ] An image of handwritten notes to process

!!! tip "Don't have a GitHub token yet?"
    Don't worry! The setup process below will guide you through obtaining one.

## Step 1: Configure Authentication

Handmark uses Azure AI services which require a GitHub token for authentication.

``` bash
handmark auth
```

You'll be prompted to enter your GitHub token:

```
Enter your GitHub token (press Enter when done):
```

!!! question "How to get a GitHub token?"
    
    1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
    2. Click "Generate new token (classic)"
    3. Give it a descriptive name (e.g., "Handmark Access")
    4. Select necessary scopes (read access is sufficient)
    5. Click "Generate token" and copy it immediately
    6. Paste it into the Handmark prompt

The token will be securely stored in a `.env` file in your project directory.

## Step 2: Select an AI Model

Choose which AI provider and model you want to use:

``` bash
handmark set-model
```

You'll see an interactive menu:

```
Available models:
1. GPT-4o (Azure OpenAI) [AVAILABLE]
2. Phi-3.5 Vision (Azure OpenAI) [AVAILABLE]
3. Llama 3.2 Vision (Ollama) [REQUIRES INSTALLATION]

Select a model (1-3):
```

!!! tip "Recommended for beginners"
    Start with **GPT-4o** (option 1) for the best results. It provides excellent handwriting recognition and handles complex mathematical notation.

### About AI Providers

=== "Azure AI (Remote)"

    **Pros:**
    
    - High accuracy for complex content
    - No local setup required
    - Handles mathematical notation well
    
    **Cons:**
    
    - Requires internet connection
    - Needs GitHub token authentication

=== "Ollama (Local)"

    **Pros:**
    
    - Completely offline processing
    - No authentication needed
    - Privacy-focused
    
    **Cons:**
    
    - Requires local installation
    - May be slower on older hardware
    - Install from [ollama.com](https://ollama.com)

## Step 3: Process Your First Image

Now you're ready to digitize your handwritten notes!

### Basic Usage

``` bash
handmark digest path/to/your/image.jpg
```

The tool will:

1. :material-upload: Upload your image to the AI service
2. :material-brain: Process the handwritten content
3. :material-text: Extract and format the text
4. :material-file-check: Save it as a Markdown file

### Example with Sample Image

If you cloned the repository, try processing the included sample:

``` bash
handmark digest samples/prova.jpeg
```

![Sample handwritten exam](assets/images/prova.jpeg)

*Sample image: Handwritten mathematics exam in Portuguese*

Expected output:

```
Processing image: samples/prova.jpeg
✓ Image uploaded successfully
✓ Content extracted
✓ Title detected: Primeiro Exercício Escolar - 2025.1
✓ File saved: primeiro-exercicio-escolar-2025-1.md
```

!!! success "Your first document!"
    Open the generated file to see your handwritten notes converted to formatted Markdown with proper LaTeX math equations!

## Step 4: Explore Output Formats

Handmark supports multiple output formats beyond Markdown:

### Markdown (Default)

``` bash
handmark digest image.jpg
```

Perfect for documentation, notes, and blog posts.

### JSON

``` bash
handmark digest image.jpg -f json
```

Structured data format, great for:

- Data processing pipelines
- API integrations
- Database storage

### YAML

``` bash
handmark digest image.jpg -f yaml
```

Human-readable configuration format, ideal for:

- Configuration files
- Structured notes
- Data serialization

### XML

``` bash
handmark digest image.jpg -f xml
```

Enterprise-friendly format for:

- Legacy system integration
- Document management
- Data exchange

## Step 5: Customize Output

### Specify Output Directory

``` bash
handmark digest image.jpg -o ./my-notes
```

### Custom Filename

``` bash
handmark digest image.jpg --filename lecture-notes-01.md
```

### Combine Options

``` bash
handmark digest image.jpg -o ./structured-data -f json --filename data.json
```

## Common Workflow Examples

### Processing Academic Notes

``` bash
# Process exam questions
handmark digest exam-questions.jpg -o ./exams

# Process lecture notes with custom name
handmark digest lecture.jpg -o ./lectures --filename calculus-2025-03-15.md
```

### Creating Structured Data

``` bash
# Convert handwritten forms to JSON
handmark digest form.jpg -f json -o ./data

# Convert meeting notes to YAML
handmark digest meeting-notes.jpg -f yaml -o ./meetings
```

### Batch Processing Tips

!!! tip "Processing Multiple Images"
    
    Use shell loops to process multiple images:
    
    === "Bash/Zsh"
    
        ``` bash
        for img in *.jpg; do
            handmark digest "$img" -o ./processed
        done
        ```
    
    === "Fish"
    
        ``` fish
        for img in *.jpg
            handmark digest $img -o ./processed
        end
        ```

## Verification Commands

Check your setup and configuration:

### View Current Configuration

``` bash
handmark config
```

### Check Provider Status

``` bash
handmark status
```

Shows:

- Available AI providers
- Installed models
- Current configuration
- Connection status

### Test Connection

``` bash
handmark test-connection
```

Verifies your authentication and connection to AI services.

## What's Next?

Now that you've completed the quick start, explore more advanced features:

:octicons-terminal-16: **[Usage Guide](usage.md)**
:   Comprehensive reference for all commands and options

:octicons-gear-16: **[Configuration](configuration.md)**
:   Customize prompts, formats, and default settings

:octicons-question-16: **[Troubleshooting](troubleshooting.md)**
:   Solutions to common issues

## Getting Help

Need assistance? Here are your resources:

- :material-book-open-variant: Read the [full documentation](usage.md)
- :material-bug: Report bugs on [GitHub Issues](https://github.com/devgabrielsborges/handmark/issues)
- :material-comment-question: Ask questions in [Discussions](https://github.com/devgabrielsborges/handmark/discussions)
