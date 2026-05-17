# 🚀 DocBridge

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>Convert Markdown to Office documents with AI dialog support</b><br>
  <b>一键将 Markdown 和 AI 对话转换为 Word、Excel、PowerPoint</b><br>
  <b>一鍵將 Markdown 和 AI 對話轉換為 Word、Excel、PowerPoint</b>
</p>

<p align="center">
  <a href="#english">English</a> •
  <a href="#简体中文">简体中文</a> •
  <a href="#繁體中文">繁體中文</a>
</p>

---

<a name="english"></a>
## 🎉 Introduction

**DocBridge** is a powerful CLI tool that converts Markdown documents to Microsoft Office formats (Word, Excel, PowerPoint) with intelligent AI dialog recognition. Perfect for converting your ChatGPT, Claude, DeepSeek conversations into professional documents.

### ✨ Key Features

- 📝 **Multi-format Support**: Convert Markdown to Word (.docx), Excel (.xlsx), PowerPoint (.pptx)
- 🤖 **AI Dialog Recognition**: Automatically detects and formats AI conversations from ChatGPT, Claude, DeepSeek, Gemini
- 💻 **Code Highlighting**: Preserves syntax highlighting for code blocks
- 📊 **Table Conversion**: Smart Markdown table to Office table conversion
- 🎨 **Custom Styling**: YAML-based style configuration
- 🚀 **Zero Dependencies**: Pure Python implementation with minimal dependencies
- ⚡ **Batch Processing**: Convert multiple files at once
- 🌐 **Cross-platform**: Works on Windows, macOS, and Linux

---

<a name="简体中文"></a>
## 🎉 项目介绍

**DocBridge** 是一款强大的命令行工具，可以将 Markdown 文档转换为 Microsoft Office 格式（Word、Excel、PowerPoint），并智能识别 AI 对话格式。完美适用于将 ChatGPT、Claude、DeepSeek 的对话内容转换为专业文档。

### ✨ 核心特性

- 📝 **多格式支持**：将 Markdown 转换为 Word (.docx)、Excel (.xlsx)、PowerPoint (.pptx)
- 🤖 **AI 对话识别**：自动识别并格式化来自 ChatGPT、Claude、DeepSeek、Gemini 的 AI 对话
- 💻 **代码高亮**：保留代码块的语法高亮
- 📊 **表格转换**：智能将 Markdown 表格转换为 Office 表格
- 🎨 **自定义样式**：基于 YAML 的样式配置
- 🚀 **零依赖**：纯 Python 实现，依赖最少
- ⚡ **批量处理**：一次性转换多个文件
- 🌐 **跨平台**：支持 Windows、macOS 和 Linux

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**DocBridge** 是一款強大的命令列工具，可以將 Markdown 文件轉換為 Microsoft Office 格式（Word、Excel、PowerPoint），並智慧識別 AI 對話格式。完美適用於將 ChatGPT、Claude、DeepSeek 的對話內容轉換為專業文件。

### ✨ 核心特性

- 📝 **多格式支援**：將 Markdown 轉換為 Word (.docx)、Excel (.xlsx)、PowerPoint (.pptx)
- 🤖 **AI 對話識別**：自動識別並格式化來自 ChatGPT、Claude、DeepSeek、Gemini 的 AI 對話
- 💻 **程式碼高亮**：保留程式碼區塊的語法高亮
- 📊 **表格轉換**：智慧將 Markdown 表格轉換為 Office 表格
- 🎨 **自訂樣式**：基於 YAML 的樣式配置
- 🚀 **零依賴**：純 Python 實現，依賴最少
- ⚡ **批次處理**：一次性轉換多個檔案
- 🌐 **跨平台**：支援 Windows、macOS 和 Linux

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install docbridge

# Or install from source
git clone https://github.com/gitstq/DocBridge.git
cd DocBridge
pip install -e .
```

### Basic Usage

```bash
# Convert to Word (default)
docbridge convert input.md

# Convert to specific format
docbridge convert input.md -f docx
docbridge convert input.md -f xlsx
docbridge convert input.md -f pptx

# Specify output file
docbridge convert input.md -o output.docx

# Batch convert
docbridge batch *.md -f docx

# Analyze markdown structure
docbridge analyze input.md
```

---

## 📖 Detailed Usage

### Converting AI Dialogs

DocBridge automatically detects AI conversation formats:

```markdown
**You:** Can you explain Python decorators?

**Assistant:** Python decorators are a powerful feature...

**You:** Show me an example

**Assistant:** Here's a simple example:
```python
def my_decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper
```
```

Simply save your AI conversation as a `.md` file and convert:

```bash
docbridge convert conversation.md -o report.docx
```

### Supported Platforms

- ✅ **ChatGPT** - Detects "You:" and "ChatGPT:" patterns
- ✅ **Claude** - Detects "Human:" and "Assistant:" patterns
- ✅ **DeepSeek** - Detects "User:" and "DeepSeek:" patterns
- ✅ **Gemini** - Detects "User:" and "Gemini:" patterns

### Custom Styling

Create a `style_config.yaml` file:

```yaml
font_name: "Arial"
font_size_normal: 11
font_size_heading1: 20
color_heading: [0, 0, 0]
code_show_line_numbers: true
```

Apply custom style:

```bash
docbridge convert input.md --style style_config.yaml
```

---

## 💡 Design Philosophy

### Why DocBridge?

1. **Productivity**: Stop manually copying AI conversations into documents
2. **Consistency**: Maintain formatting across different Office applications
3. **Automation**: Batch process multiple files with a single command
4. **Flexibility**: Customizable styles for different use cases

### Technical Highlights

- **Modular Architecture**: Easy to extend with new converters
- **Clean Code**: Well-documented, type-hinted Python code
- **Error Handling**: Graceful handling of edge cases
- **Performance**: Efficient processing of large documents

---

## 📦 Packaging & Deployment

### Build from Source

```bash
# Clone repository
git clone https://github.com/gitstq/DocBridge.git
cd DocBridge

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Build distribution
python setup.py sdist bdist_wheel
```

### Requirements

- Python 3.8+
- python-docx >= 0.8.11
- openpyxl >= 3.0.10
- python-pptx >= 0.6.21

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/DocBridge.git
cd DocBridge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions
- Add tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the need to bridge AI conversations and professional documents
- Built with ❤️ for developers and knowledge workers
- Thanks to the open-source community for the amazing libraries

---

<p align="center">
  Made with ❤️ by the DocBridge Team<br>
  ⭐ Star us on GitHub if you find this useful!
</p>
