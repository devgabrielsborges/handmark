---
icon: lucide/terminal
---

# Usage Guide

This comprehensive guide covers all Handmark commands, options, and use cases. Use this as your reference for day-to-day operations.

## Command Overview

Handmark provides several commands to manage your handwriting digitization workflow:

| Command | Description |
|---------|-------------|
| [`handmark digest`](#digest-command) | Convert handwritten images to digital formats |
| [`handmark auth`](#authentication) | Configure GitHub token authentication |
| [`handmark set-model`](#model-selection) | Select and configure AI models |
| [`handmark config`](#configuration) | View current configuration |
| [`handmark status`](#status-check) | Check provider availability and model status |
| [`handmark test-connection`](#test-connection) | Test connection to AI services |
| [`handmark --version`](#version-info) | Display version information |
| [`handmark --help`](#help) | Show help information |

## Digest Command

The `digest` command is the main workhorse of Handmark, converting handwritten images into structured digital documents.

### Basic Syntax

``` bash
handmark digest <image_path> [options]
```

### Arguments

`image_path` (required)
:   Path to the handwritten image file you want to process

### Options

#### `-o, --output <directory>`

Specify the output directory for the generated file.

``` bash
handmark digest notes.jpg -o ./documents
```

!!! note "Default Behavior"
    If not specified, the file is saved in the current directory.

#### `-f, --format <format>`

Choose the output format for your digitized content.

**Available formats:**

- `markdown` (default) - Standard Markdown with LaTeX support
- `json` - Structured JSON format
- `yaml` - YAML configuration format
- `xml` - XML document format

``` bash
# Generate JSON output
handmark digest notes.jpg -f json

# Generate YAML output
handmark digest notes.jpg -f yaml

# Generate XML output
handmark digest notes.jpg -f xml
```

#### `--filename <name>`

Specify a custom filename for the output.

``` bash
handmark digest notes.jpg --filename my-custom-name.md
```

!!! tip "Automatic Title Detection"
    If you don't specify a filename, Handmark automatically extracts a title from the content and uses it for the filename. Special characters are normalized, and the title is converted to a URL-friendly format.

### Complete Examples

#### Example 1: Basic Conversion

![Sample handwritten exam](assets/images/prova.jpeg)

``` bash
handmark digest samples/prova.jpeg
```

**What happens:**

1. Image is processed using the configured AI model
2. Title is automatically extracted: "Primeiro Exercício Escolar - 2025.1"
3. Complex mathematical equations are converted to LaTeX
4. File is saved as: `primeiro-exercicio-escolar-2025-1.md`

#### Example 2: Custom Output Location

``` bash
handmark digest lecture-notes.jpg -o ./course-materials/week-5
```

Saves the output to a specific directory structure.

#### Example 3: JSON for Data Processing

``` bash
handmark digest form-data.jpg -f json -o ./data --filename survey-001.json
```

Perfect for integrating with data pipelines or databases.

#### Example 4: All Options Combined

``` bash
handmark digest meeting-notes.jpg \
    -o ./meetings/2025-03 \
    -f markdown \
    --filename team-meeting-2025-03-15.md
```

### Supported Image Formats

Handmark supports common image formats:

- :material-file-image: JPEG / JPG
- :material-file-image: PNG
- :material-file-image: GIF (static)
- :material-file-image: BMP
- :material-file-image: TIFF
- :material-file-image: WebP

!!! warning "Image Quality"
    For best results, use high-resolution images (at least 1200x1600 pixels) with good lighting and contrast. Avoid blurry or low-contrast images.

### Output Format Details

#### Markdown Format

The default format, perfect for documentation and note-taking.

**Features:**

- Automatic heading detection
- LaTeX math equation support ($...$)
- Proper paragraph formatting
- Code block preservation
- List structure maintenance

**Example output:**

``` markdown
# Meeting Notes - Q1 Planning

## Action Items

1. Review budget proposal
2. Schedule team meeting
3. Update project timeline

## Key Decisions

The team agreed to:

- Prioritize feature X
- Allocate resources to project Y
```

#### JSON Format

Structured data format for programmatic processing.

**Features:**

- Hierarchical structure
- Type-safe values
- Easy parsing in any language
- Database-ready

**Example output:**

``` json
{
  "title": "Meeting Notes - Q1 Planning",
  "sections": [
    {
      "heading": "Action Items",
      "items": [
        "Review budget proposal",
        "Schedule team meeting",
        "Update project timeline"
      ]
    }
  ]
}
```

#### YAML Format

Human-readable configuration format.

**Features:**

- Clean, minimal syntax
- Easy to edit manually
- Configuration-friendly
- Widely supported

**Example output:**

``` yaml
title: Meeting Notes - Q1 Planning
sections:
  - heading: Action Items
    items:
      - Review budget proposal
      - Schedule team meeting
      - Update project timeline
```

#### XML Format

Enterprise-standard format for system integration.

**Features:**

- Schema validation support
- Wide tool support
- Legacy system compatibility
- Structured document format

**Example output:**

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<document>
  <title>Meeting Notes - Q1 Planning</title>
  <section>
    <heading>Action Items</heading>
    <items>
      <item>Review budget proposal</item>
      <item>Schedule team meeting</item>
      <item>Update project timeline</item>
    </items>
  </section>
</document>
```

## Authentication

Configure access to Azure AI services using your GitHub token.

``` bash
handmark auth
```

**Interactive prompt:**

```
Enter your GitHub token (press Enter when done):
[Your token will be hidden]

✓ Token saved successfully to .env file
```

!!! danger "Security Note"
    Your token is stored in `.env` in the project directory. Never commit this file to version control. Add it to your `.gitignore`:
    
    ```
    .env
    .env.*
    ```

### Updating Your Token

To update your token, simply run `handmark auth` again and enter the new token.

### Removing Authentication

To remove stored credentials:

``` bash
rm .env
```

## Model Selection

Choose which AI provider and model to use for processing.

``` bash
handmark set-model
```

**Interactive menu:**

```
Available models:

Azure AI Models (Remote):
  1. GPT-4o                    [AVAILABLE]
  2. Phi-3.5 Vision            [AVAILABLE]

Ollama Models (Local):
  3. Llama 3.2 Vision          [REQUIRES INSTALLATION]
  4. Llava 1.6                 [REQUIRES INSTALLATION]

Select a model (1-4): 
```

### Model Information

#### Azure AI Models

These models run on Microsoft's cloud infrastructure:

**GPT-4o**

- :material-check: Best overall accuracy
- :material-check: Excellent with mathematical notation
- :material-check: Strong handwriting recognition
- :material-minus: Requires internet connection
- :material-minus: Requires GitHub token

**Phi-3.5 Vision**

- :material-check: Good balance of speed and accuracy
- :material-check: Lower latency than GPT-4o
- :material-minus: May struggle with complex equations
- :material-minus: Requires internet connection

#### Ollama Models (Local)

These models run entirely on your local machine:

**Llama 3.2 Vision**

- :material-check: Completely offline
- :material-check: No authentication needed
- :material-check: Privacy-focused
- :material-minus: Requires powerful hardware
- :material-minus: Slower processing

**Installation:**

``` bash
# Install Ollama from ollama.com
# Then pull the model:
ollama pull llama3.2-vision
```

### Checking Current Model

``` bash
handmark config
```

Shows your currently configured model.

## Configuration

View your current Handmark configuration:

``` bash
handmark config
```

**Example output:**

```
Current Configuration:
---------------------
Model: GPT-4o (Azure OpenAI)
Provider: Azure
Output Format: markdown
Config File: /path/to/project/config.yaml
Authentication: Configured ✓
```

## Status Check

Check the availability of AI providers and models:

``` bash
handmark status
```

**Example output:**

```
Provider Status:
---------------

Azure AI:
  Status: Available ✓
  Models: GPT-4o, Phi-3.5 Vision
  Authentication: Valid

Ollama:
  Status: Not installed ✗
  Models: None
  Note: Install from ollama.com

Current Configuration:
  Active Model: GPT-4o
  Provider: Azure AI
```

## Test Connection

Verify connectivity to your configured AI service:

``` bash
handmark test-connection
```

**Success output:**

```
Testing connection to Azure AI...
✓ Connection successful
✓ Authentication valid
✓ Model accessible

Status: Ready to process images
```

**Failure output:**

```
Testing connection to Azure AI...
✗ Connection failed

Error: Invalid authentication token
Solution: Run 'handmark auth' to reconfigure
```

## Version Info

Display the installed Handmark version:

``` bash
handmark --version
```

Output:

```
Handmark version 0.5.0
```

## Help

Display help information for any command:

``` bash
# General help
handmark --help

# Command-specific help
handmark digest --help
handmark auth --help
```

## Advanced Workflows

### Batch Processing

Process multiple images in a directory:

=== "Bash/Zsh"

    ``` bash
    #!/bin/bash
    
    # Process all JPG images in a directory
    for image in ./scans/*.jpg; do
        echo "Processing: $image"
        handmark digest "$image" -o ./processed
    done
    ```

=== "Python Script"

    ``` python
    import subprocess
    from pathlib import Path
    
    # Process all images in directory
    scan_dir = Path("./scans")
    output_dir = Path("./processed")
    
    for image in scan_dir.glob("*.jpg"):
        print(f"Processing: {image}")
        subprocess.run([
            "handmark", "digest", str(image),
            "-o", str(output_dir)
        ])
    ```

### Format Conversion Pipeline

Convert handwritten notes to multiple formats:

``` bash
#!/bin/bash

IMAGE="$1"
BASENAME=$(basename "$IMAGE" | sed 's/\.[^.]*$//')

# Create output directory
mkdir -p "./output/$BASENAME"

# Generate all formats
handmark digest "$IMAGE" -f markdown -o "./output/$BASENAME"
handmark digest "$IMAGE" -f json -o "./output/$BASENAME"
handmark digest "$IMAGE" -f yaml -o "./output/$BASENAME"
handmark digest "$IMAGE" -f xml -o "./output/$BASENAME"

echo "✓ Processed $IMAGE to all formats"
```

### Integration with Git

Track changes to your digitized notes:

``` bash
#!/bin/bash

# Process image
handmark digest "$1" -o ./notes

# Commit to git
cd notes
git add .
git commit -m "Add digitized notes from $(date +%Y-%m-%d)"
git push
```

### Quality Assurance Script

Validate output quality:

``` bash
#!/bin/bash

IMAGE="$1"
OUTPUT_DIR="./validated"

# Process image
handmark digest "$IMAGE" -o "$OUTPUT_DIR"

# Check if file was created
if [ $? -eq 0 ]; then
    echo "✓ Processing successful"
    
    # Check file size (should be > 0)
    LATEST_FILE=$(ls -t "$OUTPUT_DIR"/*.md | head -1)
    FILE_SIZE=$(wc -c < "$LATEST_FILE")
    
    if [ "$FILE_SIZE" -gt 0 ]; then
        echo "✓ Output file is valid (${FILE_SIZE} bytes)"
    else
        echo "✗ Output file is empty"
        exit 1
    fi
else
    echo "✗ Processing failed"
    exit 1
fi
```

## Performance Tips

### Optimizing Image Files

For best performance and accuracy:

1. **Resolution**: Use at least 1200x1600 pixels
2. **Format**: JPEG with 85% quality is optimal
3. **Size**: Keep files under 10MB for faster upload
4. **Preprocessing**: Crop unnecessary borders

### Speed Considerations

**Faster:**

- Smaller images (while maintaining readability)
- Ollama local models (no network latency)
- PNG format (less decoding overhead)

**Slower:**

- Very high resolution images (> 4K)
- Complex mathematical notation
- Multiple pages in one image
- Poor image quality requiring multiple retries

## Next Steps

:octicons-gear-16: **[Configuration](configuration.md)**
:   Learn how to customize Handmark's behavior

:octicons-question-16: **[Troubleshooting](troubleshooting.md)**
:   Find solutions to common issues

:octicons-book-16: **[API Reference](api.md)**
:   Detailed technical documentation
