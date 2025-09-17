"""Basic conversation parser for AI chat exports"""
import re
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ParsedConversation:
    title: str
    content: str
    source: str
    word_count: int

class ConversationParser:
    """Conversation parser class for compatibility with enhanced analyzer"""

    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> ParsedConversation:
        """Parse conversation file and return basic structure"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title from markdown heading
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled Conversation"

        # Basic analysis
        word_count = len(content.split())

        return ParsedConversation(
            title=title,
            content=content,
            source='claude' if 'claude' in content.lower() else 'unknown',
            word_count=word_count
        )

    def parse_content(self, content: str) -> ParsedConversation:
        """Parse conversation content and return basic structure"""
        # Extract title from markdown heading
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled Conversation"

        # Basic analysis
        word_count = len(content.split())

        return ParsedConversation(
            title=title,
            content=content,
            source='claude' if 'claude' in content.lower() else 'unknown',
            word_count=word_count
        )

def parse_file(file_path: str) -> ParsedConversation:
    """Parse conversation file and return basic structure"""
    parser = ConversationParser()
    return parser.parse_file(file_path)
