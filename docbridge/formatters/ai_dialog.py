"""
AI Dialog formatter for AI conversation content
"""
from typing import List, Tuple, Dict, Any, Optional
import re


class AIDialogFormatter:
    """
    Formatter for AI dialog content from ChatGPT, Claude, DeepSeek, etc.
    """

    # Platform-specific patterns
    PLATFORM_PATTERNS = {
        'chatgpt': {
            'user_labels': ['You', 'User'],
            'assistant_labels': ['ChatGPT', 'Assistant', 'AI'],
            'patterns': [
                r'^\*\*(You|ChatGPT):\*\*',
                r'^(You|ChatGPT):\s*$',
            ]
        },
        'claude': {
            'user_labels': ['Human', 'User'],
            'assistant_labels': ['Assistant', 'Claude'],
            'patterns': [
                r'^\*\*(Human|Assistant):\*\*',
                r'^(Human|Assistant):\s*$',
            ]
        },
        'deepseek': {
            'user_labels': ['User'],
            'assistant_labels': ['DeepSeek', 'Assistant'],
            'patterns': [
                r'^\*\*(User|DeepSeek):\*\*',
                r'^(User|DeepSeek):\s*$',
            ]
        },
        'gemini': {
            'user_labels': ['User'],
            'assistant_labels': ['Gemini', 'Assistant'],
            'patterns': [
                r'^\*\*(User|Gemini):\*\*',
                r'^(User|Gemini):\s*$',
            ]
        },
    }

    def __init__(self, platform: Optional[str] = None):
        self.platform = platform
        self.user_color = (0, 100, 200)  # Blue
        self.assistant_color = (0, 150, 100)  # Green

    def detect_platform(self, text: str) -> Optional[str]:
        """
        Detect AI platform from text patterns.

        Args:
            text: The text to analyze

        Returns:
            Platform name or None
        """
        for platform, config in self.PLATFORM_PATTERNS.items():
            for pattern in config['patterns']:
                if re.search(pattern, text, re.MULTILINE):
                    return platform
        return None

    def parse_dialog(self, text: str, platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Parse AI dialog into structured format.

        Args:
            text: The dialog text
            platform: Optional platform hint

        Returns:
            List of dialog entries with speaker and content
        """
        if platform is None:
            platform = self.detect_platform(text)

        if platform is None:
            # Try generic parsing
            return self._parse_generic(text)

        config = self.PLATFORM_PATTERNS.get(platform, {})
        user_labels = config.get('user_labels', ['User'])
        assistant_labels = config.get('assistant_labels', ['Assistant'])

        # Build pattern for this platform
        all_labels = user_labels + assistant_labels
        pattern = r'(?:^|\n)\*?\*?(' + '|'.join(all_labels) + r'):\*?\*?\s*\n?'

        parts = re.split(pattern, text)
        dialog = []

        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                speaker = parts[i].strip()
                content = parts[i + 1].strip()

                if content:
                    is_user = speaker in user_labels
                    dialog.append({
                        'speaker': speaker,
                        'content': content,
                        'is_user': is_user,
                        'color': self.user_color if is_user else self.assistant_color,
                    })

        return dialog

    def _parse_generic(self, text: str) -> List[Dict[str, Any]]:
        """Parse dialog using generic patterns."""
        # Common patterns
        generic_pattern = r'(?:^|\n)\*?\*?(User|Assistant|You|AI|Human|Bot):\*?\*?\s*\n?'

        parts = re.split(generic_pattern, text)
        dialog = []

        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                speaker = parts[i].strip()
                content = parts[i + 1].strip()

                if content:
                    is_user = speaker.lower() in ['user', 'you', 'human']
                    dialog.append({
                        'speaker': speaker,
                        'content': content,
                        'is_user': is_user,
                        'color': self.user_color if is_user else self.assistant_color,
                    })

        return dialog

    def format_dialog_entry(self, entry: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Format a dialog entry for display.

        Args:
            entry: Dialog entry dictionary

        Returns:
            List of (text, style) tuples
        """
        segments = []

        # Speaker label
        speaker_text = f"**{entry['speaker']}:** "
        segments.append((speaker_text, {
            'bold': True,
            'color': entry['color'],
        }))

        # Content
        content = entry['content']
        segments.append((content, {
            'color': (0, 0, 0),
        }))

        return segments

    def is_ai_dialog(self, text: str) -> bool:
        """Check if text appears to be an AI dialog."""
        return self.detect_platform(text) is not None

    def get_platform_name(self, platform: str) -> str:
        """Get display name for platform."""
        names = {
            'chatgpt': 'ChatGPT',
            'claude': 'Claude',
            'deepseek': 'DeepSeek',
            'gemini': 'Gemini',
        }
        return names.get(platform, platform.capitalize())
