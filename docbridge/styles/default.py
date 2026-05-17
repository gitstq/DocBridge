"""
Default styles for DocBridge converters
"""
from typing import Dict, Any, Optional


class DefaultStyle:
    """
    Default style configuration for document conversion.
    """

    def __init__(self):
        # Font settings
        self.font_name = "Arial"
        self.font_name_mono = "Courier New"
        self.font_name_cjk = "SimSun"  # For Chinese characters

        # Font sizes (in points)
        self.font_size_normal = 11
        self.font_size_heading1 = 18
        self.font_size_heading2 = 16
        self.font_size_heading3 = 14
        self.font_size_heading4 = 12
        self.font_size_code = 10
        self.font_size_small = 9

        # Colors (RGB tuples)
        self.color_text = (0, 0, 0)
        self.color_heading = (0, 0, 0)
        self.color_code_bg = (245, 245, 245)
        self.color_code_border = (220, 220, 220)
        self.color_link = (0, 0, 255)
        self.color_quote_border = (200, 200, 200)
        self.color_quote_bg = (250, 250, 250)

        # Spacing (in points)
        self.space_paragraph = 12
        self.space_heading1_before = 24
        self.space_heading1_after = 12
        self.space_heading2_before = 20
        self.space_heading2_after = 10
        self.space_code_before = 6
        self.space_code_after = 6
        self.space_table_before = 12
        self.space_table_after = 12

        # Page settings
        self.page_width = 612  # Letter size in points (8.5 inches)
        self.page_height = 792  # Letter size in points (11 inches)
        self.margin_left = 72  # 1 inch
        self.margin_right = 72
        self.margin_top = 72
        self.margin_bottom = 72

        # Code block settings
        self.code_show_line_numbers = True
        self.code_line_number_color = (150, 150, 150)
        self.code_highlight_theme = "default"

        # Table settings
        self.table_border_color = (200, 200, 200)
        self.table_header_bg = (240, 240, 240)
        self.table_cell_padding = 6

        # AI Dialog settings
        self.ai_user_label = "You"
        self.ai_assistant_label = "Assistant"
        self.ai_user_color = (0, 100, 200)
        self.ai_assistant_color = (0, 150, 100)
        self.ai_dialog_indent = 36

    def get_heading_style(self, level: int) -> Dict[str, Any]:
        """Get style dictionary for heading level."""
        styles = {
            1: {
                'font_size': self.font_size_heading1,
                'bold': True,
                'space_before': self.space_heading1_before,
                'space_after': self.space_heading1_after,
            },
            2: {
                'font_size': self.font_size_heading2,
                'bold': True,
                'space_before': self.space_heading2_before,
                'space_after': self.space_heading2_after,
            },
            3: {
                'font_size': self.font_size_heading3,
                'bold': True,
                'space_before': self.space_heading2_before,
                'space_after': self.space_heading2_after // 2,
            },
            4: {
                'font_size': self.font_size_heading4,
                'bold': True,
                'italic': True,
                'space_before': self.space_heading2_before // 2,
                'space_after': self.space_heading2_after // 2,
            },
        }
        return styles.get(level, styles[4])

    def to_dict(self) -> Dict[str, Any]:
        """Convert style to dictionary."""
        return {
            'font_name': self.font_name,
            'font_name_mono': self.font_name_mono,
            'font_name_cjk': self.font_name_cjk,
            'font_size_normal': self.font_size_normal,
            'font_size_heading1': self.font_size_heading1,
            'font_size_heading2': self.font_size_heading2,
            'font_size_heading3': self.font_size_heading3,
            'font_size_heading4': self.font_size_heading4,
            'font_size_code': self.font_size_code,
            'color_text': self.color_text,
            'color_heading': self.color_heading,
            'color_code_bg': self.color_code_bg,
            'color_link': self.color_link,
            'space_paragraph': self.space_paragraph,
            'code_show_line_numbers': self.code_show_line_numbers,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DefaultStyle':
        """Create style from dictionary."""
        style = cls()
        for key, value in data.items():
            if hasattr(style, key):
                setattr(style, key, value)
        return style
