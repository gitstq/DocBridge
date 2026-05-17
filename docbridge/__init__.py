"""
DocBridge - Markdown to Office Document Converter

Convert Markdown to Word, Excel, and PowerPoint with AI dialog support.

Example:
    >>> from docbridge import WordConverter
    >>> converter = WordConverter()
    >>> converter.convert_file("input.md", "output.docx")
"""

__version__ = "1.0.0"
__author__ = "DocBridge Team"
__license__ = "MIT"

from .converters.word import WordConverter
from .converters.excel import ExcelConverter
from .converters.powerpoint import PowerPointConverter

__all__ = [
    "WordConverter",
    "ExcelConverter",
    "PowerPointConverter",
    "__version__",
]
