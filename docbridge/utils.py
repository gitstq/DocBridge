"""
Utility functions for DocBridge
"""
import re
import os
from typing import Optional, Tuple, List
from urllib.parse import urlparse


def detect_ai_platform(text: str) -> Optional[str]:
    """
    Detect which AI platform the text is from based on dialog patterns.

    Args:
        text: The markdown text to analyze

    Returns:
        Platform name or None if not detected
    """
    patterns = {
        'chatgpt': [
            r'^\*\*You:\*\*',
            r'^\*\*ChatGPT:\*\*',
            r'^You:\s*$',
            r'^ChatGPT:\s*$',
        ],
        'claude': [
            r'^\*\*Human:\*\*',
            r'^\*\*Assistant:\*\*',
            r'^Human:\s*$',
            r'^Assistant:\s*$',
        ],
        'deepseek': [
            r'^\*\*User:\*\*',
            r'^\*\*DeepSeek:\*\*',
            r'^User:\s*$',
            r'^DeepSeek:\s*$',
        ],
        'gemini': [
            r'^\*\*User:\*\*',
            r'^\*\*Gemini:\*\*',
            r'^User:\s*$',
            r'^Gemini:\s*$',
        ],
    }

    for platform, platform_patterns in patterns.items():
        for pattern in platform_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return platform

    return None


def parse_ai_dialog(text: str, platform: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Parse AI dialog into list of (speaker, message) tuples.

    Args:
        text: The dialog text
        platform: Optional platform hint

    Returns:
        List of (speaker, message) tuples
    """
    if platform is None:
        platform = detect_ai_platform(text)

    if platform == 'chatgpt':
        pattern = r'(?:^|\n)\*?\*?(You|ChatGPT):\*?\*?\s*\n?'
    elif platform == 'claude':
        pattern = r'(?:^|\n)\*?\*?(Human|Assistant):\*?\*?\s*\n?'
    elif platform == 'deepseek':
        pattern = r'(?:^|\n)\*?\*?(User|DeepSeek):\*?\*?\s*\n?'
    elif platform == 'gemini':
        pattern = r'(?:^|\n)\*?\*?(User|Gemini):\*?\*?\s*\n?'
    else:
        # Generic pattern
        pattern = r'(?:^|\n)\*?\*?(User|Assistant|You|AI|Human|Bot):\*?\*?\s*\n?'

    parts = re.split(pattern, text)
    dialog = []

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            speaker = parts[i].strip()
            message = parts[i + 1].strip()
            if message:
                dialog.append((speaker, message))

    return dialog


def is_url(path: str) -> bool:
    """Check if path is a URL."""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_file_extension(path: str) -> str:
    """Get file extension from path."""
    return os.path.splitext(path)[1].lower()


def ensure_extension(path: str, extension: str) -> str:
    """Ensure path has the given extension."""
    if not path.lower().endswith(extension.lower()):
        path += extension
    return path


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for filesystem compatibility."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_code_language(code_block: str) -> Tuple[str, str]:
    """
    Extract language from code block.

    Args:
        code_block: The code block content

    Returns:
        Tuple of (language, code)
    """
    lines = code_block.split('\n')
    if lines and lines[0].startswith('```'):
        lang = lines[0][3:].strip()
        code = '\n'.join(lines[1:-1]) if len(lines) > 2 else ''
        return lang, code
    return '', code_block


def is_markdown_table(line: str) -> bool:
    """Check if line is part of a markdown table."""
    return '|' in line and line.strip().startswith('|')


def parse_markdown_table(table_text: str) -> List[List[str]]:
    """
    Parse markdown table text into 2D list.

    Args:
        table_text: The markdown table text

    Returns:
        2D list of cell values
    """
    lines = table_text.strip().split('\n')
    rows = []

    for line in lines:
        if '|' not in line:
            continue
        # Skip separator lines
        if re.match(r'^[\|\-\:\s]+$', line.strip()):
            continue
        # Parse cells
        cells = [cell.strip() for cell in line.split('|')]
        # Remove empty cells from start/end
        cells = [c for c in cells if c or c == '']
        if cells:
            rows.append(cells)

    return rows


def count_markdown_elements(text: str) -> dict:
    """
    Count various markdown elements in text.

    Returns:
        Dictionary with element counts
    """
    return {
        'headings': len(re.findall(r'^#{1,6}\s', text, re.MULTILINE)),
        'code_blocks': len(re.findall(r'```[\s\S]*?```', text)),
        'inline_code': len(re.findall(r'`[^`]+`', text)),
        'tables': len(re.findall(r'\|.*\|.*\n\|[-:\|\s]+\|', text)),
        'links': len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)),
        'images': len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text)),
        'bold': len(re.findall(r'\*\*[^*]+\*\*|__[^_]+__', text)),
        'italic': len(re.findall(r'\*[^*]+\*|_[^_]+_', text)),
    }
