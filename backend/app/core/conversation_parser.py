"""
Conversation parser for various AI chat exports
"""
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ConversationMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime] = None

@dataclass
class ParsedConversation:
    title: str
    messages: List[ConversationMessage]
    source: str  # 'claude', 'chatgpt', etc.
    export_date: datetime
    metadata: Dict = None

class ConversationParser:
    """Parse exported AI conversations into structured format"""
    
    def __init__(self):
        self.supported_formats = ['claude_export', 'chatgpt_export']
    
    def parse_claude_export(self, content: str) -> ParsedConversation:
        """Parse Save My Chatbot Claude export format"""
        lines = content.split('\n')
        title = "Untitled Conversation"
        messages = []
        
        # Extract title from first heading
        for line in lines[:10]:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Simple parsing - this will be enhanced
        # For now, just return basic structure
        return ParsedConversation(
            title=title,
            messages=messages,
            source='claude',
            export_date=datetime.now(),
            metadata={}
        )
    
    def parse_file(self, file_path: str) -> ParsedConversation:
        """Parse conversation file and return structured data"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Detect format and parse accordingly
        if 'Claude Chat' in content or 'claude.ai' in content:
            return self.parse_claude_export(content)
        else:
            raise ValueError("Unsupported conversation format")
