---
icon: lucide/settings
---

# Configuration

Handmark uses a centralized YAML configuration system that allows extensive customization of AI prompts, output formats, and model settings. This guide explains how to configure Handmark to suit your specific needs.

## Configuration File Location

The main configuration file is located at:

```
<project-root>/config.yaml
```

This file is included with your Handmark installation and controls:

- AI model prompts and behavior
- Output format settings
- Available models and providers
- Default preferences

## Configuration Structure

### Overview

``` yaml
# AI Model Prompts
system_message_content: "..."
user_message_content: "..."

# Output Formats
formats:
  markdown: {...}
  json: {...}
  yaml: {...}
  xml: {...}

# Available Models
available_models:
  - name: "gpt-4o"
    ...
```

## System Message Configuration

The system message defines how the AI interprets and processes your images.

### Default Configuration

``` yaml
system_message_content: |
  You are a highly skilled assistant specialized in converting 
  handwritten images into structured digital documents.
```

### Customization Examples

#### Academic Focus

``` yaml
system_message_content: |
  You are an academic assistant specialized in converting 
  handwritten lecture notes and mathematical content. Pay special 
  attention to:
  - Mathematical notation and equations
  - Citation formats
  - Academic terminology
  - Proper LaTeX formatting
```

#### Business Focus

``` yaml
system_message_content: |
  You are a business assistant specialized in converting 
  handwritten meeting notes and business documents. Focus on:
  - Action items and deadlines
  - Professional terminology
  - Organizational structure
  - Key decisions and outcomes
```

## User Message Configuration

The user message tells the AI exactly what to do with the image.

### Default Configuration

``` yaml
user_message_content: |
  Convert the content of this handwritten image into a structured 
  document. Preserve formatting, mathematics, and structure.
```

### Customization Examples

#### Detailed Formatting

``` yaml
user_message_content: |
  Convert this handwritten image with the following requirements:
  1. Maintain hierarchical structure (headings, subheadings)
  2. Convert math equations to LaTeX format
  3. Preserve lists and bullet points
  4. Extract dates in ISO 8601 format
  5. Identify and highlight action items
```

#### Language-Specific

``` yaml
user_message_content: |
  Convert this Portuguese handwritten content to structured text.
  Maintain original language. Pay attention to:
  - Portuguese accents and diacritics
  - Brazilian vs European Portuguese variations
  - Technical terms in Portuguese
```

## Format Configuration

Each output format has its own configuration section.

### Markdown Format

``` yaml
formats:
  markdown:
    file_extension: ".md"
    content_type: "text/markdown"
    system_message_content: |
      Convert handwritten content to clean Markdown format.
      Use proper heading hierarchy (# ## ###).
      Format code blocks with language specifiers.
      Convert equations to LaTeX ($...$).
    user_message_content: |
      Return only the Markdown content without additional commentary.
```

**Customization options:**

``` yaml
formats:
  markdown:
    # Add custom metadata
    include_metadata: true
    metadata_format: "yaml-frontmatter"
    
    # Enable/disable features
    enable_latex: true
    enable_code_blocks: true
    enable_tables: true
    
    # Heading style
    heading_style: "atx"  # or "setext"
```

### JSON Format

``` yaml
formats:
  json:
    file_extension: ".json"
    content_type: "application/json"
    indent: 2
    ensure_ascii: false
```

**Customization options:**

``` yaml
formats:
  json:
    # Formatting
    indent: 4  # Number of spaces for indentation
    ensure_ascii: false  # Allow UTF-8 characters
    sort_keys: true  # Sort keys alphabetically
    
    # Structure
    include_timestamp: true
    include_metadata: true
    nest_sections: true
```

### YAML Format

``` yaml
formats:
  yaml:
    file_extension: ".yaml"
    content_type: "text/yaml"
    default_flow_style: false
```

**Customization options:**

``` yaml
formats:
  yaml:
    # Formatting
    indent: 2
    width: 80  # Line width for wrapping
    default_flow_style: false
    
    # Features
    allow_unicode: true
    explicit_start: true  # Add --- at start
    explicit_end: false   # Add ... at end
```

### XML Format

``` yaml
formats:
  xml:
    file_extension: ".xml"
    content_type: "application/xml"
    encoding: "UTF-8"
```

**Customization options:**

``` yaml
formats:
  xml:
    # XML Declaration
    include_declaration: true
    encoding: "UTF-8"
    standalone: true
    
    # Formatting
    indent: "  "  # Two spaces
    pretty_print: true
    
    # Schema
    root_element: "document"
    namespace: "http://example.com/handmark"
```

## Model Configuration

Define available AI models and their properties.

### Azure AI Models

``` yaml
available_models:
  - name: "gpt-4o"
    pretty_name: "GPT-4o"
    provider: "Azure OpenAI"
    rate_limit: "10000 requests/day"
    description: "Best overall accuracy for complex content"
    capabilities:
      - "vision"
      - "text-generation"
      - "math-notation"
    
  - name: "Phi-3.5-vision-instruct"
    pretty_name: "Phi-3.5 Vision"
    provider: "Azure OpenAI"
    rate_limit: "15000 requests/day"
    description: "Fast and efficient for general content"
```

### Ollama Models

``` yaml
available_models:
  - name: "llama3.2-vision"
    pretty_name: "Llama 3.2 Vision"
    provider: "Ollama"
    local: true
    description: "Local processing, no internet required"
    requirements:
      - "ollama >= 0.1.0"
      - "RAM >= 8GB"
      - "GPU recommended"
```

