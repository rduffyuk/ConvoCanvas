"""Basic tests to ensure CI pipeline passes."""

import pytest
from app.core.conversation_parser import parse_file, ParsedConversation
import tempfile
import os


def test_parse_file_basic():
    """Test basic file parsing functionality."""
    content = "# Test Conversation\n\nThis is a test conversation with Claude."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        result = parse_file(tmp_file_path)
        assert isinstance(result, ParsedConversation)
        assert result.title == "Test Conversation"
        assert result.source == "claude"
        assert result.word_count > 0
    finally:
        os.unlink(tmp_file_path)


def test_parse_file_empty():
    """Test parsing empty file raises ValueError."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
        tmp_file.write("")
        tmp_file_path = tmp_file.name
    
    try:
        with pytest.raises(ValueError, match="File is empty"):
            parse_file(tmp_file_path)
    finally:
        os.unlink(tmp_file_path)


def test_parse_file_no_title():
    """Test parsing file without markdown title."""
    content = "This is a conversation without a title."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        result = parse_file(tmp_file_path)
        assert result.title == "Untitled Conversation"
        assert result.word_count > 0
    finally:
        os.unlink(tmp_file_path)