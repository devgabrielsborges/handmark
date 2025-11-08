---
icon: lucide/help-circle
---

# Troubleshooting

This guide helps you diagnose and resolve common issues when using Handmark. If you don't find your issue here, please [open an issue](https://github.com/devgabrielsborges/handmark/issues) on GitHub.

## Quick Diagnostics

Before diving into specific issues, run these diagnostic commands:

``` bash
# Check version
handmark --version

# Check configuration
handmark config

# Check provider status
handmark status

# Test connection
handmark test-connection
```

## Authentication Issues

### Error: GitHub token not configured or invalid

**Symptom:**

```text
Error: GitHub token not configured or invalid
Please run 'handmark auth' to configure authentication
```

**Solution:**

1. Run the authentication setup:

    ``` bash
    handmark auth
    ```

2. Enter a valid GitHub token when prompted
3. Verify the token has appropriate permissions

!!! tip "Getting a GitHub Token"
    Visit [GitHub Settings → Tokens](https://github.com/settings/tokens) to create a new personal access token. Read access is sufficient for Handmark.

### Error: Authentication token expired

**Symptom:**

```text
Error: HTTP 401 - Unauthorized
Authentication token may be expired
```

**Solution:**

1. Generate a new GitHub token
2. Run `handmark auth` again
3. Enter the new token

### Environment Variable Not Found

**Symptom:**

```text
Error: GITHUB_TOKEN environment variable not found
```

**Solution:**

Check if `.env` file exists and contains your token:

``` bash
# View .env file (be careful not to share this!)
cat .env
```

Should contain:

```bash
GITHUB_TOKEN=your_token_here
```

If missing, run `handmark auth` to create it.

## Connection Issues

### Error: Connection timeout

**Symptom:**

```text
HTTPSConnectionPool(host='models.github.ai', port=443): Read timed out
```

**Causes:**

- Slow internet connection
- AI service experiencing high load
- Firewall or proxy blocking connection
- Image too large for processing

**Solutions:**

=== "Solution 1: Retry"

    Wait a few minutes and try again. The service may be temporarily overloaded.

=== "Solution 2: Check Connection"

    ``` bash
    # Test connection
    handmark test-connection
    
    # Check if you can reach the service
    ping models.github.ai
    ```

=== "Solution 3: Use Local Processing"

    Switch to Ollama for offline processing:
    
    ``` bash
    handmark set-model
    # Select an Ollama model
    ```

=== "Solution 4: Reduce Image Size"

    Resize large images before processing:
    
    ``` bash
    # Using ImageMagick
    convert input.jpg -resize 2000x2000\> output.jpg
    
    # Process the smaller image
    handmark digest output.jpg
    ```

### Error: Network unreachable

**Symptom:**

```text
Error: [Errno 101] Network is unreachable
```

**Solution:**

1. Check your internet connection
2. Verify network configuration
3. Check firewall settings
4. Try using a VPN if your network blocks the service
5. Use Ollama for offline processing

### Proxy Configuration

If you're behind a corporate proxy:

``` bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Then run handmark
handmark digest image.jpg
```

## Model Issues

### Error: No model configured

**Symptom:**

```text
Warning: No model configured. Using default model
```

**Solution:**

Select your preferred model:

``` bash
handmark set-model
```

This is a warning, not an error. Handmark will use a default model, but explicitly selecting one is recommended.

### Error: Model not available

**Symptom:**

```text
Error: Selected model 'llama3.2-vision' is not available
Ollama service may not be running or model not installed
```

**Solution for Ollama:**

1. **Install Ollama:**

    Visit [ollama.com](https://ollama.com) and follow installation instructions

2. **Start Ollama service:**

    ``` bash
    # macOS/Linux
    ollama serve
    
    # Check if running
    ollama list
    ```

3. **Pull the model:**

    ``` bash
    ollama pull llama3.2-vision
    ```

4. **Verify installation:**

    ``` bash
    handmark status
    ```

### Error: Model rate limit exceeded

**Symptom:**

```text
Error: HTTP 429 - Too Many Requests
Rate limit exceeded for model
```

**Solution:**

1. **Wait and retry**: Rate limits reset after a period
2. **Switch models**: Try a different model with `handmark set-model`
3. **Use Ollama**: No rate limits for local processing

## Image Issues

### Error: Unsupported image format

**Symptom:**

```text
Error: Unsupported image format: .heic
Supported formats: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp
```

**Solution:**

Convert the image to a supported format:

``` bash
# Using ImageMagick
convert input.heic output.jpg

# Or using Python
pip install pillow
python -c "from PIL import Image; Image.open('input.heic').save('output.jpg')"

# Then process
handmark digest output.jpg
```

### Error: Image file not found

**Symptom:**

```text
Error: Image file not found: path/to/image.jpg
```

**Solution:**

1. **Check file path**: Ensure the path is correct and file exists

    ``` bash
    # List files to verify
    ls -la path/to/
    ```

2. **Use absolute path**: Try using the full path

    ``` bash
    handmark digest /full/path/to/image.jpg
    ```

3. **Check permissions**: Ensure file is readable

    ``` bash
    chmod +r image.jpg
    ```

### Poor Recognition Quality

**Symptom:** Handmark produces inaccurate or incomplete results

**Solutions:**

=== "Improve Image Quality"

    - Use higher resolution (minimum 1200x1600 pixels)
    - Ensure good lighting
    - Avoid shadows and glare
    - Take photo straight-on, not at an angle
    - Use high contrast (dark ink on light paper)

=== "Preprocess Image"

    ``` bash
    # Enhance contrast
    convert input.jpg -contrast-stretch 0 output.jpg
    
    # Remove noise
    convert input.jpg -despeckle output.jpg
    
    # Increase brightness
    convert input.jpg -brightness-contrast 10x20 output.jpg
    ```

=== "Try Different Model"

    ``` bash
    handmark set-model
    # Try GPT-4o for best accuracy
    ```

=== "Crop to Content"

    Remove unnecessary borders and focus on the content area

### Image Too Large

**Symptom:**

```text
Error: Image file size exceeds maximum (10MB)
```

**Solution:**

Reduce image file size:

``` bash
# Reduce quality
convert input.jpg -quality 85 output.jpg

# Resize dimensions
convert input.jpg -resize 2000x2000\> output.jpg

# Both quality and size
convert input.jpg -resize 2000x2000\> -quality 85 output.jpg
```

## Output Issues

### Error: Permission denied writing output

**Symptom:**

```text
Error: [Errno 13] Permission denied: 'output.md'
```

**Solution:**

1. **Check directory permissions:**

    ``` bash
    ls -la output-directory/
    ```

2. **Make directory writable:**

    ``` bash
    chmod u+w output-directory/
    ```

3. **Try different output directory:**

    ``` bash
    handmark digest image.jpg -o ~/Documents/
    ```

### Empty or Invalid Output

**Symptom:** Generated file is empty or contains errors

**Debugging steps:**

1. **Check file contents:**

    ``` bash
    cat output-file.md
    ```

2. **Verify image processing:**

    ``` bash
    handmark test-connection
    handmark status
    ```

3. **Try different format:**

    ``` bash
    # Try JSON for structured output
    handmark digest image.jpg -f json
    ```

4. **Check logs:**

    Enable debug logging:
    
    ``` bash
    export HANDMARK_LOG_LEVEL=DEBUG
    handmark digest image.jpg
    ```

### Filename Issues

**Symptom:** Generated filename contains special characters or is unreadable

**Solution:**

Specify a custom filename:

``` bash
handmark digest image.jpg --filename custom-name.md
```

Or configure title extraction in `config.yaml`.

## Configuration Issues

### Error: Configuration file not found

**Symptom:**

```text
Error: Configuration file 'config.yaml' not found
```

**Solution:**

1. **Check working directory:**

    ``` bash
    pwd
    ls -la | grep config
    ```

2. **Reinstall Handmark:**

    ``` bash
    pip install --force-reinstall handmark
    ```

3. **Create custom config:**

    Copy from template or documentation

### Error: Invalid YAML syntax

**Symptom:**

```text
Error: Error parsing config.yaml at line 15
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solution:**

1. **Validate YAML:**

    Use an online YAML validator or:
    
    ``` bash
    python -c "import yaml; yaml.safe_load(open('config.yaml'))"
    ```

2. **Common YAML issues:**

    - Incorrect indentation (use spaces, not tabs)
    - Missing colons after keys
    - Unquoted special characters
    - Mismatched brackets/quotes

3. **Reset to default:**

    ``` bash
    # Backup your config
    mv config.yaml config.yaml.backup
    
    # Reinstall to get default
    pip install --force-reinstall handmark
    ```

## Platform-Specific Issues

### macOS Issues

#### Gatekeeper Blocking

**Symptom:** macOS prevents Handmark from running

**Solution:**

``` bash
# Allow Handmark to run
xattr -d com.apple.quarantine $(which handmark)
```

#### SSL Certificate Errors

**Solution:**

``` bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Windows Issues

#### Path Length Limit

**Symptom:** Errors with long file paths

**Solution:**

Enable long paths in Windows:

1. Run as Administrator: `gpedit.msc`
2. Navigate to: Local Computer Policy → Computer Configuration → Administrative Templates → System → Filesystem
3. Enable "Enable Win32 long paths"

#### PowerShell Execution Policy

**Symptom:** Cannot run handmark in PowerShell

**Solution:**

``` powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux Issues

#### Missing Dependencies

**Solution:**

``` bash
# Debian/Ubuntu
sudo apt-get install python3-dev python3-pip

# Fedora/RHEL
sudo dnf install python3-devel python3-pip

# Arch
sudo pacman -S python python-pip
```

## Performance Issues

### Slow Processing

**Causes and solutions:**

=== "Large Images"

    Resize images before processing:
    
    ``` bash
    convert input.jpg -resize 2000x2000\> output.jpg
    ```

=== "Slow Internet"

    Use Ollama for local processing:
    
    ``` bash
    handmark set-model
    # Select Ollama model
    ```

=== "Complex Content"

    Complex mathematical notation or tables may take longer. This is normal.

### High Memory Usage

**Solution:**

Process images one at a time, or increase system memory.

## Getting More Help

### Enable Debug Logging

Get detailed information about what's happening:

``` bash
export HANDMARK_LOG_LEVEL=DEBUG
handmark digest image.jpg 2>&1 | tee debug.log
```

Share `debug.log` when reporting issues.

### Collect System Information

When reporting issues, include:

``` bash
# System info
uname -a

# Python version
python --version

# Handmark version
handmark --version

# Handmark status
handmark status

# pip list
pip list | grep handmark
```

### Where to Get Help

:material-github: **GitHub Issues**
:   [github.com/devgabrielsborges/handmark/issues](https://github.com/devgabrielsborges/handmark/issues)
    
    For bugs, feature requests, and technical problems

:material-chat: **Discussions**
:   [github.com/devgabrielsborges/handmark/discussions](https://github.com/devgabrielsborges/handmark/discussions)
    
    For questions, ideas, and community support

:material-book: **Documentation**
:   [Read the full docs](index.md)
    
    Comprehensive guides and references

### Before Reporting an Issue

- [ ] Check this troubleshooting guide
- [ ] Search existing GitHub issues
- [ ] Update to the latest version
- [ ] Try with a simple test image
- [ ] Collect debug logs
- [ ] Document steps to reproduce

### Creating a Good Issue Report

Include:

1. **Handmark version** (`handmark --version`)
2. **Operating system** and version
3. **Python version** (`python --version`)
4. **Complete error message** (with stack trace)
5. **Steps to reproduce** the issue
6. **Expected behavior** vs actual behavior
7. **Sample image** (if applicable and not sensitive)
8. **Debug logs** (`HANDMARK_LOG_LEVEL=DEBUG`)

## Common Error Messages Reference

| Error | Meaning | Quick Fix |
|-------|---------|-----------|
| `GitHub token not configured` | Authentication not set up | Run `handmark auth` |
| `Connection timeout` | Network or service issue | Retry or use Ollama |
| `Unsupported image format` | Image format not supported | Convert to JPG/PNG |
| `Model not available` | Ollama model not installed | Run `ollama pull model-name` |
| `Rate limit exceeded` | Too many requests | Wait or switch models |
| `Permission denied` | File permission issue | Check directory permissions |
| `Configuration file not found` | Missing config.yaml | Reinstall Handmark |
| `Invalid YAML syntax` | Config file error | Validate YAML syntax |

## Next Steps

:octicons-book-16: **[Usage Guide](usage.md)**
:   Learn all commands and options

:octicons-gear-16: **[Configuration](configuration.md)**
:   Customize Handmark behavior

:octicons-home-16: **[Back to Home](index.md)**
:   Return to documentation home