### Adding Custom Models

To add your own model:

``` yaml
available_models:
  - name: "custom-model-name"
    pretty_name: "My Custom Model"
    provider: "Custom Provider"
    endpoint: "https://api.custom-provider.com/v1"
    api_key_env: "CUSTOM_API_KEY"  # Environment variable name
    rate_limit: "5000 requests/day"
    description: "Custom model description"
```

## Environment Variables

Sensitive configuration can be stored in environment variables.

### .env File

Create a `.env` file in your project root:

```bash
# Azure AI / GitHub Token
GITHUB_TOKEN=your_github_token_here

# Custom API Keys
CUSTOM_API_KEY=your_custom_key_here

# Advanced Settings
HANDMARK_LOG_LEVEL=INFO
HANDMARK_TIMEOUT=30
HANDMARK_MAX_RETRIES=3
```

!!! danger "Security Warning"
    Never commit `.env` files to version control! Add to `.gitignore`:
    
    ```
    .env
    .env.*
    *.env
    ```

### Supported Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | Authentication token for Azure AI | None |
| `HANDMARK_LOG_LEVEL` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) | INFO |
| `HANDMARK_TIMEOUT` | Request timeout in seconds | 30 |
| `HANDMARK_MAX_RETRIES` | Maximum retry attempts | 3 |
| `HANDMARK_OUTPUT_DIR` | Default output directory | Current directory |
| `HANDMARK_DEFAULT_FORMAT` | Default output format | markdown |

## Advanced Configuration

### Rate Limiting

Configure rate limiting to avoid API throttling:

``` yaml
rate_limiting:
  enabled: true
  max_requests_per_minute: 60
  max_requests_per_hour: 1000
  backoff_strategy: "exponential"
  max_backoff_time: 300  # seconds
```

### Caching

Enable caching to avoid reprocessing identical images:

``` yaml
caching:
  enabled: true
  cache_dir: ".handmark_cache"
  max_cache_size_mb: 100
  ttl_hours: 24  # Cache lifetime
  cache_strategy: "hash"  # or "filename"
```

### Logging

Customize logging behavior:

``` yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(levelname)s - %(message)s"
  file: "handmark.log"
  max_size_mb: 10
  backup_count: 5
```

### Timeouts

Configure timeout settings:

``` yaml
timeouts:
  connection: 10  # seconds
  read: 30  # seconds
  upload: 60  # seconds for large images
```

## Configuration Best Practices

### 1. Version Control

Keep a template configuration in version control:

``` yaml
# config.template.yaml
system_message_content: "Default system message"
user_message_content: "Default user message"

# Users copy this to config.yaml and customize
```

### 2. Profile-Based Configuration

Create different profiles for different use cases:

```
config/
├── config.yaml          # Default
├── academic.yaml        # Academic focus
├── business.yaml        # Business focus
└── development.yaml     # Development/testing
```

Load specific profile:

``` bash
HANDMARK_CONFIG=config/academic.yaml handmark digest image.jpg
```

### 3. Validation

Validate your configuration before use:

``` bash
handmark config --validate
```

### 4. Documentation

Document your customizations:

``` yaml
# Custom Configuration for Project X
# Purpose: Academic paper digitization
# Modified: 2025-03-15
# Author: Your Name

system_message_content: |
  Custom message...
```

## Troubleshooting Configuration

### Configuration Not Loading

1. **Check file location**: Ensure `config.yaml` is in the project root
2. **Check YAML syntax**: Use a YAML validator
3. **Check permissions**: Ensure the file is readable

### Invalid Configuration

Run configuration validation:

``` bash
handmark config --validate
```

Common errors:

- Invalid YAML syntax (indentation, special characters)
- Missing required fields
- Invalid model names
- Incorrect data types

### Configuration Changes Not Applied

1. **Restart the application** after configuration changes
2. **Clear cache** if caching is enabled
3. **Check environment variables** that might override settings

## Example Configurations

### Academic Research

``` yaml
system_message_content: |
  You are an academic research assistant. Convert handwritten
  research notes with attention to:
  - Citations and references
  - Mathematical proofs and equations
  - Academic terminology
  - Hypothesis and conclusions

formats:
  markdown:
    enable_latex: true
    citation_format: "apa"
    include_metadata: true
```

### Medical Notes

``` yaml
system_message_content: |
  You are a medical transcription assistant. Convert handwritten
  medical notes with attention to:
  - Medical terminology
  - Dosage and prescriptions
  - Patient information (keep confidential)
  - Dates and timestamps

formats:
  markdown:
    enable_abbreviation_expansion: true
    highlight_medical_terms: true
```

### Software Development

``` yaml
system_message_content: |
  You are a software development assistant. Convert handwritten
  technical notes with attention to:
  - Code snippets and algorithms
  - Technical diagrams
  - API specifications
  - Architecture decisions

formats:
  markdown:
    enable_code_blocks: true
    code_language_detection: true
    preserve_indentation: true
```

## Next Steps

:octicons-question-16: **[Troubleshooting](troubleshooting.md)**
:   Find solutions to common configuration issues

:octicons-terminal-16: **[Usage Guide](usage.md)**
:   Learn how to use your customized configuration

:octicons-book-16: **[API Reference](api.md)**
:   Technical details about configuration options
