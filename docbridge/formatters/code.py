"""
Code block formatter with syntax highlighting
"""
from typing import Optional, List, Tuple
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class CodeFormatter:
    """
    Formatter for code blocks with syntax highlighting support.
    """

    def __init__(self, theme: str = "default", show_line_numbers: bool = True):
        self.theme = theme
        self.show_line_numbers = show_line_numbers

    def format_code(self, code: str, language: Optional[str] = None) -> List[Tuple[str, dict]]:
        """
        Format code into styled segments.

        Args:
            code: The code to format
            language: Programming language (optional)

        Returns:
            List of (text, style_dict) tuples
        """
        lines = code.split('\n')
        formatted_lines = []

        for i, line in enumerate(lines, 1):
            segments = []

            # Add line number if enabled
            if self.show_line_numbers:
                segments.append((f"{i:4d} | ", {'color': (150, 150, 150), 'font_name': 'mono'}))

            # Add code content
            segments.append((line, {'font_name': 'mono'}))
            formatted_lines.append(segments)

        return formatted_lines

    def highlight_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Highlight code using Pygments.

        Args:
            code: The code to highlight
            language: Programming language

        Returns:
            HTML formatted code
        """
        try:
            if language:
                lexer = get_lexer_by_name(language)
            else:
                lexer = guess_lexer(code)
        except ClassNotFound:
            lexer = get_lexer_by_name('text')

        formatter = HtmlFormatter(style=self.theme, linenos=self.show_line_numbers)
        return highlight(code, lexer, formatter)

    def get_language_from_extension(self, filename: str) -> Optional[str]:
        """Get language from file extension."""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'objective-c',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'zsh',
            '.ps1': 'powershell',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.less': 'less',
            '.md': 'markdown',
            '.dockerfile': 'docker',
            '.makefile': 'makefile',
            '.cmake': 'cmake',
            '.vim': 'vim',
            '.lua': 'lua',
            '.perl': 'perl',
            '.pl': 'perl',
        }

        import os
        ext = os.path.splitext(filename)[1].lower()
        return extension_map.get(ext)

    def detect_language(self, code: str) -> str:
        """Try to detect programming language from code."""
        try:
            lexer = guess_lexer(code)
            return lexer.name.lower()
        except ClassNotFound:
            return 'text'
