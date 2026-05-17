"""
Base converter class for DocBridge
"""
from abc import ABC, abstractmethod
from typing import Optional, Union, List
from pathlib import Path

from ..styles.default import DefaultStyle


class BaseConverter(ABC):
    """
    Base class for all document converters.
    """

    def __init__(self, style: Optional[DefaultStyle] = None):
        """
        Initialize converter.

        Args:
            style: Style configuration (uses default if None)
        """
        self.style = style or DefaultStyle()
        self._document = None

    @abstractmethod
    def convert(self, markdown_text: str) -> Union[object, List[object]]:
        """
        Convert markdown text to document.

        Args:
            markdown_text: The markdown text to convert

        Returns:
            Converted document object(s)
        """
        pass

    @abstractmethod
    def convert_file(self, input_path: Union[str, Path],
                     output_path: Optional[Union[str, Path]] = None) -> str:
        """
        Convert markdown file to document file.

        Args:
            input_path: Path to input markdown file
            output_path: Path for output file (optional)

        Returns:
            Path to output file
        """
        pass

    def _read_file(self, path: Union[str, Path]) -> str:
        """Read file content."""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _write_file(self, path: Union[str, Path], content: bytes) -> None:
        """Write file content."""
        with open(path, 'wb') as f:
            f.write(content)

    def _ensure_output_path(self, input_path: Union[str, Path],
                           output_path: Optional[Union[str, Path]],
                           extension: str) -> Path:
        """
        Ensure output path has correct extension.

        Args:
            input_path: Input file path
            output_path: Output file path (optional)
            extension: Required extension

        Returns:
            Validated output path
        """
        if output_path is None:
            input_path = Path(input_path)
            output_path = input_path.with_suffix(extension)
        else:
            output_path = Path(output_path)
            if not output_path.suffix:
                output_path = output_path.with_suffix(extension)

        return output_path

    def set_style(self, style: DefaultStyle) -> None:
        """Set style configuration."""
        self.style = style

    def get_document_info(self) -> dict:
        """Get information about the current document."""
        return {
            'has_document': self._document is not None,
            'style': self.style.to_dict(),
        }
