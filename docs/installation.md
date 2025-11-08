---
icon: lucide/download
---

# Installation

This guide will help you install Handmark on your system. Handmark is distributed as a Python package and can be installed using various package managers.

## Prerequisites

Before installing Handmark, ensure you have the following:

!!! info "System Requirements"
    - **Python**: Version 3.10 or higher
    - **Package Manager**: `pip` (included with Python) or `uv` (recommended)
    - **GitHub Token**: Required for Azure AI access (can be configured after installation)

### Check Python Version

To verify your Python installation:

=== "macOS / Linux"

    ``` bash
    python3 --version
    ```

=== "Windows"

    ``` bash
    python --version
    ```

!!! tip "Installing Python"
    If you don't have Python installed, visit the [Python website](https://www.python.org/) and follow the [Python Setup and Usage](https://docs.python.org/3/using) instructions for your operating system.

## Installation Methods

### Install with pip

The simplest way to install Handmark is using `pip`, Python's built-in package manager:

=== "macOS / Linux"

    ``` bash
    # Optional: Create a virtual environment (recommended)
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Install Handmark
    pip install handmark
    ```

=== "Windows"

    ``` bash
    # Optional: Create a virtual environment (recommended)
    python -m venv .venv
    .venv\Scripts\activate
    
    # Install Handmark
    pip install handmark
    ```

### Install with uv :material-star:{ .recommended }

If you're developing software using Python, you might be using [uv](https://docs.astral.sh/uv/) as a package manager. To install Handmark with `uv`:

``` bash
# Initialize uv project (if needed)
uv init

# Install Handmark
uv pip install handmark
```

!!! success "Recommended for Developers"
    `uv` is faster and provides better dependency resolution than traditional `pip`. It's becoming the standard in the Python community.

### Install from Source

For development or to get the latest features, you can install directly from the GitHub repository:

``` bash
# Clone the repository
git clone https://github.com/devgabrielsborges/handmark.git
cd handmark

# Install in editable mode
pip install -e .
```

!!! warning "Development Installation"
    Installing from source is intended for developers who want to contribute to Handmark or test unreleased features. For regular usage, install from PyPI using pip or uv.

## Verify Installation

After installation, verify that Handmark is correctly installed:

``` bash
handmark --version
```

You should see output similar to:

```
Handmark version 0.5.0
```

## Next Steps

Now that Handmark is installed, you need to configure authentication:

1. **Configure GitHub Token**: Run `handmark auth` to set up Azure AI access
2. **Select AI Model**: Use `handmark set-model` to choose your preferred AI provider
3. **Process Your First Image**: Try the [Quick Start](quickstart.md) guide

!!! tip "Quick Start"
    Ready to start digitizing your handwritten notes? Check out the [Quick Start Guide](quickstart.md) for a hands-on tutorial.

## Updating Handmark

To update Handmark to the latest version:

=== "pip"

    ``` bash
    pip install --upgrade handmark
    ```

=== "uv"

    ``` bash
    uv pip install --upgrade handmark
    ```

## Uninstalling

To remove Handmark from your system:

=== "pip"

    ``` bash
    pip uninstall handmark
    ```

=== "uv"

    ``` bash
    uv pip uninstall handmark
    ```

## Troubleshooting Installation

### Common Issues

??? question "Permission denied error"
    
    If you encounter a permission error during installation, try one of these solutions:
    
    - **Use a virtual environment** (recommended):
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      pip install handmark
      ```
    
    - **Install for current user only**:
      ```bash
      pip install --user handmark
      ```

??? question "Python version error"
    
    If you see an error about Python version compatibility:
    
    ```
    ERROR: Python 3.10 or higher is required
    ```
    
    You need to upgrade your Python installation. Visit [python.org](https://www.python.org/) to download the latest version.

??? question "Package not found"
    
    If pip cannot find the Handmark package:
    
    - Ensure you have an active internet connection
    - Update pip to the latest version:
      ```bash
      pip install --upgrade pip
      ```
    - Try installing from the test PyPI repository:
      ```bash
      pip install -i https://test.pypi.org/simple/ handmark
      ```

## Getting Help

If you encounter issues during installation:

- Check the [Troubleshooting](troubleshooting.md) guide for common problems
- Search existing [GitHub Issues](https://github.com/devgabrielsborges/handmark/issues)
- Create a new issue with details about your environment and the error message
