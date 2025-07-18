# OpenConvert CLI Tool

A command-line interface for connecting to the OpenConvert OpenAgents network to discover file conversion services and perform file conversions.

## Overview

OpenConvert CLI allows you to:
- Connect to an OpenConvert OpenAgents network
- Discover available file conversion agents
- Convert files between different formats
- Handle single files or batch convert directories
- Add custom prompts for intelligent conversions

## Installation
### From pip

```bash
pip install openconvert
```


### From Source

1. Navigate to the openconvert tool directory:
```bash
cd tools/openconvert
```

2. Install the package:
```bash
pip install .
```

Or for development:
```bash
pip install -e .
```

### Prerequisites

- Python 3.8 or higher
- Access to an OpenConvert OpenAgents network
- OpenAgents framework (automatically installed as dependency)

## Usage

### Basic Syntax

```bash
openconvert -i INPUT -o OUTPUT [OPTIONS]
```

### Examples

#### Single File Conversion (Auto-detect formats)
```bash
openconvert -i document.txt -o document.pdf
```

#### Directory Conversion with Specific Formats
```bash
openconvert -i images/ -o converted/ --from image/png --to application/pdf
```

#### Conversion with Custom Prompt
```bash
openconvert -i data.csv -o report.pdf --prompt "Create a formatted report with charts"
```

#### Specify Network Connection
```bash
openconvert -i file.doc -o file.md --host remote.server.com --port 8765
```

### Command-Line Options

#### Required Arguments
- `-i, --input`: Input file or directory path
- `-o, --output`: Output file or directory path

#### Optional Arguments
- `--from`: Source MIME type (e.g., 'text/plain', 'image/png'). Auto-detected if not specified.
- `--to`: Target MIME type (e.g., 'application/pdf', 'text/markdown'). Auto-detected from output extension if not specified.
- `--prompt`: Additional instructions for the conversion
- `--host`: OpenConvert network host (default: localhost)
- `--port`: OpenConvert network port (default: 8765)
- `--verbose, -v`: Enable verbose logging
- `--quiet, -q`: Suppress all output except errors

### Supported Formats

The tool supports conversion between various file formats depending on available agents in the network:

#### Documents
- Text: txt, md, html, rtf
- Documents: pdf, docx, epub
- Data: csv, xlsx, json, xml

#### Images  
- Raster: png, jpg, jpeg, bmp, gif, tiff, webp
- Vector: svg
- Output: pdf (for image-to-document conversion)

#### Audio
- Formats: mp3, wav, ogg, flac, aac

#### Video
- Formats: mp4, avi, mkv, mov, webm

#### Archives
- Formats: zip, rar, 7z, tar, gz

#### Code/Markup
- Formats: json, xml, yaml, html, latex

#### 3D Models
- Formats: stl, obj, fbx, ply, glb

*Note: Available conversions depend on the agents connected to your OpenConvert network.*

## Network Setup

### Starting an OpenConvert Network

1. Use the demo network configuration:
```bash
cd demos/openconvert
openagents launch-network network_config.yaml
```

2. Start conversion agents in separate terminals:
```bash
# Image conversion agent
python run_agent.py image

# Document conversion agent  
python run_agent.py doc

# Audio conversion agent
python run_agent.py audio
```

### Custom Network Configuration

Create your own network configuration YAML file based on `demos/openconvert/network_config.yaml` and launch it:

```bash
openagents launch-network your_config.yaml
```

## Advanced Usage

### Batch Processing

Process all PNG files in a directory:
```bash
openconvert -i photos/ -o converted_pdfs/ --from image/png --to application/pdf
```

### Format Auto-Detection

The tool automatically detects file formats based on extensions:
```bash
openconvert -i photo.jpg -o photo.png  # Detects image/jpeg -> image/png
```

### Custom Prompts for AI-Enhanced Conversion

Use prompts to guide intelligent conversion:
```bash
openconvert -i sales_data.csv -o report.pdf --prompt "Create a professional sales report with charts and summary statistics"
```

### Verbose Output

Get detailed information about the conversion process:
```bash
openconvert -i file.txt -o file.pdf --verbose
```

## Error Handling

The tool provides comprehensive error handling:

- **Connection errors**: Clear messages when network is unavailable
- **Format errors**: Helpful suggestions for unsupported conversions  
- **File errors**: Detailed information about file access issues
- **Agent errors**: Information about agent availability and capabilities

## Development

### Project Structure

```
tools/openconvert/
├── __init__.py          # Package initialization
├── openconvert_cli.py   # Main CLI interface
├── client.py           # OpenConvert network client
├── setup.py            # Package setup
└── README.md           # This file
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Troubleshooting

### Common Issues

#### "No agents found for conversion"
- Ensure the OpenConvert network is running
- Check that appropriate conversion agents are connected
- Verify the source and target formats are supported

#### "Failed to connect to network"
- Check network host and port settings
- Ensure the OpenConvert network server is running
- Verify firewall settings allow connections

#### "Input file not found"
- Check file path spelling and permissions
- Ensure the file exists and is readable

### Getting Help

```bash
openconvert --help
```

For more information, see the OpenAgents documentation or visit the project repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 