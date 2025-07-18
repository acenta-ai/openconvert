<div align="center">

# 🔄 OpenConvert CLI

### *Intelligent File Conversion for the Distributed Age*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![OpenAgents](https://img.shields.io/badge/powered%20by-OpenAgents-orange.svg)](https://github.com/openagents/openagents)

*Transform any file to any format using distributed AI agents*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-usage) • [🤝 Contributing](#-contributing) • [💬 Community](#-community)

</div>

---

## 🌟 **What is OpenConvert?**

OpenConvert CLI is a command-line tool that connects to distributed OpenAgents networks to discover and utilize file conversion services. Instead of installing multiple conversion tools, OpenConvert leverages distributed agents to handle various file conversion tasks.

### ✅ **Currently Implemented**

🔗 **Network-Powered** • Connect to OpenAgents conversion networks  
🤖 **Prompt Support** • Use natural language prompts (agent-dependent)  
📁 **Batch Processing** • Convert files and directories  
🔍 **Auto-Detection** • Automatic MIME type detection  
🛡️ **Error Handling** • Comprehensive error reporting  
⚡ **Async Operations** • Non-blocking network operations  
🔧 **Python API** • Import and use `from openconvert import convert`  
📊 **Format Discovery** • `--list-formats` to see available conversions  

### 🚧 **Planned Features**

🚀 **Enhanced Format Support** • Expand to 50+ formats as agents join  
🐳 **Easy Deployment** • Docker and Kubernetes support  
⚙️ **Configuration Files** • YAML config for defaults and preferences  

---

## 🎬 **See It In Action**

```bash
# Convert a document with AI enhancement
openconvert -i data.csv -o report.pdf --prompt "Create a professional report with charts"

# Batch convert an entire photo library
openconvert -i photos/ -o pdfs/ --from image/jpeg --to application/pdf

# Simple format conversion
openconvert -i document.txt -o document.pdf

# Discover available conversions
openconvert --list-formats
```

> 💡 **Pro Tip**: Use natural language prompts to guide conversions (depends on agent capabilities)!

---

## 🚀 **Quick Start**

### Installation

```bash
# Currently: Install from source
git clone https://github.com/openagents/openconvert.git
cd openconvert
pip install -e .

# Future: PyPI package (planned)
# pip install openconvert
```

### Your First Conversion

```bash
# Start an OpenConvert network (one-time setup)
openagents launch-network demos/openconvert/network_config.yaml

# Launch some conversion agents
python demos/openconvert/run_agent.py doc &
python demos/openconvert/run_agent.py image &

# Convert your first file!
openconvert -i document.txt -o document.pdf
```

That's it! 🎉

> ⚠️ **Current Status**: This is an early-stage project. Basic functionality works, but many advanced features are still in development.

---

## 📖 **Usage**

### **Basic Syntax**

```bash
openconvert -i INPUT -o OUTPUT [OPTIONS]
```

### **Real-World Examples**

<details>
<summary><b>📄 Document Conversions</b></summary>

```bash
# Text to PDF with custom styling
openconvert -i notes.txt -o notes.pdf --prompt "Use a professional layout with headers"

# Markdown to Word document
openconvert -i README.md -o README.docx

# CSV to formatted Excel with charts
openconvert -i sales.csv -o sales.xlsx --prompt "Add charts and formatting"
```
</details>

<details>
<summary><b>🖼️ Image Processing</b></summary>

```bash
# Convert and compress images
openconvert -i photos/ -o thumbnails/ --from image/jpeg --to image/webp --prompt "Resize to 800px width"

# Create PDF from images
openconvert -i scans/ -o document.pdf --from image/png --to application/pdf

# Batch image format conversion
openconvert -i raw_images/ -o processed/ --from image/tiff --to image/png
```
</details>

<details>
<summary><b>🎵 Media Files</b></summary>

```bash
# Audio format conversion
openconvert -i music.wav -o music.mp3 --prompt "High quality encoding"

# Video format conversion
openconvert -i video.avi -o video.mp4 --prompt "Optimize for web streaming"

# Extract audio from video
openconvert -i movie.mp4 -o soundtrack.mp3
```
</details>

<details>
<summary><b>🗂️ Archives & Data</b></summary>

```bash
# Create compressed archives
openconvert -i project/ -o project.zip

# Convert between archive formats
openconvert -i backup.rar -o backup.tar.gz

# JSON to other formats
openconvert -i data.json -o data.xlsx --prompt "Create tables with proper headers"
```
</details>

### **Command-Line Options**

| Option | Description | Example |
|--------|-------------|---------|
| `-i, --input` | Input file or directory | `-i documents/` |
| `-o, --output` | Output file or directory | `-o converted/` |
| `--from` | Source MIME type | `--from image/png` |
| `--to` | Target MIME type | `--to application/pdf` |
| `--prompt` | AI conversion instructions | `--prompt "Compress by 50%"` |
| `--host` | Network host | `--host remote.example.com` |
| `--port` | Network port | `--port 8765` |
| `-v, --verbose` | Detailed output | `-v` |
| `-q, --quiet` | Minimal output | `-q` |
| `--list-formats` | Discover available conversions | `--list-formats` |

---

## 🌐 **Supported Formats**

<div align="center">

| Category | Formats | Count |
|----------|---------|-------|
| **📄 Documents** | txt, pdf, docx, html, md, rtf, csv, xlsx, epub | 9+ |
| **🖼️ Images** | png, jpg, gif, bmp, tiff, svg, webp, ico | 8+ |
| **🎵 Audio** | mp3, wav, ogg, flac, aac, m4a | 6+ |
| **🎬 Video** | mp4, avi, mkv, mov, webm, gif | 6+ |
| **🗜️ Archives** | zip, rar, 7z, tar, gz, bz2 | 6+ |
| **💻 Code** | json, xml, yaml, html, css, js, py | 7+ |
| **🎯 3D Models** | stl, obj, fbx, ply, glb | 5+ |

**Total: 50+ formats supported!**

</div>

> 📈 **Growing Library**: New formats added regularly as agents join the network

---

## 🏗️ **Network Setup**

### **Quick Network Setup**

```bash
# 1. Clone the OpenAgents repository
git clone https://github.com/openagents/openagents.git
cd openagents

# 2. Start the network
openagents launch-network demos/openconvert/network_config.yaml

# 3. Launch conversion agents (in separate terminals)
python demos/openconvert/run_agent.py doc     # Document conversions
python demos/openconvert/run_agent.py image   # Image processing  
python demos/openconvert/run_agent.py audio   # Audio conversions
python demos/openconvert/run_agent.py video   # Video processing
```

### **Production Deployment (Planned)**

> 🚧 **Coming Soon**: Docker and Kubernetes deployment configurations are being developed.
> 
> Currently: Use the manual setup method above for development and testing.

---

## 🔧 **Advanced Usage**

### **Batch Processing Power**

```bash
# Convert all images in a folder structure
find ./photos -name "*.raw" -exec openconvert -i {} -o {}.jpg \;

# Parallel processing with xargs
ls *.txt | xargs -I {} -P 4 openconvert -i {} -o {}.pdf

# Directory-wide conversions
openconvert -i ./documents --from text/plain --to application/pdf --prompt "Professional formatting"
```

### **Python Integration**

```python
# Simple file conversion
from openconvert import convert_file

success = convert_file("document.txt", "document.pdf")
if success:
    print("✅ Conversion successful!")

# Advanced batch conversion
from openconvert import convert
from pathlib import Path

success = convert(
    input_files=[Path("file1.txt"), Path("file2.txt")],
    output_path=Path("merged.pdf"),
    from_format="text/plain",
    to_format="application/pdf",
    prompt="Merge into single document with table of contents"
)

# Advanced async usage (for custom integrations)
from openconvert.client import OpenConvertClient

async def custom_conversion():
    client = OpenConvertClient()
    await client.connect("my-network.com", 8765)
    
    result = await client.convert_file(
        input_file=Path("data.xlsx"),
        output_file=Path("report.pdf"), 
        source_format="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        target_format="application/pdf",
        prompt="Create executive summary with charts"
    )
    
    await client.disconnect()
    return result
```

### **Configuration Files (Planned)**

> 🚧 **Coming Soon**: Configuration file support is planned for future releases.

---

## 🛠️ **Development**

### **Project Structure**

```
openconvert/
├── 📁 openconvert/           # Main package
│   ├── 🐍 __init__.py       # Package init
│   ├── 🖥️ openconvert_cli.py # CLI interface
│   ├── 🌐 client.py         # Network client
│   └── 📄 __main__.py       # Module entry
├── 🧪 tests/                # Test suite
├── 📖 docs/                 # Documentation
├── 🐳 docker/               # Docker configs
├── ⚙️ setup.py              # Installation
└── 📋 README.md             # This file
```

### **Contributing Workflow**

```bash
# 1. Fork & clone
git clone https://github.com/yourusername/openconvert.git
cd openconvert

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Set up development environment
pip install -e ".[dev]"
pre-commit install

# 4. Make changes & test
pytest tests/
black openconvert/
flake8 openconvert/

# 5. Submit PR
git push origin feature/amazing-feature
```

### **Running Tests**

```bash
# Unit tests
pytest tests/

# Integration tests (requires network)
pytest tests/integration/ --network

# Performance tests
pytest tests/performance/ --benchmark

# Coverage report
pytest --cov=openconvert --cov-report=html
```

---

## 🤝 **Contributing**

We ❤️ contributions! Here's how you can help:

### **🐛 Found a Bug?**
- [Open an issue](https://github.com/openagents/openconvert/issues/new?template=bug_report.md)
- Include reproduction steps
- Mention your OS and Python version

### **💡 Have an Idea?**
- [Start a discussion](https://github.com/openagents/openconvert/discussions)
- Propose new features or improvements
- Share your use cases

### **🛠️ Want to Code?**
- Check [good first issues](https://github.com/openagents/openconvert/labels/good%20first%20issue)
- Read our [contributing guide](CONTRIBUTING.md)
- Join our [developer Discord](https://discord.gg/openagents)

### **📝 Improve Documentation?**
- Fix typos or unclear sections
- Add examples and tutorials
- Translate to other languages

---

## 💬 **Community**

<div align="center">

[![Discord](https://img.shields.io/discord/123456789?logo=discord&label=Discord)](https://discord.gg/openagents)
[![Twitter Follow](https://img.shields.io/twitter/follow/openagents?style=social)](https://twitter.com/openagents)
[![GitHub Discussions](https://img.shields.io/github/discussions/openagents/openconvert)](https://github.com/openagents/openconvert/discussions)

</div>

- **💬 Chat**: [Discord Server](https://discord.gg/openagents)
- **🐦 Updates**: [@openagents](https://twitter.com/openagents)
- **💡 Discussions**: [GitHub Discussions](https://github.com/openagents/openconvert/discussions)
- **📧 Email**: hello@openagents.org

---

## 🗺️ **Roadmap**

### **🚀 Coming Soon**

- [ ] **Plugin System** - Custom conversion agents
- [ ] **Web Interface** - Browser-based UI
- [ ] **API Gateway** - REST API for integrations
- [ ] **Cloud Hosting** - Managed OpenConvert service
- [ ] **Mobile Apps** - iOS and Android clients

### **🎯 Long Term**

- [ ] **AI-Generated Agents** - Automatic agent creation
- [ ] **Blockchain Integration** - Decentralized agent rewards
- [ ] **Real-time Collaboration** - Multi-user conversion workflows
- [ ] **Format Prediction** - ML-powered format suggestions

---

## 🏆 **Acknowledgments**

Special thanks to:

- **OpenAgents Team** - For the amazing framework
- **Contributors** - Everyone who helps improve OpenConvert
- **Community** - Users who provide feedback and ideas
- **Dependencies** - All the great open source libraries we use

### **Built With**

- [OpenAgents](https://github.com/openagents/openagents) - Distributed agent framework
- [Click](https://click.palletsprojects.com/) - Command line interface
- [AsyncIO](https://docs.python.org/3/library/asyncio.html) - Asynchronous programming
- [Typer](https://typer.tiangolo.com/) - CLI framework

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[⭐ Star this repo](https://github.com/openagents/openconvert) if you found it helpful!**

Made with ❤️ by the OpenAgents community

*Transforming files, one conversion at a time* 🔄

</div> 