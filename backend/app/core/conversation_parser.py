"""Basic conversation parser for AI chat exports"""

import re
from dataclasses import dataclass


@dataclass
class ParsedConversation:
    title: str
    content: str
    source: str
    word_count: int


def parse_file(file_path: str) -> ParsedConversation:
    """Parse conversation file and return basic structure.

    Args:
        file_path: Path to the conversation file

    Returns:
        ParsedConversation: Structured conversation data

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file content is invalid
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Conversation file not found: {file_path}")
    except UnicodeDecodeError:
        raise ValueError("File encoding not supported. Please use UTF-8.")

    if not content.strip():
        raise ValueError("File is empty or contains only whitespace")

    # Extract title from markdown heading
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled Conversation"

    # Basic analysis
    words = content.split()
    word_count = len(words)

    if word_count == 0:
        raise ValueError("No readable content found in file")

    # Determine source based on content
    content_lower = content.lower()
    source = "unknown"
    if "claude" in content_lower:
        source = "claude"
    elif "chatgpt" in content_lower or "gpt" in content_lower:
        source = "chatgpt"
    elif "gemini" in content_lower:
        source = "gemini"
    elif "perplexity" in content_lower:
        source = "perplexity"

    return ParsedConversation(
        title=title,
        content=content,
        source=source,
        word_count=word_count,
    )
