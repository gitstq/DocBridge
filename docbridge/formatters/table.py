"""
Table formatter for markdown tables
"""
from typing import List, Dict, Any, Optional
import re


class TableFormatter:
    """
    Formatter for markdown tables.
    """

    def __init__(self):
        self.default_alignment = 'left'

    def parse_table(self, table_text: str) -> Dict[str, Any]:
        """
        Parse markdown table into structured data.

        Args:
            table_text: The markdown table text

        Returns:
            Dictionary with headers, rows, and alignments
        """
        lines = table_text.strip().split('\n')

        if len(lines) < 2:
            return {'headers': [], 'rows': [], 'alignments': []}

        # Parse header
        header_line = lines[0]
        headers = self._parse_row(header_line)

        # Parse alignment row
        alignment_line = lines[1] if len(lines) > 1 else ''
        alignments = self._parse_alignments(alignment_line)

        # Parse data rows
        rows = []
        for line in lines[2:]:
            if line.strip() and '|' in line:
                row = self._parse_row(line)
                # Ensure row has same number of columns as headers
                while len(row) < len(headers):
                    row.append('')
                rows.append(row[:len(headers)])

        return {
            'headers': headers,
            'rows': rows,
            'alignments': alignments[:len(headers)] if alignments else ['left'] * len(headers)
        }

    def _parse_row(self, line: str) -> List[str]:
        """Parse a table row into cells."""
        # Remove leading/trailing pipes
        line = line.strip()
        if line.startswith('|'):
            line = line[1:]
        if line.endswith('|'):
            line = line[:-1]

        # Split by pipe and clean up
        cells = [cell.strip() for cell in line.split('|')]
        return cells

    def _parse_alignments(self, line: str) -> List[str]:
        """Parse alignment row."""
        if not line or ':' not in line:
            return []

        cells = self._parse_row(line)
        alignments = []

        for cell in cells:
            cell = cell.strip()
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')

        return alignments

    def format_cell(self, content: str, alignment: str = 'left') -> Dict[str, Any]:
        """
        Format a table cell.

        Args:
            content: Cell content
            alignment: Text alignment (left, center, right)

        Returns:
            Formatted cell dictionary
        """
        return {
            'content': content,
            'alignment': alignment,
            'bold': False,
            'italic': False,
        }

    def is_table_line(self, line: str) -> bool:
        """Check if line is part of a markdown table."""
        if '|' not in line:
            return False

        line = line.strip()
        # Check for separator line
        if re.match(r'^[\|\-\:\s]+$', line):
            return True
        # Check for data line
        if line.startswith('|') or line.endswith('|'):
            return True

        return False

    def merge_tables(self, tables: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple tables into one (if compatible)."""
        if not tables:
            return {'headers': [], 'rows': [], 'alignments': []}

        if len(tables) == 1:
            return tables[0]

        # Use first table's headers and alignments
        merged = {
            'headers': tables[0]['headers'],
            'rows': [],
            'alignments': tables[0]['alignments']
        }

        for table in tables:
            merged['rows'].extend(table['rows'])

        return merged
